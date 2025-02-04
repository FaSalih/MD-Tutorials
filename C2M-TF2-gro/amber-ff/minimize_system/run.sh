#!/bin/bash
#$ -M fsalih@nd.edu    # Email address for job notification
#$ -m abe              # Send mail when job begins, ends and aborts
#$ -pe smp 24           # Specify parallel environment and legal core size
#$ -q long        # Specify queue
#$ -N MIN-HBET               # Specify job name

module load gromacs

# Define if second minimization should be run
min2=false

# Define input and output names
if [ ${min2} == "true" ]; then
    output="min0"
    echo "Second minimization will be run. First output name is ${output}"
else
    output="min"
    echo "Second minimization will NOT be run. Output name is ${output}"
fi
input="full_system"
run_script="minimize"

rm *.top *.gro *.itp mdout* *.edr *.log *.tpr *.trr *.xtc *.cpt *.xvg

# Copy all topology/forcefield files from create_system directory
cp ../create_system/full_system.top .
cp ../create_system/$input.gro .

## MD Run
gmx grompp -v -f ${run_script}.mdp -c ${input}.gro -p full_system.top -o ${output}.tpr
mpirun gmx mdrun -v -s ${output}.tpr -deffnm  ${output}

## Visualization
# Define group number to visulaize 
GroupNumber=0       # 0 = entire system

# # Create movie of trajectory
# echo $GroupNumber | gmx trjconv -pbc mol -s ${output}.tpr -f ${output}.trr -o video.gro

# Create xvg files from edr output
property_list=(Potential Kinetic-En. Total-Energy Pressure Temperature Density)
for property in ${property_list[@]}
do
    if [ ${min2} == "true" ]; then
        property_name=${property}_min0
    else
        property_name=${property}
    fi
    echo -e "${property} \n" | gmx energy -f ${output}.edr -o ${property_name}.xvg
done

# Create plots from xvg files
conda activate gromacs_env
window_size=10
python3 plot_gmx.py ${window_size}

# ------------------------------------------------
## Optional second minimization

# check if min2 is true
if [ ${min2} == "true" ]; then
    # Deactivate plotting environment
    conda deactivate 
    conda activate base

    # Define input and output names
    output="min"
    input="min0"
    run_script="minimize2"

    ## MD Run
    gmx grompp -v -f ${run_script}.mdp -c ${input}.gro -p full_system.top -o ${output}.tpr
    mpirun gmx mdrun -v -s ${output}.tpr -deffnm  ${output}

    ## Visualization
    # Define group number to visulaize 
    GroupNumber=0       # 0 = entire system

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
    window_size=10
    python3 plot_gmx.py ${window_size}
fi