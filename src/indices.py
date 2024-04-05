def indices_function(lsImg):
  fName = ft.get("Fire_ID")
  fire = ft
  fireBounds = ft.geometry().bounds()
  fireYear = ee.Date.parse('YYYY', fire.get('Fire_Year'))
  preFireYear = fireYear.advance(-1, 'year')
  postFireYear = fireYear.advance(1, 'year')
  preFireYearAd = preFireYear.advance(11, 'month')
  fireYearAd = fireYear.advance(2, 'month')
  postFireYearAd = postFireYear.advance(2, 'month')
  postFireYearAd = postFireYearAd.advance(20, 'day')
  fireYearAd2 = fireYear.advance(11, 'month')
  fireYearAd = fireYearAd.advance(20, 'day')
  preFireYearAd = preFireYearAd.advance(20, 'day')
  fireYearAd2 = fireYearAd2.format('Y-M-d').getInfo()
  postFireYearAd = postFireYearAd.format('Y-M-d').getInfo()
  fireYearAd = fireYearAd.format('Y-M-d').getInfo()
  preFireYearAd = preFireYearAd.format('Y-M-d').getInfo()
  preFireIndices = (lsCol.filterBounds(fireBounds).filterDate(preFireYearAd, fireYearAd).mean().rename('preNBR'))
  postFireIndices = (lsCol.filterBounds(fireBounds).filterDate(fireYearAd2, postFireYearAd).mean().rename('postNBR'))
  fireIndices = preFireIndices.addBands(postFireIndices)
  burnIndices = (fireIndices.expression(
              "(b('preNBR') - b('postNBR')) * 1000")
              .rename('dnbr').toFloat().addBands(fireIndices))
  ring  = fire.buffer(180).difference(fire);
  burnIndices2 = (ee.Image.constant(ee.Number(burnIndices.select('dnbr').reduceRegion(**{
      'reducer': ee.Reducer.mean(),
      'geometry': ring.geometry(),
      'scale': 30,
      'maxPixels': 1e9}).get('dnbr'))).rename('offset').toFloat().addBands(burnIndices)) 
  burnIndices3 = (burnIndices2.expression(
            "b('dnbr') - b('offset')").
            rename('dnbr_w_offset').toFloat().addBands(burnIndices2))
  burnIndices4 = (burnIndices3.expression(
            "b('dnbr') / (b('preNBR') + 1.001)")
            .rename('rbr').toFloat().addBands(burnIndices3))
  burnIndices5 = (burnIndices4.expression(
            "b('dnbr_w_offset') / (b('preNBR') + 1.001)")
            .rename('rbr_w_offset').toFloat().addBands(burnIndices4))
  burnIndices6 = (burnIndices5.expression(
            "abs(b('preNBR')) < 0.001 ? 0.001" + 
            ": b('preNBR')")
            .abs().sqrt().rename('preNBR2').toFloat().addBands(burnIndices5))
  burnIndices7 = (burnIndices6.expression(
            "b('dnbr') / b('preNBR2')")
            .rename('rdnbr').toFloat().addBands(burnIndices6))
  burnIndices8 = (burnIndices7.expression(
            "b('dnbr_w_offset') / b('preNBR2')")
            .rename('rdnbr_w_offset').toFloat().addBands(burnIndices7))
  burnIndices8 = burnIndices8.select(bandList);
  burnIndices8.set('fireID' , ft.get('Fire_ID'),'fireName' , ft.get('Fire_Name'), 'fireYear' ,  ft.get('Year'))
  return burnIndices8

