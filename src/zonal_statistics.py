

def zonalStats(ic, fc, params):
  # Initialize internal params dictionary.
  _params = {
    'reducer': ee.Reducer.mean(),
    'scale': None,
    'crs': None,
    'bands': None,
    'bandsRename': None,
    'imgProps': None,
    'imgPropsRename': None,
    'datetimeName': 'datetime',
    'datetimeFormat': 'YYYY-MM-dd HH:'mm':ss'
  }

  # Replace initialized params with provided params.
  if (params) {
    for param in params:
      _params[param] = params[param] || _params[param]

  }

  # Set default parameters based on an image representative.
  imgRep = ic.first()
  nonSystemImgProps = ee.Feature(None) \
    .copyProperties(imgRep).propertyNames()
  if (!_params.bands) _params.bands = imgRep.bandNames()
  if (!_params.bandsRename) _params.bandsRename = _params.bands
  if (!_params.imgProps) _params.imgProps = nonSystemImgProps
  if (!_params.imgPropsRename) _params.imgPropsRename = _params.imgProps

  # Map the reduceRegions function over the image collection.

def func_ohf(img):
    # Select bands (optionally rename), set a datetime & timestamp property.
    img = ee.Image(img.select(_params.bands, _params.bandsRename)) \
      .set(_params.datetimeName, img.date().format(_params.datetimeFormat)) \
      .set('timestamp', img.get('system:time_start'))

    # Define final image property dictionary to set in output features.
    propsFrom = ee.List(_params.imgProps) \
      .cat(ee.List([_params.datetimeName, 'timestamp']))
    propsTo = ee.List(_params.imgPropsRename) \
      .cat(ee.List([_params.datetimeName, 'timestamp']))
    imgProps = img.toDictionary(propsFrom).rename(propsFrom, propsTo)

    # Subset points that intersect the given image.
    fcSub = fc.filterBounds(img.geometry())

    # Reduce the image by regions.
    return img.reduceRegions({
      'collection': fcSub,
      'reducer': _params.reducer,
      'scale': _params.scale,
      'crs': _params.crs
    }) \
    .map(function(f) {
      return f.set(imgProps)
    })

  results = ic.map(func_ohf
).flatten().filter(ee.Filter.NotNull(_params.bandsRename))

).flatten().filter(ee.Filter.NotNull(_params.bandsRename))

  return results
