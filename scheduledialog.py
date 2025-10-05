import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class ScheduleDialog(tk.Toplevel):
    """Dialog for managing scheduled profile loading."""
    def __init__(self, parent, profiles, schedule_path):
        super().__init__(parent)
        self.transient(parent)
        self.title("Manage Schedule")
        self.parent = parent
        self.profiles = profiles
        self.schedule_path = schedule_path
        self.schedule = self.load_schedule()
        self.result = None
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)

        self.create_widgets()
        self.populate_schedule_list()
        self.center_window()
        self.grab_set()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Schedule List
        list_frame = ttk.LabelFrame(main_frame, text="Schedule Entries")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.schedule_listbox = tk.Listbox(list_frame, exportselection=False, height=10)
        self.schedule_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for the listbox
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.schedule_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.schedule_listbox.config(yscrollcommand=scrollbar.set)

        # Buttons for list management
        list_button_frame = ttk.Frame(main_frame)
        list_button_frame.pack(fill=tk.X, pady=5)

        ttk.Button(list_button_frame, text="Add New", command=self.add_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(list_button_frame, text="Edit Selected", command=self.edit_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(list_button_frame, text="Delete Selected", command=self.delete_entry).pack(side=tk.LEFT, padx=5)

        # Close button
        close_button = ttk.Button(main_frame, text="Close", command=self.on_ok)
        close_button.pack(side=tk.RIGHT, pady=(10, 0))

    def populate_schedule_list(self):
        self.schedule_listbox.delete(0, tk.END)
        for entry in self.schedule:
            days = ", ".join(entry['days'])
            display_text = f"{entry['profile']} from {entry['start_time']} to {entry['end_time']} on {days}"
            self.schedule_listbox.insert(tk.END, display_text)

    def add_entry(self):
        dialog = ScheduleEntryDialog(self, self.profiles)
        self.wait_window(dialog)
        if dialog.result:
            self.schedule.append(dialog.result)
            self.save_schedule()
            self.populate_schedule_list()

    def edit_entry(self):
        selected_indices = self.schedule_listbox.curselection()
        if not selected_indices:
            return
        index = selected_indices[0]
        entry_data = self.schedule[index]

        dialog = ScheduleEntryDialog(self, self.profiles, entry_data)
        self.wait_window(dialog)
        if dialog.result:
            self.schedule[index] = dialog.result
            self.save_schedule()
            self.populate_schedule_list()

    def delete_entry(self):
        selected_indices = self.schedule_listbox.curselection()
        if not selected_indices:
            return
        index = selected_indices[0]
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this schedule entry?", parent=self):
            del self.schedule[index]
            self.save_schedule()
            self.populate_schedule_list()

    def load_schedule(self):
        try:
            with open(self.schedule_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_schedule(self):
        with open(self.schedule_path, 'w') as f:
            json.dump(self.schedule, f, indent=4)

    def on_ok(self):
        self.result = True
        self.destroy()

    def on_cancel(self):
        self.result = False
        self.destroy()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

class ScheduleEntryDialog(tk.Toplevel):
    def __init__(self, parent, profiles, entry_data=None):
        super().__init__(parent)
        self.transient(parent)
        self.title("Schedule Entry")
        self.parent = parent
        self.profiles = profiles
        self.entry_data = entry_data
        self.result = None
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)

        self.create_widgets()
        if self.entry_data:
            self.load_entry_data()

        self.center_window()
        self.grab_set()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Profile selection
        ttk.Label(main_frame, text="Profile:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.profile_var = tk.StringVar()
        profile_names = [p['name'] for p in self.profiles]
        self.profile_menu = ttk.Combobox(main_frame, textvariable=self.profile_var, values=profile_names, state="readonly")
        self.profile_menu.grid(row=0, column=1, columnspan=2, sticky=tk.EW, pady=2)

        # Time selection
        ttk.Label(main_frame, text="Start Time:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.start_time_var = tk.StringVar()
        self.start_time_entry = ttk.Entry(main_frame, textvariable=self.start_time_var)
        self.start_time_entry.grid(row=1, column=1, columnspan=2, sticky=tk.EW, pady=2)

        ttk.Label(main_frame, text="End Time:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.end_time_var = tk.StringVar()
        self.end_time_entry = ttk.Entry(main_frame, textvariable=self.end_time_var)
        self.end_time_entry.grid(row=2, column=1, columnspan=2, sticky=tk.EW, pady=2)

        # Day selection
        ttk.Label(main_frame, text="Days:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.day_vars = {}
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        day_frame = ttk.Frame(main_frame)
        day_frame.grid(row=3, column=1, columnspan=2, sticky=tk.W)
        for i, day in enumerate(days):
            var = tk.BooleanVar()
            self.day_vars[day] = var
            ttk.Checkbutton(day_frame, text=day, variable=var).pack(side=tk.LEFT)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=(10, 0))
        ttk.Button(button_frame, text="OK", command=self.on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.on_cancel).pack(side=tk.LEFT, padx=5)

    def load_entry_data(self):
        self.profile_var.set(self.entry_data.get("profile", ""))
        self.start_time_var.set(self.entry_data.get("start_time", ""))
        self.end_time_var.set(self.entry_data.get("end_time", ""))
        for day, var in self.day_vars.items():
            if day in self.entry_data.get("days", []):
                var.set(True)

    def on_ok(self):
        profile = self.profile_var.get()
        start_time = self.start_time_var.get()
        end_time = self.end_time_var.get()
        days = [day for day, var in self.day_vars.items() if var.get()]

        if not all([profile, start_time, end_time, days]):
            messagebox.showerror("Missing Information", "Please fill all fields.", parent=self)
            return

        try:
            datetime.strptime(start_time, "%H:%M")
            datetime.strptime(end_time, "%H:%M")
        except ValueError:
            messagebox.showerror("Invalid Time", "Time must be in HH:MM format.", parent=self)
            return

        self.result = {"profile": profile, "start_time": start_time, "end_time": end_time, "days": days}
        self.destroy()

    def on_cancel(self):
        self.result = None
        self.destroy()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')