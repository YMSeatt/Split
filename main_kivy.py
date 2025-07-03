import kivy
kivy.require('2.3.1') # replace with your Kivy version if needed

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line, PushMatrix, PopMatrix, Translate, Scale, InstructionGroup
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
from kivy.input.motionevent import MotionEvent
from kivy.utils import get_color_from_hex
from kivy.core.text import Label as CoreLabel
from kivy.properties import BooleanProperty, ObjectProperty, ListProperty, StringProperty, NumericProperty, DictProperty


import json
import os
import sys
import subprocess
from datetime import datetime, timedelta, date as datetime_date
from typing import IO, Any, Dict, List, Optional, Set, Tuple, Callable
import PIL.EpsImagePlugin
import PIL.ImageFile
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font as OpenpyxlFont, Alignment as OpenpyxlAlignment
from openpyxl.utils import get_column_letter
import re
import shutil
import zipfile
import csv
import PIL
from PIL import Image
import webbrowser

from plyer import filechooser
# from plyer import storagepath
# from plyer import uniqueid
# from plyer import vibrator


import threading
import io
import tempfile
from io import BytesIO

# --- Application Constants ---
APP_NAME = "BehaviorLogger"
APP_VERSION = "v54.0"
CURRENT_DATA_VERSION_TAG = "v9"

# --- Default Configuration ---
DEFAULT_STUDENT_BOX_WIDTH = 130
DEFAULT_STUDENT_BOX_HEIGHT = 80
MIN_ITEM_WIDTH = 20
MIN_ITEM_HEIGHT = 20
REBBI_DESK_WIDTH = 200
REBBI_DESK_HEIGHT = 100
DEFAULT_FONT_FAMILY = "Roboto"
DEFAULT_FONT_SIZE = 10
DEFAULT_FONT_COLOR = "black"
DEFAULT_BOX_FILL_COLOR = "skyblue"
DEFAULT_BOX_OUTLINE_COLOR = "blue"
DEFAULT_QUIZ_SCORE_FONT_COLOR = "darkgreen"
DEFAULT_QUIZ_SCORE_FONT_STYLE_BOLD = True
DEFAULT_HOMEWORK_SCORE_FONT_COLOR = "purple"
DEFAULT_HOMEWORK_SCORE_FONT_STYLE_BOLD = True
GROUP_COLOR_INDICATOR_SIZE = 12
DEFAULT_THEME = "System"
THEME_LIST = ["Light", "Dark", "System"]
DRAG_THRESHOLD = 5
DEFAULT_GRID_SIZE = 20
MAX_UNDO_HISTORY_DAYS = 90
LAYOUT_COLLISION_OFFSET = 5
RESIZE_HANDLE_SIZE = 8
RESIZE_HANDLE_TOUCH_PADDING = 4

def get_app_data_path(filename):
    app = App.get_running_app()
    if app:
        user_data_dir = app.user_data_dir
        if not os.path.exists(user_data_dir):
            os.makedirs(user_data_dir, exist_ok=True)
        return os.path.join(user_data_dir, filename)
    else:
        print("Warning: get_app_data_path called before Kivy app is running. Using CWD as fallback (not recommended for Android).")
        fallback_path = os.path.join(os.getcwd(), APP_NAME)
        if not os.path.exists(fallback_path):
             os.makedirs(fallback_path, exist_ok=True)
        return os.path.join(fallback_path, filename)

DATA_FILE_PATTERN = f"classroom_data_{CURRENT_DATA_VERSION_TAG}.json"
CUSTOM_BEHAVIORS_FILE_PATTERN = f"custom_behaviors_{CURRENT_DATA_VERSION_TAG}.json"
CUSTOM_HOMEWORK_TYPES_FILE_PATTERN = f"custom_homework_types_{CURRENT_DATA_VERSION_TAG}.json"
CUSTOM_HOMEWORK_STATUSES_FILE_PATTERN = f"custom_homework_statuses_{CURRENT_DATA_VERSION_TAG}.json"
AUTOSAVE_EXCEL_FILE_PATTERN = f"autosave_log_{CURRENT_DATA_VERSION_TAG}.xlsx"
LAYOUT_TEMPLATES_DIR_NAME = "layout_templates"
STUDENT_GROUPS_FILE_PATTERN = f"student_groups_{CURRENT_DATA_VERSION_TAG}.json"
QUIZ_TEMPLATES_FILE_PATTERN = f"quiz_templates_{CURRENT_DATA_VERSION_TAG}.json"
HOMEWORK_TEMPLATES_FILE_PATTERN = f"homework_templates_{CURRENT_DATA_VERSION_TAG}.json"

DATA_FILE = ""
CUSTOM_BEHAVIORS_FILE = ""
CUSTOM_HOMEWORK_TYPES_FILE = ""
CUSTOM_HOMEWORK_STATUSES_FILE = ""
AUTOSAVE_EXCEL_FILE = ""
LAYOUT_TEMPLATES_DIR = ""
STUDENT_GROUPS_FILE = ""
QUIZ_TEMPLATES_FILE = ""
HOMEWORK_TEMPLATES_FILE = ""
LOCK_FILE_PATH = ""
IMAGENAMEW = "export_layout_as_image_helper"

DEFAULT_BEHAVIORS_LIST = ["Talking", "Off Task", "Out of Seat", "Uneasy", "Placecheck", "Great Participation", "Called On", "Complimented", "Fighting", "Other"]
DEFAULT_HOMEWORK_TYPES_LIST = ["Reading Assignment", "Worksheet", "Math Problems", "Project Work", "Study for Test"]
DEFAULT_HOMEWORK_LOG_BEHAVIORS = ["Done", "Not Done", "Partially Done", "Signed", "Returned", "Late", "Excellent Work"]
DEFAULT_HOMEWORK_SESSION_BUTTONS = [{"name": "Done"}, {"name": "Not Done"}, {"name": "Signed"}, {"name": "Returned"}]
DEFAULT_HOMEWORK_SESSION_BUTTONS2 = ["Done", "Not Done", "Signed", "Returned"]
DEFAULT_HOMEWORK_STATUSES = ["Done", "Not Done", "Partially Done", "Signed", "Returned", "Late", "Excellent Work"]
DEFAULT_GROUP_COLORS = ["#FFADAD", "#FFD6A5", "#FDFFB6", "#CAFFBF", "#9BF6FF", "#A0C4FF", "#BDB2FF", "#FFC6FF", "#E0E0E0"]
DEFAULT_QUIZ_MARK_TYPES = [
    {"id": "mark_correct", "name": "Correct", "contributes_to_total": True, "is_extra_credit": False, "default_points": 1},
    {"id": "mark_incorrect", "name": "Incorrect", "contributes_to_total": True, "is_extra_credit": False, "default_points": 0},
    {"id": "mark_partial", "name": "Partial Credit", "contributes_to_total": True, "is_extra_credit": False, "default_points": 0.5},
    {"id": "extra_credit", "name": "Bonus", "contributes_to_total": False, "is_extra_credit": True, "default_points": 1}
]
DEFAULT_HOMEWORK_MARK_TYPES = [
    {"id": "hmark_complete", "name": "Complete", "default_points": 10},
    {"id": "hmark_incomplete", "name": "Incomplete", "default_points": 5},
    {"id": "hmark_notdone", "name": "Not Done", "default_points": 0},
    {"id": "hmark_effort", "name": "Effort Score (1-5)", "default_points": 3}
]
MAX_CUSTOM_TYPES = 90
MASTER_RECOVERY_PASSWORD_HASH = "d3c01af653d8940fc36ea1e1f33a8dc03f47dd864d2cd0d8814e2643fa37e70de0a2228e58d7d591eb2f124e2f4f9ff7c98686f4f5da3de6bbfc0267db3c1a0e"

# --- Kivy Command Classes ---
class Command:
    def __init__(self, app_logic):
        self.app_logic = app_logic
        self.timestamp = datetime.now().isoformat()
    def execute(self): raise NotImplementedError
    def undo(self): raise NotImplementedError
    def to_dict(self): return {"type": self.__class__.__name__, "timestamp": self.timestamp}
    @staticmethod
    def from_dict(app_logic, data: Dict[str, Any]) -> Any:
        command_type = data.get("type")
        command_classes = {
            "AddItemCommand": AddItemCommand, "DeleteItemCommand": DeleteItemCommand,
            "EditItemCommand": EditItemCommand, "MoveItemsCommand": MoveItemsCommand,
            "ChangeItemsSizeCommand": ChangeItemsSizeCommand, "LogEntryCommand": LogEntryCommand,
            "LogHomeworkEntryCommand": LogHomeworkEntryCommand, "MarkLiveQuizQuestionCommand": MarkLiveQuizQuestionCommand,
            "MarkLiveHomeworkCommand": MarkLiveHomeworkCommand, "ChangeStudentStyleCommand": ChangeStudentStyleCommand,
            "ManageStudentGroupCommand": ManageStudentGroupCommand,
        }
        cls = command_classes.get(command_type)
        if cls and hasattr(cls, 'from_dict_data'): return cls.from_dict_data(app_logic, data)
        print(f"Warning: Unknown or non-deserializable command type '{command_type}' in from_dict.")
        return None

class AddItemCommand(Command):
    def __init__(self, app_logic, item_id, item_type, item_data, original_next_id_num_for_type):
        super().__init__(app_logic)
        self.item_id = item_id; self.item_type = item_type; self.item_data = item_data.copy()
        self.original_next_id_num_for_type = original_next_id_num_for_type
        self.data_key_in_settings = f"next_{item_type}_id_num"
    def execute(self):
        ds = self.app_logic.students if self.item_type == "student" else self.app_logic.furniture
        ds[self.item_id] = self.item_data
        if self.item_type == "student":
            self.app_logic.next_student_id_num = self.item_data.get("original_next_id_num_after_add", self.app_logic.next_student_id_num)
            self.app_logic.settings[self.data_key_in_settings] = self.app_logic.next_student_id_num
        elif self.item_type == "furniture":
            self.app_logic.next_furniture_id_num = self.item_data.get("original_next_id_num_after_add", self.app_logic.next_furniture_id_num)
            self.app_logic.settings[self.data_key_in_settings] = self.app_logic.next_furniture_id_num
        if hasattr(self.app_logic.app, 'seating_canvas_widget'): self.app_logic.app.seating_canvas_widget.redraw_all_items_on_canvas()
        self.app_logic.update_status(f"{self.item_type.capitalize()} '{self.item_data.get('full_name', self.item_data.get('name'))}' added.")
    def undo(self):
        ds = self.app_logic.students if self.item_type == "student" else self.app_logic.furniture
        if self.item_id in ds: del ds[self.item_id]
        if self.item_type == "student":
            self.app_logic.next_student_id_num = self.original_next_id_num_for_type
            self.app_logic.settings[self.data_key_in_settings] = self.app_logic.next_student_id_num
        elif self.item_type == "furniture":
            self.app_logic.next_furniture_id_num = self.original_next_id_num_for_type
            self.app_logic.settings[self.data_key_in_settings] = self.app_logic.next_furniture_id_num
        if hasattr(self.app_logic.app, 'seating_canvas_widget'): self.app_logic.app.seating_canvas_widget.redraw_all_items_on_canvas()
        self.app_logic.update_status(f"Undo: Added {self.item_type} '{self.item_data.get('full_name', self.item_data.get('name'))}' removed.")
    def to_dict(self): d = super().to_dict(); d.update({"item_id": self.item_id, "item_type": self.item_type, "item_data": self.item_data, "original_next_id_num_for_type": self.original_next_id_num_for_type}); return d
    @classmethod
    def from_dict_data(cls, app_logic, data): return cls(app_logic, data["item_id"], data["item_type"], data["item_data"], data["original_next_id_num_for_type"])

class LogEntryCommand(Command):
    def __init__(self, app_logic, log_entry, student_id, timestamp=None):
        super().__init__(app_logic); self.log_entry = log_entry.copy(); self.student_id = student_id
        if timestamp: self.log_entry["timestamp"] = timestamp; self.timestamp = timestamp
    def execute(self):
        self.app_logic.behavior_log.append(self.log_entry)
        if hasattr(self.app_logic.app, 'seating_canvas_widget'): self.app_logic.app.seating_canvas_widget.redraw_all_items_on_canvas()
        self.app_logic.update_status(f"Logged: {self.log_entry.get('behavior', 'Log')} for {self.student_id}")
    def undo(self):
        try:
            self.app_logic.behavior_log.remove(self.log_entry)
            if hasattr(self.app_logic.app, 'seating_canvas_widget'): self.app_logic.app.seating_canvas_widget.redraw_all_items_on_canvas()
            self.app_logic.update_status(f"Undo: Log for {self.student_id} removed.")
        except ValueError: self.app_logic.update_status(f"Undo failed: Log entry for {self.student_id} not found.")
    def to_dict(self): d = super().to_dict(); d.update({"log_entry": self.log_entry, "student_id": self.student_id}); return d
    @classmethod
    def from_dict_data(cls, app_logic, data): return cls(app_logic, data["log_entry"], data["student_id"], timestamp=data.get("timestamp"))

class LogHomeworkEntryCommand(Command):
    def __init__(self, app_logic, log_entry, student_id, timestamp=None):
        super().__init__(app_logic); self.log_entry = log_entry.copy(); self.student_id = student_id
        if timestamp: self.log_entry["timestamp"] = timestamp; self.timestamp = timestamp
    def execute(self):
        self.app_logic.homework_log.append(self.log_entry)
        if hasattr(self.app_logic.app, 'seating_canvas_widget'): self.app_logic.app.seating_canvas_widget.redraw_all_items_on_canvas()
        self.app_logic.update_status(f"Logged HW: {self.log_entry.get('homework_type', 'Entry')} for {self.student_id}")
    def undo(self):
        try:
            self.app_logic.homework_log.remove(self.log_entry)
            if hasattr(self.app_logic.app, 'seating_canvas_widget'): self.app_logic.app.seating_canvas_widget.redraw_all_items_on_canvas()
            self.app_logic.update_status(f"Undo: HW Log for {self.student_id} removed.")
        except ValueError: self.app_logic.update_status(f"Undo failed: HW Log entry for {self.student_id} not found.")
    def to_dict(self): d = super().to_dict(); d.update({"log_entry": self.log_entry, "student_id": self.student_id}); return d
    @classmethod
    def from_dict_data(cls, app_logic, data): return cls(app_logic, data["log_entry"], data["student_id"], timestamp=data.get("timestamp"))

class DeleteItemCommand(Command):
    def __init__(self, app_logic, item_id, item_type, deleted_item_data, associated_behavior_logs=None, associated_homework_logs=None):
        super().__init__(app_logic); self.item_id = item_id; self.item_type = item_type; self.deleted_item_data = deleted_item_data.copy()
        self.associated_behavior_logs = [log.copy() for log in associated_behavior_logs] if associated_behavior_logs else []
        self.associated_homework_logs = [log.copy() for log in associated_homework_logs] if associated_homework_logs else []
        self.original_next_id_num_for_type = None
        if item_type == "student": self.original_next_id_num_for_type = app_logic.next_student_id_num
        elif item_type == "furniture": self.original_next_id_num_for_type = app_logic.next_furniture_id_num
    def execute(self):
        if self.item_type == "student":
            if self.item_id in self.app_logic.students: del self.app_logic.students[self.item_id]
            self.app_logic.behavior_log = [log for log in self.app_logic.behavior_log if log["student_id"] != self.item_id]
            self.app_logic.homework_log = [log for log in self.app_logic.homework_log if log["student_id"] != self.item_id]
            if self.item_id in self.app_logic.live_quiz_scores: del self.app_logic.live_quiz_scores[self.item_id]
            if self.item_id in self.app_logic.live_homework_scores: del self.app_logic.live_homework_scores[self.item_id]
            if self.item_id in self.app_logic._per_student_last_cleared: del self.app_logic._per_student_last_cleared[self.item_id]
        elif self.item_type == "furniture":
            if self.item_id in self.app_logic.furniture: del self.app_logic.furniture[self.item_id]
        if hasattr(self.app_logic.app, 'seating_canvas_widget'): self.app_logic.app.seating_canvas_widget.redraw_all_items_on_canvas()
        self.app_logic.update_status(f"Deleted {self.item_type} '{self.deleted_item_data.get('full_name', self.deleted_item_data.get('name', self.item_id))}'.")
    def undo(self):
        if self.item_type == "student":
            self.app_logic.students[self.item_id] = self.deleted_item_data
            self.app_logic.behavior_log.extend(self.associated_behavior_logs); self.app_logic.behavior_log.sort(key=lambda x: x["timestamp"])
            self.app_logic.homework_log.extend(self.associated_homework_logs); self.app_logic.homework_log.sort(key=lambda x: x["timestamp"])
            if self.original_next_id_num_for_type is not None:
                 self.app_logic.next_student_id_num = self.original_next_id_num_for_type
                 self.app_logic.settings[f"next_{self.item_type}_id_num"] = self.app_logic.next_student_id_num
        elif self.item_type == "furniture":
            self.app_logic.furniture[self.item_id] = self.deleted_item_data
            if self.original_next_id_num_for_type is not None:
                 self.app_logic.next_furniture_id_num = self.original_next_id_num_for_type
                 self.app_logic.settings[f"next_{self.item_type}_id_num"] = self.app_logic.next_furniture_id_num
        if hasattr(self.app_logic.app, 'seating_canvas_widget'): self.app_logic.app.seating_canvas_widget.redraw_all_items_on_canvas()
        self.app_logic.update_status(f"Undo: Deletion of {self.item_type} '{self.deleted_item_data.get('full_name', self.deleted_item_data.get('name', self.item_id))}' reverted.")
    def to_dict(self): d = super().to_dict(); d.update({"item_id": self.item_id, "item_type": self.item_type, "deleted_item_data": self.deleted_item_data, "associated_behavior_logs": self.associated_behavior_logs, "associated_homework_logs": self.associated_homework_logs, "original_next_id_num_for_type": self.original_next_id_num_for_type}); return d
    @classmethod
    def from_dict_data(cls, app_logic, data): return cls(app_logic, data["item_id"], data["item_type"], data["deleted_item_data"], data.get("associated_behavior_logs"), data.get("associated_homework_logs"))

class EditItemCommand(Command):
    def __init__(self, app_logic, item_id, item_type, old_item_data_snapshot, new_item_data_changes):
        super().__init__(app_logic); self.item_id = item_id; self.item_type = item_type; self.old_item_data_snapshot = old_item_data_snapshot.copy(); self.new_item_data_changes = new_item_data_changes.copy()
    def execute(self):
        ds = self.app_logic.students if self.item_type == "student" else self.app_logic.furniture
        if self.item_id in ds:
            for key, value in self.new_item_data_changes.items(): ds[self.item_id][key] = value
            if hasattr(self.app_logic.app, 'seating_canvas_widget'): self.app_logic.app.seating_canvas_widget.redraw_all_items_on_canvas()
            self.app_logic.update_status(f"Edited {self.item_type} '{ds[self.item_id].get('full_name', ds[self.item_id].get('name', self.item_id))}'.")
    def undo(self):
        ds = self.app_logic.students if self.item_type == "student" else self.app_logic.furniture
        if self.item_id in ds:
            ds[self.item_id] = self.old_item_data_snapshot.copy()
            if hasattr(self.app_logic.app, 'seating_canvas_widget'): self.app_logic.app.seating_canvas_widget.redraw_all_items_on_canvas()
            self.app_logic.update_status(f"Undo: Edit of {self.item_type} '{self.old_item_data_snapshot.get('full_name', self.old_item_data_snapshot.get('name', self.item_id))}' reverted.")
    def to_dict(self): d = super().to_dict(); d.update({"item_id": self.item_id, "item_type": self.item_type, "old_item_data_snapshot": self.old_item_data_snapshot, "new_item_data_changes": self.new_item_data_changes}); return d
    @classmethod
    def from_dict_data(cls, app_logic, data): return cls(app_logic, data["item_id"], data["item_type"], data["old_item_data_snapshot"], data["new_item_data_changes"])

class MoveItemsCommand(Command):
    def __init__(self, app_logic, items_move_data: List[Dict[str, Any]]):
        super().__init__(app_logic); self.items_move_data = [item.copy() for item in items_move_data]
    def _apply_positions(self, use_new_coords: bool):
        for item_info in self.items_move_data:
            item_id, item_type = item_info["id"], item_info["type"]
            data_source = self.app_logic.students if item_type == "student" else self.app_logic.furniture
            if item_id in data_source:
                data_source[item_id]["x"] = item_info["new_x"] if use_new_coords else item_info["old_x"]
                data_source[item_id]["y"] = item_info["new_y"] if use_new_coords else item_info["old_y"]
        if hasattr(self.app_logic.app, 'seating_canvas_widget'): self.app_logic.app.seating_canvas_widget.redraw_all_items_on_canvas()
    def execute(self): self._apply_positions(True); self.app_logic.update_status(f"Moved {len(self.items_move_data)} items.")
    def undo(self): self._apply_positions(False); self.app_logic.update_status(f"Undo: Movement of {len(self.items_move_data)} items reverted.")
    def to_dict(self): d = super().to_dict(); d["items_move_data"] = self.items_move_data; return d
    @classmethod
    def from_dict_data(cls, app_logic, data): return cls(app_logic, data["items_move_data"])

class ChangeItemsSizeCommand(Command):
    def __init__(self, app_logic, items_size_data: List[Dict[str, Any]]):
        super().__init__(app_logic); self.items_size_data = [item.copy() for item in items_size_data]
    def _apply_sizes(self, use_new_sizes: bool):
        for item_info in self.items_size_data:
            item_id, item_type = item_info["id"], item_info["type"]
            ds = self.app_logic.students if item_type == "student" else self.app_logic.furniture
            if item_id in ds:
                item_data = ds[item_id]
                w_key, h_key = ("new_w", "new_h") if use_new_sizes else ("old_w", "old_h")
                new_w, new_h = item_info[w_key], item_info[h_key]
                if item_type == "student":
                    if "style_overrides" not in item_data: item_data["style_overrides"] = {}
                    item_data["style_overrides"]["width"] = new_w; item_data["style_overrides"]["height"] = new_h
                item_data["width"] = new_w; item_data["height"] = new_h
        if hasattr(self.app_logic.app, 'seating_canvas_widget'): self.app_logic.app.seating_canvas_widget.redraw_all_items_on_canvas()
    def execute(self): self._apply_sizes(True); self.app_logic.update_status(f"Resized {len(self.items_size_data)} items.")
    def undo(self): self._apply_sizes(False); self.app_logic.update_status(f"Undo: Resize of {len(self.items_size_data)} items reverted.")
    def to_dict(self): d = super().to_dict(); d["items_size_data"] = self.items_size_data; return d
    @classmethod
    def from_dict_data(cls, app_logic, data): return cls(app_logic, data["items_size_data"])

class MarkLiveQuizQuestionCommand(Command):
    def __init__(self, app_logic, student_id, mark_action):
        super().__init__(app_logic); self.student_id = student_id; self.mark_action = mark_action; self.old_score_data = None
    def execute(self):
        if not self.app_logic.is_live_quiz_active or self.student_id not in self.app_logic.students: return
        self.old_score_data = self.app_logic.live_quiz_scores.get(self.student_id, {"correct":0, "total_asked":0, "marks_breakdown":{}}).copy()
        current_scores = self.app_logic.live_quiz_scores.setdefault(self.student_id, {"correct":0, "total_asked":0, "marks_breakdown":{}})
        current_scores["total_asked"] +=1
        mark_type_config = next((mt for mt in self.app_logic.settings.get("quiz_mark_types", []) if mt["id"] == self.mark_action), None)
        if mark_type_config:
            current_scores["marks_breakdown"][self.mark_action] = current_scores["marks_breakdown"].get(self.mark_action, 0) + 1
            if mark_type_config.get("default_points", 0) > 0 and not mark_type_config.get("is_extra_credit", False):
                 current_scores["correct"] += mark_type_config.get("default_points", 1)
        elif self.mark_action == "mark_correct": current_scores["correct"] +=1
        if hasattr(self.app_logic.app, 'seating_canvas_widget'): self.app_logic.app.seating_canvas_widget.redraw_all_items_on_canvas()
    def undo(self):
        if self.old_score_data is not None and self.student_id in self.app_logic.live_quiz_scores:
            self.app_logic.live_quiz_scores[self.student_id] = self.old_score_data
            if hasattr(self.app_logic.app, 'seating_canvas_widget'): self.app_logic.app.seating_canvas_widget.redraw_all_items_on_canvas()
    def to_dict(self): d = super().to_dict(); d.update({"student_id": self.student_id, "mark_action": self.mark_action, "old_score_data": self.old_score_data}); return d
    @classmethod
    def from_dict_data(cls, app_logic, data): cmd = cls(app_logic, data["student_id"], data["mark_action"]); cmd.old_score_data = data.get("old_score_data"); return cmd

class MarkLiveHomeworkCommand(Command):
    def __init__(self, app_logic, student_id, actions, session_mode):
        super().__init__(app_logic); self.student_id = student_id; self.actions = actions; self.session_mode = session_mode; self.old_hw_data_for_student = None
    def execute(self):
        if not self.app_logic.is_live_homework_active or self.student_id not in self.app_logic.students: return
        self.old_hw_data_for_student = self.app_logic.live_homework_scores.get(self.student_id, {}).copy()
        current_hw_data = self.app_logic.live_homework_scores.setdefault(self.student_id, {})
        if self.session_mode == "Yes/No":
            for action in self.actions: current_hw_data[action["type_id"]] = action["status"]
        elif self.session_mode == "Select": current_hw_data["selected_options"] = list(set(self.actions))
        if hasattr(self.app_logic.app, 'seating_canvas_widget'): self.app_logic.app.seating_canvas_widget.redraw_all_items_on_canvas()
    def undo(self):
        if self.old_hw_data_for_student is not None and self.student_id in self.app_logic.live_homework_scores:
            self.app_logic.live_homework_scores[self.student_id] = self.old_hw_data_for_student
        elif self.student_id in self.app_logic.live_homework_scores and self.old_hw_data_for_student is None :
             del self.app_logic.live_homework_scores[self.student_id]
        if hasattr(self.app_logic.app, 'seating_canvas_widget'): self.app_logic.app.seating_canvas_widget.redraw_all_items_on_canvas()
    def to_dict(self): d = super().to_dict(); d.update({"student_id": self.student_id, "actions": self.actions, "session_mode": self.session_mode, "old_hw_data_for_student": self.old_hw_data_for_student}); return d
    @classmethod
    def from_dict_data(cls, app_logic, data): cmd = cls(app_logic, data["student_id"], data["actions"], data["session_mode"]); cmd.old_hw_data_for_student = data.get("old_hw_data_for_student"); return cmd

class ChangeStudentStyleCommand(Command):
    def __init__(self, app_logic, student_id, property_name, old_value, new_value):
        super().__init__(app_logic); self.student_id = student_id; self.property_name = property_name; self.old_value = old_value; self.new_value = new_value
    def _apply_style(self, value_to_apply):
        student = self.app_logic.students.get(self.student_id)
        if not student: return
        if "style_overrides" not in student: student["style_overrides"] = {}
        if value_to_apply is None and self.property_name in student["style_overrides"]: del student["style_overrides"][self.property_name]
        elif value_to_apply is not None: student["style_overrides"][self.property_name] = value_to_apply
        if self.property_name == "width": student["width"] = value_to_apply if value_to_apply is not None else self.app_logic.settings.get("default_student_box_width")
        elif self.property_name == "height": student["height"] = value_to_apply if value_to_apply is not None else self.app_logic.settings.get("default_student_box_height")
        if hasattr(self.app_logic.app, 'seating_canvas_widget'): self.app_logic.app.seating_canvas_widget.redraw_all_items_on_canvas()
    def execute(self): self._apply_style(self.new_value); self.app_logic.update_status(f"Style '{self.property_name}' changed for {self.student_id}.")
    def undo(self): self._apply_style(self.old_value); self.app_logic.update_status(f"Undo: Style for {self.student_id} reverted.")
    def to_dict(self): d = super().to_dict(); d.update({"student_id": self.student_id, "property_name": self.property_name, "old_value": self.old_value, "new_value": self.new_value}); return d
    @classmethod
    def from_dict_data(cls, app_logic, data): return cls(app_logic, data["student_id"], data["property_name"], data["old_value"], data["new_value"])

class ManageStudentGroupCommand(Command):
    def __init__(self, app_logic, old_groups, new_groups, old_assignments, new_assignments, old_next_id, new_next_id):
        super().__init__(app_logic); self.old_groups_snapshot = old_groups; self.new_groups_snapshot = new_groups; self.old_student_assignments_snapshot = old_assignments; self.new_student_assignments_snapshot = new_assignments; self.old_next_group_id_num = old_next_id; self.new_next_group_id_num = new_next_id
    def _apply_state(self, groups_to_apply, assignments_to_apply, next_id_to_apply):
        self.app_logic.student_groups.clear(); self.app_logic.student_groups.update(groups_to_apply)
        for student_id, student_data in self.app_logic.students.items(): student_data["group_id"] = assignments_to_apply.get(student_id)
        self.app_logic.next_group_id_num = next_id_to_apply; self.app_logic.settings["next_group_id_num"] = next_id_to_apply
        if hasattr(self.app_logic.app, 'seating_canvas_widget'): self.app_logic.app.seating_canvas_widget.redraw_all_items_on_canvas()
    def execute(self): self._apply_state(self.new_groups_snapshot, self.new_student_assignments_snapshot, self.new_next_group_id_num); self.app_logic.update_status("Student groups updated.")
    def undo(self): self._apply_state(self.old_groups_snapshot, self.old_student_assignments_snapshot, self.old_next_group_id_num); self.app_logic.update_status("Undo: Group update reverted.")
    def to_dict(self): d = super().to_dict(); d.update({"old_groups": self.old_groups_snapshot, "new_groups": self.new_groups_snapshot, "old_assignments": self.old_student_assignments_snapshot, "new_assignments": self.new_student_assignments_snapshot, "old_next_id": self.old_next_group_id_num, "new_next_id": self.new_next_group_id_num}); return d
    @classmethod
    def from_dict_data(cls, app_logic, data): return cls(app_logic, data["old_groups"], data["new_groups"], data["old_assignments"], data["new_assignments"], data["old_next_id"], data["new_next_id"])
# --- End Kivy Command Classes ---


class SeatingChartAppLogic:
    # ... (All methods as defined in the previous version, including __init__, app_started, execute_command, undo/redo, dialog openers, etc.) ...
    def __init__(self, app_instance):
        self.app = app_instance
        global DATA_FILE, CUSTOM_BEHAVIORS_FILE, CUSTOM_HOMEWORK_TYPES_FILE, \
               CUSTOM_HOMEWORK_STATUSES_FILE, AUTOSAVE_EXCEL_FILE, LAYOUT_TEMPLATES_DIR, \
               STUDENT_GROUPS_FILE, QUIZ_TEMPLATES_FILE, HOMEWORK_TEMPLATES_FILE, LOCK_FILE_PATH
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
        self.all_homework_types = []
        self.custom_homework_types = []
        self.all_homework_statuses = []
        self.custom_homework_statuses = []
        self.all_homework_session_types = []
        self.last_excel_export_path = None
        self.selected_items: Set[str] = set()
        self.undo_stack: List[Command] = []
        self.redo_stack: List[Command] = []
        self.theme_style_using = "System"
        self.settings = self._get_default_settings()
        self.drag_data_canvas = {}
        self._potential_click_target = None
        self._drag_started_on_item = False
        self._recent_incidents_hidden_globally = False
        self._recent_homeworks_hidden_globally = False
        self._per_student_last_cleared = {}
        self.last_used_quiz_name = ""
        self.initial_num_questions = ""
        self.last_used_quiz_name_timestamp = None
        self.last_used_homework_name = ""
        self.initial_num_homework_items = ""
        self.last_used_homework_name_timestamp = None
        self.is_live_quiz_active = False
        self.current_live_quiz_name = ""
        self.live_quiz_scores = {}
        self.is_live_homework_active = False
        self.current_live_homework_name = ""
        self.live_homework_scores = {}
        self.current_zoom_level = 1.0
        self.canvas_orig_width = 2000
        self.canvas_orig_height = 1500
        self.custom_canvas_color = None
        self.zoom_level = 1.0
        self.pan_x = 0.0
        self.pan_y = 0.0
        self.student_widgets: Dict[str, StudentWidget] = {}
        self.furniture_widgets: Dict[str, FurnitureWidget] = {}
        self.edit_mode_var_kivy = BooleanProperty(False)
        self.undo_button_kivy: Optional[Button] = None
        self.redo_button_kivy: Optional[Button] = None


    def app_started(self):
        global DATA_FILE, CUSTOM_BEHAVIORS_FILE, CUSTOM_HOMEWORK_TYPES_FILE, \
               CUSTOM_HOMEWORK_STATUSES_FILE, AUTOSAVE_EXCEL_FILE, LAYOUT_TEMPLATES_DIR, \
               STUDENT_GROUPS_FILE, QUIZ_TEMPLATES_FILE, HOMEWORK_TEMPLATES_FILE, LOCK_FILE_PATH

        DATA_FILE = get_app_data_path(DATA_FILE_PATTERN)
        CUSTOM_BEHAVIORS_FILE = get_app_data_path(CUSTOM_BEHAVIORS_FILE_PATTERN)
        CUSTOM_HOMEWORK_TYPES_FILE = get_app_data_path(CUSTOM_HOMEWORK_TYPES_FILE_PATTERN)
        CUSTOM_HOMEWORK_STATUSES_FILE = get_app_data_path(CUSTOM_HOMEWORK_STATUSES_FILE_PATTERN)
        AUTOSAVE_EXCEL_FILE = get_app_data_path(AUTOSAVE_EXCEL_FILE_PATTERN)
        LAYOUT_TEMPLATES_DIR = get_app_data_path(LAYOUT_TEMPLATES_DIR_NAME)
        if not os.path.exists(LAYOUT_TEMPLATES_DIR):
            os.makedirs(LAYOUT_TEMPLATES_DIR, exist_ok=True)
        STUDENT_GROUPS_FILE = get_app_data_path(STUDENT_GROUPS_FILE_PATTERN)
        QUIZ_TEMPLATES_FILE = get_app_data_path(QUIZ_TEMPLATES_FILE_PATTERN)
        HOMEWORK_TEMPLATES_FILE = get_app_data_path(HOMEWORK_TEMPLATES_FILE_PATTERN)
        LOCK_FILE_PATH = get_app_data_path(f"{APP_NAME}.lock")

        self.load_custom_behaviors()
        self.load_custom_homework_types()
        self.load_custom_homework_statuses()
        self.load_student_groups()
        self.load_quiz_templates()
        self.load_homework_templates()

        self.update_all_behaviors()
        self.update_all_homework_types()
        self.update_all_homework_statuses()
        self.update_all_homework_session_types()

        self.load_data()
        self._ensure_next_ids()

        if hasattr(self.app, 'seating_canvas_widget') and self.app.seating_canvas_widget:
            self.app.seating_canvas_widget.redraw_all_items_on_canvas()
        self.update_status(f"App started. Data loaded from: {os.path.dirname(DATA_FILE if DATA_FILE else '.')}")
        self.update_undo_redo_buttons_kivy_state()


    def app_stopping(self):
        self.save_data_wrapper(source="app_stop")

    def execute_command(self, command: Command):
        try:
            command.execute()
            self.undo_stack.append(command)
            self.redo_stack.clear()
            self.update_undo_redo_buttons_kivy_state()
            self.save_data_wrapper(source="command_execution")
        except Exception as e:
            print(f"Command execution error: {e}\n{type(command)}")
            self.update_status(f"Error executing command: {e}")
            self.show_messagebox("error", "Command Error", f"Error: {e}")


    def undo_last_action(self):
        if self.undo_stack:
            command = self.undo_stack.pop()
            try:
                command.undo()
                self.redo_stack.append(command)
                self.save_data_wrapper(source="undo_command")
                self.update_status("Last action undone.")
            except Exception as e:
                self.show_messagebox("error", "Undo Error", f"Error undoing action: {e}")
                self.undo_stack.append(command)
            self.update_undo_redo_buttons_kivy_state()
        else:
            self.update_status("Nothing to undo.")

    def redo_last_action(self):
        if self.redo_stack:
            command = self.redo_stack.pop()
            try:
                command.execute()
                self.undo_stack.append(command)
                self.save_data_wrapper(source="redo_command")
                self.update_status("Last action redone.")
            except Exception as e:
                self.show_messagebox("error", "Redo Error", f"Error redoing action: {e}")
                self.redo_stack.append(command)
            self.update_undo_redo_buttons_kivy_state()
        else:
            self.update_status("Nothing to redo.")

    def update_undo_redo_buttons_kivy_state(self):
        if hasattr(self, 'undo_button_kivy') and self.undo_button_kivy:
            self.undo_button_kivy.disabled = not bool(self.undo_stack)
        if hasattr(self, 'redo_button_kivy') and self.redo_button_kivy:
            self.redo_button_kivy.disabled = not bool(self.redo_stack)


    def world_to_canvas_coords_kivy(self, world_x, world_y, canvas_widget):
        if hasattr(self.app, 'seating_canvas_widget'):
            return self.app.seating_canvas_widget.to_local(world_x, world_y, relative=False)
        return world_x, world_y

    def canvas_to_world_coords_kivy(self, screen_x, screen_y, canvas_widget):
        if hasattr(self.app, 'seating_canvas_widget'):
            return self.app.seating_canvas_widget.to_local(screen_x, screen_y, relative=True)
        return screen_x, screen_y

    def draw_single_student_kivy(self, student_id, canvas_layout_widget: ScatterLayout):
        student_data = self.students.get(student_id)
        if not student_data:
            if student_id in self.student_widgets:
                widget_to_remove = self.student_widgets.pop(student_id)
                canvas_layout_widget.remove_widget(widget_to_remove)
            return

        world_x, world_y = student_data["x"], student_data["y"]
        world_w = student_data.get("width", DEFAULT_STUDENT_BOX_WIDTH)
        world_h = student_data.get("height", DEFAULT_STUDENT_BOX_HEIGHT)

        if student_id in self.student_widgets:
            widget = self.student_widgets[student_id]
            widget.student_data = student_data
            widget.pos = (world_x, world_y)
            widget.size = (world_w, world_h)
            widget.is_selected = student_id in self.selected_items
        else:
            widget = StudentWidget(student_data=student_data, logic=self, item_id=student_id)
            widget.pos = (world_x, world_y)
            widget.size = (world_w, world_h)
            widget.is_selected = student_id in self.selected_items
            self.student_widgets[student_id] = widget
            canvas_layout_widget.add_widget(widget)
        widget.redraw()

    def draw_single_furniture_kivy(self, furniture_id, canvas_layout_widget: ScatterLayout):
        furniture_data = self.furniture.get(furniture_id)
        if not furniture_data:
            if furniture_id in self.furniture_widgets:
                widget_to_remove = self.furniture_widgets.pop(furniture_id)
                canvas_layout_widget.remove_widget(widget_to_remove)
            return

        world_x, world_y = furniture_data["x"], furniture_data["y"]
        world_w = furniture_data.get("width", REBBI_DESK_WIDTH)
        world_h = furniture_data.get("height", REBBI_DESK_HEIGHT)

        if furniture_id in self.furniture_widgets:
            widget = self.furniture_widgets[furniture_id]
            widget.furniture_data = furniture_data
            widget.pos = (world_x, world_y)
            widget.size = (world_w, world_h)
            widget.is_selected = furniture_id in self.selected_items
        else:
            widget = FurnitureWidget(furniture_data=furniture_data, logic=self, item_id=furniture_id)
            widget.pos = (world_x, world_y)
            widget.size = (world_w, world_h)
            widget.is_selected = furniture_id in self.selected_items
            self.furniture_widgets[furniture_id] = widget
            canvas_layout_widget.add_widget(widget)
        widget.redraw()

    def draw_all_items_kivy(self, canvas_layout_widget):
        current_student_widgets_ids = set(self.student_widgets.keys())
        current_furniture_widgets_ids = set(self.furniture_widgets.keys())
        data_student_ids = set(self.students.keys())
        data_furniture_ids = set(self.furniture.keys())

        for item_id_to_remove in current_student_widgets_ids - data_student_ids:
            if item_id_to_remove in self.student_widgets:
                canvas_layout_widget.remove_widget(self.student_widgets.pop(item_id_to_remove))
        for item_id_to_remove in current_furniture_widgets_ids - data_furniture_ids:
            if item_id_to_remove in self.furniture_widgets:
                canvas_layout_widget.remove_widget(self.furniture_widgets.pop(item_id_to_remove))

        for student_id in self.students:
            self.draw_single_student_kivy(student_id, canvas_layout_widget)
        for furniture_id in self.furniture:
            self.draw_single_furniture_kivy(furniture_id, canvas_layout_widget)

        print(f"Logic.draw_all_items_kivy: {len(self.student_widgets)} student, {len(self.furniture_widgets)} furniture widgets.")


    def export_layout_as_image(self): # ... (as before) ...
        try:
            default_filename = f"layout_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filechooser.save_file(title="Save Layout As PNG", default_path=default_filename, filters=[("PNG Image", "*.png")], on_selection=self._save_layout_image_callback)
        except Exception as e:
            self.update_status(f"Error opening file chooser: {e}")

    def _save_layout_image_callback(self, selection): # ... (as before) ...
        if not selection:
            self.update_status("Image export cancelled.")
            return
        file_path = selection[0]
        if not self.app.seating_canvas_widget:
            self.update_status("Canvas widget not available for export.")
            return
        try:
            self.app.seating_canvas_widget.export_to_png(file_path)
            self.update_status(f"Layout exported as image: {os.path.basename(file_path)}")
        except Exception as e:
            self.update_status(f"Failed to save image: {e}")

    def get_recent_incidents_for_student(self, student_id):
        now = datetime.now()
        time_window = timedelta(hours=self.settings.get("recent_incident_time_window_hours", 24))
        num_to_show = self.settings.get("num_recent_incidents_to_show", 2)
        reverse_order = self.settings.get("reverse_incident_order", True)

        recent_incidents = []
        for log in reversed(self.behavior_log):
            if log["student_id"] == student_id:
                log_time = datetime.fromisoformat(log["timestamp"])
                if now - log_time <= time_window:
                    recent_incidents.append(log)
                if len(recent_incidents) >= num_to_show:
                    break
        
        if not reverse_order:
            return recent_incidents
        return list(reversed(recent_incidents))

    def _get_default_settings(self): # ... (as before) ...
        return {
            "show_recent_incidents_on_boxes": True, "num_recent_incidents_to_show": 2, "recent_incident_time_window_hours": 24, "show_full_recent_incidents": False, "reverse_incident_order": True, "selected_recent_behaviors_filter": None,
            "show_recent_homeworks_on_boxes": True, "num_recent_homeworks_to_show": 2, "recent_homework_time_window_hours": 24, "show_full_recent_homeworks": False, "reverse_homework_order": True, "selected_recent_homeworks_filter": None,
            "autosave_interval_ms": 30000, "default_student_box_width": DEFAULT_STUDENT_BOX_WIDTH, "default_student_box_height": DEFAULT_STUDENT_BOX_HEIGHT, "student_box_fill_color": DEFAULT_BOX_FILL_COLOR, "student_box_outline_color": DEFAULT_BOX_OUTLINE_COLOR,
            "student_font_family": DEFAULT_FONT_FAMILY, "student_font_size": DEFAULT_FONT_SIZE, "behavior_font_size": DEFAULT_FONT_SIZE, "student_font_color": DEFAULT_FONT_COLOR, "grid_snap_enabled": False, "grid_size": DEFAULT_GRID_SIZE, "behavior_initial_overrides": {}, "homework_initial_overrides": {},
            "current_mode": "behavior", "max_undo_history_days": MAX_UNDO_HISTORY_DAYS, "conditional_formatting_rules": [], "student_groups_enabled": True, "show_zoom_level_display": True,
            "default_quiz_name": "Pop Quiz", "last_used_quiz_name_timeout_minutes": 60, "show_recent_incidents_during_quiz": True, "live_quiz_score_font_color": DEFAULT_QUIZ_SCORE_FONT_COLOR, "live_quiz_score_font_style_bold": DEFAULT_QUIZ_SCORE_FONT_STYLE_BOLD,
            "quiz_mark_types": DEFAULT_QUIZ_MARK_TYPES.copy(), "default_quiz_questions": 10, "quiz_score_calculation": "percentage", "combine_marks_for_display": True,
            "default_homework_name": "Homework Check", "live_homework_session_mode": "Yes/No", "log_homework_marks_enabled": True, "homework_mark_types": DEFAULT_HOMEWORK_MARK_TYPES.copy(), "default_homework_items_for_yes_no_mode": 5,
            "live_homework_score_font_color": DEFAULT_HOMEWORK_SCORE_FONT_COLOR, "live_homework_score_font_style_bold": DEFAULT_HOMEWORK_SCORE_FONT_STYLE_BOLD,
            "app_password_hash": None, "password_on_open": False, "password_on_edit_action": False, "password_auto_lock_enabled": False, "password_auto_lock_timeout_minutes": 15,
            "next_student_id_num": 1, "next_furniture_id_num": 1, "next_group_id_num": 1, "next_quiz_template_id_num": 1, "next_homework_template_id_num": 1, "next_custom_homework_type_id_num": 1,
            "_last_used_quiz_name_for_session": "", "_last_used_quiz_name_timestamp_for_session": None, "_last_used_q_num_for_session": 10,
            "_last_used_homework_name_for_session": "", "_last_used_homework_name_timestamp_for_session": None, "_last_used_hw_items_for_session": 5,
            "theme": "System", "enable_text_background_panel": True,
            "show_rulers": False, # New setting for rulers
            "show_grid": False, # New setting for grid
        }

    def update_status(self, message):
        print(f"Status: {message}")
        if self.app and hasattr(self.app, 'status_bar_label'):
             self.app.status_bar_label.text = message

    def prompt_for_password(self, title, prompt_message, for_editing=False):
        print(f"PROMPT PASSWORD: {title} - {prompt_message}")
        return True

    def show_messagebox(self, type, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_layout.add_widget(Label(text=message, text_size=(350, None)))
        btn = Button(text="OK", size_hint_y=None, height=40)
        popup_layout.add_widget(btn)
        popup = Popup(title=title, content=popup_layout, size_hint=(None, None), size=(400, 200))
        btn.bind(on_press=popup.dismiss)
        popup.open()

    def show_messagebox_yesno(self, title, message, yes_callback=None, no_callback=None): # Added callbacks
        print(f"MESSAGEBOX YES/NO: {title} - {message}")
        # In a real scenario, this would show a popup and invoke callbacks.
        # For now, let's assume "yes" for automated flow where it makes sense (e.g. load layout)
        if yes_callback:
            yes_callback() # Simulate user clicking yes
        return True # Or return a value indicating "yes" was chosen

    def get_new_student_id(self):
        current_id_to_assign = self.next_student_id_num
        return f"student_{current_id_to_assign}", self.next_student_id_num + 1

    def get_new_furniture_id(self):
        current_id_to_assign = self.next_furniture_id_num
        return f"furniture_{current_id_to_assign}", self.next_furniture_id_num + 1

    def open_add_student_dialog(self):
        popup = AddEditStudentPopup(logic=self)
        popup.open()

    def add_student_logic(self, first_name, last_name, nickname, gender, group_id_selection):
        old_next_student_id_num_for_command = self.next_student_id_num
        student_id_str, next_id_val_for_app_state_after_this = self.get_new_student_id()
        full_name = f"{first_name} \"{nickname}\" {last_name}" if nickname else f"{first_name} {last_name}"
        x, y = (50,50)

        student_data = {"first_name": first_name, "last_name": last_name, "nickname": nickname, "full_name": full_name, "gender": gender,
                        "x": x, "y": y, "id": student_id_str, "width": self.settings.get("default_student_box_width"),
                        "height": self.settings.get("default_student_box_height"), "original_next_id_num_after_add": next_id_val_for_app_state_after_this,
                        "group_id": group_id_selection if group_id_selection else None, "style_overrides": {}}

        command = AddItemCommand(self, student_id_str, 'student', student_data, old_next_student_id_num_for_command)
        self.execute_command(command)

    def open_add_furniture_dialog(self):
        popup = AddFurniturePopup(logic=self)
        popup.open()

    def add_furniture_logic(self, name, item_type, width, height):
        old_next_furniture_id_num_for_command = self.next_furniture_id_num
        furniture_id_str, next_id_val_for_app_state_after_this = self.get_new_furniture_id()
        x, y = (70, 70)

        furniture_data = {"name": name, "type": item_type, "x": x, "y": y, "id": furniture_id_str,
                          "width": width, "height": height,
                          "fill_color": "lightgray", "outline_color": "dimgray",
                          "original_next_id_num_after_add": next_id_val_for_app_state_after_this}
        command = AddItemCommand(self, furniture_id_str, 'furniture', furniture_data, old_next_furniture_id_num_for_command)
        self.execute_command(command)

    def get_student_full_name(self, student_id):
        student = self.students.get(student_id)
        return student.get("full_name", "Unknown Student") if student else "Unknown Student"

    def open_log_behavior_dialog(self, student_id):
        student = self.students.get(student_id)
        if not student:
            self.show_messagebox("error", "Error", "Student not found.")
            return
        self.update_all_behaviors()
        popup = BehaviorLogPopup(logic=self, student_id=student_id, student_full_name=student.get("full_name", "Unknown"))
        popup.open()

    def log_behavior_entry_logic(self, student_id, behavior, comment):
        student = self.students.get(student_id)
        if not student: return

        log_entry = {"timestamp": datetime.now().isoformat(), "student_id": student_id,
                     "student_first_name": student["first_name"], "student_last_name": student["last_name"],
                     "behavior": behavior, "comment": comment, "type": "behavior", "day": datetime.now().strftime('%A')}

        command = LogEntryCommand(self, log_entry, student_id)
        self.execute_command(command)

    def open_settings_dialog(self):
        popup = SettingsPopup(logic=self)
        popup.open()

    def save_settings_logic(self, new_settings_values):
        print("Kivy: Settings received by logic:", new_settings_values)
        for key, value in new_settings_values.items():
            if key in self.settings:
                current_type = type(self.settings.get(key))
                try:
                    if current_type == bool: self.settings[key] = bool(value)
                    elif current_type == int: self.settings[key] = int(value)
                    elif current_type == float: self.settings[key] = float(value)
                    else: self.settings[key] = str(value)
                except (ValueError, TypeError):
                    print(f"Warning: Could not convert setting {key} to {current_type}. Value: {value}")
            else: self.settings[key] = value

        self.save_data_wrapper(source="settings_dialog_kivy")
        if hasattr(self.app, 'seating_canvas_widget'):
            self.app.seating_canvas_widget.redraw_all_items_on_canvas()
        self.update_status("Settings updated (Kivy).")

    def open_log_quiz_score_dialog(self, student_id):
        student = self.students.get(student_id)
        if not student:
            self.show_messagebox("error", "Error", "Student not found.")
            return
        self.load_quiz_templates()
        self.update_all_behaviors()
        popup = QuizScorePopup(logic=self, student_id=student_id, student_full_name=student.get("full_name", "Unknown"))
        popup.open()

    def log_quiz_score_entry_logic(self, student_id, quiz_name, marks_data, comment, num_questions):
        student = self.students.get(student_id)
        if not student: return

        log_entry = {
            "timestamp": datetime.now().isoformat(), "student_id": student_id,
            "student_first_name": student["first_name"], "student_last_name": student["last_name"],
            "behavior": quiz_name, "comment": comment, "marks_data": marks_data,
            "num_questions": num_questions, "type": "quiz", "day": datetime.now().strftime('%A')
        }
        command = LogEntryCommand(self, log_entry, student_id)
        self.execute_command(command)

        self.last_used_quiz_name = quiz_name
        self.last_used_quiz_name_timestamp = datetime.now().isoformat()
        self.initial_num_questions = str(num_questions)
        self.settings["_last_used_quiz_name_for_session"] = self.last_used_quiz_name
        self.settings["_last_used_quiz_name_timestamp_for_session"] = self.last_used_quiz_name_timestamp
        self.settings["_last_used_q_num_for_session"] = self.initial_num_questions

    def open_log_homework_dialog(self, student_id):
        student = self.students.get(student_id)
        if not student:
            self.show_messagebox("error", "Error", "Student not found.")
            return
        self.update_all_homework_types()
        self.update_all_homework_statuses()
        self.load_homework_templates()

        log_marks_enabled = self.settings.get("log_homework_marks_enabled", True)
        popup = ManualHomeworkLogPopup(logic=self, student_id=student_id,
                                       student_full_name=student.get("full_name", "Unknown"),
                                       log_marks_enabled=log_marks_enabled)
        popup.open()

    def log_homework_entry_logic(self, student_id, homework_type, comment, marks_data=None, num_items=None, homework_status=None):
        student = self.students.get(student_id)
        if not student: return

        log_entry_type = "homework"
        behavior_field_value = homework_type

        if homework_status:
            behavior_field_value = f"{homework_type}: {homework_status}"

        log_entry = {
            "timestamp": datetime.now().isoformat(), "student_id": student_id,
            "student_first_name": student["first_name"], "student_last_name": student["last_name"],
            "behavior": behavior_field_value,
            "homework_type": homework_type,
            "comment": comment, "type": log_entry_type,
            "day": datetime.now().strftime('%A')
        }
        if marks_data is not None: log_entry["marks_data"] = marks_data
        if num_items is not None: log_entry["num_items"] = num_items
        if homework_status is not None: log_entry["homework_status"] = homework_status

        command = LogHomeworkEntryCommand(self, log_entry, student_id)
        self.execute_command(command)

    def open_data_folder_kivy(self):
        data_dir = os.path.dirname(DATA_FILE if DATA_FILE else get_app_data_path("dummy.txt"))
        self.update_status(f"Data folder is: {data_dir}")
        try:
            if sys.platform == "win32": os.startfile(data_dir)
            elif sys.platform == "darwin": subprocess.Popen(["open", data_dir])
            else:
                if os.path.isdir(data_dir): subprocess.Popen(["xdg-open", data_dir])
                else: self.show_messagebox("error", "Error", f"Data directory not found: {data_dir}")
        except Exception as e:
            self.show_messagebox("error", "Error Opening Folder", f"Could not open folder: {e}")
            self.update_status(f"Error opening folder: {e}")

    def exit_app_kivy(self):
        self.save_data_wrapper(source="exit_app_kivy")
        App.get_running_app().stop()

    def toggle_edit_mode_kivy(self, checkbox_instance, active_state):
        self.edit_mode_var_kivy = active_state
        self.update_status(f"Edit Mode {'Enabled' if self.edit_mode_var_kivy else 'Disabled'}.")
        if hasattr(self.app, 'seating_canvas_widget'):
            self.app.seating_canvas_widget.redraw_all_items_on_canvas()

    def open_export_log_dialog_kivy(self, export_type):
        # if self.password_manager.is_locked: # TODO
        #     if not self.prompt_for_password("Unlock to Export", "Enter password to export log data:"): return

        # Ensure lists are fresh for the dialog (though they are usually updated on load/settings change)
        # self.update_all_students_list_for_filter() # If a specific list of student names/ids is needed
        self.update_all_behaviors()
        self.update_all_homework_types() # or session types + statuses depending on filter complexity

        popup = ExportFilterPopup(logic=self, export_format=export_type)
        popup.open()

    def export_log_data_kivy(self, filter_settings, export_format):
        default_filename = f"behavior_log_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        file_ext = f".{export_format}" if export_format != "csv" else "_csv.zip"
        default_filename += file_ext

        file_types_map = {
            "xlsx": [("Excel files", "*.xlsx")],
            "xlsm": [("Excel Macro-Enabled files", "*.xlsm")], # Not typically generated by openpyxl directly
            "csv": [("ZIP archives", "*.zip")]
        }

        try:
            filechooser.save_file(
                title=f"Save Exported Log as {export_format.upper()}",
                default_path=default_filename,
                filters=file_types_map.get(export_format, [("All files", "*.*")]),
                on_selection=lambda sel: self._on_export_file_select(sel, export_format, filter_settings)
            )
        except Exception as e:
            self.update_status(f"Error opening file chooser for export: {e}")
            self.show_messagebox("error", "Export Error", f"Could not open file chooser: {e}")

    def _on_export_file_select(self, selection, export_format, filter_settings):
        if not selection:
            self.update_status("Export cancelled.")
            return
        file_path = selection[0]
        try:
            if export_format in ["xlsx", "xlsm"]: # Treat xlsm as xlsx for openpyxl
                self.export_data_to_excel(file_path, "xlsx", filter_settings) # openpyxl saves as .xlsx
            elif export_format == "csv":
                self.export_data_to_csv_zip(file_path, filter_settings)

            self.last_excel_export_path = file_path
            # self.update_open_last_export_folder_menu_item_kivy() # TODO: Update Kivy menu if this is shown
            self.save_data_wrapper(source="export_log_kivy") # Save last export path
            self.update_status(f"Log exported to {os.path.basename(file_path)}")
            # self.show_messagebox_yesno_kivy("Export Successful", f"Log exported to:\n{file_path}\n\nOpen file location?",
            #                               yes_callback=lambda: self.open_specific_export_folder_kivy(file_path)) # TODO
        except Exception as e:
            self.show_messagebox("error", "Export Error", f"Failed to export log: {e}")
            self.update_status(f"Error exporting log: {e}")
            print(f"Export Error: {e}")


    def load_data(self, file_path=None, is_restore=False): # ... (implementation as before, ensure Command.from_dict is used for undo/redo) ...
        target_file = file_path or DATA_FILE
        if not target_file:
            print("load_data called before DATA_FILE path is initialized. Aborting load.")
            return

        default_settings_copy = self._get_default_settings()
        data_loaded_successfully = False

        if os.path.exists(target_file):
            try:
                with open(target_file, 'r', encoding='utf-8') as f: data = json.load(f)
                file_basename = os.path.basename(target_file)
                data_version_from_filename = None
                try:
                    version_num_str = ''.join(filter(str.isdigit, os.path.basename(target_file)))
                    if version_num_str: data_version_from_filename = int(version_num_str)
                except: pass
                current_tag_num = int(''.join(filter(str.isdigit, CURRENT_DATA_VERSION_TAG)))
                if data_version_from_filename is None:
                     data = self._migrate_v3_edited_data(data); data = self._migrate_v4_data(data); data = self._migrate_v5_data(data); data = self._migrate_v6_data(data); data = self._migrate_v7_data(data); data = self._migrate_v8_data(data)
                elif data_version_from_filename < current_tag_num:
                    if data_version_from_filename < 4: data = self._migrate_v3_edited_data(data)
                    if data_version_from_filename < 5: data = self._migrate_v4_data(data)
                    if data_version_from_filename < 6: data = self._migrate_v5_data(data)
                    if data_version_from_filename < 7: data = self._migrate_v6_data(data)
                    if data_version_from_filename < 8: data = self._migrate_v7_data(data)
                    if data_version_from_filename < 9: data = self._migrate_v8_data(data)

                final_settings = default_settings_copy.copy()
                final_settings.update(data.get("settings", {}))
                data["settings"] = final_settings

                self.students = data.get("students", {})
                self.furniture = data.get("furniture", {})
                self.behavior_log = data.get("behavior_log", [])
                self.homework_log = data.get("homework_log", [])
                self.settings = data.get("settings", default_settings_copy.copy())
                self.last_excel_export_path = data.get("last_excel_export_path", None)
                self._per_student_last_cleared = data.get("_per_student_last_cleared", {})
                self.undo_stack.clear(); self.redo_stack.clear()

                loaded_undo_stack = data.get("undo_stack", [])
                cutoff_date_iso = (datetime.now() - timedelta(days=self.settings.get("max_undo_history_days", MAX_UNDO_HISTORY_DAYS))).isoformat()
                for cmd_data in loaded_undo_stack:
                    if cmd_data.get('timestamp', '0') >= cutoff_date_iso:
                        cmd_obj = Command.from_dict(self, cmd_data)
                        if cmd_obj: self.undo_stack.append(cmd_obj)

                loaded_redo_stack = data.get("redo_stack", [])
                for cmd_data in loaded_redo_stack:
                     if cmd_data.get('timestamp', '0') >= cutoff_date_iso:
                        cmd_obj = Command.from_dict(self, cmd_data)
                        if cmd_obj: self.redo_stack.append(cmd_obj)

                data_loaded_successfully = True
            except Exception as e:
                print(f"Error loading data from {target_file}: {e}. Using defaults.")
                self.students, self.furniture, self.behavior_log, self.homework_log = {}, {}, [], []
                self.settings = default_settings_copy.copy()
        else:
            print(f"Data file {target_file} not found. Using defaults.")
            self.students, self.furniture, self.behavior_log, self.homework_log = {}, {}, [], []
            self.settings = default_settings_copy.copy()

        for key, value in default_settings_copy.items():
            if key not in self.settings: self.settings[key] = value
        self._ensure_next_ids()

        if data_loaded_successfully and not is_restore and file_path is None and \
           (os.path.basename(DATA_FILE) != f"classroom_data_{CURRENT_DATA_VERSION_TAG}.json" or \
            (data_version_from_filename is not None and data_version_from_filename < current_tag_num)):
            print(f"Data file loaded from an older version. Saving in new format.")
            self.save_data_wrapper(source="migration_save")

    def _migrate_v3_edited_data(self, data): print("Migrating v3 (stub)"); return data
    def _migrate_v4_data(self, data): print("Migrating v4 (stub)"); return data
    def _migrate_v5_data(self, data): print("Migrating v5 (stub)"); return data
    def _migrate_v6_data(self, data): print("Migrating v6 (stub)"); return data
    def _migrate_v7_data(self, data): print("Migrating v7 (stub)"); return data
    def _migrate_v8_data(self, data): print("Migrating v8 (stub)"); return data

    def save_data_wrapper(self, event=None, source="manual"):
        if not DATA_FILE:
            print("save_data_wrapper: DATA_FILE not set, cannot save.")
            return
        self._ensure_next_ids()
        serializable_undo_stack = [cmd.to_dict() for cmd in self.undo_stack if hasattr(cmd, 'to_dict')]
        serializable_redo_stack = [cmd.to_dict() for cmd in self.redo_stack if hasattr(cmd, 'to_dict')]
        data_to_save = {
            "students": self.students, "furniture": self.furniture,
            "behavior_log": self.behavior_log, "homework_log": self.homework_log,
            "settings": self.settings, "last_excel_export_path": self.last_excel_export_path,
            "_per_student_last_cleared": self._per_student_last_cleared,
            "undo_stack": serializable_undo_stack,
            "redo_stack": serializable_redo_stack
        }
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f: json.dump(data_to_save, f, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")
        self.save_student_groups(); self.save_custom_behaviors(); self.save_custom_homework_types(); self.save_custom_homework_statuses(); self.save_quiz_templates(); self.save_homework_templates()

    def load_custom_behaviors(self):
        if CUSTOM_BEHAVIORS_FILE and os.path.exists(CUSTOM_BEHAVIORS_FILE):
            try:
                with open(CUSTOM_BEHAVIORS_FILE, 'r', encoding='utf-8') as f: self.custom_behaviors = json.load(f)
            except Exception as e: print(f"Error loading custom behaviors: {e}"); self.custom_behaviors = []
        else: self.custom_behaviors = []
    def save_custom_behaviors(self):
        if CUSTOM_BEHAVIORS_FILE:
            try:
                with open(CUSTOM_BEHAVIORS_FILE, 'w', encoding='utf-8') as f: json.dump(self.custom_behaviors, f, indent=4)
            except Exception as e: print(f"Error saving custom behaviors: {e}")

    def load_custom_homework_types(self):
        if CUSTOM_HOMEWORK_TYPES_FILE and os.path.exists(CUSTOM_HOMEWORK_TYPES_FILE):
            try:
                with open(CUSTOM_HOMEWORK_TYPES_FILE, 'r', encoding='utf-8') as f: self.custom_homework_types = json.load(f)
            except Exception as e: print(f"Error loading custom_homework_types: {e}"); self.custom_homework_types = []
        else: self.custom_homework_types = []
    def save_custom_homework_types(self):
        if CUSTOM_HOMEWORK_TYPES_FILE:
            try:
                with open(CUSTOM_HOMEWORK_TYPES_FILE, 'w', encoding='utf-8') as f: json.dump(self.custom_homework_types, f, indent=4)
            except Exception as e: print(f"Error saving custom_homework_types: {e}")

    def load_custom_homework_statuses(self):
        if CUSTOM_HOMEWORK_STATUSES_FILE and os.path.exists(CUSTOM_HOMEWORK_STATUSES_FILE):
            try:
                with open(CUSTOM_HOMEWORK_STATUSES_FILE, 'r', encoding='utf-8') as f: self.custom_homework_statuses = json.load(f)
            except Exception as e: print(f"Error loading custom_homework_statuses: {e}"); self.custom_homework_statuses = []
        else: self.custom_homework_statuses = []
    def save_custom_homework_statuses(self):
        if CUSTOM_HOMEWORK_STATUSES_FILE:
            try:
                with open(CUSTOM_HOMEWORK_STATUSES_FILE, 'w', encoding='utf-8') as f: json.dump(self.custom_homework_statuses, f, indent=4)
            except Exception as e: print(f"Error saving custom_homework_statuses: {e}")

    def load_student_groups(self):
        if STUDENT_GROUPS_FILE and os.path.exists(STUDENT_GROUPS_FILE):
            try:
                with open(STUDENT_GROUPS_FILE, 'r', encoding='utf-8') as f: self.student_groups = json.load(f)
            except Exception as e: print(f"Error loading student_groups: {e}"); self.student_groups = {}
        else: self.student_groups = {}
    def save_student_groups(self):
        if STUDENT_GROUPS_FILE:
            try:
                with open(STUDENT_GROUPS_FILE, 'w', encoding='utf-8') as f: json.dump(self.student_groups, f, indent=4)
            except Exception as e: print(f"Error saving student_groups: {e}")

    def load_quiz_templates(self):
        if QUIZ_TEMPLATES_FILE and os.path.exists(QUIZ_TEMPLATES_FILE):
            try:
                with open(QUIZ_TEMPLATES_FILE, 'r', encoding='utf-8') as f: self.quiz_templates = json.load(f)
            except Exception as e: print(f"Error loading quiz_templates: {e}"); self.quiz_templates = {}
        else: self.quiz_templates = {}
    def save_quiz_templates(self):
        if QUIZ_TEMPLATES_FILE:
            try:
                with open(QUIZ_TEMPLATES_FILE, 'w', encoding='utf-8') as f: json.dump(self.quiz_templates, f, indent=4)
            except Exception as e: print(f"Error saving quiz_templates: {e}")

    def load_homework_templates(self):
        if HOMEWORK_TEMPLATES_FILE and os.path.exists(HOMEWORK_TEMPLATES_FILE):
            try:
                with open(HOMEWORK_TEMPLATES_FILE, 'r', encoding='utf-8') as f: self.homework_templates = json.load(f)
            except Exception as e: print(f"Error loading homework_templates: {e}"); self.homework_templates = {}
        else: self.homework_templates = {}
    def save_homework_templates(self):
        if HOMEWORK_TEMPLATES_FILE:
            try:
                with open(HOMEWORK_TEMPLATES_FILE, 'w', encoding='utf-8') as f: json.dump(self.homework_templates, f, indent=4)
            except Exception as e: print(f"Error saving homework_templates: {e}")

    def update_all_behaviors(self): self.all_behaviors = DEFAULT_BEHAVIORS_LIST + [b["name"] if isinstance(b, dict) else str(b) for b in self.custom_behaviors]
    def update_all_homework_types(self): self.all_homework_types = DEFAULT_HOMEWORK_TYPES_LIST + [item["name"] for item in self.custom_homework_types]
    def update_all_homework_statuses(self): self.all_homework_statuses = DEFAULT_HOMEWORK_STATUSES + [item["name"] for item in self.custom_homework_statuses]
    def update_all_homework_session_types(self):
        default_as_dicts = [{"id": f"default_{name.lower().replace(' ','_')}", "name": name} for name in DEFAULT_HOMEWORK_TYPES_LIST]
        self.all_homework_session_types = default_as_dicts + [ct for ct in self.custom_homework_types if isinstance(ct, dict)]

    def _ensure_next_ids(self):
        max_s_id = 0; max_f_id = 0; max_g_id = 0; max_qt_id = 0; max_ht_id = 0; max_chwt_id = 0
        for sid in self.students:
            if sid.startswith("student_"): try: max_s_id = max(max_s_id, int(sid.split("_")[1]))
            except: pass
        self.settings["next_student_id_num"] = max(self.settings.get("next_student_id_num", 1), max_s_id + 1)
        self.next_student_id_num = self.settings["next_student_id_num"]
        for fid in self.furniture:
            if fid.startswith("furniture_"): try: max_f_id = max(max_f_id, int(fid.split("_")[1]))
            except: pass
        self.settings["next_furniture_id_num"] = max(self.settings.get("next_furniture_id_num", 1), max_f_id + 1)
        self.next_furniture_id_num = self.settings["next_furniture_id_num"]
        for gid in self.student_groups:
            if gid.startswith("group_"): try: max_g_id = max(max_g_id, int(gid.split("_")[1]))
            except: pass
        self.settings["next_group_id_num"] = max(self.settings.get("next_group_id_num", 1), max_g_id + 1)
        self.next_group_id_num = self.settings["next_group_id_num"]
        for qtid in self.quiz_templates:
            if qtid.startswith("quiztemplate_"): try: max_qt_id = max(max_qt_id, int(qtid.split("_")[1]))
            except: pass
        self.settings["next_quiz_template_id_num"] = max(self.settings.get("next_quiz_template_id_num", 1), max_qt_id + 1)
        self.next_quiz_template_id_num = self.settings["next_quiz_template_id_num"]
        for htid in self.homework_templates:
            if htid.startswith("hwtemplate_"): try: max_ht_id = max(max_ht_id, int(htid.split("_")[1]))
            except: pass
        self.settings["next_homework_template_id_num"] = max(self.settings.get("next_homework_template_id_num", 1), max_ht_id + 1)
        self.next_homework_template_id_num = self.settings["next_homework_template_id_num"]
        for chwt in self.custom_homework_types:
            if isinstance(chwt, dict) and chwt.get('id', '').startswith("hwtype_"):
                try: max_chwt_id = max(max_chwt_id, int(chwt['id'].split("_")[1]))
                except: pass
        self.settings["next_custom_homework_type_id_num"] = max(self.settings.get("next_custom_homework_type_id_num", 1), max_chwt_id + 1)

    def toggle_rulers(self):
        self.settings['show_rulers'] = not self.settings.get('show_rulers', False)
        self.update_status(f"Rulers {'shown' if self.settings['show_rulers'] else 'hidden'}.")
        if hasattr(self.app, 'seating_canvas_widget'):
            self.app.seating_canvas_widget.guides_to_draw.clear() # Clear temporary guides
            self.app.seating_canvas_widget.redraw_all_items_on_canvas() # This will trigger ruler redraw

    def toggle_grid(self):
        self.settings['show_grid'] = not self.settings.get('show_grid', False)
        self.update_status(f"Grid {'shown' if self.settings['show_grid'] else 'hidden'}.")
        if hasattr(self.app, 'seating_canvas_widget'):
            self.app.seating_canvas_widget.redraw_all_items_on_canvas()

    def distribute_selected_items_evenly(self, direction='horizontal'):
        if len(self.selected_items) < 2:
            self.update_status("Select at least two items to distribute.")
            return

        items_to_distribute = []
        for item_id in self.selected_items:
            item_data = None
            item_type = None
            if item_id in self.students:
                item_data = self.students[item_id]
                item_type = "student"
            elif item_id in self.furniture:
                item_data = self.furniture[item_id]
                item_type = "furniture"

            if item_data:
                items_to_distribute.append({
                    "id": item_id,
                    "type": item_type,
                    "x": float(item_data["x"]),
                    "y": float(item_data["y"]),
                    "width": float(item_data.get("width", DEFAULT_STUDENT_BOX_WIDTH if item_type == "student" else REBBI_DESK_WIDTH)),
                    "height": float(item_data.get("height", DEFAULT_STUDENT_BOX_HEIGHT if item_type == "student" else REBBI_DESK_HEIGHT)),
                })

        if not items_to_distribute:
            return

        moves_for_command = []

        if direction == 'horizontal':
            items_to_distribute.sort(key=lambda item: item['x'])
            min_x = items_to_distribute[0]['x']
            max_x_item = items_to_distribute[-1]
            max_x_coord = max_x_item['x'] + max_x_item['width']

            total_items_width = sum(item['width'] for item in items_to_distribute)
            total_span = max_x_coord - min_x

            if len(items_to_distribute) > 1:
                available_space_for_gaps = total_span - total_items_width
                if available_space_for_gaps < 0: # Overlapping, use a minimum gap
                    gap_size = 5 # Or some small default positive gap
                else:
                    gap_size = available_space_for_gaps / (len(items_to_distribute) - 1)
            else: # Single item, no distribution needed (already handled by < 2 check)
                return

            current_x = min_x
            for i, item in enumerate(items_to_distribute):
                if item['x'] != current_x:
                    moves_for_command.append({
                        'id': item['id'], 'type': item['type'],
                        'old_x': item['x'], 'old_y': item['y'], # Keep original y
                        'new_x': current_x, 'new_y': item['y']
                    })
                current_x += item['width'] + gap_size

        elif direction == 'vertical':
            items_to_distribute.sort(key=lambda item: item['y'])
            min_y = items_to_distribute[0]['y']
            max_y_item = items_to_distribute[-1]
            max_y_coord = max_y_item['y'] + max_y_item['height']

            total_items_height = sum(item['height'] for item in items_to_distribute)
            total_span = max_y_coord - min_y

            if len(items_to_distribute) > 1:
                available_space_for_gaps = total_span - total_items_height
                if available_space_for_gaps < 0: # Overlapping
                    gap_size = 5
                else:
                    gap_size = available_space_for_gaps / (len(items_to_distribute) - 1)
            else:
                return

            current_y = min_y
            for i, item in enumerate(items_to_distribute):
                if item['y'] != current_y:
                    moves_for_command.append({
                        'id': item['id'], 'type': item['type'],
                        'old_x': item['x'], 'old_y': item['y'], # Keep original x
                        'new_x': item['x'], 'new_y': current_y
                    })
                current_y += item['height'] + gap_size

        if moves_for_command:
            command = MoveItemsCommand(self, moves_for_command)
            self.execute_command(command)
            self.update_status(f"Distributed {len(moves_for_command)} items {direction}ly.")
        else:
            self.update_status(f"Items already distributed {direction}ly or no change needed.")


# ... (Kivy App, Popup, and Widget classes as defined previously) ...
# (Pasted content from previous `overwrite_file_with_block` for these classes)

class SeatingChartKivyApp(App):
    # ... (build method with File menu, Export Log menu, Add Student, Settings, Undo, Redo buttons) ...
    def build(self):
        self.logic = SeatingChartAppLogic(self)
        root_widget = BoxLayout(orientation='vertical')

        top_controls = BoxLayout(size_hint_y=None, height="50dp", spacing="5dp", padding="5dp")

        # File Menu
        self.file_dropdown = DropDown()
        btn_texts_file = ["Save Now", "Open Data Folder", "Save Layout As...", "Load Layout...", "Backup Data...", "Restore Data...", "---", "Exit"]
        btn_actions_file = [
            lambda: self.logic.save_data_wrapper(source="manual_save_kivy"),
            lambda: self.logic.open_data_folder_kivy(),
            lambda: self.logic.open_save_layout_template_dialog_kivy(),
            lambda: self.logic.open_load_layout_template_dialog_kivy(),
            lambda: self.logic.show_messagebox("info","TODO", "Backup Data not yet implemented"),
            lambda: self.logic.show_messagebox("info","TODO", "Restore Data not yet implemented"),
            None,
            lambda: self.logic.exit_app_kivy()
        ]
        for text, action in zip(btn_texts_file, btn_actions_file):
            if text == "---": continue
            else:
                btn = Button(text=text, size_hint_y=None, height="44dp")
                btn.action = action
                btn.bind(on_release=lambda instance: instance.action() if instance.action else None)
                self.file_dropdown.add_widget(btn)

        file_button = Button(text="File")
        file_button.bind(on_release=self.file_dropdown.open)
        top_controls.add_widget(file_button)

        # Export Log Menu
        self.export_log_dropdown = DropDown()
        export_options = [("To Excel (.xlsx)", "xlsx"), ("To CSV Files (.zip)", "csv")]
        for text, ex_type in export_options:
            btn = Button(text=text, size_hint_y=None, height="44dp")
            btn.export_type = ex_type
            btn.bind(on_release=lambda instance: self.logic.open_export_log_dialog_kivy(instance.export_type))
            self.export_log_dropdown.add_widget(btn)

        export_button = Button(text="Export Log")
        export_button.bind(on_release=self.export_log_dropdown.open)
        top_controls.add_widget(export_button)

        btn_add_student = Button(text="Add Student")
        btn_add_student.bind(on_press=lambda x: self.logic.open_add_student_dialog())
        top_controls.add_widget(btn_add_student)

        btn_settings = Button(text="Settings")
        btn_settings.bind(on_press=lambda x: self.logic.open_settings_dialog())
        top_controls.add_widget(btn_settings)

        edit_mode_box = BoxLayout(size_hint_x=None, width="150dp", spacing="5dp")
        edit_mode_box.add_widget(Label(text="Edit Mode:", size_hint_x=0.7))
        self.edit_mode_checkbox = CheckBox(active=self.logic.edit_mode_var_kivy, size_hint_x=0.3)
        self.edit_mode_checkbox.bind(active=self.logic.toggle_edit_mode_kivy)
        edit_mode_box.add_widget(self.edit_mode_checkbox)
        top_controls.add_widget(edit_mode_box)

        btn_undo = Button(text="Undo", disabled=True)
        btn_undo.bind(on_press=lambda x: self.logic.undo_last_action())
        top_controls.add_widget(btn_undo)
        self.logic.undo_button_kivy = btn_undo

        btn_redo = Button(text="Redo", disabled=True)
        btn_redo.bind(on_press=lambda x: self.logic.redo_last_action())
        top_controls.add_widget(btn_redo)
        self.logic.redo_button_kivy = btn_redo

        # Distribute buttons
        btn_dist_h = Button(text="Distribute H")
        btn_dist_h.bind(on_press=lambda x: self.logic.distribute_selected_items_evenly('horizontal'))
        top_controls.add_widget(btn_dist_h)

        btn_dist_v = Button(text="Distribute V")
        btn_dist_v.bind(on_press=lambda x: self.logic.distribute_selected_items_evenly('vertical'))
        top_controls.add_widget(btn_dist_v)

        btn_toggle_rulers = Button(text="Toggle Rulers")
        btn_toggle_rulers.bind(on_press=lambda x: self.logic.toggle_rulers())
        top_controls.add_widget(btn_toggle_rulers)

        btn_toggle_grid = Button(text="Toggle Grid")
        btn_toggle_grid.bind(on_press=lambda x: self.logic.toggle_grid())
        top_controls.add_widget(btn_toggle_grid)

        root_widget.add_widget(top_controls)
        self.seating_canvas_widget = SeatingCanvasLayout()
        root_widget.add_widget(self.seating_canvas_widget)
        self.status_bar_label = Label(text="Status Bar Placeholder", size_hint_y=None, height="30dp")
        root_widget.add_widget(self.status_bar_label)
        self.logic.update_status("Kivy App Initialized. Loading data...")
        return root_widget

    def on_start(self):
        self.logic.app_started()

    def on_stop(self):
        print("App stopping. Data should be saved by logic if needed.")
        self.logic.app_stopping()

class AddEditStudentPopup(Popup): # ... (as before)
    def __init__(self, logic, student_data=None, **kwargs):
        super().__init__(**kwargs)
        self.logic = logic
        self.student_data = student_data
        self.title = "Edit Student" if student_data else "Add Student"
        self.size_hint = (0.9, 0.8)
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        grid = GridLayout(cols=2, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        grid.add_widget(Label(text="First Name:"))
        self.first_name_input = TextInput(text=student_data.get('first_name', '') if student_data else '', multiline=False)
        grid.add_widget(self.first_name_input)
        grid.add_widget(Label(text="Last Name:"))
        self.last_name_input = TextInput(text=student_data.get('last_name', '') if student_data else '', multiline=False)
        grid.add_widget(self.last_name_input)
        grid.add_widget(Label(text="Nickname:"))
        self.nickname_input = TextInput(text=student_data.get('nickname', '') if student_data else '', multiline=False)
        grid.add_widget(self.nickname_input)
        grid.add_widget(Label(text="Gender:"))
        self.gender_spinner = Spinner(text=student_data.get('gender', 'Boy') if student_data else 'Boy', values=('Boy', 'Girl', 'Other'))
        grid.add_widget(self.gender_spinner)
        grid.add_widget(Label(text="Group:"))
        current_group_name = "None"
        if student_data and student_data.get('group_id'):
            group = self.logic.student_groups.get(student_data['group_id'])
            if group: current_group_name = group.get('name', 'Unknown Group')
        self.group_label = Label(text=current_group_name)
        grid.add_widget(self.group_label)
        content.add_widget(grid)
        buttons_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        save_button = Button(text="Save")
        save_button.bind(on_press=self.save_student)
        buttons_layout.add_widget(save_button)
        cancel_button = Button(text="Cancel")
        cancel_button.bind(on_press=self.dismiss)
        buttons_layout.add_widget(cancel_button)
        content.add_widget(Widget(size_hint_y=1))
        content.add_widget(buttons_layout)
        self.content = content

    def save_student(self, instance):
        first_name = self.first_name_input.text.strip()
        last_name = self.last_name_input.text.strip()
        nickname = self.nickname_input.text.strip()
        gender = self.gender_spinner.text
        group_id_selection = self.student_data.get('group_id') if self.student_data else None
        if not first_name or not last_name:
            self.logic.show_messagebox("error", "Invalid Name", "First and Last names cannot be empty.")
            return
        if self.student_data:
            old_data = self.student_data.copy()
            if "style_overrides" in old_data: old_data["style_overrides"] = old_data["style_overrides"].copy()
            changes = {
                "first_name": first_name, "last_name": last_name, "nickname": nickname, "gender": gender,
                "full_name": f"{first_name} \"{nickname}\" {last_name}" if nickname else f"{first_name} {last_name}"
            }
            actual_changes = {k: v for k, v in changes.items() if v != old_data.get(k)}
            if actual_changes:
                command = EditItemCommand(self.logic, self.student_data['id'], 'student', old_data, actual_changes)
                self.logic.execute_command(command)
        else:
            self.logic.add_student_logic(first_name, last_name, nickname, gender, group_id_selection)
        self.dismiss()

class AddFurniturePopup(Popup): # ... (as before) ...
    def __init__(self, logic, furniture_data=None, **kwargs):
        super().__init__(**kwargs)
        self.logic = logic
        self.furniture_data = furniture_data
        self.title = "Add Furniture Item"
        self.size_hint = (0.9, 0.7)
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        grid = GridLayout(cols=2, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        grid.add_widget(Label(text="Item Name:"))
        self.name_input = TextInput(multiline=False)
        grid.add_widget(self.name_input)
        grid.add_widget(Label(text="Item Type:"))
        self.type_input = TextInput(text="Desk", multiline=False)
        grid.add_widget(self.type_input)
        grid.add_widget(Label(text="Width:"))
        self.width_input = TextInput(text=str(DEFAULT_STUDENT_BOX_WIDTH), multiline=False, input_filter='int')
        grid.add_widget(self.width_input)
        grid.add_widget(Label(text="Height:"))
        self.height_input = TextInput(text=str(DEFAULT_STUDENT_BOX_HEIGHT), multiline=False, input_filter='int')
        grid.add_widget(self.height_input)
        content.add_widget(grid)
        buttons_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        save_button = Button(text="Add Furniture")
        save_button.bind(on_press=self.save_furniture)
        buttons_layout.add_widget(save_button)
        cancel_button = Button(text="Cancel")
        cancel_button.bind(on_press=self.dismiss)
        buttons_layout.add_widget(cancel_button)
        content.add_widget(Widget(size_hint_y=1))
        content.add_widget(buttons_layout)
        self.content = content

    def save_furniture(self, instance):
        name = self.name_input.text.strip()
        item_type = self.type_input.text.strip()
        try:
            width = int(self.width_input.text); height = int(self.height_input.text)
        except ValueError:
            self.logic.show_messagebox("error", "Invalid Dimensions", "Width and Height must be numbers.")
            return
        if not name or not item_type:
            self.logic.show_messagebox("error", "Invalid Input", "Name and Type cannot be empty.")
            return
        self.logic.add_furniture_logic(name, item_type, width, height)
        self.dismiss()

class BehaviorLogPopup(Popup): # ... (as before) ...
    def __init__(self, logic, student_id, student_full_name, **kwargs):
        super().__init__(**kwargs)
        self.logic = logic
        self.student_id = student_id
        self.student_full_name = student_full_name
        self.title = f"Log Behavior for {self.student_full_name}"
        self.size_hint = (0.9, 0.7)

        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        grid = GridLayout(cols=2, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        grid.add_widget(Label(text="Behavior:"))
        effective_behaviors = self.logic.all_behaviors
        if not effective_behaviors:
            default_behavior_text = "No behaviors available"
            effective_behaviors = [default_behavior_text]
            spinner_disabled = True
        else:
            default_behavior_text = effective_behaviors[0]
            spinner_disabled = False

        self.behavior_spinner = Spinner(text=default_behavior_text, values=tuple(effective_behaviors))
        self.behavior_spinner.disabled = spinner_disabled
        grid.add_widget(self.behavior_spinner)

        grid.add_widget(Label(text="Comment:"))
        self.comment_input = TextInput(text='', multiline=True, size_hint_y=None, height=100)
        grid.add_widget(self.comment_input)

        content.add_widget(grid)
        content.add_widget(Widget(size_hint_y=1))

        buttons_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        log_button = Button(text="Log Behavior")
        log_button.bind(on_press=self.log_behavior_action)
        buttons_layout.add_widget(log_button)

        cancel_button = Button(text="Cancel")
        cancel_button.bind(on_press=self.dismiss)
        buttons_layout.add_widget(cancel_button)

        content.add_widget(buttons_layout)
        self.content = content

    def log_behavior_action(self, instance):
        behavior = self.behavior_spinner.text
        comment = self.comment_input.text.strip()

        if behavior == "No behaviors available" or not behavior:
            self.logic.show_messagebox("error", "Input Error", "Please select a valid behavior.")
            return

        self.logic.log_behavior_entry_logic(self.student_id, behavior, comment)
        self.dismiss()

class SettingsPopup(Popup): # ... (as before) ...
    def __init__(self, logic, **kwargs):
        super().__init__(**kwargs)
        self.logic = logic
        self.title = "Application Settings"
        self.size_hint = (0.95, 0.9)

        main_content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        scroll_view = ScrollView(size_hint=(1, 1))
        settings_grid = GridLayout(cols=2, spacing=10, size_hint_y=None)
        settings_grid.bind(minimum_height=settings_grid.setter('height'))
        self.setting_widgets = {}

        settings_grid.add_widget(Label(text="Show Recent Logs on Boxes:"))
        chk_show_logs = CheckBox(active=self.logic.settings.get("show_recent_incidents_on_boxes", True))
        self.setting_widgets["show_recent_incidents_on_boxes"] = chk_show_logs
        settings_grid.add_widget(chk_show_logs)

        settings_grid.add_widget(Label(text="Number of Recent Logs:"))
        txt_num_logs = TextInput(text=str(self.logic.settings.get("num_recent_incidents_to_show", 2)), input_filter='int', multiline=False)
        self.setting_widgets["num_recent_incidents_to_show"] = txt_num_logs
        settings_grid.add_widget(txt_num_logs)

        settings_grid.add_widget(Label(text="Autosave Interval (ms):"))
        txt_autosave = TextInput(text=str(self.logic.settings.get("autosave_interval_ms", 30000)), input_filter='int', multiline=False)
        self.setting_widgets["autosave_interval_ms"] = txt_autosave
        settings_grid.add_widget(txt_autosave)

        settings_grid.add_widget(Label(text="Default Student Width:"))
        txt_stud_w = TextInput(text=str(self.logic.settings.get("default_student_box_width", DEFAULT_STUDENT_BOX_WIDTH)), input_filter='int', multiline=False)
        self.setting_widgets["default_student_box_width"] = txt_stud_w
        settings_grid.add_widget(txt_stud_w)

        scroll_view.add_widget(settings_grid)
        main_content.add_widget(scroll_view)

        buttons_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        save_button = Button(text="Save Settings")
        save_button.bind(on_press=self.save_settings_action)
        buttons_layout.add_widget(save_button)
        cancel_button = Button(text="Cancel")
        cancel_button.bind(on_press=self.dismiss)
        buttons_layout.add_widget(cancel_button)
        main_content.add_widget(buttons_layout)
        self.content = main_content

    def save_settings_action(self, instance):
        new_settings = {}
        try:
            new_settings["show_recent_incidents_on_boxes"] = self.setting_widgets["show_recent_incidents_on_boxes"].active
            new_settings["num_recent_incidents_to_show"] = int(self.setting_widgets["num_recent_incidents_to_show"].text)
            new_settings["autosave_interval_ms"] = int(self.setting_widgets["autosave_interval_ms"].text)
            new_settings["default_student_box_width"] = int(self.setting_widgets["default_student_box_width"].text)
        except ValueError:
            self.logic.show_messagebox("error", "Invalid Input", "Please ensure all numeric fields are valid numbers.")
            return
        self.logic.save_settings_logic(new_settings)
        self.dismiss()

class QuizScorePopup(Popup): # ... (as before) ...
    def __init__(self, logic, student_id, student_full_name, **kwargs):
        super().__init__(**kwargs)
        self.logic = logic
        self.student_id = student_id
        self.student_full_name = student_full_name
        self.title = f"Log Quiz Score for {self.student_full_name}"
        self.size_hint = (0.9, 0.9)
        self.mark_inputs_dict = {}

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        scroll_content = ScrollView()
        form_layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        form_layout.bind(minimum_height=form_layout.setter('height'))

        form_layout.add_widget(Label(text="Quiz Name:"))
        self.quiz_name_input = TextInput(text=self.logic.settings.get("default_quiz_name", "Pop Quiz"), multiline=False)
        form_layout.add_widget(self.quiz_name_input)

        form_layout.add_widget(Label(text="Load Template:"))
        template_names = ["None"] + [t_data.get("name", t_id) for t_id, t_data in self.logic.quiz_templates.items()]
        self.template_spinner = Spinner(text="None", values=tuple(template_names))
        self.template_spinner.bind(text=self.load_template_data_action)
        form_layout.add_widget(self.template_spinner)

        form_layout.add_widget(Label(text="Number of Questions:"))
        self.num_questions_input = TextInput(text=str(self.logic.settings.get("default_quiz_questions", 10)), input_filter='int', multiline=False)
        form_layout.add_widget(self.num_questions_input)

        self.marks_grid = GridLayout(cols=2, spacing=5, size_hint_y=None)
        self.marks_grid.bind(minimum_height=self.marks_grid.setter('height'))
        self.populate_mark_inputs()

        form_layout.add_widget(Label(text="Marks:", size_hint_y=None, height=30))
        form_layout.add_widget(self.marks_grid)

        form_layout.add_widget(Label(text="Comment:"))
        self.comment_input = TextInput(text="", multiline=True, size_hint_y=None, height=80)
        form_layout.add_widget(self.comment_input)

        scroll_content.add_widget(form_layout)
        main_layout.add_widget(scroll_content)

        buttons_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        log_button = Button(text="Log Score")
        log_button.bind(on_press=self.log_score_action)
        buttons_layout.add_widget(log_button)
        cancel_button = Button(text="Cancel")
        cancel_button.bind(on_press=self.dismiss)
        buttons_layout.add_widget(cancel_button)
        main_layout.add_widget(buttons_layout)
        self.content = main_layout

    def populate_mark_inputs(self, template_marks=None):
        self.marks_grid.clear_widgets()
        self.mark_inputs_dict.clear()
        quiz_mark_types = self.logic.settings.get("quiz_mark_types", DEFAULT_QUIZ_MARK_TYPES)

        for mark_type in quiz_mark_types:
            mark_id = mark_type["id"]
            mark_name = mark_type["name"]
            default_val_str = str(template_marks.get(mark_id, 0) if template_marks else 0)

            self.marks_grid.add_widget(Label(text=f"{mark_name}:", size_hint_y=None, height=30))
            mark_input = TextInput(text=default_val_str, input_filter='int', multiline=False, size_hint_y=None, height=40)
            self.mark_inputs_dict[mark_id] = mark_input
            self.marks_grid.add_widget(mark_input)

    def load_template_data_action(self, spinner, text):
        if text == "None":
            self.quiz_name_input.text = self.logic.settings.get("default_quiz_name", "Pop Quiz")
            self.num_questions_input.text = str(self.logic.settings.get("default_quiz_questions", 10))
            self.populate_mark_inputs()
            self.comment_input.text = ""
            return

        selected_template_data = None
        for t_id, t_data in self.logic.quiz_templates.items():
            if t_data.get("name", t_id) == text:
                selected_template_data = t_data
                break

        if selected_template_data:
            self.quiz_name_input.text = selected_template_data.get("name", "")
            self.num_questions_input.text = str(selected_template_data.get("num_questions", self.logic.settings.get("default_quiz_questions", 10)))
            self.populate_mark_inputs(template_marks=selected_template_data.get("marks_data", {}))
            self.comment_input.text = selected_template_data.get("comment", "")

    def log_score_action(self, instance):
        quiz_name = self.quiz_name_input.text.strip()
        comment = self.comment_input.text.strip()
        marks_data = {}

        try:
            num_questions = int(self.num_questions_input.text)
            if num_questions < 0: raise ValueError("Number of questions cannot be negative.")
        except ValueError:
            self.logic.show_messagebox("error", "Invalid Input", "Number of Questions must be a valid non-negative integer.")
            return

        if not quiz_name:
            self.logic.show_messagebox("error", "Invalid Input", "Quiz Name cannot be empty.")
            return

        try:
            for mark_id, text_input_widget in self.mark_inputs_dict.items():
                marks_data[mark_id] = int(text_input_widget.text) if text_input_widget.text else 0
        except ValueError:
            self.logic.show_messagebox("error", "Invalid Input", "All mark fields must be valid integers.")
            return

        self.logic.log_quiz_score_entry_logic(self.student_id, quiz_name, marks_data, comment, num_questions)
        self.dismiss()

class ManualHomeworkLogPopup(Popup): # ... (as before) ...
    def __init__(self, logic, student_id, student_full_name, log_marks_enabled, **kwargs):
        super().__init__(**kwargs)
        self.logic = logic
        self.student_id = student_id
        self.student_full_name = student_full_name
        self.log_marks_enabled = log_marks_enabled
        self.title = f"Log Homework for {self.student_full_name}"
        self.size_hint = (0.9, 0.85)
        self.hw_mark_inputs_dict = {}

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        scroll_content = ScrollView()
        form_layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        form_layout.bind(minimum_height=form_layout.setter('height'))

        if not self.log_marks_enabled:
            form_layout.add_widget(Label(text="Homework Type:"))
            hw_types = self.logic.all_homework_types if self.logic.all_homework_types else ["No types defined"]
            self.homework_type_spinner = Spinner(text=hw_types[0], values=tuple(hw_types))
            form_layout.add_widget(self.homework_type_spinner)

            form_layout.add_widget(Label(text="Status:"))
            hw_statuses = self.logic.all_homework_statuses if self.logic.all_homework_statuses else ["No statuses defined"]
            self.homework_status_spinner = Spinner(text=hw_statuses[0], values=tuple(hw_statuses))
            form_layout.add_widget(self.homework_status_spinner)

            form_layout.add_widget(Label(text="Comment:"))
            self.comment_input_simple = TextInput(text="", multiline=True, size_hint_y=None, height=100)
            form_layout.add_widget(self.comment_input_simple)
        else:
            form_layout.add_widget(Label(text="Homework Type/Name:"))
            self.homework_name_input_detailed = TextInput(text="", multiline=False)
            form_layout.add_widget(self.homework_name_input_detailed)

            form_layout.add_widget(Label(text="Load Template:"))
            hw_template_names = ["None"] + [t_data.get("name", t_id) for t_id, t_data in self.logic.homework_templates.items()]
            self.hw_template_spinner = Spinner(text="None", values=tuple(hw_template_names))
            self.hw_template_spinner.bind(text=self.load_hw_template_data_action)
            form_layout.add_widget(self.hw_template_spinner)

            form_layout.add_widget(Label(text="Number of Items:"))
            self.num_hw_items_input = TextInput(text="1", input_filter='int', multiline=False)
            form_layout.add_widget(self.num_hw_items_input)

            self.hw_marks_grid = GridLayout(cols=2, spacing=5, size_hint_y=None)
            self.hw_marks_grid.bind(minimum_height=self.hw_marks_grid.setter('height'))
            self.populate_hw_mark_inputs()

            form_layout.add_widget(Label(text="Marks:", size_hint_y=None, height=30))
            form_layout.add_widget(self.hw_marks_grid)

            form_layout.add_widget(Label(text="Comment:"))
            self.comment_input_detailed = TextInput(text="", multiline=True, size_hint_y=None, height=80)
            form_layout.add_widget(self.comment_input_detailed)

        scroll_content.add_widget(form_layout)
        main_layout.add_widget(scroll_content)

        buttons_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        log_button = Button(text="Log Homework")
        log_button.bind(on_press=self.log_homework_action)
        buttons_layout.add_widget(log_button)
        cancel_button = Button(text="Cancel")
        cancel_button.bind(on_press=self.dismiss)
        buttons_layout.add_widget(cancel_button)
        main_layout.add_widget(buttons_layout)
        self.content = main_layout

        if self.log_marks_enabled and hasattr(self, 'hw_template_spinner') and self.logic.homework_templates:
             if len(hw_template_names) == 2 and hw_template_names[0] == "None":
                self.hw_template_spinner.text = hw_template_names[1]

    def populate_hw_mark_inputs(self, template_marks=None):
        if not hasattr(self, 'hw_marks_grid'): return
        self.hw_marks_grid.clear_widgets()
        self.hw_mark_inputs_dict.clear()
        homework_mark_types = self.logic.settings.get("homework_mark_types", DEFAULT_HOMEWORK_MARK_TYPES)

        for mark_type in homework_mark_types:
            mark_id = mark_type["id"]
            mark_name = mark_type["name"]
            default_val_str = str(template_marks.get(mark_id, "") if template_marks else "")

            self.hw_marks_grid.add_widget(Label(text=f"{mark_name}:", size_hint_y=None, height=30))
            mark_input = TextInput(text=default_val_str, input_filter='float', multiline=False, size_hint_y=None, height=40)
            self.hw_mark_inputs_dict[mark_id] = mark_input
            self.hw_marks_grid.add_widget(mark_input)

    def load_hw_template_data_action(self, spinner, text):
        if not self.log_marks_enabled or text == "None":
            if self.log_marks_enabled and hasattr(self, 'homework_name_input_detailed'):
                self.homework_name_input_detailed.text = ""
                self.num_hw_items_input.text = "1"
                self.populate_hw_mark_inputs()
                if hasattr(self, 'comment_input_detailed'): self.comment_input_detailed.text = ""
            return

        selected_template_data = None
        for t_id, t_data in self.logic.homework_templates.items():
            if t_data.get("name", t_id) == text:
                selected_template_data = t_data
                break

        if selected_template_data and hasattr(self, 'homework_name_input_detailed'):
            self.homework_name_input_detailed.text = selected_template_data.get("name", "")
            self.num_hw_items_input.text = str(selected_template_data.get("num_items", 1))
            self.populate_hw_mark_inputs(template_marks=selected_template_data.get("marks_data", {}))
            if hasattr(self, 'comment_input_detailed'): self.comment_input_detailed.text = selected_template_data.get("comment", "")

    def log_homework_action(self, instance):
        if not self.log_marks_enabled:
            homework_type = self.homework_type_spinner.text
            homework_status = self.homework_status_spinner.text
            comment = self.comment_input_simple.text.strip()

            if homework_type == "No types defined" or not homework_type:
                self.logic.show_messagebox("error", "Input Error", "Please select a homework type.")
                return
            if homework_status == "No statuses defined" or not homework_status:
                self.logic.show_messagebox("error", "Input Error", "Please select a homework status.")
                return
            self.logic.log_homework_entry_logic(self.student_id, homework_type, comment, homework_status=homework_status)
        else:
            homework_type = self.homework_name_input_detailed.text.strip()
            comment = self.comment_input_detailed.text.strip()
            marks_data = {}
            try:
                num_items_str = self.num_hw_items_input.text
                num_items = int(num_items_str) if num_items_str else 0
                if num_items < 0: raise ValueError("Number of items cannot be negative.")
            except ValueError:
                self.logic.show_messagebox("error", "Invalid Input", "Number of Items must be a valid non-negative integer.")
                return

            if not homework_type:
                self.logic.show_messagebox("error", "Invalid Input", "Homework Type/Name cannot be empty.")
                return
            try:
                for mark_id, text_input_widget in self.hw_mark_inputs_dict.items():
                    val_str = text_input_widget.text.strip()
                    marks_data[mark_id] = float(val_str) if val_str else 0.0
            except ValueError:
                self.logic.show_messagebox("error", "Invalid Input", "All mark fields must be valid numbers.")
                return
            self.logic.log_homework_entry_logic(self.student_id, homework_type, comment, marks_data=marks_data, num_items=num_items)
        self.dismiss()

class ExportFilterPopup(Popup): # ... (as before) ...
    def __init__(self, logic, export_format, **kwargs):
        super().__init__(**kwargs)
        self.logic = logic
        self.export_format = export_format
        self.title = f"Export Log Options ({export_format.upper()})"
        self.size_hint = (0.95, 0.9)
        self.filter_widgets = {}

        main_layout = BoxLayout(orientation='vertical', padding="10dp", spacing="10dp")
        scroll_view = ScrollView()
        grid = GridLayout(cols=2, spacing="10dp", size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        grid.add_widget(Label(text="Start Date (YYYY-MM-DD):"))
        self.start_date_input = TextInput(text="", multiline=False, hint_text="Optional")
        grid.add_widget(self.start_date_input); self.filter_widgets['start_date'] = self.start_date_input
        grid.add_widget(Label(text="End Date (YYYY-MM-DD):"))
        self.end_date_input = TextInput(text="", multiline=False, hint_text="Optional")
        grid.add_widget(self.end_date_input); self.filter_widgets['end_date'] = self.end_date_input
        grid.add_widget(Label(text="Students:"))
        self.student_filter_spinner = Spinner(text="All Students", values=("All Students", "Specific (TODO)"))
        grid.add_widget(self.student_filter_spinner); self.filter_widgets['selected_students_option'] = self.student_filter_spinner
        grid.add_widget(Label(text="Behaviors/Quizzes:"))
        self.behavior_filter_spinner = Spinner(text="All Behaviors/Quizzes", values=("All Behaviors/Quizzes", "Specific (TODO)"))
        grid.add_widget(self.behavior_filter_spinner); self.filter_widgets['selected_behaviors_option'] = self.behavior_filter_spinner
        grid.add_widget(Label(text="Homework Types:"))
        self.homework_filter_spinner = Spinner(text="All Homework Types", values=("All Homework Types", "Specific (TODO)"))
        grid.add_widget(self.homework_filter_spinner); self.filter_widgets['selected_homework_types_option'] = self.homework_filter_spinner

        log_types_box = BoxLayout(orientation='vertical', size_hint_y=None); log_types_box.bind(minimum_height=log_types_box.setter('height'))
        log_types_box.add_widget(Label(text="Include Log Types:", bold=True, size_hint_y=None, height='30dp'))
        self.chk_behavior = CheckBox(active=True); log_types_box.add_widget(BoxLayout(children=[self.chk_behavior, Label(text="Behavior Logs")]))
        self.chk_quiz = CheckBox(active=True);     log_types_box.add_widget(BoxLayout(children=[self.chk_quiz, Label(text="Quiz Logs")]))
        self.chk_homework = CheckBox(active=True); log_types_box.add_widget(BoxLayout(children=[self.chk_homework, Label(text="Homework Logs")]))
        grid.add_widget(log_types_box)
        self.filter_widgets['include_behavior_logs'] = self.chk_behavior
        self.filter_widgets['include_quiz_logs'] = self.chk_quiz
        self.filter_widgets['include_homework_logs'] = self.chk_homework
        grid.add_widget(Widget())

        if self.export_format in ["xlsx", "xlsm"]:
            excel_options_box = BoxLayout(orientation='vertical', size_hint_y=None); excel_options_box.bind(minimum_height=excel_options_box.setter('height'))
            excel_options_box.add_widget(Label(text="Excel Options:", bold=True, size_hint_y=None, height='30dp'))
            self.chk_summaries = CheckBox(active=True); excel_options_box.add_widget(BoxLayout(children=[self.chk_summaries, Label(text="Include Summaries")]))
            self.chk_separate_sheets = CheckBox(active=True); excel_options_box.add_widget(BoxLayout(children=[self.chk_separate_sheets, Label(text="Separate Sheets by Log Type")]))
            self.chk_master_log = CheckBox(active=True); excel_options_box.add_widget(BoxLayout(children=[self.chk_master_log, Label(text="Include Master Log (if separate)")]))
            grid.add_widget(excel_options_box)
            self.filter_widgets['include_summaries'] = self.chk_summaries
            self.filter_widgets['separate_sheets_by_log_type'] = self.chk_separate_sheets
            self.filter_widgets['include_master_log'] = self.chk_master_log
            grid.add_widget(Widget())

        scroll_content.add_widget(grid)
        main_layout.add_widget(scroll_content)

        buttons_layout = BoxLayout(size_hint_y=None, height="50dp", spacing="10dp")
        export_btn = Button(text="Export"); export_btn.bind(on_press=self.export_action)
        buttons_layout.add_widget(export_btn)
        cancel_btn = Button(text="Cancel"); cancel_btn.bind(on_press=self.dismiss)
        buttons_layout.add_widget(cancel_btn)
        main_layout.add_widget(buttons_layout)
        self.content = main_layout

    def export_action(self, instance):
        filter_settings = {
            "start_date": self.filter_widgets['start_date'].text or None,
            "end_date": self.filter_widgets['end_date'].text or None,
            "selected_students": "all" if self.filter_widgets['selected_students_option'].text == "All Students" else "specific",
            "student_ids": [],
            "selected_behaviors": "all" if self.filter_widgets['selected_behaviors_option'].text == "All Behaviors/Quizzes" else "specific",
            "behaviors_list": [],
            "selected_homework_types": "all" if self.filter_widgets['selected_homework_types_option'].text == "All Homework Types" else "specific",
            "homework_types_list": [],
            "include_behavior_logs": self.filter_widgets['include_behavior_logs'].active,
            "include_quiz_logs": self.filter_widgets['include_quiz_logs'].active,
            "include_homework_logs": self.filter_widgets['include_homework_logs'].active,
        }
        if self.export_format in ["xlsx", "xlsm"]:
            filter_settings["include_summaries"] = self.filter_widgets['include_summaries'].active
            filter_settings["separate_sheets_by_log_type"] = self.filter_widgets['separate_sheets_by_log_type'].active
            filter_settings["include_master_log"] = self.filter_widgets['include_master_log'].active

        for date_key in ['start_date', 'end_date']:
            date_str = filter_settings[date_key]
            if date_str:
                try: filter_settings[date_key] = datetime_date.fromisoformat(date_str)
                except ValueError: self.logic.show_messagebox("error", "Invalid Date", f"Invalid format for {date_key.replace('_',' ').title()}. Use YYYY-MM-DD."); return

        self.logic.export_log_data_kivy(filter_settings, self.export_format)
        self.dismiss()


class StudentWidget(Widget): # ... (as before, with on_size/on_pos redraw bindings) ...
    item_id = StringProperty('')
    is_selected = BooleanProperty(False)
    student_data = ObjectProperty(None)

    def __init__(self, student_data, logic, item_id, **kwargs):
        super().__init__(**kwargs)
        self.student_data = student_data
        self.logic = logic
        self.item_id = item_id
        self.size_hint = (None, None)
        self.bind(size=self.redraw, pos=self.redraw) # Redraw when Kivy changes size/pos

    def on_student_data(self, instance, value): self.redraw()
    def on_is_selected(self, instance, value): self.redraw()

    def redraw(self, *args): # Added *args for Kivy property bindings
        self.canvas.clear()
        if not self.student_data: return

        with self.canvas:
            style_overrides = self.student_data.get("style_overrides", {})

            # Use self.size directly as ScatterLayout parent sets it in world units converted to screen pixels by its transform

            fill_color_str = style_overrides.get("fill_color", self.logic.settings.get("student_box_fill_color", DEFAULT_BOX_FILL_COLOR))
            outline_color_str = style_overrides.get("outline_color", self.logic.settings.get("student_box_outline_color", DEFAULT_BOX_OUTLINE_COLOR))

            try: Color(*get_color_from_hex(fill_color_str))
            except: Color(0.5, 0.5, 0.5, 1)
            Rectangle(pos=(0,0), size=self.size)

            try: Color(*get_color_from_hex(outline_color_str))
            except: Color(0.2, 0.2, 0.2, 1)
            Line(rectangle=(0,0, self.width, self.height), width=1.5)

            if self.is_selected:
                Color(1, 0, 0, 0.5)
                Line(rectangle=(-2,-2, self.width+4, self.height+4), width=3)
                if self.logic.edit_mode_var_kivy:
                    handle_size = RESIZE_HANDLE_SIZE # This is in screen pixels
                    Color(1,0,0,0.8)
                    # Handle positions are relative to widget's (0,0)
                    self.resize_handles_instructions = {}
                    handle_positions = {
                        "tl": (0, self.height - handle_size), "tm": (self.width/2 - handle_size/2, self.height - handle_size),
                        "tr": (self.width - handle_size, self.height - handle_size), "ml": (0, self.height/2 - handle_size/2),
                        "mr": (self.width - handle_size, self.height/2 - handle_size/2), "bl": (0, 0),
                        "bm": (self.width/2 - handle_size/2, 0), "br": (self.width - handle_size, 0)
                    }
                    for name, pos_val in handle_positions.items():
                        group = InstructionGroup(group=f'resize_handle_{name}') # Group name for hit testing
                        group.add(Rectangle(pos=pos_val, size=(handle_size, handle_size)))
                        self.canvas.add(group)
                        self.resize_handles_instructions[name] = group


            name_to_display = self.student_data.get('nickname') or self.student_data['first_name']
            font_size_sp = self.logic.settings.get("student_font_size", DEFAULT_FONT_SIZE)
            behavior_font_size_sp = self.logic.settings.get("behavior_font_size", DEFAULT_FONT_SIZE)

            label = CoreLabel(text=name_to_display, font_size=font_size_sp, color=get_color_from_hex(DEFAULT_FONT_COLOR))
            label.refresh()
            text_texture = label.texture
            if text_texture:
                text_w, text_h = text_texture.size
                max_text_w = self.width * 0.9
                if text_w > max_text_w and max_text_w > 0 :
                    scale_factor = max_text_w / text_w
                    text_w *= scale_factor
                    text_h *= scale_factor

                text_x = (self.width - text_w) / 2
                text_y = (self.height - text_h) / 2 + text_h * 0.3
                Color(*get_color_from_hex(DEFAULT_FONT_COLOR))
                Rectangle(texture=text_texture, size=(text_w, text_h), pos=(text_x, text_y))

            # Draw behavior logs
            if self.logic.settings.get("show_recent_incidents_on_boxes", True):
                y_offset = text_y - 5
                for log in self.logic.get_recent_incidents_for_student(self.item_id):
                    log_text = log['behavior']
                    log_label = CoreLabel(text=log_text, font_size=behavior_font_size_sp, color=get_color_from_hex(DEFAULT_FONT_COLOR))
                    log_label.refresh()
                    log_texture = log_label.texture
                    if log_texture:
                        log_w, log_h = log_texture.size
                        max_log_w = self.width * 0.9
                        if log_w > max_log_w and max_log_w > 0:
                            log_scale_factor = max_log_w / log_w
                            log_w *= log_scale_factor
                            log_h *= log_scale_factor
                        log_x = (self.width - log_w) / 2
                        y_offset -= log_h
                        Color(*get_color_from_hex(DEFAULT_FONT_COLOR))
                        Rectangle(texture=log_texture, size=(log_w, log_h), pos=(log_x, y_offset))


class FurnitureWidget(Widget): # ... (as before, with on_size/on_pos redraw bindings and handle drawing) ...
    item_id = StringProperty('')
    is_selected = BooleanProperty(False)
    furniture_data = ObjectProperty(None)

    def __init__(self, furniture_data, logic, item_id, **kwargs):
        super().__init__(**kwargs)
        self.furniture_data = furniture_data
        self.logic = logic
        self.item_id = item_id
        self.size_hint = (None, None)
        self.bind(size=self.redraw, pos=self.redraw)

    def on_furniture_data(self, instance, value): self.redraw()
    def on_is_selected(self, instance, value): self.redraw()

    def redraw(self, *args):
        self.canvas.clear()
        if not self.furniture_data: return
        with self.canvas:
            fill_color_str = self.furniture_data.get("fill_color", "#CCCCCC")
            outline_color_str = self.furniture_data.get("outline_color", "#888888")
            try: Color(*get_color_from_hex(fill_color_str))
            except: Color(0.8, 0.8, 0.8, 1)
            Rectangle(pos=(0,0), size=self.size)
            try: Color(*get_color_from_hex(outline_color_str))
            except: Color(0.5, 0.5, 0.5, 1)
            Line(rectangle=(0,0, self.width, self.height), width=1.5)

            if self.is_selected:
                Color(0, 0, 1, 0.5)
                Line(rectangle=(-2,-2, self.width+4, self.height+4), width=3)
                if self.logic.edit_mode_var_kivy:
                    handle_size = RESIZE_HANDLE_SIZE
                    Color(0,0,1,0.8) # Blue handles for furniture
                    self.resize_handles_instructions = {}
                    handle_positions = {
                        "tl": (0, self.height - handle_size), "tm": (self.width/2 - handle_size/2, self.height - handle_size),
                        "tr": (self.width - handle_size, self.height - handle_size), "ml": (0, self.height/2 - handle_size/2),
                        "mr": (self.width - handle_size, self.height/2 - handle_size/2), "bl": (0, 0),
                        "bm": (self.width/2 - handle_size/2, 0), "br": (self.width - handle_size, 0)
                    }
                    for name, pos_val in handle_positions.items():
                        group = InstructionGroup(group=f'resize_handle_{name}')
                        group.add(Rectangle(pos=pos_val, size=(handle_size, handle_size)))
                        self.canvas.add(group)
                        self.resize_handles_instructions[name] = group

            name_to_display = self.furniture_data.get('name', "Furniture")
            font_size_sp = self.logic.settings.get("student_font_size", DEFAULT_FONT_SIZE) -1
            label = CoreLabel(text=name_to_display, font_size=font_size_sp, color=get_color_from_hex(DEFAULT_FONT_COLOR))
            label.refresh()
            text_texture = label.texture
            if text_texture:
                text_w, text_h = text_texture.size
                max_text_w = self.width * 0.9
                if text_w > max_text_w and max_text_w > 0:
                    scale_factor = max_text_w / text_w
                    text_w *= scale_factor; text_h *= scale_factor
                text_x = (self.width - text_w) / 2; text_y = (self.height - text_h) / 2
                Color(*get_color_from_hex(DEFAULT_FONT_COLOR))
                Rectangle(texture=text_texture, size=(text_w, text_h), pos=(text_x, text_y))


class SeatingCanvasLayout(ScatterLayout):
    # ... (init, redraw_all_items_on_canvas, get_widget_at_touch, get_resize_handle_at_touch as before) ...
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app_logic = App.get_running_app().logic
        self.do_rotation = False; self.do_scale = True; self.do_translation_x = True; self.do_translation_y = True
        self.scale_min = 0.2; self.scale_max = 5.0
        self.current_drag_info: Optional[Dict[str, Any]] = None
        self.last_touch_pos = (0,0)
        self.ruler_size = 30  # In screen pixels
        self.ruler_color = get_color_from_hex("#e0e0e0")
        self.ruler_line_color = get_color_from_hex("#555555")
        self.ruler_text_color = get_color_from_hex("#333333")
        self.guide_line_color = get_color_from_hex("#0000FF80") # Blue with alpha
        self.active_guide_placement: Optional[Tuple[str, float]] = None # e.g. ('h', 100.5) or ('v', 50.0)
        self.guides_to_draw: List[Tuple[str, float]] = [] # List of ('h' or 'v', world_coord)

    def redraw_all_items_on_canvas(self, *args):
        self.canvas.before.clear()
        self.canvas.after.clear()

        if self.app_logic.settings.get('show_rulers', False):
            self.draw_rulers()

        if self.app_logic.settings.get('show_grid', False):
            self.draw_grid()

        self.draw_guides() # Draw temporary guides

        self.app_logic.draw_all_items_kivy(self)

    def draw_grid(self):
        with self.canvas.before: # Draw grid before items and rulers
            grid_size = self.app_logic.settings.get('grid_size', DEFAULT_GRID_SIZE)
            if grid_size <= 0: return

            Color(0.8, 0.8, 0.8, 0.5) # Light grey for grid lines

            # Get visible world rect
            bottom_left_world = self.to_local(0,0)
            top_right_world = self.to_local(self.width, self.height)

            visible_world_x_min = bottom_left_world[0]
            visible_world_x_max = top_right_world[0]
            visible_world_y_min = bottom_left_world[1]
            visible_world_y_max = top_right_world[1]

            # Vertical grid lines
            start_grid_x = (int(visible_world_x_min / grid_size)) * grid_size
            for world_x in range(start_grid_x, int(visible_world_x_max + grid_size), grid_size):
                # Transform world x to screen x for line drawing
                screen_x_start, screen_y_start = self.to_parent(world_x, visible_world_y_min)
                screen_x_end, screen_y_end = self.to_parent(world_x, visible_world_y_max)
                # Ensure lines are drawn within ScatterLayout's bounds if they map outside due to rotation/scale
                # This is simplified; true clipping to viewport is more complex with Scatter's transform
                Line(points=[screen_x_start, 0, screen_x_end, self.height], width=0.5)


            # Horizontal grid lines
            start_grid_y = (int(visible_world_y_min / grid_size)) * grid_size
            for world_y in range(start_grid_y, int(visible_world_y_max + grid_size), grid_size):
                screen_x_start, screen_y_start = self.to_parent(visible_world_x_min, world_y)
                screen_x_end, screen_y_end = self.to_parent(visible_world_x_max, world_y)
                Line(points=[0, screen_y_start, self.width, screen_y_end], width=0.5)


    def draw_rulers(self):
        # Rulers are drawn in screen space, but markings reflect world coordinates
        # This requires transforming world coordinates to screen coordinates considering pan and zoom.
        # The ScatterLayout's transform (self.transform) does this.

        # Horizontal Ruler (Top)
        with self.canvas.before: # Draw before items
            Color(*self.ruler_color)
            Rectangle(pos=(0, self.height - self.ruler_size), size=(self.width, self.ruler_size))
            Color(*self.ruler_line_color)
            Line(points=[0, self.height - self.ruler_size, self.width, self.height - self.ruler_size], width=1)

            # Vertical Ruler (Left)
            Color(*self.ruler_color)
            Rectangle(pos=(0, 0), size=(self.ruler_size, self.height - self.ruler_size)) # Avoid overlap with H ruler
            Color(*self.ruler_line_color)
            Line(points=[self.ruler_size, 0, self.ruler_size, self.height - self.ruler_size], width=1)

            # Markings - this is the tricky part due to zoom/pan
            # We need to find what world coordinates are visible and map them to screen positions
            # The ScatterLayout's to_local and to_parent methods handle coordinate transformations.
            # to_local: screen/parent to widget local. to_parent: widget local to screen/parent.
            # For rulers, we are interested in the world coordinates visible in the viewport.

            # Get visible world rect (approximate)
            bottom_left_world = self.to_local(0, 0)
            top_right_world = self.to_local(self.width, self.height)

            visible_world_x_min = bottom_left_world[0]
            visible_world_x_max = top_right_world[0]
            visible_world_y_min = bottom_left_world[1]
            visible_world_y_max = top_right_world[1]

            # Horizontal Ruler Markings
            # Determine a suitable interval for markings based on zoom level
            # World units per 100 pixels on screen (approx)
            world_per_100px_h = abs(self.to_local(100,0)[0] - self.to_local(0,0)[0])
            interval_h = 10
            if world_per_100px_h > 50: interval_h = 50
            if world_per_100px_h > 100: interval_h = 100
            if world_per_100px_h > 200: interval_h = 200
            if world_per_100px_h < 10 : interval_h = 5
            if world_per_100px_h < 2 : interval_h = 1


            start_mark_x = (int(visible_world_x_min / interval_h)) * interval_h
            for world_x in range(start_mark_x, int(visible_world_x_max + interval_h), interval_h):
                screen_x, _ = self.to_parent(world_x, 0) # Convert world_x to screen_x
                if screen_x > self.ruler_size and screen_x < self.width: # Draw only if visible on ruler
                    tick_height = 5 if world_x % (interval_h * 5) != 0 else 10
                    Line(points=[screen_x, self.height - self.ruler_size, screen_x, self.height - self.ruler_size + tick_height], width=1)
                    if tick_height == 10:
                        label = CoreLabel(text=str(world_x), font_size=10, color=self.ruler_text_color)
                        label.refresh()
                        if label.texture:
                             Rectangle(texture=label.texture, pos=(screen_x + 2, self.height - self.ruler_size + tick_height + 2), size=label.texture.size)

            # Vertical Ruler Markings
            world_per_100px_v = abs(self.to_local(0,100)[1] - self.to_local(0,0)[1])
            interval_v = 10
            if world_per_100px_v > 50: interval_v = 50
            if world_per_100px_v > 100: interval_v = 100
            if world_per_100px_v > 200: interval_v = 200
            if world_per_100px_v < 10 : interval_v = 5
            if world_per_100px_v < 2 : interval_v = 1


            start_mark_y = (int(visible_world_y_min / interval_v)) * interval_v
            for world_y in range(start_mark_y, int(visible_world_y_max + interval_v), interval_v):
                _, screen_y = self.to_parent(0, world_y)
                if screen_y > 0 and screen_y < self.height - self.ruler_size:
                    tick_width = 5 if world_y % (interval_v * 5) != 0 else 10
                    Line(points=[self.ruler_size - tick_width, screen_y, self.ruler_size, screen_y], width=1)
                    if tick_width == 10:
                        label = CoreLabel(text=str(world_y), font_size=10, color=self.ruler_text_color)
                        label.refresh()
                        if label.texture:
                            # Rotate text for vertical ruler (Kivy labels don't rotate easily, draw texture rotated)
                            # This is complex with PushMatrix/Rotate/PopMatrix or drawing to Fbo then texture.
                            # For simplicity, draw text horizontally next to ruler for now.
                            Rectangle(texture=label.texture, pos=(self.ruler_size - tick_width - label.texture.width - 2, screen_y - label.texture.height / 2), size=label.texture.size)

    def draw_guides(self):
        with self.canvas.after: # Draw guides on top of items
            Color(*self.guide_line_color)
            for guide_type, world_coord in self.guides_to_draw:
                if guide_type == 'h': # Horizontal guide
                    # Convert world_coord (y) to screen coordinates
                    _, screen_y = self.to_parent(0, world_coord)
                    Line(points=[0, screen_y, self.width, screen_y], width=1.2)
                elif guide_type == 'v': # Vertical guide
                    # Convert world_coord (x) to screen coordinates
                    screen_x, _ = self.to_parent(world_coord, 0)
                    Line(points=[screen_x, 0, screen_x, self.height], width=1.2)


    def get_widget_at_touch(self, touch_pos_screen):
        for widget in reversed(self.children): # Children are StudentWidget, FurnitureWidget
            if widget.collide_point(*widget.to_local(*touch_pos_screen, relative_to=self)):
                return widget
        return None

    def get_resize_handle_at_touch(self, widget, touch_pos_widget_local):
        h_size = RESIZE_HANDLE_SIZE
        pad = RESIZE_HANDLE_TOUCH_PADDING
        w, h = widget.size

        handles = {
            "tl": (0-pad, h-h_size-pad, h_size+2*pad, h_size+2*pad),
            "tm": (w/2-h_size/2-pad, h-h_size-pad, h_size+2*pad, h_size+2*pad),
            "tr": (w-h_size-pad, h-h_size-pad, h_size+2*pad, h_size+2*pad),
            "ml": (0-pad, h/2-h_size/2-pad, h_size+2*pad, h_size+2*pad),
            "mr": (w-h_size-pad, h/2-h_size/2-pad, h_size+2*pad, h_size+2*pad),
            "bl": (0-pad, 0-pad, h_size+2*pad, h_size+2*pad),
            "bm": (w/2-h_size/2-pad, 0-pad, h_size+2*pad, h_size+2*pad),
            "br": (w-h_size-pad, 0-pad, h_size+2*pad, h_size+2*pad),
        }
        for handle_type, (hx, hy, hw, hh) in handles.items():
            if hx <= touch_pos_widget_local[0] <= hx + hw and \
               hy <= touch_pos_widget_local[1] <= hy + hh:
                return handle_type
        return None

    def on_touch_down(self, touch: MotionEvent):
        if not self.collide_point(*touch.pos): return False
        self.last_touch_pos = touch.pos
        app_logic = self.app_logic

        # Check for ruler clicks first if rulers are active
        if app_logic.settings.get('show_rulers', False):
            # Horizontal ruler area (top)
            if touch.y > self.height - self.ruler_size and touch.x > self.ruler_size :
                world_x, _ = self.to_local(*touch.pos) # Get world x-coordinate from touch
                self.active_guide_placement = ('v', world_x) # Prepare to place a vertical guide
                app_logic.update_status(f"Click on canvas to place vertical guide at x={world_x:.1f}")
                return True # Consume touch
            # Vertical ruler area (left)
            elif touch.x < self.ruler_size and touch.y < self.height - self.ruler_size:
                _, world_y = self.to_local(*touch.pos) # Get world y-coordinate from touch
                self.active_guide_placement = ('h', world_y) # Prepare to place a horizontal guide
                app_logic.update_status(f"Click on canvas to place horizontal guide at y={world_y:.1f}")
                return True # Consume touch

        # If a guide is pending placement, place it on canvas click
        if self.active_guide_placement:
            guide_type, world_coord = self.active_guide_placement
            # Check if click is on canvas area (not on rulers again)
            if not (touch.y > self.height - self.ruler_size and touch.x > self.ruler_size) and \
               not (touch.x < self.ruler_size and touch.y < self.height - self.ruler_size):
                self.guides_to_draw.append((guide_type, world_coord))
                self.redraw_all_items_on_canvas()
                app_logic.update_status(f"Placed {guide_type} guide at {world_coord:.1f}. Guides are temporary.")
            else: # Clicked on ruler again, cancel placement
                app_logic.update_status("Guide placement cancelled.")
            self.active_guide_placement = None
            return True


        touched_item_widget = self.get_widget_at_touch(touch.pos)

        if touch.is_right_click: # Context Menu
            if self.active_guide_placement: # Cancel guide placement on right click
                self.active_guide_placement = None
                app_logic.update_status("Guide placement cancelled.")
                return True
            if touched_item_widget and hasattr(touched_item_widget, 'item_id'):
                app_logic.show_item_context_menu_kivy(touched_item_widget.item_id,
                                                     "student" if isinstance(touched_item_widget, StudentWidget) else "furniture",
                                                     touch.pos)
            else:
                app_logic.show_canvas_context_menu_kivy(touch.pos)
            return True


        if touched_item_widget and hasattr(touched_item_widget, 'item_id'):
            item_id = touched_item_widget.item_id
            item_data_source = app_logic.students if item_id.startswith("student_") else app_logic.furniture
            item_data_snapshot = item_data_source.get(item_id, {}).copy()
            if "style_overrides" in item_data_snapshot: # Deep copy style_overrides
                item_data_snapshot["style_overrides"] = item_data_snapshot["style_overrides"].copy()


            touch_pos_widget_local = touched_item_widget.to_local(*touch.pos, relative_to=self)

            if app_logic.edit_mode_var_kivy and item_id in app_logic.selected_items:
                handle_type = self.get_resize_handle_at_touch(touched_item_widget, touch_pos_widget_local)
                if handle_type:
                    self.current_drag_info = {
                        'is_resizing': True, 'resize_handle_type': handle_type,
                        'item_id_being_resized': item_id,
                        'start_touch_world_pos': self.to_local(*touch.pos),
                        'original_item_world_data_snapshot': item_data_snapshot,
                        'original_item_world_pos': (item_data_snapshot['x'], item_data_snapshot['y']),
                        'original_item_world_size': (item_data_snapshot['width'], item_data_snapshot['height'])
                    }
                    touch.grab(self); return True

            if touch.is_double_tap:
                 app_logic.update_status(f"Double tap on {item_id}")
                 # TODO: Call edit dialog for the item
                 return True

            is_ctrl_select = 'ctrl' in Window.keyboard_modifiers or 'meta' in Window.keyboard_modifiers
            if not is_ctrl_select:
                if not (len(app_logic.selected_items) == 1 and item_id in app_logic.selected_items):
                    app_logic.selected_items.clear()
            if item_id in app_logic.selected_items:
                if is_ctrl_select: app_logic.selected_items.remove(item_id)
            else: app_logic.selected_items.add(item_id)

            app_logic.draw_all_items_kivy(self)
            app_logic.update_status(f"{len(app_logic.selected_items)} item(s) selected.")

            self.current_drag_info = {
                'items_being_dragged': list(app_logic.selected_items),
                'start_touch_screen_pos': touch.pos,
                'original_item_positions': {
                    sel_id: ( (app_logic.students if sel_id.startswith("student_") else app_logic.furniture)[sel_id]['x'],
                               (app_logic.students if sel_id.startswith("student_") else app_logic.furniture)[sel_id]['y'] )
                    for sel_id in app_logic.selected_items
                    if sel_id in (app_logic.students if sel_id.startswith("student_") else app_logic.furniture)
                }
            }
            touch.grab(self); return True
        else:
            if app_logic.selected_items:
                app_logic.selected_items.clear()
                app_logic.draw_all_items_kivy(self)
                app_logic.update_status("Selection cleared.")
            return super().on_touch_down(touch)

    def on_touch_move(self, touch: MotionEvent):
        if touch.grab_current is not self or not self.current_drag_info:
            return super().on_touch_move(touch)

        app_logic = self.app_logic
        current_touch_world_pos = self.to_local(*touch.pos)
        start_touch_world_pos = self.current_drag_info['start_touch_world_pos']
        dx_world = current_touch_world_pos[0] - start_touch_world_pos[0]
        dy_world = current_touch_world_pos[1] - start_touch_world_pos[1]

        if self.current_drag_info.get('is_resizing'):
            item_id = self.current_drag_info['item_id_being_resized']
            item_widget = app_logic.student_widgets.get(item_id) or app_logic.furniture_widgets.get(item_id)
            item_data_source = app_logic.students if item_id.startswith("student_") else app_logic.furniture
            item_data = item_data_source[item_id]

            orig_x, orig_y = self.current_drag_info['original_item_world_pos']
            orig_w, orig_h = self.current_drag_info['original_item_world_size']
            handle = self.current_drag_info['resize_handle_type']

            new_x, new_y, new_w, new_h = orig_x, orig_y, orig_w, orig_h

            if 'l' in handle: new_x = orig_x + dx_world; new_w = orig_w - dx_world
            if 'r' in handle: new_w = orig_w + dx_world
            if 'b' in handle: new_y = orig_y + dy_world; new_h = orig_h - dy_world
            if 't' in handle: new_h = orig_h + dy_world

            if handle == 'tm': new_y = orig_y + dy_world; new_h = orig_h - dy_world
            elif handle == 'bm': new_h = orig_h + dy_world
            elif handle == 'ml': new_x = orig_x + dx_world; new_w = orig_w - dx_world
            elif handle == 'mr': new_w = orig_w + dx_world

            min_w = MIN_ITEM_WIDTH; min_h = MIN_ITEM_HEIGHT
            if new_w < min_w:
                if 'l' in handle : new_x = orig_x + (orig_w - min_w)
                new_w = min_w
            if new_h < min_h:
                if 't' in handle: new_y = orig_y + (orig_h - min_h)
                new_h = min_h

            item_widget.pos = (new_x, new_y); item_widget.size = (new_w, new_h)
            item_data['x'], item_data['y'], item_data['width'], item_data['height'] = new_x, new_y, new_w, new_h
            if item_id.startswith("student_"):
                if "style_overrides" not in item_data: item_data["style_overrides"] = {}
                item_data["style_overrides"]["width"], item_data["style_overrides"]["height"] = new_w, new_h
        else:
            for item_id in self.current_drag_info['items_being_dragged']:
                original_pos = self.current_drag_info['original_item_positions'].get(item_id)
                if not original_pos: continue
                widget_to_move = app_logic.student_widgets.get(item_id) or app_logic.furniture_widgets.get(item_id)
                if widget_to_move:
                    widget_to_move.pos = (original_pos[0] + dx_world, original_pos[1] + dy_world)
        return True

    def on_touch_up(self, touch: MotionEvent):
        if touch.grab_current is self and self.current_drag_info:
            touch.ungrab(self)
            app_logic = self.app_logic

            if self.current_drag_info.get('is_resizing'):
                item_id = self.current_drag_info['item_id_being_resized']
                item_data_source = app_logic.students if item_id.startswith("student_") else app_logic.furniture
                final_item_data = item_data_source[item_id]
                original_snapshot = self.current_drag_info['original_item_world_data_snapshot']

                changes_dict = {}
                keys_to_check = ['x', 'y', 'width', 'height']
                if item_id.startswith("student_"): keys_to_check.append('style_overrides')

                for key in keys_to_check:
                    new_val = final_item_data.get(key)
                    old_val = original_snapshot.get(key)
                    if isinstance(new_val, dict) and isinstance(old_val, dict): # For style_overrides
                        if new_val != old_val: changes_dict[key] = new_val.copy() # Store a copy
                    elif new_val != old_val:
                        changes_dict[key] = new_val

                if changes_dict:
                    command = EditItemCommand(app_logic, item_id,
                                              "student" if item_id.startswith("student_") else "furniture",
                                              original_snapshot, changes_dict)
                    app_logic.execute_command(command)
                else: # No significant change, redraw to snap back if needed based on original data
                    item_data_source[item_id] = original_snapshot # Revert to pre-drag data
                    app_logic.draw_all_items_kivy(self)


            else: # Was a drag-move operation
                dx_screen = touch.x - self.current_drag_info['start_touch_screen_pos'][0]
                dy_screen = touch.y - self.current_drag_info['start_touch_screen_pos'][1]
                if abs(dx_screen) > DRAG_THRESHOLD or abs(dy_screen) > DRAG_THRESHOLD :
                    dx_world = dx_screen / self.scale
                    dy_world = dy_screen / self.scale
                    moves_for_command = []
                    for item_id in self.current_drag_info['items_being_dragged']:
                        original_pos = self.current_drag_info['original_item_positions'].get(item_id)
                        if not original_pos: continue
                        item_type = "student" if item_id.startswith("student_") else "furniture"
                        new_x, new_y = original_pos[0] + dx_world, original_pos[1] + dy_world
                        if app_logic.settings.get("grid_snap_enabled", False):
                            grid_size = app_logic.settings.get("grid_size", DEFAULT_GRID_SIZE)
                            if grid_size > 0: new_x = round(new_x / grid_size) * grid_size; new_y = round(new_y / grid_size) * grid_size
                        moves_for_command.append({'id': item_id, 'type': item_type, 'old_x': original_pos[0], 'old_y': original_pos[1], 'new_x': new_x, 'new_y': new_y})
                    if moves_for_command:
                        command = MoveItemsCommand(app_logic, moves_for_command)
                        app_logic.execute_command(command) # This saves and redraws all from data
                else: # Not a significant drag, might be a tap
                    # Tap logic could be here, but on_touch_down already handles selection.
                    # If a specific tap action (other than selection) is needed, it would go here.
                    app_logic.draw_all_items_kivy(self) # Ensure final state if no command

            self.current_drag_info = None
            return True
        return super().on_touch_up(touch)


if __name__ == '__main__':
    SeatingChartKivyApp().run()
