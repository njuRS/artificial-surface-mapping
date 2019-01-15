#author = "Chang Liu"
#copyright = "Copyright 2019, Nanjing University, njuRS"
#license = "GPL"
#version = "0.1"
#maintainer = "Chang Liu"
#email = "changliu811@gmail.com"
#status = "Production"
#description = "artificial surface mapping"

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

temppath = r'M:\test\temp'
maskPath = r'M:\test\mask'
if os.path.exists(maskPath)==False:
        os.mkdir(maskPath)


env.workspace= temppath
env.overwriteOutput = True
rasters=arcpy.ListRasters('*', 'tif')
for raster in rasters:
    if 'stack_TOA' in raster:
        blueband = Raster(raster + '\\Band_2')
        greenband = Raster(raster + '\\Band_3')
        redband = Raster(raster + '\\Band_4')
        nirband = Raster(raster + '\\Band_5')
        swir1 = Raster(raster + '\\Band_6')
        swir2 = Raster(raster + '\\Band_7')
 
        ndviRaster=Float(nirband - redband) / Float(redband + nirband)
        ndvi_filename = 'NDVI_' + raster
        ndviRaster.save(os.path.join(maskPath,ndvi_filename))

        MNDWIRaster = Float(greenband-swir1) / Float(greenband + swir1)
        MNDWI_filename = "MNDWI_" + raster
        MNDWIRaster.save(os.path.join(maskPath,MNDWI_filename))
                    
        arcpy.Delete_management("in_memory")
