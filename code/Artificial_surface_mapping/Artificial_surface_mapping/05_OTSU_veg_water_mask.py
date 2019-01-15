#author = "Chang Liu"
#copyright = "Copyright 2019, Nanjing University, njuRS"
#license = "GPL"
#version = "0.1"
#maintainer = "Chang Liu"
#email = "changliu811@gmail.com"
#status = "Production"
#description = "artificial surface mapping"

from skimage import data,filters,io
from skimage.filters import threshold_otsu
from skimage.util import img_as_ubyte
import os
import shutil
import sys
from osgeo import gdal, osr, gdal_array
import numpy as np


maskPath = r'M:\test\mask'
temppath = r'M:\test\temp'

#get Landsat-8 image path
for root,dirs,files in os.walk(temppath):
    for file in files:
        if 'stack_TOA' in file and file.endswith('.tif'):
            L8Path = os.path.join(root,file)
            print L8Path
ds = gdal.Open(L8Path) 

for root,dirs,files in os.walk(maskPath):
    for file in files:
        if 'NDVI' in file and file.endswith('.tif'):
            NDVIPath = os.path.join(root,file)
            print NDVIPath
        if 'MNDWI' in file and file.endswith('.tif'):
            MNDWIPath = os.path.join(root,file)
            print MNDWIPath

ds = gdal.Open(L8Path) 

NDVI_filename = '\\NDVI_otsu'
MNDWI_filename = '\\MNDWI_otsu'

geotransform = ds.GetGeoTransform()  
proj = ds.GetProjection()  
band_refer = ds.GetRasterBand(1)  
nodata = band_refer.GetNoDataValue()
data_refer = band_refer.ReadAsArray()  
xNum = data_refer.shape[1]     
yNum = data_refer.shape[0]  
 

NDVI_img = io.imread(NDVIPath)
rows,cols=NDVI_img.shape
for i in range(rows):
    for j in range(cols):
        if (NDVI_img[i,j]<-1):
            NDVI_img[i,j]=-1;
        elif (NDVI_img[i,j]>1):
            NDVI_img[i,j]=1

NDVI_dst = img_as_ubyte(NDVI_img) #float to unit8

threshold_global_otsu = threshold_otsu(NDVI_dst)
global_otsu = NDVI_dst >= threshold_global_otsu
NDVI_mask = (global_otsu == False)
NDVI_data = NDVI_mask.astype(np.int)

driver = gdal.GetDriverByName('GTiff')
output_ds = driver.Create( maskPath + NDVI_filename + '.tif' ,xNum,yNum,1,gdal.GDT_Float64)
output_ds.SetGeoTransform(geotransform)
output_ds.SetProjection(proj)
output_ds.GetRasterBand(1).WriteArray(NDVI_data)
output_ds.GetRasterBand(1).SetNoDataValue(0.0)
output_ds = None



MNDWI_img = io.imread(MNDWIPath)
rows,cols=MNDWI_img.shape
for i in range(rows):
    for j in range(cols):
        if (MNDWI_img[i,j]<-1):
            MNDWI_img[i,j]=-1;
        elif (MNDWI_img[i,j]>1):
            MNDWI_img[i,j]=1

MNDWI_dst = img_as_ubyte(MNDWI_img) #float to unit8

threshold_global_otsu = threshold_otsu(MNDWI_dst)
global_otsu = MNDWI_dst >= threshold_global_otsu
MNDWI_mask = (global_otsu == False)
MNDWI_data = MNDWI_mask.astype(np.int)

driver = gdal.GetDriverByName('GTiff')
output_ds = driver.Create( maskPath + MNDWI_filename + '.tif' ,xNum,yNum,1,gdal.GDT_Float64)
output_ds.SetGeoTransform(geotransform)
output_ds.SetProjection(proj)
output_ds.GetRasterBand(1).WriteArray(MNDWI_data)
output_ds.GetRasterBand(1).SetNoDataValue(0.0)
output_ds = None






