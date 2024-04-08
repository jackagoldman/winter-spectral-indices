# raster processing

crop_rasters <- function(dir, shapefile, out_dir, file_extension){
  
  #get a list of all files with ndvi in the name in your directory
  files<-list.files(path=dir, pattern='*.tif', full.names = TRUE)
  
  if (file_extension == "defol"){
    # get file name and filter it from shapefile
    for (file in files){
      name <- file
      raster <- terra::rast(file)
      name <- basename(name)
      name <- gsub(".tif", "", name)
      
      # get shp that matches name
      shp <- shapefile |> dplyr::filter(Fire_ID == name)
      
      #crop
      cropped_raster <- terra::crop(raster, shp, mask=TRUE)
      
      # get output path
      savename<-paste0(out_dir, name, "defol")
      
      # write raster
      terra::writeRaster(cropped_raster, filename = savename)
    }}else if (file_extension == "non_defol"){
      for (file in files){
        name <- file
        raster <- terra::rast(file)
        name <- basename(name)
        name <- gsub(".tif", "", name)
        
        # get shp that matches name
        shp <- shapefile |> dplyr::filter(Fire_ID == name)
        
        #crop
        cropped_raster <- terra::crop(raster, shp, mask=TRUE)
        
        # get output path
        savename<-paste0(out_dir, name, "non_defol")
        
        # write raster
        terra::writeRaster(cropped_raster, filename = savename)
        
      }}
      
}


get_raster_values <- function(img){

  #rbr offset
  v_ro <- terra::values(img$rbr_w_offset)
  v_ro <- na.omit(v_ro)
  mean_vro <- mean(v_ro)
  median_vro <- median(v_ro)
  cv_vro <- goeveg::cv(v_ro)
  ext_vro <- quantile(v_ro, 0.95)[[1]]
  vro <- cbind(mean_vro, median_vro, cv_vro, ext_vro) |>  as.data.frame()
  
  #rbr
  v_r <- terra::values(img$rbr)
  v_r <- na.omit(v_r)
  mean_vr <- mean(v_r)
  median_vr <- median(v_r)
  cv_vr <- goeveg::cv(v_r)
  ext_vr <- quantile(v_r, 0.95)[[1]]
  vr <- cbind(mean_vr, median_vr, cv_vr, ext_vr)|>  as.data.frame()
  
  #dnbr_w_offset
  v_do <- terra::values(img$dnbr_w_offset)
  v_do <- na.omit(v_do)
  mean_do <- mean(v_do)
  median_do <- median(v_do)
  cv_do <- goeveg::cv(v_do)
  ext_do <- quantile(v_do, 0.95)[[1]]
  do <- cbind(mean_do, median_do, cv_do, ext_do)|>  as.data.frame()
  
  
  #dnbr
  v_d <- terra::values(img$dnbr)
  v_d <- na.omit(v_d)
  mean_d <- mean(v_d)
  median_d <- median(v_d)
  cv_d <- goeveg::cv(v_d)
  ext_d <- quantile(v_d, 0.95)[[1]]
  d <- cbind(mean_d, median_d, cv_d, ext_d)|>  as.data.frame()
  
  #pre
  v_pre <- terra::values(img$preNBR)
  v_pre <- na.omit(v_pre)
  mean_pre <- mean(v_pre)
  median_pre <- median(v_pre)
  cv_pre <- goeveg::cv(v_pre)
  ext_pre <- quantile(v_pre, 0.95)[[1]]
  pre <- cbind(mean_pre, median_pre, cv_pre, ext_pre)|>  as.data.frame()
  
  #post
  v_post <- terra::values(img$postNBR)
  v_post <- na.omit(v_post)
  mean_post <- mean(v_post)
  median_post <- median(v_post)
  cv_post <- goeveg::cv(v_post)
  ext_post <- quantile(v_post, 0.95)[[1]]
  post <- cbind(mean_post, median_post, cv_post, ext_post)|>  as.data.frame()
  
  df <- cbind(vro, vr, do, d, pre, post)
  
  names(df) <- df |> 
    names() |>  
    stringr::str_replace( "vro", "rbr_ofst") |> 
    stringr::str_replace( "vr", "rbr") |> 
    stringr::str_replace( "do", "dnbr_ofst") |> 
    stringr::str_replace( "_d", "_dnbr") |> 
    stringr::str_replace( "pre", "preNBR") |> 
    stringr::str_replace( "post", "postNBR")  
    
    
    
  
  return(df)
  
}



area_weighted_raster_values <- function(img){
  
  
  
}
