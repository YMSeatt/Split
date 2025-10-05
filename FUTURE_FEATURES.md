# Future Features Roadmap

This document outlines features that have been discussed and are planned for future versions of the application.

## 1. Advanced Per-Setting Sharing UI

**Goal:** Provide a user interface within the settings dialog to allow users to individually manage whether each setting is "global" (shared across all profiles) or "per-profile".

**Implementation Details:**

*   **UI Mockup:** In the `SettingsDialog`, next to each setting control (e.g., a font selector, a color picker), there should be a small button or icon (like a globe or a user icon).
*   **Toggle Logic:** Clicking this icon would toggle the setting's mode between "global" and "per-profile".
    *   When a setting is "global", its value is read from and saved to `global_settings.json`. The UI control for this setting might be disabled and show a small label like "(managed globally)".
    *   When a setting is "per-profile", its value is read from and saved to the active profile's `settings.json` file, and the UI control is enabled.
*   **Configuration Storage:** The state of each setting (i.e., whether it's "global" or "per-profile") will be stored in the `settings_sharing_config.json` file. The UI will read this file to determine the initial state of the toggle icons for each setting.

## 2. Scheduled, Time-Based Profile Loading

**Goal:** Allow users to define a schedule that automatically loads a specific profile at certain times of the day on certain days of the week.

**Implementation Details:**

*   **UI for Scheduling:** A new section in the settings dialog will be needed to manage the schedule. This would be a list-based editor where a user can add, edit, or remove schedule entries.
    *   Each entry would need:
        *   A profile selector (dropdown).
        *   A start time picker.
        *   An end time picker.
        *   A way to select the days of the week (e.g., a set of checkboxes for Mon, Tue, Wed, etc.).
*   **Schedule Storage:** The schedule data should be stored in a new JSON file in the main application data directory (e.g., `schedule.json`).
*   **Startup Logic:** At application startup, before the profile selection dialog is shown, the application will:
    1.  Check if a schedule exists.
    2.  Check the current time and day of the week.
    3.  If the current time falls within a scheduled slot, it will automatically load the corresponding profile, bypassing the profile selection dialog.
    4.  If no scheduled profile is active, the normal profile selection logic will proceed.
*   **In-App Updates:** A background timer could periodically check the schedule. If the application is running when a new profile's scheduled time begins, it could prompt the user: "It's time for the 'Period 2' profile. Would you like to switch now?"