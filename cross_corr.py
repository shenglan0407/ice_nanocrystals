#! /usr/bin/env python

##############################################################################
# Copyright 2015 Stanford University and the Author
#
# Author: Shenglan Qiao
#
#
#
#############################################################################


##############################################################################
# Imports
##############################################################################

import numpy as np

import h5py
import os

import matplotlib.pyplot as plt
##############################################################################
# Code
##############################################################################

# f1 = h5py.File("simulated_data/50.0_m1_s10000sc_1.hdf5",'a')
f2 = h5py.File("simulated_data/50.0_m1_s10000sc_2.hdf5",'a')

# PI1=f1['polar_intensities'][:]
PI=f2['polar_intensities'][:]
phi=f2['phi_values'][:]


n_shots=len(PI)
print n_shots
print len(PI[0][0])
stride=2


def calc_corr(shot1,shot2, delta):
    
    return np.mean([shot1[ii]*shot2[ii+delta] for ii in range(len(phi)-delta)])
    
        

deltas = np.arange(0,len(phi),stride)
corr = np.zeros(len(deltas))
for shots in PI:
    corr =corr+[calc_corr(shots[0],shots[1],delta) for delta in deltas]

# save the correlation data in the same hd5f file
f2.create_dataset('crosscorr_all',data=corr)
f2.close()

#show a plot
plt.plot(deltas,corr)
plt.xlim(2,360)
plt.xlabel('phi(deg)')
plt.ylabel('Corr')
plt.show()

