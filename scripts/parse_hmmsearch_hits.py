import os

# Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
hits_dir = os.path.abspath(os.path.join(script_dir, "../results/hits"))
parsed_dir = os.path.abspath(os.path.join(script_dir, "../results/parsed_hits"))
os.makedirs(parsed_dir, exist_ok=True)

# Filter and parse each .tbl file
for fname in os.listdir(hits_dir):
    if not fname.endswith(".tbl"):
        continue

    input_path = os.path.join(hits_dir, fname)
    output_path = os.path.join(parsed_dir, fname.replace(".tbl", ".best_hit.txt"))

    with open(input_path, "r") as f:
        lines = [line for line in f if not line.startswith("#")]

    # Skip if no hits
    if not lines:
        continue

    # Sort hits by bit score (column 5) descending
    sorted_hits = sorted(lines, key=lambda x: float(x.split()[5]), reverse=True)

    # Get top hit
    top_hit_line = sorted_hits[0]
    fields = top_hit_line.split()
    protein_id = fields[0]
    bitscore = fields[5]

    with open(output_path, "w") as out:
        out.write(f"{protein_id}\t{bitscore}\n")

    print(f"Best hit from {fname}: {protein_id} (score: {bitscore})")
