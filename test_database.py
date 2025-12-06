import unittest
import sqlite3
# Import your DatabaseManager class from the database.py file
from database import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    """Unit tests for the DatabaseManager class, using an in-memory database."""

    def setUp(self):
        """
        Sets up an in-memory database instance for each test run.
        """
        # Use ':memory:' to create a temporary, in-memory database
        self.db = DatabaseManager(db_name=':memory:')

        # Test Data for Patient
        self.patient_data = {
            'name': 'Juan Dela Cruz',
            'dob': '1990-01-01',
            'phone': '09171234567'
        }
        # Insert initial patient and store their ID
        self.patient_id = self._insert_test_patient()

        # Test Data for Treatment
        self.treatment_data = {
            'patient_id': self.patient_id,
            'date': '2023-10-25',
            'description': 'Root Canal',
            'cost': 8500.00
        }
        # Insert initial treatment
        self._insert_test_treatment(self.treatment_data)

    def tearDown(self):
        """
        Closes the database connection after each test.
        (For an in-memory database, this deletes the database content).
        """
        self.db.close()

    # --- Helper Methods for Test Setup ---
    def _insert_test_patient(self):
        """Quickly inserts a patient and returns their patient_id."""
        self.db.insert_patient(**self.patient_data)
        # Retrieve the ID using the phone number, as it is unique.
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT patient_id FROM patients WHERE phone = ?", (self.patient_data['phone'],))
        return cursor.fetchone()[0]

    def _insert_test_treatment(self, data):
        """Quickly inserts a treatment."""
        self.db.insert_treatment(**data)

    # =======================================================
    #                   TEST METHODS
    # =======================================================

    ## --- Structure and Basic Setup Tests ---

    def test_a_create_tables(self):
        """Test if the necessary tables were created."""
        cursor = self.db.conn.cursor()
        # Check for 'patients' table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='patients'")
        self.assertIsNotNone(cursor.fetchone(), "The 'patients' table was not created.")
        # Check for 'treatments' table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='treatments'")
        self.assertIsNotNone(cursor.fetchone(), "The 'treatments' table was not created.")

    ## --- Patient CRUD Tests ---

    def test_b_insert_patient_success(self):
        """Test successful patient insertion."""
        result = self.db.insert_patient('Maria Santos', '1995-05-15', '09209876543')
        self.assertTrue(result, "Patient insertion should be successful.")

        # Verify insertion
        patients = self.db.search_patients('Maria Santos')
        self.assertEqual(len(patients), 1)

    def test_c_insert_patient_duplicate_phone(self):
        """Test inserting a patient with a duplicate phone number (IntegrityError)."""
        # Try to insert the same phone number again
        result = self.db.insert_patient(**self.patient_data)
        self.assertFalse(result, "Insertion should fail due to duplicate phone number.")

    def test_d_fetch_all_patients(self):
        """Test fetching all patients and checking the name-based sorting."""
        # Insert a second patient for sorting check
        self.db.insert_patient('Anna Gomez', '2000-03-20', '09181112222')
        patients = self.db.fetch_all_patients()
        self.assertEqual(len(patients), 2)
        # Should be sorted by name ASC ('Anna Gomez' before 'Juan Dela Cruz')
        self.assertEqual(patients[0][1], 'Anna Gomez')
        self.assertEqual(patients[1][1], 'Juan Dela Cruz')

    def test_e_search_patients(self):
        """Test searching patients across ID, Name, Phone, and DOB."""
        # Patient 2
        self.db.insert_patient('Anna Gomez', '2000-03-20', '09181112222')

        # Search by Name
        results_name = self.db.search_patients('Juan Dela Cruz')
        self.assertGreater(len(results_name), 0)
        self.assertEqual(results_name[0][1], 'Juan Dela Cruz')

        # Search by Phone
        results_phone = self.db.search_patients('09171234567')
        self.assertGreater(len(results_phone), 0)
        self.assertEqual(results_phone[0][3], '09171234567')

        # Search by Partial Name
        results_partial = self.db.search_patients('Del')
        self.assertGreater(len(results_partial), 0)

    def test_f_update_patient(self):
        """Test updating patient details."""
        new_name = 'Juan Santos'
        new_phone = '09987654321'
        result = self.db.update_patient(self.patient_id, new_name, '1990-01-01', new_phone)
        self.assertTrue(result)

        # Verify the update
        updated_patient = self.db.search_patients(new_name)[0]
        self.assertEqual(updated_patient[1], new_name)
        self.assertEqual(updated_patient[3], new_phone)

    def test_g_delete_patient_and_cascade(self):
        """Test deleting a patient and the cascading deletion of treatments."""
        # Patient ID already has treatment history from setUp.

        # Delete the patient
        result = self.db.delete_patient(self.patient_id)
        self.assertTrue(result)

        # Verify patient is gone
        self.assertEqual(len(self.db.search_patients(self.patient_data['phone'])), 0)

        # Verify treatments are also deleted (Cascade Delete)
        treatments = self.db.fetch_patient_history(self.patient_id)
        self.assertEqual(len(treatments), 0, "Treatments should be deleted due to CASCADE.")

    ## --- Treatment Tests ---

    def test_h_insert_treatment(self):
        """Test successful treatment insertion."""
        new_treatment = {
            'patient_id': self.patient_id,
            'date': '2023-11-01',
            'description': 'Tooth Extraction',
            'cost': 2000.00
        }
        result = self.db.insert_treatment(**new_treatment)
        self.assertTrue(result, "Treatment insertion should be successful.")

        # Verify insertion
        history = self.db.fetch_patient_history(self.patient_id)
        self.assertEqual(len(history), 2)  # 1 from setup + 1 new insertion

    def test_i_fetch_patient_history(self):
        """Test retrieving a patient's treatment history."""
        history = self.db.fetch_patient_history(self.patient_id)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0][1], 'Root Canal')  # description

    ## --- Reporting/Dashboard Tests ---

    def test_j_fetch_available_months(self):
        """Test retrieving unique months (YYYY-MM) for filtering."""
        # Add a treatment in a different month
        self._insert_test_treatment(
            {'patient_id': self.patient_id, 'date': '2023-09-15', 'description': 'Cleaning', 'cost': 1500.00})

        months = self.db.fetch_available_months()
        # Should be ordered by DESC date
        self.assertListEqual(months, ['2023-10', '2023-09'])

    def test_k_fetch_treatment_counts_by_month(self):
        """Test retrieving treatment counts for a specific month."""
        # Add another 'Root Canal' in the same month
        self._insert_test_treatment(
            {'patient_id': self.patient_id, 'date': '2023-10-26', 'description': 'Root Canal', 'cost': 8000.00})
        # Add a different treatment type in the same month
        self._insert_test_treatment(
            {'patient_id': self.patient_id, 'date': '2023-10-27', 'description': 'Filling', 'cost': 1200.00})

        counts = self.db.fetch_treatment_counts_by_month('2023-10')
        expected_counts = [
            ('Filling', 1),
            ('Root Canal', 2)
        ]
        # Compare sorted lists because SQLite's GROUP BY results order isn't guaranteed
        self.assertListEqual(sorted(counts), sorted(expected_counts))

    def test_l_fetch_treatment_revenue_by_month(self):
        """Test retrieving total revenue per treatment type for a specific month."""
        # Initial treatment: Root Canal, 8500.00 (from setup)
        # Add another 'Root Canal'
        self._insert_test_treatment(
            {'patient_id': self.patient_id, 'date': '2023-10-26', 'description': 'Root Canal', 'cost': 8000.00})
        # Add 'Filling'
        self._insert_test_treatment(
            {'patient_id': self.patient_id, 'date': '2023-10-27', 'description': 'Filling', 'cost': 1200.00})

        revenue = self.db.fetch_treatment_revenue_by_month('2023-10')
        expected_revenue = [
            ('Filling', 1200.0),
            ('Root Canal', 16500.0)  # 8500.00 + 8000.00
        ]
        self.assertListEqual(sorted(revenue), sorted(expected_revenue))


if __name__ == '__main__':
    # Run all tests in this file
    unittest.main()