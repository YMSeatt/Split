import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from datetime import date

# A placeholder for tkcalendar if it's not installed.
# For full functionality of ExportFilterDialog, you would need to install it:
# pip install tkcalendar

from tkcalendar import DateEntry


# --- Main Requested Dialog: Undo History ---

class UndoHistoryDialog(tk.Toplevel):
    """
    A dialog that displays the undo history, allowing the user to select
    a point to revert to and redo, effectively branching the history.
    """
    def __init__(self, parent, app):
        """
        Initializes the Undo History dialog.
        Args:
            parent: The parent window (the main application root).
            app: The instance of the main SeatingChartApp.
        """
        super().__init__(parent)
        self.transient(parent)
        self.title("Undo History")
        self.app = app
        self.result = None

        self.geometry("550x450")
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.grab_set()

        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        info_label = ttk.Label(main_frame, text="Select an action to return to. This will discard all subsequent changes.", wraplength=500)
        info_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)

        self.listbox = tk.Listbox(list_frame, selectmode=tk.SINGLE, font=("TkDefaultFont", 10))
        self.listbox.grid(row=0, column=0, sticky="nsew")
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        self.listbox.bind('<Double-1>', lambda e: self.on_redo())


        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.populate_history()

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, sticky="e", pady=(10, 0))

        self.redo_button = ttk.Button(button_frame, text="Go to This Action", command=self.on_redo, state=tk.DISABLED)
        self.redo_button.pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.LEFT)

        # Center the dialog on the parent
        self.update_idletasks()
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_w = parent.winfo_width()
        parent_h = parent.winfo_height()
        dialog_w = self.winfo_width()
        dialog_h = self.winfo_height()
        self.geometry(f"+{parent_x + (parent_w - dialog_w) // 2}+{parent_y + (parent_h - dialog_h) // 2}")


        self.wait_window(self)

    def populate_history(self):
        """
        Clears and fills the listbox with descriptions of commands
        from the application's undo stack.
        """
        self.listbox.delete(0, tk.END)
        # The undo_stack is in chronological order. We reverse it for display
        # so the most recent action appears at the top of the list.
        if not self.app.undo_stack:
            self.listbox.insert(tk.END, " No actions in history.")
            self.listbox.config(state=tk.DISABLED)
            return

        for i, command in enumerate(reversed(self.app.undo_stack)):
            try:
                # NOTE: This assumes your Command objects have a `get_description()` method.
                description = command.get_description()
                # Display with a number, like "15: Moved 1 item(s)"
                self.listbox.insert(tk.END, f" {len(self.app.undo_stack) - i}: {description}")
            except Exception as e:
                # Fallback if get_description fails for any reason
                self.listbox.insert(tk.END, f" {len(self.app.undo_stack) - i}: {type(command).__name__}")
                print(f"Could not get description for command {type(command).__name__}: {e}")

    def on_select(self, event=None):
        """Enables the 'Redo' button when an item is selected in the listbox."""
        if self.listbox.curselection():
            self.redo_button.config(state=tk.NORMAL)
        else:
            self.redo_button.config(state=tk.DISABLED)

    def on_redo(self):
        """
        Handles the 'Go to This Action' button click.
        It calculates the correct index and calls the app's selective redo method.
        """
        selection_indices = self.listbox.curselection()
        if not selection_indices:
            return

        # The listbox is visually reversed, so we must convert the selected
        # listbox index back to the correct index for the `undo_stack`.
        selected_listbox_index = selection_indices[0]
        target_command_index = (len(self.app.undo_stack) - 1) - selected_listbox_index

        if messagebox.askyesno("Confirm Action",
                               "This will revert the application to the selected point in history, discarding all changes made after it. This cannot be undone.\n\nAre you sure you want to proceed?",
                               parent=self, icon='warning'):
            # Call the main app's logic handler
            self.app.selective_redo_action(target_command_index)
            self.destroy()

    def cancel(self):
        """Closes the dialog."""
        self.destroy()



