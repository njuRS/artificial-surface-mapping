#author = "Chang Liu"
#copyright = "Copyright 2019, Nanjing University, njuRS"
#license = "GPL"
#version = "0.1"
#maintainer = "Chang Liu"
#email = "changliu811@gmail.com"
#status = "Production"
#description = "artificial surface mapping"

#this step is to clip the nighttime data based on the Landsat-8 image.

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


NTLpath = r'F:\nighttime_data\annual_2015\SVDNB_npp_20150101-20151231_75N060W_v10_c201701311200'
TOA_cpsbandsPath =  r'M:\test\TOAcompositebands'
clip_NTLpath = r'M:\test\NTL' 
temppath = r'M:\test\temp'

if os.path.exists(clip_NTLpath)==False:
        os.mkdir(clip_NTLpath)
if os.path.exists(temppath )==False:
        os.mkdir(temppath)


# get the Landsat-8 image coordinate reference system
for root, dirs, files in os.walk(TOA_cpsbandsPath):
    for name in files:
        if "copyRaster" in name and name.endswith ('.tif'):          
            pathL8_compositebands = os.path.join(root, name)
            shutil.copyfile(pathL8_compositebands, temppath + '\\' + name)

spatial_ref = arcpy.Describe(pathL8_compositebands).spatialReference
coodinate = "{0}".format(spatial_ref.name)

#copy NTL data to tempfile
os.chdir(NTLpath)
env.workspace= NTLpath
env.overwriteOutput = True
rasters=arcpy.ListRasters('*', 'tif')
for NTL_raster in rasters:
    if 'vcm-orm-ntl' in NTL_raster:
        print NTL_raster
        NTL_name = NTL_raster.split('_vcm-orm-ntl')[0] + '.tif' 
        shutil.copyfile(NTLpath + '\\' + NTL_raster,temppath + '\\' + NTL_name)

#clip the nighttime data based on the Landsat-8 image.
os.chdir(temppath)
env.workspace= temppath
env.overwriteOutput = True
rasters=arcpy.ListRasters('*', 'tif')
for raster in rasters:
    if 'SVDNB_npp' in raster:
        NTL_raster = raster
        print NTL_raster
    if 'stack_TOA' in raster:
        L8_raster = raster
        print L8_raster


arcpy.env.extent = pathL8_compositebands
arcpy.env.mask = pathL8_compositebands
arcpy.env.snapRaster = pathL8_compositebands
NTL_ExtractByMask = ExtractByMask(NTL_raster, L8_raster)
arcpy.ProjectRaster_management(NTL_ExtractByMask, clip_NTLpath + '//reproject_NTL.tif',\
                               spatial_ref, "BILINEAR", '30',\
                               "#", "#", "#")

