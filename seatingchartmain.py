import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog, font as tkfont
import json
import os
import sys
import subprocess
from datetime import datetime, timedelta, date as datetime_date
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font as OpenpyxlFont, Alignment as OpenpyxlAlignment
from openpyxl.utils import get_column_letter
import re
import shutil
import zipfile
import csv
import PIL
from PIL import Image
from settingsdialog import SettingsDialog
from commands import Command, DeleteGuideCommand, MoveItemsCommand, AddItemCommand, DeleteItemCommand, LogEntryCommand, \
    LogHomeworkEntryCommand, EditItemCommand, ChangeItemsSizeCommand, MarkLiveQuizQuestionCommand, \
        MarkLiveHomeworkCommand, ChangeStudentStyleCommand, ManageStudentGroupCommand, MoveGuideCommand, AddGuideCommand
from dialogs import PasswordPromptDialog, AddEditStudentDialog, AddFurnitureDialog, BehaviorDialog, \
    ManualHomeworkLogDialog, QuizScoreDialog, LiveQuizMarkDialog, LiveHomeworkMarkDialog, ExitConfirmationDialog, \
        ImportExcelOptionsDialog, SizeInputDialog, StudentStyleDialog,  AttendanceReportDialog, ManageStudentGroupsDialog
from quizhomework import ManageQuizTemplatesDialog, ManageHomeworkTemplatesDialog
from other import FileLockManager, PasswordManager, HelpDialog
from exportdialog import ExportFilterDialog
from data_locker import unlock_file, DATA_FILE
import json
from data_encryption import encrypt_data, decrypt_data
# Replace with your actual path to gswinXXc.exe
#EpsImagePlugin.gs_windows_binary = "C:\\Program Files\\gs\\gs10.05.1\bin\\gswin64c.exe" 
# Only use this ^ if something really doesn't work. Otherwise, it works even with just installing Ghostscript regularly, without any additional steps.
import sv_ttk # For themed widgets
import darkdetect # For dark mode detection
# Conditional import for platform-specific screenshot capability
import threading
import io
import tempfile
import cryptography.fernet # For making sure that the program can properly handle encrypted and non-encrypted data files
try:
    if sys.platform == "win32":
        import win32gui
        import win32ui
        import win32con
    else:
        # For non-Windows, these modules won't be available or needed for the current screenshot method.
        # The postscript-based method is platform-independent.
        win32gui = None
except ImportError:
    win32gui = None # Explicitly set to None if import fails
    print("Warning: win32gui/win32ui/win32con not found. Full window screenshot (deprecated) might not work if called.")

# def listener(callback: typing.Callable[[str], None]) -> None: ...
# TODO: make conditional formatting work by quizzes. add thing for homework also.

# --- Application Constants ---
APP_NAME = "BehaviorLogger"
APP_VERSION = "v55.0" # Version incremented
CURRENT_DATA_VERSION_TAG = "v10" # Incremented for guide saving

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
    """
    Determines the appropriate path for application data files based on the operating system.

    This function ensures that data files are stored in standard locations (e.g., AppData on Windows,
    Application Support on macOS, .config on Linux) when the application is packaged (frozen).
    If the application is running as a script, it uses the script's directory.

    Args:
        filename (str): The name of the file for which to get the path.

    Returns:
        str: The full, absolute path to the data file.
    """
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
IMAGENAMEW = "export_layout_as_image_helper"

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

MASTER_RECOVERY_PASSWORD_HASH = "5bf881cb69863167a3172fda5c552694a3328548a43c7ee258d6d7553fc0e1a1a8bad378fb131fbe10e37efbd9e285b22c29b75d27dcc2283d48d8edf8063292" # SHA256 of "RecoverMyData123!" # It's actually SHA3_512 or something else, which only Yaakov Maimon (me) has, although you can add your own if you like

def levenshtein_distance(s1, s2):
    """
    Calculates the Levenshtein distance between two strings.

    The Levenshtein distance is the minimum number of single-character edits (insertions, deletions,
    or substitutions) required to change one word into the other.

    Args:
        s1 (str): The first string.
        s2 (str): The second string.

    Returns:
        int: The Levenshtein distance between the two strings.
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def name_similarity_ratio(s1, s2):
    """
    Calculates a name similarity ratio between 0.0 and 1.0 based on Levenshtein distance.

    A ratio of 1.0 means the names are identical (case-insensitively). A ratio of 0.0 means the
    names are completely different. This is useful for fuzzy matching, such as when loading
    layout templates.

    Args:
        s1 (str): The first name string.
        s2 (str): The second name string.

    Returns:
        float: The similarity ratio, where 1.0 is a perfect match.
    """
    if not s1 and not s2: return 1.0 # Both empty
    if not s1 or not s2: return 0.0   # One empty
    distance = levenshtein_distance(s1.lower(), s2.lower())
    max_len = max(len(s1), len(s2))
    if max_len == 0: return 1.0 # Should be caught by above, but defensive
    return 1.0 - (distance / max_len)

# --- Main Application Class ---
class SeatingChartApp:
    """
    The main application class for the Seating Chart and Behavior Logger.

    This class orchestrates the entire application, including the user interface (UI),
    data management, command handling (for undo/redo), and all core logic for tracking
    students, behaviors, quizzes, and homework.
    """
    def __init__(self, root_window):
        """
        Initializes the main application.

        Sets up the main window, loads all data (students, settings, logs, etc.),
        initializes UI components, and binds event handlers.

        Args:
            root_window (tk.Tk): The root Tkinter window for the application.
        """
        # ... (initial part of __init__ is the same) ...
        self.root = root_window
        self.root.title(f"Classroom Behavior Tracker - {APP_NAME} - {APP_VERSION}")
        self.root.geometry("1400x980")
        self.root.state('zoomed') # Maximizes the window on Windows
        self.file_lock_manager = FileLockManager(LOCK_FILE_PATH)
        if not self.file_lock_manager.acquire_lock():
            self.root.destroy()
            sys.exit(1)

        self.is_beginning = True
        
        self.students = {}
        self.furniture = {}
        self.behavior_log = []
        self.homework_log = []
        self.student_groups = {}
        self.quiz_templates = {}
        self.homework_templates = {}

        self.next_student_id_num = 1
        self.next_furniture_id_num = 1
        self.next_group_id_num = 1
        self.next_quiz_template_id_num = 1
        self.next_homework_template_id_num = 1

        self.all_behaviors = []
        self.custom_behaviors = []
        
        # RENAMED/REPURPOSED
        self.all_homework_types = [] # For "Reading Assignment", "Worksheet", etc.
        self.custom_homework_types = []

        self.all_homework_statuses = [] # For "Done", "Not Done", etc.
        self.custom_homework_statuses = []
        
        # This list is now derived from all_homework_types
        self.all_homework_session_types = [] 

        self.last_excel_export_path = None
        self.selected_items = set()
        self.undo_stack = []
        self.redo_stack = []
        self.type_theme = "sv_ttk"
        try:
            self.theme_style_using = sv_ttk.get_theme()
        except:
            self.theme_style_using = "System"
        
        self.settings = self._get_default_settings()
        self.password_manager = PasswordManager(self.settings)

        self.canvas_frame = None; self.canvas = None; self.h_scrollbar = None; self.v_scrollbar = None
        self.status_bar_label = None; self.zoom_display_label = None
        self.mode_var = tk.StringVar(value=self.settings["current_mode"])
        self.edit_mode_var = tk.BooleanVar(value=False)

        self.drag_data = {"x": 0, "y": 0, "item_id": None, "item_type": None,
                          "start_x_world": 0, "start_y_world": 0, # Start of drag in world coords
                          "original_positions": {}, "is_resizing": False, "resize_handle_corner": None,
                          "original_size_world": {}} # Original W/H in world coords
        self._potential_click_target = None
        self._drag_started_on_item = False
        self._recent_incidents_hidden_globally = False
        self._recent_homeworks_hidden_globally = False # New
        self._per_student_last_cleared = {}

        self.last_used_quiz_name = ""
        self.initial_num_questions = "" # For quiz
        self.last_used_quiz_name_timestamp = None

        # Attributes for remembering the last used homework name and items for manual logging
        self.last_used_homework_name = ""
        self.initial_num_homework_items = "" # For manual log, if needed in future
        self.last_used_homework_name_timestamp = None

        self.is_live_quiz_active = False
        self.current_live_quiz_name = ""
        self.live_quiz_scores = {}

        self.is_live_homework_active = False # New
        self.current_live_homework_name = "" # New
        self.live_homework_scores = {} # New {student_id: {"homework_type_name": "yes/no/selected_option", ...} or {"selected_options": [...]}}

        self.current_zoom_level = 1.0
        self.canvas_orig_width = 2000
        self.canvas_orig_height = 1500
        self.custom_canvas_color = None
        
        self.zoom_level = 1.0
        self.pan_x = 0.0
        self.pan_y = 0.0

        # Ruler and guide attributes
        self.guides = {} # To store {'id': str, 'type': 'v'/'h', 'world_coord': float, 'canvas_item_id': int}
        self.next_guide_id_num = 1
        self.add_guide_mode: Optional[str] = None # 'vertical', 'horizontal', or None
        self.active_guide_button: Optional[ttk.Button] = None # To manage button visual state

        self.ruler_thickness = 35  # pixels
        self.ruler_bg_color = "#f0f0f0"
        self.ruler_line_color = "#555555"
        self.ruler_text_color = "#333333"
        self.active_ruler_guide_coord_x: Optional[float] = None
        self.active_ruler_guide_coord_y: Optional[float] = None
        self.temporary_guides: List[Dict[str, Any]] = [] # List of {'type': 'h'/'v', 'world_coord': float, 'canvas_id': int}
        
        
        self.load_custom_behaviors()
        self.load_custom_homework_types() # NEW
        self.load_custom_homework_statuses() # RENAMED
        self.load_student_groups()
        self.load_quiz_templates()
        self.load_homework_templates()
        
        self.update_all_behaviors()
        self.update_all_homework_types() # NEW
        self.update_all_homework_statuses() # RENAMED
        self.update_all_homework_session_types() # This now depends on the others

        self.load_data() # Loads main data, including settings
        self._ensure_next_ids()
        self.theme_auto(init=True)

        self.guide_line_color = self.settings.get("guides_color", "blue")
        self.setup_ui()
        # self.root.after_idle(self.draw_all_items) # Defer initial draw until window is mapped
        self.update_status(f"Application started. Data loaded from: {os.path.dirname(DATA_FILE)}") # type: ignore
        self.update_undo_redo_buttons_state()
        self.toggle_mode(initial=True) # Apply initial mode
        self.root.after(30000, self.periodic_checks)
        self.root.after(self.settings.get("autosave_interval_ms", 30000), self.autosave_data_wrapper)
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit_protocol)
        
        if self.password_manager.is_password_set() and self.settings.get("password_on_open", False):
            self.root.withdraw()
            if not self.prompt_for_password("Application Locked", "Enter password to open:"):
                self.on_exit_protocol(force_quit=True) # Ensure lock is released if exit fails here
            self.root.deiconify()

    def on_canvas_configure(self, event):
        """
        Called when the canvas is first configured or resized.
        We use this to trigger the very first draw_all_items() call,
        ensuring the canvas has its final size.
        """
        self.draw_all_items()
        

    def capture_tkinter_window(self, filename="tkinter_screenshot.png"):
        """
        Captures the content of a specific Tkinter window by its handle.
        This method is now deprecated in favor of export_layout_as_image for full canvas capture.
        """
        root_window = self.root
        hwnd = root_window.winfo_id() # Get the window handle (HWND) of the Tkinter root

        # Get the window dimensions
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bot - top

        # Create a device context (DC) for the window
        hdc = win32gui.GetWindowDC(hwnd)
        dc_obj = win32ui.CreateDCFromHandle(hdc)
        mem_dc = dc_obj.CreateCompatibleDC()

        # Create a bitmap object
        bitmap = win32ui.CreateBitmap()
        bitmap.CreateCompatibleBitmap(dc_obj, width, height)
        mem_dc.SelectObject(bitmap)

        # Copy the window content to the bitmap
        # Note: PrintWindow is generally better as it can capture minimized/obscured windows,
        # but GetWindowDC + BitBlt works well for visible windows.
        # For PrintWindow, you might need to find the exact flags.
        mem_dc.BitBlt((0, 0), (width, height), dc_obj, (0, 0), win32con.SRCCOPY)

        # Get the bitmap bits and create a PIL Image
        bmpinfo = bitmap.GetInfo()
        bmpstr = bitmap.GetBitmapBits(True)
        img = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        # Clean up the DCs
        dc_obj.DeleteDC()
        mem_dc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hdc)

        #print(os.listdir(os.path.dirname(get_app_data_path(filename))))
        default_filename = f"app_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        file_path = filedialog.asksaveasfilename(defaultextension=".png", initialfile=default_filename + ".png",
                                                       filetypes=[("Image files", "*.png"), ("All Files", "*.*")], parent=self.root)
        
        #if filename in os.listdir(os.path.dirname(get_app_data_path(filename))): print(filename, 1); filename = "tkinter_screenshot3.png"; print(filename, 2) 
            
        output_dpi = int(self.settings.get("output_dpi", 600))
        #print(path)
        #img.save(output_image_file, dpi=(output_dpi, output_dpi))
        img.save(file_path, dpi=(output_dpi, output_dpi))
        print(f"Screenshot saved to {filename}")
        self.update_status(f"Screenshot saved to {file_path}")
        if messagebox.askyesno("Export Successful", f"Layout image saved to:\n{file_path}\n\nDo you want to open the file location?", parent=self.root): 
            self.open_specific_export_folder(file_path)



    def _read_and_decrypt_file(self, file_path):
        """Reads a file, attempts to decrypt it, and loads the JSON data."""
        if not os.path.exists(file_path):
            return None
        try:
            with open(file_path, 'rb') as f:
                file_content = f.read()
            
            if not file_content: # File is empty
                return None

            try:
                # Attempt to decrypt first
                decrypted_data_string = decrypt_data(file_content)
            except cryptography.fernet.InvalidToken:
                # If decryption fails, it's likely plaintext (or corrupt)
                # Assume it's a UTF-8 encoded string.
                decrypted_data_string = file_content.decode('utf-8')

            return json.loads(decrypted_data_string)

        except (json.JSONDecodeError, IOError, UnicodeDecodeError) as e:
            print(f"Error loading and decoding file {os.path.basename(file_path)}: {e}")
            return None

    def _encrypt_and_write_file(self, file_path, data_to_write):
        """Encodes data to JSON, encrypts if enabled, and writes to a file."""
        try:
            json_data_string = json.dumps(data_to_write, indent=4)
            
            # Use the app's setting to decide whether to encrypt
            if self.settings.get("encrypt_data_files", True):
                data_to_write_bytes = encrypt_data(json_data_string)
            else:
                data_to_write_bytes = json_data_string.encode('utf-8')

            with open(file_path, 'wb') as f:
                f.write(data_to_write_bytes)

        except IOError as e:
            print(f"Error saving file {os.path.basename(file_path)}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while saving {os.path.basename(file_path)}: {e}")




    def _get_default_settings(self):
        """
        Returns a dictionary containing the default settings for the application.

        This function is crucial for ensuring the application has a consistent starting state
        and for migrating settings from older data file versions.

        Returns:
            dict: A dictionary of default settings.
        """
        return {
            "show_recent_incidents_on_boxes": True,
            "num_recent_incidents_to_show": 2,
            "recent_incident_time_window_hours": 24,
            "show_full_recent_incidents": False,
            "reverse_incident_order": True,
            "selected_recent_behaviors_filter": None, # List of behavior names, or None for all

            "show_recent_homeworks_on_boxes": True, # New
            "num_recent_homeworks_to_show": 2, # New
            "recent_homework_time_window_hours": 24, # New
            "show_full_recent_homeworks": False, # New
            "reverse_homework_order": True, # New
            "selected_recent_homeworks_filter": None, # New

            "autosave_interval_ms": 30000,
            "default_student_box_width": DEFAULT_STUDENT_BOX_WIDTH,
            "default_student_box_height": DEFAULT_STUDENT_BOX_HEIGHT,
            "student_box_fill_color": DEFAULT_BOX_FILL_COLOR,
            "student_box_outline_color": DEFAULT_BOX_OUTLINE_COLOR,
            "student_font_family": DEFAULT_FONT_FAMILY,
            "student_font_size": DEFAULT_FONT_SIZE,
            "student_font_color": DEFAULT_FONT_COLOR,
            "grid_snap_enabled": False,
            "grid_size": DEFAULT_GRID_SIZE,
            "behavior_initial_overrides": {},
            "homework_initial_overrides": {}, # New for homework display initials
            "current_mode": "behavior", # "behavior", "quiz", or "homework"
            "max_undo_history_days": MAX_UNDO_HISTORY_DAYS,
            "conditional_formatting_rules": [], # Each rule will be a dict. See ConditionalFormattingRuleDialog
            # Example rule:
            # {
            #  "type": "group", "group_id": "group_1", "color": "#FF0000", "outline": "#AA0000",
            #  "enabled": True, "active_times": [], "active_modes": []
            # }
            # {
            #  "type": "behavior_count", "behavior_name": "Talking", "count_threshold": 3, "time_window_hours": 2,
            #  "color": "#FFFF00", "outline": null,
            #  "enabled": True, "active_times": [{"start_time": "09:00", "end_time": "10:30", "days_of_week": [0,1,2,3,4]}],
            #  "active_modes": ["behavior"]
            # }
            "student_groups_enabled": True,
            "show_zoom_level_display": True,
            "available_fonts": sorted(list(tkfont.families())),

            # Quiz specific
            "default_quiz_name": "Pop Quiz",
            "last_used_quiz_name_timeout_minutes": 60, # Timeout for remembering quiz name
            "show_recent_incidents_during_quiz": True,
            "live_quiz_score_font_color": DEFAULT_QUIZ_SCORE_FONT_COLOR,
            "live_quiz_score_font_style_bold": DEFAULT_QUIZ_SCORE_FONT_STYLE_BOLD,
            "quiz_mark_types": DEFAULT_QUIZ_MARK_TYPES.copy(),
            "default_quiz_questions": 10,
            "quiz_score_calculation": "percentage",
            "combine_marks_for_display": True,

            # Homework specific (New)
            "default_homework_name": "Homework Check", # Default name for manual log & live session
            "last_used_homework_name_timeout_minutes": 60, # Timeout for remembering homework name (manual log)
            "behavior_log_font_size": DEFAULT_FONT_SIZE -1, # Specific font size for behavior log text
            "quiz_log_font_size": DEFAULT_FONT_SIZE,       # Specific font size for quiz log text
            "homework_log_font_size": DEFAULT_FONT_SIZE -1, # Specific font size for homework log text
            "live_homework_session_mode": "Yes/No", # "Yes/No" or "Select"
            "log_homework_marks_enabled": True, # Enable/disable detailed marks for manual log
            "homework_mark_types": DEFAULT_HOMEWORK_MARK_TYPES.copy(),
            "default_homework_items_for_yes_no_mode": 5, # For live session "Yes/No"
            "live_homework_score_font_color": DEFAULT_HOMEWORK_SCORE_FONT_COLOR,
            "live_homework_score_font_style_bold": DEFAULT_HOMEWORK_SCORE_FONT_STYLE_BOLD,


            # Password settings
            "app_password_hash": None,
            "password_on_open": False,
            "password_on_edit_action": False,
            "password_auto_lock_enabled": False,
            "password_auto_lock_timeout_minutes": 15,

            # Next ID counters (managed by _ensure_next_ids but good to have defaults)
            "next_student_id_num": 1,
            "next_furniture_id_num": 1,
            "next_group_id_num": 1,
            "next_quiz_template_id_num": 1,
            "next_homework_template_id_num": 1, # New
            "next_custom_homework_type_id_num": 1, # For custom homework types in Yes/No mode

            # Internal state storage (prefixed with underscore)
            "_last_used_quiz_name_for_session": "", # Stores last used quiz name for manual log
            "_last_used_quiz_name_timestamp_for_session": None, # Timestamp for quiz name timeout
            "_last_used_q_num_for_session": 10, # Stores last used num questions for manual quiz log

            "_last_used_homework_name_for_session": "", # Stores last used homework name for manual log
            "_last_used_homework_name_timestamp_for_session": None, # Timestamp for homework name timeout
            "_last_used_hw_items_for_session": 5, # Stores last used num items for manual homework log
            "theme": "System", # Newer
            "enable_text_background_panel": True, # Default for the new setting
            "show_rulers": False, # Default for rulers
            "show_grid": False, # Default for grid visibility
            "grid_color": "#000000", # Default light gray for grid lines
            "save_guides_to_file": True, # New setting for guides
            "guides_stay_when_rulers_hidden": True, # New setting for guides
            "next_guide_id_num": 1, # Added in migration, also good here
            "guides_color": "blue", # Default color for guides
        }

   
    def _ensure_next_ids(self):
        """
        Ensures that the next ID counters for all item types (students, furniture, etc.) are
        correct and up-to-date.

        This function scans the existing data to find the highest current ID for each type
        and sets the "next_id" counter to one greater than the maximum found. This prevents
        ID collisions when new items are created. It's called after data is loaded.
        """
        # Student IDs
        max_s_id = 0
        for sid in self.students:
            if sid.startswith("student_"):
                try: max_s_id = max(max_s_id, int(sid.split("_")[1]))
                except (ValueError, IndexError): pass
        self.next_student_id_num = max(self.settings.get("next_student_id_num", 1), max_s_id + 1)
        self.settings["next_student_id_num"] = self.next_student_id_num

        # Furniture IDs
        max_f_id = 0
        for fid in self.furniture:
            if fid.startswith("furniture_"):
                try: max_f_id = max(max_f_id, int(fid.split("_")[1]))
                except (ValueError, IndexError): pass
        self.next_furniture_id_num = max(self.settings.get("next_furniture_id_num", 1), max_f_id + 1)
        self.settings["next_furniture_id_num"] = self.next_furniture_id_num

        # Group IDs
        max_g_id = 0
        for gid in self.student_groups:
            if gid.startswith("group_"):
                try: max_g_id = max(max_g_id, int(gid.split("_")[1]))
                except (ValueError, IndexError): pass
        self.next_group_id_num = max(self.settings.get("next_group_id_num", 1), max_g_id + 1)
        self.settings["next_group_id_num"] = self.next_group_id_num

        # Quiz Template IDs
        max_qt_id = 0
        for qtid in self.quiz_templates:
            if qtid.startswith("quiztemplate_"):
                try: max_qt_id = max(max_qt_id, int(qtid.split("_")[1]))
                except (ValueError, IndexError): pass
        self.next_quiz_template_id_num = max(self.settings.get("next_quiz_template_id_num", 1), max_qt_id + 1)
        self.settings["next_quiz_template_id_num"] = self.next_quiz_template_id_num

        # Homework Template IDs (New)
        max_ht_id = 0
        for htid in self.homework_templates:
            if htid.startswith("hwtemplate_"):
                try: max_ht_id = max(max_ht_id, int(htid.split("_")[1]))
                except (ValueError, IndexError): pass
        self.next_homework_template_id_num = max(self.settings.get("next_homework_template_id_num", 1), max_ht_id + 1)
        self.settings["next_homework_template_id_num"] = self.next_homework_template_id_num

        # Custom Homework Type IDs (MODIFIED)
        max_chwt_id = 0
        # Use the new custom_homework_types attribute here
        for chwt in self.custom_homework_types:
            if isinstance(chwt, dict) and chwt.get('id', '').startswith("hwtype_"):
                try: max_chwt_id = max(max_chwt_id, int(chwt['id'].split("_")[1]))
                except (ValueError, IndexError): pass
        self.settings["next_custom_homework_type_id_num"] = max(self.settings.get("next_custom_homework_type_id_num", 1), max_chwt_id + 1)

        # Guide IDs
        max_g_id_num = 0
        # Ensure self.guides exists and is iterable; it might not be populated if loading very old data before migration
        if hasattr(self, 'guides') and isinstance(self.guides, dict):
            for guide_info in self.guides:
                guide_id_str = self.guides[guide_info].get('id', '') #guide_info.get('id', '')
                if guide_id_str.startswith("guide_v_") or guide_id_str.startswith("guide_h_"):
                    try: max_g_id_num = max(max_g_id_num, int(guide_id_str.split("_")[-1]))
                    except (ValueError, IndexError, TypeError): pass

        # self.next_guide_id_num is now a direct attribute, not in settings dictionary initially
        # It will be loaded from the main data file if present, otherwise defaults to 1.
        # This ensures it's correctly set after loading data that might contain guides.
        self.next_guide_id_num = max(getattr(self, 'next_guide_id_num', 1), max_g_id_num + 1)


    def periodic_checks(self):
        """
        Performs periodic checks, currently focused on the password auto-lock feature.

        This method is scheduled to run at regular intervals using `root.after()`.
        """
        self.password_manager.check_auto_lock()
        if self.password_manager.is_locked and not hasattr(self, '_lock_screen_active'):
            self.show_lock_screen()
        self.root.after(30000, self.periodic_checks)

    def show_lock_screen(self):
        """
        Displays a modal dialog that covers the application, requiring a password to unlock.

        This is triggered by the auto-lock feature or manual locking.
        """
        if hasattr(self, '_lock_screen_active') and self._lock_screen_active.winfo_exists(): return
        self._lock_screen_active = tk.Toplevel(self.root)
        self._lock_screen_active.title("Application Locked")
        self._lock_screen_active.transient(self.root)
        self._lock_screen_active.grab_set()
        self._lock_screen_active.protocol("WM_DELETE_WINDOW", lambda: None)
        self.root.update_idletasks()
        px, py, pw, ph = self.root.winfo_x(), self.root.winfo_y(), self.root.winfo_width(), self.root.winfo_height()
        dw, dh = 300, 150
        x, y = px + (pw // 2) - (dw // 2), py + (ph // 2) - (dh // 2)
        self._lock_screen_active.geometry(f"{dw}x{dh}+{x}+{y}")
        self._lock_screen_active.resizable(False, False)
        ttk.Label(self._lock_screen_active, text="Application is locked. Enter password:", font=("", 12)).pack(pady=10)
        password_var = tk.StringVar()
        password_entry = ttk.Entry(self._lock_screen_active, textvariable=password_var, show="*", width=30)
        password_entry.pack(pady=5); password_entry.focus_set()
        status_label_lock = ttk.Label(self._lock_screen_active, text="", foreground="red"); status_label_lock.pack(pady=2)
        def attempt_unlock():
            if self.password_manager.unlock_application(password_var.get()):
                self._lock_screen_active.destroy(); del self._lock_screen_active
                self.update_status("Application unlocked.")
            else:
                status_label_lock.config(text="Incorrect password."); password_entry.select_range(0, tk.END)
        ttk.Button(self._lock_screen_active, text="Unlock", command=attempt_unlock).pack(pady=10)
        self._lock_screen_active.bind('<Return>', lambda e: attempt_unlock())

    def prompt_for_password(self, title, prompt_message, for_editing=False):
        """
        Prompts the user for a password before performing a sensitive action.

        This function encapsulates the logic for when a password prompt is necessary,
        based on application settings.

        Args:
            title (str): The title for the password prompt dialog.
            prompt_message (str): The message to display to the user.
            for_editing (bool): If True, respects the "password_on_edit_action" setting.

        Returns:
            bool: True if the action is allowed (password correct or not required), False otherwise.
        """
        if self.password_manager.is_locked:
             if not hasattr(self, '_lock_screen_active') or not self._lock_screen_active.winfo_exists(): self.show_lock_screen()
             return not self.password_manager.is_locked
        if for_editing and not self.settings.get("password_on_edit_action", False) and not self.password_manager.is_password_set(): return True
        if not self.password_manager.is_password_set(): return True
        dialog = PasswordPromptDialog(self.root, title, prompt_message, self.password_manager)
        return dialog.result

    def execute_command(self, command: Command):
        """
        Executes a command object, adding it to the undo stack.

        This is the central method for making any change to the application's state
        that should be undoable. It also handles password checks for sensitive edits.

        Args:
            command (Command): The command object to execute.
        """
        is_sensitive_edit = isinstance(command, (AddItemCommand, DeleteItemCommand, EditItemCommand, ChangeItemsSizeCommand, ManageStudentGroupCommand))
        if is_sensitive_edit and self.settings.get("password_on_edit_action", False) and self.password_manager.is_password_set():
            if not self.prompt_for_password("Confirm Action", "Enter password to make this change:", for_editing=True):
                self.update_status("Action cancelled: Password not provided or incorrect."); return
        try:
            command.execute()
            self.undo_stack.append(command)
            self.redo_stack.clear()
            self.update_undo_redo_buttons_state()
            if not isinstance(command, (MarkLiveQuizQuestionCommand, MarkLiveHomeworkCommand)):
                self.save_data_wrapper(source="command_execution")
            self.password_manager.record_activity()
        except Exception as e:
            messagebox.showerror("Command Error", f"Error executing command: {e}\nCommand Type: {type(command).__name__}", parent=self.root)
            print(f"Command execution error: {e}\n{type(command)}")

    def undo_last_action(self):
        """
        Undoes the most recent command from the undo stack.
        """
        if self.password_manager.is_locked:
            if not self.prompt_for_password("Unlock Required", "Enter password to undo action:"): return # type: ignore
        if self.undo_stack:
            command = self.undo_stack.pop()
            try:
                command.undo()
                self.redo_stack.append(command)
                self.update_undo_redo_buttons_state()
                if not isinstance(command, (MarkLiveQuizQuestionCommand, MarkLiveHomeworkCommand)):
                    self.save_data_wrapper(source="undo_command")
                self.password_manager.record_activity()
            except Exception as e:
                messagebox.showerror("Undo Error", f"Error undoing action: {e}", parent=self.root)
                self.undo_stack.append(command); print(f"Undo error: {e}\n{type(command)}")

    def redo_last_action(self):
        """
        Redoes the most recently undone command from the redo stack.
        """
        if self.password_manager.is_locked:
            if not self.prompt_for_password("Unlock Required", "Enter password to redo action:"): return
        if self.redo_stack:
            command = self.redo_stack.pop()
            try:
                command.execute()
                self.undo_stack.append(command)
                self.update_undo_redo_buttons_state()
                if not isinstance(command, (MarkLiveQuizQuestionCommand, MarkLiveHomeworkCommand)):
                    self.save_data_wrapper(source="redo_command")
                self.password_manager.record_activity()
            except Exception as e:
                messagebox.showerror("Redo Error", f"Error redoing action: {e}", parent=self.root)
                self.redo_stack.append(command); print(f"Redo error: {e}\n{type(command)}")

    def update_undo_redo_buttons_state(self):
        """
        Updates the enabled/disabled state of the Undo and Redo buttons based on
        whether their respective stacks are empty.
        """
        if hasattr(self, 'undo_btn'): self.undo_btn.config(state=tk.NORMAL if self.undo_stack else tk.DISABLED)
        if hasattr(self, 'redo_btn'): self.redo_btn.config(state=tk.NORMAL if self.redo_stack else tk.DISABLED)

    def get_new_student_id(self):
        """Generates a new, unique ID for a student."""
        current_id_to_assign = self.next_student_id_num
        return f"student_{current_id_to_assign}", self.next_student_id_num + 1
    def get_new_furniture_id(self):
        """Generates a new, unique ID for a piece of furniture."""
        current_id_to_assign = self.next_furniture_id_num
        return f"furniture_{current_id_to_assign}", self.next_furniture_id_num + 1
    def get_new_group_id(self):
        """Generates a new, unique ID for a student group."""
        current_id_to_assign = self.next_group_id_num
        return f"group_{current_id_to_assign}", self.next_group_id_num + 1
    def get_new_quiz_template_id(self):
        """Generates a new, unique ID for a quiz template."""
        current_id_to_assign = self.next_quiz_template_id_num
        return f"quiztemplate_{current_id_to_assign}", self.next_quiz_template_id_num + 1
    def get_new_homework_template_id(self): # New
        """Generates a new, unique ID for a homework template."""
        current_id_to_assign = self.next_homework_template_id_num
        return f"hwtemplate_{current_id_to_assign}", self.next_homework_template_id_num + 1
    def get_new_custom_homework_type_id(self): # New
        """Generates a new, unique ID for a custom homework type."""
        current_id_to_assign = self.settings.get("next_custom_homework_type_id_num", 1)
        return f"hwtype_{current_id_to_assign}", current_id_to_assign + 1


    def update_status(self, message):
        """
        Updates the text in the application's status bar.

        Args:
            message (str): The message to display.
        """
        if self.status_bar_label: self.status_bar_label.configure(text=message)

    def setup_ui(self):
        """
        Sets up the entire user interface of the application, including menus, toolbars,
        the main canvas, and event bindings.
        """
        self.main_frame = ttk.Frame(self.root, padding="5"); self.main_frame.pack(fill=tk.BOTH, expand=True)
        top_controls_frame_row1 = ttk.Frame(self.main_frame); top_controls_frame_row1.pack(side=tk.TOP, fill=tk.X, pady=(0, 2))
        self.undo_btn = ttk.Button(top_controls_frame_row1, text="Undo", command=self.undo_last_action, state=tk.DISABLED); self.undo_btn.pack(side=tk.LEFT, padx=2)
        self.redo_btn = ttk.Button(top_controls_frame_row1, text="Redo", command=self.redo_last_action, state=tk.DISABLED); self.redo_btn.pack(side=tk.LEFT, padx=2)

        self.file_menu_btn = ttk.Menubutton(top_controls_frame_row1, text="File"); self.file_menu = tk.Menu(self.file_menu_btn, tearoff=0)
        self.file_menu.add_command(label="Save Now", command=self.save_data_wrapper, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Import Students from Excel...", command=self.import_students_from_excel_dialog)
        self.file_menu.add_separator(); self.file_menu.add_command(label="Open Data Folder", command=self.open_data_folder)
        self.open_export_folder_menu_entry_index = self.file_menu.index(tk.END)
        self.file_menu.add_command(label="Open Last Export Folder (None)", command=self.open_last_export_folder, state=tk.DISABLED)
        self.open_export_folder_menu_entry_index = self.file_menu.index(tk.END)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Backup All Application Data (.zip)...", command=self.backup_all_data_dialog)
        self.file_menu.add_command(label="Restore All Application Data...", command=self.restore_all_data_dialog)
        self.file_menu.add_separator(); self.file_menu.add_command(label="Reset Application (Caution!)...", command=self.reset_application_dialog)
        self.file_menu.add_separator(); self.file_menu.add_command(label="Exit", command=self.on_exit_protocol, accelerator="Ctrl+Q")
        self.file_menu_btn["menu"] = self.file_menu; self.file_menu_btn.pack(side=tk.LEFT, padx=2)
        self.update_open_last_export_folder_menu_item()
        self.root.bind_all("<Control-s>", lambda event: self.save_data_wrapper())
        self.root.bind_all("<Control-q>", lambda event: self.save_and_quit_app())
        self.root.bind_all("<Control-Q>", lambda event: self.save_and_quit_app())
        self.root.bind_all("<Control-z>", lambda event: self.undo_last_action())
        self.root.bind_all("<Control-y>", lambda event: self.redo_last_action())
        self.root.bind_all("<Control-Shift-Z>", lambda event: self.redo_last_action()) # Common alternative for redo
        self.root.bind_all("<Control-r>", lambda event: self.reload_canvas())
        self.root.bind_all("<Control-R>", lambda event: self.reload_canvas())
        self.root.bind_all("<S>", lambda event: self.open_settings_dialog())
        self.root.bind_all("<p>", lambda event: self.show_help_dialog())
        self.root.bind_all("<Control-plus>", lambda event: self.zoom_canvas(1.1))
        self.root.bind_all("<Control-equal>", lambda event: self.zoom_canvas(1.1))
        self.root.bind_all("<Control-minus>", lambda event: self.zoom_canvas(0.9))
        self.root.bind_all("<Control-0>", lambda event: self.zoom_canvas(0))
        self.root.bind_all("<E>", lambda event: self.toggle_edit_mode_shortcut())
        self.root.bind_all("<B>", lambda event: self.toggle_mode_("behavior"))
        self.root.bind_all("<Q>", lambda event: self.toggle_mode_("quiz"))
        self.root.bind_all("<H>", lambda event: self.toggle_mode_("homework"))
        
        # Edit Menu (for Undo History)
        # self.edit_menu_btn = ttk.Menubutton(top_controls_frame_row1, text="Edit")
        # self.edit_menu = tk.Menu(self.edit_menu_btn, tearoff=0)
        # self.edit_menu.add_command(label="Undo", command=self.undo_last_action, accelerator="Ctrl+Z")
        # self.edit_menu.add_command(label="Redo", command=self.redo_last_action, accelerator="Ctrl+Y")
        # self.edit_menu.add_separator()
        # self.edit_menu.add_command(label="Show Undo History...", command=self.show_undo_history_dialog)
        # self.edit_menu_btn["menu"] = self.edit_menu
        # self.edit_menu_btn.pack(side=tk.LEFT, padx=2)

        self.export_menu_btn = ttk.Menubutton(top_controls_frame_row1, text="Export Log"); self.export_menu = tk.Menu(self.export_menu_btn, tearoff=0)
        self.export_menu.add_command(label="To Excel (.xlsx)", command=lambda: self.export_log_dialog_with_filter(export_type="xlsx"))
        self.export_menu.add_command(label="To Excel Macro-Enabled (.xlsm)", command=lambda: self.export_log_dialog_with_filter(export_type="xlsm"))
        self.export_menu.add_command(label="To CSV Files (.zip)", command=lambda: self.export_log_dialog_with_filter(export_type="csv"))
        self.export_menu.add_separator()
        self.export_menu.add_command(label="Export Layout as Image (see Help)...", command=self.export_layout_as_image) #self.export_layout_as_image)
        self.export_menu.add_command(label="Generate Attendance Report...", command=self.generate_attendance_report_dialog)
        self.export_menu_btn["menu"] = self.export_menu; self.export_menu_btn.pack(side=tk.LEFT, padx=2)
        ttk.Button(top_controls_frame_row1, text="Settings", underline=0, command=self.open_settings_dialog).pack(side=tk.LEFT, padx=2)
        
        self.mode_frame = ttk.LabelFrame(top_controls_frame_row1, text="Mode", padding=2); self.mode_frame.pack(side=tk.LEFT, padx=3); self.mode_frame.pack_propagate(True)
        ttk.Radiobutton(self.mode_frame, text="Behavior", underline=0, variable=self.mode_var, value="behavior", command=self.toggle_mode).pack(side=tk.LEFT)
        ttk.Radiobutton(self.mode_frame, text="Quiz", underline=0, variable=self.mode_var, value="quiz", command=self.toggle_mode).pack(side=tk.LEFT)
        ttk.Radiobutton(self.mode_frame, text="Homework", underline=0, variable=self.mode_var, value="homework", command=self.toggle_mode).pack(side=tk.LEFT) # New Homework mode

        self.live_quiz_button_frame = ttk.LabelFrame(top_controls_frame_row1, text="Class Quiz")
        self.start_live_quiz_btn = ttk.Button(self.live_quiz_button_frame, text="Start Session", command=self.start_live_quiz_session_dialog); self.start_live_quiz_btn.pack(side=tk.LEFT, padx=3, pady=3)
        self.end_live_quiz_btn = ttk.Button(self.live_quiz_button_frame, text="End Session", command=self.end_live_quiz_session, state=tk.DISABLED); self.end_live_quiz_btn.pack(side=tk.LEFT, padx=3, pady=3)

        self.live_homework_button_frame = ttk.LabelFrame(top_controls_frame_row1, text="Homework Session") # New
        self.start_live_homework_btn = ttk.Button(self.live_homework_button_frame, text="Start Session", command=self.start_live_homework_session_dialog); self.start_live_homework_btn.pack(side=tk.LEFT, padx=3, pady=3)
        self.end_live_homework_btn = ttk.Button(self.live_homework_button_frame, text="End Session", command=self.end_live_homework_session, state=tk.DISABLED); self.end_live_homework_btn.pack(side=tk.LEFT, padx=3, pady=3)

        

        self.top_controls_frame_row2 = ttk.Frame(self.main_frame); self.top_controls_frame_row2.pack(side=tk.TOP, fill=tk.X, pady=(2, 5))
        
        self.zoom_var = tk.StringVar(value=str(float(self.current_zoom_level)*100))
        view_controls_frame = ttk.LabelFrame(top_controls_frame_row1, text="View & Edit", padding=2); view_controls_frame.pack(side=tk.LEFT, padx=5)
        ttk.Button(view_controls_frame, text="In", command=lambda: self.zoom_canvas(1.1)).pack(side=tk.LEFT, padx=2)
        self.zoom_display_label = ttk.Entry(view_controls_frame, textvariable=self.zoom_var, width=5)
        if self.settings.get("show_zoom_level_display", True): self.zoom_display_label.pack(side=tk.LEFT, padx=1)
        ttk.Button(view_controls_frame, text="Out", command=lambda: self.zoom_canvas(0.9)).pack(side=tk.LEFT, padx=2)
        ttk.Button(view_controls_frame, text="Reset", command=lambda: self.zoom_canvas(0)).pack(side=tk.LEFT, padx=2)
        self.edit_mode_checkbutton = ttk.Checkbutton(view_controls_frame, text="Edit Mode", underline=0, variable=self.edit_mode_var, command=self.toggle_edit_mode); self.edit_mode_checkbutton.pack(side=tk.LEFT, padx=5)
        self.toggle_incidents_btn = ttk.Button(view_controls_frame, text="Hide Recent Logs", command=self.toggle_global_recent_logs_visibility); self.toggle_incidents_btn.pack(side=tk.LEFT, padx=2) # Renamed
        self.update_toggle_incidents_button_text()

        self.toggle_rulers_btn = ttk.Button(view_controls_frame, text="Toggle Rulers", command=self.toggle_rulers_visibility)
        self.toggle_rulers_btn.pack(side=tk.LEFT, padx=2)

        self.toggle_grid_btn = ttk.Button(view_controls_frame, text="Toggle Grid", command=self.toggle_grid_visibility)
        self.toggle_grid_btn.pack(side=tk.LEFT, padx=2)

        # Add Guide Buttons
        self.add_v_guide_btn = ttk.Button(view_controls_frame, text="Add V Guide", command=lambda: self.toggle_add_guide_mode("vertical", self.add_v_guide_btn))
        self.add_v_guide_btn.pack(side=tk.LEFT, padx=2)
        self.add_h_guide_btn = ttk.Button(view_controls_frame, text="Add H Guide", command=lambda: self.toggle_add_guide_mode("horizontal", self.add_h_guide_btn))
        self.add_h_guide_btn.pack(side=tk.LEFT, padx=2)

        

        self.manage_boxes_frame = ttk.Frame(self.top_controls_frame_row2); self.manage_boxes_frame.pack(side=tk.LEFT, padx=2)
        layout_tools_frame = ttk.LabelFrame(self.manage_boxes_frame, text="Layout Tools", padding=2); layout_tools_frame.pack(side=tk.LEFT, padx=2)
        ttk.Button(layout_tools_frame, text="Align Top", command=lambda: self.align_selected_items("top")).pack(side=tk.LEFT,pady=1, padx=1)
        ttk.Button(layout_tools_frame, text="Align Bottom", command=lambda: self.align_selected_items("bottom")).pack(side=tk.LEFT,pady=1, padx=1)
        ttk.Button(layout_tools_frame, text="Align Left", command=lambda: self.align_selected_items("left")).pack(side=tk.LEFT,pady=1, padx=1)
        ttk.Button(layout_tools_frame, text="Align Right", command=lambda: self.align_selected_items("right")).pack(side=tk.LEFT,pady=1, padx=1)
        ttk.Button(layout_tools_frame, text="Distribute H", command=lambda: self.distribute_selected_items_evenly("horizontal")).pack(side=tk.LEFT, pady=1, padx=1)
        ttk.Button(layout_tools_frame, text="Distribute V", command=lambda: self.distribute_selected_items_evenly("vertical")).pack(side=tk.LEFT, pady=1, padx=1)

        templates_groups_frame = ttk.LabelFrame(self.manage_boxes_frame, text="Layout & Groups", padding=2); 
        templates_groups_frame.pack(side=tk.LEFT, padx=2)
        ttk.Button(templates_groups_frame, text="Save Layout...", command=self.save_layout_template_dialog).pack(side=tk.LEFT,pady=1, padx=1)
        ttk.Button(templates_groups_frame, text="Load Layout...", command=self.load_layout_template_dialog).pack(side=tk.LEFT,pady=1, padx=1)
        self.manage_groups_btn = ttk.Button(templates_groups_frame, text="Manage Groups...", command=self.manage_student_groups_dialog); self.manage_groups_btn.pack(side=tk.LEFT,pady=1, padx=1)        
        
        # Toggle Dragging Button
        self.toggle_dragging_btn = ttk.Button(self.manage_boxes_frame, text="Disable Dragging", command=self.toggle_dragging_allowed)
        self.toggle_dragging_btn.pack(side=tk.LEFT, padx=(2))
        self._update_toggle_dragging_button_text() # Initialize button text
        
        ttk.Button(self.manage_boxes_frame, text="Show undo history", command=self.show_undo_history_dialog).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(self.manage_boxes_frame, text="Add Student", command=self.add_student_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.manage_boxes_frame, text="Add Furniture", command=self.add_furniture_dialog).pack(side=tk.LEFT, padx=2)

        self.lock_app_btn = ttk.Button(top_controls_frame_row1, text="Lock", command=self.lock_application_ui_triggered); self.lock_app_btn.pack(side=tk.RIGHT, padx=5)
        self.update_lock_button_state()
        self.root.bind_all("<Control-l>", lambda e: self.lock_application_ui_triggered())
        ttk.Button(top_controls_frame_row1, text="Help", underline=3, command=self.show_help_dialog).pack(side=tk.RIGHT, padx=2)
        
        self.zoom_display_label.bind("<FocusOut>", lambda e: self.update_zoom_display2())
        self.zoom_display_label.bind("<Return>", lambda e: self.update_zoom_display2())
        
        

        self.theme_auto(init=True)
            
        self.canvas_frame = ttk.Frame(self.main_frame); self.canvas_frame.pack(fill=tk.BOTH, after=self.top_controls_frame_row2, expand=True)
        self.h_scrollbar = ttk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas_xview_custom)
        self.v_scrollbar = ttk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas_yview_custom) #else "#1F1F1F"
        self.canvas = tk.Canvas(self.canvas_frame, bg=self.canvas_color, relief=tk.SUNKEN, borderwidth=1, xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set) # type: ignore
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X); self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y); self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.config(scrollregion=(0, 0, self.canvas_orig_width * self.current_zoom_level, self.canvas_orig_height * self.current_zoom_level))
        self.canvas.bind("<ButtonPress-1>", self.on_canvas_left_press); self.canvas.bind("<ButtonPress-3>", self.on_canvas_right_press)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag); self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.canvas.bind("<Control-Button-1>", self.on_canvas_ctrl_click); self.canvas.bind("<KeyPress-Delete>", self.on_delete_key_press); self.canvas.bind("<BackSpace>", self.on_delete_key_press)
        self.canvas.bind("<Control-MouseWheel>", self.on_mousewheel_zoom); self.canvas.bind("<Control-Button-4>", self.on_mousewheel_zoom); self.canvas.bind("<Control-Button-5>", self.on_mousewheel_zoom)
        self.canvas.bind("<ButtonPress-2>", self.on_pan_start); self.canvas.bind("<B2-Motion>", self.on_pan_move); self.canvas.bind("<ButtonRelease-2>", self.on_pan_end)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel_scroll); self.canvas.bind("<Button-4>", self.on_mousewheel_scroll); self.canvas.bind("<Button-5>", self.on_mousewheel_scroll)
        if sys.platform == "darwin": self.canvas.bind("<Shift-MouseWheel>", self.on_mousewheel_scroll_horizontal_mac)
        else: self.canvas.bind("<Shift-MouseWheel>", self.on_mouse_wheel_horizontal) # For Windows/Linux with Shift

        self.status_bar_label = ttk.Label(self.root, text="Welcome!", relief=tk.SUNKEN, anchor=tk.W, padding=5); self.status_bar_label.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.focus_set()
        self.toggle_student_groups_ui_visibility()
        self.toggle_manage_boxes_visibility()

    def canvas_xview_custom(self, *args):
        """Custom wrapper for the canvas's xview method to record user activity."""
        self.canvas.xview(*args); self.password_manager.record_activity()
    def canvas_yview_custom(self, *args):
        """Custom wrapper for the canvas's yview method to record user activity."""
        self.canvas.yview(*args); self.password_manager.record_activity()
    def on_mousewheel_scroll(self, event):
        """Handles vertical scrolling with the mouse wheel on the canvas."""
        if self.password_manager.is_locked: return
        self.password_manager.record_activity()
        if event.num == 5 or event.delta < 0: self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0: self.canvas.yview_scroll(-1, "units")
    def on_mouse_wheel_horizontal(self, event): # For Shift+Wheel on Windows/Linux
        """Handles horizontal scrolling with Shift + Mouse Wheel on Windows and Linux."""
        if self.password_manager.is_locked: return
        self.password_manager.record_activity()
        if event.delta < 0: self.canvas.xview_scroll(1, "units") # Scroll right
        elif event.delta > 0: self.canvas.xview_scroll(-1, "units") # Scroll left
    def on_mousewheel_scroll_horizontal_mac(self, event):
        """Handles horizontal scrolling with the mouse wheel on macOS."""
        if self.password_manager.is_locked: return
        self.password_manager.record_activity()
        if event.delta < 0: self.canvas.xview_scroll(1, "units")
        elif event.delta > 0: self.canvas.xview_scroll(-1, "units")

    def lock_application_ui_triggered(self):
        """
        Locks the application when triggered by the UI (e.g., Lock button).

        Prompts for password setup if one is not already set.
        """
        if self.password_manager.is_password_set():
            if self.password_manager.lock_application():
                self.update_status("Application locked."); self.show_lock_screen(); self.update_lock_button_state()
            else: self.update_status("Failed to lock: No password set or already locked.")
        else:
            messagebox.showinfo("Password Not Set", "Please set an application password in Settings first.", parent=self.root)
            self.open_settings_dialog()
    def update_lock_button_state(self):
        """Updates the state of the 'Lock' button based on whether a password is set."""
        if hasattr(self, 'lock_app_btn'): self.lock_app_btn.config(state=tk.NORMAL if self.password_manager.is_password_set() else tk.DISABLED)
    def save_and_quit_app(self):
        """
        Saves all data and quits the application.

        Handles confirmation prompts for active live sessions before quitting.
        """
        if self.password_manager.is_locked:
            if not self.prompt_for_password("Unlock to Save & Quit", "Enter password to save and quit:"): return
        if self.is_live_quiz_active and not self.prompt_end_live_session_on_mode_switch("quiz"): return
        if self.is_live_homework_active and not self.prompt_end_live_session_on_mode_switch("homework"): return # New
        self.save_data_wrapper(source="save_and_quit")
        self.on_exit_protocol(force_quit=True) # Call main exit to release lock

    def on_delete_key_press(self, event=None):
        """Handles the Delete key press to remove selected items."""
        if self.password_manager.is_locked: return
        if self.selected_items: self.delete_selected_items_confirm()
        self.password_manager.record_activity()
    def update_open_last_export_folder_menu_item(self):
        """
        Updates the 'Open Last Export Folder' menu item with the path of the last export.
        """
        if hasattr(self, 'file_menu') and self.file_menu:
            label_text, state = "Open Last Export Folder (None)", tk.DISABLED
            if self.last_excel_export_path and os.path.exists(os.path.dirname(self.last_excel_export_path)):
                label_text, state = f"Open Last Export Folder ({os.path.basename(os.path.dirname(self.last_excel_export_path))})", tk.NORMAL
            try:
                if self.open_export_folder_menu_entry_index is not None and self.open_export_folder_menu_entry_index <= self.file_menu.index(tk.END):
                    self.file_menu.entryconfigure(self.open_export_folder_menu_entry_index, label=label_text, state=state)
            except tk.TclError as e: print(f"Error updating 'Open Last Export Folder' menu item: {e}.")

    def prompt_end_live_session_on_mode_switch(self, session_type_to_check): # "quiz" or "homework"
        """
        Prompts the user to end an active live session when switching modes or exiting.

        Args:
            session_type_to_check (str): The type of session to check for ("quiz" or "homework").

        Returns:
            bool: True if the mode switch can proceed, False if cancelled.
        """
        is_active_flag = self.is_live_quiz_active if session_type_to_check == "quiz" else self.is_live_homework_active
        current_name = self.current_live_quiz_name if session_type_to_check == "quiz" else self.current_live_homework_name
        end_function = self.end_live_quiz_session if session_type_to_check == "quiz" else self.end_live_homework_session
        start_btn = self.start_live_quiz_btn if session_type_to_check == "quiz" else self.start_live_homework_btn
        end_btn = self.end_live_quiz_btn if session_type_to_check == "quiz" else self.end_live_homework_btn
        scores_dict = self.live_quiz_scores if session_type_to_check == "quiz" else self.live_homework_scores

        if is_active_flag:
            msg = f"A Class {session_type_to_check.capitalize()} session ('{current_name}') is active.\n\nDo you want to end and log this session?"
            response = messagebox.askyesnocancel(f"Class {session_type_to_check.capitalize()} Active", msg, parent=self.root)
            if response is True: end_function(confirm=False); return True
            elif response is False: # Discard
                if session_type_to_check == "quiz": self.is_live_quiz_active = False; self.current_live_quiz_name = ""
                else: self.is_live_homework_active = False; self.current_live_homework_name = ""
                scores_dict.clear()
                start_btn.config(state=tk.NORMAL); end_btn.config(state=tk.DISABLED)
                self.update_status(f"Class {session_type_to_check.capitalize()} session discarded.")
                self.draw_all_items(check_collisions_on_redraw=True); return True
            else: return False # Cancel
        return True # No active session of this type

    def toggle_mode_(self, mode):
        """
        Sets the application mode via a direct call (e.g., from a keyboard shortcut).

        Args:
            mode (str): The mode to switch to ("behavior", "quiz", or "homework").
        """
        self.mode_var.set(mode)
        self.toggle_mode()

    def toggle_mode(self, initial=False):
        """
        Toggles the application's primary mode (Behavior, Quiz, Homework).

        Handles UI changes and prompts for ending live sessions if necessary.

        Args:
            initial (bool): True if this is the initial mode set on startup.
        """
        if self.password_manager.is_locked:
            if not self.prompt_for_password("Unlock to Change Mode", "Enter password to change mode:"):
                self.mode_var.set(self.settings["current_mode"]); return

        new_mode = self.mode_var.get()
        old_mode = self.settings["current_mode"]

        if old_mode == "quiz" and new_mode != "quiz" and self.is_live_quiz_active:
            if not self.prompt_end_live_session_on_mode_switch("quiz"): self.mode_var.set("quiz"); return
        if old_mode == "homework" and new_mode != "homework" and self.is_live_homework_active: # New
            if not self.prompt_end_live_session_on_mode_switch("homework"): self.mode_var.set("homework"); return


        self.settings["current_mode"] = new_mode
        if not initial:
            self.update_status(f"Mode switched to {new_mode.capitalize()}.")

        if hasattr(self, 'live_quiz_button_frame'):
            if new_mode == "quiz":
                self.live_quiz_button_frame.pack(side=tk.LEFT, padx=(0,3), after=self.mode_frame)
                self.start_live_quiz_btn.config(state=tk.DISABLED if self.is_live_quiz_active else tk.NORMAL)
                self.end_live_quiz_btn.config(state=tk.NORMAL if self.is_live_quiz_active else tk.DISABLED)
            else: self.live_quiz_button_frame.pack_forget()

        if hasattr(self, 'live_homework_button_frame'): # New
            if new_mode == "homework":
                self.live_homework_button_frame.pack(side=tk.LEFT, padx=(0,3), after=self.mode_frame)
                self.start_live_homework_btn.config(state=tk.DISABLED if self.is_live_homework_active else tk.NORMAL)
                self.end_live_homework_btn.config(state=tk.NORMAL if self.is_live_homework_active else tk.DISABLED)
            else: self.live_homework_button_frame.pack_forget()

        self.draw_all_items(check_collisions_on_redraw=True)
        self.save_data_wrapper(source="toggle_mode")
        self.password_manager.record_activity()

    def toggle_edit_mode_shortcut(self):
        """Toggles edit mode via a keyboard shortcut."""
        self.edit_mode_var.set(value=True if self.edit_mode_var.get() != True else False)
        self.toggle_edit_mode()
        
    def toggle_edit_mode(self):
        """
        Toggles the edit mode for resizing items.

        When enabled, resize handles appear on selected items.
        """
        if self.password_manager.is_locked:
            if not self.prompt_for_password("Unlock to Toggle Edit Mode", "Enter password to change edit mode:"):
                self.edit_mode_var.set(not self.edit_mode_var.get()); return
        is_edit_mode = self.edit_mode_var.get()
        self.update_status(f"Edit Mode {'Enabled' if is_edit_mode else 'Disabled'}. Click item corners to resize.")
        self.toggle_manage_boxes_visibility()
        self.draw_all_items(check_collisions_on_redraw=True)
        self.password_manager.record_activity()

    def start_live_quiz_session_dialog(self):
        """
        Opens a dialog to start a new live quiz session.
        """
        if self.password_manager.is_locked:
            if not self.prompt_for_password("Unlock to Start Quiz", "Enter password to start quiz session:"): return
        if self.is_live_quiz_active:
            messagebox.showinfo("Class Quiz Active", "A Class Quiz session is already active.", parent=self.root); return
        quiz_name = simpledialog.askstring("Start Class Quiz", "Enter a name for this quiz session:", initialvalue=self.settings.get("default_quiz_name", "Class Quiz"), parent=self.root)
        if quiz_name and quiz_name.strip():
            self.current_live_quiz_name = quiz_name.strip()
            self.is_live_quiz_active = True; self.live_quiz_scores.clear()
            self.start_live_quiz_btn.config(state=tk.DISABLED); self.end_live_quiz_btn.config(state=tk.NORMAL)
            self.update_status(f"Class Quiz '{self.current_live_quiz_name}' started. Click a student to mark.")
            self.draw_all_items(check_collisions_on_redraw=True); self.password_manager.record_activity()
        else: self.update_status("Class Quiz start cancelled.")

    def end_live_quiz_session(self, confirm=True):
        """
        Ends the current live quiz session, logging all collected scores.

        Args:
            confirm (bool): If True, asks the user for confirmation before ending.
        """
        if self.password_manager.is_locked:
            if not self.prompt_for_password("Unlock to End Quiz", "Enter password to end quiz session:"): return
        if not self.is_live_quiz_active: self.update_status("No active Class Quiz session to end."); return
        if confirm and not messagebox.askyesno("End Class Quiz", f"End Class Quiz session: '{self.current_live_quiz_name}'?\nScores will be logged.", parent=self.root): return

        log_commands = []
        for student_id, score_data in self.live_quiz_scores.items():
            if student_id in self.students and score_data["total_asked"] > 0:
                student = self.students[student_id]
                log_entry = {"timestamp": datetime.now().isoformat(), "student_id": student_id,
                             "student_first_name": student["first_name"], "student_last_name": student["last_name"],
                             "behavior": self.current_live_quiz_name, "score_details": score_data.copy(),
                             "comment": "From Class Quiz session.", "type": "quiz", "day": datetime.now().strftime('%A')}
                log_commands.append(LogEntryCommand(self, log_entry, student_id))
        for cmd in log_commands: self.execute_command(cmd)
        if log_commands: self.save_data_wrapper(source="end_live_quiz")
        self.update_status(f"Class Quiz '{self.current_live_quiz_name}' ended. {len(log_commands)} student scores logged.")
        self.is_live_quiz_active = False; self.current_live_quiz_name = ""; self.live_quiz_scores.clear()
        self.start_live_quiz_btn.config(state=tk.NORMAL); self.end_live_quiz_btn.config(state=tk.DISABLED)
        self.draw_all_items(check_collisions_on_redraw=True); self.password_manager.record_activity()

    def handle_live_quiz_tap(self, student_id):
        """
        Handles a click/tap on a student during a live quiz session, opening the marking dialog.

        Args:
            student_id (str): The ID of the student who was clicked.
        """
        if self.password_manager.is_locked:
            if not self.prompt_for_password("Unlock to Mark Quiz", "Enter password to mark quiz:"): return
        if not self.is_live_quiz_active or student_id not in self.students: return
        dialog = LiveQuizMarkDialog(self.root, student_id, self, session_type="Quiz")
        if dialog.result:
            self.execute_command(MarkLiveQuizQuestionCommand(self, student_id, dialog.result))
            self.password_manager.record_activity()

    # --- Live Homework Session Methods (New) ---
    def start_live_homework_session_dialog(self):
        """Opens a dialog to start a new live homework session."""
        if self.password_manager.is_locked:
            if not self.prompt_for_password("Unlock to Start Homework Session", "Enter password to start homework session:"): return
        if self.is_live_homework_active:
            messagebox.showinfo("Homework Session Active", "A Homework session is already active.", parent=self.root); return

        homework_session_name = simpledialog.askstring("Start Homework Session", "Enter a name for this homework session:",
                                                       initialvalue=self.settings.get("default_homework_name", "Homework Check"), parent=self.root)
        if homework_session_name and homework_session_name.strip():
            self.current_live_homework_name = homework_session_name.strip()
            self.is_live_homework_active = True
            self.live_homework_scores.clear() # {student_id: {hw_type_id: "yes"/"no"} or {student_id: {"selected_options": [...]}}}
            self.start_live_homework_btn.config(state=tk.DISABLED)
            self.end_live_homework_btn.config(state=tk.NORMAL)
            self.update_status(f"Homework Session '{self.current_live_homework_name}' started. Click a student to mark.")
            self.draw_all_items(check_collisions_on_redraw=True)
            self.password_manager.record_activity()
        else:
            self.update_status("Homework Session start cancelled.")

    def end_live_homework_session(self, confirm=True):
        """
        Ends the current live homework session, logging all collected data.

        Args:
            confirm (bool): If True, asks the user for confirmation before ending.
        """
        if self.password_manager.is_locked:
            if not self.prompt_for_password("Unlock to End Homework Session", "Enter password to end homework session:"): return
        if not self.is_live_homework_active:
            self.update_status("No active Homework Session to end."); return
        if confirm and not messagebox.askyesno("End Homework Session", f"End Homework Session: '{self.current_live_homework_name}'?\nData will be logged.", parent=self.root):
            return

        log_commands = []
        for student_id, hw_data in self.live_homework_scores.items():
            if student_id in self.students and hw_data: # Ensure there's some data to log
                student = self.students[student_id]
                # Log entry structure depends on session mode
                if self.settings.get('live_homework_session_mode') == "Yes/No":
                    type2 = "y"
                else: type2 = "s"
                log_entry = {
                    "timestamp": datetime.now().isoformat(), "student_id": student_id,
                    "student_first_name": student["first_name"], "student_last_name": student["last_name"],
                    "behavior": self.current_live_homework_name, # Session name
                    "homework_details": hw_data.copy(), # Store the collected data
                    "comment": f"From Live Homework Session ({self.settings.get('live_homework_session_mode', 'Yes/No')} mode).",
                    "type": f"homework_session_{type2}", # Distinguish from manual homework log
                    "day": datetime.now().strftime('%A')
                }
                log_commands.append(LogHomeworkEntryCommand(self, log_entry, student_id)) # Use homework log command

        for cmd in log_commands: self.execute_command(cmd)
        if log_commands: self.save_data_wrapper(source="end_live_homework_session")

        self.update_status(f"Homework Session '{self.current_live_homework_name}' ended. {len(log_commands)} student entries logged.")
        self.is_live_homework_active = False; self.current_live_homework_name = ""; self.live_homework_scores.clear()
        self.start_live_homework_btn.config(state=tk.NORMAL); self.end_live_homework_btn.config(state=tk.DISABLED)
        self.draw_all_items(check_collisions_on_redraw=True); self.password_manager.record_activity()

    def handle_live_homework_tap(self, student_id):
        """
        Handles a click/tap on a student during a live homework session, opening the marking dialog.

        Args:
            student_id (str): The ID of the student who was clicked.
        """
        if self.password_manager.is_locked:
            if not self.prompt_for_password("Unlock to Mark Homework", "Enter password to mark homework:"): return
        if not self.is_live_homework_active or student_id not in self.students: return

        session_mode = self.settings.get("live_homework_session_mode", "Yes/No")
        current_student_hw_data = self.live_homework_scores.get(student_id, {}).copy()

        dialog = LiveHomeworkMarkDialog(self.root, student_id, self,
                                        session_mode=session_mode,
                                        current_hw_data=current_student_hw_data)
        if dialog.result_actions is not None: # Dialog returns actions or None if cancelled
            cmd = MarkLiveHomeworkCommand(self, student_id, dialog.result_actions, session_mode)
            self.execute_command(cmd)
            self.password_manager.record_activity()

    def add_student_dialog(self):
        """Opens the dialog to add a new student."""
        if self.password_manager.is_locked:
            if not self.prompt_for_password("Unlock to Add Student", "Enter password to add student:"): return
        dialog = AddEditStudentDialog(self.root, "Add Student", app=self)
        if dialog.result:
            first_name, last_name, nickname, gender, group_id_selection = dialog.result
            if first_name and last_name:
                old_next_student_id_num_for_command = self.next_student_id_num
                student_id_str, next_id_val_for_app_state_after_this = self.get_new_student_id()
                full_name = f"{first_name} \"{nickname}\" {last_name}" if nickname else f"{first_name} {last_name}"
                x, y = self.canvas_to_world_coords(50 + (len(self.students) % 10) * 20, 50 + ((len(self.students) // 10) * 20))
                student_data = {"first_name": first_name, "last_name": last_name, "nickname": nickname, "full_name": full_name, "gender": gender,
                                "x": x, "y": y, "id": student_id_str, "width": self.settings.get("default_student_box_width"),
                                "height": self.settings.get("default_student_box_height"), "original_next_id_num_after_add": next_id_val_for_app_state_after_this,
                                "group_id": group_id_selection if group_id_selection else None, "style_overrides": {}}
                self.execute_command(AddItemCommand(self, student_id_str, 'student', student_data, old_next_student_id_num_for_command))
                self.password_manager.record_activity()
            else: messagebox.showwarning("Invalid Name", "First and Last names cannot be empty.", parent=self.root)

    def add_furniture_dialog(self):
        """Opens the dialog to add a new piece of furniture."""
        if self.password_manager.is_locked:
            if not self.prompt_for_password("Unlock to Add Furniture", "Enter password to add furniture:"): return
        dialog = AddFurnitureDialog(self.root, "Add Furniture Item")
        if dialog.result:
            name, item_type, width, height = dialog.result
            if name and item_type:
                old_next_furniture_id_num_for_command = self.next_furniture_id_num
                furniture_id_str, next_id_val_for_app_state_after_this = self.get_new_furniture_id()
                x, y = self.canvas_to_world_coords(70 + (len(self.furniture) % 10) * 20, 70 + ((len(self.furniture) // 10) * 20))
                furniture_data = {"name": name, "type": item_type, "x": x, "y": y, "id": furniture_id_str, "width": width, "height": height,
                                  "fill_color": "lightgray", "outline_color": "dimgray", "original_next_id_num_after_add": next_id_val_for_app_state_after_this}
                self.execute_command(AddItemCommand(self, furniture_id_str, 'furniture', furniture_data, old_next_furniture_id_num_for_command))
                self.password_manager.record_activity()

    def toggle_global_recent_logs_visibility(self): # Renamed for clarity
        """
        Toggles the global visibility of recent log entries (both behavior and homework)
        on all student boxes.
        """
        if self.password_manager.is_locked:
            if not self.prompt_for_password("Unlock to Change Setting", "Enter password to change log visibility:"): return
        # This now toggles both behavior and homework visibility together for simplicity,
        # or could be split into two separate global toggles if needed.
        self._recent_incidents_hidden_globally = not self._recent_incidents_hidden_globally
        self._recent_homeworks_hidden_globally = self._recent_incidents_hidden_globally # Link them for now
        self.draw_all_items(check_collisions_on_redraw=True)
        self.update_toggle_incidents_button_text() # Button text reflects combined state
        status_msg = "Recent behavior/homework logs hidden globally." if self._recent_incidents_hidden_globally else "Recent behavior/homework logs shown globally."
        self.update_status(status_msg)
        self.password_manager.record_activity()

    def update_toggle_incidents_button_text(self): # Renamed
        """Updates the text of the 'Hide/Show Recent Logs' button."""
        if hasattr(self, "toggle_incidents_btn"):
            # Text reflects combined state of behavior and homework logs
            text = "Show Recent Logs" if self._recent_incidents_hidden_globally or self._recent_homeworks_hidden_globally else "Hide Recent Logs"
            self.toggle_incidents_btn.config(text=text)

    def clear_recent_logs_for_student(self, student_id): # Renamed
        """
        Hides recent log entries for a specific student until a new log is added
        or they are explicitly shown again.

        Args:
            student_id (str): The ID of the student.
        """
        if self.password_manager.is_locked:
            if not self.prompt_for_password("Unlock to Clear Logs", "Enter password to clear logs for student:"): return
        self._per_student_last_cleared[student_id] = datetime.now().isoformat()
        self.draw_single_student(student_id, check_collisions=True)
        student = self.students.get(student_id)
        if student: self.update_status(f"Recent behavior/homework logs cleared for {student['full_name']}.")
        self.save_data_wrapper(); self.password_manager.record_activity()

    def show_recent_logs_for_student(self, student_id): # Renamed
        """
        Resumes showing recent log entries for a student who previously had them hidden.

        Args:
            student_id (str): The ID of the student.
        """
        if self.password_manager.is_locked:
            if not self.prompt_for_password("Unlock to Show Logs", "Enter password to show logs for student:"): return
        if student_id in self._per_student_last_cleared:
            del self._per_student_last_cleared[student_id]
            self.draw_single_student(student_id, check_collisions=True)
            student = self.students.get(student_id)
            if student: self.update_status(f"Recent behavior/homework logs will now show for {student['full_name']}.")
            self.save_data_wrapper(); self.password_manager.record_activity()

    def _get_recent_logs_for_student(self, student_id, log_type_key): # "behavior" or "homework"
        """
        Retrieves a formatted list of recent log entries for a student to be displayed
        on their box.

        Args:
            student_id (str): The ID of the student.
            log_type_key (str): The type of log to retrieve ("behavior" or "homework").

        Returns:
            list[str]: A list of strings, each representing a recent log entry.
        """
        student = self.students.get(student_id)
        if not student: return []

        summary_lines_list = []
        log_source = self.behavior_log if log_type_key == "behavior" else self.homework_log
        setting_prefix = "recent_incidents" if log_type_key == "behavior" else "recent_homeworks" # For settings keys
        global_hidden_flag = self._recent_incidents_hidden_globally if log_type_key == "behavior" else self._recent_homeworks_hidden_globally
        behavior_key_in_log = "behavior" if log_type_key == "behavior" else "homework_type" # Or "behavior" for manual homework log

        if not global_hidden_flag and self.settings.get(f"show_{setting_prefix}_on_boxes", True):
            num_to_show = self.settings.get(f"num_{setting_prefix}_to_show", 0)
            if num_to_show > 0:
                time_window_hours = self.settings.get(f"{setting_prefix}_time_window_hours", 24)
                cutoff_time = datetime.now() - timedelta(hours=time_window_hours)
                last_cleared_iso = self._per_student_last_cleared.get(student_id)
                cleared_dt = datetime.fromisoformat(last_cleared_iso) if last_cleared_iso else None

                # Adjust filter for log type. Behavior logs have "type":"behavior", quiz logs have "type":"quiz".
                # Homework logs have "type":"homework" or "type":"homework_session".
                type_filter_values = []
                if log_type_key == "behavior": type_filter_values = ["behavior", "quiz"] # Behavior tab shows both
                elif log_type_key == "homework": type_filter_values = ["homework", "homework_session_y", "homework_session_s"]


                all_recent_logs = sorted(
                    [log for log in log_source
                     if log["student_id"] == student_id and log.get("type") in type_filter_values and
                        datetime.fromisoformat(log["timestamp"]) >= cutoff_time and
                        (not cleared_dt or datetime.fromisoformat(log["timestamp"]) > cleared_dt)],
                    key=lambda x: x["timestamp"], reverse=True
                )

                specific_filter_list = self.settings.get(f"selected_{setting_prefix}_filter", None)
                filtered_logs = []
                if specific_filter_list is None: filtered_logs = all_recent_logs
                elif isinstance(specific_filter_list, list) and not specific_filter_list: filtered_logs = [] # Empty list means filter all
                elif isinstance(specific_filter_list, list):
                    filtered_logs = [log for log in all_recent_logs if log.get(behavior_key_in_log, log.get("behavior")) in specific_filter_list]


                recent_to_display = filtered_logs[:num_to_show]
                if self.settings.get(f"reverse_{setting_prefix.replace('s', '')}_order", True): recent_to_display.reverse()

                initial_overrides_key = "behavior_initial_overrides" if log_type_key == "behavior" else "homework_initial_overrides"
                initial_overrides = self.settings.get(initial_overrides_key, {})
                
                #string_for_get = 
                
                if self.settings.get(f"show_full_{setting_prefix}", False):
                    summary_lines_list = [log.get(behavior_key_in_log, log.get("behavior")) for log in recent_to_display if log.get(behavior_key_in_log, log.get("behavior"))]
                else:
                    temp_initials = []
                    for entry in recent_to_display:
                        name = entry.get(behavior_key_in_log, entry.get("behavior"))
                        if name in initial_overrides and initial_overrides[name]: temp_initials.append(initial_overrides[name])
                        elif name: temp_initials.append(''.join(part[0].upper() for part in name.split() if part))
                        else: temp_initials.append("?")
                    if temp_initials: summary_lines_list.append('  '.join(temp_initials))
        return summary_lines_list

    def _get__logs_for_student(self, student_id, log_type_key, num_max, window, name_of_spec): # "behavior" or "homework"
        """
        Retrieves a count of specific log entries for a student, used by conditional formatting.
        (Internal helper function)
        """
        student = self.students.get(student_id)
        if not student: return []
        #print(num_max)
        summary_lines_list = []
        log_source = self.behavior_log if log_type_key == "behavior" else self.homework_log
        setting_prefix = "recent_incidents" if log_type_key == "behavior" else "recent_homeworks" # For settings keys
        global_hidden_flag = self._recent_incidents_hidden_globally if log_type_key == "behavior" else self._recent_homeworks_hidden_globally
        behavior_key_in_log = "behavior" if log_type_key == "behavior" else "homework_type" # Or "behavior" for manual homework log

        if not global_hidden_flag and self.settings.get(f"show_{setting_prefix}_on_boxes", True):
            num_to_show = num_max
            if num_to_show > 0:
                time_window_hours = window
                cutoff_time = datetime.now() - timedelta(hours=time_window_hours)

                # Adjust filter for log type. Behavior logs have "type":"behavior", quiz logs have "type":"quiz".
                # Homework logs have "type":"homework" or "type":"homework_session".
                type_filter_values = []
                if log_type_key == "behavior": type_filter_values = ["behavior", "quiz"] # Behavior tab shows both
                elif log_type_key == "homework": type_filter_values = ["homework", "homework_session_y", "homework_session_s"]


                all_recent_logs = sorted(
                    [log for log in log_source
                     if log["student_id"] == student_id and log.get("type") in type_filter_values and
                        datetime.fromisoformat(log["timestamp"]) >= cutoff_time],
                    key=lambda x: x["timestamp"], reverse=True
                )

                specific_filter_list = [name_of_spec]
                filtered_logs = []
                if specific_filter_list is None: filtered_logs = all_recent_logs
                elif isinstance(specific_filter_list, list) and not specific_filter_list: filtered_logs = [] # Empty list means filter all
                elif isinstance(specific_filter_list, list):
                    filtered_logs = [log for log in all_recent_logs if log.get(behavior_key_in_log, log.get("behavior")) in specific_filter_list]


                recent_to_display = filtered_logs[:num_to_show]
                
                
                summary_lines_list = [log.get(behavior_key_in_log, log.get("behavior")) for log in recent_to_display if log.get(behavior_key_in_log, log.get("behavior"))]
                
        return len(summary_lines_list)

    def update_student_display_text(self, student_id):
        """
        Updates the text content to be displayed on a student's box.

        This includes the student's name and any relevant log entries or live session scores,
        depending on the current application mode.

        Args:
            student_id (str): The ID of the student to update.
        """
        student = self.students.get(student_id)
        if not student: return

        name_to_display = student.get('nickname') or student['first_name']
        main_content_lines = [name_to_display, student['last_name']]
        incident_display_lines = [] # List of dicts: {"text": "...", "type": "incident/quiz_score/homework_score"}

        current_mode = self.mode_var.get()
        if current_mode == "quiz" and self.is_live_quiz_active:
            score_text = f"{self.current_live_quiz_name}: (Pending)"
            if student_id in self.live_quiz_scores:
                score_info = self.live_quiz_scores[student_id]
                score_text = f"{self.current_live_quiz_name}: {score_info['correct']} of {score_info['total_asked']}"
            incident_display_lines.append({"text": score_text, "type": "quiz_score"})
            if self.settings.get("show_recent_incidents_during_quiz", True):
                for line_text in self._get_recent_logs_for_student(student_id, "behavior"):
                    if line_text: incident_display_lines.append({"text": line_text, "type": "incident"})

        elif current_mode == "homework" and self.is_live_homework_active: # New for live homework
            hw_session_mode = self.settings.get("live_homework_session_mode", "Yes/No")
            hw_score_data = self.live_homework_scores.get(student_id, {})
            hw_display_texts = []
            if hw_session_mode == "Yes/No":
                for hw_type_id, status in hw_score_data.items():
                    # Find homework type name from custom_homework_session_types or defaults
                    hw_type_obj = next((ht for ht in self.all_homework_session_types if isinstance(ht, dict) and ht.get('id') == hw_type_id), None)
                    hw_name_display = hw_type_obj['name'] if hw_type_obj else hw_type_id
                    hw_display_texts.append(f"{hw_name_display}: {status.capitalize()}")
            elif hw_session_mode == "Select" and "selected_options" in hw_score_data:
                hw_display_texts = list(hw_score_data["selected_options"])

            if hw_display_texts:
                incident_display_lines.append({"text": f"{self.current_live_homework_name}:", "type": "homework_score_header"})
                for text in hw_display_texts:
                    incident_display_lines.append({"text": f"  {text}", "type": "homework_score_item"})
            else:
                incident_display_lines.append({"text": f"{self.current_live_homework_name}: (Pending)", "type": "homework_score_header"})


        else: # Behavior mode or non-live quiz/homework mode
            # Show recent behavior/quiz logs
            for line_text in self._get_recent_logs_for_student(student_id, "behavior"):
                if line_text: incident_display_lines.append({"text": line_text, "type": "incident"})
            # Show recent homework logs
            homework_lines = self._get_recent_logs_for_student(student_id, "homework")
            if homework_lines and incident_display_lines: # Add separator if both types of logs exist
                incident_display_lines.append({"text": "--- Homework ---", "type": "separator"})
            for line_text in homework_lines:
                if line_text: incident_display_lines.append({"text": line_text, "type": "homework_log"})


        student["display_lines"] = main_content_lines
        student["incident_display_lines"] = incident_display_lines

    def applies_to_conditional(self, student_id, rule):
        """
        Checks if a specific conditional formatting rule applies to a given student
        at the current moment.

        This function evaluates all conditions of a rule, including type, enabled status,
        active modes, and active times.

        Args:
            student_id (str): The ID of the student to check.
            rule (dict): The conditional formatting rule dictionary.

        Returns:
            bool: True if the rule applies, False otherwise.
        """
        student_data = self.students.get(student_id)
        if not student_data: return False # Student data is essential

        # Preliminary checks based on new rule fields
        if not rule.get("enabled", True): # Default to enabled if key is missing (should be set by load_data)
            return False

        # Check active_modes
        active_modes = rule.get("active_modes", [])
        if active_modes: # If list is not empty, mode must match
            current_app_mode = self.mode_var.get() # "behavior", "quiz", "homework"
            effective_mode = current_app_mode # Base mode

            # Determine more specific "session" modes
            if current_app_mode == "quiz" and self.is_live_quiz_active:
                effective_mode = "quiz_session"
            elif current_app_mode == "homework" and self.is_live_homework_active:
                effective_mode = "homework_session"

            if effective_mode not in active_modes:
                return False

        # Check active_times
        active_times = rule.get("active_times", [])
        if active_times: # If list is not empty, time must match
            now = datetime.now()
            current_time_str = now.strftime("%H:%M")
            current_day_of_week = now.weekday() # Monday is 0 and Sunday is 6

            time_match_found = False
            for time_slot in active_times:
                slot_days = time_slot.get("days_of_week", list(range(7))) # Default to all days if not specified
                if current_day_of_week in slot_days:
                    start_time_str = time_slot.get("start_time")
                    end_time_str = time_slot.get("end_time")
                    if start_time_str and end_time_str:
                        if start_time_str <= current_time_str < end_time_str:
                            time_match_found = True
                            break
            if not time_match_found:
                return False

        # If all preliminary checks passed, proceed to rule-specific logic
        rule_type = rule.get("type")

        # --- Live Session Conditional Formatting Rules ---
        if rule_type == "live_quiz_response":
            if not self.is_live_quiz_active or student_id not in self.live_quiz_scores:
                return False
            student_live_score = self.live_quiz_scores[student_id]
            last_response_mark_id = student_live_score.get("last_response_details") # Assuming this is set by MarkLiveQuizQuestionCommand
            if not last_response_mark_id: return False

            effective_response_type = ""
            for mt in self.settings.get("quiz_mark_types", []):
                if mt["id"] == last_response_mark_id:
                    if "correct" in mt["name"].lower() or "bonus" in mt["name"].lower() or \
                       (mt.get("default_points", 0) > 0 and not mt.get("is_extra_credit", False)) or \
                       (mt.get("default_points", 0) > 0 and mt.get("is_extra_credit", True)):
                        effective_response_type = "Correct"
                    elif "incorrect" in mt["name"].lower() or mt.get("default_points", 0) == 0:
                         effective_response_type = "Incorrect"
                    break

            rule_quiz_response = rule.get("quiz_response")
            return bool(effective_response_type and rule_quiz_response and effective_response_type == rule_quiz_response)

        elif rule_type == "live_homework_yes_no":
            if not self.is_live_homework_active or self.settings.get("live_homework_session_mode") != "Yes/No" or \
               student_id not in self.live_homework_scores:
                return False
            student_hw_data = self.live_homework_scores.get(student_id, {})
            rule_hw_type_id = rule.get("homework_type_id")
            rule_hw_response = rule.get("homework_response")
            return bool(rule_hw_type_id in student_hw_data and student_hw_data[rule_hw_type_id] == rule_hw_response)

        elif rule_type == "live_homework_select":
            if not self.is_live_homework_active or self.settings.get("live_homework_session_mode") != "Select" or \
               student_id not in self.live_homework_scores:
                return False
            student_hw_data = self.live_homework_scores.get(student_id, {})
            rule_option_name = rule.get("homework_option_name")
            return bool("selected_options" in student_hw_data and rule_option_name in student_hw_data["selected_options"])

        # --- Standard Conditional Formatting Rules (Non-Live Session) ---
        if rule_type == "behavior_count":
            time_window_hours = rule.get("time_window_hours", 24) # Default if not set
            count_threshold = rule.get("count_threshold", 1)
            behavior_name = rule.get("behavior_name", "")
            if not behavior_name: # Behavior name is essential for this rule type
                return False

            # _get__logs_for_student returns the count of matching logs to be displayed
            # The third argument to _get__logs_for_student is num_max (for display),
            # but here it's used as the threshold for comparison.
            # This might be okay if _get__logs_for_student correctly counts beyond num_max internally
            # or if the intent is to check against the *displayed* count.
            # For now, assuming existing logic of _get__logs_for_student is what's intended.
            actual_count = self._get__logs_for_student(student_id, "behavior", count_threshold, time_window_hours, behavior_name)
            
            # The comparison was actual_count >= count_threshold.
            # If _get__logs_for_student returns a count that is capped by its num_max (which is count_threshold here),
            # then (result >= count_threshold) would only be true if result == count_threshold.
            # This needs careful check of _get__logs_for_student's behavior or adjustment here.
            # For now, sticking to the original comparison structure.
            if actual_count >= count_threshold:
                return True
            return False # Explicitly return False if condition not met

        elif rule_type == "quiz_score_threshold":
            operator = rule.get("operator", "<=")
            quiz_name_contains = rule.get("quiz_name_contains", "")
            score_threshold_percent = rule.get("score_threshold_percent", 50.0)
            
            # Placeholder for actual quiz score logic - to be implemented next
            # This will iterate through relevant quiz logs for the student
            # calculate score % and compare.
            for log_entry in self.behavior_log:
                if log_entry.get("student_id") == student_id and log_entry.get("type") == "quiz":
                    # Check quiz name
                    if quiz_name_contains and quiz_name_contains.lower() not in log_entry.get("behavior", "").lower():
                        continue

                    current_score_percentage = self._calculate_quiz_score_percentage(log_entry)
                    if current_score_percentage is None:
                        continue

                    # Compare with threshold
                    if operator == "<=" and current_score_percentage <= score_threshold_percent: return True
                    elif operator == ">=" and current_score_percentage >= score_threshold_percent: return True
                    elif operator == "==" and abs(current_score_percentage - score_threshold_percent) < 0.01 : return True # Using tolerance for float comparison
                    elif operator == "<" and current_score_percentage < score_threshold_percent: return True
                    elif operator == ">" and current_score_percentage > score_threshold_percent: return True
            return False # No matching quiz log found or condition not met

        elif rule_type == "quiz_mark_count":
            quiz_name_contains = rule.get("quiz_name_contains", "").lower()
            mark_type_id_to_check = rule.get("mark_type_id")
            operator = rule.get("mark_operator", ">=") # Default operator
            count_threshold = rule.get("mark_count_threshold", 1)

            if not mark_type_id_to_check: # Mark type ID is essential
                return False

            for log_entry in self.behavior_log:
                if log_entry.get("student_id") == student_id and log_entry.get("type") == "quiz":
                    # Check quiz name
                    if quiz_name_contains and quiz_name_contains not in log_entry.get("behavior", "").lower():
                        continue

                    marks_data = log_entry.get("marks_data", {})
                    actual_count = marks_data.get(mark_type_id_to_check, 0) # Default to 0 if mark_type not in log

                    if not isinstance(actual_count, (int, float)): # Ensure we are comparing numbers
                        actual_count = 0

                    # Compare with threshold
                    if operator == ">=" and actual_count >= count_threshold: return True
                    elif operator == "<=" and actual_count <= count_threshold: return True
                    elif operator == "==" and actual_count == count_threshold: return True
                    elif operator == ">" and actual_count > count_threshold: return True
                    elif operator == "<" and actual_count < count_threshold: return True
                    elif operator == "!=" and actual_count != count_threshold: return True
            return False # No matching quiz log found or condition not met

        elif rule_type == "group":
            # Group rules are handled directly in draw_single_student before this method is called.
            # If it reaches here, it means it's not a group rule being evaluated by this function.
            return False
        
        return False # Default for unknown or unhandled rule types
        #if student_data.get()
        
    def draw_single_student(self, student_id, check_collisions=False):
        """
        Draws or updates a single student's box on the canvas.

        This method handles all visual aspects of a student box, including its size, position,
        colors, text content, selection highlight, resize handles, and conditional formatting.

        Args:
            student_id (str): The ID of the student to draw.
            check_collisions (bool): If True, checks for and resolves layout collisions after drawing.
        """
        # ... (largely same as v51, but needs to handle new "homework_score_header/item" and "separator" types for drawing)
        # This method is long, so I'll highlight the key change area for incident_display_lines
        try:
            student_data = self.students.get(student_id)
            if not student_data: return
            self.update_student_display_text(student_id)

            style_overrides = student_data.get("style_overrides", {})
            world_x, world_y = student_data["x"], student_data["y"]
            world_width = style_overrides.get("width", student_data.get("width", self.settings.get("default_student_box_width")))
            world_base_height = style_overrides.get("height", student_data.get("height", self.settings.get("default_student_box_height")))
            canvas_x, canvas_y = self.world_to_canvas_coords(world_x, world_y)
            canvas_width = world_width * self.current_zoom_level
            canvas_base_height = world_base_height * self.current_zoom_level

            fill_color = style_overrides.get("fill_color", self.settings.get("student_box_fill_color"))
            outline_color_orig = style_overrides.get("outline_color", self.settings.get("student_box_outline_color"))
            font_family = style_overrides.get("font_family", self.settings.get("student_font_family"))
            font_size_world = style_overrides.get("font_size", self.settings.get("student_font_size"))
            font_size_canvas = int(max(6, font_size_world * self.current_zoom_level))
            font_color = style_overrides.get("font_color", self.settings.get("student_font_color"))

            group_id = student_data.get("group_id"); group_indicator_color = None
            if self.settings.get("student_groups_enabled", True) and group_id and group_id in self.student_groups:
                group_data = self.student_groups[group_id]
                group_indicator_color = group_data.get("color")
                # Apply the first matching group rule to the base fill_color and outline_color_orig
                for rule in self.settings.get("conditional_formatting_rules", []):
                    if rule.get("type") == "group" and rule.get("group_id") == group_id:
                        if rule.get("color"): # Check if color is not empty or None
                            fill_color = rule["color"]
                        if rule.get("outline"): # Check if outline is not empty or None
                            outline_color_orig = rule["outline"]
                        break # First matching group rule takes precedence for base colors

            # Now, collect all other (non-group) applicable conditional formatting rules
            active_rules_colors = []
            # Base colors that will be used if no other rules apply or for the first stripe.
            # These might have been set by a group rule already.
            # If active_rules_colors remains empty, these base colors will be used for the whole box.
            
            # Store the base colors derived from defaults, overrides, or group rules.
            # These will be used if no other active_rules_colors are found, or as the first "layer" if we decide to.
            # For now, if active_rules_colors gets populated, those will define the stripes.
            # If active_rules_colors is empty, the single fill_color/outline_color_orig will be used.

            if self.settings.get("conditional_formatting_rules", []):
                for rule in self.settings.get("conditional_formatting_rules", []):
                    if rule.get("type") == "group":
                        continue  # Group rules already processed for base color

                    if self.applies_to_conditional(student_id, rule):
                        rule_fill = rule.get("color")
                        rule_outline = rule.get("outline")
                        if rule_fill or rule_outline: # Only add if the rule specifies a color
                            active_rules_colors.append({
                                "fill": rule_fill if rule_fill else None,
                                "outline": rule_outline if rule_outline else None
                            })
                            # No break here, collect all matching non-group rules.
            
            # If active_rules_colors is empty, the drawing logic
            # will use the existing fill_color and outline_color_orig for the single rectangle.
            # If populated, it will draw stripes based on these collected colors.
            # The original fill_color and outline_color_orig (potentially set by a group rule)
            # can be considered the "base" if no other rules apply.

            live_override_applied = False
            # Process override rules first for live sessions
            if self.is_live_quiz_active or self.is_live_homework_active:
                for rule in self.settings.get("conditional_formatting_rules", []):
                    if rule.get("type") in ["live_quiz_response", "live_homework_yes_no", "live_homework_select"] and \
                       rule.get("application_style") == "override":
                        if self.applies_to_conditional(student_id, rule):
                            if rule.get("color"): fill_color = rule["color"]
                            if rule.get("outline"): outline_color_orig = rule["outline"]
                            active_rules_colors = []  # Clear any standard stripes if overridden
                            live_override_applied = True
                            break

            # Collect stripe rules (standard and live, if no live override took place)
            if not live_override_applied:
                active_rules_colors = [] # Ensure it's clean before collecting stripes
                for rule in self.settings.get("conditional_formatting_rules", []):
                    rule_type = rule.get("type")
                    is_live_rule = rule_type in ["live_quiz_response", "live_homework_yes_no", "live_homework_select"]

                    if rule_type == "group":
                        continue

                    applies_now = False
                    if is_live_rule:
                        if rule.get("application_style") == "stripe":
                            if (self.is_live_quiz_active and rule_type == "live_quiz_response") or \
                               (self.is_live_homework_active and rule_type in ["live_homework_yes_no", "live_homework_select"]):
                                applies_now = self.applies_to_conditional(student_id, rule)
                    else:
                        applies_now = self.applies_to_conditional(student_id, rule)

                    if applies_now:
                        rule_fill = rule.get("color")
                        rule_outline = rule.get("outline")
                        if rule_fill or rule_outline:
                            active_rules_colors.append({
                                "fill": rule_fill if rule_fill else None,
                                "outline": rule_outline if rule_outline else None
                            })

            # Font setup using new specific settings
            name_font_obj = tkfont.Font(family=font_family, size=font_size_canvas, weight="bold")

            behavior_log_font_size_canvas = int(max(5, self.settings.get("behavior_log_font_size", DEFAULT_FONT_SIZE -1) * self.current_zoom_level))
            incident_font_obj = tkfont.Font(family=font_family, size=behavior_log_font_size_canvas)

            quiz_log_font_size_canvas = int(max(5, self.settings.get("quiz_log_font_size", DEFAULT_FONT_SIZE) * self.current_zoom_level))
            quiz_score_font_color_setting = self.settings.get("live_quiz_score_font_color")
            quiz_score_font_bold_setting = self.settings.get("live_quiz_score_font_style_bold")
            quiz_score_font_weight = "bold" if quiz_score_font_bold_setting else "normal"
            quiz_score_font_obj = tkfont.Font(family=font_family, size=quiz_log_font_size_canvas, weight=quiz_score_font_weight)

            homework_log_font_size_canvas = int(max(5, self.settings.get("homework_log_font_size", DEFAULT_FONT_SIZE -1) * self.current_zoom_level))
            hw_score_font_color_setting = self.settings.get("live_homework_score_font_color", DEFAULT_HOMEWORK_SCORE_FONT_COLOR)
            hw_score_font_bold_setting = self.settings.get("live_homework_score_font_style_bold", DEFAULT_HOMEWORK_SCORE_FONT_STYLE_BOLD)
            hw_score_font_weight = "bold" if hw_score_font_bold_setting else "normal"
            # For homework_score_header, use the dedicated homework_log_font_size
            hw_score_font_obj = tkfont.Font(family=font_family, size=homework_log_font_size_canvas, weight=hw_score_font_weight)
            # For homework_score_item, also use homework_log_font_size (or could be a new setting if finer control is needed)
            hw_score_item_font_obj = tkfont.Font(family=font_family, size=homework_log_font_size_canvas, weight=hw_score_font_weight)
            
            self.canvas.delete(student_id)
            rect_tag = ("student_item", student_id, "rect")

            world_padding = 5; canvas_padding = world_padding * self.current_zoom_level
            current_y_offset_for_calc_world = world_padding
            for name_line_text in student_data.get("display_lines", []):
                font_for_calc = tkfont.Font(family=font_family, size=font_size_world, weight="bold")
                current_y_offset_for_calc_world += font_for_calc.metrics('linespace')

            if student_data.get("incident_display_lines"):
                current_y_offset_for_calc_world += world_padding / 2
                for line_info in student_data.get("incident_display_lines", []):
                    line_text, line_type = line_info["text"], line_info["type"]
                    current_font_world_calc = tkfont.Font(family=font_family, size=font_size_world -1)
                    if line_type == "quiz_score": current_font_world_calc = tkfont.Font(family=font_family, size=font_size_world, weight=quiz_score_font_weight)
                    elif line_type == "homework_score_header": current_font_world_calc = tkfont.Font(family=font_family, size=font_size_world, weight=hw_score_font_weight)
                    elif line_type == "homework_score_item": current_font_world_calc = tkfont.Font(family=font_family, size=max(5, font_size_world -1), weight=hw_score_font_weight)
                    elif line_type == "separator": current_font_world_calc = tkfont.Font(family=font_family, size=max(4, font_size_world -2)) # Smaller for separator

                    text_width_pixels_world = current_font_world_calc.measure(line_text)
                    visual_lines_world = 1
                    available_width_for_text_world = world_width - 2 * world_padding
                    if available_width_for_text_world > 0 and text_width_pixels_world > available_width_for_text_world:
                        visual_lines_world = -(-text_width_pixels_world // available_width_for_text_world)
                    current_y_offset_for_calc_world += visual_lines_world * current_font_world_calc.metrics('linespace')

            world_text_content_height_with_padding = current_y_offset_for_calc_world + world_padding
            world_dynamic_height = max(world_base_height, world_text_content_height_with_padding)
            canvas_dynamic_height = world_dynamic_height * self.current_zoom_level
            student_data['_current_world_height'] = world_dynamic_height
            student_data['_current_world_width'] = world_width

            # Box drawing logic:
            if not active_rules_colors:
                # No specific non-group rules apply, draw a single box with base/group colors
                self.canvas.create_rectangle(canvas_x, canvas_y, canvas_x + canvas_width, canvas_y + canvas_dynamic_height,
                                             fill=fill_color, outline=outline_color_orig, width=max(1, int(2 * self.current_zoom_level)), tags=rect_tag)
            else:
                num_effective_rules = min(len(active_rules_colors), 3) # Max 3 stripes
                stripe_height_canvas = canvas_dynamic_height / num_effective_rules

                base_default_fill = self.settings.get("student_box_fill_color")
                base_default_outline = self.settings.get("student_box_outline_color")

                for i in range(num_effective_rules):
                    rule_colors = active_rules_colors[i]
                    stripe_fill = rule_colors.get("fill") if rule_colors.get("fill") else fill_color # Fallback to base fill_color (from group/default)
                    stripe_outline = rule_colors.get("outline") if rule_colors.get("outline") else outline_color_orig # Fallback to base outline_color_orig

                    # If even the fallback is None (e.g. student default is empty string), provide a very basic default.
                    if not stripe_fill: stripe_fill = base_default_fill
                    if not stripe_outline: stripe_outline = base_default_outline

                    stripe_y_start = canvas_y + (i * stripe_height_canvas)
                    stripe_y_end = canvas_y + ((i + 1) * stripe_height_canvas)

                    # For the last stripe, ensure it goes exactly to the bottom edge to avoid floating point issues
                    if i == num_effective_rules - 1:
                        stripe_y_end = canvas_y + canvas_dynamic_height

                    self.canvas.create_rectangle(canvas_x, stripe_y_start, canvas_x + canvas_width, stripe_y_end,
                                                 fill=stripe_fill,
                                                 outline=stripe_outline,
                                                 width=max(1, int(1 * self.current_zoom_level)), # Thinner outline for stripes
                                                 tags=rect_tag + (f"stripe_{i}",))

            # --- Text Drawing ---
            current_y_text_draw_canvas = canvas_y + canvas_padding
            available_text_width_canvas = canvas_width - 2 * canvas_padding
            colored = True if self.settings.get("always_show_text_background_panel", False) or active_rules_colors else False
            if self.settings.get("enable_text_background_panel", True) and colored:
                text_panel_fill = "#F0F0F0" # Light gray for text background
                text_panel_internal_padding = 2 * self.current_zoom_level # Small padding around text within its panel

                # Panel for Name Lines
                name_lines_content_for_panel = student_data.get("display_lines", [])
                if name_lines_content_for_panel:
                    name_block_height_canvas = 0
                    max_name_width_pixels = 0
                    for name_line_text_calc in name_lines_content_for_panel:
                        name_block_height_canvas += name_font_obj.metrics('linespace')
                        max_name_width_pixels = max(max_name_width_pixels, name_font_obj.measure(name_line_text_calc))

                    name_panel_width = min(max_name_width_pixels + 2 * text_panel_internal_padding, available_text_width_canvas - 2 * text_panel_internal_padding)
                    name_panel_height = name_block_height_canvas

                    name_panel_x0 = canvas_x + (canvas_width - name_panel_width) / 2
                    name_panel_y0 = (canvas_y + canvas_padding) - text_panel_internal_padding
                    name_panel_x1 = name_panel_x0 + name_panel_width
                    name_panel_y1 = name_panel_y0 + name_panel_height + 2 * text_panel_internal_padding

                    if name_panel_y1 < (canvas_y + canvas_dynamic_height - canvas_padding * 0.5):
                        self.canvas.create_rectangle(name_panel_x0, name_panel_y0, name_panel_x1, name_panel_y1,
                                                     fill=text_panel_fill, outline="",
                                                     tags=("student_item", student_id, "text_background_name"))

                # Panel for Incident/Score Lines
                incident_lines_content_for_panel = student_data.get("incident_display_lines", [])
                if incident_lines_content_for_panel:
                    incident_block_start_y_for_panel = (canvas_y + canvas_padding) + \
                                                       sum(name_font_obj.metrics('linespace') for _ in name_lines_content_for_panel) + \
                                                       (canvas_padding / 2 if name_lines_content_for_panel else 0)
                    incident_block_height_canvas = 0
                    max_incident_width_pixels = 0

                    for line_info_calc in incident_lines_content_for_panel:
                        line_text_calc, line_type_calc = line_info_calc["text"], line_info_calc["type"]
                        current_font_for_calc = incident_font_obj
                        if line_type_calc == "quiz_score": current_font_for_calc = quiz_score_font_obj
                        elif line_type_calc == "homework_score_header": current_font_for_calc = hw_score_font_obj
                        elif line_type_calc == "homework_score_item": current_font_for_calc = hw_score_item_font_obj
                        elif line_type_calc == "separator": current_font_for_calc = tkfont.Font(family=font_family, size=max(4, int((font_size_world-2)*self.current_zoom_level)))

                        text_width_pixels_canvas_calc = current_font_for_calc.measure(line_text_calc)
                        available_incident_text_width_calc = available_text_width_canvas - (text_panel_internal_padding if line_type_calc == "homework_score_item" else 0)
                        visual_lines_calc = 1
                        if available_incident_text_width_calc > 0 and text_width_pixels_canvas_calc > available_incident_text_width_calc:
                            visual_lines_calc = -(-text_width_pixels_canvas_calc // available_incident_text_width_calc)
                        incident_block_height_canvas += visual_lines_calc * current_font_for_calc.metrics('linespace')
                        max_incident_width_pixels = max(max_incident_width_pixels, min(text_width_pixels_canvas_calc, available_incident_text_width_calc))

                    if incident_block_height_canvas > 0:
                        incident_panel_width = min(max_incident_width_pixels + 2 * text_panel_internal_padding, available_text_width_canvas - 2 * text_panel_internal_padding)
                        incident_panel_height = incident_block_height_canvas

                        inc_panel_x0 = canvas_x + (canvas_width - incident_panel_width) / 2
                        inc_panel_y0 = incident_block_start_y_for_panel - text_panel_internal_padding
                        inc_panel_x1 = inc_panel_x0 + incident_panel_width
                        inc_panel_y1 = inc_panel_y0 + incident_panel_height + 2 * text_panel_internal_padding

                        if inc_panel_y1 < (canvas_y + canvas_dynamic_height - canvas_padding * 0.5):
                             self.canvas.create_rectangle(inc_panel_x0, inc_panel_y0, inc_panel_x1, inc_panel_y1,
                                                         fill=text_panel_fill, outline="",
                                                         tags=("student_item", student_id, "text_background_incidents"))

            # Draw Name Lines (always drawn, panel is conditional)
            name_lines_content = student_data.get("display_lines", [])
            for name_line_text in name_lines_content:
                self.canvas.create_text(canvas_x + canvas_width / 2, current_y_text_draw_canvas, text=name_line_text,
                                        fill=font_color, font=name_font_obj, tags=("student_item", student_id, "text", "student_name"),
                                        anchor=tk.N, width=max(1, available_text_width_canvas), justify=tk.CENTER)
                current_y_text_draw_canvas += name_font_obj.metrics('linespace')

            # Draw Incident/Score Lines (always drawn, panel is conditional)
            incident_lines_content = student_data.get("incident_display_lines", [])
            if incident_lines_content:
                current_y_text_draw_canvas += canvas_padding / 2 # Space before incidents

                for line_info in incident_lines_content:
                    line_text, line_type = line_info["text"], line_info["type"]
                    current_font_canvas_draw, current_color_canvas_draw = incident_font_obj, font_color
                    text_anchor_canvas, text_justify_canvas = tk.N, tk.CENTER
                    text_x_pos_canvas = canvas_x + canvas_width / 2

                    if line_type == "quiz_score": current_font_canvas_draw, current_color_canvas_draw = quiz_score_font_obj, quiz_score_font_color_setting
                    elif line_type == "homework_score_header": current_font_canvas_draw, current_color_canvas_draw = hw_score_font_obj, hw_score_font_color_setting
                    elif line_type == "homework_score_item":
                        current_font_canvas_draw, current_color_canvas_draw = hw_score_item_font_obj, hw_score_font_color_setting
                        text_anchor_canvas, text_justify_canvas = tk.NW, tk.LEFT
                        text_x_pos_canvas = canvas_x + canvas_padding
                    elif line_type == "separator":
                        current_font_canvas_draw = tkfont.Font(family=font_family, size=max(4, int((font_size_world-2)*self.current_zoom_level)))
                        current_color_canvas_draw = "gray"

                    self.canvas.create_text(text_x_pos_canvas, current_y_text_draw_canvas, text=line_text,
                                            fill=current_color_canvas_draw, font=current_font_canvas_draw,
                                            tags=("student_item", student_id, "text", f"student_{line_type}"),
                                            anchor=text_anchor_canvas, width=max(1, available_text_width_canvas if text_anchor_canvas == tk.N else available_text_width_canvas - canvas_padding),
                                            justify=text_justify_canvas)
                    text_width_pixels_canvas = current_font_canvas_draw.measure(line_text)
                    visual_lines_canvas = 1
                    if available_text_width_canvas > 0 and text_width_pixels_canvas > available_text_width_canvas:
                        visual_lines_canvas = -(-text_width_pixels_canvas // available_text_width_canvas)
                    current_y_text_draw_canvas += visual_lines_canvas * current_font_canvas_draw.metrics('linespace')

            if self.settings.get("student_groups_enabled", True) and group_indicator_color:
                indicator_size_canvas = GROUP_COLOR_INDICATOR_SIZE * self.current_zoom_level
                indicator_padding_canvas = 2 * self.current_zoom_level
                indicator_x = canvas_x + canvas_width - indicator_size_canvas - indicator_padding_canvas
                indicator_y = canvas_y + indicator_padding_canvas
                self.canvas.create_rectangle(indicator_x, indicator_y, indicator_x + indicator_size_canvas, indicator_y + indicator_size_canvas,
                                            fill=group_indicator_color, outline=outline_color_orig, tags=("student_item", student_id, "group_indicator"))
            if student_id in self.selected_items:
                sel_outline_width = max(1, int(2 * self.current_zoom_level))
                self.canvas.create_rectangle(canvas_x - sel_outline_width, canvas_y - sel_outline_width,
                                             canvas_x + canvas_width + sel_outline_width, canvas_y + canvas_dynamic_height + sel_outline_width,
                                             outline="red", width=sel_outline_width, tags=("student_item", student_id, "selection_highlight"))
            if self.edit_mode_var.get() and student_id in self.selected_items:
                handle_size_canvas = RESIZE_HANDLE_SIZE * self.current_zoom_level
                br_x = canvas_x + canvas_width - handle_size_canvas / 2 # Center handle on corner
                br_y = canvas_y + canvas_dynamic_height - handle_size_canvas / 2
                self.canvas.create_rectangle(br_x - handle_size_canvas/2, br_y - handle_size_canvas/2,
                                             br_x + handle_size_canvas/2, br_y + handle_size_canvas/2,
                                             fill="gray", outline="black", tags=("student_item", student_id, "resize_handle", "br_handle"))
            if check_collisions and self.settings.get("check_for_collisions", True): self.handle_layout_collision(student_id)
        except AttributeError: pass # Canvas might not be fully initialized during early calls

    def draw_single_furniture(self, furniture_id):
        """
        Draws or updates a single piece of furniture on the canvas.

        Args:
            furniture_id (str): The ID of the furniture item to draw.
        """
        # ... (same as v51)
        item_data = self.furniture.get(furniture_id)
        if not item_data: return
        world_x, world_y = item_data["x"], item_data["y"]
        world_width = item_data.get("width", DEFAULT_STUDENT_BOX_WIDTH)
        world_height = item_data.get("height", DEFAULT_STUDENT_BOX_HEIGHT)
        canvas_x, canvas_y = self.world_to_canvas_coords(world_x, world_y)
        canvas_width = world_width * self.current_zoom_level
        canvas_height = world_height * self.current_zoom_level
        item_data['_current_world_height'] = world_height
        item_data['_current_world_width'] = world_width
        fill_color = item_data.get("fill_color", "lightgrey")
        outline_color = item_data.get("outline_color", "dimgray")
        name = item_data.get("name", "Furniture")
        try:
            self.canvas.delete(furniture_id)
            rect_tag = ("furniture_item", furniture_id, "rect")
            self.canvas.create_rectangle(canvas_x, canvas_y, canvas_x + canvas_width, canvas_y + canvas_height,
                                         fill=fill_color, outline=outline_color, width=max(1, int(2*self.current_zoom_level)), tags=rect_tag)
            font_size_canvas = int(max(6, (self.settings.get("student_font_size", DEFAULT_FONT_SIZE) -1) * self.current_zoom_level))
            font_spec = (self.settings.get("student_font_family", DEFAULT_FONT_FAMILY), font_size_canvas)
            self.canvas.create_text(canvas_x + canvas_width / 2, canvas_y + canvas_height / 2, text=name,
                                    fill=self.settings.get("student_font_color", DEFAULT_FONT_COLOR), font=font_spec,
                                    tags=("furniture_item", furniture_id, "text"), anchor=tk.CENTER,
                                    width=max(1, canvas_width - int(10*self.current_zoom_level)), justify=tk.CENTER)
            if furniture_id in self.selected_items:
                sel_outline_width = max(1, int(2 * self.current_zoom_level))
                self.canvas.create_rectangle(canvas_x - sel_outline_width, canvas_y - sel_outline_width,
                                             canvas_x + canvas_width + sel_outline_width, canvas_y + canvas_height + sel_outline_width,
                                             outline="red", width=sel_outline_width, tags=("furniture_item", furniture_id, "selection_highlight"))
            if self.edit_mode_var.get() and furniture_id in self.selected_items:
                handle_size_canvas = RESIZE_HANDLE_SIZE * self.current_zoom_level
                br_x = canvas_x + canvas_width - handle_size_canvas / 2
                br_y = canvas_y + canvas_height - handle_size_canvas / 2
                self.canvas.create_rectangle(br_x - handle_size_canvas/2, br_y - handle_size_canvas/2,
                                             br_x + handle_size_canvas/2, br_y + handle_size_canvas/2,
                                             fill="gray", outline="black", tags=("furniture_item", furniture_id, "resize_handle", "br_handle"))
        except AttributeError: pass

    def draw_all_items(self, check_collisions_on_redraw=False):
        """
        Clears and redraws all items on the canvas, including students, furniture,
        grid, rulers, and guides. Also recalculates the scroll region.

        Args:
            check_collisions_on_redraw (bool): If True, runs collision detection after drawing.
        """
        if not self.canvas: return
        self.canvas.delete("all") # Clear canvas before redrawing everything

        if self.settings.get("show_grid", False):
            self.draw_grid()

        if self.settings.get("show_rulers", False):
            self.draw_rulers()

        # Draw temporary guides first, so they are under items if needed (though typically on top)
        #self.draw_temporary_guides() # Guides will be drawn after items for better visibility
        # The new self.draw_guides() is called after items.

        all_items_data = list(self.students.values()) + list(self.furniture.values())
        
        if ((self.edit_mode_var.get() == True or self.settings.get("always_show_box_management", False) == True) and self.settings.get("show_canvas_border_lines", False) == True) or self.settings.get("force_canvas_border_lines", False) == True:
            self.canvas.create_line(0,0,1,2000, tags=("border_line", "border_vertical")) # These seem to be fixed debug lines, not dynamic with canvas/zoom
            self.canvas.create_line(0,0,2000,1, tags=("border_line", "border_horizontal")) # Consider removing or making them dynamic if kept.
        if not all_items_data:
            try:
                default_sr_w = self.canvas_orig_width * self.current_zoom_level; default_sr_h = self.canvas_orig_height * self.current_zoom_level
                self.canvas.configure(scrollregion=(0, 0, default_sr_w, default_sr_h))
            except AttributeError: pass
        else:
            min_x_world, min_y_world = float('inf'), float('inf'); max_x_world_br, max_y_world_br = float('-inf'), float('-inf')
            for item_data in all_items_data:
                item_world_x, item_world_y = item_data['x'], item_data['y']
                item_world_w = item_data.get('_current_world_width', item_data.get('width', DEFAULT_STUDENT_BOX_WIDTH))
                item_world_h = item_data.get('_current_world_height', item_data.get('height', DEFAULT_STUDENT_BOX_HEIGHT))
                min_x_world = min(min_x_world, item_world_x); min_y_world = min(min_y_world, item_world_y)
                max_x_world_br = max(max_x_world_br, item_world_x + item_world_w); max_y_world_br = max(max_y_world_br, item_world_y + item_world_h)
            padding_world = 100
            scroll_min_x_canvas, scroll_min_y_canvas = self.world_to_canvas_coords(min_x_world - padding_world, min_y_world - padding_world)
            scroll_max_x_canvas, scroll_max_y_canvas = self.world_to_canvas_coords(max_x_world_br + padding_world, max_y_world_br + padding_world)
            try:
                visible_canvas_width = self.canvas.winfo_width(); visible_canvas_height = self.canvas.winfo_height()
                final_scroll_max_x = max(scroll_max_x_canvas, scroll_min_x_canvas + visible_canvas_width)
                final_scroll_max_y = max(scroll_max_y_canvas, scroll_min_y_canvas + visible_canvas_height)
            except AttributeError: final_scroll_max_x, final_scroll_max_y = scroll_max_x_canvas, scroll_max_y_canvas # Fallback if winfo fails
            final_scroll_min_x = min(scroll_min_x_canvas, 0); final_scroll_min_y = min(scroll_min_y_canvas, 0)
            try: self.canvas.config(scrollregion=(final_scroll_min_x, final_scroll_min_y, final_scroll_max_x, final_scroll_max_y))
            except AttributeError: pass
        for student_id in self.students: self.draw_single_student(student_id, check_collisions=check_collisions_on_redraw)
        for furniture_id in self.furniture: self.draw_single_furniture(furniture_id)

        self.draw_guides() # Draw guides on top of items
        self.update_toggle_incidents_button_text(); self.update_zoom_display()
        self.update_toggle_rulers_button_text()
        self.update_toggle_grid_button_text()

    def draw_guides(self):
        """Draws all stored guides on the canvas."""
        if not self.canvas: return
        self.canvas.delete("guide") # Delete only items tagged 'guide'

        for guide_info in self.guides:
            guide_type = self.guides[guide_info].get('type')
            world_coord = self.guides[guide_info].get('world_coord') #guide_info['world_coord']
            guide_id_tag = self.guides[guide_info].get('id') #guide_info['id'] # e.g., "guide_v_1"

            canvas_item_id = None
            if guide_type == 'h': # Horizontal guide
                _, screen_y = self.world_to_canvas_coords(0, world_coord)
                canvas_item_id = self.canvas.create_line(
                    0, screen_y, self.canvas.winfo_width(), screen_y,
                    fill=self.guide_line_color, tags=("guide", guide_id_tag, "guide_h"), width=1, dash=(4, 2)
                )
            elif guide_type == 'v': # Vertical guide
                screen_x, _ = self.world_to_canvas_coords(world_coord, 0)
                canvas_item_id = self.canvas.create_line(
                    screen_x, 0, screen_x, self.canvas.winfo_height(),
                    fill=self.guide_line_color, tags=("guide", guide_id_tag, "guide_v"), width=1, dash=(4, 2)
                )
            self.guides[guide_info]['canvas_item_id'] = canvas_item_id #guide_info['canvas_item_id'] = canvas_item_id # Store/update Tkinter canvas item ID

    def toggle_grid_visibility(self):
        """Toggles the visibility of the grid on the canvas."""
        self.settings["show_grid"] = not self.settings.get("show_grid", False)
        self.draw_all_items()
        self.update_toggle_grid_button_text()
        self.update_status(f"Grid {'shown' if self.settings['show_grid'] else 'hidden'}.")

    def reload_canvas(self, event=None):
        """Forces a full redraw of the canvas."""
        self.draw_all_items()
        self.update_status("Reloaded")

    def update_toggle_grid_button_text(self):
        """Updates the text of the 'Toggle Grid' button."""
        if hasattr(self, 'toggle_grid_btn'):
            text = "Hide Grid" if self.settings.get("show_grid", False) else "Show Grid"
            self.toggle_grid_btn.config(text=text)

    def toggle_add_guide_mode(self, mode: str, button_pressed: ttk.Button):
        """
        Toggles the mode for adding guides and updates button visuals.

        Args:
            mode (str): The type of guide to add ('vertical' or 'horizontal').
            button_pressed (ttk.Button): The button that was pressed to activate the mode.
        """
        if self.add_guide_mode == mode: # Toggle off
            self.add_guide_mode = None
            if self.active_guide_button:
                self.active_guide_button.state(['!pressed', '!focus']) # Remove pressed and focus state
            self.active_guide_button = None
            self.update_status("Add guide mode deactivated.")
        else: # Toggle on for the given mode
            if self.active_guide_button: # Deactivate any other active guide button
                self.active_guide_button.state(['!pressed', '!focus'])

            self.add_guide_mode = mode
            self.active_guide_button = button_pressed
            self.active_guide_button.state(['pressed', 'focus']) # Set pressed and focus state
            self.update_status(f"Click on canvas to add a {mode} guide. Click button again to cancel.")

        # Ensure other button is not in pressed state
        if mode == "vertical" and hasattr(self, 'add_h_guide_btn') and self.add_h_guide_btn != button_pressed:
            self.add_h_guide_btn.state(['!pressed', '!focus'])
        elif mode == "horizontal" and hasattr(self, 'add_v_guide_btn') and self.add_v_guide_btn != button_pressed:
            self.add_v_guide_btn.state(['!pressed', '!focus'])

    def draw_grid(self):
        """Draws the grid lines on the canvas based on the current settings."""
        if not self.canvas: return
        grid_size = self.settings.get("grid_size", DEFAULT_GRID_SIZE)
        grid_color = self.settings.get("grid_color", "#d3d3d3")
        if grid_size <= 0: return

        canvas_width_screen = self.canvas.winfo_width()
        canvas_height_screen = self.canvas.winfo_height()

        # Get the visible world coordinates
        world_x_start, world_y_start = self.canvas_to_world_coords(0, 0)
        world_x_end, world_y_end = self.canvas_to_world_coords(canvas_width_screen, canvas_height_screen)

        # Adjust start coordinates to the nearest lower grid line
        start_grid_x_world = int(world_x_start / grid_size) * grid_size
        start_grid_y_world = int(world_y_start / grid_size) * grid_size

        # Vertical lines
        for world_x in range(start_grid_x_world, int(world_x_end) + grid_size, grid_size):
            canvas_x, _ = self.world_to_canvas_coords(world_x, world_y_start)
            # Draw line across the current visible canvas height, adjusted for ruler if present
            line_y_start_on_canvas = self.ruler_thickness if self.settings.get("show_rulers", False) else 0
            self.canvas.create_line(canvas_x, line_y_start_on_canvas, canvas_x, canvas_height_screen,
                                    fill=grid_color, tags="grid_line", width=1, dash=(2,4))

        # Horizontal lines
        for world_y in range(start_grid_y_world, int(world_y_end) + grid_size, grid_size):
            _, canvas_y = self.world_to_canvas_coords(world_x_start, world_y)
            # Draw line across the current visible canvas width, adjusted for ruler if present
            line_x_start_on_canvas = self.ruler_thickness if self.settings.get("show_rulers", False) else 0
            self.canvas.create_line(line_x_start_on_canvas, canvas_y, canvas_width_screen, canvas_y,
                                    fill=grid_color, tags="grid_line", width=1, dash=(2,4))


    def toggle_rulers_visibility(self):
        """Toggles the visibility of the rulers on the canvas."""
        self.settings["show_rulers"] = not self.settings.get("show_rulers", False)

        if not self.settings["show_rulers"]: # Rulers are being hidden
            self.active_ruler_guide_coord_x = None # Always cancel pending guide placement
            self.active_ruler_guide_coord_y = None
            if not self.settings.get("guides_stay_when_rulers_hidden", True):
                self.clear_temporary_guides() # Clear data and canvas items
            else:
                # Keep data, just delete canvas items and nullify canvas_id
                if self.canvas:
                    for guide_info in self.temporary_guides:
                        if guide_info.get('canvas_id') is not None:
                            self.canvas.delete(guide_info['canvas_id'])
                            guide_info['canvas_id'] = None

        self.draw_all_items() # This will redraw rulers if shown, and guides if data exists and rulers shown
        self.update_toggle_rulers_button_text()
        self.update_status(f"Rulers {'shown' if self.settings['show_rulers'] else 'hidden'}.")

    def update_toggle_rulers_button_text(self):
        """Updates the text of the 'Toggle Rulers' button."""
        if hasattr(self, 'toggle_rulers_btn'):
            text = "Hide Rulers" if self.settings.get("show_rulers", False) else "Show Rulers"
            self.toggle_rulers_btn.config(text=text)

    def draw_rulers(self):
        """Draws the horizontal and vertical rulers on the canvas."""
        if not self.canvas: return
        # Horizontal Ruler (Top)
        self.canvas.create_rectangle(0, 0, self.canvas.winfo_width(), self.ruler_thickness,
                                    #  fill=self.ruler_bg_color,
                                     outline=self.ruler_line_color, tags="ruler_bg")
        # Vertical Ruler (Left)
        self.canvas.create_rectangle(0, self.ruler_thickness, self.ruler_thickness, self.canvas.winfo_height(),
                                    #  fill=self.ruler_bg_color, 
                                     outline=self.ruler_line_color, tags="ruler_bg")

        # Markings
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Determine visible world coordinates
        world_x_start, world_y_start = self.canvas_to_world_coords(0,0)
        world_x_end, world_y_end = self.canvas_to_world_coords(canvas_width, canvas_height)

        # Adjust for ruler thickness when calculating visible world range for markings
        world_x_for_hruler_start, _ = self.canvas_to_world_coords(self.ruler_thickness, self.ruler_thickness)
        world_x_for_hruler_end, _ = self.canvas_to_world_coords(canvas_width, self.ruler_thickness)

        _, world_y_for_vruler_start = self.canvas_to_world_coords(self.ruler_thickness, self.ruler_thickness)
        _, world_y_for_vruler_end = self.canvas_to_world_coords(self.ruler_thickness, canvas_height)


        # Dynamic interval based on zoom - simplified
        interval = 50
        if self.current_zoom_level < 0.5: interval = 100
        elif self.current_zoom_level > 2: interval = 20

        # Horizontal Markings
        start_mark_x = int(world_x_for_hruler_start / interval) * interval
        for world_x in range(start_mark_x, int(world_x_for_hruler_end) + interval, interval):
            canvas_x, _ = self.world_to_canvas_coords(world_x, world_y_start) # Use world_y_start for consistency
            if canvas_x >= self.ruler_thickness and canvas_x <= canvas_width:
                tick_len = 5 if world_x % (interval * 2) != 0 else 10
                self.canvas.create_line(canvas_x, self.ruler_thickness - tick_len, canvas_x, self.ruler_thickness,
                                        fill=self.ruler_line_color, tags="ruler_marking")
                if tick_len == 10:
                    self.canvas.create_text(canvas_x, self.ruler_thickness - tick_len - 5, text=str(world_x),
                                            fill=self.ruler_text_color, anchor=tk.S, tags="ruler_marking_text", font=(DEFAULT_FONT_FAMILY, 8))
        # Vertical Markings
        start_mark_y = int(world_y_for_vruler_start / interval) * interval
        for world_y in range(start_mark_y, int(world_y_for_vruler_end) + interval, interval):
            _, canvas_y = self.world_to_canvas_coords(world_x_start, world_y) # Use world_x_start for consistency
            if canvas_y >= self.ruler_thickness and canvas_y <= canvas_height:
                tick_len = 5 if world_y % (interval * 2) != 0 else 10
                self.canvas.create_line(self.ruler_thickness - tick_len, canvas_y, self.ruler_thickness, canvas_y,
                                        fill=self.ruler_line_color, tags="ruler_marking")
                if tick_len == 10:
                    self.canvas.create_text(self.ruler_thickness - tick_len - 5, canvas_y, text=str(world_y),
                                            fill=self.ruler_text_color, anchor=tk.E, tags="ruler_marking_text", font=(DEFAULT_FONT_FAMILY, 8))

    def draw_temporary_guides(self):
        """Draws temporary guides on the canvas."""
        if not self.canvas: return
        self.canvas.delete("temporary_guide") # Clear old guides before redrawing

        # Redraw persistent guides based on self.temporary_guides list
        # Note: This loop is for redrawing guides that were previously added and stored.
        # The actual 'canvas_id' stored in the dictionary is not used here for redrawing,
        # as we are clearing all "temporary_guide" tagged items and redrawing.
        # If we wanted to selectively update/remove, canvas_id would be useful.
        for guide_info in self.temporary_guides:
            guide_type = guide_info['type']
            world_coord = guide_info['world_coord']

            guide_canvas_id = None
            if guide_type == 'h': # Horizontal guide
                # Convert world_coord (y) to current screen coordinates
                _, screen_y = self.world_to_canvas_coords(0, world_coord) # x doesn't matter for horizontal line screen y
                guide_canvas_id = self.canvas.create_line(0, screen_y, self.canvas.winfo_width(), screen_y,
                                                          fill=self.guide_line_color, tags=("temporary_guide", guide_info.get('id', 'unknown_guide')), width=1, dash=(4, 2))
            elif guide_type == 'v': # Vertical guide
                # Convert world_coord (x) to current screen coordinates
                screen_x, _ = self.world_to_canvas_coords(world_coord, 0) # y doesn't matter for vertical line screen x
                guide_canvas_id = self.canvas.create_line(screen_x, 0, screen_x, self.canvas.winfo_height(),
                                                          fill=self.guide_line_color, tags=("temporary_guide", guide_info.get('id', 'unknown_guide')), width=1, dash=(4, 2))
            if guide_canvas_id:
                guide_info['canvas_id'] = guide_canvas_id # Store the canvas ID

    def clear_temporary_guides(self):
        """Clears all temporary guides from the canvas and internal list."""
        self.temporary_guides.clear()
        if self.canvas:
            self.canvas.delete("temporary_guide")


    def _calculate_quiz_score_percentage(self, log_entry):
        """
        Calculates the score percentage for a given quiz log entry.

        This handles both live quiz session scores and manually logged quiz scores.

        Args:
            log_entry (dict): The quiz log entry dictionary.

        Returns:
            float or None: The calculated score percentage, or None if it cannot be calculated.
        """
        if not log_entry or log_entry.get("type") != "quiz":
            return None

        marks_data = log_entry.get("marks_data", {})
        num_questions = log_entry.get("num_questions", 0)
        score_details = log_entry.get("score_details") # For live quiz sessions

        if num_questions <= 0 and not score_details: # Cannot calculate percentage if no questions or score details
            return None

        # Handle live quiz session scores first
        if score_details and isinstance(score_details, dict):
            correct = score_details.get("correct", 0)
            total_asked = score_details.get("total_asked", 0)
            if total_asked > 0:
                return (correct / total_asked) * 100
            return 0 # Or None if no questions asked yet

        # Handle manually logged quiz scores with marks_data
        if not marks_data or num_questions <= 0: # Need marks_data and num_questions for this path
             return None

        total_earned_points = 0
        total_possible_points_main = 0 # Points from questions that contribute to the main total (not bonus)

        quiz_mark_types_settings = self.settings.get("quiz_mark_types", DEFAULT_QUIZ_MARK_TYPES)

        # Determine the point value of a single "fully correct" non-bonus question.
        # This is used as the basis for the percentage calculation if num_questions is the primary driver.
        # A common approach is to find the "correct" mark type.
        default_points_per_main_question = 1 # Fallback
        correct_mark_type = next((mt for mt in quiz_mark_types_settings if mt.get("id") == "mark_correct" and mt.get("contributes_to_total")), None)
        if correct_mark_type:
            default_points_per_main_question = correct_mark_type.get("default_points", 1)

        total_possible_points_main = num_questions * default_points_per_main_question

        for mark_id, count in marks_data.items():
            if not isinstance(count, (int, float)) or count == 0:
                continue # Skip if count is not a number or zero

            mark_config = next((mt for mt in quiz_mark_types_settings if mt.get("id") == mark_id), None)
            if not mark_config:
                continue

            points_for_this_mark_type = count * mark_config.get("default_points", 0)

            if not mark_config.get("is_extra_credit", False):
                # Only add to total_earned_points if it's not extra credit,
                # as extra credit is handled separately to potentially exceed 100%.
                # This logic assumes that points for main questions are summed up here.
                total_earned_points += points_for_this_mark_type
            else: # Is extra credit
                total_earned_points += points_for_this_mark_type # Add extra credit to earned points

        if total_possible_points_main > 0:
            return (total_earned_points / total_possible_points_main) * 100
        elif total_earned_points > 0 : # e.g. only extra credit was scored, and no main possible points
            return 100.0 # Or handle as a special case, like "Bonus Achieved"

        return 0.0 # Default to 0% if no points possible or earned meaningfully


    def handle_layout_collision(self, moved_item_id):
        """
        Detects and resolves layout collisions by shifting items vertically.

        When an item is moved and overlaps with another, this function shifts the lower
        item down to resolve the overlap.

        Args:
            moved_item_id (str): The ID of the item that was just moved.
        """
        # ... (same as v51)
        if moved_item_id not in self.students: return
        moved_item_data = self.students[moved_item_id]
        moved_x1, moved_y1 = moved_item_data['x'], moved_item_data['y']
        moved_w = moved_item_data.get('_current_world_width', moved_item_data.get('width', DEFAULT_STUDENT_BOX_WIDTH))
        moved_h = moved_item_data.get('_current_world_height', moved_item_data.get('height', DEFAULT_STUDENT_BOX_HEIGHT))
        moved_x2, moved_y2 = moved_x1 + moved_w, moved_y1 + moved_h
        items_to_shift_data = []
        all_other_items = []
        for sid, sdata in self.students.items():
            if sid != moved_item_id: all_other_items.append({'id': sid, 'type': 'student', 'data': sdata})
        for fid, fdata in self.furniture.items(): all_other_items.append({'id': fid, 'type': 'furniture', 'data': fdata})
        for other_item_info in all_other_items:
            other_id, other_data = other_item_info['id'], other_item_info['data']
            other_x1, other_y1 = other_data['x'], other_data['y']
            other_w = other_data.get('_current_world_width', other_data.get('width', DEFAULT_STUDENT_BOX_WIDTH))
            other_h = other_data.get('_current_world_height', other_data.get('height', DEFAULT_STUDENT_BOX_HEIGHT))
            other_x2, other_y2 = other_x1 + other_w, other_y1 + other_h
            is_colliding = not (moved_x2 <= other_x1 or moved_x1 >= other_x2 or moved_y2 <= other_y1 or moved_y1 >= other_y2)
            if is_colliding:
                vertical_overlap = moved_y2 - other_y1
                if vertical_overlap > 0 :
                    shift_by = vertical_overlap + LAYOUT_COLLISION_OFFSET
                    items_to_shift_data.append({'id': other_id, 'type': other_item_info['type'], 'old_x': other_x1, 'old_y': other_y1, 'new_x': other_x1, 'new_y': other_y1 + shift_by})
        if items_to_shift_data:
            self.execute_command(MoveItemsCommand(self, items_to_shift_data))
            self.update_status(f"Adjusted layout for {len(items_to_shift_data)} items due to overlap with {moved_item_data['full_name']}.")

    """def world_to_canvas_coords(self, world_x, world_y):
        return world_x * self.current_zoom_level, world_y * self.current_zoom_level"""
    def world_to_canvas_coords(self, world_x, world_y):
        """
        Converts world coordinates to the "infinite" virtual canvas coordinates
        for drawing. This is the forward transformation.
        """
        canvas_x = (world_x * self.current_zoom_level) + self.pan_x
        canvas_y = (world_y * self.current_zoom_level) + self.pan_y
        return canvas_x, canvas_y
    
    def world_to_canvas_coords_guides(self, world_x, world_y):
        """
        Converts world coordinates to the "infinite" virtual canvas coordinates
        for drawing. This is the forward transformation.
        """
        canvas_x = (world_x * self.current_zoom_level) + self.pan_x
        canvas_y = (world_y * self.current_zoom_level) + self.pan_y
        return canvas_x, canvas_y
    
    """
    def canvas_to_world_coords(self, canvas_x_on_screen, canvas_y_on_screen):
        
        
        if self.current_zoom_level == 0: return canvas_x_on_screen, canvas_y_on_screen
        
        #if not self.canvas.isscrolled(): return canvas_x_on_screen, canvas_y_on_screen
        
        
        true_canvas_x = self.canvas.canvasx(canvas_x_on_screen)
        true_canvas_y = self.canvas.canvasy(canvas_y_on_screen)
        return true_canvas_x / self.current_zoom_level, true_canvas_y / self.current_zoom_level
        
        
        true_canvas_x = self.canvas.canvasx(canvas_x_on_screen)
        true_canvas_y = self.canvas.canvasy(canvas_y_on_screen)
        
        # Divide by the current zoom level to convert canvas coordinates to world coordinates.
        # This single logic path should handle scrolled, unscrolled, zoomed, and unzoomed cases.
        return true_canvas_x / self.current_zoom_level, true_canvas_y / self.current_zoom_level
    
    """
    
    def canvas_to_world_coords(self, screen_x, screen_y):
        """
        Converts screen coordinates to world coordinates, accounting for
        pan, zoom, and canvas scrolling.
        """
        # Step 1: Account for canvas scrolling (if any)
        # This gives the coordinate on the "infinite" virtual canvas
        true_canvas_x = self.canvas.canvasx(screen_x)
        true_canvas_y = self.canvas.canvasy(screen_y)

        # Step 2: Account for panning and zooming (the inverse of drawing)
        # This is the crucial step you were missing.
        world_x = (true_canvas_x - self.pan_x) / self.zoom_level
        world_y = (true_canvas_y - self.pan_y) / self.zoom_level

        return world_x, world_y
    
    def canvas_to_world_coords_guides(self, screen_x, screen_y):
        """
        Converts screen coordinates to world coordinates, accounting for
        pan, zoom, and canvas scrolling.
        """
        # Step 1: Account for canvas scrolling (if any)
        # This gives the coordinate on the "infinite" virtual canvas
        true_canvas_x = self.canvas.canvasx(screen_x)
        true_canvas_y = self.canvas.canvasy(screen_y)

        # Step 2: Account for panning and zooming (the inverse of drawing)
        # This is the crucial step you were missing.
        world_x = (true_canvas_x - self.pan_x) / self.current_zoom_level
        world_y = (true_canvas_y - self.pan_y) / self.current_zoom_level

        return world_x, world_y
    

    def update_zoom_display(self):
        """Updates the zoom level display in the UI."""
        if hasattr(self, 'zoom_display_label') and self.zoom_display_label:
            if self.settings.get("show_zoom_level_display", True):
                #self.zoom_display_label.config(text=f"{self.current_zoom_level*100:.0f}%")
                self.zoom_var.set(value=str(self.current_zoom_level*100.0))
                if not self.zoom_display_label.winfo_ismapped():
                    zoom_in_btn = next((child for child in self.zoom_display_label.master.winfo_children() if isinstance(child, ttk.Button) and "Zoom In" in child.cget("text")), None)
                    if zoom_in_btn: self.zoom_display_label.pack(side=tk.LEFT, padx=1, after=zoom_in_btn)
                    else: self.zoom_display_label.pack(side=tk.LEFT, padx=1)
            elif self.zoom_display_label.winfo_ismapped(): self.zoom_display_label.pack_forget()

    def update_zoom_display2(self):
        """Updates the zoom level from the entry widget."""
        #print("Return")
        self.current_zoom_level = float(self.zoom_var.get())/100.0
        self.zoom_var.set(value=str(float(self.current_zoom_level)*100.0))
        self.zoom_canvas(1)

    def zoom_canvas(self, factor):
        """
        Zooms the canvas in or out by a given factor.

        Args:
            factor (float): The zoom factor. > 1 for zoom in, < 1 for zoom out. 0 resets zoom.
        """
        # ... (same as v51)
        if self.password_manager.is_locked: return
        world_center_x_before, world_center_y_before = self.canvas_to_world_coords(self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2)
        if factor == 0: self.current_zoom_level = 1.0
        else: self.current_zoom_level = max(0.1, min(self.current_zoom_level * factor, 10.0))
        self.draw_all_items(check_collisions_on_redraw=False)
        # Centering logic after zoom could be added here if desired, similar to v50/v51
        self.update_status(f"Zoom level: {self.current_zoom_level:.2f}x"); self.update_zoom_display(); self.password_manager.record_activity()
        self.zoom_var.set(value=str(self.current_zoom_level*100.0))
        self.zoom_display_label.configure(textvariable=self.zoom_var)
        #print(self.zoom_var.get())

    def on_mousewheel_zoom(self, event):
        """Handles zooming with Ctrl + Mouse Wheel."""
        if self.password_manager.is_locked: return
        factor = 0.9 if (event.num == 5 or event.delta < 0) else 1.1
        self.zoom_canvas(factor)
    def on_pan_start(self, event):
        """
        Initiates canvas panning on middle-click.
        """
        # ... (same as v51)
        if self.password_manager.is_locked: return
        world_event_x, world_event_y = self.canvas_to_world_coords(event.x, event.y)
        item_ids_under_cursor = self.canvas.find_overlapping(event.x-1, event.y-1, event.x+1, event.y+1) # Use screen coords for find_overlapping
        clicked_on_item = False
        for item_canvas_id in item_ids_under_cursor:
            tags = self.canvas.gettags(item_canvas_id)
            if any(t.startswith("student_") or t.startswith("furniture_") for t in tags if "rect" in tags or "resize_handle" in tags):
                clicked_on_item = True; break
        if not clicked_on_item:
            self.canvas.scan_mark(event.x, event.y); self.update_status("Panning canvas..."); self._drag_started_on_item = False
        else: self._drag_started_on_item = True
        self.password_manager.record_activity()

    def on_pan_move(self, event):
        """Handles canvas panning movement."""
        if self.password_manager.is_locked: return
        if not self._drag_started_on_item: self.canvas.scan_dragto(event.x, event.y, gain=1)
        self.password_manager.record_activity()
    def on_pan_end(self, event):
        """Finalizes canvas panning."""
        if self.password_manager.is_locked: return
        if not self._drag_started_on_item: self.update_status("Canvas panned.")
        self._drag_started_on_item = False; self.password_manager.record_activity()
    def on_canvas_ctrl_click(self, event):
        """Handles Ctrl + Left-click for multi-selecting items."""
        # ... (same as v51)
        if self.password_manager.is_locked:
            if not self.prompt_for_password("Unlock to Select", "Enter password to select items:"): return
        world_click_x, world_click_y = self.canvas_to_world_coords(event.x, event.y)
        item_canvas_ids = self.canvas.find_overlapping(world_click_x -1, world_click_y -1, world_click_x +1, world_click_y+1) # Use screen coords
        topmost_item_id, topmost_item_type = None, None
        for item_c_id in reversed(item_canvas_ids):
            tags = self.canvas.gettags(item_c_id); current_item_id, current_item_type = None, None
            for tag in tags:
                if tag.startswith("student_") and tag in self.students: current_item_id, current_item_type = tag, "student"; break
                elif tag.startswith("furniture_") and tag in self.furniture: current_item_id, current_item_type = tag, "furniture"; break
            if current_item_id and any("rect" in t for t in tags): topmost_item_id, topmost_item_type = current_item_id, current_item_type; break
        if topmost_item_id:
            if topmost_item_id in self.selected_items: self.selected_items.remove(topmost_item_id)
            else: self.selected_items.add(topmost_item_id)
            if topmost_item_type == "student": self.draw_single_student(topmost_item_id)
            elif topmost_item_type == "furniture": self.draw_single_furniture(topmost_item_id)
            self.update_status(f"{len(self.selected_items)} items selected.")
        self.password_manager.record_activity()

    def _get_guide_at_canvas_coords(self, event_x, event_y, tolerance=10):
        """
        Checks if a click at canvas coordinates (event_x, event_y) is on/near a guide.
        Returns the ID of the guide if hit, otherwise None.
        Uses a tolerance for easier clicking.
        """
        for guide_info in reversed(self.guides): # Check topmost guides first
            if self.guides[guide_info].get('canvas_item_id') is None: #guide_info.get('canvas_item_id') is None:
                continue # Guide not drawn or ID missing

            # Get current screen coordinates of the guide line
            # For Tkinter, self.canvas.coords(item_id) returns [x1, y1, x2, y2]
            try:
                coords = self.canvas.coords(self.guides[guide_info].get('canvas_item_id')) #guide_info['canvas_item_id'])
                if not coords: continue
            except tk.TclError: # Item might have been deleted unexpectedly
                continue

            guide_type = self.guides[guide_info].get('type')#guide_info['type']

            if guide_type == 'h': # Horizontal guide
                # coords are [x1, y1, x2, y1] - check y-coordinate proximity
                guide_screen_y = coords[1]
                if abs(event_y - guide_screen_y) < tolerance and \
                   min(coords[0], coords[2]) <= event_x <= max(coords[0], coords[2]):
                    return self.guides[guide_info].get('id') #guide_info['id']
            elif guide_type == 'v': # Vertical guide
                # coords are [x1, y1, x1, y2] - check x-coordinate proximity
                guide_screen_x = coords[0]
                if abs(event_x - guide_screen_x) < tolerance and \
                   min(coords[1], coords[3]) <= event_y <= max(coords[1], coords[3]):
                    return self.guides[guide_info].get('id') #guide_info['id']
        return None

    def on_canvas_left_press(self, event):
        """
        Handles the initial left-click on the canvas.

        This method is the starting point for various interactions: selecting items,
        initiating a drag/resize, placing guides, etc.
        """
        if self.password_manager.is_locked:
            if not self.prompt_for_password("Unlock to Interact", "Enter password to interact with canvas:"): return
        self.canvas.focus_set()

        # Check if dragging is allowed # This is obsolete (I removed it's function)
        #if not self.settings.get("allow_box_dragging", True):
        # ... (code for handling clicks when dragging is disabled) ...

        x_coords = event.x; y_coords = event.y
        world_event_x, world_event_y = self.canvas_to_world_coords(event.x, event.y)
        # Guide Creation via Add Guide Mode
        if self.add_guide_mode:
            # ... (code for adding guides) ...
            return # Consume event

        # Check for guide dragging
        if not self.add_guide_mode:
            clicked_guide_id = self._get_guide_at_canvas_coords(world_event_x, world_event_y)
            if clicked_guide_id:
                # ... (code for initiating guide drag) ...
                return # Consume event, guide drag initiated

        # Ruler interaction
        if self.settings.get("show_rulers", False) and not self.add_guide_mode:
            # ... (code for placing guides via rulers) ...
            return # Consume click

        # Place active guide if pending
        if self.active_ruler_guide_coord_x is not None or self.active_ruler_guide_coord_y is not None:
            # ... (code for placing pending guide) ...
            return # Consume click

        # Item interaction (selection, drag, resize)
        world_event_x, world_event_y = self.canvas_to_world_coords(event.x, event.y)
        self.drag_data = {"x": world_event_x, "y": world_event_y, "item_id": None, "item_type": None,
                          "start_x_world": world_event_x, "start_y_world": world_event_y,
                          "original_positions": {}, "is_resizing": False, "resize_handle_corner": None,
                          "original_size_world": {}}
        self._potential_click_target = None; self._drag_started_on_item = False

        if self.edit_mode_var.get():
            # ... (code for initiating resize) ...
            return

        # ... (code for item selection and initiating move) ...
        self.password_manager.record_activity()

    def on_canvas_drag(self, event):
        """
        Handles the drag motion on the canvas.

        This method is responsible for moving or resizing items/guides based on the
        information stored in `self.drag_data` from `on_canvas_left_press`.
        """
        if self.password_manager.is_locked: return

        # ... (logic for dragging guides) ...

        if self.drag_data.get('is_dragging_guide'):
            # ... (guide dragging implementation) ...
            return

        # ... (logic for moving/resizing items) ...

        if not self.drag_data.get("item_id") or not self._drag_started_on_item: return

        world_event_x, world_event_y = self.canvas_to_world_coords(event.x, event.y)

        if self.drag_data.get("is_resizing"):
            # ... (resizing implementation) ...
        else: # Moving
            # ... (moving implementation) ...

        self.drag_data["x"] = world_event_x # Update last world position for next delta
        self.drag_data["y"] = world_event_y
        self.password_manager.record_activity()

    def on_canvas_release(self, event):
        """
        Handles the release of the left mouse button on the canvas.

        This method finalizes actions like moving, resizing, or clicking. It creates
        and executes the appropriate command objects for undo/redo functionality.
        """
        if self.password_manager.is_locked: return

        # ... (logic to finalize guide drag) ...

        clicked_item_id_at_press = self._potential_click_target
        dragged_item_id = self.drag_data.get("item_id")
        was_resizing = self.drag_data.get("is_resizing", False)
        actual_drag_initiated = self.drag_data.get("_actual_drag_initiated", False)
        world_event_x, world_event_y = self.canvas_to_world_coords(event.x, event.y)

        if was_resizing and dragged_item_id:
            # ... (finalize resize and create ChangeItemsSizeCommand) ...
        elif clicked_item_id_at_press and not actual_drag_initiated:
            # ... (handle item click/tap for logging) ...
        elif actual_drag_initiated and dragged_item_id and not was_resizing:
            # ... (finalize move and create MoveItemsCommand) ...
            
        self.drag_data.clear(); self._potential_click_target = None; self._drag_started_on_item = False; self.password_manager.record_activity()

    def on_canvas_right_press(self, event):
        """
        Handles right-clicks on the canvas to show context menus.
        """
        # ... (logic to determine what was clicked and show the appropriate context menu) ...
        if self.password_manager.is_locked:
            if not self.prompt_for_password("Unlock to Open Menu", "Enter password to open context menu:"): return
        self.canvas.focus_set()
        world_event_x, world_event_y = self.canvas_to_world_coords(event.x, event.y)
        item_canvas_ids_context = self.canvas.find_overlapping(world_event_x -1, world_event_y -1, world_event_x +1, world_event_y +1) # Screen coords
        context_item_id, context_item_type = None, None
        for item_c_id in reversed(item_canvas_ids_context):
            tags = self.canvas.gettags(item_c_id); temp_id, temp_type, is_main_rect = None, None, False
            i=0
            for tag in tags:
                if tag.startswith("student_") and tag in self.students: temp_id, temp_type = tag, "student"
                elif tag.startswith("furniture_") and tag in self.furniture: temp_id, temp_type = tag, "furniture"
                elif tag.startswith("guide") and self.is_in_guides(tag): temp_id, temp_type = tag, "guide"; context_item_id = "guide"
                elif tag == ("current"): 
                    temp_id, temp_type = tags[1], "guide"
                    context_item_id = "guide"
                    break
                if "rect" in tag: is_main_rect = True
                i+=1
            if temp_id and is_main_rect: context_item_id, context_item_type = temp_id, temp_type; break
        if context_item_id:
            if context_item_id not in self.selected_items:
                self.deselect_all_items(); self.selected_items.add(context_item_id)
                if context_item_type == "student": self.draw_single_student(context_item_id)
                else: self.draw_single_furniture(context_item_id)
            if context_item_type == "student": self.show_student_context_menu(event, context_item_id)
            elif context_item_type == "furniture": self.show_furniture_context_menu(event, context_item_id)
            elif context_item_id == "guide":
                self.show_guide_context_menu(event, temp_id)
        else: self.show_general_context_menu(event)
        self.password_manager.record_activity()

    def show_general_context_menu(self, event):
        """Displays the general context menu for the canvas background."""
        # ... (implementation of general context menu) ...

    def show_student_context_menu(self, event, student_id):
        """Displays the context menu for a specific student."""
        # ... (implementation of student context menu) ...

    def show_furniture_context_menu(self, event, furniture_id):
        """Displays the context menu for a specific piece of furniture."""
        # ... (implementation of furniture context menu) ...

    def is_in_guides(self, tag):
        """Checks if a given tag corresponds to a guide."""
        for guide in self.guides:
            if self.guides[guide] == tag: return True
        return False
    
    def show_guide_context_menu(self, event, guide_id):
        """Displays the context menu for a guide."""
        # ... (implementation of guide context menu) ...

    def delete_guide(self, guide_id):
        """Deletes a specific guide."""
        # ... (implementation of guide deletion) ...

    def delete_all_guides(self):
        """Deletes all guides from the canvas."""
        # ... (implementation of deleting all guides) ...

    def _select_items_by_type(self, item_type_key):
        """
        Selects all items of a given type ("students", "furniture", or "all").
        """
        # ... (implementation of item selection) ...

    def select_all_students(self): self._select_items_by_type("students")
    def select_all_furniture(self): self._select_items_by_type("furniture")
    def select_all_items(self): self._select_items_by_type("all")
    
    def deselect_all_items(self):
        """Deselects all currently selected items."""
        # ... (implementation of deselection) ...

    def change_item_size_dialog(self, item_id, item_type):
        """Opens a dialog to change the size of a single item."""
        # ... (implementation of size change dialog) ...

    def change_size_selected_dialog(self):
        """Opens a dialog to change the size of all selected items."""
        # ... (implementation of bulk size change dialog) ...

    def edit_student_dialog(self, student_id):
        """Opens the dialog to edit a student's details."""
        # ... (implementation of student edit dialog) ...

    def edit_furniture_dialog(self, furniture_id):
        """Opens the dialog to edit a furniture item's details."""
        # ... (implementation of furniture edit dialog) ...

    def customize_student_style_dialog(self, student_id):
        """Opens the dialog to customize a student's box style."""
        # ... (implementation of style customization dialog) ...

    def delete_student_confirm(self, student_id):
        """Confirms and deletes a student and their associated logs."""
        # ... (implementation of student deletion) ...

    def delete_furniture_confirm(self, furniture_id):
        """Confirms and deletes a piece of furniture."""
        # ... (implementation of furniture deletion) ...

    def delete_selected_items_confirm(self):
        """Confirms and deletes all selected items."""
        # ... (implementation of bulk deletion) ...

    def log_behavior_dialog(self, student_id):
        """Opens the dialog to log a behavior for a student."""
        # ... (implementation of behavior logging dialog) ...

    def log_homework_dialog(self, student_id):
        """
        Handles manual homework logging, showing either a simplified or detailed dialog
        based on settings.
        """
        # ... (implementation of homework logging dialog) ...

    def log_quiz_score_dialog(self, student_id):
        """Opens the dialog to log a quiz score for a student."""
        # ... (implementation of quiz score dialog) ...
    
    def save_data_wrapper(self, event=None, source="manual"):
        """
        Saves all application data to their respective files.

        This is a central save function called from various points in the application.

        Args:
            event: The event that triggered the save (optional).
            source (str): A string indicating the source of the save call for debugging.
        """
        # ... (implementation of saving all data) ...

    def _update_toggle_dragging_button_text(self):
        """Updates the text of the 'Enable/Disable Dragging' button."""
        if hasattr(self, 'toggle_dragging_btn'):
            if self.settings.get("allow_box_dragging", True):
                self.toggle_dragging_btn.config(text="Disable Dragging")
            else:
                self.toggle_dragging_btn.config(text="Enable Dragging")

    def toggle_dragging_allowed(self):
        """Toggles the setting that allows or disallows dragging of items."""
        if self.password_manager.is_locked:
            if not self.prompt_for_password("Unlock to Toggle Dragging", "Enter password to toggle dragging:"): return

        current_setting = self.settings.get("allow_box_dragging", True)
        self.settings["allow_box_dragging"] = not current_setting
        self._update_toggle_dragging_button_text()
        self.update_status(f"Box dragging {'enabled' if self.settings['allow_box_dragging'] else 'disabled'}.")
        self.save_data_wrapper(source="toggle_dragging_button") # Save settings immediately
        self.password_manager.record_activity()
    
    def load_data(self, file_path=None, is_restore=False):
        """
        Loads all application data from files.

        This function handles loading the main data file, which includes students, furniture,
        logs, and settings. It also triggers data migration if loading from an older version.

        Args:
            file_path (str, optional): The specific file path to load from. Defaults to the standard data file.
            is_restore (bool): True if this load is part of a backup restore operation.
        """
        # ... (implementation of loading all data, including migration calls) ...

    def _migrate_v8_data(self, data):
        """Migrates data from version 8 to 9."""
        # ... (implementation of v8 to v9 migration) ...

    def _migrate_v9_data(self, data):
        """Migrates data from version 9 to 10."""
        # ... (implementation of v9 to v10 migration) ...

    # ... (other migration functions as needed) ...

    def autosave_data_wrapper(self):
        """
        Wrapper for autosaving data at regular intervals. Also triggers Excel autosave if enabled.
        """
        self.save_data_wrapper(source="autosave")
        if hasattr(self, 'autosave_excel_log') and callable(self.autosave_excel_log):
             self.autosave_excel_log()
        self.root.after(self.settings.get("autosave_interval_ms", 30000), self.autosave_data_wrapper)

    def autosave_excel_log(self):
        """Autosaves the log data to an Excel file if the feature is enabled."""
        # ... (implementation of Excel autosave) ...
    
    def load_custom_behaviors(self):
        """Loads custom behaviors from their dedicated file."""
        # ... (implementation of loading custom behaviors) ...
    def save_custom_behaviors(self):
        """Saves custom behaviors to their dedicated file."""
        # ... (implementation of saving custom behaviors) ...
    
    # ... (load/save functions for all other custom data types: homework types, statuses, groups, templates) ...

    def update_all_behaviors(self):
        """Updates the combined list of default and custom behaviors."""
        # ... (implementation of updating all behaviors list) ...
    
    # ... (update functions for all other custom data types) ...
   
    def get_earliest_log_date(self, type):
        """
        Finds the earliest date from all log entries.

        Args:
            type (str): The part of the date to return ('y', 'm', or 'd').

        Returns:
            str: The year, month, or day of the earliest log entry.
        """
        # ... (implementation of finding earliest log date) ...
    
    def export_log_dialog_with_filter(self, export_type="xlsx"):
        """
        Opens a dialog with filtering options before exporting log data.

        Args:
            export_type (str): The format to export to ("xlsx", "xlsm", "csv").
        """
        # ... (implementation of export filter dialog) ...

    def _make_safe_sheet_name(self, name_str, id_fallback="Sheet"):
        """
        Sanitizes a string to be a valid Excel sheet name.
        """
        invalid_chars = r'[\\/?*\[\]:]'
        safe_name = re.sub(invalid_chars, '_', str(name_str))
        if not safe_name: safe_name = str(id_fallback)
        return safe_name[:31]

    def export_data_to_excel(self, file_path, export_format="xlsx", filter_settings=None, is_autosave=False, export_all_students_info = True):
        """
        Exports filtered log data to an Excel file.

        Args:
            file_path (str): The path to save the Excel file to.
            export_format (str): The Excel format ("xlsx" or "xlsm").
            filter_settings (dict): A dictionary of filter settings from the export dialog.
            is_autosave (bool): True if this is an automated autosave.
            export_all_students_info (bool): If True, includes sheets for individual students and a student info sheet.
        """
        # ... (implementation of exporting data to Excel) ...

    def export_data_to_csv_zip(self, zip_file_path, filter_settings=None):
        """
        Exports filtered log data to a ZIP archive containing CSV files.

        Args:
            zip_file_path (str): The path to save the ZIP file to.
            filter_settings (dict): A dictionary of filter settings from the export dialog.
        """
        # ... (implementation of exporting data to CSV) ...

    def export_layout_as_image(self):
        """
        Exports the current canvas layout as an image file (e.g., PNG).
        """
        # ... (implementation of image export) ...
        
    def _import_data_from_excel_logic(self, file_path, import_incidents_flag, student_sheet_name_to_import):
        """
        Contains the core logic for importing student data and incidents from an Excel file.
        """
        # ... (implementation of Excel import logic) ...

    def import_students_from_excel_dialog(self):
        """Opens a dialog to select an Excel file and import options."""
        # ... (implementation of import dialog) ...

    def save_layout_template_dialog(self):
        """Opens a dialog to save the current layout as a template."""
        # ... (implementation of saving layout template) ...

    def load_layout_template_dialog(self):
        """Opens a dialog to load a layout from a template."""
        # ... (implementation of loading layout template) ...
    
    def generate_attendance_report_dialog(self):
        """Opens a dialog to generate an attendance report."""
        # ... (implementation of attendance report dialog) ...

    def generate_attendance_data(self, start_date, end_date, student_ids):
        """
        Generates attendance data based on log entries within a date range.

        Args:
            start_date (date): The start date for the report.
            end_date (date): The end date for the report.
            student_ids (list[str]): A list of student IDs to include.

        Returns:
            dict: A dictionary containing attendance data.
        """
        # ... (implementation of generating attendance data) ...

    def export_attendance_to_excel(self, file_path, attendance_data, report_start_date, report_end_date):
        """
        Exports the generated attendance data to an Excel file.

        Args:
            file_path (str): The path to save the Excel file to.
            attendance_data (dict): The attendance data to export.
            report_start_date (date): The start date of the report.
            report_end_date (date): The end date of the report.
        """
        # ... (implementation of exporting attendance data) ...

    def align_selected_items(self, edge):
        """
        Aligns selected items to a specified edge (top, bottom, left, right, etc.).

        Args:
            edge (str): The edge to align to.
        """
        # ... (implementation of item alignment) ...

    def distribute_selected_items_evenly(self, direction='horizontal'):
        """
        Distributes selected items evenly, either horizontally or vertically.

        Args:
            direction (str): The direction of distribution ('horizontal' or 'vertical').
        """
        # ... (implementation of item distribution) ...

    def assign_student_to_group_via_menu(self, student_id, group_id):
        """
        Assigns a single student to a group, typically from a context menu.
        """
        # ... (implementation of single student group assignment) ...

    def assign_students_to_group_via_menu(self, student_ids, group_id):
        """
        Assigns multiple students to a group.
        """
        # ... (implementation of bulk student group assignment) ...

    def manage_student_groups_dialog(self):
        """Opens the dialog for managing student groups."""
        # ... (implementation of group management dialog) ...

    def toggle_student_groups_ui_visibility(self):
        """Toggles the visibility of UI elements related to student groups."""
        # ... (implementation of toggling group UI) ...

    def toggle_manage_boxes_visibility(self):
        """Toggles the visibility of the layout tools toolbar."""
        # ... (implementation of toggling layout tools) ...
            
    def manage_quiz_templates_dialog(self):
        """Opens the dialog for managing quiz templates."""
        # ... (implementation of quiz template management dialog) ...

    def manage_homework_templates_dialog(self): # New
        """Opens the dialog for managing homework templates."""
        # ... (implementation of homework template management dialog) ...
    
    def set_theme(self, theme, canvas_color):
        """
        Sets the application's visual theme and canvas color.

        Args:
            theme (str): The name of the theme to apply (e.g., "Light", "Dark").
            canvas_color (str): The hex code for the canvas background color, or "Default".
        """
        # ... (implementation of setting theme) ...
    
    def _apply_canvas_color(self):
        """Applies the current canvas color based on theme and custom settings."""
        # ... (implementation of applying canvas color) ...
    
    def theme_set(self, theme=None):
        """Applies the selected theme to the application."""
        # ... (implementation of applying theme) ...
    
    def theme_auto(self, init=False):
        """
        Automatically sets the theme based on system settings (if applicable) and applies
        the correct canvas color.
        """
        # ... (implementation of auto theme setting) ...

    def open_settings_dialog(self):
        """Opens the main settings dialog."""
        # ... (implementation of opening settings dialog) ...
        

    def reset_application_dialog(self):
        """
        Shows a confirmation dialog before resetting the entire application to its default state.
        """
        # ... (implementation of reset confirmation dialog) ...

    def _perform_reset(self):
        """Performs the actual application reset, deleting all data."""
        # ... (implementation of application reset) ...

    def backup_all_data_dialog(self, force=False):
        """
        Opens a dialog to save a backup of all application data to a ZIP file.

        Args:
            force (bool): If True, performs the backup without showing a file dialog.
        """
        # ... (implementation of backup dialog) ...

    def restore_all_data_dialog(self):
        """
        Opens a dialog to restore application data from a backup ZIP file.
        """
        # ... (implementation of restore dialog) ...

    def open_data_folder(self):
        """Opens the application's data folder in the system's file explorer."""
        # ... (implementation of opening data folder) ...

    def open_last_export_folder(self):
        """Opens the folder where the last export was saved."""
        # ... (implementation of opening last export folder) ...

    def open_specific_export_folder(self, file_path_in_folder):
        """
        Opens the containing folder for a specific file path.

        Args:
            file_path_in_folder (str): The path to a file within the folder to open.
        """
        # ... (implementation of opening specific folder) ...

    def show_help_dialog(self):
        """Displays the Help & About dialog."""
        HelpDialog(self.root, APP_VERSION)

    def show_undo_history_dialog(self):
        """Displays the Undo History dialog."""
        # ... (implementation of showing undo history) ...

    def selective_redo_action(self, target_command_index_in_undo_stack):
        """
        Performs a selective redo, reverting to a specific point in the undo history.

        Args:
            target_command_index_in_undo_stack (int): The index of the command to revert to.
        """
        # ... (implementation of selective redo) ...

    def on_exit_protocol(self, force_quit=False):
        """
        Handles the application exit process, including saving data and confirming exit.

        Args:
            force_quit (bool): If True, exits without prompting the user.
        """
        # ... (implementation of exit protocol) ...

def perform_data_operations():
    """An example function that needs to write to the data file."""
    # Before you write to the file, unlock it.
    unlock_file(DATA_FILE)

    # Now you can safely write to the file
    try:
        with open(DATA_FILE, "a") as f:
            f.write("Adding new data during program execution.\n")
        print("Successfully wrote to data file.")
    except Exception as e:
        print(f"Failed to write to data file: {e}")
    
    # Note: We will lock the file in the 'finally' block of main()
    # to ensure it's always locked on exit.





# --- Main Execution ---
if __name__ == "__main__":
    try:
        import pyi_splash
        # You can optionally update the splash screen text as things load
        pyi_splash.update_text("Loading UI...")
    except ImportError:
        pyi_splash = None # Will be None when not running from a PyInstaller bundle

    root = tk.Tk()
    # Apply a theme if available and desired
    try:
        # Examples: 'clam', 'alt', 'default', 'classic'
        # Some themes might require python -m tkinter to see available ones on your system
        # Or use ttkthemes for more options: from ttkthemes import ThemedTk
        # root = ThemedTk(theme="arc") # Example using ttkthemes
        style = ttk.Style(root)
        #available_themes = style.theme_names() # ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative') on Windows
        # print("Available themes:", available_themes)
        sv_ttk.set_theme("Light")
        #if 'vista' in available_themes: style.theme_use('vista')
        #elif 'xpnative' in available_themes: style.theme_use('xpnative')

    except Exception as e_theme:
        print(f"Could not apply custom theme: {e_theme}")
        
    app = SeatingChartApp(root)
    
    try:
        t = threading.Thread(target=darkdetect.listener, args=(app.theme_auto, ))
        t.daemon = True
        t.start()
    except: pass

    # Close the splash screen once the main app is initialized and ready
    if pyi_splash:
        pyi_splash.close()

    root.mainloop()