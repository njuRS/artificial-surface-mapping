# Artificial-Surface-Mapping
This code is to map artificial surfaces by fusing Landsat-8 imagery and NPP-VIIRS nighttime data. 
## Python Environment
Arcpy(10.4), Anaconda(2.7, download in https://www.anaconda.com/download/).
## Python Pip
Arcpy- os, math, shutil, sys.
Anaconda- os, shutil, sys, numpy (1.15.1), skimage (0.14.0), gdal (2.2.2).
## Attention
1. This code has 7 steps. All the steps run with Arcpy environment except the 5th step. The 5th step runs with anaconda environment.
2. Put the Landsat-8 imagery into the ‘predata’ file and click run step by step.
3. In the 6th step, you need to get the classification thresholds by using the Arcmap(10.4). Change the classification intervals in the code manually. Set the nighttime data DN=0 as the threshold to get the non-artificial surfaces training samples.  
![1](https://user-images.githubusercontent.com/46549560/53677829-2f4ef780-3cf1-11e9-9b45-66192d250fc3.png)
![2](https://user-images.githubusercontent.com/46549560/53677830-337b1500-3cf1-11e9-951d-97698b645fde.png)
4. Before running the 7nd step, you need to create the training features manually in Arcmap, they can not create in python automatically.
Add the ‘nonas_trainsample_dissolve.shp’ and ‘as_trainsample_dissolve.shp’ respectively into the training sample manager. Then save these feature classes as ‘merge_trainsample.shp’ in the ‘trainsamples’ file.  
![3](https://user-images.githubusercontent.com/46549560/53677832-34ac4200-3cf1-11e9-88fa-6161f10f207b.png)
![4](https://user-images.githubusercontent.com/46549560/53677833-35dd6f00-3cf1-11e9-9812-b7bcccf8bcbb.png) 
5. In the ‘result’ file, you will get the final mapping result of artificial surfaces-‘result_artificial_surface.tif’. 
![5](https://user-images.githubusercontent.com/46549560/53677834-36760580-3cf1-11e9-8cfa-9e451d56b65d.png)
## Corresponding Author
 Chang Liu, changliu811@gmail.com  
 Kang Yang, kangyang@nju.edu.cn  
 Phone: (+86)17302560154  
 School of Geography and Ocean Science, Nanjing University.
