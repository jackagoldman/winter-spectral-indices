# check_missing_imagery loop
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
  
  if not get_keys(preFireIndices, fireBounds):
    print("pre_nk", name)
    continue
  
  if not get_keys(postFireIndices, fireBounds):
    print("post_nk", name)
    continue
  
  # if pixel is 0, go to the next
  if return_pixel_count(preFireIndices, fireBounds, "preNBR") == 0:
    print("pre", name)
  
  if return_pixel_count(postFireIndices, fireBounds, "postNBR") == 0:
    print("post", name)
