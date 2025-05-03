# Ransomware Simulation Project

This repository contains the complete ransomware simulation project structured by phases, including design files, scripts, and explanations.

## Project Overview
This project demonstrates how ransomware works in a controlled environment using Python. It simulates encryption, phishing infection, file monitoring, detection of suspicious activity, and mitigation.

## Directory Structure

ransomware_project/
├── encrypt.py             # Encrypts files and sends email
├── decrypt.py             # Decrypts encrypted files using the saved key
├── SecurityUpdate.py      # Simulates a phishing-based infection
├── monitor_files.py       # Monitors file integrity and changes
├── detection_files.py     # Detects new or deleted files
├── mitigation.py          # Quarantines suspicious files
├── README.md              # Explanation of all steps
└── critical/              # Contains sample target folders and files


## Project Steps

### 1. Set Environment
- A secure Ubuntu VM was used
- Python 3 and cryptography library installed

### 2. Creating Folders
- Nested folders and test files were created in a directory named critical

### 3. Step 1 - Action (Encryption & Decryption)
- encrypt.py: Encrypts all files with .locked extension
- Sends a simulated email with the key
- decrypt.py: Recovers files using the encryption key

### 4. Step 2 - Infection
- SecurityUpdate.py: A fake security update script that runs encrypt.py silently

### 5. Monitoring
- monitor_files.py: Tracks file changes using SHA-256 hashes

### 6. Detection
- detection_files.py: Flags unusual activity like deleted or added files

### 7. Mitigation
- mitigation.py: Finds .locked files and ransom notes, moves them to quarantine

## How to Run
python3 encrypt.py
python3 decrypt.py
python3 SecurityUpdate.py
python3 monitor_files.py
python3 detection_files.py
python3 mitigation.py

## Disclaimer
This project is for academic and demonstration purposes only. Do not use in real environments.
