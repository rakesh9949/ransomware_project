import os
import shutil
import json
import datetime

# Paths
target_dir = "/home/sec-lab/critical"
baseline_file = "baseline_hashes.json"
quarantine_dir = "/home/sec-lab/quarantine"

# Function to hash files
def hash_file(file_path):
    import hashlib
    sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            sha.update(chunk)
    return sha.hexdigest()

# Scan the critical directory
def scan_directory(directory): 
    hash_map = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            hash_map[path] = hash_file(path)
    return hash_map

# Mitigation logic
def mitigate_threats():
    if not os.path.exists(baseline_file):
        print("No baseline found. Please create one first.")
        return

with open(baseline_file, "r") as f:
    baseline = json.load(f)

current = scan_directory(target_dir)

for path, current_hash in current.items():
    baseline_hash = baseline.get(path)
    if not baseline_hash:
        print(f"[MITIGATION] New suspicious file: {path}")
        filename = os.path.basename(path)
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        quarantine_name = f"{filename}.{timestamp}.quarantine"
        shutil.move(path, os.path.join(quarantine_dir, quarantine_name))
        print(f"--> Moved to quarantine as {quarantine_name}")

    elif current_hash != baseline_hash:
        print(f"[MITIGATION] File modified: {path}")
        filename = os.path.basename(path)
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        quarantine_name = f"{filename}.{timestamp}.quarantine"
        shutil.move(path, os.path.join(quarantine_dir, quarantine_name))
        print(f" --> Moved to quarantine as {quarantine_name}")

if __name__ == "__main__":
    mitigate_threats()
	

