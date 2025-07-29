import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

import os
import sys

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



# --- Quiz Template Management ---
class ManageQuizTemplatesDialog(simpledialog.Dialog):
    def __init__(self, parent, app_instance):
        self.app = app_instance # Main application instance
        self.templates_changed_flag = False
        super().__init__(parent, "Manage Quiz Templates")

    def body(self, master):
        self.master_frame = master
        top_frame = ttk.Frame(master); top_frame.pack(pady=5, padx=5, fill=tk.X)
        ttk.Button(top_frame, text="Add New Quiz Template", command=self.add_template).pack(side=tk.LEFT, padx=5)

        self.canvas_templates = tk.Canvas(master, borderwidth=0, background="#ffffff")
        self.templates_scrollable_frame = ttk.Frame(self.canvas_templates)
        self.scrollbar_templates = ttk.Scrollbar(master, orient="vertical", command=self.canvas_templates.yview)
        self.canvas_templates.configure(yscrollcommand=self.scrollbar_templates.set)

        self.scrollbar_templates.pack(side="right", fill="y")
        self.canvas_templates.pack(side="left", fill="both", expand=True)
        self.canvas_templates.create_window((0,0), window=self.templates_scrollable_frame, anchor="nw", tags="self.templates_scrollable_frame")

        self.templates_scrollable_frame.bind("<Configure>", lambda e: self.canvas_templates.configure(scrollregion=self.canvas_templates.bbox("all")))
        self.canvas_templates.bind('<MouseWheel>', self._on_mousewheel_templates)
        
        self.populate_templates_list()
        return self.templates_scrollable_frame

    def _on_mousewheel_templates(self, event):
        if event.delta: self.canvas_templates.yview_scroll(int(-1*(event.delta/120)), "units")
        else: self.canvas_templates.yview_scroll(1 if event.num == 5 else -1, "units")

    def populate_templates_list(self):
        for widget in self.templates_scrollable_frame.winfo_children(): widget.destroy()
        if not self.app.quiz_templates:
            ttk.Label(self.templates_scrollable_frame, text="No quiz templates created yet.").pack(pady=10)
            return

        sorted_templates = sorted(self.app.quiz_templates.items(), key=lambda item: item[1]['name'])
        for tpl_id, tpl_data in sorted_templates:
            tpl_frame = ttk.Frame(self.templates_scrollable_frame, padding=5, relief=tk.RIDGE, borderwidth=1)
            tpl_frame.pack(fill=tk.X, pady=3, padx=3)
            
            summary = f"{tpl_data['name']} ({tpl_data.get('num_questions', 'N/A')} Qs)"
            ttk.Label(tpl_frame, text=summary, width=40, anchor=tk.W).pack(side=tk.LEFT, padx=5)
            ttk.Button(tpl_frame, text="Edit", command=lambda tid=tpl_id: self.edit_template(tid)).pack(side=tk.LEFT, padx=3)
            ttk.Button(tpl_frame, text="Delete", command=lambda tid=tpl_id: self.delete_template(tid)).pack(side=tk.LEFT, padx=3)

    def add_template(self):
        dialog = QuizTemplateEditDialog(self, self.app, template_data=None) # Pass self as parent
        if dialog.result_template_data:
            template_id_str, next_id_val = self.app.get_new_quiz_template_id()
            
            # Check for name collision BEFORE committing ID
            if any(t['name'].lower() == dialog.result_template_data['name'].lower() for t in self.app.quiz_templates.values()):
                messagebox.showwarning("Duplicate Name", f"A quiz template named '{dialog.result_template_data['name']}' already exists.", parent=self)
                return
            
            self.app.next_quiz_template_id_num = next_id_val # Commit ID usage
            self.app.quiz_templates[template_id_str] = dialog.result_template_data
            self.templates_changed_flag = True
            self.populate_templates_list()

    def edit_template(self, template_id):
        if template_id not in self.app.quiz_templates: return
        current_template_data = self.app.quiz_templates[template_id]
        dialog = QuizTemplateEditDialog(self, self.app, template_data=current_template_data.copy(), existing_template_id=template_id)
        if dialog.result_template_data:
            # Check for name collision with OTHER templates
            if any(tid != template_id and t_data['name'].lower() == dialog.result_template_data['name'].lower() for tid, t_data in self.app.quiz_templates.items()):
                 messagebox.showwarning("Duplicate Name", f"Another quiz template named '{dialog.result_template_data['name']}' already exists. Edit cancelled.", parent=self)
                 return

            self.app.quiz_templates[template_id] = dialog.result_template_data
            self.templates_changed_flag = True
            self.populate_templates_list()

    def delete_template(self, template_id):
        if template_id not in self.app.quiz_templates: return
        tpl_name = self.app.quiz_templates[template_id]["name"]
        if messagebox.askyesno("Confirm Delete", f"Delete quiz template '{tpl_name}'?", parent=self):
            del self.app.quiz_templates[template_id]
            self.templates_changed_flag = True
            self.populate_templates_list()

    def apply(self): # OK button
        self.result = self.templates_changed_flag


class QuizTemplateEditDialog(simpledialog.Dialog):
    def __init__(self, parent_dialog, app_instance, template_data=None, existing_template_id=None):
        self.app = app_instance
        self.template_data_initial = template_data or {} # If editing, this is a copy
        self.existing_template_id = existing_template_id # Used to avoid name collision with self
        self.result_template_data = None # Populated on successful apply
        self.mark_entry_vars_tpl = {} # {mark_type_id: StringVar}
        title = "Edit Quiz Template" if template_data else "Add New Quiz Template"
        super().__init__(parent_dialog, title)

    def body(self, master):
        main_frame = ttk.Frame(master); main_frame.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
        
        name_frame = ttk.Frame(main_frame); name_frame.pack(fill=tk.X, pady=3)
        ttk.Label(name_frame, text="Template Name:").pack(side=tk.LEFT, padx=5)
        self.tpl_name_var = tk.StringVar(value=self.template_data_initial.get("name", ""))
        self.tpl_name_entry = ttk.Entry(name_frame, textvariable=self.tpl_name_var, width=35)
        self.tpl_name_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        num_q_frame = ttk.Frame(main_frame); num_q_frame.pack(fill=tk.X, pady=3)
        ttk.Label(num_q_frame, text="Number of Questions:").pack(side=tk.LEFT, padx=5)
        self.tpl_num_q_var = tk.StringVar(value=str(self.template_data_initial.get("num_questions", self.app.settings.get("default_quiz_questions",10))))
        self.tpl_num_q_spinbox = ttk.Spinbox(num_q_frame, from_=1, to=200, textvariable=self.tpl_num_q_var, width=5)
        self.tpl_num_q_spinbox.pack(side=tk.LEFT, padx=5)

        marks_frame = ttk.LabelFrame(main_frame, text="Default Marks (per question, if applicable)"); marks_frame.pack(pady=5, fill=tk.BOTH, expand=True)
        cols = 2
        current_col, current_row = 0,0
        default_marks_initial = self.template_data_initial.get("default_marks", {})
        for mt in self.app.settings.get("quiz_mark_types", []):
            mt_id = mt["id"]; mt_name = mt["name"]
            ttk.Label(marks_frame, text=f"{mt_name}:").grid(row=current_row, column=current_col*2, sticky=tk.W, padx=5, pady=2)
            var = tk.StringVar(value=str(default_marks_initial.get(mt_id, ""))) # "" if not set, or default_points
            self.mark_entry_vars_tpl[mt_id] = var
            entry = ttk.Entry(marks_frame, textvariable=var, width=8)
            entry.grid(row=current_row, column=current_col*2 + 1, sticky=tk.EW, padx=5, pady=2)
            current_col += 1
            if current_col >= cols: current_col = 0; current_row += 1
        for i in range(cols*2): marks_frame.grid_columnconfigure(i, weight=1 if i%2==1 else 0)
        
        return self.tpl_name_entry # Initial focus

    def apply(self):
        name = self.tpl_name_var.get().strip()
        if not name: messagebox.showerror("Input Required", "Template name cannot be empty.", parent=self); return
        try: num_q = int(self.tpl_num_q_var.get())
        except ValueError: messagebox.showerror("Invalid Input", "Number of questions must be an integer.", parent=self); return
        if num_q <=0: messagebox.showerror("Invalid Input", "Number of questions must be positive.", parent=self); return
        
        default_marks = {}
        for mt_id, var in self.mark_entry_vars_tpl.items():
            val_str = var.get().strip()
            if val_str: # Only store if set
                try: default_marks[mt_id] = int(val_str) # Store as int
                except ValueError: messagebox.showerror("Invalid Mark", f"Default mark for '{mt_id}' must be an integer or empty.", parent=self); return
        
        self.result_template_data = {"name": name, "num_questions": num_q, "default_marks": default_marks}

# --- Homework Template Management (New) ---
class ManageHomeworkTemplatesDialog(simpledialog.Dialog):
    def __init__(self, parent, app_instance):
        self.app = app_instance
        self.templates_changed_flag = False
        super().__init__(parent, "Manage Homework Templates")

    def body(self, master):
        self.master_frame = master
        top_frame = ttk.Frame(master); top_frame.pack(pady=5, padx=5, fill=tk.X)
        ttk.Button(top_frame, text="Add New Homework Template", command=self.add_template).pack(side=tk.LEFT, padx=5)

        self.canvas_templates = tk.Canvas(master, borderwidth=0, background="#ffffff")
        self.templates_scrollable_frame = ttk.Frame(self.canvas_templates)
        self.scrollbar_templates = ttk.Scrollbar(master, orient="vertical", command=self.canvas_templates.yview)
        self.canvas_templates.configure(yscrollcommand=self.scrollbar_templates.set)
        self.scrollbar_templates.pack(side="right", fill="y")
        self.canvas_templates.pack(side="left", fill="both", expand=True)
        self.canvas_templates.create_window((0,0), window=self.templates_scrollable_frame, anchor="nw", tags="self.templates_scrollable_frame")
        self.templates_scrollable_frame.bind("<Configure>", lambda e: self.canvas_templates.configure(scrollregion=self.canvas_templates.bbox("all")))
        self.canvas_templates.bind('<MouseWheel>', self._on_mousewheel_templates)
        self.populate_templates_list()
        return self.templates_scrollable_frame

    def _on_mousewheel_templates(self, event):
        if event.delta: self.canvas_templates.yview_scroll(int(-1*(event.delta/120)), "units")
        else: self.canvas_templates.yview_scroll(1 if event.num == 5 else -1, "units")

    def populate_templates_list(self):
        for widget in self.templates_scrollable_frame.winfo_children(): widget.destroy()
        if not self.app.homework_templates:
            ttk.Label(self.templates_scrollable_frame, text="No homework templates created yet.").pack(pady=10)
            return
        sorted_templates = sorted(self.app.homework_templates.items(), key=lambda item: item[1]['name'])
        for tpl_id, tpl_data in sorted_templates:
            tpl_frame = ttk.Frame(self.templates_scrollable_frame, padding=5, relief=tk.RIDGE, borderwidth=1)
            tpl_frame.pack(fill=tk.X, pady=3, padx=3)
            summary = f"{tpl_data['name']} ({tpl_data.get('num_items', 'N/A')} items)"
            ttk.Label(tpl_frame, text=summary, width=40, anchor=tk.W).pack(side=tk.LEFT, padx=5)
            ttk.Button(tpl_frame, text="Edit", command=lambda tid=tpl_id: self.edit_template(tid)).pack(side=tk.LEFT, padx=3)
            ttk.Button(tpl_frame, text="Delete", command=lambda tid=tpl_id: self.delete_template(tid)).pack(side=tk.LEFT, padx=3)

    def add_template(self):
        dialog = HomeworkTemplateEditDialog(self, self.app, template_data=None)
        if dialog.result_template_data:
            template_id_str, next_id_val = self.app.get_new_homework_template_id()
            if any(t['name'].lower() == dialog.result_template_data['name'].lower() for t in self.app.homework_templates.values()):
                messagebox.showwarning("Duplicate Name", f"A homework template named '{dialog.result_template_data['name']}' already exists.", parent=self)
                return
            self.app.next_homework_template_id_num = next_id_val
            self.app.homework_templates[template_id_str] = dialog.result_template_data
            self.templates_changed_flag = True
            self.populate_templates_list()

    def edit_template(self, template_id):
        if template_id not in self.app.homework_templates: return
        current_template_data = self.app.homework_templates[template_id]
        dialog = HomeworkTemplateEditDialog(self, self.app, template_data=current_template_data.copy(), existing_template_id=template_id)
        if dialog.result_template_data:
            if any(tid != template_id and t_data['name'].lower() == dialog.result_template_data['name'].lower() for tid, t_data in self.app.homework_templates.items()):
                 messagebox.showwarning("Duplicate Name", f"Another homework template named '{dialog.result_template_data['name']}' already exists. Edit cancelled.", parent=self)
                 return
            self.app.homework_templates[template_id] = dialog.result_template_data
            self.templates_changed_flag = True
            self.populate_templates_list()

    def delete_template(self, template_id):
        if template_id not in self.app.homework_templates: return
        tpl_name = self.app.homework_templates[template_id]["name"]
        if messagebox.askyesno("Confirm Delete", f"Delete homework template '{tpl_name}'?", parent=self):
            del self.app.homework_templates[template_id]
            self.templates_changed_flag = True
            self.populate_templates_list()

    def apply(self):
        self.result = self.templates_changed_flag


class HomeworkTemplateEditDialog(simpledialog.Dialog):
    def __init__(self, parent_dialog, app_instance, template_data=None, existing_template_id=None):
        self.app = app_instance
        self.template_data_initial = template_data or {}
        self.existing_template_id = existing_template_id
        self.result_template_data = None
        self.mark_entry_vars_hw_tpl = {} # {homework_mark_type_id: StringVar}
        title = "Edit Homework Template" if template_data else "Add New Homework Template"
        super().__init__(parent_dialog, title)

    def body(self, master):
        main_frame = ttk.Frame(master); main_frame.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
        name_frame = ttk.Frame(main_frame); name_frame.pack(fill=tk.X, pady=3)
        ttk.Label(name_frame, text="Template Name:").pack(side=tk.LEFT, padx=5)
        self.tpl_name_var = tk.StringVar(value=self.template_data_initial.get("name", ""))
        self.tpl_name_entry = ttk.Entry(name_frame, textvariable=self.tpl_name_var, width=35)
        self.tpl_name_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        num_items_frame = ttk.Frame(main_frame); num_items_frame.pack(fill=tk.X, pady=3)
        ttk.Label(num_items_frame, text="Number of Items/Tasks:").pack(side=tk.LEFT, padx=5)
        self.tpl_num_items_var = tk.StringVar(value=str(self.template_data_initial.get("num_items", 10))) # Default if not set
        self.tpl_num_items_spinbox = ttk.Spinbox(num_items_frame, from_=0, to=200, textvariable=self.tpl_num_items_var, width=5) # 0 if not applicable
        self.tpl_num_items_spinbox.pack(side=tk.LEFT, padx=5)

        marks_frame = ttk.LabelFrame(main_frame, text="Default Marks/Statuses"); marks_frame.pack(pady=5, fill=tk.BOTH, expand=True)
        cols = 2
        current_col, current_row = 0,0
        default_marks_initial = self.template_data_initial.get("default_marks", {})
        for hmt in self.app.settings.get("homework_mark_types", []):
            hmt_id = hmt["id"]; hmt_name = hmt["name"]
            ttk.Label(marks_frame, text=f"{hmt_name}:").grid(row=current_row, column=current_col*2, sticky=tk.W, padx=5, pady=2)
            var = tk.StringVar(value=str(default_marks_initial.get(hmt_id, ""))) # "" or default_points
            self.mark_entry_vars_hw_tpl[hmt_id] = var
            entry = ttk.Entry(marks_frame, textvariable=var, width=10) # Wider for potential text status
            entry.grid(row=current_row, column=current_col*2 + 1, sticky=tk.EW, padx=5, pady=2)
            current_col += 1
            if current_col >= cols: current_col = 0; current_row += 1
        for i in range(cols*2): marks_frame.grid_columnconfigure(i, weight=1 if i%2==1 else 0)
        return self.tpl_name_entry

    def apply(self):
        name = self.tpl_name_var.get().strip()
        if not name: messagebox.showerror("Input Required", "Template name cannot be empty.", parent=self); return
        try: num_items = int(self.tpl_num_items_var.get())
        except ValueError: messagebox.showerror("Invalid Input", "Number of items must be an integer (or 0 if not applicable).", parent=self); return
        if num_items < 0: messagebox.showerror("Invalid Input", "Number of items cannot be negative.", parent=self); return
        
        default_marks = {}
        for hmt_id, var in self.mark_entry_vars_hw_tpl.items():
            val_str = var.get().strip()
            if val_str: # Only store if set
                # Try to convert to float/int if numeric, else store as string (for statuses like "Done")
                try: default_marks[hmt_id] = float(val_str)
                except ValueError: default_marks[hmt_id] = val_str # Store as string if not purely numeric
        
        self.result_template_data = {"name": name, "num_items": num_items, "default_marks": default_marks}

class ManageInitialsDialog(simpledialog.Dialog):
    def __init__(self, parent, initials_overrides_dict, all_names_list, item_type_display_name):
        self.initials_overrides = initials_overrides_dict # Direct reference to app.settings[key]
        self.all_names = sorted(list(set(all_names_list)))
        self.item_type_name = item_type_display_name # e.g., "Behavior/Quiz" or "Homework Log"
        self.initials_changed = False
        self.entry_vars = {} # name -> StringVar
        super().__init__(parent, f"Manage Initials for {self.item_type_name}")

    def body(self, master):
        info_label = ttk.Label(master, text=f"Set custom initials for {self.item_type_name} types.\nLeave blank to use auto-generated initials.", justify=tk.LEFT)
        info_label.pack(pady=5, padx=5, anchor=tk.W)
        
        canvas_frame = ttk.Frame(master); canvas_frame.pack(fill=tk.BOTH, expand=True)
        self.canvas_initials = tk.Canvas(canvas_frame, borderwidth=0)
        scrollable_content_frame = ttk.Frame(self.canvas_initials)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas_initials.yview)
        self.canvas_initials.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y"); self.canvas_initials.pack(side="left", fill="both", expand=True)
        self.canvas_initials.create_window((0,0), window=scrollable_content_frame, anchor="nw")
        scrollable_content_frame.bind("<Configure>", lambda e: self.canvas_initials.configure(scrollregion=self.canvas_initials.bbox("all")))
        self.canvas_initials.bind('<MouseWheel>', lambda e: self.canvas_initials.yview_scroll(int(-1*(e.delta/120)), "units"))

        for name in self.all_names:
            item_frame = ttk.Frame(scrollable_content_frame); item_frame.pack(fill=tk.X, pady=1)
            ttk.Label(item_frame, text=name, width=30, anchor=tk.W).pack(side=tk.LEFT, padx=5)
            var = tk.StringVar(value=self.initials_overrides.get(name, ""))
            self.entry_vars[name] = var
            entry = ttk.Entry(item_frame, textvariable=var, width=5)
            entry.pack(side=tk.LEFT, padx=5)
        return canvas_frame # Or some specific entry if needed for focus

    def apply(self):
        for name, var in self.entry_vars.items():
            new_initial = var.get().strip()[:3] # Max 3 chars for initials
            if new_initial:
                if self.initials_overrides.get(name) != new_initial:
                    self.initials_overrides[name] = new_initial
                    self.initials_changed = True
            elif name in self.initials_overrides: # If blanked out and was set
                del self.initials_overrides[name]
                self.initials_changed = True
        # self.initials_overrides dictionary is modified directly.
        # self.initials_changed flag will be checked by SettingsDialog.


class ManageMarkTypesDialog(simpledialog.Dialog):
    def __init__(self, parent, current_mark_types_list, item_type_display_name, default_mark_types):
        self.mark_types_ref = current_mark_types_list # Direct reference, e.g., app.settings["quiz_mark_types"]
        self.item_type_name = item_type_display_name # "Quiz Mark Types" or "Homework Mark Types"
        self.default_mark_types_const = default_mark_types # The constant list for reset
        self.mark_types_changed = False
        super().__init__(parent, f"Manage {self.item_type_name}")

    def body(self, master):
        self.main_frame = master # To rebuild list
        button_frame = ttk.Frame(master); button_frame.pack(fill=tk.X, pady=5)
        ttk.Button(button_frame, text="Add New Mark Type", command=self.add_mark_type).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset to Defaults", command=self.reset_to_defaults).pack(side=tk.LEFT, padx=5)

        self.list_frame = ttk.Frame(master); self.list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.populate_mark_types_ui()
        return self.main_frame # For focus

    def populate_mark_types_ui(self):
        for widget in self.list_frame.winfo_children(): widget.destroy()
        
        headers = ["ID", "Name", "Default Points", "To Total?", "Bonus?"]
        for c, h_text in enumerate(headers):
            ttk.Label(self.list_frame, text=h_text, font=("",9,"bold")).grid(row=0,column=c,padx=3,pady=3,sticky=tk.W)

        self.mark_type_widgets = [] # Store refs to entry vars/widgets if needed for direct update
        
        for r_idx, mt_dict in enumerate(self.mark_types_ref, start=1):
            widgets_row = {}
            # ID (display only for defaults, editable for custom?) - For now, mostly fixed post-creation
            id_val = mt_dict.get("id", f"custom_{r_idx}")
            widgets_row["id_label"] = ttk.Label(self.list_frame, text=id_val, width=15); widgets_row["id_label"].grid(row=r_idx, column=0, padx=3, sticky=tk.W)
            
            # Name
            name_var = tk.StringVar(value=mt_dict.get("name","")); widgets_row["name_var"] = name_var
            name_entry = ttk.Entry(self.list_frame, textvariable=name_var, width=20); name_entry.grid(row=r_idx, column=1, padx=3, sticky=tk.EW)
            
            # Default Points
            points_var = tk.DoubleVar(value=mt_dict.get("default_points",0.0)); widgets_row["points_var"] = points_var
            points_spin = ttk.Spinbox(self.list_frame, from_=-100, to=100, increment=0.1, textvariable=points_var, width=6); points_spin.grid(row=r_idx, column=2, padx=3)

            # Contributes to Total (Bool) - Conditional
            if "contributes_to_total" in mt_dict or "Quiz" in self.item_type_name:
                to_total_var = tk.BooleanVar(value=mt_dict.get("contributes_to_total", True))
                widgets_row["to_total_var"] = to_total_var
                ttk.Checkbutton(self.list_frame, variable=to_total_var).grid(row=r_idx, column=3, padx=3)
            
            # Is Extra Credit (Bool) - Conditional
            if "is_extra_credit" in mt_dict or "Quiz" in self.item_type_name:
                is_bonus_var = tk.BooleanVar(value=mt_dict.get("is_extra_credit", False))
                widgets_row["is_bonus_var"] = is_bonus_var
                ttk.Checkbutton(self.list_frame, variable=is_bonus_var).grid(row=r_idx, column=4, padx=3)

            del_btn = ttk.Button(self.list_frame, text="X", command=lambda idx=r_idx-1: self.delete_mark_type_at_index(idx), width=3)
            del_btn.grid(row=r_idx, column=5, padx=3)
            self.mark_type_widgets.append(widgets_row) # Store the dict of vars/widgets for this row
        self.list_frame.grid_columnconfigure(1, weight=1) # Allow name entry to expand


    def add_mark_type(self):
        if len(self.mark_types_ref) >= MAX_CUSTOM_TYPES: # Or a specific limit for mark types
            messagebox.showwarning("Limit Reached", "Maximum number of mark types reached.", parent=self); return
        
        new_id_base = "custom_mark"
        new_id_suffix = 1
        while f"{new_id_base}_{new_id_suffix}" in (mt.get("id") for mt in self.mark_types_ref):
            new_id_suffix +=1
        
        new_mark = {
            "id": f"{new_id_base}_{new_id_suffix}", "name": "New Mark Type", "default_points": 0.0,
            "contributes_to_total": False, "is_extra_credit": False
        }
        self.mark_types_ref.append(new_mark)
        self.mark_types_changed = True
        self.populate_mark_types_ui()

    def delete_mark_type_at_index(self, index):
        if 0 <= index < len(self.mark_types_ref):
            # Check if it's a default one, prevent deletion (or handle carefully)
            # For now, allow deletion, user can reset to defaults
            if messagebox.askyesno("Confirm Delete", f"Delete mark type '{self.mark_types_ref[index]['name']}'?", parent=self):
                del self.mark_types_ref[index]
                self.mark_types_changed = True
                self.populate_mark_types_ui()
    
    def reset_to_defaults(self):
        if messagebox.askyesno("Confirm Reset", f"Reset all {self.item_type_name.lower()} to application defaults?", parent=self):
            self.mark_types_ref.clear()
            for default_item in self.default_mark_types_const:
                self.mark_types_ref.append(default_item.copy()) # Add copies
            self.mark_types_changed = True
            self.populate_mark_types_ui()

    def apply(self): # OK button
        # Update the list of dicts from the UI widgets
        updated_list = []
        for row_widgets in self.mark_type_widgets:
            # Get ID from label (it's not editable here, but needed for the dict)
            current_id = row_widgets["id_label"].cget("text")
            name = row_widgets["name_var"].get().strip()
            if not name:
                messagebox.showerror("Invalid Name", f"Mark type name for ID '{current_id}' cannot be empty.", parent=self)
                # To prevent dialog closing on error, simpledialog needs validate() to return false.
                # This is tricky here as apply() is called after validate().
                # For now, we'll allow it but it might lead to an empty name. Better: prevent empty.
                return # Or handle error state
            
            # Check for duplicate names before saving
            if any(item['name'] == name and item['id'] != current_id for item in updated_list):
                messagebox.showerror("Duplicate Name", f"Mark type name '{name}' is already used. Names must be unique.", parent=self)
                return

            new_item = {
                "id": current_id,
                "name": name,
                "default_points": row_widgets["points_var"].get(),
            }
            if "to_total_var" in row_widgets:
                new_item["contributes_to_total"] = row_widgets["to_total_var"].get()
            if "is_bonus_var" in row_widgets:
                new_item["is_extra_credit"] = row_widgets["is_bonus_var"].get()
            updated_list.append(new_item)
        
        # Check if actual changes were made before setting the flag
        if self.mark_types_ref != updated_list: # Simple list comparison
            self.mark_types_ref[:] = updated_list # Replace content of original list
            self.mark_types_changed = True
        
        # self.mark_types_changed flag is now set if there were modifications.

class ManageLiveSelectOptionsDialog(simpledialog.Dialog):
    def __init__(self, parent, current_options_list):
        self.current_options = [opt.copy() for opt in current_options_list] # Work on a copy
        self.options_changed_flag = False
        super().__init__(parent, "Manage 'Select' Mode Options for Live Homework")

    def body(self, master):
        self.main_frame = master
        ttk.Label(master, text="Define the buttons/options available in 'Select' mode for live homework sessions.", wraplength=350).pack(pady=5)
        
        button_frame = ttk.Frame(master); button_frame.pack(fill=tk.X, pady=5)
        ttk.Button(button_frame, text="Add New Option", command=self.add_option).pack(side=tk.LEFT, padx=5)

        self.list_frame = ttk.Frame(master); self.list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.populate_options_ui()
        return self.main_frame

    def populate_options_ui(self):
        for widget in self.list_frame.winfo_children(): widget.destroy()
        
        self.option_entry_vars = [] # List of StringVars for names

        for r_idx, option_dict in enumerate(self.current_options):
            option_frame = ttk.Frame(self.list_frame); option_frame.pack(fill=tk.X, pady=2)
            
            name_var = tk.StringVar(value=option_dict.get("name","")); self.option_entry_vars.append(name_var)
            name_entry = ttk.Entry(option_frame, textvariable=name_var, width=30)
            name_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
            
            del_btn = ttk.Button(option_frame, text="Remove", command=lambda idx=r_idx: self.delete_option_at_index(idx), width=8)
            del_btn.pack(side=tk.LEFT, padx=5)
        
        if not self.current_options:
            ttk.Label(self.list_frame, text="No options defined. Click 'Add New Option'.").pack(pady=10)

    def add_option(self):
        if len(self.current_options) >= MAX_CUSTOM_TYPES: # Use a reasonable limit
            messagebox.showwarning("Limit Reached", "Maximum number of 'Select' options reached.", parent=self); return
        
        new_name = simpledialog.askstring("New Option", "Enter name for the new option (e.g., 'Signed', 'Returned Late'):", parent=self)
        if new_name and new_name.strip():
            new_name_clean = new_name.strip()
            if any(opt.get("name","").lower() == new_name_clean.lower() for opt in self.current_options):
                messagebox.showwarning("Duplicate Name", f"An option named '{new_name_clean}' already exists.", parent=self); return
            self.current_options.append({"name": new_name_clean})
            self.options_changed_flag = True
            self.populate_options_ui()

    def delete_option_at_index(self, index):
        if 0 <= index < len(self.current_options):
            if messagebox.askyesno("Confirm Delete", f"Delete option '{self.current_options[index]['name']}'?", parent=self):
                del self.current_options[index]
                self.options_changed_flag = True
                self.populate_options_ui()

    def apply(self):
        updated_options = []
        for name_var in self.option_entry_vars:
            name = name_var.get().strip()
            if not name:
                messagebox.showerror("Invalid Name", "Option names cannot be empty.", parent=self); return
            if any(opt.get("name","") == name for opt in updated_options): # Check for duplicates within the new list
                messagebox.showerror("Duplicate Name", f"Option name '{name}' is duplicated in the list. Names must be unique.", parent=self); return
            updated_options.append({"name": name})
        
        # Compare with original to see if actual changes occurred
        # Simple comparison might fail if order changed but content is same.
        # For now, if any entry var changed from initial or list length changed, consider it changed.
        # The self.options_changed_flag handles additions/deletions. This apply covers edits.
        if self.current_options != updated_options: # If direct edits changed things
            self.options_changed_flag = True
        self.current_options = updated_options # Finalize list


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