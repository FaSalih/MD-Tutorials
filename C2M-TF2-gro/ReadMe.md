# Setting Up an Ionic Liquid System in GROMACS Using Amber and PackMol


## Pre-Requisites:
1. PackMol installation (install following the instructions in the [PackMol Repository](https://github.com/m3g/packmol))
1. MolTemplate installation (install following the instructions in the [MolTemplate Repository](https://github.com/jewettaij/moltemplate/blob/master/INSTALL.md))
1. GROMACS and Amber modules (can be installed locally or loaded as modules from the computing cluster for Notre Dame CRC users)


## Instructions:

1. Create GROMACS coordinate and topology files (`full_system.gro` and `full_system.top`, respectively).

    a. Navigate to the directory `C2M-TF2-gro/amber-ff/create_system` in your terminal.
    ```
    cd C2M-TF2-gro/amber-ff/create_system
    ```
    b. Convert the shell scripts into executables
    ```
    dos2unix *.sh   # in case the file was edited on a windows machine
    chmod +x *.sh
    ```
    c. Create the system files.
    ```
    ./create_sys.sh
    ```

1. Copy necessary topology and coordinate files to `minimize_system` directory and run GROMACS minimization.

    a. Navigate to the directory `C2M-TF2-gro/amber-ff/minimize_system` in your terminal.
    ```
    cd C2M-TF2-gro/amber-ff/minimize_system
    ```
    b. Run the shell script `run.sh` or submit to a computing cluster.
    ```
    dos2unix *.sh   # in case the file was edited on a windows machine
    chmod +x *.sh
    # ./run.sh 
    # OR:
    # qsub run.sh
    ```

## Notes:
1. `pdb` files can be downloaded from the [Protein Data Bank](https://www1.rcsb.org/), or other relevant repositories like [PubChem](https://pubchem.ncbi.nlm.nih.gov/). They can also be generated using various tools like [MolView](https://molview.org/), [RDKit.py](https://github.com/rdkit/rdkit) or Open Babel. An example script for generating `pdb` files using RDKit is available at: `C2M-TF2-gro/amber-ff/create_system/build_system_Amber/pdb-files/generate-pdb.py`

2. Different force field templates can be found in the `${INSTALLATION-DIR}/moltemplate/moltemplate/force_fields` folder. Additional force field templates can be added from online sources.