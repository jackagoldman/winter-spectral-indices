def getWinterRBR(fires, img_coll):
  #get list of fire names server side
   fids = fires.aggregate_array('Fire_ID')
   # turn it to python list
   fids = fids.getInfo()
   # get length of ID list
   idSize = fids.size()
   idSize = fids.getInfo()
  
  # loop through list of fire ids
  for i in fids:
  
  
  
  

  
  
