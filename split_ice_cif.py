import os
count = 0
outfilename = os.getcwd()+'/ice_models/'+str(count)+'.cif'
outfile=open(outfilename,'w')
new_outfile = False
with open(os.getcwd()+'/ice.cif','r') as infile:
    for line in infile:
        if len(line.split())>0 and line.split()[0] =='data_global':
            new_outfile = True
        if(new_outfile):
            outfile.close()
            count+=1
            outfilename = os.getcwd()+'/ice_models/'+str(count)+'.cif'
            outfile = open(outfilename,'w')
            
            new_outfile = False
        else:
            outfile.write(line)
outfile.close()

# remove empty file
os.remove(os.getcwd()+'/ice_models/0.cif')