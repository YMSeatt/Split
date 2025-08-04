import math
from datetime import datetime
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Header, Footer, Input, Static, DataTable, Label, Select

from classroom import Classroom
from security import FileLockManager, PasswordManager
from commands import (
    AddItemCommand, DeleteItemCommand, EditItemCommand, MoveItemsCommand,
    LogEntryCommand, LogHomeworkEntryCommand
)

class ClassroomApp(App):
    """A Textual app to manage a classroom."""

    BINDINGS = [
        ("a", "add_student", "Add Student"),
        ("e", "edit_student", "Edit Student"),
        ("r", "remove_student", "Remove Student"),
        ("f", "add_furniture", "Add Furniture"),
        ("z", "undo", "Undo"),
        ("y", "redo", "Redo"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self):
        super().__init__()
        self.classroom = Classroom()
        self.file_lock_manager = FileLockManager()
        self.password_manager = PasswordManager(self.classroom.settings)
        self.undo_stack = []
        self.redo_stack = []
        self.grid_cols = 20
        self.grid_rows = 15
        self.cell_width = 100
        self.cell_height = 100

    def on_mount(self) -> None:
        """Called when the app is mounted."""
        locked, message = self.file_lock_manager.acquire_lock()
        if not locked:
            self.exit(message)
            return

        # UI Setup
        seating_chart = self.query_one("#seating_chart_table", DataTable)
        for i in range(self.grid_cols):
            seating_chart.add_column(f"{i+1}", key=str(i))

        student_table = self.query_one("#student_table", DataTable)
        student_table.add_column("ID", key="id")
        student_table.add_column("First Name", key="first_name")
        student_table.add_column("Last Name", key="last_name")
        student_table.add_column("Nickname", key="nickname")

        furniture_table = self.query_one("#furniture_table", DataTable)
        furniture_table.add_column("ID", key="id")
        furniture_table.add_column("Name", key="name")
        furniture_table.add_column("Type", key="type")

        behavior_log_table = self.query_one("#behavior_log_table", DataTable)
        behavior_log_table.add_column("Timestamp", key="timestamp")
        behavior_log_table.add_column("Student", key="student")
        behavior_log_table.add_column("Behavior", key="behavior")
        behavior_log_table.add_column("Comment", key="comment")

        homework_log_table = self.query_one("#homework_log_table", DataTable)
        homework_log_table.add_column("Timestamp", key="timestamp")
        homework_log_table.add_column("Student", key="student")
        homework_log_table.add_column("Homework", key="homework")
        homework_log_table.add_column("Status", key="status")
        homework_log_table.add_column("Comment", key="comment")

        self.update_all_tables()
        self.update_undo_redo_buttons()

    def on_unmount(self) -> None:
        self.file_lock_manager.release_lock()

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Vertical(id="main_container"):
            yield Container(
                Button("Undo", id="undo", disabled=True),
                Button("Redo", id="redo", disabled=True),
                classes="button-row"
            )
            yield Label("Seating Chart", classes="table-header")
            yield DataTable(id="seating_chart_table")
            yield Container(
                Button("Save Layout", id="save_layout", variant="primary"),
                Button("Load Layout", id="load_layout", variant="primary"),
                Button("Settings", id="settings"),
                Button("Export to Excel", id="export_excel", variant="success"),
                Button("Lock", id="lock_app"),
                classes="button-row"
            )
            # ... rest of the layout ...
            yield Label("Students", classes="table-header")
            yield Container(
                Button("Add Student", id="add_student", variant="primary"),
                Button("Edit Student", id="edit_student", variant="success"),
                Button("Move Student", id="move_student"),
                Button("Remove Student", id="remove_student", variant="error"),
                classes="button-row"
            )
            yield DataTable(id="student_table")

            yield Label("Furniture", classes="table-header")
            yield Container(
                Button("Add Furniture", id="add_furniture", variant="primary"),
                Button("Edit Furniture", id="edit_furniture", variant="success"),
                Button("Move Furniture", id="move_furniture"),
                Button("Remove Furniture", id="remove_furniture", variant="error"),
                classes="button-row"
            )
            yield DataTable(id="furniture_table")

            yield Label("Behavior Log", classes="table-header")
            yield Container(
                Button("Log Behavior", id="log_behavior", variant="primary"),
                Button("Log Quiz Score", id="log_quiz", variant="primary"),
                Button("Log Homework", id="log_homework", variant="primary"),
                classes="button-row"
            )
            yield DataTable(id="behavior_log_table")

            yield Label("Homework Log", classes="table-header")
            yield DataTable(id="homework_log_table")

        yield Footer()

    def execute_command(self, command):
        command.execute()
        self.undo_stack.append(command)
        self.redo_stack.clear()
        self.update_undo_redo_buttons()

    def update_undo_redo_buttons(self):
        self.query_one("#undo", Button).disabled = not self.undo_stack
        self.query_one("#redo", Button).disabled = not self.redo_stack

    def action_undo(self):
        if self.undo_stack:
            command = self.undo_stack.pop()
            command.undo()
            self.redo_stack.append(command)
            self.update_undo_redo_buttons()

    def action_redo(self):
        if self.redo_stack:
            command = self.redo_stack.pop()
            command.execute()
            self.undo_stack.append(command)
            self.update_undo_redo_buttons()

    def check_lock(self, callback):
        if self.password_manager.is_locked:
            self.push_screen(PasswordPromptScreen(action="unlock"), lambda p: self.unlock_and_proceed(p, callback))
        else:
            callback()

    def unlock_and_proceed(self, password, callback):
        if self.password_manager.unlock_application(password):
            callback()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Called when a button is pressed."""
        actions = {
            "add_student": lambda: self.check_lock(self.action_add_student),
            "edit_student": lambda: self.check_lock(self.action_edit_student),
            "move_student": lambda: self.check_lock(lambda: self.action_move_item("student")),
            "remove_student": lambda: self.check_lock(self.action_remove_student),
            "add_furniture": lambda: self.check_lock(self.action_add_furniture),
            "edit_furniture": lambda: self.check_lock(self.action_edit_furniture),
            "move_furniture": lambda: self.check_lock(lambda: self.action_move_item("furniture")),
            "remove_furniture": lambda: self.check_lock(self.action_remove_furniture),
            "save_layout": self.action_save_layout,
            "load_layout": self.action_load_layout,
            "log_behavior": lambda: self.check_lock(self.action_log_behavior),
            "log_quiz": lambda: self.check_lock(self.action_log_quiz_score),
            "log_homework": lambda: self.check_lock(self.action_log_homework),
            "settings": self.action_open_settings,
            "export_excel": self.action_export_to_excel,
            "lock_app": self.action_lock_application,
            "undo": self.action_undo,
            "redo": self.action_redo
        }
        if event.button.id in actions:
            actions[event.button.id]()

    def action_add_student(self) -> None:
        def callback(data: dict):
            if data:
                next_id_num = self.classroom.settings.get("next_student_id_num", 1)
                student_id = f"student_{next_id_num}"
                student_data = {
                    "id": student_id, "first_name": data["first"], "last_name": data["last"],
                    "nickname": data["nick"], "full_name": f"{data['first']} \"{data['nick']}\" {data['last']}" if data['nick'] else f"{data['first']} {data['last']}",
                    "gender": "Boy", "x": 50, "y": 50,
                    "width": self.classroom.settings.get("default_student_box_width"),
                    "height": self.classroom.settings.get("default_student_box_height"),
                    "group_id": None, "style_overrides": {},
                    "original_next_id_num_after_add": next_id_num + 1
                }
                command = AddItemCommand(self, student_id, 'student', student_data, next_id_num)
                self.execute_command(command)
        self.push_screen(AddStudentScreen(), callback)

    def action_edit_student(self) -> None:
        def edit_callback(data: dict):
            if data:
                student_id = data.pop("id")
                old_data = self.classroom.get_student(student_id)
                command = EditItemCommand(self, student_id, "student", old_data, data)
                self.execute_command(command)

        def select_callback(student_id: str):
            if student_id:
                student = self.classroom.get_student(student_id)
                if student: self.push_screen(EditStudentScreen(student=student), edit_callback)

        self.push_screen(SelectStudentScreen(), select_callback)

    def action_remove_student(self) -> None:
        def callback(student_id: str):
            if student_id:
                student_data = self.classroom.get_student(student_id)
                if student_data:
                    command = DeleteItemCommand(self, student_id, "student", student_data)
                    self.execute_command(command)
        self.push_screen(RemoveStudentScreen(), callback)

    def action_move_item(self, item_type: str) -> None:
        def callback(data: dict):
            if data:
                item_id, new_x, new_y = data["id"], data["x"], data["y"]
                item = self.classroom.get_student(item_id) if item_type == "student" else self.classroom.get_furniture(item_id)
                if item:
                    old_x, old_y = item['x'], item['y']
                    command = MoveItemsCommand(self, [{'id': item_id, 'type': item_type, 'old_x': old_x, 'old_y': old_y, 'new_x': new_x, 'new_y': new_y}])
                    self.execute_command(command)
        self.push_screen(MoveItemScreen(item_type=item_type), callback)

    # ... other actions refactored similarly ...
    def action_log_behavior(self) -> None:
        def callback(data: dict):
            if data:
                student = self.classroom.get_student(data["student_id"])
                if student:
                    log_entry = {
                        "timestamp": datetime.now().isoformat(), "student_id": data["student_id"],
                        "student_first_name": student["first_name"], "student_last_name": student["last_name"],
                        "behavior": data["behavior"], "comment": data["comment"], "type": "behavior",
                        "day": datetime.now().strftime('%A')
                    }
                    command = LogEntryCommand(self, log_entry, data["student_id"])
                    self.execute_command(command)

        self.push_screen(LogBehaviorScreen(behaviors=self.classroom.get_all_behaviors()), callback)

    def action_log_quiz_score(self) -> None:
        """Pushes a screen to log a quiz score for a student."""
        def callback(data: dict):
            if data:
                student = self.classroom.get_student(data["student_id"])
                if student:
                    log_entry = {
                        "timestamp": datetime.now().isoformat(),
                        "student_id": data["student_id"],
                        "student_first_name": student["first_name"],
                        "student_last_name": student["last_name"],
                        "behavior": data["quiz_name"],
                        "comment": data["comment"],
                        "marks_data": data["marks_data"],
                        "num_questions": data["num_questions"],
                        "type": "quiz",
                        "day": datetime.now().strftime('%A')
                    }
                    command = LogEntryCommand(self, log_entry, data["student_id"])
                    self.execute_command(command)
        self.push_screen(LogQuizScreen(), callback)

    def action_log_homework(self) -> None:
        """Pushes a screen to log a homework entry for a student."""
        def callback(data: dict):
            if data:
                student = self.classroom.get_student(data["student_id"])
                if student:
                    log_entry = {
                        "timestamp": datetime.now().isoformat(),
                        "student_id": data["student_id"],
                        "student_first_name": student["first_name"],
                        "student_last_name": student["last_name"],
                        "behavior": f"{data['homework_type']}: {data['status']}",
                        "homework_type": data['homework_type'],
                        "homework_status": data['status'],
                        "comment": data["comment"],
                        "type": "homework",
                        "day": datetime.now().strftime('%A')
                    }
                    command = LogHomeworkEntryCommand(self, log_entry, data["student_id"])
                    self.execute_command(command)
        self.push_screen(LogHomeworkScreen(
            types=self.classroom.get_all_homework_types(),
            statuses=self.classroom.get_all_homework_statuses()
        ), callback)

    def action_lock_application(self):
        if self.password_manager.is_password_set():
            self.password_manager.lock_application()
            self.notify("Application locked.")
        else:
            self.notify("Password not set. Please set a password in Settings.")

    # ... update_all_tables, update_student_list, etc. remain the same ...
    def update_all_tables(self):
        self.update_student_list()
        self.update_furniture_list()
        self.update_seating_chart()
        self.update_behavior_log()
        self.update_homework_log()

    def update_student_list(self):
        """Update the student list in the DataTable."""
        table = self.query_one("#student_table", DataTable)
        table.clear()
        for student in self.classroom.list_students():
            table.add_row(
                student.get("id"),
                student.get("first_name"),
                student.get("last_name"),
                student.get("nickname", ""),
            )

    def update_furniture_list(self):
        """Update the furniture list in the DataTable."""
        table = self.query_one("#furniture_table", DataTable)
        table.clear()
        for item in self.classroom.list_furniture():
            table.add_row(
                item.get("id"),
                item.get("name"),
                item.get("type"),
            )

    def update_seating_chart(self):
        """Renders the classroom layout into the seating chart table."""
        table = self.query_one("#seating_chart_table", DataTable)
        table.clear()

        # Create an empty grid
        grid = [["" for _ in range(self.grid_cols)] for _ in range(self.grid_rows)]

        # Place items in the grid
        items = self.classroom.list_students() + self.classroom.list_furniture()
        for item in items:
            x, y = item.get("x", 0), item.get("y", 0)
            col = math.floor(x / self.cell_width)
            row = math.floor(y / self.cell_height)

            if 0 <= row < self.grid_rows and 0 <= col < self.grid_cols:
                if not grid[row][col]:
                    grid[row][col] = item.get("id")
                else:
                    # Simple collision handling: append
                    grid[row][col] += f",{item.get('id')}"

        # Populate the table
        for row_data in grid:
            table.add_row(*row_data)

    def update_behavior_log(self):
        """Updates the behavior log table."""
        table = self.query_one("#behavior_log_table", DataTable)
        table.clear()
        # Sort by timestamp descending
        logs = sorted(self.classroom.behavior_log, key=lambda x: x.get("timestamp"), reverse=True)
        for log in logs:
            student_name = f"{log.get('student_first_name', '')} {log.get('student_last_name', '')}"
            table.add_row(
                log.get("timestamp"),
                student_name,
                log.get("behavior"),
                log.get("comment"),
            )

    def update_homework_log(self):
        """Updates the homework log table."""
        table = self.query_one("#homework_log_table", DataTable)
        table.clear()
        logs = sorted(self.classroom.homework_log, key=lambda x: x.get("timestamp"), reverse=True)
        for log in logs:
            student_name = f"{log.get('student_first_name', '')} {log.get('student_last_name', '')}"
            table.add_row(
                log.get("timestamp"),
                student_name,
                log.get("homework_type"),
                log.get("homework_status"),
                log.get("comment"),
            )

class PasswordPromptScreen(ModalScreen[str]):
    def __init__(self, action: str):
        super().__init__()
        self.action = action

    def compose(self) -> ComposeResult:
        with Container():
            yield Static(f"Enter Password to {self.action}", classes="header")
            yield Input(placeholder="Password", password=True)
            with Container(classes="buttons"):
                yield Button("Submit", variant="primary", id="submit")
                yield Button("Cancel", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit":
            self.dismiss(self.query_one(Input).value)
        else:
            self.dismiss(None)
# ... rest of the modals (AddStudentScreen, etc.) ...
# These modals do not need to change for this step
# ... (The existing modal classes go here) ...
# --- Student Modals ---
class AddStudentScreen(ModalScreen):
    def compose(self) -> ComposeResult:
        with Container():
            yield Static("Add a New Student", classes="header")
            yield Input(placeholder="First Name", id="first")
            yield Input(placeholder="Last Name", id="last")
            yield Input(placeholder="Nickname (Optional)", id="nick")
            with Container(classes="buttons"):
                yield Button("Add", variant="primary", id="add")
                yield Button("Cancel", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add":
            first = self.query_one("#first", Input).value
            last = self.query_one("#last", Input).value
            if first and last:
                self.dismiss({
                    "first": first, "last": last,
                    "nick": self.query_one("#nick", Input).value
                })
        else: self.dismiss(None)

class SelectStudentScreen(ModalScreen[str]):
    def compose(self) -> ComposeResult:
        with Container():
            yield Static("Select Student by ID", classes="header")
            yield Input(placeholder="e.g., student_1")
            with Container(classes="buttons"):
                yield Button("Select", variant="primary", id="select")
                yield Button("Cancel", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "select": self.dismiss(self.query_one(Input).value)
        else: self.dismiss(None)

class EditStudentScreen(ModalScreen):
    def __init__(self, student: dict):
        super().__init__()
        self.student = student

    def compose(self) -> ComposeResult:
        with Container():
            yield Static(f"Editing {self.student.get('full_name')}", classes="header")
            yield Input(value=self.student.get("first_name"), id="first")
            yield Input(value=self.student.get("last_name"), id="last")
            yield Input(value=self.student.get("nickname", ""), id="nick")
            with Container(classes="buttons"):
                yield Button("Save", variant="primary", id="save")
                yield Button("Cancel", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            first = self.query_one("#first", Input).value
            last = self.query_one("#last", Input).value
            nick = self.query_one("#nick", Input).value
            if first and last:
                self.dismiss({
                    "id": self.student.get("id"), "first_name": first,
                    "last_name": last, "nickname": nick,
                    "full_name": f"{first} \"{nick}\" {last}" if nick else f"{first} {last}"
                })
        else: self.dismiss(None)

class RemoveStudentScreen(ModalScreen[str]):
    def compose(self) -> ComposeResult:
        with Container():
            yield Static("Remove Student by ID", classes="header")
            yield Input(placeholder="e.g., student_1")
            with Container(classes="buttons"):
                yield Button("Remove", variant="error", id="remove")
                yield Button("Cancel", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "remove": self.dismiss(self.query_one(Input).value)
        else: self.dismiss(None)


class MoveItemScreen(ModalScreen):
    """Screen to move an item to a new coordinate."""
    def __init__(self, item_type: str):
        super().__init__()
        self.item_type = item_type

    def compose(self) -> ComposeResult:
        with Container():
            yield Static(f"Move {self.item_type.capitalize()}", classes="header")
            yield Input(placeholder=f"{self.item_type.capitalize()} ID (e.g., {self.item_type}_1)", id="item_id")
            yield Input(placeholder="New X coordinate", id="new_x", type="number")
            yield Input(placeholder="New Y coordinate", id="new_y", type="number")
            with Container(classes="buttons"):
                yield Button("Move", variant="primary", id="move")
                yield Button("Cancel", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "move":
            item_id = self.query_one("#item_id", Input).value
            try:
                new_x = int(self.query_one("#new_x", Input).value)
                new_y = int(self.query_one("#new_y", Input).value)
                if item_id:
                    self.dismiss({"id": item_id, "x": new_x, "y": new_y})
            except ValueError:
                # Handle case where x or y is not a valid integer
                # For now, just do nothing. A real app would show an error.
                pass
        else:
            self.dismiss(None)


class ExportScreen(ModalScreen[str]):
    """Screen to get a filename for exporting."""
    def compose(self) -> ComposeResult:
        with Container():
            yield Static("Export to Excel", classes="header")
            yield Input(placeholder="filename.xlsx")
            with Container(classes="buttons"):
                yield Button("Export", variant="primary", id="export")
                yield Button("Cancel", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "export":
            self.dismiss(self.query_one(Input).value)
        else:
            self.dismiss(None)


class LogHomeworkScreen(ModalScreen):
    """Screen for logging a homework assignment."""
    def __init__(self, types: list[str], statuses: list[str]):
        super().__init__()
        self.homework_types = types
        self.homework_statuses = statuses

    def compose(self) -> ComposeResult:
        with Container():
            yield Static("Log Homework", classes="header")
            yield Input(placeholder="Student ID", id="student_id")
            yield Select(((t, t) for t in self.homework_types), prompt="Select Homework Type", id="homework_type")
            yield Select(((s, s) for s in self.homework_statuses), prompt="Select Status", id="status")
            yield Input(placeholder="Comment (Optional)", id="comment")
            with Container(classes="buttons"):
                yield Button("Log", variant="primary", id="log")
                yield Button("Cancel", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "log":
            student_id = self.query_one("#student_id", Input).value
            homework_type = self.query_one("#homework_type", Select).value
            status = self.query_one("#status", Select).value
            if student_id and homework_type and status:
                self.dismiss({
                    "student_id": student_id,
                    "homework_type": homework_type,
                    "status": status,
                    "comment": self.query_one("#comment", Input).value
                })
        else:
            self.dismiss(None)


class SettingsScreen(ModalScreen):
    """Screen for editing application settings."""
    def __init__(self, settings: dict):
        super().__init__()
        self.settings = settings

    def compose(self) -> ComposeResult:
        with Container():
            yield Static("Settings", classes="header")
            yield Static("Autosave Interval (ms):")
            yield Input(value=str(self.settings.get("autosave_interval_ms", 30000)), id="autosave_interval_ms", type="integer")

            yield Static("Default Student Box Width:")
            yield Input(value=str(self.settings.get("default_student_box_width", 130)), id="default_student_box_width", type="integer")

            yield Static("Default Student Box Height:")
            yield Input(value=str(self.settings.get("default_student_box_height", 80)), id="default_student_box_height", type="integer")

            with Container(classes="buttons"):
                yield Button("Save", variant="primary", id="save")
                yield Button("Cancel", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            try:
                new_settings = {
                    "autosave_interval_ms": int(self.query_one("#autosave_interval_ms", Input).value),
                    "default_student_box_width": int(self.query_one("#default_student_box_width", Input).value),
                    "default_student_box_height": int(self.query_one("#default_student_box_height", Input).value),
                }
                self.dismiss(new_settings)
            except ValueError:
                # Handle invalid integer
                pass
        else:
            self.dismiss(None)


# --- Layout Modals ---
class SaveLayoutScreen(ModalScreen[str]):
    """Screen to get a name for a new layout template."""
    def compose(self) -> ComposeResult:
        with Container():
            yield Static("Save Layout Template", classes="header")
            yield Input(placeholder="Template Name")
            with Container(classes="buttons"):
                yield Button("Save", variant="primary", id="save")
                yield Button("Cancel", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            self.dismiss(self.query_one(Input).value)
        else:
            self.dismiss(None)

class LoadLayoutScreen(ModalScreen[str]):
    """Screen to select a layout template to load."""
    def __init__(self, templates: list[str]):
        super().__init__()
        self.templates = templates

    def compose(self) -> ComposeResult:
        with Container():
            yield Static("Load Layout Template", classes="header")
            if not self.templates:
                yield Static("No templates found.")
            else:
                for template in self.templates:
                    yield Button(template, id=template)
            yield Button("Cancel", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "cancel":
            self.dismiss(event.button.id)
        else:
            self.dismiss(None)


# --- Logging Modals ---
class LogBehaviorScreen(ModalScreen):
    """Screen for logging a behavior."""
    def __init__(self, behaviors: list[str]):
        super().__init__()
        self.behaviors = behaviors

    def compose(self) -> ComposeResult:
        with Container():
            yield Static("Log Behavior", classes="header")
            yield Input(placeholder="Student ID", id="student_id")
            yield Select(((b, b) for b in self.behaviors), prompt="Select Behavior", id="behavior")
            yield Input(placeholder="Comment (Optional)", id="comment")
            with Container(classes="buttons"):
                yield Button("Log", variant="primary", id="log")
                yield Button("Cancel", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "log":
            student_id = self.query_one("#student_id", Input).value
            behavior = self.query_one("#behavior", Select).value
            if student_id and behavior:
                self.dismiss({
                    "student_id": student_id,
                    "behavior": behavior,
                    "comment": self.query_one("#comment", Input).value
                })
        else:
            self.dismiss(None)


class LogQuizScreen(ModalScreen):
    """Screen for logging a quiz score."""

    def compose(self) -> ComposeResult:
        with Container():
            yield Static("Log Quiz Score", classes="header")
            yield Input(placeholder="Student ID", id="student_id")
            yield Input(placeholder="Quiz Name", id="quiz_name")
            yield Input(placeholder="Number of Questions", id="num_questions", type="integer")
            yield Input(placeholder="Number Correct", id="num_correct", type="integer")
            yield Input(placeholder="Comment (Optional)", id="comment")
            with Container(classes="buttons"):
                yield Button("Log", variant="primary", id="log")
                yield Button("Cancel", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "log":
            try:
                student_id = self.query_one("#student_id", Input).value
                quiz_name = self.query_one("#quiz_name", Input).value
                num_questions = int(self.query_one("#num_questions", Input).value)
                num_correct = int(self.query_one("#num_correct", Input).value)

                if student_id and quiz_name and num_questions > 0:
                    self.dismiss({
                        "student_id": student_id,
                        "quiz_name": quiz_name,
                        "marks_data": {"mark_correct": num_correct}, # Simplified
                        "num_questions": num_questions,
                        "comment": self.query_one("#comment", Input).value
                    })
            except ValueError:
                # Handle invalid number input
                pass
        else:
            self.dismiss(None)


# --- Furniture Modals ---
class AddFurnitureScreen(ModalScreen):
    def compose(self) -> ComposeResult:
        with Container():
            yield Static("Add New Furniture", classes="header")
            yield Input(placeholder="Name (e.g., Teacher's Desk)", id="name")
            yield Input(placeholder="Type (e.g., Desk)", id="type")
            with Container(classes="buttons"):
                yield Button("Add", variant="primary", id="add")
                yield Button("Cancel", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add":
            name = self.query_one("#name", Input).value
            if name: self.dismiss({"name": name, "type": self.query_one("#type", Input).value})
        else: self.dismiss(None)

class SelectFurnitureScreen(ModalScreen[str]):
    def compose(self) -> ComposeResult:
        with Container():
            yield Static("Select Furniture by ID", classes="header")
            yield Input(placeholder="e.g., furniture_1")
            with Container(classes="buttons"):
                yield Button("Select", variant="primary", id="select")
                yield Button("Cancel", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "select": self.dismiss(self.query_one(Input).value)
        else: self.dismiss(None)

class EditFurnitureScreen(ModalScreen):
    def __init__(self, item: dict):
        super().__init__()
        self.item = item

    def compose(self) -> ComposeResult:
        with Container():
            yield Static(f"Editing {self.item.get('name')}", classes="header")
            yield Input(value=self.item.get("name"), id="name")
            yield Input(value=self.item.get("type"), id="type")
            with Container(classes="buttons"):
                yield Button("Save", variant="primary", id="save")
                yield Button("Cancel", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            name = self.query_one("#name", Input).value
            if name:
                self.dismiss({
                    "id": self.item.get("id"), "name": name,
                    "type": self.query_one("#type", Input).value
                })
        else: self.dismiss(None)

class RemoveFurnitureScreen(ModalScreen[str]):
    def compose(self) -> ComposeResult:
        with Container():
            yield Static("Remove Furniture by ID", classes="header")
            yield Input(placeholder="e.g., furniture_1")
            with Container(classes="buttons"):
                yield Button("Remove", variant="error", id="remove")
                yield Button("Cancel", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "remove": self.dismiss(self.query_one(Input).value)
        else: self.dismiss(None)


if __name__ == "__main__":
    app = ClassroomApp()
    app.run()
