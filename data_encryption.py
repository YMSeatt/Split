# data_encryption.py

from cryptography.fernet import Fernet
import os
import sys

ENCRYPTION_KEY = b'87KRv9OeBzEpeW1xSNT8NqCqN_GIizfRyEmqGZBLvxw='
f = Fernet(ENCRYPTION_KEY)

"""
def generate_key():
    
    Generates a key and saves it into a file
    
    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as key_file:
        key_file.write(key)
    print(f"Encryption key generated and saved to {KEY_PATH}")

def load_key():
    
    Loads the key from the current directory named `secret.key`
    
    if not os.path.exists(KEY_PATH):
        generate_key()
    return open(KEY_PATH, "rb").read()
"""
# --- Encryption and Decryption Functions ---

def encrypt_data(data_string):
    """
    Encrypts a string of data.
    """
    encrypted_data = f.encrypt(data_string.encode('utf-8'))
    return encrypted_data

def decrypt_data(encrypted_data):
    """
    Decrypts an encrypted string of data.
    """
    decrypted_data = f.decrypt(encrypted_data).decode('utf-8')
    return decrypted_data