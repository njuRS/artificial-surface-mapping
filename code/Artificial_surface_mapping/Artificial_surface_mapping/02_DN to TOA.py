#author = "Chang Liu"
#copyright = "Copyright 2019, Nanjing University, njuRS"
#license = "GPL"
#version = "0.1"
#maintainer = "Chang Liu"
#email = "changliu811@gmail.com"
#status = "Production"
#description = "artificial surface mapping"

#this step is to convert DN value to top of atmosphere(TOA) radiance of every Landsat-8 image band, and then composite these bands.

import os
import shutil
import math
import arcpy
import sys
from arcpy import env
from arcpy.sa import *

if arcpy.CheckExtension("Spatial") == "Available":
    arcpy.AddMessage("Checking out Spatial")
    arcpy.CheckOutExtension("Spatial")
else:
    arcpy.AddError("Unable to get spatial analyst extension")
    arcpy.AddMessage(arcpy.GetMessages(0))
    sys.exit(0)
REFLECTANCE_MULT_BAND = 0.00002
REFLECTANCE_ADD_BAND=-0.1
F1=1
F2=0
cpsbandsPath=r'M:\test\compositebands' 
predataPath=r'M:\test\predata'
TOAPath = r'M:\test\TOApredata'
TOA_cpsbandsPath =  r'M:\test\TOAcompositebands'

if os.path.exists(cpsbandsPath)==False:
        os.mkdir(cpsbandsPath)
if os.path.exists(TOAPath)==False:
        os.mkdir(TOAPath)
if os.path.exists(TOA_cpsbandsPath)==False:
        os.mkdir(TOA_cpsbandsPath)

for root,dirs,files in os.walk(predataPath):
    for file in files:
        if file.endswith('MTL.txt'):
            outputPath= TOAPath + '\\'+ file.split('_M')[0]
            os.mkdir(outputPath)
            with open(root + '/' + file,'r') as f:
                for line in f.readlines():
                    if (line.find ("SUN_ELEVATION")>= 0):
                        angle=math.sin((float(line.split('= ')[1])*math.pi)/180)
                        break
            os.chdir(cpsbandsPath)
            env.workspace= cpsbandsPath
            rasters=arcpy.ListRasters('*', 'TIF')
            for raster in rasters:
                print raster
                if file.split('_M')[0] in raster:
                    for i in range(1,8):
                        TOARaster=(Raster(raster + '\\Band_'+str(i)) * REFLECTANCE_MULT_BAND + REFLECTANCE_ADD_BAND)/angle
                        outCon1=Con(TOARaster >1, 1,TOARaster )
                        outCon2=Con(outCon1 <0, 0,outCon1)
                        filename='TOA_'+file.split('_M')[0]+"_B"+str(i)+ ".TIF"
                        outCon2.save(os.path.join(TOAPath,filename))
                        arcpy.Delete_management("in_memory")   


os.chdir(TOAPath)
env.workspace= TOAPath
fcList=[]
tiffs=arcpy.ListRasters('*', 'TIF')    
print tiffs
for tiff in tiffs:
    if tiff.endswith ('B1.TIF'):
        name = tiff.split('_B')[0]
    if 'LC08' in name:
        if tiff.endswith (('B1.TIF','B2.TIF','B3.TIF','B4.TIF','B5.TIF','B6.TIF','B7.TIF')):#green,blue,red,nir,swir,'B10.TIF' for TIR
            fcList.append(tiff)
      
fileName='stack_' + name 
print(fileName)
arcpy.CompositeBands_management(fcList,TOA_cpsbandsPath + '\\' + fileName + '.tif') 

for root,dirs,files in os.walk(TOA_cpsbandsPath):
    for file in files:
        if file.endswith('.tif'):
            copyRaster_Path = os.path.join(root,file)
            print copyRaster_Path

arcpy.CopyRaster_management(copyRaster_Path,
                           TOA_cpsbandsPath + '\\' + fileName + '_copyRaster.tif',"",
                           "","0","","","",'','')
arcpy.Delete_management("in_memory")   







