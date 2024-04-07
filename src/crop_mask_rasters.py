input_raster = '/Users/jgoldman/Google Drive/My Drive/winter_test_folder/CHA8_2012_1924.tif'
input_shapefile = '/Users/jgoldman/Desktop/OneDrive - University of Toronto/Data/chapter_3/on-qc-defol.shp'





 
  
  out_path = '/Users/jgoldman/Desktop/OneDrive - University of Toronto/Data/chapter_3/winter_bs/defoliated-rasters/'

rasters = shapefile.shape.getData()

import os

    
# read in raster, get matching shapefile, then crop
raster_path = '/Users/jgoldman/Google Drive/My Drive/winter_test_folder/'

def create_mask_from_shapefile(input_shapefile, raster_path, out_path):
"""
this function crops a raster based on a feature in a shapefile which matches the id
takes three arguments:
input_shapefile
raster_path
out_path
"""
#first loop through dir
    with os.scandir(raster_path) as p: # Open the folder containing the rasters as p.
        for raster in p: # Get each raster in the folder.
          with rasterio.open(raster, 'r') as src:
            name = src.name
            name = name.replace('/Users/jgoldman/Google Drive/My Drive/winter_test_folder/', '')
            name = name.replace('.tif', "")
            
            # read in shapefile
            with fiona.open(input_shapefile) as shp:
              for feature in shp:
                  if feature['properties']['Fire_ID'] in name:
                    shape = [feature['geometry']]
                    out_image, out_transform = mask(src, shape, crop=True) # setting all pixels outside of the feature zone to zero
                    out_meta = src.meta
        
                    out_meta.update({"driver": "GTiff",
                    "height": out_image.shape[1],
                    "width": out_image.shape[2],
                    "transform": out_transform})
            
                   # write output name
                    output_file = name + '.tif'
                
                    with rasterio.open(os.path.join(out_path, output_file), "w", **out_meta) as dest:
                        dest.write(out_image)
                    


  create_mask_from_shapefile(input_shapefile, raster_path, out_path)
  
  
