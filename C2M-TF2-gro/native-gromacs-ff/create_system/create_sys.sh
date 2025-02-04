#!/bin/bash

# Go to build_Amber
cd build_system_Amber

# Remove windows-style line endings
dos2unix antechamber_commands.sh

# Run Antechamber commands
chmod +x antechamber_commands.sh
./antechamber_commands.sh 

# Move results to parent folder
cp full_system.amb2gro/full_system.top ..
cp full_system.amb2gro/full_system.gro ..

# Go back to parent folder
cd ..

# # Change full_system.top to include SPCE water model instead of the natively defined WAT residue 
# # and to scale IL charges and sigma
# python edit_top.py $sigma_scaling