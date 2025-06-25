from cryptography.fernet import Fernet
import os

# --- IMPORTANT ---
# 1. Run this script once from your terminal: `python data_encryptor.py generate_key`
# 2. This will print a new, unique key.
# 3. Copy that key and PASTE IT BELOW, replacing the placeholder string.
# 4. This key will be embedded in your final .exe. Keep it safe!
ENCRYPTION_KEY = b'rDVLszUrXZOL-B0NRw1n0yRpUhxFGPJLZiHvv3FQc5E='


def generate_key():
    """Generates a new encryption key and prints it to the console."""
    key = Fernet.generate_key()
    print("Your new encryption key is below. Copy it into the ENCRYPTION_KEY variable in your script.")
    print("-----------------------------------------------------------------")
    print(key.decode())
    print("-----------------------------------------------------------------")


def get_cipher_suite():
    """Initializes the Fernet cipher suite with the key."""
    if ENCRYPTION_KEY == b'REPLACE_THIS_WITH_THE_KEY_YOU_GENERATE':
        raise ValueError("ENCRYPTION_KEY has not been set. Please generate a key and update the script.")
    return Fernet(ENCRYPTION_KEY)


def encrypt_data(file_path, data_to_encrypt):
    """Encrypts the given data (as a string) and writes it to the file_path."""
    cipher_suite = get_cipher_suite()
    # The data must be in bytes for encryption
    data_bytes = data_to_encrypt.encode('utf-8')

    encrypted_data = cipher_suite.encrypt(data_bytes)

    try:
        # Write the encrypted data in binary mode
        with open(file_path, 'wb') as f:
            f.write(encrypted_data)
        print(f"Data successfully encrypted and saved to '{file_path}'.")
    except IOError as e:
        print(f"Error writing encrypted file: {e}")


def decrypt_data(file_path):
    """Reads an encrypted file, decrypts its content, and returns it as a string."""
    if not os.path.exists(file_path):
        print(f"Data file '{file_path}' not found. Starting with empty data.")
        return ""  # Return empty string if no data file exists yet

    cipher_suite = get_cipher_suite()

    try:
        with open(file_path, 'rb') as f:
            encrypted_data = f.read()

        decrypted_data_bytes = cipher_suite.decrypt(encrypted_data)
        return decrypted_data_bytes.decode('utf-8')
    except Exception as e:
        # This can happen if the key is wrong or the file is corrupted/not encrypted
        print(f"FATAL: Could not decrypt file '{file_path}'. Error: {e}")
        print("The file may be corrupted, was modified, or the encryption key is incorrect.")
        return None  # Return None to indicate a critical failure


# Main block to allow key generation from the command line
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'generate_key':
        generate_key()
    else:
        print("This script is intended to be imported into your main application.")
        print("To generate a new encryption key, run: python data_encryptor.py generate_key")