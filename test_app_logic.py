import unittest
import sys
import os
import tkinter as tk
from unittest.mock import MagicMock
import datetime

# Ensure the application's root directory is in the Python path
# to allow for direct imports of your modules.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_encryption import encrypt_data, decrypt_data
from other import PasswordManager
from seatingchartmain import name_similarity_ratio, SeatingChartApp, levenshtein_distance


class TestDataEncryption(unittest.TestCase):
    """Tests for the data encryption and decryption functions."""

    def test_encrypt_decrypt_cycle(self):
        """Test that encrypting and then decrypting data returns the original data."""
        original_string = "This is a secret message for testing."
        encrypted = encrypt_data(original_string)
        decrypted = decrypt_data(encrypted)
        self.assertEqual(original_string, decrypted)

    def test_encryption_is_not_deterministic(self):
        """Test that encrypting the same string twice yields different ciphertexts."""
        original_string = "Another test string."
        encrypted1 = encrypt_data(original_string)
        encrypted2 = encrypt_data(original_string)
        self.assertNotEqual(encrypted1, encrypted2)

    def test_empty_string(self):
        """Test encrypting and decrypting an empty string."""
        original_string = ""
        encrypted = encrypt_data(original_string)
        decrypted = decrypt_data(encrypted)
        self.assertEqual(original_string, decrypted)

    def test_non_ascii_characters(self):
        """Test with non-ASCII characters to ensure UTF-8 handling is correct."""
        original_string = "你好, ప్రపంచం, שלום עולם"
        encrypted = encrypt_data(original_string)
        decrypted = decrypt_data(encrypted)
        self.assertEqual(original_string, decrypted)


class TestPasswordManager(unittest.TestCase):
    """Tests for the PasswordManager class."""

    def setUp(self):
        """Set up a mock app_settings dictionary for each test."""
        self.app_settings = {}
        self.password_manager = PasswordManager(self.app_settings)

    def test_initial_state(self):
        """Test the initial state of the PasswordManager."""
        self.assertFalse(self.password_manager.is_password_set())
        self.assertIsNone(self.app_settings.get("app_password_hash"))

    def test_set_and_check_password(self):
        """Test setting a password and checking it."""
        password = "my_secret_password"
        self.assertTrue(self.password_manager.set_password(password))
        self.assertTrue(self.password_manager.is_password_set())
        self.assertIsNotNone(self.app_settings.get("app_password_hash"))

        # Check correct password
        self.assertTrue(self.password_manager.check_password(password))

        # Check incorrect password
        self.assertFalse(self.password_manager.check_password("wrong_password"))

    def test_remove_password(self):
        """Test removing a password by setting it to None."""
        password = "password_to_remove"
        self.password_manager.set_password(password)
        self.assertTrue(self.password_manager.is_password_set())

        self.password_manager.set_password(None)
        self.assertFalse(self.password_manager.is_password_set())
        self.assertIsNone(self.app_settings.get("app_password_hash"))

        # Check that check_password now returns True for anything (since no password is set)
        self.assertTrue(self.password_manager.check_password("any_string"))
        self.assertTrue(self.password_manager.check_password(""))

    def test_recovery_password(self):
        """Test the master recovery password functionality."""
        recovery_password = "Recovery1Master2Password!1Jaffe3"
        wrong_recovery = "wrong_recovery"
        self.assertTrue(self.password_manager.check_recovery_password(recovery_password))
        self.assertFalse(self.password_manager.check_recovery_password(wrong_recovery))


class TestUtilityFunctions(unittest.TestCase):
    """Tests for standalone utility functions."""

    def test_name_similarity_ratio(self):
        """Test the name similarity calculation."""
        # Identical strings (case-insensitive)
        self.assertEqual(name_similarity_ratio("John Smith", "John Smith"), 1.0)
        self.assertEqual(name_similarity_ratio("john smith", "JOHN SMITH"), 1.0)

        # Completely different
        self.assertLess(name_similarity_ratio("John Smith", "Jane Doe"), 0.5)

        # Minor differences
        self.assertGreater(name_similarity_ratio("Jon Smith", "John Smith"), 0.8)
        self.assertGreater(name_similarity_ratio("John Smyth", "John Smith"), 0.8)

        # Swapped names
        self.assertLess(name_similarity_ratio("Smith John", "John Smith"), 0.6)

        # Empty strings
        self.assertEqual(name_similarity_ratio("", ""), 1.0)
        self.assertEqual(name_similarity_ratio("test", ""), 0.0)


class TestSeatingChartApp(unittest.TestCase):
    def setUp(self):
        # Create a mock Tk root window
        self.root = tk.Tk()
        # Mock the SeatingChartApp
        self.app = SeatingChartApp(self.root)

    def tearDown(self):
        self.app.file_lock_manager.release_lock()
        self.root.destroy()

    def test_get_default_settings(self):
        settings = self.app._get_default_settings()
        self.assertIsInstance(settings, dict)
        self.assertIn("show_recent_incidents_on_boxes", settings)
        self.assertEqual(settings["show_recent_incidents_on_boxes"], True)

    def test_get_new_student_id(self):
        id1, next_id1 = self.app.get_new_student_id()
        self.assertEqual(id1, "student_1")
        self.assertEqual(next_id1, 2)
        self.app.next_student_id_num = next_id1
        id2, next_id2 = self.app.get_new_student_id()
        self.assertEqual(id2, "student_2")
        self.assertEqual(next_id2, 3)

    def test_get_new_furniture_id(self):
        id1, next_id1 = self.app.get_new_furniture_id()
        self.assertEqual(id1, "furniture_1")
        self.assertEqual(next_id1, 2)
        self.app.next_furniture_id_num = next_id1
        id2, next_id2 = self.app.get_new_furniture_id()
        self.assertEqual(id2, "furniture_2")
        self.assertEqual(next_id2, 3)

    def test_get_new_group_id(self):
        id1, next_id1 = self.app.get_new_group_id()
        self.assertEqual(id1, "group_1")
        self.assertEqual(next_id1, 2)
        self.app.next_group_id_num = next_id1
        id2, next_id2 = self.app.get_new_group_id()
        self.assertEqual(id2, "group_2")
        self.assertEqual(next_id2, 3)

    def test_get_new_quiz_template_id(self):
        id1, next_id1 = self.app.get_new_quiz_template_id()
        self.assertEqual(id1, "quiztemplate_1")
        self.assertEqual(next_id1, 2)
        self.app.next_quiz_template_id_num = next_id1
        id2, next_id2 = self.app.get_new_quiz_template_id()
        self.assertEqual(id2, "quiztemplate_2")
        self.assertEqual(next_id2, 3)

    def test_get_new_homework_template_id(self):
        id1, next_id1 = self.app.get_new_homework_template_id()
        self.assertEqual(id1, "hwtemplate_1")
        self.assertEqual(next_id1, 2)
        self.app.next_homework_template_id_num = next_id1
        id2, next_id2 = self.app.get_new_homework_template_id()
        self.assertEqual(id2, "hwtemplate_2")
        self.assertEqual(next_id2, 3)

    def test_get_new_custom_homework_type_id(self):
        id1, next_id1 = self.app.get_new_custom_homework_type_id()
        self.assertEqual(id1, "hwtype_1")
        self.assertEqual(next_id1, 2)
        self.app.settings["next_custom_homework_type_id_num"] = next_id1
        id2, next_id2 = self.app.get_new_custom_homework_type_id()
        self.assertEqual(id2, "hwtype_2")
        self.assertEqual(next_id2, 3)

    def test_calculate_quiz_score_percentage(self):
        log_entry = {
            "type": "quiz",
            "marks_data": {"mark_correct": 8, "mark_incorrect": 2},
            "num_questions": 10,
        }
        score = self.app._calculate_quiz_score_percentage(log_entry)
        self.assertEqual(score, 80.0)

        log_entry = {
            "type": "quiz",
            "score_details": {"correct": 5, "total_asked": 10},
        }
        score = self.app._calculate_quiz_score_percentage(log_entry)
        self.assertEqual(score, 50.0)

    def test_generate_attendance_data(self):
        self.app.students = {
            "student_1": {"id": "student_1", "full_name": "John Doe"},
            "student_2": {"id": "student_2", "full_name": "Jane Doe"},
        }
        self.app.behavior_log = [
            {"student_id": "student_1", "timestamp": "2023-10-26T10:00:00"},
            {"student_id": "student_2", "timestamp": "2023-10-27T10:00:00"},
        ]
        start_date = datetime.date(2023, 10, 26)
        end_date = datetime.date(2023, 10, 27)
        student_ids = ["student_1", "student_2"]
        attendance = self.app.generate_attendance_data(start_date, end_date, student_ids)
        self.assertEqual(attendance[start_date]["student_1"], "P")
        self.assertEqual(attendance[start_date]["student_2"], "A")
        self.assertEqual(attendance[end_date]["student_1"], "A")
        self.assertEqual(attendance[end_date]["student_2"], "P")

    def test_levenshtein_distance(self):
        self.assertEqual(levenshtein_distance("kitten", "sitting"), 3)
        self.assertEqual(levenshtein_distance("saturday", "sunday"), 3)
        self.assertEqual(levenshtein_distance("", "test"), 4)
        self.assertEqual(levenshtein_distance("test", ""), 4)
        self.assertEqual(levenshtein_distance("test", "test"), 0)

if __name__ == '__main__':
    unittest.main()