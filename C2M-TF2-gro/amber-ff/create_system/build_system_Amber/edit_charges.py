"""
To be run AFTER charge scaling to ensure the total charge on each ion is equal to the charge scaling factor.
"""

import numpy as np
import pandas as pd
import os   
import shutil
import sys

edited_mols = 0

q_scaling = float(sys.argv[1])
res_name = sys.argv[2]

# res_names = ['GLY', 'TF2', 'WAT']
# res_name = res_names[0]
# n_atoms = [20, 15, 3]

folder = f'{res_name}-Amber/'
folder = ''

## Calculate current charge on each residue
# read totpology file line by line
with open(f'{folder}{res_name}.mol2', 'r') as f:
    lines = f.readlines()
    for i,line in enumerate(lines):
        # skip first 9 lines
        if i < 8:
            continue
        # check total charge on GLY residue
        if res_name == 'GLY':
            q_tot = 0
            # go to atoms section and loop over atoms
            for a in range(20):
                line = lines[i+a].split()
                # get current charge
                q = float(line[8])
                q_tot += q
            break
        # check total charge on TF2 residue
        elif res_name == 'TF2':
            q_tot = 0
            # go to atoms section and loop over atoms
            for a in range(15):
                line = lines[i+a].split()
                # get current charge
                q = float(line[8])
                q_tot += q
            break
        # check total charge on WAT residue
        elif res_name == 'WAT':
            q_tot = 0
            # go to atoms section and loop over atoms
            for a in range(3):
                line = lines[i+a].split()
                # get current charge
                q = float(line[8])
                q_tot += q
            break
        else:
            continue

## Fix charges
# check if total charge is equal to scaling factor
if np.abs(q_tot) != q_scaling:
    print(f'Total charge on {res_name} residue is {q_tot}, scaling factor is {q_scaling}.')
    print(f'Fixing charges...')

# get desired charge for residue
if res_name == 'GLY':
    q_des = q_scaling
elif res_name == 'TF2':
    q_des = -1*q_scaling
elif res_name == 'WAT':
    q_des = 0

# find charge to add
q_add = q_des - q_tot

# if for Gly residue, split the charge between 3 c3-type atoms
if res_name == 'GLY':
    q_add /= 3

# read topology file line by line
with open(f'{folder}{res_name}.mol2', 'r') as f:
    lines = f.readlines()
    for i,line in enumerate(lines):
        line = line.split()
        # skip first 9 lines
        if i < 8:
            continue
        # edit charge on c3-type atoms in Gly residues
        if res_name == 'GLY':
            num_edited_atoms = 0
            # go to atoms section and loop over atoms
            for a in range(20):
                if num_edited_atoms == 3:
                    break
                line = lines[i+a].split()
                # find C3-type atoms
                if line[5] == 'c3':
                    # get current charge
                    q = float(line[8])
                    # change charge
                    line[8] = f'{q + q_add:.6f}'
                    # write line back to file
                    lines[i+a] = f'{line[0]:>7} {line[1]:<8}{line[2]:>11}{line[3]:>11}{line[4]:>11} {line[5]:<2}{line[6]:>10} {line[7]:>3}{line[8]:>15}\n'
                    num_edited_atoms += 1
                else:
                    continue
            break
        # edit charge on ne-type atoms in TF2 residues
        elif res_name == 'TF2':
            # go to atoms section and loop over atoms
            for a in range(15):
                line = lines[i+a].split()
                # find NE-type atoms
                if line[5] == 'ne':
                    # get current charge
                    q = float(line[8])
                    # change charge
                    line[8] = f'{q + q_add:.6f}'
                    # write line back to file
                    lines[i+a] = f'{line[0]:>7} {line[1]:<8}{line[2]:>11}{line[3]:>11}{line[4]:>11} {line[5]:<2}{line[6]:>10} {line[7]:>3}{line[8]:>15}\n'
            break
        # edit charge on all atoms in WAT residues to SPC/E water charges
        elif res_name == 'WAT':
            # go to atoms section and loop over atoms
            for a in range(3):
                line = lines[i+a].split()
                if line[5] == 'oh':
                    # change charge 
                    line[8] = '-0.847600'
                    # write line back to file 
                    lines[i+a] = f'{line[0]:>7} {line[1]:<8}{line[2]:>11}{line[3]:>11}{line[4]:>11} {line[5]:<2}{line[6]:>10} {line[7]:>3}{line[8]:>15}\n'
                elif line[5] == 'ho':
                    # change charge
                    line[8] = '0.423800'
                    # write line back to file in fixed-width format 
                    lines[i+a] = f'{line[0]:>7} {line[1]:<8}{line[2]:>11}{line[3]:>11}{line[4]:>11} {line[5]:<2}{line[6]:>10} {line[7]:>3}{line[8]:>15}\n'
            break
        else:
            continue

# write lines back to file
with open(f'{folder}{res_name}.mol2', 'w') as f:
# with open(f'{folder}{res_name}_edited.mol2', 'w') as f:
    f.writelines(lines)