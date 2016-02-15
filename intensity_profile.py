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
import mdtraj as md

from thor import xray
import matlibplot.pyplot as plt
##############################################################################
# Code
##############################################################################
t = mdtraj.load("nanosphere/50.0m1.pdb")


n_shots = 100                         # total number of shots to do
n_molecules = 1                     # the number of molecules to include per shot
q_values = np.arange(1.2,2.4,0.05)  # the |q| values of the rings to sim
n_phi = 360                         # number of pts around the rings

rings = xray.Rings.simulate(t, n_molecules, q_values, n_phi, n_shots)

# check the WAXS
plt.figure()

waxs = rings.intensity_profile() # first col is |q|, second is intensity

plt.plot(waxs[:,0], waxs[:,1], lw=2)
plt.xlabel(r'$q / \AA^{-1}$')
plt.ylabel('Intensity')
plt.show()
