# Setting Up an Ionic Liquid System in LAMMPS Using MolTemplate and PackMol

Please refer to the included pdf presentation for a schematic of the general workflow till this file is updated.


## Pre-Requisites:
1. PackMol installation (install following the instructions in the [PackMol Repository](https://github.com/m3g/packmol))
1. MolTemplate installation (install following the instructions in the [MolTemplate Repository](https://github.com/jewettaij/moltemplate/blob/master/INSTALL.md))
1. LAMMPS and Amber modules (can be installed locally or loaded as modules from the computing cluster for Notre Dame CRC users)


## Instructions:

1. Create `molecule.lt` files for every residue/molecule in your system.
    a. Navigate to the directory `C2M-TF2/creating-mol-lt-files` in your terminal.
    ```
    cd C2M-TF2/creating-mol-lt-files
    ```
    b. Convert the shell scripts into executables
    ```
    dos2unix *.sh   # in case the file was edited on a windows machine
    chmod +x *.sh
    ```
    c. Convert the `pdb` files to `mol2` files.
    ```
    ./run_pdb2mol2.sh
    ```
    d. Convert `mol2` files into MolTemplate `.lt` files
    ```
    ./run_mol22lt.sh
    ```

1. Pack the system and run MolTemplate (combnied in 1 executable).
    a. Navigate to the directory `C2M-TF2/packmol+moltemplate` in your terminal.
    ```
    cd C2M-TF2/creating-mol-lt-files
    ```
    b. Convert the shell scripts into executables
    ```
    dos2unix *.sh   # in case the file was edited on a windows machine
    chmod +x *.sh
    ```
    c. Run the `create_sys.sh` executable
    ```
    ./create_sys.sh
    ```

## Notes:
1. `pdb` files can be downloaded from the [Protein Data Bank](https://www1.rcsb.org/), or other relevant repositories like [PubChem](https://pubchem.ncbi.nlm.nih.gov/). They can also be generated using various tools like [MolView](https://molview.org/), [RDKit.py](https://github.com/rdkit/rdkit) or Open Babel. An example script for generating `pdb` files using RDKit is available at: `C2M-TF2/creating-mol-lt-files/generate-pdb.py`