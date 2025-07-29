import os
import sys
from datetime import datetime
import tkinter as tk

# def listener(callback: typing.Callable[[str], None]) -> None: ...

# TODO: make conditional formatting work by quizzes. add thing for homework also.


# --- Application Constants ---
APP_NAME = "BehaviorLogger"
APP_VERSION = "v57.0" # Version incremented
CURRENT_DATA_VERSION_TAG = "v10" # Incremented for new homework/marks features

# --- Default Configuration ---
DEFAULT_STUDENT_BOX_WIDTH = 130
DEFAULT_STUDENT_BOX_HEIGHT = 80
MIN_STUDENT_BOX_WIDTH = 60
MIN_STUDENT_BOX_HEIGHT = 40
REBBI_DESK_WIDTH = 200
REBBI_DESK_HEIGHT = 100

DEFAULT_FONT_FAMILY = "TkDefaultFont"
DEFAULT_FONT_SIZE = 10
DEFAULT_FONT_COLOR = "black"
DEFAULT_BOX_FILL_COLOR = "skyblue"
DEFAULT_BOX_OUTLINE_COLOR = "blue"
DEFAULT_QUIZ_SCORE_FONT_COLOR = "darkgreen"
DEFAULT_QUIZ_SCORE_FONT_STYLE_BOLD = True
DEFAULT_HOMEWORK_SCORE_FONT_COLOR = "purple" # New for homework scores
DEFAULT_HOMEWORK_SCORE_FONT_STYLE_BOLD = True # New
GROUP_COLOR_INDICATOR_SIZE = 12
DEFAULT_THEME = "System"
THEME_LIST = ["Light", "Dark", "System"]

DRAG_THRESHOLD = 5
DEFAULT_GRID_SIZE = 20
MAX_UNDO_HISTORY_DAYS = 90
LAYOUT_COLLISION_OFFSET = 5
RESIZE_HANDLE_SIZE = 10 # World units for resize handle

# --- Path Handling ---
def get_app_data_path(filename):
    try:
        # Determine base path based on whether the app is frozen (packaged) or running from script
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # Running as a PyInstaller bundle
            if os.name == 'win32': # Windows
                base_path = os.path.join(os.getenv('APPDATA'), APP_NAME)
            elif sys.platform == 'darwin': # macOS
                base_path = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', APP_NAME)
            else: # Linux and other Unix-like
                xdg_config_home = os.getenv('XDG_CONFIG_HOME')
                if xdg_config_home:
                    base_path = os.path.join(xdg_config_home, APP_NAME)
                else:
                    base_path = os.path.join(os.path.expanduser('~'), '.config', APP_NAME)
        else:
            # Running as a script, use the script's directory
            base_path = os.path.dirname(os.path.abspath(__file__))

        # Create the base directory if it doesn't exist
        if not os.path.exists(base_path):
            os.makedirs(base_path, exist_ok=True)
        return os.path.join(base_path, filename)
    except Exception as e:
        # Fallback to current working directory if standard paths fail
        print(f"Warning: Could not determine standard app data path due to {e}. Using current working directory as fallback.")
        fallback_path = os.path.join(os.getcwd(), APP_NAME) # Create a subfolder in CWD
        if not os.path.exists(fallback_path):
             os.makedirs(fallback_path, exist_ok=True)
        return os.path.join(fallback_path, filename)

DATA_FILE_PATTERN = f"classroom_data_{CURRENT_DATA_VERSION_TAG}.json"
CUSTOM_BEHAVIORS_FILE_PATTERN = f"custom_behaviors_{CURRENT_DATA_VERSION_TAG}.json"
# NEW: For customizable homework types like "Reading Assignment", "Worksheet"
CUSTOM_HOMEWORK_TYPES_FILE_PATTERN = f"custom_homework_types_{CURRENT_DATA_VERSION_TAG}.json" 
# RENAMED: For customizable homework statuses like "Done", "Not Done"
CUSTOM_HOMEWORK_STATUSES_FILE_PATTERN = f"custom_homework_statuses_{CURRENT_DATA_VERSION_TAG}.json" 
AUTOSAVE_EXCEL_FILE_PATTERN = f"autosave_log_{CURRENT_DATA_VERSION_TAG}.xlsx" # Renamed for clarity
LAYOUT_TEMPLATES_DIR_NAME = "layout_templates"
STUDENT_GROUPS_FILE_PATTERN = f"student_groups_{CURRENT_DATA_VERSION_TAG}.json"
QUIZ_TEMPLATES_FILE_PATTERN = f"quiz_templates_{CURRENT_DATA_VERSION_TAG}.json"
HOMEWORK_TEMPLATES_FILE_PATTERN = f"homework_templates_{CURRENT_DATA_VERSION_TAG}.json" # New

DATA_FILE = get_app_data_path(DATA_FILE_PATTERN)
CUSTOM_BEHAVIORS_FILE = get_app_data_path(CUSTOM_BEHAVIORS_FILE_PATTERN)
CUSTOM_HOMEWORK_TYPES_FILE = get_app_data_path(CUSTOM_HOMEWORK_TYPES_FILE_PATTERN) # NEW
CUSTOM_HOMEWORK_STATUSES_FILE = get_app_data_path(CUSTOM_HOMEWORK_STATUSES_FILE_PATTERN) # RENAMED
AUTOSAVE_EXCEL_FILE = get_app_data_path(AUTOSAVE_EXCEL_FILE_PATTERN)
LAYOUT_TEMPLATES_DIR = get_app_data_path(LAYOUT_TEMPLATES_DIR_NAME)
STUDENT_GROUPS_FILE = get_app_data_path(STUDENT_GROUPS_FILE_PATTERN)
QUIZ_TEMPLATES_FILE = get_app_data_path(QUIZ_TEMPLATES_FILE_PATTERN)
HOMEWORK_TEMPLATES_FILE = get_app_data_path(HOMEWORK_TEMPLATES_FILE_PATTERN) # New
LOCK_FILE_PATH = get_app_data_path(f"{APP_NAME}.lock") # Lock file

if not os.path.exists(LAYOUT_TEMPLATES_DIR):
    os.makedirs(LAYOUT_TEMPLATES_DIR, exist_ok=True)

DEFAULT_BEHAVIORS_LIST = [
    "Talking", "Off Task", "Out of Seat", "Uneasy", "Placecheck",
    "Great Participation", "Called On", "Complimented", "Fighting", "Other"
]


# for manual detailed logging, i would want these | currently used for sessions (yes/no)
DEFAULT_HOMEWORK_TYPES_LIST = [ # For live session "Yes/No" mode AND now for manual logging
    "Reading Assignment", "Worksheet", "Math Problems", "Project Work", "Study for Test"
]

# these would only be for behavior-like logging (not detailed)
DEFAULT_HOMEWORK_LOG_BEHAVIORS = [ # For manual homework logging (like behavior logging)
    "Done", "Not Done", "Partially Done", "Signed", "Returned", "Late", "Excellent Work"
]


# Make these be used for the select AND Yes/No Live Homework session modes.
DEFAULT_HOMEWORK_SESSION_BUTTONS = [ # For live session "Select" mode
    {"name": "Done"}, {"name": "Not Done"}, {"name": "Signed"}, {"name": "Returned"}
]

DEFAULT_HOMEWORK_SESSION_BUTTONS2 = [ # For live session "Select" mode
    "Done", "Not Done", "Signed", "Returned"
]


DEFAULT_HOMEWORK_STATUSES = [
    "Done", "Not Done", "Partially Done", "Signed", "Returned", "Late", "Excellent Work"
]


DEFAULT_GROUP_COLORS = ["#FFADAD", "#FFD6A5", "#FDFFB6", "#CAFFBF", "#9BF6FF", "#A0C4FF", "#BDB2FF", "#FFC6FF", "#E0E0E0"]

DEFAULT_QUIZ_MARK_TYPES = [
    {"id": "mark_correct", "name": "Correct", "contributes_to_total": True, "is_extra_credit": False, "default_points": 1},
    {"id": "mark_incorrect", "name": "Incorrect", "contributes_to_total": True, "is_extra_credit": False, "default_points": 0},
    {"id": "mark_partial", "name": "Partial Credit", "contributes_to_total": True, "is_extra_credit": False, "default_points": 0.5},
    {"id": "extra_credit", "name": "Bonus", "contributes_to_total": False, "is_extra_credit": True, "default_points": 1}
]
DEFAULT_HOMEWORK_MARK_TYPES = [ # New for homework marks
    {"id": "hmark_complete", "name": "Complete", "default_points": 10},
    {"id": "hmark_incomplete", "name": "Incomplete", "default_points": 5},
    {"id": "hmark_notdone", "name": "Not Done", "default_points": 0},
    {"id": "hmark_effort", "name": "Effort Score (1-5)", "default_points": 3} # Example
]

MAX_CUSTOM_TYPES = 90 # Max for custom behaviors, homeworks, mark types


# --- Command Pattern for Undo/Redo ---
class Command:
    def __init__(self, app, timestamp=None):
        self.app = app
        self.timestamp = timestamp or datetime.now().isoformat()

    def execute(self): raise NotImplementedError
    def undo(self): raise NotImplementedError
    def to_dict(self): return {'type': self.__class__.__name__, 'timestamp': self.timestamp, 'data': self._get_data_for_serialization()}
    def _get_data_for_serialization(self): raise NotImplementedError

    def get_description(self):
        """Returns a user-friendly description of the command."""
        # Attempt to format timestamp for better readability if it's a valid ISO string
        try:
            dt_obj = datetime.fromisoformat(self.timestamp)
            # Example: "MoveItemsCommand (01/25 14:35:02)"
            # You can customize the strftime format as needed
            time_str = dt_obj.strftime("%m/%d %H:%M:%S")
            return f"{self.__class__.__name__} ({time_str})"
        except (ValueError, TypeError): # Fallback if timestamp is not a valid ISO string
            return f"{self.__class__.__name__} (Timestamp: {self.timestamp})"


    @classmethod
    def from_dict(cls, app, data_dict):
        command_type_name = data_dict['type']
        command_class = getattr(sys.modules[__name__], command_type_name, None)
        if command_class and issubclass(command_class, Command):
            try:
                return command_class._from_serializable_data(app, data_dict['data'], data_dict['timestamp'])
            except KeyError as e:
                print(f"Warning: Missing key '{e}' in data for command type '{command_type_name}'. Skipping command.")
                return None
        print(f"Warning: Unknown command type '{command_type_name}' in undo/redo history.")
        return None
    @classmethod
    def _from_serializable_data(cls, app, data, timestamp): raise NotImplementedError




class MoveGuideCommand(Command):
    def __init__(self, app, items_moves, timestamp=None):
        super().__init__(app, timestamp)
        self.items_moves = items_moves # List of dicts: {'id', 'type', 'old_x', 'old_y', 'new_x', 'new_y'}

    def execute(self):
        for item_move in self.items_moves:
            item_id, new_coord = item_move['id'], item_move['new_coord']
            data_source = self.app.guides
            
            guide_info = data_source.get(item_id)
            if guide_info:
                data_source[item_id]['world_coord'] = new_coord
        self.app.update_status(f"Moved {len(self.items_moves)} guide(s).")
        self.app.draw_all_items(check_collisions_on_redraw=True)

    def undo(self):
        for item_move in self.items_moves:
            item_id, old_x = item_move['id'], item_move['old_coord']
            data_source = self.app.guides
            guide_info = data_source.get(item_id)
            if guide_info:#item_id in data_source:
                data_source[item_id]['world_coord'] = old_x
        self.app.update_status(f"Undid move of {len(self.items_moves)} guide(s).")
        self.app.draw_all_items(check_collisions_on_redraw=True)

    def _get_data_for_serialization(self): return {'items_moves': self.items_moves}
    @classmethod
    def _from_serializable_data(cls, app, data, timestamp): return cls(app, data['items_moves'], timestamp)
    def get_description(self):
        return f"Move {len(self.items_moves)} guide(s)"

class AddGuideCommand(Command):
    def __init__(self, app, item_id, item_type, item_data, id_next_num, timestamp=None):
        super().__init__(app, timestamp)
        self.item_id = item_id
        self.item_type = item_type
        self.item_data = item_data
        self.old_next_id_num = id_next_num

    def execute(self):
        data_source = self.app.guides # if self.item_type == 'student' else self.app.furniture
        data_source[self.item_id] = self.item_data.copy()
        self.app.draw_all_items(check_collisions_on_redraw=True)

    def undo(self):
        data_source = self.app.guides # if self.item_type == 'student' else self.app.furniture
        if self.item_id in data_source:
            del data_source[self.item_id]
            self.app.canvas.delete(self.item_id)
        self.app.draw_all_items(check_collisions_on_redraw=True)

    def _get_data_for_serialization(self): return {'item_id': self.item_id, 'item_type': self.item_type, 'item_data': self.item_data, 'old_next_id_num': self.old_next_id_num}
    @classmethod
    def _from_serializable_data(cls, app, data, timestamp): return cls(app, data['item_id'], data['item_type'], data['item_data'], data['old_next_id_num'], timestamp)
    def get_description(self):
        item_name = self.item_data.get('full_name', self.item_data.get('name', self.item_id))
        return f"Add {self.item_type} guide at {self.item_data['world_coord']}"

class DeleteGuideCommand(Command):
    def __init__(self, app, item_id, item_data, timestamp=None):
        self.item_id = item_id
        self.item_type = "horizontal" if item_data.get('type') == "h" else "vertical"
        self.item_data = item_data
        super().__init__(app, timestamp)
    
    def execute(self):
        data_source = self.app.guides # if self.item_type == 'student' else self.app.furniture
        if self.item_id in data_source:
            del data_source[self.item_id]
        self.app.update_status(f"Deleted {self.item_type} guide at {self.item_data.get("world_coord")}")
        self.app.canvas.delete(self.item_id)
        self.app.draw_all_items(check_collisions_on_redraw=True)

    def undo(self):
        data_source = self.app.guides # if self.item_type == 'student' else self.app.furniture
        data_source[self.item_id] = self.item_data.copy()
        self.app.update_status(f"Undid delete of {self.item_type} guide at {self.item_data.get("world_coord")}")
        self.app.draw_all_items(check_collisions_on_redraw=True)

    def _get_data_for_serialization(self):
        return {
            'item_id': self.item_id, 'item_type': self.item_type,
            'item_data': self.item_data
        }
    @classmethod
    def _from_serializable_data(cls, app, data, timestamp):
        cmd = cls(app, data['item_id'], data['item_data'], timestamp)
        
        return cmd
    def get_description(self):
        #item_name = self.item_data.get('full_name', self.item_data.get('name', self.item_id))
        return f"Delete {self.item_type} guide at {self.item_data.get("world_coords")}"


class MoveItemsCommand(Command):
    def __init__(self, app, items_moves, timestamp=None):
        super().__init__(app, timestamp)
        self.items_moves = items_moves # List of dicts: {'id', 'type', 'old_x', 'old_y', 'new_x', 'new_y'}

    def execute(self):
        for item_move in self.items_moves:
            item_id, item_type, new_x, new_y = item_move['id'], item_move['type'], item_move['new_x'], item_move['new_y']
            data_source = self.app.students if item_type == 'student' else self.app.furniture
            if item_id in data_source:
                data_source[item_id]['x'] = new_x
                data_source[item_id]['y'] = new_y
        self.app.update_status(f"Moved {len(self.items_moves)} item(s).")
        self.app.draw_all_items(check_collisions_on_redraw=True)

    def undo(self):
        for item_move in self.items_moves:
            item_id, item_type, old_x, old_y = item_move['id'], item_move['type'], item_move['old_x'], item_move['old_y']
            data_source = self.app.students if item_type == 'student' else self.app.furniture
            if item_id in data_source:
                data_source[item_id]['x'] = old_x
                data_source[item_id]['y'] = old_y
        self.app.update_status(f"Undid move of {len(self.items_moves)} item(s).")
        self.app.draw_all_items(check_collisions_on_redraw=True)

    def _get_data_for_serialization(self): return {'items_moves': self.items_moves}
    @classmethod
    def _from_serializable_data(cls, app, data, timestamp): return cls(app, data['items_moves'], timestamp)
    def get_description(self):
        return f"Move {len(self.items_moves)} item(s)"

class AddItemCommand(Command):
    def __init__(self, app, item_id, item_type, item_data, old_next_id_num, timestamp=None):
        super().__init__(app, timestamp)
        self.item_id = item_id
        self.item_type = item_type
        self.item_data = item_data
        self.old_next_id_num = old_next_id_num

    def execute(self):
        data_source = self.app.students if self.item_type == 'student' else self.app.furniture
        data_source[self.item_id] = self.item_data.copy()
        if self.item_type == 'student':
            self.app.next_student_id_num = self.item_data.get('original_next_id_num_after_add', self.app.next_student_id_num)
            self.app.update_student_display_text(self.item_id)
            self.app.update_status(f"Student '{self.item_data['full_name']}' added.")
        else:
            self.app.next_furniture_id_num = self.item_data.get('original_next_id_num_after_add', self.app.next_furniture_id_num)
            self.app.update_status(f"Furniture '{self.item_data['name']}' added.")
        self.app.draw_all_items(check_collisions_on_redraw=True)

    def undo(self):
        data_source = self.app.students if self.item_type == 'student' else self.app.furniture
        if self.item_id in data_source:
            item_name = data_source[self.item_id].get('full_name', data_source[self.item_id].get('name'))
            del data_source[self.item_id]
            self.app.canvas.delete(self.item_id)
            if self.item_type == 'student':
                self.app.next_student_id_num = self.old_next_id_num
                self.app.update_status(f"Undid add of student '{item_name}'.")
            else:
                self.app.next_furniture_id_num = self.old_next_id_num
                self.app.update_status(f"Undid add of furniture '{item_name}'.")
        self.app.draw_all_items(check_collisions_on_redraw=True)

    def _get_data_for_serialization(self): return {'item_id': self.item_id, 'item_type': self.item_type, 'item_data': self.item_data, 'old_next_id_num': self.old_next_id_num}
    @classmethod
    def _from_serializable_data(cls, app, data, timestamp): return cls(app, data['item_id'], data['item_type'], data['item_data'], data['old_next_id_num'], timestamp)
    def get_description(self):
        item_name = self.item_data.get('full_name', self.item_data.get('name', self.item_id))
        return f"Add {self.item_type}: {item_name}"

class DeleteItemCommand(Command):
    def __init__(self, app, item_id, item_type, item_data, associated_logs=None, timestamp=None):
        super().__init__(app, timestamp)
        self.item_id = item_id
        self.item_type = item_type
        self.item_data = item_data
        self.associated_logs = associated_logs or [] # For behavior and quiz logs
        self.associated_homework_logs = [] # New for homework logs

        if item_type == 'student': # Separate homework logs for students
            self.associated_homework_logs = [log.copy() for log in app.homework_log if log["student_id"] == item_id]


    def execute(self):
        data_source = self.app.students if self.item_type == 'student' else self.app.furniture
        item_name = "Item"
        if self.item_id in data_source:
            item_name = data_source[self.item_id].get('full_name', data_source[self.item_id].get('name'))
            del data_source[self.item_id]
        self.app.canvas.delete(self.item_id)
        if self.item_id in self.app.selected_items: self.app.selected_items.remove(self.item_id)

        if self.item_type == 'student':
            original_log_count = len(self.app.behavior_log)
            self.app.behavior_log = [log for log in self.app.behavior_log if log["student_id"] != self.item_id]
            logs_removed_count = original_log_count - len(self.app.behavior_log)

            original_homework_log_count = len(self.app.homework_log)
            self.app.homework_log = [log for log in self.app.homework_log if log["student_id"] != self.item_id]
            homework_logs_removed_count = original_homework_log_count - len(self.app.homework_log)

            self.app.update_status(f"Student '{item_name}', {logs_removed_count} behavior/quiz log(s), and {homework_logs_removed_count} homework log(s) deleted.")
        else:
            self.app.update_status(f"Furniture '{item_name}' deleted.")
        self.app.draw_all_items(check_collisions_on_redraw=True)

    def undo(self):
        data_source = self.app.students if self.item_type == 'student' else self.app.furniture
        data_source[self.item_id] = self.item_data.copy()
        if self.item_type == 'student':
            self.app.update_student_display_text(self.item_id)
            for log_entry in self.associated_logs:
                if log_entry not in self.app.behavior_log: self.app.behavior_log.append(log_entry.copy())
            self.app.behavior_log.sort(key=lambda x: x.get("timestamp", ""))

            for hw_log_entry in self.associated_homework_logs: # Restore homework logs
                if hw_log_entry not in self.app.homework_log: self.app.homework_log.append(hw_log_entry.copy())
            self.app.homework_log.sort(key=lambda x: x.get("timestamp", ""))

            self.app.update_status(f"Undid delete of student '{self.item_data['full_name']}'. Logs restored.")
        else:
            self.app.update_status(f"Undid delete of furniture '{self.item_data['name']}'.")
        self.app.draw_all_items(check_collisions_on_redraw=True)

    def _get_data_for_serialization(self):
        return {
            'item_id': self.item_id, 'item_type': self.item_type,
            'item_data': self.item_data, 'associated_logs': self.associated_logs,
            'associated_homework_logs': self.associated_homework_logs # Serialize homework logs
        }
    @classmethod
    def _from_serializable_data(cls, app, data, timestamp):
        cmd = cls(app, data['item_id'], data['item_type'], data['item_data'], data.get('associated_logs'), timestamp)
        cmd.associated_homework_logs = data.get('associated_homework_logs', []) # Deserialize homework logs
        return cmd
    def get_description(self):
        item_name = self.item_data.get('full_name', self.item_data.get('name', self.item_id))
        return f"Delete {self.item_type}: {item_name}"

class LogEntryCommand(Command): # For Behavior and Quiz logs
    def __init__(self, app, log_entry, student_id, timestamp=None):
        super().__init__(app, timestamp)
        self.log_entry = log_entry
        self.student_id = student_id

    def execute(self):
        # Behavior/Quiz logs go into self.app.behavior_log
        if not any(le == self.log_entry for le in self.app.behavior_log):
            self.app.behavior_log.append(self.log_entry.copy())
            self.app.behavior_log.sort(key=lambda x: x.get("timestamp", ""))
        self.app.update_student_display_text(self.student_id)
        log_type = self.log_entry.get("type", "behavior")
        behavior_name = self.log_entry.get("behavior", "Unknown")
        student_name = self.app.students.get(self.student_id, {}).get('full_name', 'Unknown Student')
        self.app.update_status(f"{log_type.capitalize()} '{behavior_name}' logged for {student_name}.")

    def undo(self):
        try:
            self.app.behavior_log.remove(self.log_entry)
        except ValueError:
            for i, entry in enumerate(self.app.behavior_log):
                if entry["timestamp"] == self.log_entry["timestamp"] and \
                   entry["student_id"] == self.log_entry["student_id"] and \
                   entry["behavior"] == self.log_entry["behavior"]:
                    del self.app.behavior_log[i]; break
        self.app.update_student_display_text(self.student_id)
        log_type = self.log_entry.get("type", "behavior")
        behavior_name = self.log_entry.get("behavior", "Unknown")
        student_name = self.app.students.get(self.student_id, {}).get('full_name', 'Unknown Student')
        self.app.update_status(f"Undid log of {log_type.capitalize()} '{behavior_name}' for {student_name}.")

    def _get_data_for_serialization(self): return {'log_entry': self.log_entry, 'student_id': self.student_id}
    @classmethod
    def _from_serializable_data(cls, app, data, timestamp): return cls(app, data['log_entry'], data['student_id'], timestamp)
    def get_description(self):
        student_name = self.log_entry.get('student_first_name', 'Unknown')
        log_type = self.log_entry.get("type", "log").capitalize()
        behavior = self.log_entry.get("behavior", "entry")
        return f"Log {log_type}: '{behavior}' for {student_name}"

class LogHomeworkEntryCommand(Command): # New for Homework logs
    def __init__(self, app, log_entry, student_id, timestamp=None):
        super().__init__(app, timestamp)
        self.log_entry = log_entry
        self.student_id = student_id

    def execute(self):
        # Homework logs go into self.app.homework_log
        if not any(le == self.log_entry for le in self.app.homework_log):
            self.app.homework_log.append(self.log_entry.copy())
            self.app.homework_log.sort(key=lambda x: x.get("timestamp", ""))
        self.app.update_student_display_text(self.student_id) # Redraw student box
        homework_name = self.log_entry.get("homework_type", self.log_entry.get("behavior", "Unknown Homework")) # Use "homework_type" or "behavior"
        student_name = self.app.students.get(self.student_id, {}).get('full_name', 'Unknown Student')
        self.app.update_status(f"Homework '{homework_name}' logged for {student_name}.")

    def undo(self):
        try:
            self.app.homework_log.remove(self.log_entry)
        except ValueError:
            for i, entry in enumerate(self.app.homework_log):
                 # Match based on key fields for homework
                if entry["timestamp"] == self.log_entry["timestamp"] and \
                   entry["student_id"] == self.log_entry["student_id"] and \
                   entry.get("homework_type", entry.get("behavior")) == self.log_entry.get("homework_type", self.log_entry.get("behavior")):
                    del self.app.homework_log[i]; break
        self.app.update_student_display_text(self.student_id)
        homework_name = self.log_entry.get("homework_type", self.log_entry.get("behavior", "Unknown Homework"))
        student_name = self.app.students.get(self.student_id, {}).get('full_name', 'Unknown Student')
        self.app.update_status(f"Undid log of homework '{homework_name}' for {student_name}.")

    def _get_data_for_serialization(self): return {'log_entry': self.log_entry, 'student_id': self.student_id}
    @classmethod
    def _from_serializable_data(cls, app, data, timestamp): return cls(app, data['log_entry'], data['student_id'], timestamp)
    def get_description(self):
        student_name = self.log_entry.get('student_first_name', 'Unknown')
        hw_type = self.log_entry.get("homework_type", self.log_entry.get("behavior", "entry"))
        return f"Log Homework: '{hw_type}' for {student_name}"

class EditItemCommand(Command):
    def __init__(self, app, item_id, item_type, old_item_data, new_item_data_changes, timestamp=None):
        super().__init__(app, timestamp)
        self.item_id = item_id
        self.item_type = item_type
        self.old_item_data_snapshot = old_item_data
        self.new_item_data_changes = new_item_data_changes

    def execute(self):
        data_source = self.app.students if self.item_type == 'student' else self.app.furniture
        if self.item_id in data_source:
            data_source[self.item_id].update(self.new_item_data_changes)
            if self.item_type == 'student':
                self.app.update_student_display_text(self.item_id)
                self.app.update_status(f"Student '{data_source[self.item_id]['full_name']}' edited.")
            else:
                self.app.update_status(f"Furniture '{data_source[self.item_id]['name']}' edited.")
        self.app.draw_all_items(check_collisions_on_redraw=True)

    def undo(self):
        data_source = self.app.students if self.item_type == 'student' else self.app.furniture
        if self.item_id in data_source:
            data_source[self.item_id] = self.old_item_data_snapshot.copy()
            if self.item_type == 'student':
                self.app.update_student_display_text(self.item_id)
                self.app.update_status(f"Undid edit for student '{data_source[self.item_id]['full_name']}'.")
            else:
                self.app.update_status(f"Undid edit for furniture '{data_source[self.item_id]['name']}'.")
        self.app.draw_all_items(check_collisions_on_redraw=True)

    def _get_data_for_serialization(self):
        return {
            'item_id': self.item_id, 'item_type': self.item_type,
            'old_item_data_snapshot': self.old_item_data_snapshot,
            'new_item_data_changes': self.new_item_data_changes
        }
    @classmethod
    def _from_serializable_data(cls, app, data, timestamp):
        return cls(app, data['item_id'], data['item_type'],
                   data['old_item_data_snapshot'], data['new_item_data_changes'], timestamp)
    def get_description(self):
        item_name = self.old_item_data_snapshot.get('full_name', self.old_item_data_snapshot.get('name', self.item_id))
        changed_keys = ", ".join(self.new_item_data_changes.keys())
        return f"Edit {self.item_type}: {item_name} (Fields: {changed_keys})"

class ChangeItemsSizeCommand(Command):
    def __init__(self, app, items_sizes_changes, timestamp=None):
        super().__init__(app, timestamp)
        self.items_sizes_changes = items_sizes_changes

    def _apply_sizes(self, use_new_sizes):
        changed_item_names = []
        for item_size_info in self.items_sizes_changes:
            item_id, item_type = item_size_info['id'], item_size_info['type']
            w = item_size_info['new_w'] if use_new_sizes else item_size_info['old_w']
            h = item_size_info['new_h'] if use_new_sizes else item_size_info['old_h']
            data_source = self.app.students if item_type == 'student' else self.app.furniture
            if item_id in data_source:
                if item_type == 'student':
                    if 'style_overrides' not in data_source[item_id]: data_source[item_id]['style_overrides'] = {}
                    data_source[item_id]['style_overrides']['width'] = w
                    data_source[item_id]['style_overrides']['height'] = h
                    data_source[item_id]['width'] = w # Keep base in sync
                    data_source[item_id]['height'] = h
                else:
                    data_source[item_id]['width'] = w
                    data_source[item_id]['height'] = h
                changed_item_names.append(data_source[item_id].get('full_name', data_source[item_id].get('name', item_id)))
        return changed_item_names

    def execute(self):
        names = self._apply_sizes(use_new_sizes=True)
        self.app.update_status(f"Size changed for {len(names)} item(s): {', '.join(names[:3])}{'...' if len(names)>3 else ''}.")
        self.app.draw_all_items(check_collisions_on_redraw=True)

    def undo(self):
        names = self._apply_sizes(use_new_sizes=False)
        self.app.update_status(f"Undid size change for {len(names)} item(s): {', '.join(names[:3])}{'...' if len(names)>3 else ''}.")
        self.app.draw_all_items(check_collisions_on_redraw=True)

    def _get_data_for_serialization(self): return {'items_sizes_changes': self.items_sizes_changes}
    @classmethod
    def _from_serializable_data(cls, app, data, timestamp): return cls(app, data['items_sizes_changes'], timestamp)
    def get_description(self):
        return f"Resize {len(self.items_sizes_changes)} item(s)"

class MarkLiveQuizQuestionCommand(Command):
    def __init__(self, app, student_id, action_taken, timestamp=None):
        super().__init__(app, timestamp)
        self.student_id = student_id
        self.action_taken = action_taken
        self.previous_student_score_state = None

    def execute(self):
        if self.previous_student_score_state is None:
            self.previous_student_score_state = self.app.live_quiz_scores.get(self.student_id, {"correct": 0, "total_asked": 0}).copy()
        current_score = self.app.live_quiz_scores.get(self.student_id, {"correct": 0, "total_asked": 0}).copy()
        current_score["total_asked"] += 1
        if self.action_taken == "correct": current_score["correct"] += 1
        self.app.live_quiz_scores[self.student_id] = current_score
        self.app.draw_single_student(self.student_id)
        student_name = self.app.students[self.student_id]['full_name']
        self.app.update_status(f"Live Quiz: '{self.action_taken.capitalize()}' for {student_name}. Score: {current_score['correct']}/{current_score['total_asked']}")

    def undo(self):
        if self.previous_student_score_state is not None:
            self.app.live_quiz_scores[self.student_id] = self.previous_student_score_state.copy()
            if self.app.live_quiz_scores[self.student_id]["total_asked"] == 0 and self.app.live_quiz_scores[self.student_id]["correct"] == 0:
                del self.app.live_quiz_scores[self.student_id]
        elif self.student_id in self.app.live_quiz_scores:
            current_score = self.app.live_quiz_scores[self.student_id]
            current_score["total_asked"] -= 1
            if self.action_taken == "correct": current_score["correct"] -= 1
            if current_score["total_asked"] <= 0: del self.app.live_quiz_scores[self.student_id]
        self.app.draw_single_student(self.student_id)
        student_name = self.app.students[self.student_id]['full_name']
        score_info = self.app.live_quiz_scores.get(self.student_id)
        status = f"Undo Live Quiz Mark for {student_name}. Score: {score_info['correct']}/{score_info['total_asked']}" if score_info else f"Undo Live Quiz Mark for {student_name}. No questions marked."
        self.app.update_status(status)

    def _get_data_for_serialization(self):
        return {'student_id': self.student_id, 'action_taken': self.action_taken, 'previous_student_score_state': self.previous_student_score_state}
    @classmethod
    def _from_serializable_data(cls, app, data, timestamp):
        cmd = cls(app, data['student_id'], data['action_taken'], timestamp)
        cmd.previous_student_score_state = data.get('previous_student_score_state')
        return cmd
    def get_description(self):
        student_name = self.app.students.get(self.student_id, {}).get('first_name', 'Unknown')
        return f"Mark Quiz: {self.action_taken} for {student_name}"

class MarkLiveHomeworkCommand(Command): # New for Live Homework
    def __init__(self, app, student_id, homework_actions, session_mode, timestamp=None):
        super().__init__(app, timestamp)
        self.student_id = student_id
        self.homework_actions = homework_actions # Dict: {"homework_type_name": "yes/no/selected_option"} or list of selected options
        self.session_mode = session_mode # "Yes/No" or "Select"
        self.previous_homework_state = None # To store previous state for undo

    def execute(self):
        if self.previous_homework_state is None:
            self.previous_homework_state = self.app.live_homework_scores.get(self.student_id, {}).copy()

        # Update live_homework_scores based on homework_actions and session_mode
        # For "Yes/No", homework_actions might be {"Reading": "yes", "Math": "no"}
        # For "Select", homework_actions might be ["Done", "Signed"]
        current_hw_data = self.app.live_homework_scores.get(self.student_id, {}).copy()
        if self.session_mode == "Yes/No":
            current_hw_data.update(self.homework_actions) # Overwrite/add specific yes/no statuses
        elif self.session_mode == "Select":
            # Store as a list of selected actions for this student for this session
            current_hw_data["selected_options"] = list(self.homework_actions) # Ensure it's a list

        self.app.live_homework_scores[self.student_id] = current_hw_data
        self.app.draw_single_student(self.student_id) # Redraw to update display
        student_name = self.app.students[self.student_id]['full_name']
        self.app.update_status(f"Live Homework updated for {student_name}.")

    def undo(self):
        if self.previous_homework_state is not None:
            self.app.live_homework_scores[self.student_id] = self.previous_homework_state.copy()
            if not self.app.live_homework_scores[self.student_id]: # If restored to empty
                del self.app.live_homework_scores[self.student_id]
        elif self.student_id in self.app.live_homework_scores: # Should not happen if previous_homework_state was set
            del self.app.live_homework_scores[self.student_id]

        self.app.draw_single_student(self.student_id)
        student_name = self.app.students[self.student_id]['full_name']
        self.app.update_status(f"Undo Live Homework update for {student_name}.")

    def _get_data_for_serialization(self):
        return {
            'student_id': self.student_id,
            'homework_actions': self.homework_actions,
            'session_mode': self.session_mode,
            'previous_homework_state': self.previous_homework_state
        }
    @classmethod
    def _from_serializable_data(cls, app, data, timestamp):
        cmd = cls(app, data['student_id'], data['homework_actions'], data['session_mode'], timestamp)
        cmd.previous_homework_state = data.get('previous_homework_state')
        return cmd
    def get_description(self):
        student_name = self.app.students.get(self.student_id, {}).get('first_name', 'Unknown')
        action_summary = ""
        if self.session_mode == "Yes/No":
            action_summary = ", ".join(f"{k}:{v}" for k,v in self.homework_actions.items())
        elif self.session_mode == "Select":
            action_summary = ", ".join(self.homework_actions)
        return f"Mark HW ({self.session_mode}): {action_summary} for {student_name}"

class ChangeStudentStyleCommand(Command):
    def __init__(self, app, student_id, style_property, old_value, new_value, timestamp=None):
        super().__init__(app, timestamp)
        self.student_id = student_id
        self.style_property = style_property
        self.old_value = old_value
        self.new_value = new_value

    def execute(self):
        student = self.app.students.get(self.student_id)
        if student:
            if "style_overrides" not in student: student["style_overrides"] = {}
            if self.new_value is None:
                if self.style_property in student["style_overrides"]: del student["style_overrides"][self.style_property]
            else: student["style_overrides"][self.style_property] = self.new_value
            self.app.update_student_display_text(self.student_id)
            self.app.draw_single_student(self.student_id, check_collisions=True)
            self.app.update_status(f"Style '{self.style_property}' updated for {student['full_name']}.")

    def undo(self):
        student = self.app.students.get(self.student_id)
        if student:
            if "style_overrides" not in student: student["style_overrides"] = {}
            if self.old_value is None:
                if self.style_property in student["style_overrides"]: del student["style_overrides"][self.style_property]
            else: student["style_overrides"][self.style_property] = self.old_value
            if not student["style_overrides"]: del student["style_overrides"]
            self.app.update_student_display_text(self.student_id)
            self.app.draw_single_student(self.student_id, check_collisions=True)
            self.app.update_status(f"Undid style '{self.style_property}' change for {student['full_name']}.")

    def _get_data_for_serialization(self):
        return {'student_id': self.student_id, 'style_property': self.style_property, 'old_value': self.old_value, 'new_value': self.new_value}
    @classmethod
    def _from_serializable_data(cls, app, data, timestamp):
        return cls(app, data['student_id'], data['style_property'], data['old_value'], data['new_value'], timestamp)
    def get_description(self):
        student_name = self.app.students.get(self.student_id, {}).get('first_name', 'Unknown')
        return f"Style Change: {self.style_property} for {student_name}"

class ManageStudentGroupCommand(Command):
    def __init__(self, app, old_groups_snapshot, new_groups_snapshot,
                 old_student_group_assignments, new_student_group_assignments,
                 old_next_group_id_num, new_next_group_id_num, timestamp=None):
        super().__init__(app, timestamp)
        self.old_groups_snapshot = old_groups_snapshot
        self.new_groups_snapshot = new_groups_snapshot
        self.old_student_group_assignments = old_student_group_assignments
        self.new_student_group_assignments = new_student_group_assignments
        self.old_next_group_id_num = old_next_group_id_num
        self.new_next_group_id_num = new_next_group_id_num

    def execute(self):
        self.app.student_groups = self.new_groups_snapshot.copy()
        for student_id, group_id in self.new_student_group_assignments.items():
            if student_id in self.app.students: self.app.students[student_id]['group_id'] = group_id
        for student_id in self.app.students:
            if student_id not in self.new_student_group_assignments and 'group_id' in self.app.students[student_id]:
                del self.app.students[student_id]['group_id']
        self.app.next_group_id_num = self.new_next_group_id_num
        self.app.settings["next_group_id_num"] = self.new_next_group_id_num
        self.app.save_student_groups()
        self.app.draw_all_items(check_collisions_on_redraw=True)
        self.app.update_status("Student groups updated.")

    def undo(self):
        self.app.student_groups = self.old_groups_snapshot.copy()
        for student_id, group_id in self.old_student_group_assignments.items():
            if student_id in self.app.students: self.app.students[student_id]['group_id'] = group_id
        for student_id in self.app.students:
            if student_id not in self.old_student_group_assignments and 'group_id' in self.app.students[student_id]:
                del self.app.students[student_id]['group_id']
        self.app.next_group_id_num = self.old_next_group_id_num
        self.app.settings["next_group_id_num"] = self.old_next_group_id_num
        self.app.save_student_groups()
        self.app.draw_all_items(check_collisions_on_redraw=True)
        self.app.update_status("Student group update undone.")

    def _get_data_for_serialization(self):
        return {
            'old_groups_snapshot': self.old_groups_snapshot, 'new_groups_snapshot': self.new_groups_snapshot,
            'old_student_group_assignments': self.old_student_group_assignments, 'new_student_group_assignments': self.new_student_group_assignments,
            'old_next_group_id_num': self.old_next_group_id_num, 'new_next_group_id_num': self.new_next_group_id_num,
        }
    @classmethod
    def _from_serializable_data(cls, app, data, timestamp):
        return cls(app, data['old_groups_snapshot'], data['new_groups_snapshot'],
                   data['old_student_group_assignments'], data['new_student_group_assignments'],
                   data['old_next_group_id_num'], data['new_next_group_id_num'], timestamp)
    def get_description(self):
        return "Manage Student Groups"

class ResetSettingsCommand(Command):
    def __init__(self, app, timestamp=None):
        super().__init__(app, timestamp)
        self.old_settings = None
        self.new_settings = None

    def execute(self):
        if self.old_settings is None:
            self.old_settings = {k: v.copy() if isinstance(v, (dict, list)) else v for k, v in self.app.settings.items()}
        
        self.app.reset_settings_to_default()
        self.new_settings = {k: v.copy() if isinstance(v, (dict, list)) else v for k, v in self.app.settings.items()}
        
        self.app.update_status("Settings reset to default.")
        self.app.draw_all_items(check_collisions_on_redraw=True)

    def undo(self):
        if self.old_settings is not None:
            self.app.settings = self.old_settings.copy()
            self.app.update_status("Undo settings reset.")
            self.app.draw_all_items(check_collisions_on_redraw=True)

    def _get_data_for_serialization(self):
        return {
            'old_settings': self.old_settings,
            'new_settings': self.new_settings
        }

    @classmethod
    def _from_serializable_data(cls, app, data, timestamp):
        cmd = cls(app, timestamp)
        cmd.old_settings = data.get('old_settings')
        cmd.new_settings = data.get('new_settings')
        return cmd

    def get_description(self):
        return "Reset All Settings"

# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    from seatingchartmain import SeatingChartApp
    app = SeatingChartApp(root)
    try:
        import darkdetect; import threading
        t = threading.Thread(target=darkdetect.listener, args=(app.theme_auto, ))
        t.daemon = True; t.start()
    except: pass
    root.mainloop()