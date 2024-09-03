#!/bin/bash
#$ -q hpc
#$ -pe smp 16
#$ -N Example

module load lammps

mpirun -np ${NSLOTS} lmp_mpi -i example.lammps

mkdir dump-files
mv dump.* dump-files/
