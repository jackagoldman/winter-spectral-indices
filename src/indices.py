def indices_function(ft):
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
  postFireYearAd = postFireYear.advance(2, 'month')
  postFireYearAd = postFireYearAd.advance(31, 'day')
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
          
  fireIndices = preFireIndices.addBands(postFireIndices)
  
  dnbr = fireIndices.expression( "(b('preNBR') - b('postNBR')) * 1000") \
              .rename('dnbr').toFloat()
  
  ring  = fire.buffer(180).difference(fire);
  
  offset = ee.Image.constant(ee.Number(dnbr.select('dnbr').reduceRegion(**{ 
      'reducer': ee.Reducer.mean(),
      'geometry': ring.geometry(),
      'scale': 30,
      'maxPixels': 1e9}).get('dnbr')))
      
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
            
  rbr_offset = rbr_offset.addBands(rbr)
            
            
  rbr_offset = rbr_offset.set('fireID' , ft.get('Fire_ID'),'fireName' , ft.get('Fire_Name'), 'fireYear' ,  ft.get('Year')) 
  
  return rbr_offset



