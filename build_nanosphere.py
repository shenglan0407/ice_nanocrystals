import os
import numpy as np

# first decide which model of ice to use and load it's unit cell length
ice = 'ice_models/1.cif'
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

# now make a box that's at least as wide as the sphere in it's shortest dimension
radius = 5.0 # radius in anstrom
na = int(radius*5./La)+1
nb = int(radius*5./(Lb/2.0))+1
nc = int(radius*5./Lc)+1

# create a temp file of the cubic box
os.system('python cif_to_xyz.py -i %s -o temp.xyz -b %d %d %d -r'%(ice,na,nb,nc))

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

with open('sphere.xyz','w') as sphere:
    sphere.write(str(len(atoms))+'\n')
    sphere.write('NP created from '+ice+'. '+box_line)
    for this_line in atoms:
        sphere.write(this_line)