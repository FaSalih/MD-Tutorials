#!/bin/bash

#------------------------------------------------------------
## Create configuration using packmol
# Copy pdb files into local directory
cp ../creating-mol-lt-files/pdb-files/*.pdb .

# Run Packmol
packmol < full_sys.inp

#------------------------------------------------------------
## Create data file
# Copy component lt files into local directory
cp ../creating-mol-lt-files/*.lt .

# Run moltemplate
moltemplate.sh  -pdb system.pdb system.lt

