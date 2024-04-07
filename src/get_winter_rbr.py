def getWinterRBR(fires, img_coll):
  #get list of fire names server side
   fids = fires.aggregate_array('Fire_ID')
   # turn it to python list
   fids = fids.getInfo()
   
   res = ee.ImageCollection(fires.map(indices_function))
  
  # loop through list of fire ids
  for j in fids:
  name = j
  # get fire that corresponds to i
  foi = res.filter(ee.Filter.eq('Fire_ID', name))
  
  b = fires.filter(ee.Filter.eq('Fire_ID', name))
  
  fB = b.geometry().bounds()
  
  fiya = ee.Image(foi.filterMetadata('fireID', 'equals', name).first());
  #get image
  
  task = ee.batch.Export.image.toDrive(**{
    'image': fiya,
    'description': name,
    'folder':'winter_test_folder',
    'scale': 30,
    'region': fB.getInfo()['coordinates']
    })
  # start task
  task.start()
 

task.status()


return
