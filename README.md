# Classroom Behavior Tracker

Classroom Behavior Tracker is a desktop application designed to help educators manage their classroom environment effectively. It provides a visual seating chart and tools to log student behaviors, quiz performance, and homework completion.

## Key Features

*   **Visual Seating Chart:** Create and arrange students and furniture items on a canvas representing your classroom layout. Drag-and-drop interface for easy management.
*   **Comprehensive Logging:**
    *   **Behavior Logging:** Quickly log predefined or custom behaviors for individual students (e.g., "Talking," "Off Task," "Great Participation").
    *   **Quiz Logging:** Record quiz scores with detailed mark breakdowns (e.g., correct, incorrect, partial credit, bonus). Supports live quiz sessions for real-time marking.
    *   **Homework Logging:** Track homework completion status and scores. Features include:
        *   Manual logging with simplified (type/status) or detailed (with marks) views.
        *   Live homework sessions with "Yes/No" (for quick checks of multiple assignments) or "Select" (for predefined statuses like "Done," "Signed") modes.
*   **Customization:**
    *   Define custom behaviors, quiz mark types, homework types, and homework statuses.
    *   Create reusable templates for quizzes and homework assignments.
    *   Apply conditional formatting to student boxes based on group membership or behavior/quiz data.
    *   Customize student box appearance (colors, fonts, size).
*   **Data Management:**
    *   Export logs and student information to Excel (.xlsx, .xlsm) and CSV formats for reporting and analysis.
    *   Import student rosters from Excel files.
    *   Secure your application data with password protection.
    *   Backup all application data to a ZIP file and restore from backups.
*   **User Experience:**
    *   Undo/Redo functionality for most actions.
    *   Panning and zooming capabilities on the seating chart.
    *   Context menus for quick access to actions.
    *   Light and Dark theme options, with customizable canvas color.

## How to Run

1.  Ensure you have Python installed (version 3.x recommended).
2.  The application uses the Tkinter library, which is usually included with Python.
3.  Additional dependencies might include `Pillow` (for image handling) and `portalocker` (for single instance checking) and `pyscreeze`. These can typically be installed via pip:
    ```bash
    pip install Pillow portalocker pyscreeze openpyxl darkdetect sv-ttk
    ```
4.  Navigate to the project directory and run:
    ```bash
    python __main__.py
    ```
    (Note: On some systems, you might need to use `python3` instead of `python`).

## Data Storage

*   Application data (students, furniture, logs, settings, templates) is stored locally in JSON files within an application-specific directory.
*   You can access this directory via `File > Open Data Folder` in the application.
*   It is recommended to regularly use the `File > Backup All Application Data (.zip)...` feature.

## Logging Modes

The application offers three primary logging modes accessible from the main toolbar:

*   **Behavior Mode:** For general behavior tracking. Click a student to log a behavior.
*   **Quiz Mode:** For logging quiz scores or running live quiz sessions.
*   **Homework Mode:** For logging homework completion, marks, or running live homework check sessions.

The new comprehensive Homework Tracking system allows for flexible input, from quick "Yes/No" checks during a live session to detailed mark entry for individual assignments.

---

This README provides a general overview. For more detailed information, please refer to the in-application Help section.
