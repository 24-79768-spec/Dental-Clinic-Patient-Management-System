import sqlite3
import datetime

TREATMENT_OPTIONS = [
    "Cleaning/Prophylaxis",
    "Dental Filling (Composite)",
    "Root Canal Therapy",
    "Tooth Extraction",
    "Invisalign Consultation"
]

class DatabaseManager:
    """Handles all database operations (CRUD and Reporting)."""

    def __init__(self, db_name="dental_clinic.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON")
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients
            (
                patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                dob TEXT,
                phone TEXT UNIQUE NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS treatments
            (
                treatment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER,
                date TEXT NOT NULL,
                description TEXT NOT NULL,
                cost REAL,
                FOREIGN KEY (patient_id) REFERENCES patients (patient_id) ON DELETE CASCADE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS deleted_patients
            (
                patient_id INTEGER,
                name TEXT NOT NULL,
                dob TEXT,
                phone TEXT NOT NULL,
                deleted_at TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    # --- User verification
    def verify_user(self, username, password):
        self.cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        )
        return self.cursor.fetchone() is not None

    # --- Patient CRUD
    def insert_patient(self, name, dob, phone):
        try:
            self.cursor.execute(
                "INSERT INTO patients (name, dob, phone) VALUES (?, ?, ?)",
                (name, dob, phone)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception:
            return False

    def search_patients(self, search_query):
        query = f"""
            SELECT patient_id, name, dob, phone FROM patients 
            WHERE patient_id LIKE '%{search_query}%'
            OR name LIKE '%{search_query}%'
            OR phone LIKE '%{search_query}%'
            OR dob LIKE '%{search_query}%'
            ORDER BY patient_id DESC
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def fetch_all_patients(self):
        self.cursor.execute("SELECT patient_id, name, dob, phone FROM patients ORDER BY name ASC")
        return self.cursor.fetchall()

    def update_patient(self, patient_id, name, dob, phone):
        try:
            self.cursor.execute(
                "UPDATE patients SET name = ?, dob = ?, phone = ? WHERE patient_id = ?",
                (name, dob, phone, patient_id)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception:
            return False

    def delete_patient(self, patient_id):
        try:
            self.cursor.execute("SELECT patient_id, name, dob, phone FROM patients WHERE patient_id = ?", (patient_id,))
            patient = self.cursor.fetchone()
            if not patient:
                return False
            deleted_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute(
                "INSERT INTO deleted_patients (patient_id, name, dob, phone, deleted_at) VALUES (?, ?, ?, ?, ?)",
                (patient[0], patient[1], patient[2], patient[3], deleted_at)
            )
            self.cursor.execute("DELETE FROM patients WHERE patient_id = ?", (patient_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print("Error deleting patient:", e)
            return False

    # --- Treatments
    def insert_treatment(self, patient_id, date, description, cost):
        try:
            self.cursor.execute(
                "INSERT INTO treatments (patient_id, date, description, cost) VALUES (?, ?, ?, ?)",
                (patient_id, date, description, cost)
            )
            self.conn.commit()
            return True
        except Exception:
            return False

    def fetch_patient_history(self, patient_id):
        self.cursor.execute("SELECT date, description, cost FROM treatments WHERE patient_id = ?", (patient_id,))
        return self.cursor.fetchall()

    # --- Reporting
    def fetch_available_months(self):
        self.cursor.execute("SELECT DISTINCT strftime('%Y-%m', date) FROM treatments ORDER BY date DESC")
        return [row[0] for row in self.cursor.fetchall()]

    def fetch_treatment_counts_by_month(self, year_month):
        self.cursor.execute(
            "SELECT description, COUNT(*) FROM treatments WHERE strftime('%Y-%m', date) = ? GROUP BY description",
            (year_month,)
        )
        return self.cursor.fetchall()

    def fetch_treatment_revenue_by_month(self, year_month):
        self.cursor.execute(
            "SELECT description, SUM(cost) FROM treatments WHERE strftime('%Y-%m', date) = ? GROUP BY description",
            (year_month,)
        )
        return self.cursor.fetchall()

    def fetch_treatment_revenue_distribution(self):
        self.cursor.execute("SELECT description, SUM(cost) FROM treatments GROUP BY description")
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
