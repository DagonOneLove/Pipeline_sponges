import os
import subprocess

# Directories
script_dir = os.path.dirname(os.path.abspath(__file__))
faa_dir = os.path.abspath(os.path.join(script_dir, "../results/predicted_genes"))
hmm_dir = os.path.abspath(os.path.join(script_dir, "../data/hmms"))
out_dir = os.path.abspath(os.path.join(script_dir, "../results/hits"))

os.makedirs(out_dir, exist_ok=True)

# List files
hmm_files = [f for f in os.listdir(hmm_dir) if f.endswith(".hmm")]
faa_files = [f for f in os.listdir(faa_dir) if f.endswith(".faa")]

if not hmm_files:
    print("ERROR: No .hmm files in", hmm_dir)
    exit(1)
if not faa_files:
    print("ERROR: No .faa files in", faa_dir)
    exit(1)

# Run hmmsearch
for hmm in hmm_files:
    hmm_path = os.path.join(hmm_dir, hmm)
    gene_id = os.path.splitext(hmm)[0]

    for faa in faa_files:
        faa_path = os.path.join(faa_dir, faa)
        genome_id = os.path.splitext(faa)[0]

        output_file = os.path.join(out_dir, f"{genome_id}__{gene_id}.tbl")

        print(f"Searching {gene_id} in {genome_id}")
        subprocess.run([
            "hmmsearch",
            "--tblout", output_file,
            "--noali",
            hmm_path,
            faa_path
        ], check=True)
