# Classroom Management CLI

A simple command-line application for managing a classroom.

## Installation

1. Clone the repository.
2. Navigate to the `CommandLine` directory.
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

The application supports the following commands:

- `add-student <name>`: Add a new student to the classroom.
- `list-students`: List all students in the classroom.
- `remove-student <name>`: Remove a student from the classroom.

### Examples

```bash
# Add a student
python main.py add-student "John Doe"

# List all students
python main.py list-students

# Remove a student
python main.py remove-student "John Doe"
```
