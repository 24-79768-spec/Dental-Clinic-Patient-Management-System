from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from model import TREATMENT_OPTIONS

# ---- Login Dialog ----
class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dental Clinic Login")
        self.setFixedSize(700, 550)
        self.setStyleSheet("QDialog { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #E3F2FD, stop:1 #BBDEFB); border: 2px solid #2196F3; border-radius: 20px; }")
        layout = QVBoxLayout(self)
        layout.setSpacing(30)
        layout.setContentsMargins(40, 40, 40, 40)
        icon_label = QLabel("🦷")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setFont(QFont("Arial", 60))
        icon_label.setStyleSheet("color: #1976D2; margin-bottom: 0px;")
        layout.addWidget(icon_label)
        title = QLabel("ConfiDental Clinic System")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 26, QFont.Bold))
        title.setStyleSheet("color: #0D47A1; margin-bottom: 20px;")
        layout.addWidget(title)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("  Username")
        self.username_input.setFont(QFont("Arial", 16))
        self.username_input.setMinimumHeight(55)
        self.username_input.setStyleSheet("QLineEdit { padding: 10px; border: 2px solid #BBDEFB; border-radius: 10px; background-color: white; } QLineEdit:focus { border-color: #2196F3; background-color: #F8FFFF; }")
        layout.addWidget(self.username_input)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("  Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont("Arial", 16))
        self.password_input.setMinimumHeight(55)
        self.password_input.setStyleSheet("QLineEdit { padding: 10px; border: 2px solid #BBDEFB; border-radius: 10px; background-color: white; } QLineEdit:focus { border-color: #2196F3; background-color: #F8FFFF; }")
        layout.addWidget(self.password_input)
        layout.addSpacing(10)
        self.login_btn = QPushButton("LOGIN ")
        self.login_btn.setFont(QFont("Arial", 18, QFont.Bold))
        self.login_btn.setMinimumHeight(65)
        self.login_btn.setStyleSheet("QPushButton { background-color: #42A5F5; color: white; padding: 15px; border: none; border-radius: 15px; letter-spacing: 1px; box-shadow: 2px 2px 5px rgba(0,0,0,0.2); } QPushButton:hover { background-color: #2196F3; } QPushButton:pressed { background-color: #1976D2; }")
        layout.addWidget(self.login_btn)
        layout.addStretch(1)

# ---- About Dialog ----
class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Confidental Clinic")
        self.setFixedSize(750, 550)
        self.setStyleSheet("QDialog { background-color: #F8FFFF; border: 1px solid #BBDEFB; border-radius: 10px; }")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        title = QLabel("Confidental Dental Clinic 🦷")
        title.setFont(QFont("Arial", 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #1976D2;")
        layout.addWidget(title)
        about_title = QLabel(" ℹ️ ABOUT US ")
        about_title.setFont(QFont("Arial", 22, QFont.Bold))
        about_title.setStyleSheet("color: #1976D2; margin-top: 10px;")
        layout.addWidget(about_title)
        content = QLabel()
        content.setFont(QFont("Arial", 14))
        content.setStyleSheet("color: #455A64; line-height: 1.5; padding: 10px; background-color: #E3F2FD; border-radius: 5px;")
        content.setText(
            "Mission: We are committed to fostering lifetime dental health by delivering exceptional, patient-centered care and promoting preventive practices in a serene and modern environment.\n\n"
            "Core Values: Innovation, Compassion, Professionalism, Trust, and Accessibility. \n\n"
            "Location: 123 Dental St., Brgy. 456, Taguig City, Manila\n\n"
            "Contact: +63 945-123-4567 | confidental@clinic.ph"
        )
        content.setWordWrap(True)
        layout.addWidget(content)
        layout.addStretch(1)
        self.close_btn = QPushButton("Close")
        self.close_btn.setFont(QFont("Arial", 16, QFont.Bold))
        self.close_btn.setMinimumHeight(50)
        self.close_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; border: none; border-radius: 10px; } QPushButton:hover { background-color: #388E3C; }")
        layout.addWidget(self.close_btn)

# ---- Services Dialog ----
class ServicesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Services Offered")
        self.setFixedSize(550, 650)
        self.setStyleSheet("QDialog { background-color: #F8FFFF; border: 1px solid #BBDEFB; border-radius: 10px; }")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        title = QLabel(" 📋 Services Offered")
        title.setFont(QFont("Arial", 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #1976D2;")
        layout.addWidget(title)
        for service in TREATMENT_OPTIONS:
            lbl = QLabel(f" ✅ {service}")
            lbl.setFont(QFont("Arial", 16))
            lbl.setStyleSheet("color: #388E3C;")
            layout.addWidget(lbl)
        layout.addStretch(1)
        self.close_btn = QPushButton("Close")
        self.close_btn.setFont(QFont("Arial", 16, QFont.Bold))
        self.close_btn.setMinimumHeight(50)
        self.close_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; border: none; border-radius: 10px; } QPushButton:hover { background-color: #388E3C; }")
        layout.addWidget(self.close_btn)


class HomeTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("WELCOME TO CONFIDENTAL CLINIC! ")
        title.setFont(QFont("Arial", 48, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #1976D2; padding: 100px 0 50px 0; line-height: 1.5;")
        layout.addWidget(title)
        button_container = QHBoxLayout()
        button_container.addStretch(1)
        self.about_btn = QPushButton("ℹ️ ABOUT US")
        self.about_btn.setFont(QFont("Arial", 22, QFont.Bold))
        self.about_btn.setFixedSize(400, 75)
        self.about_btn.setStyleSheet("""
            QPushButton { background-color: #FFB300; color: white; border: none; border-radius: 15px; box-shadow: 3px 3px 6px rgba(0,0,0,0.3); }
            QPushButton:hover { background-color: #FFA000; }
        """)
        button_container.addWidget(self.about_btn)
        button_container.addSpacing(20)
        self.services_btn = QPushButton("🏥 SERVICES OFFERED")
        self.services_btn.setFont(QFont("Arial", 22, QFont.Bold))
        self.services_btn.setFixedSize(450, 75)
        self.services_btn.setStyleSheet("""
            QPushButton { background-color: #00BCD4; color: white; border: none; border-radius: 15px; box-shadow: 3px 3px 6px rgba(0,0,0,0.3); }
            QPushButton:hover { background-color: #00ACC1; }
        """)
        button_container.addWidget(self.services_btn)
        button_container.addStretch(1)
        layout.addLayout(button_container)
        layout.addStretch(2)

class RegisterPatientTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(25)
        title_label = QLabel(" 🦷  New Patient Registration")
        title_font = QFont("Arial", 28, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        name_label = QLabel(" 👤  Name:")
        name_label.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(name_label)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(" 👤  Full Name (Required)")
        self.name_input.setFont(QFont("Arial", 16))
        self.name_input.setMinimumHeight(60)
        layout.addWidget(self.name_input)
        dob_label = QLabel(" 📅  Date of Birth:")
        dob_label.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(dob_label)
        self.dob_input = QDateEdit(QDate(2000, 1, 1))
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setDisplayFormat("yyyy-MM-dd")
        self.dob_input.setFont(QFont("Arial", 16))
        self.dob_input.setMinimumHeight(60)
        layout.addWidget(self.dob_input)
        phone_label = QLabel(" 📱  Phone:")
        phone_label.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(phone_label)
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText(" 📱  Phone Number (Required, Unique)")
        self.phone_input.setFont(QFont("Arial", 16))
        self.phone_input.setMinimumHeight(60)
        layout.addWidget(self.phone_input)
        register_btn = QPushButton(" 💾  Register Patient")
        register_btn.setFont(QFont("Arial", 20, QFont.Bold))
        register_btn.setMinimumHeight(70)
        register_btn.setStyleSheet("""
            QPushButton { background-color: #2196F3; color: white; border: none; padding: 20px; border-radius: 15px; }
            QPushButton:hover { background-color: #1E88E5; }
        """)
        self.register_btn = register_btn
        layout.addWidget(register_btn)
        layout.addStretch(1)
        self.setLayout(layout)

class ViewPatientsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        left_panel = QVBoxLayout()
        left_panel.setSpacing(25)
        title_label = QLabel(" 🔍  Patient Records (View/Search)")
        title_font = QFont("Arial", 28, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        left_panel.addWidget(title_label)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(" 🔎  Search by ID, Name, Phone or DOB...")
        self.search_input.setFont(QFont("Arial", 16))
        self.search_input.setMinimumHeight(50)
        search_layout.addWidget(self.search_input)
        search_btn = QPushButton(" 🔍  Search")
        search_btn.setFont(QFont("Arial", 18, QFont.Bold))
        search_btn.setMinimumHeight(60)
        search_btn.setStyleSheet("background-color: #42A5F5; color: white; border-radius: 10px;")
        self.search_btn = search_btn
        search_layout.addWidget(search_btn)
        left_panel.addLayout(search_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["  ID", "   Name", "   DOB", "   Phone"])
        self.table.horizontalHeader().setFont(QFont("Arial", 14, QFont.Bold))
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setFont(QFont("Arial", 12))
        self.table.setStyleSheet("QTableWidget { selection-background-color: #BBDEFB; }")
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        left_panel.addWidget(self.table)

        refresh_btn = QPushButton(" 🔄  Refresh All Patients")
        refresh_btn.setFont(QFont("Arial", 20, QFont.Bold))
        refresh_btn.setMinimumHeight(60)
        refresh_btn.setStyleSheet("background-color: #FF9800; color: white; border-radius: 15px;")
        self.refresh_btn = refresh_btn
        left_panel.addWidget(refresh_btn)
        main_layout.addLayout(left_panel, 2)

        right_panel = QVBoxLayout()
        right_panel.setSpacing(20)
        details_frame = QFrame()
        details_frame.setFrameShape(QFrame.StyledPanel)
        details_frame.setStyleSheet("background-color: #E3F2FD; border-radius: 15px; padding: 20px;")
        details_layout = QVBoxLayout(details_frame)
        details_title = QLabel(" ✏️  Patient Details (Update/Delete)")
        details_title.setFont(QFont("Arial", 24, QFont.Bold))
        details_title.setAlignment(Qt.AlignCenter)
        details_layout.addWidget(details_title)
        self.id_input = QLineEdit()
        self.id_input.setReadOnly(True)
        self.id_input.setFont(QFont("Arial", 16, QFont.Bold))
        self.id_input.setStyleSheet("background-color: #CFD8DC;")
        details_layout.addWidget(QLabel("ID:"))
        details_layout.addWidget(self.id_input)
        self.name_input_u = QLineEdit()
        self.name_input_u.setPlaceholderText("Name")
        self.name_input_u.setFont(QFont("Arial", 16))
        details_layout.addWidget(QLabel("Name:"))
        details_layout.addWidget(self.name_input_u)
        self.dob_input_u = QLineEdit()
        self.dob_input_u.setPlaceholderText("DOB (YYYY-MM-DD)")
        self.dob_input_u.setFont(QFont("Arial", 16))
        details_layout.addWidget(QLabel("DOB:"))
        details_layout.addWidget(self.dob_input_u)
        self.phone_input_u = QLineEdit()
        self.phone_input_u.setPlaceholderText("Phone")
        self.phone_input_u.setFont(QFont("Arial", 16))
        details_layout.addWidget(QLabel("Phone:"))
        details_layout.addWidget(self.phone_input_u)

        button_layout = QHBoxLayout()
        update_btn = QPushButton(" 💾  Update")
        update_btn.setFont(QFont("Arial", 20, QFont.Bold))
        update_btn.setMinimumHeight(70)
        update_btn.setStyleSheet("background-color: #2196F3; color: white; border-radius: 15px;")
        self.update_btn = update_btn
        button_layout.addWidget(update_btn)
        delete_btn = QPushButton(" 🗑️  Delete")
        delete_btn.setFont(QFont("Arial", 20, QFont.Bold))
        delete_btn.setMinimumHeight(70)
        delete_btn.setStyleSheet("background-color: #F44336; color: white; border-radius: 15px;")
        self.delete_btn = delete_btn
        button_layout.addWidget(delete_btn)

        details_layout.addLayout(button_layout)
        right_panel.addWidget(details_frame)
        right_panel.addStretch(1)
        main_layout.addLayout(right_panel, 1)
        self.setLayout(main_layout)

class AddTreatmentTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(25)
        title_label = QLabel(" 💉  Add New Treatment Record")
        title_font = QFont("Arial", 28, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        patient_label = QLabel(" 👤  Patient:")
        patient_label.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(patient_label)
        self.patient_combo = QComboBox()
        self.patient_combo.setFont(QFont("Arial", 16))
        self.patient_combo.setMinimumHeight(60)
        self.patient_combo.setStyleSheet("padding: 15px; color: black;")
        layout.addWidget(self.patient_combo)
        date_label = QLabel(" 📅  Date:")
        date_label.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(date_label)
        self.date_input = QDateEdit(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.date_input.setFont(QFont("Arial", 16))
        self.date_input.setMinimumHeight(60)
        layout.addWidget(self.date_input)
        desc_label = QLabel(" 💉  Treatment Description:")
        desc_label.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(desc_label)
        self.desc_combo = QComboBox()
        self.desc_combo.addItems(TREATMENT_OPTIONS)
        self.desc_combo.setFont(QFont("Arial", 16))
        self.desc_combo.setMinimumHeight(60)
        self.desc_combo.setStyleSheet("padding: 15px; color: black;")
        layout.addWidget(self.desc_combo)
        cost_label = QLabel(" 💰  Cost (₱):")
        cost_label.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(cost_label)
        self.cost_input = QLineEdit()
        self.cost_input.setPlaceholderText(" 💰  Cost (e.g., 150.00)")
        self.cost_input.setFont(QFont("Arial", 16))
        self.cost_input.setMinimumHeight(60)
        layout.addWidget(self.cost_input)
        add_btn = QPushButton(" ➕  Record Treatment")
        add_btn.setFont(QFont("Arial", 20, QFont.Bold))
        add_btn.setMinimumHeight(70)
        add_btn.setStyleSheet("""
            QPushButton { background-color: #9C27B0; color: white; border: none; padding: 20px; border-radius: 15px; }
            QPushButton:hover { background-color: #7B1FA2; }
        """)
        self.add_btn = add_btn
        layout.addWidget(add_btn)
        layout.addStretch(1)
        self.setLayout(layout)

    def load_patient_list(self, patient_data):
        self.patient_combo.clear()
        if not patient_data:
            self.patient_combo.addItem(" ❌  No Patients Found")
            return
        for pid, name, _, phone in patient_data:
            self.patient_combo.addItem(f" 👤 {name} - 🆔 {pid} ({phone})", userData=pid)

class HistoryReportTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(25)
        title_label = QLabel(" 📊  Patient Reports & History")
        title_label.setFont(QFont("Arial", 28, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        history_title = QLabel(" 📋  Individual Patient History")
        history_title.setFont(QFont("Arial", 20, QFont.Bold))
        main_layout.addWidget(history_title)
        lookup_label = QLabel(" 🆔  Enter Patient ID:")
        lookup_label.setFont(QFont("Arial", 18, QFont.Bold))
        main_layout.addWidget(lookup_label)
        lookup_layout = QHBoxLayout()
        self.patient_lookup_input = QLineEdit()
        self.patient_lookup_input.setPlaceholderText(" 🆔  Enter Patient ID to view history...")
        self.patient_lookup_input.setFont(QFont("Arial", 16))
        self.patient_lookup_input.setMinimumHeight(60)
        lookup_layout.addWidget(self.patient_lookup_input)
        lookup_btn = QPushButton(" 📊  View History")
        lookup_btn.setFont(QFont("Arial", 20, QFont.Bold))
        lookup_btn.setMinimumHeight(70)
        lookup_btn.setStyleSheet("""
            QPushButton { background-color: #607D8B; color: white; border: none; padding: 20px; border-radius: 15px; }
            QPushButton:hover { background-color: #455A64; }
        """)
        self.lookup_btn = lookup_btn
        lookup_layout.addWidget(lookup_btn)
        main_layout.addLayout(lookup_layout)
        table_label = QLabel(" 📈  Treatment History:")
        table_label.setFont(QFont("Arial", 18, QFont.Bold))
        main_layout.addWidget(table_label)
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(3)
        self.history_table.setHorizontalHeaderLabels([" 📅  Date", " 💉  Description", " 💰  Cost"])
        header_font = QFont("Arial", 14, QFont.Bold)
        self.history_table.horizontalHeader().setFont(header_font)
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.setFont(QFont("Arial", 12))
        self.history_table.setStyleSheet("QTableWidget { gridline-color: #ccc; }")
        self.history_table.setMinimumHeight(400)
        main_layout.addWidget(self.history_table)
        main_layout.addStretch(1)
        self.setLayout(main_layout)

class DashboardTab(QWidget):
    def __init__(self):
        super().__init__()
        self.figure_bar, self.ax_bar = plt.subplots(figsize=(6, 4))
        self.canvas_bar = FigureCanvas(self.figure_bar)
        self.figure_pie, self.ax_pie = plt.subplots(figsize=(6, 4))
        self.canvas_pie = FigureCanvas(self.figure_pie)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        title_label = QLabel(" 📈  Clinic Performance Dashboard")
        title_label.setFont(QFont("Arial", 30, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #1976D2;")
        main_layout.addWidget(title_label)
        filter_group = QHBoxLayout()
        filter_label = QLabel(" 📅 Filter by Month:")
        filter_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.month_combo = QComboBox()
        self.month_combo.setFont(QFont("Arial", 16))
        self.month_combo.setMinimumHeight(50)
        self.month_combo.setStyleSheet("color: black;")
        filter_group.addWidget(filter_label)
        filter_group.addWidget(self.month_combo)
        filter_group.addStretch(1)
        main_layout.addLayout(filter_group)
        chart_area = QHBoxLayout()
        bar_container = QVBoxLayout()
        bar_title = QLabel("Treatments Performed (Count)")
        bar_title.setFont(QFont("Arial", 20, QFont.Bold))
        bar_title.setAlignment(Qt.AlignCenter)
        bar_container.addWidget(bar_title)
        bar_container.addWidget(self.canvas_bar)
        chart_area.addLayout(bar_container, 1)
        pie_container = QVBoxLayout()
        pie_title = QLabel("Service Revenue Distribution (Monthly)")
        pie_title.setFont(QFont("Arial", 20, QFont.Bold))
        pie_title.setAlignment(Qt.AlignCenter)
        pie_container.addWidget(pie_title)
        pie_container.addWidget(self.canvas_pie)
        chart_area.addLayout(pie_container, 1)
        main_layout.addLayout(chart_area)
        self.setLayout(main_layout)

    def draw_bar_chart(self, data, month):
        self.ax_bar.clear()
        if data:
            treatments, counts = zip(*data)
            x_pos = np.arange(len(treatments))
            self.ax_bar.bar(x_pos, counts, align='center', color='#42A5F5')
            self.ax_bar.set_xticks(x_pos)
            self.ax_bar.set_xticklabels(treatments, fontsize=10, rotation=45, ha='right')
            self.ax_bar.set_ylabel('Number of Times Performed')
            self.ax_bar.set_title(f'Treatment Frequency in {month}')
            self.ax_bar.grid(axis='y', linestyle='--', alpha=0.6)
            for i, v in enumerate(counts):
                self.ax_bar.text(i, v, str(v), color='black', ha='center', va='bottom', fontweight='bold')
        else:
            self.ax_bar.text(0.5, 0.5, 'No Treatments Recorded This Month',
                             ha='center', va='center', transform=self.ax_bar.transAxes, fontsize=14, color='red')
            self.ax_bar.set_xticks([])
            self.ax_bar.set_yticks([])
        self.figure_bar.tight_layout()
        self.canvas_bar.draw()

    def draw_pie_chart(self, data, month):
        self.ax_pie.clear()
        if data:
            treatments, revenues = zip(*data)
            total_revenue = sum(revenues)
            if total_revenue == 0:
                self.ax_pie.text(0.5, 0.5, 'No Revenue Data This Month',
                                 ha='center', va='center', transform=self.ax_pie.transAxes, fontsize=14, color='red')
                self.ax_pie.set_xticks([])
                self.ax_pie.set_yticks([])
            else:
                def func(pct, allvals):
                    absolute = int(np.round(pct / 100. * total_revenue))
                    return f"₱{absolute}\n({pct:.1f}%)"
                self.ax_pie.pie(revenues, labels=treatments, autopct=lambda pct: func(pct, revenues),
                                startangle=90, wedgeprops={'edgecolor': 'black'},
                                textprops={'fontsize': 10, 'fontweight': 'bold'})
                self.ax_pie.axis('equal')
                self.ax_pie.set_title(f'Monthly Revenue by Service in {month}', pad=20)
        else:
            self.ax_pie.text(0.5, 0.5, 'No Revenue Data Available This Month',
                             ha='center', va='center', transform=self.ax_pie.transAxes, fontsize=14, color='red')
            self.ax_pie.set_xticks([])
            self.ax_pie.set_yticks([])
        self.figure_pie.tight_layout()
        self.canvas_pie.draw()

    def draw_empty_charts(self):
        self.ax_bar.clear()
        self.ax_bar.text(0.5, 0.5, 'No Data Available to Plot', ha='center', va='center', transform=self.ax_bar.transAxes, fontsize=16)
        self.canvas_bar.draw()
        self.ax_pie.clear()
        self.ax_pie.text(0.5, 0.5, 'No Data Available to Plot', ha='center', va='center', transform=self.ax_pie.transAxes, fontsize=16)
        self.canvas_pie.draw()


class DentalClinicMainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" 🦷  Dental Clinic Management System")
        self.setGeometry(100, 100, 1800, 1000)
        app_font = QFont("Arial", 14)
        QApplication.setFont(app_font)

        # Main layout structure
        main_content = QWidget()
        main_layout = QHBoxLayout(main_content)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(280)
        sidebar.setStyleSheet("""
            QFrame { background-color: #1976D2; border-right: 2px solid #0D47A1; }
            QPushButton { background-color: transparent; color: white; border: none; padding: 25px 15px; text-align: left; font-size: 18px; font-weight: bold; border-left: 5px solid transparent; }
            QPushButton:hover { background-color: #1565C0; }
            QPushButton:checked { background-color: #2196F3; border-left: 5px solid #FFC107; }
        """)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setAlignment(Qt.AlignTop)
        logo_label = QLabel("DENTAL CLINIC")
        logo_label.setFont(QFont("Arial", 22, QFont.Bold))
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet("color: white; padding: 20px; margin-bottom: 20px;")
        sidebar_layout.addWidget(logo_label)

        # Buttons
        buttons = [
            (" 🏠  HOME", 0),
            (" ➕  Register Patient", 1),
            (" 👀  View/Edit Patients", 2),
            (" 💉  Add Treatment", 3),
            (" 📊  Dashboard", 4),
            (" 📋  History", 5),
        ]
        self.tab_buttons = {}
        for text, index in buttons:
            btn = QPushButton(text)
            btn.setCheckable(True)
            self.tab_buttons[index] = btn
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch(1)
        logout_btn = QPushButton(" 🚪  LOGOUT")
        logout_btn.setFont(QFont("Arial", 18, QFont.Bold))
        logout_btn.setMinimumHeight(60)
        logout_btn.setStyleSheet("""
            QPushButton { background-color: #D32F2F; color: white; border: none; padding: 15px; border-radius: 10px; margin: 20px 10px 10px 10px; }
            QPushButton:hover { background-color: #C62828; }
        """)
        self.logout_btn = logout_btn
        sidebar_layout.addWidget(logout_btn)

        main_layout.addWidget(sidebar)

        # Stacked content
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("""
            QStackedWidget { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F5F8FF, stop:1 #E6F3FF); border: none; padding: 20px; }
        """)
        # instantiate Views (not controllers)
        self.home_tab = HomeTab()
        self.register_tab = RegisterPatientTab()
        self.view_tab = ViewPatientsTab()
        self.add_treatment_tab = AddTreatmentTab()
        self.dashboard_tab = DashboardTab()
        self.history_tab = HistoryReportTab()

        self.stacked_widget.addWidget(self.home_tab)
        self.stacked_widget.addWidget(self.register_tab)
        self.stacked_widget.addWidget(self.view_tab)
        self.stacked_widget.addWidget(self.add_treatment_tab)
        self.stacked_widget.addWidget(self.dashboard_tab)
        self.stacked_widget.addWidget(self.history_tab)

        main_layout.addWidget(self.stacked_widget, 1)

        self.setCentralWidget(main_content)

# ---- Additional tabs & main window classes omitted here due to length ----
# You will include HomeTab, RegisterPatientTab, ViewPatientsTab, AddTreatmentTab,
# HistoryReportTab, DashboardTab, DentalClinicMainView in full just like above,
# importing TREATMENT_OPTIONS from model.

