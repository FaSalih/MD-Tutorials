#!/bin/bash

# This script is used to submit all the temperature runs for a given system.
temps=( 293 298 303 308 313 318 323)

# submit all annealing jobs
for temp in "${temps[@]}"
do
    # enter annealing directory
    cd ${temp}K/anneal_system/

    # check if results are already present
    if [ -f 'Energies.png' ]; then
        echo "Annealing already completed for ${temp}K"
        cd ../../
        continue
    fi
    
    # submit annealing job
    qsub run.sh

    # go back to the parent directory
    cd ../../
done

# submit all equilibration jobs
for temp in "${temps[@]}"
do
    # check if annealing is finished (if results are present)
    if [ ! -f ${temp}K/anneal_system/Energies.png ]; then
        echo "Annealing not completed for ${temp}K"
        continue
    fi
    
    # enter equilibration directory
    cd ${temp}K/equilibrate_system/
    
    # check if equilibration is already completed
    if [ -f 'equil.gro' ]; then
        echo "Equilibration already completed for ${temp}K"
        cd ../../
        continue
    fi

    # submit equilibration job
    qsub run.sh

    # go back to the parent directory
    cd ../../
done