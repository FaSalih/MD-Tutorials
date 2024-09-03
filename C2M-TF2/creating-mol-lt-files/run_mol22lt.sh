#!/bin/bash

module load amber 

# Define arrays for system components and their net charges
res_names=('TF2' 'C2M')
charges=(-1 1)

for i in "${!res_names[@]}"
do

	# Start by creating directories for each of the residues you want to parametrize using GAFF
	res_name=${res_names[$i]}
	charge=${charges[$i]}

    # Enter folder containing residue.mol2 files
    res_folder=${res_name}-Amber
    cd ${res_folder}

    # ## Needs Debugging
    # # Create template of force field modification files
    # amber2lt.py --in frcmod.${res_name} --name ${res_name}_ForceField > ${res_name}_force_field.lt

    # # Convert mol2 files to lt files using the modified force field  files
    # mol22lt.py --in ${res_name}.mol2 --out ${res_name}.lt --name ${res_name} --ff ${res_name}_ForceField --ff-file ${res_name}_force_field.lt

    # Convert mol2 files to lt files
    mol22lt.py --in ${res_name}.mol2 --out ${res_name}.lt --name ${res_name} --ff GAFF2 --ff-file gaff2.lt

    # Save the lt files in the parent folder
    cp *.lt ../
    cd ..
done