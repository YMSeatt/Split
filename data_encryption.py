# data_encryption.py

from cryptography.fernet import Fernet
import os
from encryption_key import encryption_key as ENCRYPTION_KEY # For me.
import json
import cryptography.fernet

# ENCRYPTION_KEY = Fernet.generate_key()
#ENCRYPTION_KEY = b''
#if not ENCRYPTION_KEY:
#    ENCRYPTION_KEY = b'' # Enter your own encryption key here. You can generate your own with the code below:

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

def _read_and_decrypt_file(file_path):
        """Reads a file, attempts to decrypt it, and loads the JSON data."""
        if not os.path.exists(file_path):
            return None
        try:
            with open(file_path, 'rb') as f:
                file_content = f.read()
            
            if not file_content: # File is empty
                return None

            try:
                # Attempt to decrypt first
                decrypted_data_string = decrypt_data(file_content)
            except cryptography.fernet.InvalidToken:
                # If decryption fails, it's likely plaintext (or corrupt)
                # Assume it's a UTF-8 encoded string.
                decrypted_data_string = file_content.decode('utf-8')

            return json.loads(decrypted_data_string)

        except (json.JSONDecodeError, IOError, UnicodeDecodeError) as e:
            print(f"Error loading and decoding file {os.path.basename(file_path)}: {e}")
            return None
        
def _encrypt_and_write_file(file_path, data_to_write, rule):
        """Encodes data to JSON, encrypts if enabled, and writes to a file."""
        try:
            json_data_string = json.dumps(data_to_write, indent=4)
            
            # Use the app's setting to decide whether to encrypt
            if rule: #self.settings.get("encrypt_data_files", True):
                data_to_write_bytes = encrypt_data(json_data_string)
            else:
                data_to_write_bytes = json_data_string.encode('utf-8')

            with open(file_path, 'wb') as f:
                f.write(data_to_write_bytes)

        except IOError as e:
            print(f"Error saving file {os.path.basename(file_path)}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while saving {os.path.basename(file_path)}: {e}")