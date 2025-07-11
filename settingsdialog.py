import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, colorchooser, font as tkfont

import os
import sys
from turtle import color
#from datetime import datetime, timedelta, date as datetime_date
#from openpyxl import Workbook, load_workbook
#from openpyxl.styles import Font as OpenpyxlFont, Alignment as OpenpyxlAlignment
#from openpyxl.utils import get_column_letter

from dialogs import PasswordPromptDialog, ConditionalFormattingRuleDialog
import other
from quizhomework import ManageInitialsDialog, ManageMarkTypesDialog, ManageLiveSelectOptionsDialog 
#from seatingchartmain import SeatingChartApp


# --- Application Constants ---
APP_NAME = "BehaviorLogger"
APP_VERSION = "v55.0" # Version incremented
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


class SettingsDialog(simpledialog.Dialog):
    def __init__(self, parent, current_settings, custom_behaviors, all_behaviors, app,
                 custom_homework_statuses, all_homework_statuses, # RENAMED
                 custom_homework_types, all_homework_types, # NEW
                 password_manager_instance, theme, custom_canvas_color, styles, style):
        self.settings = current_settings
        self.custom_behaviors_ref = custom_behaviors
        self.all_behaviors_ref = all_behaviors
        self.reset = False # Flag to indicate if reset button was pressed
        # NEW/RENAMED: References to the main app's lists
        self.custom_homework_statuses_ref = custom_homework_statuses
        self.all_homework_statuses_ref = all_homework_statuses
        self.custom_homework_types_ref = custom_homework_types
        self.all_homework_types_ref = all_homework_types
        
        self.app = app
        self.password_manager = password_manager_instance
        self.theme = tk.StringVar(value=theme)
        if style == "sun-valley-light" or style == "sun-valley-dark" or style == "sv_ttk":
            style = "sun-valley (Default)"
        self.style = tk.StringVar(value=style)
        self.theme2 = self.theme.get()
        self.styles = list(styles)
        for styl in self.styles:
            if "sun-valley" in styl:
                self.styles.remove(styl)                
        self.styles.append("sun-valley (Default)")
        self.custom_canvas_color = tk.StringVar(value= custom_canvas_color if custom_canvas_color != None else "Default")
        self.settings_changed_flag = False
        self.initial_settings_snapshot = {k: (v.copy() if isinstance(v, (dict, list)) else v) for k,v in current_settings.items()}
        super().__init__(parent, f"Settings - {APP_NAME}")

    def body(self, master):
        self.master_frame = master # Keep a reference for rebuilding tabs if needed
        self.notebook = ttk.Notebook(master)
        
        # --- General Tab ---
        general_tab = ttk.Frame(self.notebook, padding=10); self.notebook.add(general_tab, text="General")
        self.create_general_tab(general_tab)

        # --- Student Display Tab ---
        student_display_tab = ttk.Frame(self.notebook, padding=10); self.notebook.add(student_display_tab, text="Student Boxes")
        self.create_student_display_tab(student_display_tab)

        # --- Behavior/Quiz Log Tab ---
        behavior_log_tab = ttk.Frame(self.notebook, padding=10); self.notebook.add(behavior_log_tab, text="Behavior & Quiz")
        self.create_behavior_log_tab(behavior_log_tab)

        # --- Homework Log Tab (New) ---
        homework_log_tab = ttk.Frame(self.notebook, padding=10); self.notebook.add(homework_log_tab, text="Homework")
        self.create_homework_log_tab(homework_log_tab)

        # --- Data & Export Tab ---
        data_export_tab = ttk.Frame(self.notebook, padding=10); self.notebook.add(data_export_tab, text="Data & Export")
        self.create_data_export_tab(data_export_tab)

        # --- Other Settings Tab ---
        other_settings_tab = ttk.Frame(self.notebook, padding=10); self.notebook.add(other_settings_tab, text="Other Settings")
        self.create_other_settings_tab(other_settings_tab)
        
        # --- Security Tab ---
        security_tab = ttk.Frame(self.notebook, padding=10); self.notebook.add(security_tab, text="Security")
        self.create_security_tab(security_tab)

        # --- Advanced/Hidden Tab (Optional) ---
        # self.create_advanced_tab(advanced_tab)

        self.notebook.grid(column=0,row=0,columnspan=2)
        self.notebook.grid_propagate(True)
        # No specific focus needed, first field in first tab will get it.
        return self.notebook

    def create_general_tab(self, tab_frame):
        lf = ttk.LabelFrame(tab_frame, text="Application Behavior", padding=10); lf.pack(fill=tk.BOTH, side=tk.LEFT, pady=5)
        # Autosave interval
        ttk.Label(lf, text="Autosave Interval (seconds):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.autosave_interval_var = tk.IntVar(value=self.settings.get("autosave_interval_ms", 30000) // 1000)
        ttk.Spinbox(lf, from_=10, to=300, increment=10, textvariable=self.autosave_interval_var, width=5).grid(row=0, column=1, sticky=tk.W, padx=5, pady=3)


        # Student Groups Enabled
        self.groups_enabled_var = tk.BooleanVar(value=self.settings.get("student_groups_enabled", True))
        ttk.Checkbutton(lf, text="Enable Student Groups Feature", variable=self.groups_enabled_var).grid(row=3, column=0, columnspan=2, sticky=tk.W, padx=5, pady=3)
        
        # Zoom Level Display
        self.show_zoom_var = tk.BooleanVar(value=self.settings.get("show_zoom_level_display", True))
        ttk.Checkbutton(lf, text="Show Zoom Level % Display on Main Screen", variable=self.show_zoom_var).grid(row=4, column=0, columnspan=2, sticky=tk.W, padx=5, pady=3)

        # Max Undo History Days
        ttk.Label(lf, text="Max Undo History (days):").grid(row=10, column=0, sticky=tk.W, padx=5, pady=3)
        self.max_undo_days_var = tk.IntVar(value=self.settings.get("max_undo_history_days", MAX_UNDO_HISTORY_DAYS))
        ttk.Spinbox(lf, from_=1, to=90, textvariable=self.max_undo_days_var, width=5).grid(row=10, column=1, sticky=tk.W, padx=5, pady=3)
        
        
        # Theme
        
        
        
        ttk.Label(lf, text = "Theme: ").grid(row=12,column=0,sticky='W', padx=0, pady=3)
        
        style_combo = ttk.Combobox(lf, values= list(self.styles), textvariable=self.style, width=17, state='readonly')
        style_combo.grid(row=12, column=0, sticky=tk.E, columnspan=2, padx=(0,105))
        style_combo.grid_anchor("w")
        style_combo.bind("<<ComboboxSelected>>", self.style_set)
        style_combo.set(self.style.get())
        
        self.theme_combo = ttk.Combobox(lf, values = THEME_LIST, textvariable= self.theme, state='readonly', width=7)
        self.theme_combo.grid(row=12, column=1, sticky=tk.E, padx=(5,0), pady=3)
        self.theme_combo.bind("<<ComboboxSelected>>", self.theme_set)
        self.theme_combo.set(self.theme.get())

        self.style_set()
        
        
        # Canvas Management LabelFrame
        cmf = ttk.LabelFrame(tab_frame, text="Canvas Management", padding=10); cmf.pack(padx=5, fill=tk.BOTH)
        # Student box management visibility
        self.show_management_var = tk.BooleanVar(value=self.settings.get("always_show_box_management", False))
        ttk.Checkbutton(cmf, text="Always show box management tools", variable=self.show_management_var).grid(row=5, column=0, columnspan=2, sticky='W', padx=5, pady=3)


        # Check for collisions on redraw
        self.check_for_collisions_var = tk.BooleanVar(value=self.settings.get("check_for_collisions", True))
        ttk.Checkbutton(cmf, text="Check for collisions on box move", variable=self.check_for_collisions_var).grid(row=6, column=0, columnspan=2, sticky='W', padx=5, pady=3)
        
        # Canvas Color
        ttk.Label(cmf, text = "Canvas color (background): ").grid(row=13,column=0,sticky='W', padx=5, pady=3)
        
        canvas_color_entry = ttk.Entry(cmf, textvariable= self.custom_canvas_color)
        canvas_color_entry.grid(row=13, column=1, sticky="W", padx=5, pady=3)
        
        if self.custom_canvas_color.get() != "":
            self.custom2 = tk.StringVar(value=self.custom_canvas_color.get())
        
        ttk.Button(cmf, text="Choose...", command=lambda v=self.custom_canvas_color: self.choose_color_for_canvas(v)).grid(row=13,column=2,sticky=tk.W,padx=2,pady=3)
        ttk.Button(cmf, text="Default", command=lambda v=self.custom_canvas_color: self.reset_color_for_var(v, "Default")).grid(row=13,column=3, sticky='W', padx=5, pady=3)
        
        # Grid snap
        self.grid_snap_var = tk.BooleanVar(value=self.settings.get("grid_snap_enabled", False))
        ttk.Checkbutton(cmf, text="Enable Snap to Grid during Drag", variable=self.grid_snap_var).grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=5, pady=3)
        ttk.Label(cmf, text="Grid Size (pixels):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=3)
        self.grid_size_var = tk.IntVar(value=self.settings.get("grid_size", DEFAULT_GRID_SIZE))
        ttk.Spinbox(cmf, from_=5, to=100, increment=5, textvariable=self.grid_size_var, width=5).grid(row=2, column=1, sticky=tk.W, padx=5, pady=3)
        
        # Canvas Border Visibility
        self.canvas_border_var = tk.BooleanVar(value=self.settings.get("show_canvas_border_lines", False))
        ttk.Checkbutton(cmf, text="Show canvas borders (see help)", variable=self.canvas_border_var, command=self.force_canvas_border_visi).grid(row=15, column=0, sticky=tk.W, padx=5, pady=3)
        
        self.force_canvas_border_var = tk.BooleanVar(value=self.settings.get("force_canvas_border_lines", False))
        self.force_canvas_border_btn = ttk.Checkbutton(cmf, text="Always show canvas borders", variable=self.force_canvas_border_var)
        self.force_canvas_border_btn.grid(row=15, column=1, sticky=tk.W, padx=5, pady=3)
        
        self.force_canvas_border_visi()

        # Allow Box Dragging
        self.allow_box_dragging_var = tk.BooleanVar(value=self.settings.get("allow_box_dragging", True))
        ttk.Checkbutton(cmf, text="Allow dragging of student/furniture boxes", variable=self.allow_box_dragging_var).grid(row=16, column=0, columnspan=2, sticky='W', padx=5, pady=3)

        # Canvas View Options (Rulers, Grid)
        lf_view_options = ttk.LabelFrame(tab_frame, text="Canvas View Options", padding=10)
        lf_view_options.pack(fill=tk.BOTH, padx=5, pady=10)

        self.show_rulers_var = tk.BooleanVar(value=self.settings.get("show_rulers", False))
        ttk.Checkbutton(lf_view_options, text="Show Rulers", variable=self.show_rulers_var).grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)

        self.show_grid_var = tk.BooleanVar(value=self.settings.get("show_grid", False))
        ttk.Checkbutton(lf_view_options, text="Show Grid", variable=self.show_grid_var).grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)

        ttk.Label(lf_view_options, text="Grid Color:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=3)
        self.grid_color_var = tk.StringVar(value=self.settings.get("grid_color", "#d3d3d3"))
        ttk.Entry(lf_view_options, textvariable=self.grid_color_var, width=12).grid(row=2, column=1, sticky=tk.W, padx=5, pady=3)
        ttk.Button(lf_view_options, text="Choose...", command=lambda v=self.grid_color_var: self.choose_color_for_var(v)).grid(row=2, column=2, sticky=tk.W, padx=2, pady=3)

        # New Guide Settings
        self.save_guides_var = tk.BooleanVar(value=self.settings.get("save_guides_to_file", True))
        ttk.Checkbutton(lf_view_options, text="Save Guides with Layout Data", variable=self.save_guides_var).grid(row=3, column=0, columnspan=3, sticky=tk.W, padx=5, pady=3)

        self.persist_guides_toggle_var = tk.BooleanVar(value=self.settings.get("guides_stay_when_rulers_hidden", True))
        ttk.Checkbutton(lf_view_options, text="Keep Guides in Memory when 'Toggle Rulers' is Off", variable=self.persist_guides_toggle_var).grid(row=4, column=0, columnspan=3, sticky=tk.W, padx=5, pady=3)

        # Guide Color Settings
        self.guides_color_var = tk.StringVar(value=self.settings.get("guides_color", "blue"))
        ttk.Label(lf_view_options, text="Guide Color:").grid(row=0, column=3, sticky=tk.W, padx=5, pady=3)
        ttk.Entry(lf_view_options, textvariable=self.guides_color_var, width=12).grid(row=0, padx=3, column=4)
        ttk.Button(lf_view_options, text="Choose...", command=lambda v=self.guides_color_var: self.choose_color_for_var(v)).grid(row=0, column=5, sticky=tk.W, padx=2, pady=3)
        ttk.Button(lf_view_options, text="Default", command=lambda v=self.guides_color_var: self.reset_color_for_var(v, "blue")).grid(row=0, column=6, sticky=tk.W, padx=2, pady=3)
        
        
    def create_student_display_tab(self, tab_frame):
        lf_defaults = ttk.LabelFrame(tab_frame, text="Default Student Box Appearance", padding=10)
        lf_defaults.grid(sticky="nsew", column=0,row=0, pady=5)
        # Default size
        ttk.Label(lf_defaults, text="Default Width:").grid(row=0,column=0,sticky=tk.W,padx=5,pady=3)
        self.def_stud_w_var = tk.IntVar(value=self.settings.get("default_student_box_width", DEFAULT_STUDENT_BOX_WIDTH))
        ttk.Spinbox(lf_defaults, from_=MIN_STUDENT_BOX_WIDTH, to=500, textvariable=self.def_stud_w_var, width=5).grid(row=0,column=1,sticky=tk.W,padx=5,pady=3)
        ttk.Label(lf_defaults, text="Default Height:").grid(row=1,column=0,sticky=tk.W,padx=5,pady=3)
        self.def_stud_h_var = tk.IntVar(value=self.settings.get("default_student_box_height", DEFAULT_STUDENT_BOX_HEIGHT))
        ttk.Spinbox(lf_defaults, from_=MIN_STUDENT_BOX_HEIGHT, to=300, textvariable=self.def_stud_h_var, width=5).grid(row=1,column=1,sticky=tk.W,padx=5,pady=3)
        # Default colors and font
        self.create_color_font_settings_ui(lf_defaults, 2, "student_box_fill_color", "student_box_outline_color", "student_font_family", "student_font_size", "student_font_color")

        # Additional font size controls for specific log types
        row_after_defaults = 2 + 5 # After 5 rows used by create_color_font_settings_ui starting at row 2

        

        ttk.Label(lf_defaults, text="Quiz Log/Score Font Size (pts):").grid(row=row_after_defaults, column=0, sticky=tk.W, padx=5, pady=3)
        self.quiz_log_font_size_var = tk.IntVar(value=self.settings.get("quiz_log_font_size", DEFAULT_FONT_SIZE))
        ttk.Spinbox(lf_defaults, from_=6, to=24, textvariable=self.quiz_log_font_size_var, width=5).grid(row=row_after_defaults, column=1, sticky=tk.W, padx=5, pady=3)
        row_after_defaults += 1

        ttk.Label(lf_defaults, text="Homework Log/Score Font Size (pts):").grid(row=row_after_defaults, column=0, sticky=tk.W, padx=5, pady=3)
        self.homework_log_font_size_var = tk.IntVar(value=self.settings.get("homework_log_font_size", DEFAULT_FONT_SIZE - 1))
        ttk.Spinbox(lf_defaults, from_=6, to=24, textvariable=self.homework_log_font_size_var, width=5).grid(row=row_after_defaults, column=1, sticky=tk.W, padx=5, pady=3)
        row_after_defaults += 1

        # Setting for text background panel
        self.enable_text_panel_var = tk.BooleanVar(value=self.settings.get("enable_text_background_panel", True))
        ttk.Checkbutton(lf_defaults, text="Enable text background panel on student boxes\n(improves legibility on colored stripes)",
                        variable=self.enable_text_panel_var).grid(row=15, column=0, columnspan=3, sticky=tk.W, padx=5, pady=(10,3))
        
        self.enable_text_panel_always_var = tk.BooleanVar(value=self.settings.get("always_show_text_background_panel", False))
        ttk.Checkbutton(lf_defaults, text="Force enable text background panel on student boxes.\n(Not only when colored)",
                        variable=self.enable_text_panel_always_var).grid(row=16, column=0, columnspan=3, sticky=tk.W, padx=5, pady=(10,3))


        lf_cond_format = ttk.LabelFrame(tab_frame, text="Conditional Formatting Rules", padding=10, width=1000)
        lf_cond_format.grid(sticky="nse", pady=5, padx=5, column=1, columnspan=3, row=0)
        lf_cond_format.grid_anchor("e")
        ttk.Button(lf_cond_format, text="Add Rule...", command=self.add_conditional_rule).pack(pady=3, anchor=tk.W)
        self.rules_listbox = tk.Listbox(lf_cond_format, height=7, exportselection=False, width=75, selectmode=tk.EXTENDED)
        self.rules_listbox.pack(fill=tk.X, expand=True, pady=2)
        self.populate_conditional_rules_listbox()
        rule_btns_frame = ttk.Frame(lf_cond_format); rule_btns_frame.pack(fill=tk.X)
        ttk.Button(rule_btns_frame, text="Edit Selected", command=self.edit_selected_conditional_rule).pack(side=tk.LEFT, padx=2)
        ttk.Button(rule_btns_frame, text="Remove Selected", command=self.remove_selected_conditional_rule).pack(side=tk.LEFT, padx=2)
        ttk.Button(rule_btns_frame, text="Bulk Edit Selected...", command=self.bulk_edit_selected_rules).pack(side=tk.LEFT, padx=10)


    def create_behavior_log_tab(self, tab_frame):
        # Recent Incidents Display
        lf_recent = ttk.LabelFrame(tab_frame, text="Recent Incidents on Student Boxes (Behavior/Quiz)", padding=10); lf_recent.grid(sticky="nsew",column=0,row=0, pady=5)
        self.show_recent_var = tk.BooleanVar(value=self.settings.get("show_recent_incidents_on_boxes", True))
        ttk.Checkbutton(lf_recent, text="Show recent incidents on student boxes", variable=self.show_recent_var).grid(row=0,column=0,columnspan=2,sticky=tk.W, padx=5,pady=3)
        ttk.Label(lf_recent, text="Number to show:").grid(row=1,column=0,sticky=tk.W,padx=5,pady=3)
        self.num_recent_var = tk.IntVar(value=self.settings.get("num_recent_incidents_to_show", 2))
        ttk.Spinbox(lf_recent, from_=0, to=10, textvariable=self.num_recent_var, width=3).grid(row=1,column=1,sticky=tk.W,padx=5,pady=3)
        ttk.Label(lf_recent, text="Time window (hours):").grid(row=2,column=0,sticky=tk.W,padx=5,pady=3)
        self.time_window_var = tk.IntVar(value=self.settings.get("recent_incident_time_window_hours", 24))
        ttk.Spinbox(lf_recent, from_=1, to=168, textvariable=self.time_window_var, width=4).grid(row=2,column=1,sticky=tk.W,padx=5,pady=3)
        self.show_full_recent_var = tk.BooleanVar(value=self.settings.get("show_full_recent_incidents", False))
        ttk.Checkbutton(lf_recent, text="Show full behavior names (not initials)", variable=self.show_full_recent_var).grid(row=3,column=0,columnspan=2,sticky=tk.W,padx=5,pady=3)
        self.reverse_order_var = tk.BooleanVar(value=self.settings.get("reverse_incident_order", True))
        ttk.Checkbutton(lf_recent, text="Show most recent incident last (chronological)", variable=self.reverse_order_var).grid(row=4,column=0,columnspan=2,sticky=tk.W,padx=5,pady=3)

        # Custom Behaviors
        lf_custom_b = ttk.LabelFrame(tab_frame, text="Custom Behaviors & Initials", padding=10); lf_custom_b.grid(sticky="nsew",column=1,row=0, pady=5)
        custom_b_btns_frame = ttk.Frame(lf_custom_b); custom_b_btns_frame.pack(fill=tk.X)
        ttk.Button(custom_b_btns_frame, text="Add Behavior...", command=self.add_custom_behavior).pack(side=tk.LEFT, padx=2, pady=3)
        ttk.Button(custom_b_btns_frame, text="Manage Behavior/Quiz Initials...", command=self.manage_behavior_initials).pack(side=tk.LEFT, padx=2, pady=3)
        ttk.Button(custom_b_btns_frame, text="Manage Quiz Mark Types...", command=self.manage_quiz_mark_types).pack(side=tk.LEFT, padx=2, pady=3)


        self.custom_behaviors_listbox = tk.Listbox(lf_custom_b, height=5, exportselection=False)
        self.custom_behaviors_listbox.pack(fill=tk.X, expand=True, pady=(5,2))
        self.populate_custom_behaviors_listbox()
        custom_b_edit_btns_frame = ttk.Frame(lf_custom_b); custom_b_edit_btns_frame.pack(fill=tk.X)
        ttk.Button(custom_b_edit_btns_frame, text="Edit Selected", command=self.edit_selected_custom_behavior).pack(side=tk.LEFT, padx=2)
        ttk.Button(custom_b_edit_btns_frame, text="Remove Selected", command=self.remove_selected_custom_behavior).pack(side=tk.LEFT, padx=2)

        # Quiz Settings
        lf_quiz = ttk.LabelFrame(tab_frame, text="Quiz Logging & Session Settings", padding=10); lf_quiz.grid(sticky="nsew",column=0,row=1, pady=5)
        ttk.Label(lf_quiz, text="Default Quiz Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.def_quiz_name_var = tk.StringVar(value=self.settings.get("default_quiz_name", "Pop Quiz"))
        ttk.Entry(lf_quiz, textvariable=self.def_quiz_name_var, width=20).grid(row=0,column=1,sticky=tk.W,padx=5,pady=3)

        ttk.Label(lf_quiz, text="Default #Questions (Manual Log):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.def_quiz_q_var = tk.IntVar(value=self.settings.get("default_quiz_questions",10))
        ttk.Spinbox(lf_quiz, from_=1, to=100, textvariable=self.def_quiz_q_var, width=5).grid(row=1,column=1,sticky=tk.W,padx=5,pady=3)

        ttk.Label(lf_quiz, text="Quiz Name Memory Timeout (mins):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=3)
        self.quiz_timeout_var = tk.IntVar(value=self.settings.get("last_used_quiz_name_timeout_minutes", 60))
        ttk.Spinbox(lf_quiz, from_=0, to=1440, textvariable=self.quiz_timeout_var, width=5).grid(row=2,column=1,sticky=tk.W,padx=5,pady=3)

        self.show_inc_quiz_var = tk.BooleanVar(value=self.settings.get("show_recent_incidents_during_quiz", True))
        ttk.Checkbutton(lf_quiz, text="Show recent behaviors during live quiz", variable=self.show_inc_quiz_var).grid(row=3,column=0,columnspan=2,sticky=tk.W, padx=5,pady=3)
        
        self.combine_marks_display_var = tk.BooleanVar(value=self.settings.get("combine_marks_for_display", True))
        # ttk.Checkbutton(lf_quiz, text="Combine mark counts for log display (e.g., Correct: 8/10)", variable=self.combine_marks_display_var).grid(row=4,column=0,columnspan=2,sticky=tk.W, padx=5,pady=3) # Removed for now, logic complex

        ttk.Button(lf_quiz, text="Quiz Templates...", command=self.app.manage_quiz_templates_dialog).grid(row=0,column=2, padx=10, pady=3, sticky=tk.E)
        lf_quiz.grid_columnconfigure(2, weight=1)

    def create_homework_log_tab(self, tab_frame):
        """Rebuilt homework tab with clear sections for Types and Statuses."""
        
        # --- Column 0: Customization of Lists ---
        customization_frame = tk.Canvas(tab_frame, width=1000)
        customization_frame.grid(row=0, column=1, columnspan=2, rowspan=2, sticky="nsew", padx=(0,10))
        customization_frame.grid_propagate(True)
        customization_frame.grid_columnconfigure(0,weight=1, minsize=600)
        customization_frame.grid_rowconfigure(1,weight=1, minsize=100)
        
        
        # A: Custom Homework TYPES (e.g., "Reading Assignment")
        lf_custom_hw_types = ttk.LabelFrame(customization_frame, text="A: Homework Types", padding=10)
        lf_custom_hw_types.grid(column=0, row=0, sticky='nsew', pady=(0,0))
        ttk.Label(lf_custom_hw_types, text="For simplified & detailed logging, and live sessions.").pack(anchor='w', pady=(0,5))
        
        custom_hw_types_btns_frame = ttk.Frame(lf_custom_hw_types); custom_hw_types_btns_frame.pack(fill=tk.X)
        ttk.Button(custom_hw_types_btns_frame, text="Add Type...", command=self.add_custom_homework_type).pack(side=tk.LEFT, padx=2, pady=2)

        self.custom_hw_types_listbox = tk.Listbox(lf_custom_hw_types, height=5, exportselection=False)
        self.custom_hw_types_listbox.pack(fill=tk.BOTH, pady=(5,2))
        self.populate_custom_homework_types_listbox()
        
        custom_hw_types_edit_btns_frame = ttk.Frame(lf_custom_hw_types); custom_hw_types_edit_btns_frame.pack(fill=tk.X)
        ttk.Button(custom_hw_types_edit_btns_frame, text="Edit Selected", command=self.edit_selected_custom_homework_type).pack(side=tk.LEFT, padx=2)
        ttk.Button(custom_hw_types_edit_btns_frame, text="Remove Selected", command=self.remove_selected_custom_homework_type).pack(side=tk.LEFT, padx=2)

        # B: Custom Homework STATUSES (e.g., "Done", "Late")
        lf_custom_hw_statuses = ttk.LabelFrame(customization_frame, text="B: Homework Statuses", padding=10)
        lf_custom_hw_statuses.grid(column=0, row=1, sticky='nsew', pady=0)
        ttk.Label(lf_custom_hw_statuses, text="For the simplified view's second popup.").pack(anchor='w', pady=(0,5))

        custom_hw_statuses_btns_frame = ttk.Frame(lf_custom_hw_statuses); custom_hw_statuses_btns_frame.pack(fill=tk.X)
        ttk.Button(custom_hw_statuses_btns_frame, text="Add Status...", command=self.add_custom_homework_status).pack(side=tk.LEFT, padx=2, pady=2)
        
        self.custom_hw_statuses_listbox = tk.Listbox(lf_custom_hw_statuses, height=5, exportselection=False)
        self.custom_hw_statuses_listbox.pack(fill=tk.BOTH, expand=True, pady=(5,2))
        self.populate_custom_homework_statuses_listbox()
        
        custom_hw_statuses_edit_btns_frame = ttk.Frame(lf_custom_hw_statuses); custom_hw_statuses_edit_btns_frame.pack(fill=tk.X)
        ttk.Button(custom_hw_statuses_edit_btns_frame, text="Edit Selected", command=self.edit_selected_custom_homework_status).pack(side=tk.LEFT, padx=2)
        ttk.Button(custom_hw_statuses_edit_btns_frame, text="Remove Selected", command=self.remove_selected_custom_homework_status).pack(side=tk.LEFT, padx=2)
        
        # --- Column 1: Other Settings ---
        #settings_frame = ttk.Frame(tab_frame)
        #settings_frame.grid(row=0, column=1, sticky="ns")
        
        
        
        
        # Recent Homework Display
        lf_recent_hw = ttk.LabelFrame(tab_frame, text="Recent Homework on Student Boxes", padding=10)
        lf_recent_hw.grid(sticky="nsew",column=0,row=0, pady=0, padx=10)
        self.show_recent_hw_var = tk.BooleanVar(value=self.settings.get("show_recent_homeworks_on_boxes", True))
        ttk.Checkbutton(lf_recent_hw, text="Show recent homework logs on student boxes", variable=self.show_recent_hw_var).grid(row=0,column=0,columnspan=2,sticky=tk.W, padx=5,pady=3)
        ttk.Label(lf_recent_hw, text="Number to show:").grid(row=1,column=0,sticky=tk.W,padx=5,pady=3)
        self.num_recent_hw_var = tk.IntVar(value=self.settings.get("num_recent_homeworks_to_show", 2))
        ttk.Spinbox(lf_recent_hw, from_=0, to=10, textvariable=self.num_recent_hw_var, width=3).grid(row=1,column=1,sticky=tk.W,padx=5,pady=3)
        ttk.Label(lf_recent_hw, text="Time window (hours):").grid(row=2,column=0,sticky=tk.W,padx=5,pady=3)
        self.time_window_hw_var = tk.IntVar(value=self.settings.get("recent_homework_time_window_hours", 24))
        ttk.Spinbox(lf_recent_hw, from_=1, to=168, textvariable=self.time_window_hw_var, width=4).grid(row=2,column=1,sticky=tk.W,padx=5,pady=3)
        self.show_full_recent_hw_var = tk.BooleanVar(value=self.settings.get("show_full_recent_homeworks", False))
        ttk.Checkbutton(lf_recent_hw, text="Show full homework names (not initials)", variable=self.show_full_recent_hw_var).grid(row=3,column=0,columnspan=2,sticky=tk.W,padx=5,pady=3)
        self.reverse_hw_order_var = tk.BooleanVar(value=self.settings.get("reverse_homework_order", True))
        ttk.Checkbutton(lf_recent_hw, text="Show most recent homework last (chronological)", variable=self.reverse_hw_order_var).grid(row=4,column=0,columnspan=2,sticky=tk.W,padx=5,pady=3)
        """
        # Custom Homework Log Behaviors (for manual logging options like "Done", "Not Done")
        lf_custom_hw_log = ttk.LabelFrame(tab_frame, text="Custom Homework Log Options & Initials", padding=10)
        lf_custom_hw_log.grid(sticky="nsew", column=1,row=0, pady=0)
        custom_hw_log_btns_frame = ttk.Frame(lf_custom_hw_log); custom_hw_log_btns_frame.pack(fill=tk.X)
        ttk.Button(custom_hw_log_btns_frame, text="Add Log Option...", command=self.add_custom_homework_status).pack(side=tk.LEFT, padx=2, pady=3)
        ttk.Button(custom_hw_log_btns_frame, text="Manage Homework Log Initials...", command=self.manage_homework_initials).pack(side=tk.LEFT, padx=2, pady=3)
        ttk.Button(custom_hw_log_btns_frame, text="Manage Homework Mark Types...", command=self.manage_homework_mark_types).pack(side=tk.LEFT, padx=2, pady=3)


        self.custom_hw_log_behaviors_listbox = tk.Listbox(lf_custom_hw_log, height=4, exportselection=False)
        self.custom_hw_log_behaviors_listbox.pack(fill=tk.X, expand=True, pady=(5,2))
        self.populate_custom_homework_statuses_listbox()
        custom_hw_log_edit_btns_frame = ttk.Frame(lf_custom_hw_log); custom_hw_log_edit_btns_frame.pack(fill=tk.X)
        ttk.Button(custom_hw_log_edit_btns_frame, text="Edit Selected", command=self.edit_selected_custom_homework_status).pack(side=tk.LEFT, padx=2)
        ttk.Button(custom_hw_log_edit_btns_frame, text="Remove Selected", command=self.remove_selected_custom_homework_status).pack(side=tk.LEFT, padx=2)
        """
        # Live Homework Session Settings
        lf_live_hw = ttk.LabelFrame(tab_frame, text="Live Homework Session Settings", padding=10)
        lf_live_hw.grid(sticky="nsew", column=0, row=1, pady=0, padx=5)
        ttk.Label(lf_live_hw, text="Default Session Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.def_hw_session_name_var = tk.StringVar(value=self.settings.get("default_homework_name", "Homework Check"))
        ttk.Entry(lf_live_hw, textvariable=self.def_hw_session_name_var, width=20).grid(row=0,column=1,sticky=tk.W,padx=5,pady=3)

        ttk.Label(lf_live_hw, text="Session Mode:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.live_hw_mode_var = tk.StringVar(value=self.settings.get("live_homework_session_mode", "Yes/No"))
        hw_mode_combo = ttk.Combobox(lf_live_hw, textvariable=self.live_hw_mode_var, values=["Yes/No", "Select"], state="readonly", width=10)
        hw_mode_combo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=3)
        hw_mode_combo.bind("<<ComboboxSelected>>", self.on_live_hw_mode_change)

        
        # Settings specific to "Yes/No" mode
        self.yes_no_settings_frame = ttk.Frame(lf_live_hw)
        self.yes_no_settings_frame.grid(row=2, column=0, columnspan=3, sticky=tk.EW, padx=5, pady=3)
        # Custom Homework Session Types (for Yes/No mode list)
        lf_custom_hw_session_types = ttk.LabelFrame(self.yes_no_settings_frame, text="Custom Homework Types for 'Yes/No' Session", padding=5)
        lf_custom_hw_session_types.pack(fill=tk.X, pady=3)
        custom_hw_session_btns_frame = ttk.Frame(lf_custom_hw_session_types); custom_hw_session_btns_frame.pack(fill=tk.X)
        ttk.Button(custom_hw_session_btns_frame, text="Add Type...", command=self.add_custom_homework_type).pack(side=tk.LEFT, padx=2, pady=2)
        self.custom_hw_session_types_listbox = tk.Listbox(lf_custom_hw_session_types, height=3, exportselection=False)
        self.custom_hw_session_types_listbox.pack(fill=tk.X, expand=True, pady=(3,2))
        self.populate_custom_homework_types_listbox()
        custom_hw_session_edit_btns_frame = ttk.Frame(lf_custom_hw_session_types); custom_hw_session_edit_btns_frame.pack(fill=tk.X)
        ttk.Button(custom_hw_session_edit_btns_frame, text="Edit Selected", command=self.edit_selected_custom_homework_type).pack(side=tk.LEFT, padx=2)
        ttk.Button(custom_hw_session_edit_btns_frame, text="Remove Selected", command=self.remove_selected_custom_homework_type).pack(side=tk.LEFT, padx=2)


        # Settings specific to "Select" mode
        self.select_mode_settings_frame = ttk.Frame(lf_live_hw)
        # self.select_mode_settings_frame.grid(row=2, column=0, columnspan=3, sticky=tk.EW, padx=5, pady=3) # Positioned by on_live_hw_mode_change
        lf_select_options = ttk.LabelFrame(self.select_mode_settings_frame, text="Options for 'Select' Session Mode", padding=5)
        lf_select_options.pack(fill=tk.X, pady=3)
        # Add UI to manage self.settings["live_homework_select_mode_options"] (list of dicts {"name": "..."})
        # For now, it uses DEFAULT_HOMEWORK_SESSION_BUTTONS. A more complex UI would allow user to customize these.
        ttk.Button(lf_select_options, text="Manage 'Select' Options...", command=self.manage_live_homework_select_options).pack(pady=3, anchor=tk.W)
        

        # General Homework Settings
        self.log_hw_marks_var = tk.BooleanVar(value=self.settings.get("log_homework_marks_enabled", True))
        ttk.Checkbutton(lf_live_hw, text="Enable Detailed Marks for Manual Homework Logging", variable=self.log_hw_marks_var).grid(row=3,column=0,columnspan=3,sticky=tk.W, padx=5,pady=3)
        ttk.Button(lf_live_hw, text="Homework Templates...", command=self.app.manage_homework_templates_dialog).grid(row=0,column=2, padx=10, pady=3, sticky=tk.E)
        lf_live_hw.grid_columnconfigure(2, weight=1)

        #self.on_live_hw_mode_change(None) # Show/hide mode-specific frames


    # --- Methods for managing the new custom lists ---
    
    # Custom Homework TYPES
    def populate_custom_homework_types_listbox(self):
        self.custom_hw_types_listbox.delete(0, tk.END)
        print(self.custom_homework_types_ref)
        for item in self.custom_homework_types_ref:
            self.custom_hw_types_listbox.insert(tk.END, item["name"])
    
    def add_custom_homework_type(self):
        name = simpledialog.askstring("Add Homework Type", "Enter name for the new type (e.g., 'Project Milestone 1'):", parent=self)
        if name and name.strip():
            name = name.strip()
            if any(item["name"].lower() == name.lower() for item in self.custom_homework_types_ref):
                 messagebox.showwarning("Duplicate", f"Type '{name}' already exists.", parent=self); return
            # The concept of a separate ID is now less critical if we just use the name, but good for robustness
            type_id_str, next_id_val = self.app.get_new_custom_homework_type_id() # Reusing this ID generator
            self.app.settings["next_custom_homework_type_id_num"] = next_id_val
            self.custom_homework_types_ref.append({"id": type_id_str, "name": name})
            self.settings_changed_flag = True; self.app.save_custom_homework_types(); self.populate_custom_homework_types_listbox()

    def edit_selected_custom_homework_type(self):
        sel_idx = self.custom_hw_types_listbox.curselection()
        if not sel_idx: return
        idx = sel_idx[0]; old_name = self.custom_homework_types_ref[idx]["name"]
        new_name = simpledialog.askstring("Edit Homework Type", "Enter new name:", initialvalue=old_name, parent=self)
        if new_name and new_name.strip():
            new_name = new_name.strip()
            if new_name.lower() != old_name.lower() and any(item["name"].lower() == new_name.lower() for i, item in enumerate(self.custom_homework_types_ref) if i != idx):
                 messagebox.showwarning("Duplicate", f"Type '{new_name}' already exists.", parent=self); return
            self.custom_homework_types_ref[idx]["name"] = new_name
            self.settings_changed_flag = True; self.app.save_custom_homework_types(); self.populate_custom_homework_types_listbox()
    
    def remove_selected_custom_homework_type(self):
        sel_idx = self.custom_hw_types_listbox.curselection()
        if not sel_idx: return
        if messagebox.askyesno("Confirm Remove", "Remove selected homework type?", parent=self):
            del self.custom_homework_types_ref[sel_idx[0]]
            self.settings_changed_flag = True; self.app.save_custom_homework_types(); self.populate_custom_homework_types_listbox()

    # Custom Homework STATUSES
    def populate_custom_homework_statuses_listbox(self):
        self.custom_hw_statuses_listbox.delete(0, tk.END)
        #self.custom_hw_log_behaviors_listbox
        for item in self.custom_homework_statuses_ref:
            self.custom_hw_statuses_listbox.insert(tk.END, item["name"])

    def add_custom_homework_status(self):
        name = simpledialog.askstring("Add Homework Status", "Enter name for the new status (e.g., 'Excellent Effort'):", parent=self)
        if name and name.strip():
            name = name.strip()
            if any(item["name"].lower() == name.lower() for item in self.custom_homework_statuses_ref):
                 messagebox.showwarning("Duplicate", f"Status '{name}' already exists.", parent=self); return
            self.custom_homework_statuses_ref.append({"name": name})
            self.settings_changed_flag = True; self.app.save_custom_homework_statuses(); self.populate_custom_homework_statuses_listbox()

    def edit_selected_custom_homework_status(self):
        sel_idx = self.custom_hw_statuses_listbox.curselection()
        if not sel_idx: return
        idx = sel_idx[0]; old_name = self.custom_homework_statuses_ref[idx]["name"]
        new_name = simpledialog.askstring("Edit Homework Status", "Enter new name:", initialvalue=old_name, parent=self)
        if new_name and new_name.strip():
            new_name = new_name.strip()
            if new_name.lower() != old_name.lower() and any(item["name"].lower() == new_name.lower() for i, item in enumerate(self.custom_homework_statuses_ref) if i != idx):
                 messagebox.showwarning("Duplicate", f"Status '{new_name}' already exists.", parent=self); return
            self.custom_homework_statuses_ref[idx]["name"] = new_name
            self.settings_changed_flag = True; self.app.save_custom_homework_statuses(); self.populate_custom_homework_statuses_listbox()
            
    def remove_selected_custom_homework_status(self):
        sel_idx = self.custom_hw_statuses_listbox.curselection()
        if not sel_idx: return
        if messagebox.askyesno("Confirm Remove", "Remove selected homework status?", parent=self):
            del self.custom_homework_statuses_ref[sel_idx[0]]
            self.settings_changed_flag = True; self.app.save_custom_homework_statuses(); self.populate_custom_homework_statuses_listbox()


    
    def on_live_hw_mode_change(self, event):
        mode = self.live_hw_mode_var.get()
        if mode == "Yes/No":
            self.select_mode_settings_frame.grid_remove()
            self.yes_no_settings_frame.grid(row=2, column=0, columnspan=3, sticky=tk.EW, padx=5, pady=3)
        elif mode == "Select":
            self.yes_no_settings_frame.grid_remove()
            self.select_mode_settings_frame.grid(row=2, column=0, columnspan=3, sticky=tk.EW, padx=5, pady=3)
        else:
            self.yes_no_settings_frame.grid_remove()
            self.select_mode_settings_frame.grid_remove()

    def create_data_export_tab(self, tab_frame):
        lf_excel = ttk.LabelFrame(tab_frame, text="Excel Export Defaults", padding=10); lf_excel.pack(fill=tk.X, pady=5)
        self.excel_sep_sheets_var = tk.BooleanVar(value=self.settings.get("excel_export_separate_sheets_by_default", True))
        ttk.Checkbutton(lf_excel, text="Separate log types into different sheets by default", variable=self.excel_sep_sheets_var).pack(anchor=tk.W, padx=5, pady=2)
        self.excel_inc_summary_var = tk.BooleanVar(value=self.settings.get("excel_export_include_summaries_by_default", True))
        ttk.Checkbutton(lf_excel, text="Include summary sheet by default", variable=self.excel_inc_summary_var).pack(anchor=tk.W, padx=5, pady=2)

        lf_autosave_excel = ttk.LabelFrame(tab_frame, text="Excel Log Autosave (Experimental)", padding=10); lf_autosave_excel.pack(fill=tk.X, pady=5)
        self.enable_excel_autosave_var = tk.BooleanVar(value=self.settings.get("enable_excel_autosave", False))
        ttk.Checkbutton(lf_autosave_excel, text=f"Enable autosaving log to Excel file ({os.path.basename(AUTOSAVE_EXCEL_FILE)})", variable=self.enable_excel_autosave_var).pack(anchor=tk.W, padx=5, pady=2)
        ttk.Label(lf_autosave_excel, text="Note: This uses current export filters if set, or exports all data. File is overwritten each time.").pack(anchor=tk.W, padx=5, pady=2)

        lf_export_image = ttk.LabelFrame(tab_frame, text="Image Exporting", padding=10); lf_export_image.pack(fill=tk.X, pady=5)
        self.dpi_image_export_var = tk.StringVar(value=self.settings.get("output_dpi", 600))
        ttk.Label(lf_export_image, text="Set output dpi for image exports:").pack(anchor=tk.W, padx=5, pady=2)
        self.export_image_spin = ttk.Spinbox(lf_export_image, to=900, values=['300', '600', '900']); self.export_image_spin.pack(anchor=tk.W, padx=5, pady=2)
        self.export_image_spin.set(self.dpi_image_export_var.get())

    def create_security_tab(self, tab_frame):
        lf_password = ttk.LabelFrame(tab_frame, text="Application Password", padding=10)
        lf_password.pack(fill=tk.X, pady=5)

        current_pw_set = self.password_manager.is_password_set()
        self.current_pw_status_label = ttk.Label(lf_password, text="Status: Password IS SET" if current_pw_set else "Status: Password NOT SET")
        self.current_pw_status_label.grid(row=0, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)

        ttk.Label(lf_password, text="New Password:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.new_pw_var = tk.StringVar()
        new_pw_entry = ttk.Entry(lf_password, textvariable=self.new_pw_var, show="*", width=25)
        new_pw_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=3)

        ttk.Label(lf_password, text="Confirm New Password:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=3)
        self.confirm_pw_var = tk.StringVar()
        confirm_pw_entry = ttk.Entry(lf_password, textvariable=self.confirm_pw_var, show="*", width=25)
        confirm_pw_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=3)

        set_pw_btn = ttk.Button(lf_password, text="Set/Change Password", command=self.set_or_change_password)
        set_pw_btn.grid(row=3, column=0, padx=5, pady=10)
        remove_pw_btn = ttk.Button(lf_password, text="Remove Password", command=self.remove_password, state=tk.NORMAL if current_pw_set else tk.DISABLED)
        remove_pw_btn.grid(row=3, column=1, padx=5, pady=10, sticky=tk.W)
        self.remove_pw_button_ref = remove_pw_btn # To update state

        lf_pw_options = ttk.LabelFrame(tab_frame, text="Password Options", padding=10)
        lf_pw_options.pack(fill=tk.X, pady=5)
        self.pw_on_open_var = tk.BooleanVar(value=self.settings.get("password_on_open", False))
        ttk.Checkbutton(lf_pw_options, text="Require password on application open", variable=self.pw_on_open_var).pack(anchor=tk.W, padx=5, pady=2)
        self.pw_on_edit_var = tk.BooleanVar(value=self.settings.get("password_on_edit_action", False))
        ttk.Checkbutton(lf_pw_options, text="Require password for sensitive actions (add/edit/delete items, layout changes)", variable=self.pw_on_edit_var).pack(anchor=tk.W, padx=5, pady=2)
        
        auto_lock_frame = ttk.Frame(lf_pw_options); auto_lock_frame.pack(fill=tk.X, pady=2)
        self.pw_auto_lock_var = tk.BooleanVar(value=self.settings.get("password_auto_lock_enabled", False))
        ttk.Checkbutton(auto_lock_frame, text="Auto-lock application after inactivity for", variable=self.pw_auto_lock_var).pack(side=tk.LEFT, anchor=tk.W, padx=5)
        self.pw_auto_lock_timeout_var = tk.IntVar(value=self.settings.get("password_auto_lock_timeout_minutes", 15))
        ttk.Spinbox(auto_lock_frame, from_=1, to=120, textvariable=self.pw_auto_lock_timeout_var, width=4).pack(side=tk.LEFT, padx=2)
        ttk.Label(auto_lock_frame, text="minutes").pack(side=tk.LEFT)

        ttk.Label(lf_pw_options, text="For the Master Recovery Password, ask Yaakov Maimon (see Help)", foreground="blue", wraplength=420).pack(anchor=tk.W, padx=5, pady=5)

    def create_other_settings_tab(self, tab_frame):
        # Create content for the Other Settings tab
        lf_other_options = ttk.LabelFrame(tab_frame, text="Other Options", padding=10)
        lf_other_options.pack(fill=tk.X, pady=5)
        
        ttk.Button(lf_other_options, text="Reset All Settings to Default", command=self.reset_all_settings, style="Warning.TButton").pack(anchor=tk.W, padx=5, pady=5)
        
    def reset_all_settings(self):
        if self.password_manager.is_locked:
            if not self.prompt_for_password("Confirm Reset", "Enter password to confirm reset of all settings to default. This cannot be undone.", for_editing=True):
                return
        if messagebox.askyesno("Reset Settings", "Are you sure you want to reset all settings to default? This cannot be undone.", parent=self):
            self.reset = True
            self.settings_changed_flag = True
            messagebox.showinfo("Settings Reset", "All settings have been reset to default.", parent=self)
            self.settings = self._get_default_settings()
            self.ok()# Reload settings

    def _get_default_settings(self):
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
            "current_mode": "behavior", # "behavior", "quiz", or "homework"
            "max_undo_history_days": MAX_UNDO_HISTORY_DAYS,
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
            "type_theme": "sun-valley-light", # Newer
            "enable_text_background_panel": True, # Default for the new setting
            "show_rulers": False, # Default for rulers
            "show_grid": False, # Default for grid visibility
            "grid_color": "#000000", # Default light gray for grid lines
            "save_guides_to_file": True, # New setting for guides
            "guides_stay_when_rulers_hidden": True, # New setting for guides
            "next_guide_id_num": 1, # Added in migration, also good here
            "guides_color": "blue", # Default color for guides
            "allow_box_dragging": True, # New setting for box dragging
        }

   


    def theme_set(self, event):
        #print(self.app.theme_style_using, "old")
        self.app.theme_style_using = self.theme.get()
        self.settings_changed_flag = True
        #print("Theme: ", self.theme.get())
        self.theme2 = self.theme.get()
        #print("theme2", self.theme2)

    def style_set(self, event=None):
        self.app.type_theme = self.style.get()
        self.theme_combo.configure(state='disabled' if "sun-valley" not in self.style.get().lower() else 'readonly')
        self.theme_combo.set("Light") if "sun-valley" not in self.style.get().lower() else "System"

    def set_or_change_password(self):
        new_pw = self.new_pw_var.get()
        confirm_pw = self.confirm_pw_var.get()
        if not new_pw:
            messagebox.showerror("Password Error", "New password cannot be empty.", parent=self)
            return
        if new_pw != confirm_pw:
            messagebox.showerror("Password Error", "Passwords do not match.", parent=self)
            return
        if len(new_pw) < 4: # Basic length check
            messagebox.showwarning("Weak Password", "Password should be at least 4 characters.", parent=self)
            # Allow user to proceed if they insist
        
        self.password_manager.set_password(new_pw)
        self.settings_changed_flag = True # Settings (hash) changed
        self.new_pw_var.set(""); self.confirm_pw_var.set("")
        self.current_pw_status_label.config(text="Status: Password IS SET")
        self.remove_pw_button_ref.config(state=tk.NORMAL)
        messagebox.showinfo("Password Set", "Application password has been set/changed.", parent=self)

    def prompt_for_password(self, title, prompt_message, for_editing=False):
        if self.password_manager.is_locked:
             if not hasattr(self, '_lock_screen_active') or not self._lock_screen_active.winfo_exists(): self.show_lock_screen()
             return not self.password_manager.is_locked
        if for_editing and not self.settings.get("password_on_edit_action", False) and not self.password_manager.is_password_set(): return True
        if not self.password_manager.is_password_set(): return True
        dialog = PasswordPromptDialog(self.master, title, prompt_message, self.password_manager)
        return dialog.result

    def remove_password(self):
        if self.password_manager.is_password_set():
            if self.prompt_for_password("Confirm Password", "Enter current password to confirm identity", for_editing=True):
                if messagebox.askyesno("Confirm Removal", "Are you sure you want to remove the application password?", parent=self):
                    self.password_manager.set_password(None) # Set to None effectively removes it
                    self.settings_changed_flag = True
                    self.current_pw_status_label.config(text="Status: Password NOT SET")
                    self.remove_pw_button_ref.config(state=tk.DISABLED)
                    self.pw_on_open_var.set(False) # Disable options that require a password
                    self.pw_on_edit_var.set(False)
                    self.pw_auto_lock_var.set(False)
                    messagebox.showinfo("Password Removed", "Application password has been removed.", parent=self)
        else:
            messagebox.showinfo("No Password", "No application password is currently set.", parent=self)
    

    # --- UI Helper for color/font settings ---
    def create_color_font_settings_ui(self, parent_frame, start_row, fill_key, outline_key, font_fam_key, font_size_key, font_color_key):
        # Fill Color
        ttk.Label(parent_frame, text="Default Fill Color:").grid(row=start_row,column=0,sticky=tk.W,padx=5,pady=3)
        fill_var = tk.StringVar(value=self.settings.get(fill_key, DEFAULT_BOX_FILL_COLOR))
        setattr(self, f"{fill_key}_var", fill_var) # Store var on self
        ttk.Entry(parent_frame, textvariable=fill_var, width=12).grid(row=start_row,column=1,sticky=tk.W,padx=5,pady=3)
        ttk.Button(parent_frame, text="Choose...", command=lambda v=fill_var: self.choose_color_for_var(v)).grid(row=start_row,column=2,sticky=tk.W,padx=2,pady=3)
        # Outline Color
        ttk.Label(parent_frame, text="Default Outline Color:").grid(row=start_row+1,column=0,sticky=tk.W,padx=5,pady=3)
        outline_var = tk.StringVar(value=self.settings.get(outline_key, DEFAULT_BOX_OUTLINE_COLOR))
        setattr(self, f"{outline_key}_var", outline_var)
        ttk.Entry(parent_frame, textvariable=outline_var, width=12).grid(row=start_row+1,column=1,sticky=tk.W,padx=5,pady=3)
        ttk.Button(parent_frame, text="Choose...", command=lambda v=outline_var: self.choose_color_for_var(v)).grid(row=start_row+1,column=2,sticky=tk.W,padx=2,pady=3)
        # Font Family
        ttk.Label(parent_frame, text="Default Font Family:").grid(row=start_row+2,column=0,sticky=tk.W,padx=5,pady=3)
        font_fam_var = tk.StringVar(value=self.settings.get(font_fam_key, DEFAULT_FONT_FAMILY))
        setattr(self, f"{font_fam_key}_var", font_fam_var)
        available_fonts = self.settings.get("available_fonts", [DEFAULT_FONT_FAMILY])
        ff_combo = ttk.Combobox(parent_frame, textvariable=font_fam_var, values=available_fonts, width=20, state="readonly")
        ff_combo.grid(row=start_row+2,column=1,columnspan=2,sticky=tk.EW,padx=5,pady=3)
        ff_combo.bind("<MouseWheel>", lambda event: "break") # Prevent main canvas scroll
        # Font Size
        ttk.Label(parent_frame, text="Names Font Size (pts):").grid(row=start_row+3,column=0,sticky=tk.W,padx=5,pady=3)
        font_size_var = tk.IntVar(value=self.settings.get(font_size_key, DEFAULT_FONT_SIZE))
        setattr(self, f"{font_size_key}_var", font_size_var)
        ttk.Spinbox(parent_frame, from_=6, to=24, textvariable=font_size_var, width=5).grid(row=start_row+3,column=1,sticky=tk.W,padx=5,pady=3)
        # Font Color
        ttk.Label(parent_frame, text="Default Font Color:").grid(row=start_row+4,column=0,sticky=tk.W,padx=5,pady=3)
        font_color_var = tk.StringVar(value=self.settings.get(font_color_key, DEFAULT_FONT_COLOR))
        setattr(self, f"{font_color_key}_var", font_color_var)
        ttk.Entry(parent_frame, textvariable=font_color_var, width=12).grid(row=start_row+4,column=1,sticky=tk.W,padx=5,pady=3)
        ttk.Button(parent_frame, text="Choose...", command=lambda v=font_color_var: self.choose_color_for_var(v)).grid(row=start_row+4,column=2,sticky=tk.W,padx=2,pady=3)
        ttk.Button(parent_frame, text="Reset", command=lambda v=font_color_var: self.reset_color_for_var(v, DEFAULT_FONT_COLOR)).grid(row=start_row+4,column=3,sticky=tk.W,padx=2,pady=3)
        
        # Behaviors Font Size
        ttk.Label(parent_frame, text="Behaviors Font Size (pts):").grid(row=start_row+5,column=0,sticky=tk.W,padx=5,pady=3)
        behavior_font_size_var = tk.IntVar(value=self.settings.get('behavior_font_size', DEFAULT_FONT_SIZE))
        setattr(self, 'behavior_font_size_var', behavior_font_size_var)
        ttk.Spinbox(parent_frame, from_=6, to=24, textvariable=behavior_font_size_var, width=5).grid(row=start_row+5,column=1,sticky=tk.W,padx=5,pady=3)

    def reset_color_for_var(self, color_var, default): # Helper for color reset buttons in settings
        color_var.set(default) # Reset to empty string

    def choose_color_for_var(self, color_var): # Helper for color choosers in settings
        initial_color = color_var.get()
        if not initial_color: # If empty, pick a default to show in chooser
            if "fill" in color_var._name: initial_color = DEFAULT_BOX_FILL_COLOR
            elif "outline" in color_var._name: initial_color = DEFAULT_BOX_OUTLINE_COLOR
            else: initial_color = DEFAULT_FONT_COLOR
        
        color_code = colorchooser.askcolor(initial_color, title="Choose color", parent=self)
        if color_code and color_code[1]: color_var.set(color_code[1])

    def choose_color_for_canvas(self, color_var): # Helper for color choosers in settings
        initial_color = color_var.get()
        if initial_color == "Default": initial_color = None
        if not initial_color: # If empty, pick a default to show in chooser
            if "fill" in color_var._name: initial_color = DEFAULT_BOX_FILL_COLOR
            elif "outline" in color_var._name: initial_color = DEFAULT_BOX_OUTLINE_COLOR
            else: initial_color = DEFAULT_FONT_COLOR
        
        color_code = colorchooser.askcolor(initial_color, title="Choose color", parent=self)
        if color_code and color_code[1]: color_var.set(color_code[1])
        
    """def reset_canvas_color(self, button):
        button.set("Default")"""

    # --- Methods for managing custom lists ---
    def populate_conditional_rules_listbox(self):
        self.rules_listbox.delete(0, tk.END)
        for i, rule in enumerate(self.settings.get("conditional_formatting_rules", [])):
            desc = f"Rule {i+1}: Type='{rule.get('type', 'Unknown')}'"
            if rule['type'] == 'group':
                group_name = self.app.student_groups.get(rule.get('group_id'), {}).get('name', 'Unknown Group')
                desc += f", Group='{group_name}'"
            elif rule['type'] == 'behavior_count':
                desc += f", Behavior='{rule.get('behavior_name', 'N/A')}', Count>={rule.get('count_threshold',0)}, Hours={rule.get('time_window_hours',0)}"
            elif rule['type'] == 'quiz_score_threshold':
                desc += f", Quiz~'{rule.get('quiz_name_contains','Any')}', Score {rule.get('operator','N/A')} {rule.get('score_threshold_percent','N/A')}%"
            elif rule['type'] == 'quiz_mark_count':
                mark_name = "N/A"
                for mt in self.app.settings.get("quiz_mark_types", []):
                    if mt.get("id") == rule.get("mark_type_id"):
                        mark_name = mt.get("name"); break
                desc += f", Quiz~'{rule.get('quiz_name_contains','Any')}', Mark='{mark_name}', {rule.get('mark_operator','N/A')} {rule.get('mark_count_threshold','N/A')}"
            elif rule['type'] == 'live_quiz_response':
                desc += f", Quiz Response='{rule.get('quiz_response', 'N/A')}'"
            elif rule['type'] == 'live_homework_yes_no':
                hw_type_name = "N/A"
                for ht in self.app.all_homework_session_types: # These are dicts with 'id' and 'name'
                    if ht.get('id') == rule.get('homework_type_id'):
                        hw_type_name = ht.get('name'); break
                desc += f", HW Type='{hw_type_name}', Response='{rule.get('homework_response', 'N/A')}'"
            elif rule['type'] == 'live_homework_select':
                desc += f", HW Option='{rule.get('homework_option_name', 'N/A')}'"

            desc += f" -> Fill='{rule.get('color','None')}', Outline='{rule.get('outline','None')}', Style='{rule.get('application_style','stripe')}'"
            self.rules_listbox.insert(tk.END, desc)

    def add_conditional_rule(self):
        dialog = ConditionalFormattingRuleDialog(self.master_frame, self.app) # Pass app and correct parent
        if dialog.result:
            if "conditional_formatting_rules" not in self.settings: self.settings["conditional_formatting_rules"] = []
            self.settings["conditional_formatting_rules"].append(dialog.result)
            self.settings_changed_flag = True
            self.populate_conditional_rules_listbox()
    def edit_selected_conditional_rule(self):
        selected_idx = self.rules_listbox.curselection()
        if not selected_idx: messagebox.showinfo("No Selection", "Please select a rule to edit.", parent=self); return
        idx_to_edit = selected_idx[0]
        rule_copy = self.settings["conditional_formatting_rules"][idx_to_edit].copy()
        dialog = ConditionalFormattingRuleDialog(self, self.app, rule_to_edit=rule_copy)
        if dialog.result:
            self.settings["conditional_formatting_rules"][idx_to_edit] = dialog.result
            self.settings_changed_flag = True
            self.populate_conditional_rules_listbox()

    def remove_selected_conditional_rule(self):
        selected_indices = self.rules_listbox.curselection() # Will be tuple of indices
        if not selected_indices:
            messagebox.showinfo("No Selection", "Please select rule(s) to remove.", parent=self)
            return

        confirm_msg = f"Are you sure you want to remove {len(selected_indices)} selected conditional formatting rule(s)?"
        if messagebox.askyesno("Confirm Remove", confirm_msg, parent=self):
            # Iterate reversed to avoid index shifting issues when deleting multiple items
            for idx in sorted(selected_indices, reverse=True):
                del self.settings["conditional_formatting_rules"][idx]
            self.settings_changed_flag = True
            self.populate_conditional_rules_listbox()

    def bulk_edit_selected_rules(self):
        selected_indices = self.rules_listbox.curselection()
        if not selected_indices:
            messagebox.showinfo("No Selection", "Please select at least one rule to bulk edit.", parent=self)
            return

        # Pass a list of rule *copies* to the dialog to avoid direct modification before confirmation
        # Or pass indices and let dialog fetch/modify. For now, let's pass copies of rule dicts.
        # However, the dialog will modify the actual rules in self.settings["conditional_formatting_rules"]
        # if changes are applied.

        # The dialog will need access to the main 'app' instance for things like available modes,
        # and it will modify self.settings["conditional_formatting_rules"] directly or via a callback.
        # Let's design it to modify a temporary copy and then apply changes back.

        rules_to_edit_copies = [self.settings["conditional_formatting_rules"][i].copy() for i in selected_indices]

        # Placeholder for the new dialog - will be created in dialogs.py
        from dialogs import BulkEditConditionalRulesDialog # Assuming it will be in dialogs.py

        bulk_dialog = BulkEditConditionalRulesDialog(self, self.app, rules_to_edit_copies, selected_indices) # Pass self (SettingsDialog) as parent

        if bulk_dialog.changes_applied_flag: # If the dialog successfully applied changes
            # The bulk_dialog should have modified the original rules in self.settings
            # or returned the modified rules to be applied here.
            # Assuming the dialog modifies the rules in place for now.
            self.settings_changed_flag = True # Mark that settings have changed overall
            self.populate_conditional_rules_listbox() # Refresh the listbox
            messagebox.showinfo("Bulk Edit Complete", f"{len(selected_indices)} rules updated.", parent=self)
        else:
            # self.update_status("Bulk edit cancelled or no changes made.") # No status bar here
            pass


    def force_canvas_border_visi(self):
        self.force_canvas_border_btn.configure(state="normal" if self.canvas_border_var.get() == True else 'disabled')



    def _manage_custom_list_generic(self, listbox, custom_list_ref, item_type_name, add_func_name, edit_func_name):
        # This is a placeholder for a more generic dialog if needed, for now specific ones are used
        pass

    # Custom Behaviors (for Log Behavior dialog)
    def populate_custom_behaviors_listbox(self):
        self.custom_behaviors_listbox.delete(0, tk.END)
        for behavior_item in self.custom_behaviors_ref: # List of dicts or old strings
            name = behavior_item["name"] if isinstance(behavior_item, dict) else behavior_item
            self.custom_behaviors_listbox.insert(tk.END, name)
    def add_custom_behavior(self):
        if len(self.custom_behaviors_ref) >= MAX_CUSTOM_TYPES:
            messagebox.showwarning("Limit Reached", f"Maximum of {MAX_CUSTOM_TYPES} custom {item_type_name.lower()}s allowed.", parent=self); return
        name = simpledialog.askstring("Add Custom Behavior", "Enter name for the new behavior:", parent=self)
        if name and name.strip():
            name = name.strip()
            if any(cb_item == name or (isinstance(cb_item, dict) and cb_item.get("name") == name) for cb_item in self.custom_behaviors_ref):
                 messagebox.showwarning("Duplicate", f"Behavior '{name}' already exists.", parent=self); return
            self.custom_behaviors_ref.append({"name": name}) # Store as dict
            self.settings_changed_flag = True; self.app.save_custom_behaviors(); self.populate_custom_behaviors_listbox()
    def edit_selected_custom_behavior(self):
        sel_idx = self.custom_behaviors_listbox.curselection()
        if not sel_idx: messagebox.showinfo("No Selection", "Please select a behavior to edit.", parent=self); return
        idx = sel_idx[0]
        old_item = self.custom_behaviors_ref[idx]
        old_name = old_item["name"] if isinstance(old_item, dict) else old_item
        new_name = simpledialog.askstring("Edit Custom Behavior", "Enter new name:", initialvalue=old_name, parent=self)
        if new_name and new_name.strip():
            new_name = new_name.strip()
            if new_name != old_name and any(cb_item == new_name or (isinstance(cb_item, dict) and cb_item.get("name") == new_name and (idx != i if isinstance(cb_item,dict) else True) ) for i, cb_item in enumerate(self.custom_behaviors_ref)):
                 messagebox.showwarning("Duplicate", f"Behavior '{new_name}' already exists.", parent=self); return
            self.custom_behaviors_ref[idx] = {"name": new_name}
            self.settings_changed_flag = True; self.app.save_custom_behaviors(); self.populate_custom_behaviors_listbox()
    def remove_selected_custom_behavior(self):
        sel_idx = self.custom_behaviors_listbox.curselection()
        if not sel_idx: messagebox.showinfo("No Selection", "Please select a behavior to remove.", parent=self); return
        if messagebox.askyesno("Confirm Remove", "Remove selected custom behavior?", parent=self):
            del self.custom_behaviors_ref[sel_idx[0]]
            self.settings_changed_flag = True; self.app.save_custom_behaviors(); self.populate_custom_behaviors_listbox()
    """
    # Custom Homework Log Behaviors (for Manual Homework Log dialog options)
    def populate_custom_homework_log_behaviors_listbox(self):
        self.custom_hw_log_behaviors_listbox.delete(0, tk.END)
        for item in self.custom_homework_log_behaviors_ref:
            self.custom_hw_log_behaviors_listbox.insert(tk.END, item["name"])
    def add_custom_homework_log_behavior(self):
        if len(self.custom_homework_log_behaviors_ref) >= MAX_CUSTOM_TYPES:
             messagebox.showwarning("Limit Reached", f"Maximum of {MAX_CUSTOM_TYPES} custom homework log options allowed.", parent=self); return
        name = simpledialog.askstring("Add Homework Log Option", "Enter name for the new option (e.g., 'Excellent Effort'):", parent=self)
        if name and name.strip():
            name = name.strip()
            if any(item["name"] == name for item in self.custom_homework_log_behaviors_ref):
                 messagebox.showwarning("Duplicate", f"Option '{name}' already exists.", parent=self); return
            self.custom_homework_log_behaviors_ref.append({"name": name})
            self.settings_changed_flag = True; self.app.save_custom_homework_log_behaviors(); self.populate_custom_homework_log_behaviors_listbox()
    def edit_selected_custom_homework_log_behavior(self):
        sel_idx = self.custom_hw_log_behaviors_listbox.curselection()
        if not sel_idx: messagebox.showinfo("No Selection", "Please select an option to edit.", parent=self); return
        idx = sel_idx[0]; old_name = self.custom_homework_log_behaviors_ref[idx]["name"]
        new_name = simpledialog.askstring("Edit Homework Log Option", "Enter new name:", initialvalue=old_name, parent=self)
        if new_name and new_name.strip():
            new_name = new_name.strip()
            if new_name != old_name and any(item["name"] == new_name for i, item in enumerate(self.custom_homework_log_behaviors_ref) if i != idx):
                 messagebox.showwarning("Duplicate", f"Option '{new_name}' already exists.", parent=self); return
            self.custom_homework_log_behaviors_ref[idx]["name"] = new_name
            self.settings_changed_flag = True; self.app.save_custom_homework_log_behaviors(); self.populate_custom_homework_log_behaviors_listbox()
    def remove_selected_custom_homework_log_behavior(self):
        sel_idx = self.custom_hw_log_behaviors_listbox.curselection()
        if not sel_idx: messagebox.showinfo("No Selection", "Please select an option to remove.", parent=self); return
        if messagebox.askyesno("Confirm Remove", "Remove selected homework log option?", parent=self):
            del self.custom_homework_log_behaviors_ref[sel_idx[0]]
            self.settings_changed_flag = True; self.app.save_custom_homework_log_behaviors(); self.populate_custom_homework_log_behaviors_listbox()

    # Custom Homework Session Types (for Live Homework "Yes/No" mode)
    def populate_custom_homework_session_types_listbox(self):
        self.custom_hw_session_types_listbox.delete(0, tk.END)
        for item in self.custom_homework_session_types_ref: # list of {"id", "name"}
            self.custom_hw_session_types_listbox.insert(tk.END, item["name"])
    def add_custom_homework_session_type(self):
        if len(self.custom_homework_session_types_ref) >= MAX_CUSTOM_TYPES:
             messagebox.showwarning("Limit Reached", f"Maximum of {MAX_CUSTOM_TYPES} custom homework types for sessions allowed.", parent=self); return
        name = simpledialog.askstring("Add Homework Session Type", "Enter name for the new type (e.g., 'Project Milestone 1'):", parent=self)
        if name and name.strip():
            name = name.strip()
            if any(item["name"] == name for item in self.custom_homework_session_types_ref):
                 messagebox.showwarning("Duplicate", f"Type '{name}' already exists.", parent=self); return
            type_id_str, next_id_val = self.app.get_new_custom_homework_type_id()
            self.app.settings["next_custom_homework_type_id_num"] = next_id_val # Commit ID usage
            self.custom_homework_session_types_ref.append({"id": type_id_str, "name": name})
            self.settings_changed_flag = True; self.app.save_custom_homework_session_types(); self.populate_custom_homework_session_types_listbox()
    def edit_selected_custom_homework_session_type(self):
        sel_idx = self.custom_hw_session_types_listbox.curselection()
        if not sel_idx: messagebox.showinfo("No Selection", "Please select a type to edit.", parent=self); return
        idx = sel_idx[0]; old_name = self.custom_homework_session_types_ref[idx]["name"]
        new_name = simpledialog.askstring("Edit Homework Session Type", "Enter new name:", initialvalue=old_name, parent=self)
        if new_name and new_name.strip():
            new_name = new_name.strip()
            if new_name != old_name and any(item["name"] == new_name for i, item in enumerate(self.custom_homework_session_types_ref) if i != idx):
                 messagebox.showwarning("Duplicate", f"Type '{new_name}' already exists.", parent=self); return
            self.custom_homework_session_types_ref[idx]["name"] = new_name
            self.settings_changed_flag = True; self.app.save_custom_homework_session_types(); self.populate_custom_homework_session_types_listbox()
    def remove_selected_custom_homework_session_type(self):
        sel_idx = self.custom_hw_session_types_listbox.curselection()
        if not sel_idx: messagebox.showinfo("No Selection", "Please select a type to remove.", parent=self); return
        if messagebox.askyesno("Confirm Remove", "Remove selected homework session type?", parent=self):
            del self.custom_homework_session_types_ref[sel_idx[0]]
            self.settings_changed_flag = True; self.app.save_custom_homework_session_types(); self.populate_custom_homework_session_types_listbox()
    """
    def manage_behavior_initials(self):
        dialog = ManageInitialsDialog(self, self.settings["behavior_initial_overrides"], self.app.all_behaviors, "Behavior/Quiz")
        if dialog.initials_changed: self.settings_changed_flag = True
    def manage_homework_initials(self): # New
        dialog = ManageInitialsDialog(self, self.settings["homework_initial_overrides"], self.app.all_homework_statuses, "Homework Log")
        if dialog.initials_changed: self.settings_changed_flag = True
    def manage_quiz_mark_types(self):
        dialog = ManageMarkTypesDialog(self, self.settings["quiz_mark_types"], "Quiz Mark Types", DEFAULT_QUIZ_MARK_TYPES)
        if dialog.mark_types_changed: self.settings_changed_flag = True
    def manage_homework_mark_types(self): # New
        dialog = ManageMarkTypesDialog(self, self.settings["homework_mark_types"], "Homework Mark Types", DEFAULT_HOMEWORK_MARK_TYPES)
        if dialog.mark_types_changed: self.settings_changed_flag = True
    def manage_live_homework_select_options(self):
        dialog = ManageLiveSelectOptionsDialog(self, self.settings.get("live_homework_select_mode_options", DEFAULT_HOMEWORK_SESSION_BUTTONS.copy()))
        if dialog.options_changed_flag:
            self.settings["live_homework_select_mode_options"] = dialog.current_options
            self.settings_changed_flag = True

    """def buttonbox(self):
        ttk.Button(self, text= "Ok", command=self.ok).grid(column=0,row=1)
        ttk.Button(self, text="Cancel", command=self.cancel).grid(column=1,row=1, padx=10)
    """
    
    
    def apply(self): # OK button of SettingsDialog
        if self.reset == False: # If reset button was pressed
            # General Tab
            self.settings["autosave_interval_ms"] = self.autosave_interval_var.get() * 1000
            self.settings["grid_snap_enabled"] = self.grid_snap_var.get()
            self.settings["grid_size"] = self.grid_size_var.get()
            self.settings["student_groups_enabled"] = self.groups_enabled_var.get()
            self.settings["show_zoom_level_display"] = self.show_zoom_var.get()
            self.settings["max_undo_history_days"] = self.max_undo_days_var.get()
            self.settings["theme"] = self.theme.get()
            self.settings["canvas_color"] = self.custom_canvas_color.get()
            self.app.theme_style_using = self.theme2
            self.settings["type_theme"] = self.style.get() if self.style.get() != "sun-valley (Default)" else "sv_ttk"
            self.app.type_theme = self.style.get() if self.style.get() != "sun-valley (Default)" else "sv_ttk"
            self.app.custom_canvas_color = self.custom_canvas_color.get()
            self.settings["always_show_box_management"] = self.show_management_var.get()
            self.settings["check_for_collisions"] = self.check_for_collisions_var.get()
            self.settings["show_canvas_border_lines"] = self.canvas_border_var.get()
            self.settings["force_canvas_border_lines"] = self.force_canvas_border_var.get()
            self.settings["allow_box_dragging"] = self.allow_box_dragging_var.get()

            # Canvas View Options from General Tab
            self.settings["show_rulers"] = self.show_rulers_var.get()
            self.settings["show_grid"] = self.show_grid_var.get()
            self.settings["grid_color"] = self.grid_color_var.get()
            self.settings["save_guides_to_file"] = self.save_guides_var.get()
            self.settings["guides_stay_when_rulers_hidden"] = self.persist_guides_toggle_var.get()
            self.settings["guides_color"] = self.guides_color_var.get()

            #print("Theme2", self.theme2)
            #print(self.theme.get(), "Get")
            # Student Display Tab
            self.settings["default_student_box_width"]=self.def_stud_w_var.get()
            self.settings["default_student_box_height"]=self.def_stud_h_var.get()
            self.settings["student_box_fill_color"]=self.student_box_fill_color_var.get()
            self.settings["student_box_outline_color"]=self.student_box_outline_color_var.get()
            self.settings["student_font_family"]=self.student_font_family_var.get()
            self.settings["student_font_size"]=self.student_font_size_var.get()
            self.settings["behavior_font_size"]=self.behavior_font_size_var.get()
            self.settings["student_font_color"]=self.student_font_color_var.get()
            
            self.settings["quiz_log_font_size"] = self.quiz_log_font_size_var.get()
            self.settings["homework_log_font_size"] = self.homework_log_font_size_var.get()
            self.settings["enable_text_background_panel"] = self.enable_text_panel_var.get() # New setting
            self.settings["always_show_text_background_panel"] = self.enable_text_panel_always_var.get()
            # Behavior/Quiz Log Tab
            self.settings["show_recent_incidents_on_boxes"] = self.show_recent_var.get()
            self.settings["num_recent_incidents_to_show"] = self.num_recent_var.get()
            self.settings["recent_incident_time_window_hours"] = self.time_window_var.get()
            self.settings["show_full_recent_incidents"] = self.show_full_recent_var.get()
            self.settings["reverse_incident_order"] = self.reverse_order_var.get()
            self.settings["default_quiz_name"] = self.def_quiz_name_var.get()
            self.settings["default_quiz_questions"] = self.def_quiz_q_var.get()
            self.settings["last_used_quiz_name_timeout_minutes"] = self.quiz_timeout_var.get()
            self.settings["show_recent_incidents_during_quiz"] = self.show_inc_quiz_var.get()
            # self.settings["combine_marks_for_display"] = self.combine_marks_display_var.get()
            # Homework Log Tab
            self.settings["show_recent_homeworks_on_boxes"] = self.show_recent_hw_var.get()
            self.settings["num_recent_homeworks_to_show"] = self.num_recent_hw_var.get()
            self.settings["recent_homework_time_window_hours"] = self.time_window_hw_var.get()
            self.settings["show_full_recent_homeworks"] = self.show_full_recent_hw_var.get()
            self.settings["reverse_homework_order"] = self.reverse_hw_order_var.get()
            self.settings["default_homework_name"] = self.def_hw_session_name_var.get()
            self.settings["live_homework_session_mode"] = self.live_hw_mode_var.get()
            self.settings["log_homework_marks_enabled"] = self.log_hw_marks_var.get()
            # Data & Export Tab
            self.settings["excel_export_separate_sheets_by_default"] = self.excel_sep_sheets_var.get()
            self.settings["excel_export_include_summaries_by_default"] = self.excel_inc_summary_var.get()
            self.settings["enable_excel_autosave"] = self.enable_excel_autosave_var.get()
            self.settings["output_dpi"] = self.export_image_spin.get()
            # Security Tab
            self.settings["password_on_open"] = self.pw_on_open_var.get()
            self.settings["password_on_edit_action"] = self.pw_on_edit_var.get()
            self.settings["password_auto_lock_enabled"] = self.pw_auto_lock_var.get()
            self.settings["password_auto_lock_timeout_minutes"] = self.pw_auto_lock_timeout_var.get()
        else:
            self.app.type_theme = "sun-valley-light" # Reset to default theme
            
        # Check if any significant setting actually changed by comparing with snapshot
        for key, initial_val in self.initial_settings_snapshot.items():
            current_val = self.settings.get(key)
            if isinstance(current_val, (list, dict)): # For mutable types, content comparison is needed
                if initial_val != current_val: # This might not catch all deep changes if not careful
                    self.settings_changed_flag = True; break
            elif initial_val != current_val:
                self.settings_changed_flag = True; break
        # If any custom list (behaviors, marks, etc.) was modified, their specific dialogs
        # would have set self.settings_changed_flag = True already.
        self.result = self.settings_changed_flag # Simpledialog will check this




# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    from seatingchartmain import SeatingChartApp
    import sv_ttk
    sv_ttk.set_theme("Light")
    app = SeatingChartApp(root)
    try:
        import darkdetect; import threading
        t = threading.Thread(target=darkdetect.listener, args=(app.theme_auto, ))
        t.daemon = True; t.start()
    except: pass
    root.mainloop()