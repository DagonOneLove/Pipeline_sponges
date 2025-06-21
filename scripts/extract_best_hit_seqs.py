import os
import Bio
from Bio import SeqIO

# Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
faa_dir = os.path.abspath(os.path.join(script_dir, "../results/predicted_genes"))
parsed_dir = os.path.abspath(os.path.join(script_dir, "../results/parsed_hits"))
extracted_dir = os.path.abspath(os.path.join(script_dir, "../results/extracted_seqs"))

os.makedirs(extracted_dir, exist_ok=True)

# Group hits per gene (e.g. geneA.faa should contain all hits from all genomes)
gene_to_records = {}

# Loop through best hit files
for fname in os.listdir(parsed_dir):
    if not fname.endswith(".best_hit.txt"):
        continue

    # Get genome and gene IDs from filename
    parts = fname.replace(".best_hit.txt", "").split("__")
    genome_id = parts[0]
    gene_id = parts[1]

    # Read best hit protein ID
    best_hit_path = os.path.join(parsed_dir, fname)
    with open(best_hit_path) as f:
        line = f.readline().strip()
        if not line:
            continue
        protein_id = line.split("\t")[0]

    # Load .faa file for this genome
    faa_path = os.path.join(faa_dir, f"{genome_id}.faa")
    if not os.path.exists(faa_path):
        print(f"WARNING: Missing .faa file for {genome_id}")
        continue

    # Search for the matching sequence
    for record in SeqIO.parse(faa_path, "fasta"):
        if record.id == protein_id or record.id.startswith(protein_id):
            if gene_id not in gene_to_records:
                gene_to_records[gene_id] = []
            record.id = f"{genome_id}__{record.id}"
            record.description = ""
            gene_to_records[gene_id].append(record)
            break

# Write one FASTA per gene
for gene_id, records in gene_to_records.items():
    out_path = os.path.join(extracted_dir, f"{gene_id}.faa")
    with open(out_path, "w") as f:
        SeqIO.write(records, f, "fasta")

    print(f"Wrote {len(records)} sequences to {gene_id}.faa")
