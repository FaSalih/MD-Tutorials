#!/bin/bash

# ----------------------------------------------------------
# Source of Instructions: https://ambermd.org/tutorials/advanced/tutorial15/Tutorial2.php
# Amber Tutorial: Simulations of a room-temperature ionic liquid. By Chris Lim and David A Case
# Followed till step 5 - Generating the coordinate and topology files. Then used the amb2gro_top_gro.py tool to convert amber files to gromacs files.
# ----------------------------------------------------------

# Define arrays for system components and their net charges
res_names=('TF2' 'C2M')
charges=(-1 1)

# Load amber and ambertools
module load amber

for i in "${!res_names[@]}"
do

	# Start by creating directories for each of the residues you want to parametrize using GAFF
	res_name=${res_names[$i]}
	charge=${charges[$i]}

	res_folder=${res_name}-Amber
        mkdir ${res_folder}


	# Copy the raw pdb files into the new directory
	cp pdb-files/${res_name}.pdb ${res_folder}

	cd  ${res_folder}

	# Clean pdb file to remove unnnecessary fields
	pdb4amber -i ${res_name}.pdb -o ${res_name}_cleaned.pdb

	# Generate mol2 file
	antechamber -i ${res_name}_cleaned.pdb -fi pdb -o ${res_name}.mol2 -fo mol2 -c bcc -nc ${charge}

	# This is where you would edit charges in the mol2 file if necessary

	# Generate FF modification files if necessary (will be mostly empty if not needed)
	parmchk2 -i ${res_name}.mol2 -f mol2 -o frcmod.${res_name}

	# Back to parent folder
	cd ..

done
