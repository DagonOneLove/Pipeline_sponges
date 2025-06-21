import os
import subprocess

# Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
input_dir = os.path.abspath(os.path.join(script_dir, "../results/extracted_seqs"))
output_dir = os.path.abspath(os.path.join(script_dir, "../results/aligned_genes"))
os.makedirs(output_dir, exist_ok=True)

# Align all .faa files with MAFFT
for fname in os.listdir(input_dir):
    if not fname.endswith(".faa"):
        continue

    input_path = os.path.join(input_dir, fname)
    output_path = os.path.join(output_dir, fname.replace(".faa", ".aligned.faa"))

    cmd = ["mafft", "--auto", "--reorder", input_path]
    print(f"Aligning {fname}...")

    with open(output_path, "w") as out_f:
        subprocess.run(cmd, stdout=out_f, stderr=subprocess.DEVNULL)

    print(f"Saved alignment to {output_path}")
