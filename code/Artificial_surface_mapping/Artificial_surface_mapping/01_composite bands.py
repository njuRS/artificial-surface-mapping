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
from arcpy import env
from arcpy.sa import *

arcpy.CheckOutExtension = 'Spatial' 

#set the workspace and list all of the raster dataset
inputPath = r'M:\test\predata'
outputPath = r'M:\test\compositebands'


if os.path.exists(outputPath)==False:
        os.mkdir(outputPath)

env.workspace= inputPath
rootDir=arcpy.ListWorkspaces('*','Folder')
for root in rootDir:
    env.workspace= root
    fcList=[]
    tiffs=arcpy.ListRasters('*', 'TIF')    
    for tiff in tiffs:
        if tiff.endswith ('B1.TIF'):
            name = tiff.split('_B')[0]
        if 'LC08' in name:
            if tiff.endswith (('B1.TIF','B2.TIF','B3.TIF','B4.TIF','B5.TIF','B6.TIF','B7.TIF')):#green,blue,red,nir,swir,'B10.TIF' for TIR
                fcList.append(tiff)
       
    fileName='stack_' + name + '.tif'
    print(fileName)
    arcpy.CompositeBands_management(fcList,outputPath + '\\' + fileName) 
    arcpy.Delete_management("in_memory")    
