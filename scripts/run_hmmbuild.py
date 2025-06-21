import os
import subprocess

# === SETTINGS ===
script_dir = os.path.dirname(os.path.abspath(__file__))
input_dir = os.path.abspath(os.path.join(script_dir, "../data/raw_data"))
aligned_dir = os.path.abspath(os.path.join(script_dir, "../data/aligned_data"))
hmm_dir = os.path.abspath(os.path.join(script_dir, "../data/hmms"))

# === SETUP OUTPUT DIRS ===
os.makedirs(aligned_dir, exist_ok=True)
os.makedirs(hmm_dir, exist_ok=True)

# === GET INPUT FILES ===
files = [f for f in os.listdir(input_dir) if f.endswith(".faa") or f.endswith(".fasta")]

if not files:
    print(f"No FASTA files found in '{input_dir}'.")
    exit(1)

# === PROCESS FILES ===
for filename in files:
    name = os.path.splitext(filename)[0]
    input_path = os.path.join(input_dir, filename)
    aligned_path = os.path.join(aligned_dir, f"{name}_aligned.faa")
    hmm_path = os.path.join(hmm_dir, f"{name}.hmm")

    print(f"\nProcessing: {filename}")

    # 1. MAFFT alignment
    try:
        with open(aligned_path, "w") as out_f:
            subprocess.run(["mafft", "--auto", input_path], stdout=out_f, check=True)
        print(f"Aligned: {aligned_path}")
    except subprocess.CalledProcessError as e:
        print(f"MAFFT failed on {filename}: {e}")
        continue

        # 2. HMM build
    try:
        subprocess.run(["hmmbuild", hmm_path, aligned_path], check=True)
        print(f"HMM built: {hmm_path}")
    except subprocess.CalledProcessError as e:
        print(f"HMMBUILD failed on {filename}: {e}")