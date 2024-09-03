"""
Generate an optimized pdb file from SMILES string.

Notes:
- SMILES strings can be found among the molecular identifiers in PubChem or can be generated from a molecule drawing tool like molview.org
- The residue may not be recognized by rdkit so the residue name in the pdb file will appear as unknown. I normally change this manually to the 3-letter residue name I want.
"""
import os
from rdkit import Chem
from rdkit.Chem import AllChem 
from rdkit.Chem import Draw

# Define residue name and create molecule from smiles string
mol_name = "C2M"
m = Chem.MolFromSmiles('CCN1C=C[N+](=C1)C')
# mol_name = "TF2"
# m = Chem.MolFromSmiles('C(F)(F)(F)S(=O)(=O)[N-]S(=O)(=O)C(F)(F)F')

# add hydrogens and calculate partial charges
m = Chem.AddHs(m)
AllChem.ComputeGasteigerCharges(m)

# Make a directory to store the charges and images
os.makedirs("rdkit-charges-and-imgs", exist_ok=True)

# Print charge info to file
with open(f"rdkit-charges-and-imgs/{mol_name}-charges.txt", "w") as f:
    # Write header
    f.write("Atom_idx, Charge\n")

    # initialize total charge 
    q_sum = 0

    # loop over atoms and get charge
    for atom in m.GetAtoms():
        # Change atom label to atom index (useful for seeing atom indices in the image)
        atom_idx = atom.GetIdx()
        atom.SetProp('atomLabel', str(atom_idx))
        # Get atomic charge
        q = m.GetAtomWithIdx(atom_idx).GetDoubleProp('_GasteigerCharge')
        print(f'Atom {atom_idx} has charge {q}')
        q_sum += q
        # write charge to file
        f.write(f"{atom_idx}, {q}\n")

    f.write(f"\n#Total charge = {q_sum}")

print(f'\nTotal charge = {q_sum}')

# Generate the molecule image
img = Draw.MolToImage(m, kekulize=True)
# Save 2D molecule image to file
img.save(f"rdkit-charges-and-imgs/numbered_{mol_name}.png")

# Optimize the geometry
AllChem.EmbedMolecule(m)
AllChem.MMFFOptimizeMolecule(m)

# Generate the molecule pdb file
Chem.MolToPDBFile(m, f"pdb-files/{mol_name}.pdb", )



