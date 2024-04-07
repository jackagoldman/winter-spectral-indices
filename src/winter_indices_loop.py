import ee
import geemap
import numpy as np
import geopandas as gpd
import pandas as pd

ee.Initialize()
# 
fires = ee.FeatureCollection("users/jandrewgoldman/on-qc-defol");
fire_names = fires.aggregate_array('Fire_ID').getInfo()
qc_fires = ee.FeatureCollection("users/jandrewgoldman/qc-fire-perims-shield-2").filter(ee.Filter.inList('Fire_ID', fire_names))
qc_names = qc_fires.aggregate_array('Fire_ID').getInfo()
on_fires = ee.FeatureCollection("users/jandrewgoldman/Ont_BurnSeverity_Trends/ON_FirePerimeters_85to2020_v0").filter(ee.Filter.inList('Fire_ID', fire_names))
on_names = on_fires.aggregate_array('Fire_ID').getInfo()

# get required columns and add them together
on_fires = on_fires.select('Fire_ID', 'Fire_Year')
qc_fires = qc_fires.select('Fire_ID', 'Fire_Year')

on_qc_fires = on_fires.merge(qc_fires)

fires = on_qc_fires

ls8SR = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2');
ls7SR = ee.ImageCollection('LANDSAT/LE07/C02/T1_L2');
ls5SR = ee.ImageCollection('LANDSAT/LT05/C02/T1_L2');
ls4SR = ee.ImageCollection('LANDSAT/LT04/C02/T1_L2');

#// Map functions across Landsat Collections
ls8 = ls8SR.map(ls8_Indices).map(lsCfmask);

ls7 = ls7SR.map(ls4_7_Indices).map(lsCfmask); 

ls5 = ls5SR.map(ls4_7_Indices).map(lsCfmask); 

ls4 = ls4SR.map(ls4_7_Indices).map(lsCfmask); 
                
# Merge Landsat Collections
lsCol = ee.ImageCollection(ls8.merge(ls7).merge(ls5))

  
fids = fires.aggregate_array('Fire_ID')
 # turn it to python list
fids = fids.getInfo()

# loop through list of fire ids
for j in fids:
name = j


fiya = fires.filterMetadata('Fire_ID', 'equals', name).first();
ft = ee.Feature(fiya)
#get image


fName = ft.get("Fire_ID")
fire = ft
fireBounds = ft.geometry().bounds()
year = ft.get('Fire_Year')
year = ee.String(year)
fireYear = ee.Date(year)
preFireYear = fireYear.advance(-1, 'year')
postFireYear = fireYear.advance(1, 'year')
preFireYearAd = preFireYear.advance(11, 'month')
fireYearAd = fireYear.advance(3, 'month')
postFireYearAd = postFireYear.advance(3, 'month')
fireYearAd2 = fireYear.advance(11, 'month')

preFireIndices = lsCol \
        .filterBounds(fireBounds) \
        .filterDate(preFireYearAd, fireYearAd) \
        .select('nbr') \
        .mean() \
        .rename('preNBR')
        
postFireIndices = lsCol \
        .filterBounds(fireBounds) \
        .filterDate(fireYearAd2, postFireYearAd) \
        .select('nbr') \
        .max() \
        .rename('postNBR')
        
# if there are no keys correspoding to pre or post fire, go to next        
if not get_keys(preFireIndices, fireBounds):
  continue

if not get_keys(postFireIndices, fireBounds):
  continue


# if pixel is 0, go to the next
if return_pixel_count(preFireIndices, fireBounds, "preNBR") == 0:
  continue

if return_pixel_count(postFireIndices, fireBounds, "postNBR") == 0:
  continue
  
fireIndices = preFireIndices.addBands(postFireIndices)

dnbr = fireIndices.expression( "(b('preNBR') - b('postNBR')) * 1000").rename('dnbr').toFloat()

ring  = ft.buffer(180).difference(ft);

offset = ee.Image.constant(ee.Number(dnbr.select('dnbr').reduceRegion(**{'reducer': ee.Reducer.mean(),'geometry': ring.geometry(),'scale': 30,'maxPixels': 1e9}).get('dnbr')))
    
offset = offset.rename('offset').toFloat()

dnbr = dnbr.addBands(offset)

dnbr = dnbr.addBands(fireIndices)


dnbr_offset = dnbr.expression("b('dnbr') - b('offset')") \
          .rename('dnbr_w_offset').toFloat()
          
dnbr_offset = dnbr_offset.addBands(fireIndices).addBands(dnbr.select('dnbr'))


rbr = dnbr_offset.expression("b('dnbr') / (b('preNBR') + 1.001)") \
          .rename('rbr').toFloat().addBands(dnbr_offset) 
          

rbr_offset = rbr.expression("b('dnbr_w_offset') / (b('preNBR') + 1.001)") \
          .rename('rbr_w_offset').toFloat().addBands(rbr)
        
          
rbr_offset = rbr_offset.set('fireID' , ft1.get('Fire_ID'),'fireName' , ft1.get('Fire_Name'), 'fireYear' ,  ft1.get('Fire_Year')) 


task = ee.batch.Export.image.toDrive(**{
  'image': rbr_offset,
  'description': name,
  'folder':'winter_burnIndices_subset',
  'scale': 30,
  'region': fireBounds.getInfo()['coordinates']
  })
# start task
task.start()
