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
APP_VERSION = "v54.0" # Version incremented
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
- Quiz Logging: Record quiz scores, including detailed marks. Supports live quiz sessions and quiz templates.
- Homework Logging: Track homework completion status and scores. Supports:
    - Manual logging (simplified type/status or detailed with marks).
    - Live homework sessions ("Yes/No" for multiple assignments or "Select" for predefined statuses).
    - Customizable homework types, statuses, and mark types.
    - Homework templates.
- Live Sessions: Conduct real-time quiz or homework checks directly on the seating chart.
- Customization: Define your own behaviors, quiz/homework mark types, homework types/statuses, and layout/quiz/homework templates.
- Conditional Formatting: Change student box appearance based on group or behavior/quiz data.
- Data Export: Export logs to Excel or CSV for reporting and analysis. Includes attendance reports.
- Data Import: Import student rosters from Excel.
- Undo/Redo: Most actions can be undone and redone.
- Password Protection: Secure your application data with optional auto-lock.
- Data Backup & Restore: Keep your classroom data safe with ZIP backups.
- Themes: Light and Dark mode support with customizable canvas color.

Navigation & Interaction Tips:
- Canvas Panning: Middle-click and drag, or Shift + Mouse Wheel for horizontal scroll.
- Canvas Zoom: Ctrl + Mouse Wheel.
- Multi-Select: Ctrl + Left-click to select multiple items.
- Context Menus: Right-click on items or the canvas for quick actions.
- Edit Mode: Toggle "Edit Mode (Resize)" to resize items by dragging their bottom-right corner (when selected).
- Combobox Scrolling: Use the mouse wheel to scroll through options in dropdown (combobox) lists.
- Data Files: Your classroom data is stored locally (JSON files). Use 'File > Open Data Folder' to access them. Regularly backup using 'File > Backup All Application Data (.zip)...'.
- Exported Layout Images: The 'Export Layout as Image' feature uses PostScript. For it to work correctly, Ghostscript needs to be installed and accessible in your system's PATH.
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

3. Homework Mode:
   - Dedicated to tracking all aspects of homework.
   - Clicking a student in this mode allows for:
     - Manual Homework Logging:
       - Simplified View: If "Enable Detailed Marks" is OFF in Homework Settings, you'll select a Homework Type (e.g., "Reading") and then a Status (e.g., "Done").
       - Detailed View: If "Enable Detailed Marks" is ON, a full dialog appears to log the homework type, comment, number of items, and specific marks (e.g., points for "Completeness," "Effort Score").
     - Live Homework Session:
       - Click "Start Session" under "Homework Session" in the top toolbar.
       - Name the session (e.g., "Nightly Reading Check").
       - Student boxes will update to show homework status for this live session.
       - Clicking a student opens a marking dialog based on the "Live Homework Session Mode" (set in Settings > Homework):
         - "Yes/No" Mode: Mark multiple predefined homework types (e.g., "Reading Assignment," "Math Problems") as "Yes" (done) or "No" (not done) for each student. These types are managed in Settings > Homework > "Custom Types for 'Yes/No' Mode".
         - "Select" Mode: Choose one or more predefined statuses (e.g., "Complete," "Handed In Late," "Signed") for the current session. These options are managed in Settings > Homework > "Options for 'Select' Mode".
       - Live statuses are displayed on student boxes.
       - End the session to log all collected data.
   - Homework Templates: Create and use templates for common homework assignments (name, number of items, default marks/statuses) via Settings > Homework. These can be quickly applied during manual detailed logging.
   - Recent Homework Logs: Similar to behavior incidents, recent homework entries can be displayed directly on student boxes if enabled in Settings.

Switching Modes:
- If a Live Quiz or Live Homework session is active, you will be prompted to end (and log) or discard the session before switching modes or closing the application. This ensures no live data is accidentally lost.
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
    - Custom Behaviors: Add your own behavior types (Settings > Behavior/Quiz > "Manage Custom Behaviors").
    - Behavior/Quiz Initials: Customize the initials displayed for behaviors/quizzes on student boxes (Settings > Behavior/Quiz > "Manage Initials...").
    - Quiz Mark Types: Define categories for quiz marks (e.g., Correct, Incorrect, Bonus), their points, and if they contribute to the total or are bonus (Settings > Behavior/Quiz > "Manage Quiz Mark Types").
    - Quiz Session Defaults: Set the default quiz name for live sessions and the default number of questions for manual quiz logging.
    - Quiz Templates: Create and manage reusable quiz structures (name, number of questions, default marks for each mark type) (Settings > Behavior/Quiz > "Manage Quiz Templates").
- Homework:
    - Recent Homework Display: Control if and how recent homework logs appear on student boxes (Settings > Homework > "Show Recent Homework Logs on Boxes", etc.).
    - Custom Homework Types (for Yes/No Live Mode & Manual Logging): Define the types of homework you assign (e.g., "Reading Assignment," "Worksheet") (Settings > Homework > "Manage Custom Homework Types"). These are used for the "Yes/No" live session mode and as types in manual logging.
    - Custom Homework Statuses (for Simplified Manual Logging): Define general statuses for the simplified manual homework log (e.g., "Done," "Not Done," "Late") (Settings > Homework > "Manage Custom Homework Statuses").
    - Homework Log Initials: Customize initials for homework log entries displayed on student boxes (Settings > Homework > "Manage Initials for Homework Logs...").
    - Homework Mark Types: Define categories for detailed homework marks (e.g., "Complete," "Incomplete," "Effort Score (1-5)") and their default points (Settings > Homework > "Manage Homework Mark Types").
    - Live Homework Session:
        - Default session name for live homework checks.
        - Session Mode: Choose between "Yes/No" (quick marking of predefined types) or "Select" (choosing from a list of statuses).
        - Options for "Select" Mode: Define the buttons/statuses available in "Select" live mode (e.g., "Done," "Signed," "Missing") (Settings > Homework > "Manage 'Select' Mode Options...").
    - Enable Detailed Marks: Toggle whether the manual homework logging dialog should include detailed mark entry fields or use the simplified type/status selection (Settings > Homework > "Enable Detailed Marks for Manual Log").
    - Homework Templates: Create and manage reusable homework assignment structures (name, number of items, pre-filled marks/statuses) (Settings > Homework > "Manage Homework Templates").
- Data & Export: Configure default options for Excel exports (e.g., whether to create separate sheets per log type, include a summary sheet). Enable/disable Excel autosave.
- Security: Set an application password, configure when password prompts occur (on application open, before sensitive edit actions), and set up an auto-lock timer for inactivity.
- Theme & Appearance: Choose between Light, Dark, or System themes. Set a custom background color for the main seating chart canvas. Enable/disable text background panels on student boxes.

Remember to click "Apply" or "OK" in the Settings dialog to save your changes!
"""
        settings_text = tk.Text(settings_tab, wrap="word", height=20, width=70, relief=tk.FLAT, font=('Arial',11))
        settings_text.insert("1.0", settings_text_content)
        settings_text.config(state="disabled")
        settings_text.pack(pady=5, fill="both", expand=True)
        notebook.add(settings_tab, text="Settings & Customization")
        
         # --- Settings & Customization Tab ---
        remarks_tab = ttk.Frame(notebook, padding=10)
        remarks_text_content = f"""Remarks & Notices:

- Image Export ('Export Layout as Image'): This feature captures the current view of your seating chart. It uses your system's PostScript capabilities. For this to work reliably, especially on Windows, you may need to have Ghostscript installed and accessible in your system's PATH. If you encounter errors, please ensure Ghostscript is set up correctly.
- Conditional Formatting:
    - Currently, conditional formatting rules based on quiz scores or specific quiz mark counts are being refined.
    - If multiple conditional formatting rules apply to a student, the application will attempt to show this by striping the box. However, for rules that set a base color (like group-based rules), the first matching rule encountered will determine the base.
- Automatic Layout Adjustment: If "Check for Collisions on Box Move" is enabled in General Settings, moving a student box might cause other items to shift to avoid overlap. If this behavior is disruptive, you can disable it.
- Data Integrity: While the application includes backup and restore features, always ensure you have manual backups of your critical data, especially before major updates or system changes. The data is stored in JSON files in the application's data folder (accessible via File > Open Data Folder).
- Feature Development: This application is actively developed. Some newer features, particularly around detailed homework analysis and advanced conditional formatting, are still evolving. Your feedback is valuable!

    - Yaakov Maimon
"""
        remarks_text = tk.Text(remarks_tab, wrap="word", height=20, width=70, relief=tk.FLAT, font=('Arial',11))
        remarks_text.insert("1.0", remarks_text_content)
        remarks_text.config(state="disabled")
        remarks_text.pack(pady=5, fill="both", expand=True)
        notebook.add(remarks_tab, text="Remarks & Notices")
        
        # --- Feedback & Contact Tab ---
        feedback_tab = ttk.Frame(notebook, padding=10)
        feedback_text_content = f"""                                                    Contact the developer:
        
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

