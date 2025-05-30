#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 12 18:19:22 2025

@author: zettergm
"""

import vtu2regular
import matplotlib.pyplot as plt
import numpy as np

# Obtain the model data and cell center locations
direc="/Users/zettergm/simulations/sdcard/May2024_10t_jankblocker/gemini_output/burst/"
filename=direc+"fort_frame_0200.vtu"
print("Reading vtu file:  "+filename)
data, centers, nodes = vtu2regular.read_vtu(filename)
iparm=np.array([6,13],dtype=np.int32)            # parameter number, must be int
lpts=np.array([4096,4096],dtype=np.int32)    # size of target grid, must be int
print("Resampling GEMINI data...")
mlims=np.array([90e3,200e3,40.25,42.75])    # magnetic extent of interpolation region, double
alti,mlati,parmi = vtu2regular.sample_gemini_2D(data,centers,parmids=iparm,
                                                   lpts=lpts,lims=mlims)
mloni=np.array([])

# Write the uniformly sampled data to a file
coordlbls=["alti","mloni","mlati"]
parmlbls=["ne","v1"]
filename = filename+".hdf5"
vtu2regular.write_sampled(alti,mloni,mlati,coordlbls,parmi,parmlbls,filename)


# Make a plot
plt.figure(dpi=150)
plt.pcolormesh(mlati,alti/1e3,np.squeeze(parmi[:,:,-1]))
plt.colorbar()
plt.xlabel("lat. (deg)")
plt.ylabel("alt. (km) ")
plt.show()
