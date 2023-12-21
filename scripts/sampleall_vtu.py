#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 16:16:24 2023

@author: zettergm
"""

import vtu2regular
import numpy as np
import os

# Obtain the model data and cell center locations
#filename="/Users/zettergm/simulations/ssd/figments_misty_3Dx_512_23/gemini_output/fort_frame_0028.vtu"
direc="/Users/zettergm/simulations/ssd/figments_misty_3Dx_2048_36_long/gemini_output/"
outdirec="/Users/zettergm/simulations/ssd/figments_misty_3Dx_2048_36_long/gemini_output_hdf5/"
if not os.path.isdir(outdirec):
    os.mkdir(outdirec)
filelist=os.listdir(direc)
filelist.sort()
filelist=filelist[1:]     # get rid of mac OS file

for filename in filelist: 
    filenamefull=direc+filename
    print("Reading vtu file:  "+filenamefull)
    data, centers, nodes = vtu2regular.read_vtu(filenamefull)
    iparm=np.array([6,13,20,27,28,34],dtype=np.int32)            # parameter number, must be int
    lpts=np.array([384,384,384],dtype=np.int32)    # size of target grid, must be int
    print("Resampling GEMINI data...")
    # mlims=np.array([90e3,500e3,-155,-145,25,33])    # extent of interpolation region, double
    # alti,mloni,mlati,parmi = vtu2regular.sample_gemini(data,centers,parmids=iparm,
    #                                                    lpts=lpts,lims=mlims,
    #                                                    targettype="geomagnetic")
    glims=np.array([90e3,500e3,136,150,33,43])    # magnetic extent of interpolation region, double
    alti,mloni,mlati,parmi = vtu2regular.sample_gemini(data,centers,parmids=iparm,
                                                   lpts=lpts,lims=glims,
                                                   targettype="geographic")
    
    # Write the uniformly sampled data to a file
    coordlbls=["alti","mloni","mlati"]
    parmlbls=["ne","v1","v2","v3","Ti","Te"]
    filenamefullhdf5 = outdirec+filename+".hdf5"
    print("Writing hdf file:  "+filenamefullhdf5)
    vtu2regular.write_sampled(alti,mloni,mlati,coordlbls,parmi,parmlbls,filenamefullhdf5)


