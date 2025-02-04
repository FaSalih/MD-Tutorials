#!/bin/bash
#$ -M fsalih@nd.edu    # Email address for job notification
#$ -m abe              # Send mail when job begins, ends and aborts
#$ -pe smp 48 # Specify parallel environment and legal core size
#$ -q long              # Specify queue
#$ -N EQ-298K-HBET # Specify job name

module load gromacs

# Remove previous run files
rm *.edr *.trr mdout* *.log *.cpt *.xvg

# assign input variables
GroupNumber=0

# Define input and output names
output="equil"
input="anneal"
run_script="equilibrate"

# Copy all topology/forcefield files from create_system directory
cp ../../create_system/full_system.top .
cp ../../create_system/spce.itp .
cp ../anneal_system/$input.gro .

## MD Run
gmx grompp -v -f ${run_script}.mdp -c ${input}.gro -p full_system.top -o ${output}.tpr -maxwarn 2
mpirun gmx mdrun -v -s ${output}.tpr -deffnm ${output}

## Visualization
# # Create movie of trajectory
# echo $GroupNumber | gmx trjconv -pbc mol -s ${output}.tpr -f ${output}.trr -o video.gro

# Create xvg files from edr output
property_list=(Potential Kinetic-En. Total-Energy Pressure Temperature Density)
for property in ${property_list[@]}
do
   echo -e "${property} \n" | gmx energy -f ${output}.edr -o ${property}.xvg
done

# Create plots from xvg files
conda activate gromacs_env
window_size=100
python3 plot_gmx.py ${window_size}


