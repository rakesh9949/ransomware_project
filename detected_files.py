import os
import hashlib
import json
import logging

#Set up logging
logging.basicConfig(filename="alerts.log", level=logging.INFO, format="%(asctime)s - %(message)s")

#HASH one file
def hash_file(file_path):
    sha = hashlib.sha256()
    try:
       with open(file_path, 'rb') as f:
           while chunk := f.read(4096):
               sha.update(chunk)
       return sha.hexdigest()
    except Exception as e:
         print(f"[ERROR] Cannot read {file_path}: {e}")
         return None

#Hash all files in directory
def scan_directory(directory):
    hash_map = {}
    for root, dirs, files in os.walk(directory):
        for name in files:
            path = os.path.join(root, name)
            file_hash = hash_file(path)
            if file_hash:
                hash_map[path] = file_hash
    return hash_map

# Target and baseline paths
target_dir = os.path.expanduser("~/critical")
baseline_file = "baseline_hashes.json"

#Monitor function
def monitor_for_changes():
    if not os.path.exists(baseline_file):
        print("[!] No baseline found. Run baseline creation first.")
        return
    with open(baseline_file, "r") as f:
        baseline = json.load(f)

    current = scan_directory(target_dir)

    for path, current_hash in current.items():
        baseline_hash = baseline.get(path)
        if not baseline_hash:
            alert = f"[!] New file added: {path}"
            print(alert)
            logging.info(alert)
        elif current_hash != baseline_hash:
            alert = f"[ALERT] File modified: {path}"
            print(alert)
            logging.info(alert)
    for path in baseline:
        if path not in current:
            alert = f"[ALERT] File deleted: {path}"
            print(alert)
            logging.info(alert)

#Execute monitoring
target_dir = "/home/sec-lab/critical"
if __name__ == "__main__":
    monitor_for_changes()
