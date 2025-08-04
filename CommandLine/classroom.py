import json
from pathlib import Path

class Classroom:
    def __init__(self, data_file="classroom_data.json"):
        self.data_file = Path(data_file)
        self.students = self._load_students()

    def _load_students(self):
        if self.data_file.exists():
            with open(self.data_file, "r") as f:
                return json.load(f)
        return []

    def _save_students(self):
        with open(self.data_file, "w") as f:
            json.dump(self.students, f, indent=4)

    def add_student(self, name):
        if name not in self.students:
            self.students.append(name)
            self._save_students()
            return True
        return False

    def remove_student(self, name):
        if name in self.students:
            self.students.remove(name)
            self._save_students()
            return True
        return False

    def list_students(self):
        return self.students
