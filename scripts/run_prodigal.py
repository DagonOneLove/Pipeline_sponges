import os
import subprocess

# Define absolute paths
script_dir = os.path.dirname(os.path.abspath(__file__))
genomes_dir = os.path.abspath(os.path.join(script_dir, "../data/genomes"))
output_dir = os.path.abspath(os.path.join(script_dir, "../results/predicted_genes"))

# Print paths for verification
print("GENOMES_DIR =", genomes_dir)
print("OUTPUT_DIR  =", output_dir)

# Check that genomes directory exists
if not os.path.exists(genomes_dir):
    print("ERROR: Genome directory does not exist:", genomes_dir)
    exit(1)

# Make output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Find input genome files
genome_files = [f for f in os.listdir(genomes_dir) if f.endswith((".fna", ".fa", ".fasta"))]

if not genome_files:
    print("ERROR: No .fna/.fa/.fasta files found in:", genomes_dir)
    exit(1)

# Run Prodigal for each genome
for fname in genome_files:
    input_path = os.path.join(genomes_dir, fname)
    output_path = os.path.join(output_dir, os.path.splitext(fname)[0] + ".faa")

    print("Running Prodigal for:", fname)
    print("Command: prodigal -i", input_path, "-a", output_path, "-p meta")

    try:
        subprocess.run([
            "prodigal",
            "-i", input_path,
            "-a", output_path,
            "-p", "meta"
        ], check=True)
        print("Done:", output_path)
    except subprocess.CalledProcessError as e:
        print("ERROR: Prodigal failed on", fname)
        print("Exit code:", e.returncode)
