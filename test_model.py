# test_model.py
import sys
import os
import unittest
import datetime

# Ensure current folder is in Python path (needed only if files are in different folders)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from model import DatabaseManager, TREATMENT_OPTIONS

class TestDatabaseManager(unittest.TestCase):

    def setUp(self):
        # Use in-memory database for testing
        self.db = DatabaseManager(":memory:")

        # Create a dummy user for login tests
        self.db.cursor.execute("CREATE TABLE users (username TEXT, password TEXT)")
        self.db.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "1234"))
        self.db.conn.commit()

    def tearDown(self):
        self.db.close()

    # --- User verification tests ---
    def test_verify_user_success(self):
        self.assertTrue(self.db.verify_user("admin", "1234"))

    def test_verify_user_failure(self):
        self.assertFalse(self.db.verify_user("admin", "wrongpassword"))
        self.assertFalse(self.db.verify_user("nonexistent", "1234"))

    # --- Patient CRUD tests ---
    def test_insert_and_fetch_patient(self):
        result = self.db.insert_patient("John Doe", "1990-01-01", "1234567890")
        self.assertTrue(result)
        patients = self.db.fetch_all_patients()
        self.assertEqual(len(patients), 1)
        self.assertEqual(patients[0][1], "John Doe")

    def test_insert_duplicate_phone(self):
        self.db.insert_patient("John Doe", "1990-01-01", "1234567890")
        result = self.db.insert_patient("Jane Doe", "1992-02-02", "1234567890")
        self.assertFalse(result)

    def test_update_patient(self):
        self.db.insert_patient("John Doe", "1990-01-01", "1234567890")
        patient_id = self.db.fetch_all_patients()[0][0]
        result = self.db.update_patient(patient_id, "John Smith", "1991-02-02", "0987654321")
        self.assertTrue(result)
        updated = self.db.fetch_all_patients()[0]
        self.assertEqual(updated[1], "John Smith")

    def test_delete_patient(self):
        self.db.insert_patient("John Doe", "1990-01-01", "1234567890")
        patient_id = self.db.fetch_all_patients()[0][0]
        result = self.db.delete_patient(patient_id)
        self.assertTrue(result)
        self.assertEqual(len(self.db.fetch_all_patients()), 0)

    # --- Treatment tests ---
    def test_insert_and_fetch_treatment(self):
        self.db.insert_patient("John Doe", "1990-01-01", "1234567890")
        patient_id = self.db.fetch_all_patients()[0][0]
        today = datetime.date.today().strftime("%Y-%m-%d")
        result = self.db.insert_treatment(patient_id, today, "Cleaning/Prophylaxis", 50.0)
        self.assertTrue(result)
        history = self.db.fetch_patient_history(patient_id)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0][1], "Cleaning/Prophylaxis")

    # --- Reporting tests ---
    def test_fetch_available_months(self):
        self.db.insert_patient("John Doe", "1990-01-01", "1234567890")
        patient_id = self.db.fetch_all_patients()[0][0]
        self.db.insert_treatment(patient_id, "2025-12-01", "Cleaning/Prophylaxis", 50)
        months = self.db.fetch_available_months()
        self.assertIn("2025-12", months)

    def test_fetch_treatment_counts_by_month(self):
        self.db.insert_patient("John Doe", "1990-01-01", "1234567890")
        patient_id = self.db.fetch_all_patients()[0][0]
        self.db.insert_treatment(patient_id, "2025-12-01", "Cleaning/Prophylaxis", 50)
        counts = self.db.fetch_treatment_counts_by_month("2025-12")
        self.assertEqual(counts[0][0], "Cleaning/Prophylaxis")
        self.assertEqual(counts[0][1], 1)

if __name__ == "__main__":
    unittest.main()
