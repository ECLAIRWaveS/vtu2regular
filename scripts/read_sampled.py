#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 10:12:37 2025

@author: zettergm
"""

import h5py
import matplotlib.pyplot as plt

file="/Volumes/MZdata/May2024_10t_jankblocker/gemini_output/burst_hdf5/fort_frame_0150.vtu.hdf5"

f = h5py.File(file,"r")
alt = f["x1i"][:]
mlat = f["x3i"][:]
coordlbls=f["coordlbls"][:]
parmlbls=f["parmlbls"][:]
parms=f["parmi"][:]
ne=parms[:,:,0]
v1=parms[:,:,1]

plt.subplots(1,2,dpi=200)

plt.subplot(1,2,1)
plt.pcolormesh(mlat,alt/1e3,v1)
plt.ylabel("alt. (km)")
plt.xlabel("mlat. (deg)")

plt.subplot(1,2,2)
plt.pcolormesh(mlat,alt/1e3,ne)
plt.ylabel("alt. (km)")
plt.xlabel("mlat. (deg)")

plt.show()

