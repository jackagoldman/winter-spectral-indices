
#--------------------       INPUTS       ------------------------------//
# import shapefile with fire polygons as a feature collection - these must have the following standard attributes  
#    as distributed by MTBS:  Fire_ID and Year.
#    Note, we use Fire_ID as unique identifier rather than 'Fire_Name' attribute which has duplicate names for different fires.
 fires = ee.FeatureCollection("users/jandrewgoldman/matched_pairs_fireimg4");

# specify fire severity metrics to create
 bandList = ['rbr', 'preNBR', 'postNBR'];


var startday = 152;
var endday   = 273;



#--------------------    END OF INPUTS   ----------------------------//


#--------------------     PROCESSING     ----------------------------//
#-------- Initialize variables for fire perimeters  -----------------//
# create two lists: one with fire names and the other with fire IDs 
var fireID    = ee.List(fires.aggregate_array('Fire_ID')).getInfo();
var nFires = fireID.length;

#------------------- Image Processing for Fires Begins Here -------------//
# Landsat 5, 7, and 8 Surface Reflectance Tier 1 collections
 ls8SR = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR');
 
 ls7SR = ee.ImageCollection('LANDSAT/LE07/C01/T1_SR');
 ls5SR = ee.ImageCollection('LANDSAT/LT05/C01/T1_SR');
 ls4SR = ee.ImageCollection('LANDSAT/LT04/C01/T1_SR');


# Returns vegetation indices for LS8
def ls8_Indices(lsImage):
  nbr = lsImage.normalizedDifference(['B5', 'B7']).toFloat()
  qa = lsImage.select(['pixel_qa'])
  nbr.addBands([qa]).select([0,1], ['nbr', 'pixel_qa']).copyProperties(lsImage, ['system:time_start'])
  return nbr
  
#// Returns vegetation indices for LS4, LS5 and LS7
 def ls4_7_Indices(lsImage):
   nbr = lsImage.normalizedDifference(['B4', 'B7']).toFloat()
   qa = lsImage.select(['pixel_qa'])
   return nbr.addBands([qa]).select([0,1], ['nbr', 'pixel_qa']).copyProperties(lsImage, ['system:time_start'])
  

# Mask Landsat surface reflectance images
# Creates a mask for clear pixels 
 def lsCfmask(lsImg):
   quality = lsImg.select(['pixel_qa'])
   clear = quality.bitwiseAnd(8).eq(0)
   clear = quality.bitwiseAnd(32).eq(0)
   clear = quality.bitwiseAnd(4).eq(0)
   clear = quality.bitwiseAnd(16).eq(0)
   return lsImg.updateMask(clear).select([0]).copyProperties(lsImg, ['system:time_start'])


#// Map functions across Landsat Collections
ls8 = ls8SR.map(ls8_Indices).map(lsCfmask);

ls7 = ls7SR.map(ls4_7_Indices).map(lsCfmask); 

ls5 = ls5SR.map(ls4_7_Indices).map(lsCfmask); 

ls4 = ls4SR.map(ls4_7_Indices).map(lsCfmask); 
                
# Merge Landsat Collections
lsCol = ee.ImageCollection(ls8.merge(ls7).merge(ls5).merge(ls4));

fire = ee.Feature(fires.first())

indices = ee.ImageCollection(fires.map(indices_function))



task = ee.batch.Export.image.toDrive(**{
    'image': t,
    'description': 'imageToDriveExample',
    'folder':'Example_folder',
    'scale': 30,
    'region': fireBounds.getInfo()['coordinates']
})
task.start()
import time 

while task.active(): 
  print('Polling for task (id: {}).'.format(task.id))
  time.sleep(5)



