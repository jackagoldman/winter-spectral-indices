#' winter NBR 
#'
#' @param data 
#' @param ls_col 
#'
#' @return
#' @export
#'
#' @examples
winterNBR<- function(data, colNBR){
  
  require(sf)
  require(rgee)
  require(tidyverse)
  
  
  #get info
  fireID <- data$Fire_ID
  defol <- data$defoliated
  fire_Year <- data$Fire_Year
  
  #get geometry
  geom <- sf_as_ee(data)
  
  #get start date and end date the filter imagery for prefire
  preFireYear <- timeFrame(data)$preFireYear
  fireYear <- timeFrame(data)$fireYear
  ## get post fire start date and end date and filter the imagery
  postFireYear <- timeFrame(data)$postFireYear
  fireYearDec <- timeFrame(data)$fireYearDec
  
  # read in imagery and filter by pre to postfire
  ls8 <-ee$ImageCollection('LANDSAT/LC08/C02/T1_L2')$
    filterBounds(geom$geometry())$
    map(ls8Nbr)
  ls7 <-ee$ImageCollection('LANDSAT/LE07/C02/T1_L2')$
    filterBounds(geom$geometry())$
    map(ls47NBR)
  ls5 <- ee$ImageCollection('LANDSAT/LT04/C02/T2_L2')$
    filterBounds(geom$geometry())$
    map(ls47NBR)
  ls4 <- ee$ImageCollection('LANDSAT/LT04/C02/T1_L2')$
    filterBounds(geom$metry())$
    map(ls47NBR)
  
  colNBR <-ee$ImageCollection(ls8$merge(ls7)$merge(ls5)$merge(ls4))
  
  preFireYear = rdate_to_eedate(preFireYear)
  fireYear <- rdate_to_eedate(fireYear)
  ## PREFIRE
  # get mean composite over timeframe
  preComp <- colNBR$select("nbr")$
    filterBounds(geom)$
    filterDate(preFireYear, fireYear)
  
  
    mean()$
    rename("preNBR")
  
  
  ##POSTFIRE
  # get mean composite over timeframe
  postComp <- colNBR$select('nbr')$
    filterBounds(geom)$
    filterDate(fireYearDec, postFireYear)$
    mean()$
    rename("postNBR")
    
  
  #Add post and pre together
  composite <- preComp$addBands(postComp)
  
  preNBR <- composite$select("preNBR")
  postNBR <- composite$select("postNBR")
  dnbr <- preNBR$subtract(postNBR)$multiply(1000)$rename("dnbr")$float()$addBands(composite)
  rbr <- dnbr$divide(preNBR)$add(1.001)$rename("rbr")$float()$addBands(dnbr)
  
  # extract metrics for each image
  task_img <- ee_image_to_drive(
    image = preComp,
    fileFormat = "GEO_TIFF",
    region = geom,
    fileNamePrefix = "my_image_demo"
  )

  task_img$start()
  ee_monitoring(task_img)
  
}








