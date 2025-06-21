import os
from collections import defaultdict
from Bio import SeqIO

# Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
input_dir = os.path.abspath(os.path.join(script_dir, "../results/aligned_genes"))
output_dir = os.path.abspath(os.path.join(script_dir, "../results/concatenated"))
os.makedirs(output_dir, exist_ok=True)

# Step 1: Collect alignments
genome_to_concat = defaultdict(list)
genomes = set()
gene_order = []
gene_lengths = {}

for fname in sorted(os.listdir(input_dir)):
    if not fname.endswith(".aligned.faa"):
        continue

    gene_name = fname.replace(".aligned.faa", "")
    gene_order.append(gene_name)

    gene_path = os.path.join(input_dir, fname)
    records = list(SeqIO.parse(gene_path, "fasta"))
    if not records:
        continue

    aln_len = len(records[0].seq)
    gene_lengths[gene_name] = aln_len

    for record in records:
        genome_id = record.id.split("__")[0]
        genomes.add(genome_id)
        genome_to_concat[genome_id].append((gene_name, str(record.seq)))

# Step 2: Write supermatrix
output_fasta = os.path.join(output_dir, "supermatrix.faa")
with open(output_fasta, "w") as out_f:
    for genome in sorted(genomes):
        final_seq = ""
        gene_seq_dict = {g: s for g, s in genome_to_concat.get(genome, [])}

        for gene in gene_order:
            if gene in gene_seq_dict:
                final_seq += gene_seq_dict[gene]
            else:
                final_seq += "-" * gene_lengths[gene]

        out_f.write(f">{genome}\n{final_seq}\n")

print(f"Supermatrix written to {output_fasta}")
