#author = "Chang Liu"
#copyright = "Copyright 2019, Nanjing University, njuRS"
#license = "GPL"
#version = "0.1"
#maintainer = "Chang Liu"
#email = "changliu811@gmail.com"
#status = "Production"
#description = "artificial surface mapping"

#this step is to create training samples.
#Before running this step, you need to get the classification thresholds of Jenks natural breaks by using ArcGis.

import arcpy,os,sys
import os
import shutil
from arcpy import env
from arcpy.sa import *

if arcpy.CheckExtension('Spatial') == 'Available':
    arcpy.AddMessage('Checking out Spatial')
    arcpy.CheckOutExtension('Spatial')
else:
    arcpy.AddError('Unable to get spatial analyst extension')
    arcpy.AddMessage(arcpy.GetMessages(0))
    sys.exit(0)

clip_NTLpath= r'M:\test\NTL' 
maskPath = r'M:\test\mask'
trainpath = r'M:\test\trainsamples'
if os.path.exists(trainpath )==False:
        os.mkdir(trainpath)


for root,dirs,files in os.walk(clip_NTLpath):
    for file in files:
        if 'reproject' in file and file.endswith('.tif'):
            NTLimg_Path = os.path.join(root,file)
            print NTLimg_Path

env.workspace= maskPath
rasters=arcpy.ListRasters('*', 'TIF')
for raster_1 in rasters:
    if "NDVI_otsu" in raster_1:
        NDVI_raster = raster_1
for raster_2 in rasters:
    if "MNDWI_otsu" in raster_2:
        MNDWI_raster = raster_2

os.chdir(trainpath)
field = "VALUE"
as_remapString = "0 81.01102941 0;81.01102941 276 1"
arcpy.Reclassify_3d(NTLimg_Path, field, as_remapString, trainpath + '\\aspotential_trainsample.tif','NODATA')
nonas_remapString = "-1 0 1;0 276 0"
arcpy.Reclassify_3d(NTLimg_Path, field, nonas_remapString, trainpath + '\\nonas_trainsample.tif','NODATA')
Target_remapString = "-1 6.480882353 0;6.480882353 276 1"
arcpy.Reclassify_3d(NTLimg_Path, field, Target_remapString, trainpath + '\\Target_area_NTL.tif', 'NODATA')

for as_ntl_root, dirs, files in os.walk(trainpath):
    for as_ntl_name in files:
        if 'aspotential_trainsample.tif' in as_ntl_name and as_ntl_name.endswith ('.tif'):
            train_as_ntl_mask = os.path.join(as_ntl_root,as_ntl_name)
            print train_as_ntl_mask

train_as = Raster(NDVI_raster) & Raster(train_as_ntl_mask) & Raster(MNDWI_raster)
train_as_filename = 'as_trainsample.tif'
train_as.save(os.path.join(trainpath,train_as_filename))


env.workspace= trainpath
env.overwriteOutput = True
rasters=arcpy.ListRasters('*', 'tif')
for raster in rasters:
    if 'as_trainsample.tif' in raster or 'nonas_trainsample.tif' in raster:
        print raster.split('.tif')[0]
        outPolygons = trainpath + '\\' + raster.split('.tif')[0] + '.shp'
        field = "VALUE"
        arcpy.RasterToPolygon_conversion(raster, outPolygons,"NO_SIMPLIFY", field)
        dissolveFields = 'GRIDCODE'
        outFeatureClass = trainpath + '\\' + raster.split('.tif')[0] + '_dissolve'+ '.shp'
        arcpy.Dissolve_management(outPolygons, outFeatureClass, dissolveFields)
        arcpy.Delete_management("in_memory")