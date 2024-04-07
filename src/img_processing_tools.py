def check_image_info(img):
  imgInf = img.getInfo()
  print(imgInf)
  
  # Returns vegetation indices for LS8 / change to CO2_T2_L2
def ls8_Indices(lsImage):
  nbr = lsImage.normalizedDifference(['SR_B5', 'SR_B7']).toFloat()
  qa = lsImage.select(['QA_PIXEL'])
  ndsi = image.normalizedDifference({'SR_B3', 'SR_B6'}).toFloat()
  nbr = nbr.addBands(ndsi)
  return nbr.addBands([qa]).select([0,1,2], ['nbr', 'ndsi','QA_PIXEL']).copyProperties(lsImage, ['system:time_start'])

  
#// Returns vegetation indices for LS4, LS5 and LS7 . change to CO2_T2_L2
 def ls4_7_Indices(lsImage):
   nbr = lsImage.normalizedDifference(['SR_B4', 'SR_B7']).toFloat()
   ndsi = image.normalizedDifference({'SR_B2', 'SR_B5'}).toFloat()
   nbr = nbr.addBands(ndsi)
   qa = lsImage.select(['QA_PIXEL'])
   return nbr.addBands([qa]).select([0,1,2], ['nbr','ndsi', 'QA_PIXEL']).copyProperties(lsImage, ['system:time_start'])
  
 
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
   
   
#  check to see if there are pixels: this prints to console
def check_pixel_count(img, geom):
  res = img.reduceRegion(**{
  'reducer': ee.Reducer.count(),\
  'geometry':geom,\
  'scale': 30})
  print(res.getInfo())


# check to see if there are pixels: this returns a number object
def return_pixel_count(img, geom, time):
  res = img.reduceRegion(**{
  'reducer': ee.Reducer.count(),\
  'geometry':geom,\
  'scale': 30})
  if time == "preNBR":
    res = res.getNumber('preNBR')
  elif time == "postNBR":
    res = res.getNumber('postNBR')
  return(res.getInfo())

# check dates - converts ee date to y-m-d and prints in console
def check_dates(date):
  date = date.format('Y-M-d')
  print(date.getInfo())


# check if image contains key
def get_keys(img, geom):
  res = img.reduceRegion(**{
  'reducer': ee.Reducer.count(),\
  'geometry':geom,\
  'scale': 30})
  res = res.keys()
  return(res.getInfo())
