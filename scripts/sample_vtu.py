#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 16:49:24 2023

This shows how to read a forestgemini output vtu file into python and do some 
basic interpolation and plotting operations on it.  

@author: zettergm
"""

import vtu2regular
import matplotlib.pyplot as plt
import numpy as np

# Obtain the model data and cell center locations
#filename="/Users/zettergm/simulations/ssd/figments_misty_3Dx_512_23/gemini_output/fort_frame_0028.vtu"
direc="/Users/zettergm/simulations/ssd/misty_NM_256_quasistatic/gemini_output/"
filename=direc+"fort_frame_0020.vtu"
print("Reading vtu file:  "+filename)
data, centers, nodes = vtu2regular.read_vtu(filename)
iparm=np.array([13],dtype=np.int32)            # parameter number, must be int
lpts=np.array([256,256,256],dtype=np.int32)    # size of target grid, must be int
print("Resampling GEMINI data...")
mlims=np.array([90e3,500e3,-155,-145,25,33])    # magnetic extent of interpolation region, double
#alti,mloni,mlati,parmi = vtu2regular.sample_gemini(data,centers,parmids=iparm,
#                                                   lpts=lpts,lims=mlims,
##                                                   targettype="geomagnetic")
glims=np.array([90e3,500e3,249,258,29,36])    # magnetic extent of interpolation region, double
alti,mloni,mlati,parmi = vtu2regular.sample_gemini(data,centers,parmids=iparm,
                                                   lpts=lpts,lims=glims,
                                                   targettype="geographic")
#alti,mloni,mlati,parmi = vtu2regular.sample_gemini(data,centers,parmids=iparm,
#                                                   lpts=lpts,
#                                                   targettype="geographic")

# Write the uniformly sampled data to a file
coordlbls=["alti","mloni","mlati"]
parmlbls=["v1"]
filename = filename+".hdf5"
vtu2regular.write_sampled(alti,mloni,mlati,coordlbls,parmi,parmlbls,filename)


# Make a plot
plt.subplots(1,3,dpi=100)

plt.subplot(1,3,1)
plt.pcolormesh(mloni,alti/1e3,parmi[:,:,lpts[2]//2,0])
plt.colorbar()
plt.xlabel("lon. (deg)")
plt.ylabel("alt. (km) ")

plt.subplot(1,3,2)
plt.pcolormesh(mlati,alti/1e3,np.squeeze(parmi[:,lpts[1]//2,:,0]))
plt.colorbar()
plt.xlabel("lat. (deg)")
plt.ylabel("alt. (km) ")

plt.subplot(1,3,3)
altref=300e3
ialt=np.argmin(abs(alti-altref))
plt.pcolormesh(mloni,mlati,np.squeeze(parmi[ialt,:,:,0]).transpose())
plt.colorbar()
plt.xlabel("lon. (deg)")
plt.ylabel("lat. (deg) ")

plt.show()


###############################################################################
# x=centers[:,0]
# y=centers[:,1]
# z=centers[:,2]
# parm=data[:,13]   #parallel velocities


# # Express the source coordinates in a magnetic coordinate system for plotting
# r=np.sqrt(x**2+y**2+z**2)
# rho=np.sqrt(x**2+y**2)
# theta=np.arccos(z/rho)
# phi=np.arctan2(y,x)
# mlat=90-theta*180/np.pi
# mlon=phi*180/np.pi
# alt=r-Re


# # Create a regular mesh spanning range 
# lalti=384
# lloni=192
# llati=384
# print("Defining regular set of interpolation sites of size ",lalti," ",lloni," ",llati)
# #alti=np.linspace(alt.min(),alt.max(),lalti)
# #mloni=np.linspace(mlon.min(),mlon.max(),lloni)
# #mlati=np.linspace(mlat.min(),mlat.max(),llati)
# alti=np.linspace(90e3,500e3,lalti)
# mloni=np.linspace(-153,-147,lloni)
# mlati=np.linspace(26,32,llati)
# [ALTi,MLONi,MLATi]=np.meshgrid(alti,mloni,mlati,indexing="ij")   # we want target interpolation sites to be a grid in alt,mlon,mlat


# # for purposes of interpolation we need to pass interpolation sites in Cartesian; 
# #   elsewise the nearest neighbor gets a bit weird since it is compuuting distances
# #   using coordinates with different units
# THETAi=np.pi/2-MLATi*np.pi/180
# PHIi=MLONi*np.pi/180
# Ri=ALTi+Re
# Zi=Ri*np.cos(THETAi)
# Xi=Ri*np.sin(THETAi)*np.cos(PHIi)
# Yi=Ri*np.sin(THETAi)*np.sin(PHIi)


# # Use scipy to interplate to regular grid, note linear or better interpolation is miserably slow to the point of being useless
# print("Scattered interpolation of data...")
# #parmi = griddata((alt,mlon,mlat), parm, (ALTi.flatten(order="F"),MLONi.flatten(order="F"),MLATi.flatten(order="F")), 
# #                 method="nearest", fill_value=np.nan)
# #parmi=parmi.reshape((lalti,lloni,llati),order="F")
# #parmi = griddata((alt,mlon,mlat), parm, (ALTi,MLONi,MLATi),method="nearest")
# parmi = griddata((x,y,z), parm, (Xi.flatten(order="F"),Yi.flatten(order="F"),Zi.flatten(order="F")),method="nearest")
# parmi=parmi.reshape((lalti,lloni,llati),order="F")
###############################################################################