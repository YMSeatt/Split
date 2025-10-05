import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class ProfileDialog(tk.Toplevel):
    """Dialog for selecting, creating, or deleting a user profile."""
    def __init__(self, parent, profiles):
        super().__init__(parent)
        self.transient(parent)
        self.title("Select Profile")
        self.parent = parent
        self.result = None
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)

        self.profiles = profiles

        self.create_widgets()
        self.center_window()
        self.grab_set()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Select a profile to load:", font=("-size 12")).pack(pady=(0, 10))

        self.profile_listbox = tk.Listbox(main_frame, exportselection=False, height=8)
        for profile in self.profiles:
            display_text = profile.get('name', 'Unnamed Profile')
            if profile.get('school'):
                display_text += f" ({profile['school']})"
            self.profile_listbox.insert(tk.END, display_text)

        if self.profiles:
            self.profile_listbox.select_set(0)

        self.profile_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        self.profile_listbox.bind("<Double-1>", self.on_load)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        self.load_button = ttk.Button(button_frame, text="Load Profile", command=self.on_load)
        self.load_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        if not self.profiles:
            self.load_button.config(state=tk.DISABLED)

        self.create_button = ttk.Button(button_frame, text="Create New", command=self.on_create)
        self.create_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        self.delete_button = ttk.Button(button_frame, text="Delete", command=self.on_delete)
        self.delete_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))
        if not self.profiles:
            self.delete_button.config(state=tk.DISABLED)

    def on_load(self, event=None):
        selected_indices = self.profile_listbox.curselection()
        if not selected_indices:
            return
        profile_data = self.profiles[selected_indices[0]]
        self.result = {"action": "load", "profile": profile_data['name']}
        self.destroy()

    def on_create(self):
        self.result = {"action": "create"}
        self.destroy()

    def on_delete(self):
        selected_indices = self.profile_listbox.curselection()
        if not selected_indices:
            return
        profile_to_delete = self.profiles[selected_indices[0]]
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the profile '{profile_to_delete['name']}'?\nThis will permanently delete all associated data.", parent=self):
            self.result = {"action": "delete", "profile": profile_to_delete['name']}
            self.destroy()

    def on_cancel(self):
        self.result = {"action": "cancel"}
        self.destroy()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

class CreateProfileDialog(tk.Toplevel):
    """Dialog for creating a new profile."""
    def __init__(self, parent, existing_profiles):
        super().__init__(parent)
        self.transient(parent)
        self.title("Create New Profile")
        self.parent = parent
        self.existing_profiles = [p['name'].lower() for p in existing_profiles]
        self.result = None
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)

        self.create_widgets()
        self.center_window()
        self.grab_set()
        self.name_entry.focus_set()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Profile Name:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.name_entry = ttk.Entry(main_frame, width=40)
        self.name_entry.grid(row=0, column=1, sticky=tk.EW, pady=2)

        ttk.Label(main_frame, text="School (Optional):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.school_entry = ttk.Entry(main_frame, width=40)
        self.school_entry.grid(row=1, column=1, sticky=tk.EW, pady=2)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=(10, 0))

        ttk.Button(button_frame, text="Create", command=self.on_create).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.on_cancel).pack(side=tk.LEFT, padx=5)

    def on_create(self):
        profile_name = self.name_entry.get().strip()
        if not profile_name:
            messagebox.showerror("Invalid Name", "Profile name cannot be empty.", parent=self)
            return

        if profile_name.lower() in self.existing_profiles:
            messagebox.showerror("Name Exists", "A profile with this name already exists.", parent=self)
            return

        self.result = {
            "name": profile_name,
            "school": self.school_entry.get().strip()
        }
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