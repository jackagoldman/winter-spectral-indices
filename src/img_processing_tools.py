def check_image_info(img):
  imgInf = img.getInfo()
  print(imgInf)
  
  
  # Returns vegetation indices for LS8 / change to CO2_T2_L2
def ls8_Indices(lsImage):
  nbr = lsImage.normalizedDifference(['SR_B5', 'SR_B7']).toFloat()
  qa = lsImage.select(['QA_PIXEL'])
  return nbr.addBands([qa]).select([0,1], ['nbr', 'QA_PIXEL']).copyProperties(lsImage, ['system:time_start'])

  
#// Returns vegetation indices for LS4, LS5 and LS7 . change to CO2_T2_L2
 def ls4_7_Indices(lsImage):
   nbr = lsImage.normalizedDifference(['SR_B4', 'SR_B7']).toFloat()
   qa = lsImage.select(['QA_PIXEL'])
   return nbr.addBands([qa]).select([0,1], ['nbr', 'QA_PIXEL']).copyProperties(lsImage, ['system:time_start'])
  
 
# Mask Landsat surface reflectance images
# Creates a mask for clear pixels 
 def lsCfmask(lsImg):
  qa = lsImg.select("QA_PIXEL")
  cloudBitMask = 1 << 3
  cirrusBitMask = 1 << 4
  waterBitMask = 1 << 7
  mask = qa.bitwiseAnd(cloudBitMask).eq(0).And(qa.bitwiseAnd(cirrusBitMask).eq(0)).And(
    qa.bitwiseAnd(waterBitMask).eq(0))
  return lsImg.updateMask(mask) \
      .select("nbr") \
      .copyProperties(lsImg, ["system:time_start"])
   
   
   
   def check_pixel_count(img, geom):
  res = img.reduceRegion(**{
  'reducer': ee.Reducer.count(),\
  'geometry':geom,\
  'scale': 30})
  return(res)
   
