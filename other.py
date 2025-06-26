import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import os
import sys

from datetime import datetime
import hashlib # For password hashing

import portalocker
# Conditional import for platform-specific screenshot capability


# def listener(callback: typing.Callable[[str], None]) -> None: ...

# TODO: make conditional formatting work by quizzes. add thing for homework also.

# --- Application Constants ---
APP_NAME = "BehaviorLogger"
APP_VERSION = "v52.0" # Version incremented
CURRENT_DATA_VERSION_TAG = "v9" # Incremented for new homework/marks features

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

MASTER_RECOVERY_PASSWORD_HASH = "d3c01af653d8940fc36ea1e1f33a8dc03f47dd864d2cd0d8814e2643fa37e70de0a2228e58d7d591eb2f124e2f4f9ff7c98686f4f5da3de6bbfc0267db3c1a0e" # SHA256 of "RecoverMyData123!"
#Recovery1Master2Password!Jaffe1












# --- File Lock Manager ---
class FileLockManager:
    def __init__(self, lock_file_path):
        self.lock_file_path = lock_file_path
        self.lock = None

    def acquire_lock(self):
        try:
            # Open the lock file in exclusive mode, creating it if it doesn't exist.
            # portalocker will raise an exception if the lock cannot be acquired.
            self.lock = open(self.lock_file_path, 'w')
            portalocker.lock(self.lock, portalocker.LOCK_EX | portalocker.LOCK_NB)
            # Write PID to lock file for informational purposes (optional)
            self.lock.write(str(os.getpid()))
            self.lock.flush()
            return True
        except ( IOError, BlockingIOError) as e:
            # Check if lock file exists and try to read PID
            pid_in_lock = None
            if os.path.exists(self.lock_file_path):
                try:
                    with open(self.lock_file_path, 'r') as f_read:
                        pid_in_lock = f_read.read().strip()
                except IOError:
                    pass # Could not read PID
            
            error_message = f"Another instance of {APP_NAME} may already be running."
            if pid_in_lock:
                error_message += f" (PID in lock file: {pid_in_lock})"
            else:
                error_message += " (Could not read PID from lock file)."
            error_message += f"\n\nIf you are sure no other instance is running, you can manually delete the lock file:\n{self.lock_file_path}\n\nError details: {e}"
            
            messagebox.showerror("Application Already Running?", error_message)
            if self.lock: # Close the file handle if it was opened but locking failed
                portalocker.unlock(self.lock)
                self.lock.close()
                self.lock = None
            return False
        
    def release_lock(self):
        if self.lock:
            try:
                portalocker.unlock(self.lock)
                self.lock.close()
            except Exception as e:
                print(f"Warning: Error releasing file lock: {e}")
            finally:
                self.lock = None
                # Attempt to delete the lock file
                try:
                    if os.path.exists(self.lock_file_path):
                        os.remove(self.lock_file_path)
                except OSError as e:
                    print(f"Warning: Could not delete lock file {self.lock_file_path}: {e}")
# --- Password Management ---
class PasswordManager:
    def __init__(self, app_settings):
        self.app_settings = app_settings
        self.is_locked = False
        self.last_activity_time = datetime.now()

    def _hash_password(self, password):
        return hashlib.sha3_512(password.encode('utf-8')).hexdigest()

    def set_password(self, password):
        if not password:
            self.app_settings["app_password_hash"] = None
            return True
        self.app_settings["app_password_hash"] = self._hash_password(password)
        return True

    def check_password(self, password):
        stored_hash = self.app_settings.get("app_password_hash")
        if not stored_hash: return True
        return self._hash_password(password) == stored_hash

    def check_recovery_password(self, recovery_password):
        return self._hash_password(recovery_password) == MASTER_RECOVERY_PASSWORD_HASH

    def is_password_set(self):
        return bool(self.app_settings.get("app_password_hash"))

    def lock_application(self):
        if self.is_password_set():
            self.is_locked = True
            return True
        return False

    def unlock_application(self, password_attempt):
        if self.check_password(password_attempt) or self.check_recovery_password(password_attempt):
            self.is_locked = False
            self.last_activity_time = datetime.now()
            return True
        return False

    def check_auto_lock(self):
        if self.is_locked or not self.is_password_set() or not self.app_settings.get("password_auto_lock_enabled", False):
            return
        timeout_minutes = self.app_settings.get("password_auto_lock_timeout_minutes", 15)
        if timeout_minutes > 0:
            if (datetime.now() - self.last_activity_time).total_seconds() / 60 > timeout_minutes:
                self.lock_application()

    def record_activity(self):
        self.last_activity_time = datetime.now()


class HelpDialog(simpledialog.Dialog):
    def __init__(self, parent, app_version):
        self.app_version = app_version
        super().__init__(parent, f"Help & About - {APP_NAME}")

    def body(self, master):
        main_frame = ttk.Frame(master); main_frame.pack(expand=True, fill="both")
        
        header_label = ttk.Label(main_frame, text=f"{APP_NAME} - Version {self.app_version}", font=("", 14, "bold"))
        header_label.pack(pady=(10,5))
        
        notebook = ttk.Notebook(main_frame)
        
        # --- General Info Tab ---
        info_tab = ttk.Frame(notebook, padding=10)
        info_text_content = f"""Welcome to {APP_NAME}!

This application helps you track student behaviors, quiz scores, and homework completion in a visual classroom layout.

Key Features:
- Visual seating chart: Drag and drop students and furniture.
- Behavior Logging: Quickly log predefined or custom behaviors for students.
- Quiz Logging: Record quiz scores, including detailed marks.
- Homework Logging: Track homework status via manual logs or live sessions.
- Live Sessions: Conduct real-time quiz or homework checks directly on the seating chart.
- Customization: Define your own behaviors, homework types, mark types, and layout templates.
- Data Export: Export logs to Excel or CSV for reporting and analysis.
- Undo/Redo: Most actions can be undone and redone.
- Password Protection: Secure your application data.
- Data Backup & Restore: Keep your classroom data safe.

Navigation & Interaction Tips:
- Canvas Panning: Middle-click and drag to pan the seating chart.
- Canvas Zoom: Ctrl + Mouse Wheel to zoom in/out. Shift + Mouse Wheel for horizontal scroll.
- Multi-Select: Ctrl + Left-click to select multiple items.
- Context Menus: Right-click on items or the canvas for quick actions.
- Edit Mode: Toggle "Edit Mode (Resize)" to resize items by dragging their bottom-right corner.
- Combobox Scrolling: You can often use the mouse wheel to scroll through options in dropdown (combobox) lists, even if a scrollbar isn't visible.
- Data Files: Your classroom data is stored locally. Use 'File > Open Data Folder' to access these files. Regularly backup using 'File > Backup All Application Data'.
"""
        info_text = tk.Text(info_tab, wrap="word", height=20, width=70, relief=tk.FLAT, font=('Arial',11))
        info_text.insert("1.0", info_text_content)
        info_text.config(state="disabled")
        info_text.pack(pady=5, fill="both", expand=True)
        notebook.add(info_tab, text="General Info")

        # --- Modes Tab ---
        modes_tab = ttk.Frame(notebook, padding=10)
        modes_text_content = f"""Application Modes:

The application operates in three main modes, selectable from the top toolbar:

1. Behavior Mode:
   - Default mode for general classroom management.
   - Clicking a student allows logging of behaviors (e.g., "Talking", "Great Participation").
   - Recent behavior logs can be displayed on student boxes.

2. Quiz Mode:
   - Focused on quiz-related activities.
   - Clicking a student allows logging of a quiz score with detailed marks.
   - Live Quiz Session:
     - Start a "Class Quiz" session to mark students' answers (Correct/Incorrect/Skip) in real-time.
     - Scores are displayed live on student boxes.
     - Session data is logged upon ending the session.
   - Quiz Templates: Define reusable quiz structures (name, number of questions, default marks) in Settings.

3. Homework Mode (New!):
   - Dedicated to tracking homework.
   - Clicking a student allows:
     - Manual Logging: Log detailed homework status (e.g., "Done", "Not Done", "Signed") and optionally record marks/scores if enabled in settings.
     - Live Homework Session:
       - Start a "Homework Session" (e.g., "Daily Homework Check").
       - Session Mode (configurable in Settings > Homework):
         - "Yes/No" Mode: Quickly mark predefined homework types (e.g., "Reading Assignment: Yes/No", "Math Worksheet: Yes/No"). Define these types in Settings > Homework.
         - "Select" Mode: Choose from a list of predefined statuses (e.g., "Done", "Signed", "Missing"). Define these options in Settings > Homework.
       - Statuses are displayed live on student boxes.
       - Session data is logged upon ending.
   - Homework Templates: Define reusable homework assignments (name, number of items, default marks/statuses) in Settings.
   - Recent homework logs can be displayed on student boxes.

Switching Modes:
- If a Live Quiz or Live Homework session is active, you will be prompted to end or discard the session before switching modes or closing the application.
"""
        modes_text = tk.Text(modes_tab, wrap="word", height=20, width=70, relief=tk.FLAT, font=('Arial',11))
        modes_text.insert("1.0", modes_text_content)
        modes_text.config(state="disabled")
        modes_text.pack(pady=5, fill="both", expand=True)
        notebook.add(modes_tab, text="Application Modes")

        # --- Settings & Customization Tab ---
        settings_tab = ttk.Frame(notebook, padding=10)
        settings_text_content = f"""Settings & Customization:

The "Settings" dialog allows extensive customization:

- General: Autosave interval, grid snapping, student group feature toggle, max undo history.
- Student Boxes: Default appearance (size, colors, font), and Conditional Formatting rules (e.g., change box color if a student is in a specific group or has many recent incidents).
- Behavior & Quiz:
    - Recent Incidents Display: Control how behavior/quiz logs appear on student boxes.
    - Custom Behaviors: Add your own behavior types.
    - Behavior/Quiz Initials: Customize the initials displayed for behaviors/quizzes.
    - Quiz Mark Types: Define the categories for quiz marks (e.g., Correct, Incorrect, Bonus) and their properties.
    - Quiz Session Defaults: Default quiz name, number of questions for manual log.
    - Quiz Templates: Manage reusable quiz structures.
- Homework (New!):
    - Recent Homework Display: Control how homework logs appear on student boxes.
    - Custom Homework Log Options: Define statuses for manual homework logging (e.g., "Done", "Not Done", "Late").
    - Homework Log Initials: Customize initials for homework log entries.
    - Homework Mark Types: Define categories for homework marks (e.g., Complete, Incomplete, Effort Score) and their properties.
    - Live Homework Session:
        - Default session name.
        - Session Mode: Choose between "Yes/No" or "Select".
        - Custom Types for "Yes/No" Mode: Define the list of homeworks to check (e.g., "Reading", "Math").
        - Options for "Select" Mode: Define the buttons available (e.g., "Done", "Signed").
    - Enable Detailed Marks: Toggle whether to log detailed scores/marks for manual homework entries.
    - Homework Templates: Manage reusable homework assignment structures.
- Data & Export: Default options for Excel export (separate sheets, include summary). Enable experimental Excel autosave.
- Security: Set an application password, configure password prompts (on open, for sensitive actions), and auto-lock settings.

Remember to save your settings after making changes!
"""
        settings_text = tk.Text(settings_tab, wrap="word", height=20, width=70, relief=tk.FLAT, font=('Arial',11))
        settings_text.insert("1.0", settings_text_content)
        settings_text.config(state="disabled")
        settings_text.pack(pady=5, fill="both", expand=True)
        notebook.add(settings_tab, text="Settings & Customization")
        
         # --- Settings & Customization Tab ---
        remarks_tab = ttk.Frame(notebook, padding=10)
        remarks_text_content = f"""
        Please note the following:
        
- The 'Export Layout as Image' function now works!!! Just make sure to have Ghostscript installed.
- I am still working on the homework logging and exporting - so expect to see more features, and don't be surprised if something doesn't work as expected.
- The Conditional Formatting feature now works for quizzes, and if you have more than one rule applying to the same box, it will split the box into different sections.
- If you are trying to undo or redo a move of a box and the program keeps saying "Adjusted layout for _ items due to overlap with _______." you may need to turn off checking for collisions on box move in settings (General Tab).
- The Help section is not updated often enough, so it may not contain up-to-date information.
    -Yaakov Maimon
"""        
        remarks_text = tk.Text(remarks_tab, wrap="word", height=20, width=70, relief=tk.FLAT, font=('Arial',11))
        remarks_text.insert("1.0", remarks_text_content)
        remarks_text.config(state="disabled")
        remarks_text.pack(pady=5, fill="both", expand=True)
        notebook.add(remarks_tab, text="Remarks & Notices")
        
        # --- Feedback & Contact Tab ---
        feedback_tab = ttk.Frame(notebook, padding=10)
        feedback_text_content = f"""
Contact Me:
        
Yaakov Maimon
Email: yaakovmaimon592@gmail.com
Phone: +1 206-750-5557

"""
        feedback_text = tk.Text(feedback_tab, wrap="word", height=20, width=70, relief=tk.FLAT, font=('Arial',11))
        feedback_text.insert("1.0", feedback_text_content)
        feedback_text.config(state="disabled")
        feedback_text.pack(pady=5, fill="both", expand=True)
        notebook.add(feedback_tab, text="Feedback")
        

        notebook.pack(expand=True, fill="both", pady=5)
        return main_frame # No specific focus needed

    def buttonbox(self): # Override to only show an OK button
        box = ttk.Frame(self)
        ok_button = ttk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        ok_button.pack(pady=5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.ok)
        box.pack()

