# PyQt Imports
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLineEdit, QPushButton,
    QLabel, QTableWidget, QTableWidgetItem, QMessageBox,
    QHeaderView, QDateEdit, QComboBox, QFrame,
    QDialog, QStackedWidget
)

# Local Imports
from model import TREATMENT_OPTIONS
from database import DatabaseManager

# --- Login Dialog ---
class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dental Clinic Login")
        self.setFixedSize(700, 550)

        # Modern UI Styling for the whole dialog (BLUE/CYAN THEME)
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #E3F2FD, stop:1 #BBDEFB);
                border: 2px solid #2196F3;
                border-radius: 20px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(30)
        layout.setContentsMargins(40, 40, 40, 40)

        # 1. Clinic Icon/Visual Header
        icon_label = QLabel("🦷")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setFont(QFont("Arial", 60))
        icon_label.setStyleSheet("color: #1976D2; margin-bottom: 0px;")
        layout.addWidget(icon_label)

        # 2. Title
        title = QLabel("ConfiDental Clinic System")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 26, QFont.Bold))
        title.setStyleSheet("color: #0D47A1; margin-bottom: 20px;")
        layout.addWidget(title)

        # 3. Username field
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("  Username")
        self.username_input.setFont(QFont("Arial", 16))
        self.username_input.setMinimumHeight(55)
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #BBDEFB;
                border-radius: 10px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #2196F3;
                background-color: #F8FFFF;
            }
        """)
        layout.addWidget(self.username_input)

        # 4. Password field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("  Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont("Arial", 16))
        self.password_input.setMinimumHeight(55)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #BBDEFB;
                border-radius: 10px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #2196F3;
                background-color: #F8FFFF;
            }
        """)
        layout.addWidget(self.password_input)

        layout.addSpacing(10)

        # 5. Login Button
        login_btn = QPushButton("LOGIN ")
        login_btn.setFont(QFont("Arial", 18, QFont.Bold))
        login_btn.setMinimumHeight(65)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #42A5F5;
                color: white;
                padding: 15px;
                border: none;
                border-radius: 15px;
                letter-spacing: 1px;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            }
            QPushButton:hover {
                background-color: #2196F3;
            }
            QPushButton:pressed {
                background-color: #1976D2;
            }
        """)
        login_btn.clicked.connect(self.accept_login)
        layout.addWidget(login_btn)

        layout.addStretch(1)

    def accept_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        db = DatabaseManager()

        login_okay = db.validate_login(username, password)

        # Simple demo validation
        if login_okay == True:
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password!")


# --- About Dialog ---
class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Confidental Clinic")
        self.setFixedSize(750, 550)
        self.setStyleSheet("QDialog { background-color: #F8FFFF; border: 1px solid #BBDEFB; border-radius: 10px; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # 1. Title
        title = QLabel("Confidental Dental Clinic 🦷")
        title.setFont(QFont("Arial", 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #1976D2;")
        layout.addWidget(title)

        # 2. ABOUT US Content
        about_title = QLabel(" ℹ️ ABOUT US ")
        about_title.setFont(QFont("Arial", 22, QFont.Bold))
        about_title.setStyleSheet("color: #1976D2; margin-top: 10px;")
        layout.addWidget(about_title)

        content = QLabel()
        content.setFont(QFont("Arial", 14))
        content.setStyleSheet(
            "color: #455A64; line-height: 1.5; padding: 10px; background-color: #E3F2FD; border-radius: 5px;")
        content.setText(
            "Mission: We are committed to fostering lifetime dental health by delivering exceptional, patient-centered care and promoting preventive practices in a serene and modern environment.\n\n"
            "Core Values: Innovation, Compassion, Professionalism, Trust, and Accessibility. \n\n"
            "Location: 123 Dental St., Brgy. 456, Taguig City, Manila\n\n"
            "Contact: +63 945-123-4567 | confidental@clinic.ph"
        )
        content.setWordWrap(True)
        layout.addWidget(content)

        layout.addStretch(1)

        # Close Button
        close_btn = QPushButton("Close")
        close_btn.setFont(QFont("Arial", 16, QFont.Bold))
        close_btn.setMinimumHeight(50)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)


# --- Services Dialog ---
class ServicesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Services Offered")
        self.setFixedSize(550, 650)
        self.setStyleSheet("QDialog { background-color: #F8FFFF; border: 1px solid #BBDEFB; border-radius: 10px; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # 1. Title
        title = QLabel(" 📋 Services Offered")
        title.setFont(QFont("Arial", 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #1976D2;")
        layout.addWidget(title)

        # Services List Container
        list_frame = QFrame()
        list_frame.setStyleSheet(
            "QFrame { background-color: white; border: 1px solid #BBDEFB; border-radius: 10px; padding: 20px; }")
        list_layout = QVBoxLayout(list_frame)
        list_layout.setSpacing(15)

        # Populate list from the global TREATMENT_OPTIONS constant
        for service in TREATMENT_OPTIONS:
            service_label = QLabel(f" ✅ {service}")
            service_label.setFont(QFont("Arial", 16))
            service_label.setStyleSheet("color: #388E3C;")
            list_layout.addWidget(service_label)

        list_layout.addStretch(1)
        layout.addWidget(list_frame)

        layout.addStretch(1)

        # Close Button
        close_btn = QPushButton("Close")
        close_btn.setFont(QFont("Arial", 16, QFont.Bold))
        close_btn.setMinimumHeight(50)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)


# --- Home Tab (The simplest tab view) ---
class HomeTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        title = QLabel("WELCOME TO CONFIDENTAL CLINIC! ")
        title.setFont(QFont("Arial", 48, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #1976D2; padding: 100px 0 50px 0; line-height: 1.5;")
        layout.addWidget(title)

        # --- Button Layout ---
        button_container = QHBoxLayout()
        button_container.addStretch(1)

        # 1. ABOUT US Button
        self.about_btn = QPushButton("ℹ️ ABOUT US")
        self.about_btn.setFont(QFont("Arial", 22, QFont.Bold))
        self.about_btn.setFixedSize(400, 75)
        self.about_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFB300;
                color: white;
                border: none;
                border-radius: 15px;
                box-shadow: 3px 3px 6px rgba(0, 0, 0, 0.3);
            }
            QPushButton:hover {
                background-color: #FFA000;
            }
        """)
        self.about_btn.clicked.connect(self.show_about)
        button_container.addWidget(self.about_btn)

        button_container.addSpacing(20)

        # 2. SERVICES OFFERED Button
        self.services_btn = QPushButton("🏥 SERVICES OFFERED")
        self.services_btn.setFont(QFont("Arial", 22, QFont.Bold))
        self.services_btn.setFixedSize(450, 75)
        self.services_btn.setStyleSheet("""
            QPushButton {
                background-color: #00BCD4;
                color: white;
                border: none;
                border-radius: 15px;
                box-shadow: 3px 3px 6px rgba(0, 0, 0, 0.3);
            }
            QPushButton:hover {
                background-color: #00ACC1;
            }
        """)
        self.services_btn.clicked.connect(self.show_services)
        button_container.addWidget(self.services_btn)

        button_container.addStretch(1)

        layout.addLayout(button_container)
        layout.addStretch(2)

    # --- Methods to Show Dialogs (Part of HomeTab's simple controller logic) ---
    def show_about(self):
        dialog = AboutDialog(self)
        dialog.exec_()

    def show_services(self):
        dialog = ServicesDialog(self)
        dialog.exec_()