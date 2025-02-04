'''
Reads an input mol2 file and a desired net charge and 
checks if the net charge in the mol2 file is equal to the desired net charge.
'''

import pandas as pd
import sys
import numpy as np

# Read input args
mol2_file = sys.argv[1]
desired_net_charge = float(sys.argv[2])

# Get number of atoms from mol2 file header
with open(mol2_file) as f:
    for i, line in enumerate(f):
        if i == 2:
            num_atoms = int(line.split()[0])
            break
# Read mol2 file
df=pd.read_fwf(mol2_file, skiprows=8,sep='\t', nrows=15, header=None, 
               colspecs=[(1,8),(8,18), (18,28), (29,40), (40,50),
                          (50,54), (55, 63), (63,67), (68, 82)], 
                index_col=0, 
                col_names=['name', 'x', 'y', 'z', 'type', 'occ', 'resname', 'q'])