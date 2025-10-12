import unittest
import tkinter as tk
from seatingchartmain import SeatingChartApp, DEFAULT_BEHAVIORS_LIST

class TestBehaviorLogic(unittest.TestCase):
    def setUp(self):
        """Set up a mock application environment for each test."""
        self.root = tk.Tk()
        # We can "hide" the main window during tests
        self.root.withdraw()
        self.app = SeatingChartApp(self.root)

    def tearDown(self):
        """Clean up after each test."""
        self.root.destroy()

    def test_update_all_behaviors_with_overrides(self):
        """
        Tests that the update_all_behaviors function correctly applies
        overrides to default behaviors while preserving the original categories
        of non-overridden behaviors.
        """
        # 1. Setup: Define an override for a default behavior
        # We will change "Talking" from "Bad" to "Good"
        self.app.settings["default_behavior_overrides"] = {
            "Talking": "Good"
        }

        # 2. Action: Call the function to update behaviors
        self.app.update_all_behaviors()

        # 3. Assertions
        all_behaviors_map = {b['name']: b for b in self.app.all_behaviors}

        # Check that the override was applied correctly
        self.assertIn("Talking", all_behaviors_map)
        self.assertEqual(all_behaviors_map["Talking"]["category"], "Good")

        # Check that a non-overridden default behavior retains its original category
        # "Great Participation" is "Good" in the default list.
        self.assertIn("Great Participation", all_behaviors_map)
        self.assertEqual(all_behaviors_map["Great Participation"]["category"], "Good")

        # Check that another non-overridden default behavior retains its original category
        # "Off Task" is "Bad" in the default list.
        self.assertIn("Off Task", all_behaviors_map)
        self.assertEqual(all_behaviors_map["Off Task"]["category"], "Bad")

        # Check a neutral one
        self.assertIn("Complimented", all_behaviors_map)
        self.assertEqual(all_behaviors_map["Complimented"]["category"], "Neutral")

if __name__ == '__main__':
    unittest.main()