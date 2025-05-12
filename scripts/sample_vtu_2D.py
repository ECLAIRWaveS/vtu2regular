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
direc="/Users/zettergm/simulations/sdcard/2DMAGIC_2DhalfGEMINI/gemini_output/"
filename=direc+"fort_frame_0020.vtu"
print("Reading vtu file:  "+filename)
data, centers, nodes = vtu2regular.read_vtu(filename)
iparm=np.array([13],dtype=np.int32)            # parameter number, must be int
lpts=np.array([256,256],dtype=np.int32)    # size of target grid, must be int
print("Resampling GEMINI data...")
mlims=np.array([90e3,500e3,25,33])    # magnetic extent of interpolation region, double


alti,mlati,parmi = vtu2regular.sample_gemini_2D(data,centers,parmids=iparm,
                                                   lpts=lpts)

# Make a plot
plt.figure(dpi=150)
plt.pcolormesh(mlati,alti/1e3,np.squeeze(parmi[:,:,0]))
plt.colorbar()
plt.xlabel("lat. (deg)")
plt.ylabel("alt. (km) ")
plt.show()
