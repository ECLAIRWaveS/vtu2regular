#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 30 10:53:53 2025

@author: zettergm
"""


import vtu2regular
import numpy as np
import os

# Obtain the model data and cell center locations
direc="/Volumes/T9/simulations_AIRWaveS/May2024_10t_jankblocker/gemini_output/burst/"
outdirec="/Volumes/T9/simulations_AIRWaveS/May2024_10t_jankblocker/gemini_output/burst_hdf5/"
if not os.path.isdir(outdirec):
    os.mkdir(outdirec)
filelist=os.listdir(direc)
filelist.sort()
#filelist=filelist[1:]     # get rid of mac OS file

for filename in filelist: 
    filenamefull=direc+filename
    print("Reading vtu file:  "+filenamefull)
    data, centers, nodes = vtu2regular.read_vtu(filenamefull)
    
    iparm=np.array([6,13],dtype=np.int32)            # parameter number, must be int
    lpts=np.array([10000,15000],dtype=np.int32)    # size of target grid, must be int
    print("Resampling GEMINI data...")
    mlims=np.array([90e3,350e3,39.5,43.5])    # magnetic extent of interpolation region, double
    alti,mlati,parmi = vtu2regular.sample_gemini_2D(data,centers,parmids=iparm,
                                                       lpts=lpts,lims=mlims)
    mloni=np.array([])
    
    # Write the uniformly sampled data to a file
    coordlbls=["alti","mloni","mlati"]
    parmlbls=["ne","v1"]
    filenamefullhdf5 = outdirec+filename+".hdf5"
    print("Writing hdf file:  "+filenamefullhdf5)
    vtu2regular.write_sampled(alti,mloni,mlati,coordlbls,parmi,parmlbls,filenamefullhdf5)
    