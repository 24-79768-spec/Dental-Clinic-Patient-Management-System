import sqlite3

class DatabaseManager:
    """Handles all database operations (CRUD and Reporting)."""

    def __init__(self, db_name="dental_clinic.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        # Enable foreign key support for cascade deletes
        self.cursor.execute("PRAGMA foreign_keys = ON")
        self.create_tables()

    def create_tables(self):
        """Creates the necessary tables if they don't exist."""
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
                                FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
                            )
                            ''')
        self.conn.commit()

    # --- Patient CRUD Operations ---
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
        """Searches patients across ID, Name, DOB, and Phone (SAFE from SQL Injection)."""
        # Ihanda ang variable para sa LIKE clause, na may kasamang wildcards
        like_query = f"%{search_query}%"

        # Gamitin ang ? placeholder para sa lahat ng user input
        query = """
                SELECT patient_id, name, dob, phone \
                FROM patients
                WHERE CAST(patient_id AS TEXT) LIKE ?
                   OR name LIKE ?
                   OR phone LIKE ?
                   OR dob LIKE ?
                ORDER BY patient_id DESC \
                """
        # I-execute at ipasa ang like_query nang apat na beses bilang parameter
        self.cursor.execute(query, (like_query, like_query, like_query, like_query))
        return self.cursor.fetchall()

    def fetch_all_patients(self):
        """Fetches all patients, ordered by Name for better usability in lists."""
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
            self.cursor.execute("DELETE FROM patients WHERE patient_id = ?", (patient_id,))
            self.conn.commit()
            return True
        except Exception:
            return False

    # --- Treatment Operations ---
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

    # --- Dashboard/Reporting Methods ---
    def fetch_available_months(self):
        """Fetches unique YYYY-MM strings for filtering."""
        self.cursor.execute("SELECT DISTINCT strftime('%Y-%m', date) FROM treatments ORDER BY date DESC")
        return [row[0] for row in self.cursor.fetchall()]

    def fetch_treatment_counts_by_month(self, year_month):
        """Fetches treatment counts for a specific month (YYYY-MM)."""
        self.cursor.execute(
            "SELECT description, COUNT(*) FROM treatments WHERE strftime('%Y-%m', date) = ? GROUP BY description",
            (year_month,)
        )
        return self.cursor.fetchall()

    def fetch_treatment_revenue_by_month(self, year_month):
        """Fetches total revenue (SUM of cost) for each treatment type for a specific month (YYYY-MM)."""
        self.cursor.execute(
            "SELECT description, SUM(cost) FROM treatments WHERE strftime('%Y-%m', date) = ? GROUP BY description",
            (year_month,)
        )
        return self.cursor.fetchall()

    def validate_login(self, username, password):
        """Searches patients across ID, Name, DOB, and Phone (SAFE from SQL Injection)."""

        # Gamitin ang ? placeholder para sa lahat ng user input
        query = "SELECT password FROM users WHERE username = ?"
        # I-execute at ipasa ang like_query nang apat na beses bilang parameter
        self.cursor.execute(query, (username,))
        results =  self.cursor.fetchall()

        if results[0] == (password,):
            return True
        else:
            return False

    def close(self):
        self.conn.close()