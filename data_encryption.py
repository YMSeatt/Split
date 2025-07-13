# data_encryption.py

from cryptography.fernet import Fernet
import os
import sys
from encryption_key import encryption_key as ENCRYPTION_KEY # For me.

if not ENCRYPTION_KEY:
    ENCRYPTION_KEY = b'' # Enter your own encryption key here. You can generate your own with the code below:

# def generate_key():
#     """
#     Generates a key and saves it into a file
#     """
#     key = Fernet.generate_key()
#     print(key)

""" # Useless - I don't use it
def load_key():
    
    Loads the key from the current directory named `secret.key`
    
    if not os.path.exists(KEY_PATH):
        generate_key()
    return open(KEY_PATH, "rb").read()
"""
f = Fernet(ENCRYPTION_KEY)
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