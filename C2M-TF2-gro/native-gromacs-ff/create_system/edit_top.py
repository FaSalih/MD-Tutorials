import sys

# read scaling factor from command line
sigma_scaling = float(sys.argv[1])

## Find molecule definition sections
moleculetype_idxs = []
moleculenames = []
# read topology file line by line
with open('full_system.top', 'r') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        # find all lines containing [ moleculetype ]
        if '[ moleculetype ]' in line:
            # find index of line containing [ moleculetype ]
            moleculetype_idxs.append(i)
            # find molecule name for that molecule type
            moleculename = lines[i+2].split()[0]
            moleculenames.append(moleculename)

## Edit water molecule definition section
# water molecule index
wat_idx = moleculenames.index('WAT')
# range of lines to replace
start_idx = moleculetype_idxs[wat_idx]
end_idx = moleculetype_idxs[wat_idx+1]

# read topology file 
with open('full_system.top', 'r') as f:
    lines = f.readlines()

# edit water molecule definition section
lines[start_idx] = '; include SPCE water model\n'
lines[start_idx+1] = '#include "spce.itp"\n'
lines[start_idx+2:end_idx] = ['\n']

# ----------------------------------------------
## Edit atom definition section
# read topology file line by line to find atomtype line
with open('full_system.top', 'r') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        # find all lines containing [ atomtypes ]
        if '[ atomtypes ]' in line:
            # find index of line containing [ atomtypes ]
            atomtype_idx = i
            break

# edit atom section
atom1_idx = atomtype_idx + 2
atomN_idx = atomtype_idx + 2 + 10
for i in range(atom1_idx, atomN_idx+1):
    # split line into columns
    line = lines[i].split()
    # get atom type
    atomtype = line[0]
    # get atom sigma
    sigma = float(line[5])
    # if atom belongs to water skip it
    if atomtype in ['oh', 'ho']:
        sigma *= 1.0 # no sigma scaling for established SPCE water model
    else:
        # scale sigma
        sigma *= sigma_scaling
    # change sigma in line
    line[5] = f'{sigma:.6f}'
    # write line back to file
    lines[i] = f'{line[0]:<12}{line[1]:>3}{line[2]:>12}{line[3]:>12}{line[4]:>3}{line[5]:>15}{line[6]:>15}\n'

## Save edited topology file
with open('full_system.top', 'w') as f:
    f.writelines(lines)