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
import sys
import getopt

from thor import xray
import matplotlib.pyplot as plt
##############################################################################
# Code
##############################################################################
def usage():
    print './polar_intensities.py -i <mol_model> -o <outputfile> -q <qvalues> -p <nphi> -s <nshot> -n <nmol>'

def main(argv):
##############################################################################
# default settings
    sphere = "50.0_m1"

    # default simulation parameters
    n_shots = 10                      # total number of shots to do
    n_molecules = 1                     # the number of molecules to include per shot
    q_values = [1.71]  # the |q| values of the rings to sim
    n_phi = 360                         # number of pts around the rings
    
    output_file = "simulated_data/"+sphere+"_s"+str(n_shots)+'sc_2'+'.hdf5'
##############################################################################


    try:
        opts, args = getopt.getopt(argv,"hi:o:q:p:s:n:",["mol_model=","ofile=","qvalues=","nphi=","nshots=","nmol="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-i", "--mol_model"):
            sphere = arg
        elif opt in ("-o", "--ofile"):
            output_file = "simulated_data/%s.hdf5"%arg
        elif opt in ("-q", "--qvalues"):
            qs = arg.split('/')
            
            if len(qs) > 1:
                try:
                    q_values = np.arange(float(qs[0]),float(qs[1]),float(qs[2]))
                except ValueError:
                    print 'Enter lower bound, upper bound, step for q values, separated by /'
                    sys.exit(2)
            else:
                try:
                    q_values = [float(arg)]
                except ValueError:
                    print 'Enter a single value of q of a range of values separated by space'
                    sys.exit(2)
                
        elif opt in ("-p","--nphi"):
            n_phi = int(arg)
        
        elif opt in ("-s","--nshots"):
            n_shots = int(arg)
        
        elif opt in ("-n","--nmol"):
            n_molecules = int(arg)
            
    
    t=mdtraj.load('nanosphere/'+sphere+'.pdb')

    
    while os.path.isfile(output_file):
        print "Will not overwrite old file. Please enter new name:"
        output_file = "simulated_data/%s.hdf5"%raw_input()
##############################################################################
# print settings  
    print "Computing polar intensities for model %s"%sphere
    print "--> Num of snapshots: %d"%n_shots
    print "--> Num of molecules per snapshot: %d"%n_molecules
    print "--> q values: %s"%str(q_values)
    print "--> Num of phi between 0 and pi: %d"%n_phi
    print "Output saved in %s\n" %output_file

##############################################################################
# do the simulations
    rings = xray.Rings.simulate(t, n_molecules, q_values, n_phi, n_shots)

    # data to save
    PI=rings.polar_intensities
    phis=rings.phi_values
    qs=rings.q_values

    # save the data
    f = h5py.File(output_file,'a')
    f.create_dataset('polar_intensities',data=PI)
    f.create_dataset('phi_values',data=phis)
    f.create_dataset('q_values',data=qs)
    f['polar_intensities'].attrs.create('num_molecules',n_molecules)

    f.close()


if __name__ == "__main__":
   main(sys.argv[1:])
