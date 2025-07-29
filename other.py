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
APP_VERSION = "v57.0" # Version incremented
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

MASTER_RECOVERY_PASSWORD_HASH = "5bf881cb69863167a3172fda5c552694a3328548a43c7ee258d6d7553fc0e1a1a8bad378fb131fbe10e37efbd9e285b22c29b75d27dcc2283d48d8edf8063292" # SHA256 of "RecoverMyData123!"
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
        info_text = tk.Text(info_tab, wrap="word", height=20, width=70, relief=tk.FLAT, font=('Arial', 11))
        info_text.tag_configure("bold", font=('Arial', 11, 'bold'))

        info_text.insert("end", f"Welcome to {APP_NAME}!\n\n")
        info_text.insert("end", "This application helps you track student behaviors, quiz scores, and homework completion in a visual classroom layout.\n\n")

        info_text.insert("end", "Key Features:\n", "bold")
        info_text.insert("end",
                         "- Visual seating chart: Drag-and-drop students and furniture. Includes Rulers, a Grid, and draggable Guides for precise alignment.\n"
                         "- Layout Tools: Align and distribute multiple selected items for a clean layout.\n"
                         "- Behavior Logging: Quickly log predefined or custom behaviors for students.\n"
                         "- Quiz Logging: Record quiz scores with detailed marks. Supports live quiz sessions and quiz templates.\n"
                         "- Homework Logging: Track homework completion status and scores. Supports:\n"
                         "    - Manual logging (simplified type/status or detailed with marks).\n"
                         "    - Live homework sessions (\"Yes/No\" for multiple assignments or \"Select\" for predefined statuses).\n"
                         "    - Customizable homework types, statuses, and mark types.\n"
                         "    - Homework templates.\n"
                         "- Live Sessions: Conduct real-time quiz or homework checks directly on the seating chart.\n"
                         "- Advanced Conditional Formatting: Automatically change student box appearance based on groups, behavior counts, quiz scores, live session responses, and more. Rules can be active during specific times and in specific application modes.\n"
                         "- Data Export & Import: Export logs to Excel/CSV for reporting. Import student rosters from Excel.\n"
                         "- Undo/Redo & History: Most actions can be undone/redone. View the full action history and revert to any point.\n"
                         "- Security: Optional password protection with auto-lock and data file encryption.\n"
                         "- Data Backup & Restore: Keep your classroom data safe with ZIP backups.\n"
                         "- Themes: Light and Dark mode support with customizable canvas color.\n\n")

        info_text.insert("end", "Navigation & Interaction Tips:\n", "bold")
        info_text.insert("end",
                         "- Canvas Panning: Middle-click and drag, or Shift + Mouse Wheel for horizontal scroll.\n"
                         "- Canvas Zoom: Ctrl + Mouse Wheel.\n"
                         "- Multi-Select: Ctrl + Left-click to select multiple items.\n"
                         "- Context Menus: Right-click on items or the canvas for quick actions.\n"
                         "- Edit Mode: Toggle \"Edit Mode\" to resize items by dragging their bottom-right corner.\n"
                         "- Layout Tools: Use the \"Layout Tools\" buttons (e.g., Align Top, Distribute H) when multiple items are selected.\n"
                         "- Visual Guides: Toggle Rulers on (in Settings or View controls) and then use \"Add V Guide\" or \"Add H Guide\" to create alignment lines you can drag around the canvas.\n"
                         "- Undo History: Use the \"Show undo history\" button to view all past actions and revert if needed.\n"
                         "- Data Files: Your classroom data is stored locally (JSON files). Use 'File > Open Data Folder' to access them. Regularly backup using 'File > Backup All Application Data (.zip)...'.\n"
                         "- Exported Layout Images: The 'Export Layout as Image' feature uses PostScript. For it to work correctly, Ghostscript needs to be installed and accessible in your system's PATH.\n\n")

        info_text.insert("end", "Keyboard Shortcuts:\n", "bold")
        info_text.insert("end",
                         "- Ctrl+S: Save data\n"
                         "- Ctrl+Q: Save and Exit\n"
                         "- Ctrl+Z: Undo last action\n"
                         "- Ctrl+Y / Ctrl+Shift+Z: Redo last action\n"
                         "- Ctrl+L: Lock the application\n"
                         "- Delete / Backspace: Delete selected item(s)\n\n"
                         "- E: Toggle Edit Mode\n"
                         "- B: Switch to Behavior Mode\n"
                         "- Q: Switch to Quiz Mode\n"
                         "- H: Switch to Homework Mode\n\n"
                         "- Ctrl + (+): Zoom In\n"
                         "- Ctrl + (-): Zoom Out\n"
                         "- Ctrl + 0: Reset Zoom\n\n"
                         "- S: Open Settings\n"
                         "- P: Open this Help dialog\n")

        info_text.config(state="disabled")
        info_text.pack(pady=5, fill="both", expand=True)
        notebook.add(info_tab, text="General Info")

        # --- What's New Tab ---
        whats_new_tab = ttk.Frame(notebook, padding=10)
        whats_new_text = tk.Text(whats_new_tab, wrap="word", height=20, width=70, relief=tk.FLAT, font=('Arial', 11))
        whats_new_text.tag_configure("bold", font=('Arial', 11, 'bold'))

        whats_new_text.insert("end", f"What's New in Version {self.app_version}:\n\n")

        whats_new_text.insert("end", "  - Settings:", "bold")
        whats_new_text.insert("end", " Added undo/redo functionality in settings. You can use the buttons or Ctrl+z, Ctrl+Shift+Z, and Ctrl+y\n\n")

        whats_new_text.insert("end", "- General Improvements:\n", "bold")
        whats_new_text.insert("end", "  - Bug fixes and performance enhancements.\n")

        whats_new_text.config(state="disabled")
        whats_new_text.pack(pady=5, fill="both", expand=True)
        notebook.add(whats_new_tab, text="What's New")

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
         - "Yes/No" Mode: Mark multiple predefined homework types (e.g., "Reading Assignment," "Math Problems") as "Yes" (done) or "No" (not done) for each student. These types are managed in Settings > Homework > "Homework Types".
         - "Select" Mode: Choose one or more predefined statuses (e.g., "Complete," "Handed In Late," "Signed") for the current session. These options are managed in Settings > Homework > "Manage 'Select' Mode Options...".
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

- General:
    - Application Behavior: Autosave interval, student group feature toggle, max undo history.
    - Canvas Management: Toggle visibility of box management tools, canvas borders, and grid. Enable/disable grid snapping, collision checks, and box dragging.
    - Canvas View Options: Configure rulers, grid, and layout guides. Set colors for grid and guides, and control whether guides are saved to the data file.
    - Theme & Appearance: Choose between Light, Dark, or System themes. Set a custom background color for the main seating chart canvas.

- Student Boxes:
    - Default Appearance: Set default size, colors, and font for student boxes.
    - Conditional Formatting: Create powerful rules to change box appearance.
        - Rule Types: Trigger formatting based on Group, Behavior Count, Quiz Score, Quiz Mark Count, Live Quiz Response, or Live Homework Status.
        - Actions: Change fill and outline colors.
        - Application Style: 'Override' replaces the box color, while 'Stripe' adds a colored stripe, allowing multiple rules to be visible at once.
        - Scoping: Rules can be restricted to run only during specific times of day or when the app is in a certain mode (e.g., only apply a rule during a live quiz session).
        - Bulk Edit: Modify the enabled status, active times, or active modes for multiple rules at once.

- Behavior & Quiz:
    - Recent Incidents Display: Control how behavior/quiz logs appear on student boxes.
    - Customization: Manage custom behaviors, their display initials, and quiz mark types (e.g., Correct, Bonus).
    - Defaults & Templates: Set default quiz names and question counts. Create reusable Quiz Templates for frequent assessments.

- Homework:
    - Recent Homework Display: Control if and how recent homework logs appear on student boxes.
    - Customization:
        - Homework Types: Define the types of homework you assign (e.g., "Reading Assignment"). Used for both manual logging and the "Yes/No" live session mode.
        - Homework Statuses: Define general statuses for the simplified manual log (e.g., "Done," "Late").
        - Initials & Mark Types: Customize display initials and define mark types for detailed grading (e.g., "Completeness," "Effort Score").
    - Live Homework Session: Configure the default session name, and choose the session mode ("Yes/No" or "Select"). Manage the options available in "Select" mode.
    - Manual Logging: Toggle between the simplified (Type/Status) and detailed (Marks) logging dialogs.
    - Homework Templates: Create reusable templates for common assignments.

- Data & Export: Configure default options for Excel exports and set the output DPI for image exports.
- Security: Set an application password, configure auto-lock, and enable/disable data file encryption.

Remember to click "Apply" or "OK" in the Settings dialog to save your changes!
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
        
- The 'Export Layout as Image' function works, but it doesn't capture Hebrew. Just make sure to have Ghostscript installed.
- I am still working on the homework logging and exporting - so expect to see more features, and don't be surprised if something doesn't work as expected.
- The Conditional Formatting feature is now very powerful, supporting quizzes, homework, and live sessions. If you have more than one 'stripe' rule applying to the same box, it will split the box into different colored sections.
- If you are trying to undo or redo a move of a box and the program keeps saying "Adjusted layout for _ items due to overlap with _______." you may need to turn off checking for collisions on box move in settings (General Tab).
- This Help section is updated as of {self.app_version}, but new features may be added.

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

# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    import sv_ttk
    sv_ttk.set_theme("Light")
    from seatingchartmain import SeatingChartApp
    app = SeatingChartApp(root)
    try:
        import darkdetect; import threading
        t = threading.Thread(target=darkdetect.listener, args=(app.theme_auto, ))
        t.daemon = True; t.start()
    except: pass
    root.mainloop()