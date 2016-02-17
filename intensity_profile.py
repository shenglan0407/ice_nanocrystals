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
import mdtraj
import h5py
import os

from thor import xray
import matplotlib.pyplot as plt
##############################################################################
# Code
##############################################################################
sphere = "50.0_m1"
t=mdtraj.load('nanosphere/'+sphere+'.pdb')

# simulation parameters
n_shots = 500                      # total number of shots to do
n_molecules = 512                     # the number of molecules to include per shot
q_values = [1.61]  # the |q| values of the rings to sim
n_phi = 360                         # number of pts around the rings


output_file = "simulated_data/"+sphere+"_s"+str(n_shots)+'.hd5f'
while os.path.isfile(output_file):
    print "Will not overwrite old file. Please enter new name:"
    outpu_file = rawinput()


# do the simulations
rings = xray.Rings.simulate(t, n_molecules, q_values, n_phi, n_shots)

# data to save
PI=rings.polar_intensities
phis=rings.phi_values
qs=rings.q_values

# save the data
f = h5py.File(output_file,'w')
f.create_dataset('polar_intensities',data=PI)
f.create_dataset('phi_values',data=phis)
f.create_dataset('q_values',data=qs)
f['polar_intensities'].attrs.create('num_molecules',n_molecules)

f.close()




# ring.save(output_file)
# 
# # check the WAXS
# plt.figure()
# 
# waxs = rings.intensity_profile() # first col is |q|, second is intensity
# 
# plt.plot(waxs[:,0], waxs[:,1], lw=2)
# plt.xlabel(r'$q / \AA^{-1}$')
# plt.ylabel('Intensity')
# plt.show()
