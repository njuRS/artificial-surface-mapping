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


trainpath = r'M:\test\trainsamples'
temppath = r'M:\test\temp'
resultpath = r'M:\test\result' 
maskPath = r'M:\test\mask'

if os.path.exists(resultpath)==False:
        os.mkdir(resultpath)


for root, dirs, files in os.walk(trainpath):
    for name in files:
        if 'merge_trainsample' in name and name.endswith('.shp'):
            train_shp = os.path.join(root, name)
for root, dirs, files in os.walk(temppath):
    for name in files:
        if "stack_TOA" in name and name.endswith ('.tif'):
            L8_compositebands = os.path.join(root, name)

arcpy.gp.TrainSupportVectorMachineClassifier(L8_compositebands, train_shp, resultpath + '//svm_classification.ecd')

classifiedraster = ClassifyRaster(L8_compositebands ,resultpath + '//svm_classification.ecd')
tempraster_filename = 'tempresult_artificial_surface.tif'
classifiedraster.save(os.path.join(resultpath,tempraster_filename))

for target_root, dirs, files in os.walk(trainpath):
    for target_name in files:
        if 'Target_area_NTL'in target_name and target_name.endswith ('.tif'):
            targetraster = os.path.join(target_root, target_name)

for tempsvm_root, dirs, files in os.walk(resultpath):
    for tempsvm_name in files:
        if 'tempresult'in tempsvm_name and tempsvm_name.endswith ('.tif'):
            temp_svm_raster = os.path.join(tempsvm_root, tempsvm_name)

for root,dirs,files in os.walk(maskPath):
    for file in files:
        if 'MNDWI_otsu' in file and file.endswith('.tif'):
            MNDWI = os.path.join(root,file)

result = Raster(temp_svm_raster) & Raster(targetraster)& Raster(MNDWI)
result_filename = 'result_artificial_surface.tif'
result.save(os.path.join(resultpath,result_filename))
arcpy.Delete_management("in_memory")