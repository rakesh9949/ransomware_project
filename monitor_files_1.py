import os
import hashlib
import json
# Step 1: Calculate SHA-256 hash of a file
def hash_file(file_path):
    sha = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                sha.update(chunk)
        return sha.hexdigest()
    except Exception as e:
        print(f"[ERROR] Could not read {file_path}: {e}")
        return None
# Step 2: Generate hash map of all files in directory
def scan_directory(directory):
    hash_map = {}
    for root, dirs, files in os.walk(directory):
        for name in files:
            path = os.path.join(root, name)
            file_hash = hash_file(path)
            if file_hash:
                hash_map[path] = file_hash
    return hash_map
# Path to monitor
target_dir = os.path.expanduser("~/critical")
baseline_file = "baseline_hashes.json"
# Step 3: Generate and store baseline hashes (initial run)
def create_baseline():
    hashes = scan_directory(target_dir)
    with open(baseline_file, "w") as f:
        json.dump(hashes, f, indent=2)
print("[+] Baseline hashes saved.")
# Step 4: Compare current hashes with baseline
def monitor_for_changes():
    if not os.path.exists(baseline_file):
        print("[!] No baseline found. Run in baseline mode first.")
        return
    with open(baseline_file, "r") as f:
        baseline = json.load(f)
    current = scan_directory(target_dir)
    for path, current_hash in current.items():
        baseline_hash = baseline.get(path)
        if not baseline_hash:
            print(f"[!] New file added: {path}")
        elif current_hash != baseline_hash:
            print(f"[ALERT] File modified: {path}")
    for path in baseline:
        if path not in current:
            print(f"[ALERT] File deleted: {path}")
# Uncomment the one we want to use
# Run this once to save baseline
#create_baseline()
# Run this later to detect changes
monitor_for_changes()
