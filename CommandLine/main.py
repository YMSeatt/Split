from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, DataTable, Static
from textual.containers import Container
from classroom import Classroom

class ClassroomApp(App):
    """A Textual app to manage a classroom."""

    BINDINGS = [
        ("a", "add_student", "Add Student"),
        ("r", "remove_student", "Remove Student"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self):
        super().__init__()
        self.classroom = Classroom()

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Container(
            Button("Add Student", id="add_student"),
            Button("Remove Student", id="remove_student"),
        )
        yield DataTable()
        yield Footer()

    def on_mount(self) -> None:
        """Called when the app is mounted."""
        self.update_student_list()

    def update_student_list(self):
        """Update the student list in the DataTable."""
        table = self.query_one(DataTable)
        table.clear(columns=True)
        table.add_column("Students")
        for student in self.classroom.list_students():
            table.add_row(student)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Called when a button is pressed."""
        if event.button.id == "add_student":
            self.action_add_student()
        elif event.button.id == "remove_student":
            self.action_remove_student()

    def action_add_student(self) -> None:
        """An action to add a student."""
        def add_student_callback(name: str):
            if name:
                self.classroom.add_student(name)
                self.update_student_list()
        self.push_screen(AddStudentScreen(), add_student_callback)

    def action_remove_student(self) -> None:
        """An action to remove a student."""
        def remove_student_callback(name: str):
            if name:
                self.classroom.remove_student(name)
                self.update_student_list()
        self.push_screen(RemoveStudentScreen(), remove_student_callback)

from textual.screen import ModalScreen
from textual.widgets import Input

class AddStudentScreen(ModalScreen):
    """Screen with a dialog to add a student."""

    def compose(self) -> ComposeResult:
        yield Container(
            Static("Enter student name:"),
            Input(placeholder="Student Name"),
            Button("Add", variant="primary", id="add"),
            Button("Cancel", id="cancel"),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add":
            input_widget = self.query_one(Input)
            self.dismiss(input_widget.value)
        else:
            self.dismiss(None)

class RemoveStudentScreen(ModalScreen):
    """Screen with a dialog to remove a student."""

    def compose(self) -> ComposeResult:
        yield Container(
            Static("Enter student name:"),
            Input(placeholder="Student Name"),
            Button("Remove", variant="error", id="remove"),
            Button("Cancel", id="cancel"),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "remove":
            input_widget = self.query_one(Input)
            self.dismiss(input_widget.value)
        else:
            self.dismiss(None)

if __name__ == "__main__":
    app = ClassroomApp()
    app.run()
