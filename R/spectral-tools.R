

# read in data
readFile <- function(path2file){
  file <- ee$ImageCollection(path2file) 
  return(file)
}


# read in fires and convert to ee object
## read in fires
readFire <- function(firePath){
  fires <- sf::read_sf(firePath)
  # convert sf objects to earth engine objects
  fires <- sf::st_set_crs(fires, 4326)
  fires <- rgee::sf_as_ee(fires)
  return(fires)
}

#rename Bands (NOT WORKING)
renameBands <- function(coll){
  bands <- list("SR_B5", "SR_B7", "QA_PIXEL")
  renameList <- list("B4", "B7", "pixel_qa")
  imgColl <- coll$select(list("SR_B5", "SR_B7", "QA_PIXEL") ,list("B4", "B7", "pixel_qa"))
  
  return(imgColl) 
}

# filter image collection by month
filter_col_winter <- function(ls_img){
  ls_date <- ls_img$
    filter(ee$Filter$calendarRange(12,2 ,'month'))
  
  return(ls_date)
}


filter_col_date <- function(ls_img, pre){
  if(pre == pre){
    ls_date <- ls_img$
      filterDate(preFireYear, fireYear)
  }else {
    ls_date <- ls_img$
      filterDate(postFireYear, fireYearDec)
  }
  
  return(ls_date)
}
#get time frame
timeFrame <- function(data){
  year <- data |> select(c(Fire_Year)) |> st_drop_geometry() 
  year <- mutate(year, Fire_Year = as.numeric(Fire_Year))
  preFire <- (year - 1) 
  preFire <- lubridate::ymd(preFire, truncated = 2L) 
  month(preFire) <- 12
  preFire <- preFire |> as.character() |> as.data.frame()
  fireYear <- lubridate::ymd(year, truncated = 2L)
  month(fireYear) <- 3
  fireYear <- fireYear |> as.character() |> as.data.frame()
  postFire <- (year + 1)
  postFire <- lubridate::ymd(postFire, truncated = 2L) 
  month(postFire) <- 3
  postFire <- postFire |> as.character() |> as.data.frame()
  yearEnd <- year
  yearEnd<- lubridate::ymd(yearEnd, truncated = 2L) 
  month(yearEnd) <- 12
  yearEnd <- yearEnd |> as.character() |> as.data.frame()
  
  postFire <- postFire |> as.character() |> as.data.frame()
  res <- cbind(preFire, fireYear, yearEnd, postFire)
  colnames(res) <- c("preFireYear", "fireYear", "fireYearDec", "postFireYear")
  
  
  return(res)
}


# get landsat 8 nbr
ls8Nbr <- function(img){
  
  quality <- img$select('QA_PIXEL')
  clear <- quality$bitwiseAnd(4)$ #cloud shadow
    And(quality$bitwiseAnd(3))$ # cloud
    And(quality$bitwiseAnd(7))$ # water
    And(quality$bitwiseAnd(5))#snow
  img <- img$updateMask(clear$Not())
  img$normalizedDifference(list("SR_B5", "SR_B7"))$float()$rename("nbr")
  
  
  
  
}

# make image collection
ls47NBR <- function(img){
  
  quality <- img$select('QA_PIXEL')
  clear <- quality$bitwiseAnd(4)$ #cloud shadow
    And(quality$bitwiseAnd(3))$ # cloud
    And(quality$bitwiseAnd(7))$ # water
    And(quality$bitwiseAnd(5))#snow
  img <- img$updateMask(clear$Not())
  img$normalizedDifference(list("SR_B4", "SR_B7"))$float()$rename("nbr")
  

}




# export top drive

exportTable <-  function(metrics, GG_DIR){
  task <- ee_table_to_drive(
    collection = metrics,
    description = "fire_severity_stats",
    folder = GG_DIR,
    fileFormat = "CSV"
  )
  task$start()
  exported.fire.stats <- ee_drive_to_local(task = task, dsn = paste0(GG_DIR, "fire_severity_stats.csv"))
  return(exported.fire.stats)
}



