import data_encryptor
from data_encryptor import encrypt_data, decrypt_data

# The name of your encrypted data file.
# It's good practice to give it a different extension, like .dat or .bin,
# to signify that it's not a plain text file.
DATA_FILE = "student_data.dat"

def main():
    """
    Main function to demonstrate the encryption and decryption of data.
    """
    # --- On Program Start: Decrypt data into a variable in memory ---
    print("Loading and decrypting data...")
    student_data_content = decrypt_data(DATA_FILE)

    if student_data_content is None:
        # This means decryption failed. The error is printed by the decryptor.
        # We should exit gracefully.
        input("Press Enter to exit.")
        return

    print("\n--- Program is running. Data is held securely in memory. ---")
    print(f"Current data:\n---\n{student_data_content or '[No data yet]'}\n---")

    # --- Your program's main logic happens here ---
    # You can now work with the 'student_data_content' string.
    # For example, let's append a new line to it.
    new_record = input("Enter a new record to add: ")
    if new_record:
        student_data_content += f"{new_record}\n"
        print(f"Added '{new_record}' to the data.")

    print("\n--- Program is finishing. ---")

    # --- On Program Exit: Encrypt the modified data and save it to disk ---
    print("Encrypting and saving data before closing...")
    encrypt_data(DATA_FILE, student_data_content)
    print("Done.")

if __name__ == "__main__":
    main()