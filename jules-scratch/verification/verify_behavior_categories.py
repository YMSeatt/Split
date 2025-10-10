import tkinter as tk
import sys
import os
sys.path.append(os.getcwd())
from seatingchartmain import SeatingChartApp
import pyautogui
import time
import signal

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException

def verify_behavior_categories():
    print("Starting verification script...")
    # Set a timeout for the script
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(30) # 30 seconds

    try:
        # The application should be running in the background.
        # We need to find the root window of the running application.
        # This is not straightforward, so we will assume that the application
        # has been started and we can just open the dialog.
        # This is a limitation of testing Tkinter applications this way.

        # We'll create a dummy root to initialize the app object, but not run its mainloop
        root = tk.Tk()
        root.withdraw()

        app = SeatingChartApp(root)

        # Give the app a moment to get its bearings
        time.sleep(2)

        print("Opening settings dialog...")
        app.open_settings_dialog()

        # Give the settings dialog time to appear
        print("Waiting for settings dialog to appear...")
        time.sleep(5)

        # Take a screenshot
        print("Taking screenshot...")
        screenshot = pyautogui.screenshot()
        if not os.path.exists("jules-scratch/verification"):
            os.makedirs("jules-scratch/verification")
        screenshot.save("jules-scratch/verification/verification.png")
        print("Screenshot saved.")

    except TimeoutException:
        print("Script timed out.")
    finally:
        # This part is tricky because we don't want to kill the main app process
        # that is running in the background. We will just exit this script.
        print("Verification script finished.")


if __name__ == "__main__":
    verify_behavior_categories()