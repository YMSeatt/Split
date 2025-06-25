import os
import stat
import sys

# --- Configuration ---
# Change this to the actual name of your data file.
DATA_FILE = "student_data.txt"

def lock_file(file_path):
    """
    Locks the specified file by making it read-only.

    This is a deterrent to prevent accidental or casual modification.
    On Windows, it sets the 'Read-only' attribute.
    On Linux/macOS, it sets permissions to 'r--r--r--' (444), which is
    read-only for the owner, group, and everyone else.
    """
    print(f"Attempting to lock '{file_path}'...")
    try:
        if not os.path.exists(file_path):
            print(f"Warning: File '{file_path}' not found. Cannot lock.")
            return

        # These permissions (read for all) will make the file read-only on
        # both Windows and POSIX systems.
        read_only_permissions = stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH
        os.chmod(file_path, read_only_permissions)

        print(f"'{file_path}' has been locked (set to read-only).")

    except Exception as e:
        print(f"An error occurred while locking the file: {e}")

def unlock_file(file_path):
    """
    Unlocks the specified file by making it writable for the owner.

    Your program should call this before it needs to modify the data.
    On Windows, it removes the 'Read-only' attribute.
    On Linux/macOS, it sets permissions to 'rw-r--r--' (644), which is
    read/write for the owner and read-only for others.
    """
    print(f"Attempting to unlock '{file_path}'...")
    try:
        if not os.path.exists(file_path):
            print(f"Warning: File '{file_path}' not found. Cannot unlock.")
            return

        # These permissions grant write access to the owner.
        writable_permissions = stat.S_IWUSR | stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH
        os.chmod(file_path, writable_permissions)

        print(f"'{file_path}' has been unlocked (set to writable).")

    except Exception as e:
        print(f"An error occurred while unlocking the file: {e}")


def main():
    """
    A simple command-line interface to demonstrate locking and unlocking.

    In your actual application, you would import and call lock_file() and
    unlock_file() directly.
    """
    # Create a dummy data file if it doesn't exist for demonstration
    if not os.path.exists(DATA_FILE):
        print(f"Creating dummy file '{DATA_FILE}' for demonstration.")
        with open(DATA_FILE, 'w') as f:
            f.write("Initial student data.\n")

    if len(sys.argv) != 2:
        print(f"\nUsage: python {sys.argv[0]} <lock|unlock>")
        print("Example:")
        print(f"  python {sys.argv[0]} lock   -> Makes '{DATA_FILE}' read-only.")
        print(f"  python {sys.argv[0]} unlock -> Makes '{DATA_FILE}' writable.")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == 'lock':
        lock_file(DATA_FILE)
    elif command == 'unlock':
        unlock_file(DATA_FILE)
    else:
        print(f"Invalid command '{command}'. Please use 'lock' or 'unlock'.")
        sys.exit(1)


if __name__ == "__main__":
    main()