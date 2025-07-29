import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import os
import sys
from datetime import datetime
from tkcalendar import DateEntry
try:
    from tkcalendar import DateEntryCustom
except ImportError:
    DateEntryCustom = DateEntry

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



class ExportFilterDialog(simpledialog.Dialog):
    # ... (updated for homework filters)
    def __init__(self, parent, students_dict, all_behaviors_list, all_homework_types_list, default_settings, earliest_date):
        self.students_dict = students_dict
        self.all_behaviors_list = sorted(list(set(all_behaviors_list)))
        self.all_homework_types_list = ((all_homework_types_list)) # New
        self.earliest_date=earliest_date
        self.default_settings = default_settings
        self.result = None
        super().__init__(parent, "Export Log Options")

    def body(self, master):
        frame = ttk.Frame(master); frame.pack(padx=10, pady=10)
        # Date Range
        date_frame = ttk.LabelFrame(frame, text="Date Range"); date_frame.grid(pady=5,column=0,row=0,columnspan=3, sticky="ew")
        ttk.Label(date_frame, text="Start Date:").grid(row=0, column=0, padx=5, pady=3, sticky=tk.W)
        self.start_date_var = tk.StringVar()
        #ttkcal = Calendar(firstweekday=calendar.SUNDAY)
        #ttkcal.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        if DateEntry: self.start_date_entry = DateEntryCustom(date_frame, textvariable=self.start_date_var, date_pattern='yyyy-mm-dd', width=12); print("Dateentry") # See DateEntryCustom for what to do
        else: self.start_date_entry = ttk.Entry(date_frame, textvariable=self.start_date_var, width=12)
        self.start_date_entry.grid(row=0, column=1, padx=5, pady=3)
        
        self.start_date_var.set(value=self.earliest_date)
        
        ttk.Label(date_frame, text="End Date:").grid(row=1, column=0, padx=5, pady=3, sticky=tk.W)
        self.end_date_var = tk.StringVar()
        
        if DateEntry: self.end_date_entry = DateEntry(date_frame, textvariable=self.end_date_var, date_pattern='yyyy-mm-dd', width=12)
        else: self.end_date_entry = ttk.Entry(date_frame, textvariable=self.end_date_var, width=12)
        self.end_date_entry.grid(row=1, column=1, padx=5, pady=3)
        ttk.Button(date_frame, text="Clear Dates", command=self.clear_dates).grid(row=1, column=2, rowspan=2, padx=5, pady=3)

        # Students
        student_frame = ttk.LabelFrame(frame, text="Students"); student_frame.grid(pady=5,column=0,row=1, sticky="nsew")
        self.student_filter_var = tk.StringVar(value="all")
        ttk.Radiobutton(student_frame, text="All Students", variable=self.student_filter_var, value="all", command=self.toggle_student_list_state).pack(anchor=tk.W)
        ttk.Radiobutton(student_frame, text="Selected Students:", variable=self.student_filter_var, value="specific", command=self.toggle_student_list_state).pack(anchor=tk.W)
        self.student_list_frame = ttk.Frame(student_frame)
        self.student_list_frame.pack(fill=tk.X, padx=(20,0))
        self.student_listbox = tk.Listbox(self.student_list_frame, selectmode=tk.MULTIPLE, height=5, exportselection=False)
        sorted_students = sorted(self.students_dict.values(), key=lambda s: (s['last_name'], s['first_name']))
        self.student_listbox_map = {} # display_name -> student_id
        for i, s_data in enumerate(sorted_students):
            display_name = f"{s_data['last_name']}, {s_data['first_name']}" + (f" ({s_data.get('nickname')})" if s_data.get('nickname') else "")
            self.student_listbox.insert(tk.END, display_name)
            self.student_listbox_map[display_name] = s_data["id"]
        self.student_listbox.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=(0,3))
        student_scroll = ttk.Scrollbar(self.student_list_frame, orient=tk.VERTICAL, command=self.student_listbox.yview)
        student_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=(0,3)); self.student_listbox.config(yscrollcommand=student_scroll.set)

        # Behaviors (for Behavior and Quiz logs)
        behavior_frame = ttk.LabelFrame(frame, text="Behavior/Quiz Types"); behavior_frame.grid(pady=5, padx=5, column=1,row=1, sticky="nsew")
        self.behavior_filter_var = tk.StringVar(value="all")
        ttk.Radiobutton(behavior_frame, text="All Behavior/Quiz Types", variable=self.behavior_filter_var, value="all", command=self.toggle_behavior_list_state).pack(anchor=tk.W)
        ttk.Radiobutton(behavior_frame, text="Selected Behavior/Quiz Types:", variable=self.behavior_filter_var, value="specific", command=self.toggle_behavior_list_state).pack(anchor=tk.W)
        self.behavior_list_frame = ttk.Frame(behavior_frame)
        self.behavior_list_frame.pack(fill=tk.X, padx=(20,0))
        self.behavior_listbox = tk.Listbox(self.behavior_list_frame, selectmode=tk.MULTIPLE, height=5, exportselection=False)
        for b_name in self.all_behaviors_list: self.behavior_listbox.insert(tk.END, b_name)
        self.behavior_listbox.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=(0,3))
        bh_scroll = ttk.Scrollbar(self.behavior_list_frame, orient=tk.VERTICAL, command=self.behavior_listbox.yview)
        bh_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=(0,3)); self.behavior_listbox.config(yscrollcommand=bh_scroll.set)

        # Homework Types (New)
        homework_frame = ttk.LabelFrame(frame, text="Homework Types"); homework_frame.grid(pady=5,padx=5,column=0,row=2,rowspan=2, sticky="new")
        self.homework_filter_var = tk.StringVar(value="all")
        ttk.Radiobutton(homework_frame, text="All Homework Types", variable=self.homework_filter_var, value="all", command=self.toggle_homework_list_state).pack(anchor=tk.W)
        ttk.Radiobutton(homework_frame, text="Selected Homework Types:", variable=self.homework_filter_var, value="specific", command=self.toggle_homework_list_state).pack(anchor=tk.W)
        self.homework_list_frame = ttk.Frame(homework_frame)
        self.homework_list_frame.pack(fill=tk.X, padx=(20,0))
        self.homework_listbox = tk.Listbox(self.homework_list_frame, selectmode=tk.MULTIPLE, height=5, exportselection=False)
        for hw_name in self.all_homework_types_list: self.homework_listbox.insert(tk.END, hw_name) # Use combined list of names
        self.homework_listbox.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=(0,3))
        hw_scroll = ttk.Scrollbar(self.homework_list_frame, orient=tk.VERTICAL, command=self.homework_listbox.yview)
        hw_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=(0,3)); self.homework_listbox.config(yscrollcommand=hw_scroll.set)


        # Log Type Inclusion
        include_frame = ttk.LabelFrame(frame, text="Include Log Types"); include_frame.grid(pady=5,column=1,row=2, sticky="nsew")
        self.include_behavior_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(include_frame, text="Behavior Logs", variable=self.include_behavior_var).pack(anchor=tk.W, padx=5)
        self.include_quiz_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(include_frame, text="Quiz Logs", variable=self.include_quiz_var).pack(anchor=tk.W, padx=5)
        self.include_homework_var = tk.BooleanVar(value=True) # New
        ttk.Checkbutton(include_frame, text="Homework Logs", variable=self.include_homework_var).pack(anchor=tk.W, padx=5)

        # Output Options
        output_options_frame = ttk.LabelFrame(frame, text="Excel Output Options"); output_options_frame.grid(pady=5, column=1,row=3, sticky="nsew")
        self.include_summaries_var = tk.BooleanVar(value=self.default_settings.get("excel_export_include_summaries_by_default", True))
        self.separate_sheets_var = tk.BooleanVar(value=self.default_settings.get("excel_export_separate_sheets_by_default", True))
        ttk.Checkbutton(output_options_frame, text="Include summary sheet", variable=self.include_summaries_var).pack(anchor=tk.W, padx=5)
        ttk.Checkbutton(output_options_frame, text="Separate sheets for Behavior, Quiz, Homework", variable=self.separate_sheets_var, command= self.toggle_master_log_btn).pack(anchor=tk.W, padx=5)
        self.master_log_var = tk.BooleanVar(value=self.default_settings.get("excel_export_master_log_by_default", True))
        self.master_log_btn = ttk.Checkbutton(output_options_frame, text="Include Master Log", variable=self.master_log_var)
        self.master_log_btn.pack(anchor=tk.W, padx=5)
        

        self.toggle_student_list_state(); self.toggle_behavior_list_state(); self.toggle_homework_list_state()
        return frame

    def clear_dates(self): self.start_date_var.set(""); self.end_date_var.set("")
    def toggle_student_list_state(self): self.student_listbox.config(state=tk.NORMAL if self.student_filter_var.get() == "specific" else tk.DISABLED)
    def toggle_behavior_list_state(self): self.behavior_listbox.config(state=tk.NORMAL if self.behavior_filter_var.get() == "specific" else tk.DISABLED)
    def toggle_homework_list_state(self): self.homework_listbox.config(state=tk.NORMAL if self.homework_filter_var.get() == "specific" else tk.DISABLED)
    #def toggle_master_log_btn(self): self.master_log_btn.pack(anchor=tk.W, padx=5) if self.separate_sheets_var.get() == True else self.master_log_btn.pack_forget()
    def toggle_master_log_btn(self): self.master_log_btn.configure(state='enabled') if self.separate_sheets_var.get() == True else self.master_log_btn.configure(state='disabled'); self.master_log_var.set(True)



    def apply(self):
        start_dt, end_dt = None, None
        try:
            if self.start_date_var.get(): start_dt = datetime.strptime(self.start_date_var.get(), '%Y-%m-%d').date()
            if self.end_date_var.get(): end_dt = datetime.strptime(self.end_date_var.get(), '%Y-%m-%d').date()
            if start_dt and end_dt and start_dt > end_dt:
                messagebox.showerror("Invalid Dates", "Start date cannot be after end date.", parent=self); return
        except ValueError: messagebox.showerror("Invalid Date Format", "Please use YYYY-MM-DD for dates.", parent=self); return

        selected_s_ids = [self.student_listbox_map[self.student_listbox.get(i)] for i in self.student_listbox.curselection()] if self.student_filter_var.get() == "specific" else []
        selected_b_names = [self.behavior_listbox.get(i) for i in self.behavior_listbox.curselection()] if self.behavior_filter_var.get() == "specific" else []
        selected_hw_names = [self.homework_listbox.get(i) for i in self.homework_listbox.curselection()] if self.homework_filter_var.get() == "specific" else [] # New

        if not (self.include_behavior_var.get() or self.include_quiz_var.get() or self.include_homework_var.get()):
            messagebox.showwarning("No Log Types", "Please select at least one log type to include.", parent=self); return

        self.result = {
            "start_date": start_dt, "end_date": end_dt,
            "selected_students": self.student_filter_var.get(), "student_ids": selected_s_ids,
            "selected_behaviors": self.behavior_filter_var.get(), "behaviors_list": selected_b_names,
            "selected_homework_types": self.homework_filter_var.get(), "homework_types_list": selected_hw_names, # New
            "include_behavior_logs": self.include_behavior_var.get(),
            "include_quiz_logs": self.include_quiz_var.get(),
            "include_homework_logs": self.include_homework_var.get(), # New
            "separate_sheets_by_log_type": self.separate_sheets_var.get(),
            "include_summaries": self.include_summaries_var.get(),
            "include_master_log": self.master_log_var.get()
        }


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