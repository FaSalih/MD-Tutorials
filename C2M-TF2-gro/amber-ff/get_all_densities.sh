#!/bin/bash

# Run this conda activate command in the shell before running
# conda activate gromacs_env

# define list of temperatures
temps=( 293 298 303 308 313 318 323)

# remove old file if it exists
rm -f densities.txt

# create a file to store the densities with a header
echo "# Temperature (K), Avg Density (mg/mL), StD Density (mg/mL)" > densities.txt

# loop over all temperatures
for temp in "${temps[@]}"
do
    # enter equilibration directory
    cd ${temp}K/equilibrate_system/

    # run plot_gmx and save printed output to a varaible
    output=$(python plot_gmx.py 250)

    # extract last token from the output
    avg_density=$(echo "$output" | tail -n 2 | head -n 1)
    std_density=$(echo "$output" | tail -n 1)
    
    # save temperature and density to file
    echo "${temp}, ${avg_density}, ${std_density}" >> ../../densities.txt
    
    # go back to the parent directory
    cd ../../
done
