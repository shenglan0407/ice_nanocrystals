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

import os
import numpy as np
import sys

import getopt

##############################################################################
# Code
##############################################################################
def usage():
    print "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *\n"
    print './build_nanosphere.py -i <ice_model> -r <radius> -d'
    print "Builds a spherical ice structure with radius r given a crystollogrphical model"
    print "radius: in angstrom for the final structure."
    print "ice_model: path/to/cif/file, strutucre of unitcell recorded in cif format."
    print "-d flag deletes temp file of intermediate cubic structure. \n"
    print "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * "
    

def main(argv):
    #default model is Ih1
    ice = 'ice_models/1.cif'
    radius = 10.0 # default is 10 angstrom
    delete_temp = False # will not delete temp.xyz by default
    
    try:
        opts, args = getopt.getopt(argv,"hi:r:d",["ice_model=","radius="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-i", "--ice_model"):
            
            if os.path.isfile(arg):
                ice = arg
            else:
                print "Model does not exist. Try again!"
                exit(2)
        elif opt in ("-r", "--radius"):
            try:
                radius = float(arg)
                
                if radius < 0.0:
                    print "Radius must be greater than zero. Try again!"
                    exit(2)
                    
            except ValueError:
                print "Radius must be a number. Try again!"
                exit(2)
        elif opt in ("-d"):
            delete_temp = True

    with open(ice,'r') as ice_model:
        for line in ice_model:
            cols = line.split()
            if len(cols)==0: continue

            # if there are stuff in the line
            if (cols[0] == '_cell_length_a'):
                La = float(cols[1])

            elif (cols[0] == '_cell_length_b'):
                Lb = float(cols[1])

            elif (cols[0] == '_cell_length_c'):
                Lc = float(cols[1])

            elif (cols[0] == '_chemical_name_mineral'):
                model_name = str(cols[1])

    # now make a box big enough to contain the sphere
    na = int(radius*3./La)+1
    nb = int(radius*3./(Lb/2.0))+1
    nc = int(radius*3./Lc)+1

    # create a temp file of the cubic box
    os.system('python cif_to_xyz.py -i %s -o nanosphere/temp.xyz -b %d %d %d -r'%(ice,na,nb,nc))

    #load the temp file and 

    with open('nanosphere/temp.xyz','r') as temp:
        atoms=[]
        count = 0
        for line in temp:
            count+=1
            if count==1: continue 
            if count == 2:
                cols = line.split('. ') 
                center = np.array(cols[1].split()[1:],dtype=float)
                box_line = cols[-1] 
                continue
            #print box_line
            cols = line.split()
        
        
            xyz=np.array(cols[1:], dtype=float)


            if np.linalg.norm(xyz-center)<radius:
                atoms.append(line)
                
    # write .xyz file of sphere for visualization
    with open('nanosphere/'+str(radius)+'_m'+ice.split('/')[-1].split('.')[0]+'.xyz','w') as sphere:
        sphere.write(str(len(atoms))+'\n')
        sphere.write('NP created from '+ice+'. '+box_line)
        for this_line in atoms:
            sphere.write(this_line)
            
    # write coor format, input for thor
    with open('nanosphere/'+str(radius)+'_m'+ice.split('/')[-1].split('.')[0]+'.coor','w') as sphere:
        for this_line in atoms:
            cols = this_line.split()
            if cols[0] == 'O':
                # atomic number of oxygen
                Z = 8
            else:
                # atomic number of hydrogne
                Z = 1
            sphere.write('%s %s %s %d\n'%(cols[1],cols[2],cols[3],Z))
            
    # write pdb format, input for thor
    with open('nanosphere/'+str(radius)+'_m'+ice.split('/')[-1].split('.')[0]+'.pdb','w') as sphere:
        sphere.write('%s        %d \n' % ('MODEL' , 1))
        count = 0
        for this_line in atoms:
            count+=1
            cols = this_line.split()
            
            
            sphere.write("%6s%5d %4s %3s %1s%4d%1s   %8.3f%8.3f%8.3f%6.2f%6.2f          %2s  \n" % ('HETATM', count,cols[0],'HOH','I',1,' '
            ,float(cols[1]),float(cols[2]),float(cols[3]), 1.0, 0.0,'O'))
            
        sphere.write('%s \n' % 'ENDMDL')
    
    # if not keeping temp.xyz
    if delete_temp:
        os.system('rm nanosphere/temp.xyz')

if __name__ == "__main__":
   main(sys.argv[1:])