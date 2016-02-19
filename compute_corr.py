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

f = h5py.File("simulated_data/50.0_m1_s10000sc_1.hdf5",'a')

PI=f['polar_intensities'][:]
phi=f['phi_values'][:]


n_shots=len(PI)
print n_shots
print len(PI[0][0])
stride=2


def calc_corr(shot, delta):
    
    return np.mean([shot[ii]*shot[ii+delta] for ii in range(len(phi)-delta)])
    
        

deltas = np.arange(0,len(phi),stride)
corr = np.zeros(len(deltas))
for this_shot in PI:
    corr =corr+[calc_corr(this_shot[0],delta) for delta in deltas]

# save the correlation data in the same hd5f file
f.create_dataset('intercorr',data=corr)
f.close()

#show a plot
plt.plot(deltas,corr)
plt.xlim(2,360)
plt.xlabel('phi(deg)')
plt.ylabel('Corr')
plt.show()

