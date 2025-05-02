import os
from cryptography.fernet import Fernet

# Function to retrieve the encryption key
def load_key():
    return open("secret.key", "rb").read()

# Function to decrypt an encrypted file
def decrypt_file(file_path, key):
    cipher = Fernet(key)
    try:
        with open(file_path, "rb") as file:
            encrypted_data = file.read()
        decrypted_data = cipher.decrypt(encrypted_data)
        original_path = file_path.replace(".locked", "")
        with open(file_path, "wb") as file:
            file.write(decrypted_data)
        
        print(f"[+] Decrypted: {file_path}")
    except Exception as e:
        print(f"[!] Skipped: {file_path} ({e})")

# Function to decrypt all files in a directory
def decrypt_directory(directory, key):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".locked"):
                file_path = os.path.join(root, file)
                decrypt_file(file_path, key)

# Load the saved encryption key
decryption_key = load_key()

# Decrypt all files in the specified directory
decrypt_directory("/home/sec-lab/critical", decryption_key)
print("Decryption completed.")
