# System and Matplotlib Imports
import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

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
from database import DatabaseManager
from model import TREATMENT_OPTIONS
from view import HomeTab, LoginDialog # Import classes needed from view

# --- Tab Controllers (Contain UI setup AND DB interaction logic) ---

class RegisterPatientTab(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
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
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 20px;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #1E88E5;
            }
        """)
        register_btn.clicked.connect(self.register_patient)
        layout.addWidget(register_btn)
        layout.addStretch(1)
        self.setLayout(layout)

    def register_patient(self):
        name = self.name_input.text().strip()
        dob = self.dob_input.date().toString("yyyy-MM-dd")
        phone = self.phone_input.text().strip()
        if not name or not phone:
            QMessageBox.warning(self, " ⚠️  Input Error", "Name and Phone are required fields.")
            return
        if self.db.insert_patient(name, dob, phone):
            QMessageBox.information(self, " ✅  Success", f"Patient **{name}** registered successfully!")
            self.name_input.clear()
            self.dob_input.setDate(QDate(2000, 1, 1))
            self.phone_input.clear()
        else:
            QMessageBox.critical(self, " ❌  Error", "Registration failed. Phone number might already exist.")


class ViewPatientsTab(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.init_ui()
        self.load_patients()

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
        search_btn.clicked.connect(self.search_patients)
        search_btn.setStyleSheet(
            "background-color: #42A5F5; color: white; border-radius: 10px;")
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
        self.table.cellClicked.connect(self.show_patient_details)
        left_panel.addWidget(self.table)

        refresh_btn = QPushButton(" 🔄  Refresh All Patients")
        refresh_btn.setFont(QFont("Arial", 20, QFont.Bold))
        refresh_btn.setMinimumHeight(60)
        refresh_btn.setStyleSheet("background-color: #FF9800; color: white; border-radius: 15px;")
        refresh_btn.clicked.connect(self.load_patients)
        left_panel.addWidget(refresh_btn)
        main_layout.addLayout(left_panel, 2)

        right_panel = QVBoxLayout()
        right_panel.setSpacing(20)
        details_frame = QFrame()
        details_frame.setFrameShape(QFrame.StyledPanel)
        details_frame.setStyleSheet(
            "background-color: #E3F2FD; border-radius: 15px; padding: 20px;")
        details_layout = QVBoxLayout(details_frame)
        details_title = QLabel(" ✏️  Patient Details (Update/Delete)")
        details_title.setFont(QFont("Arial", 24, QFont.Bold))
        details_title.setAlignment(Qt.AlignCenter)
        details_layout.addWidget(details_title)
        self.id_label = QLabel("ID:")
        self.id_input = QLineEdit()
        self.id_input.setReadOnly(True)
        self.id_input.setFont(QFont("Arial", 16, QFont.Bold))
        self.id_input.setStyleSheet("background-color: #CFD8DC;")
        details_layout.addWidget(self.id_label)
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
        update_btn.setStyleSheet(
            "background-color: #2196F3; color: white; border-radius: 15px;")
        update_btn.clicked.connect(self.update_patient)
        button_layout.addWidget(update_btn)
        delete_btn = QPushButton(" 🗑️  Delete")
        delete_btn.setFont(QFont("Arial", 20, QFont.Bold))
        delete_btn.setMinimumHeight(70)
        delete_btn.setStyleSheet("background-color: #F44336; color: white; border-radius: 15px;")
        delete_btn.clicked.connect(self.delete_patient)
        button_layout.addWidget(delete_btn)

        details_layout.addLayout(button_layout)
        right_panel.addWidget(details_frame)
        right_panel.addStretch(1)
        main_layout.addLayout(right_panel, 1)
        self.setLayout(main_layout)

    def show_patient_details(self, row, column):
        try:
            patient_id = self.table.item(row, 0).text()
            name = self.table.item(row, 1).text()
            dob = self.table.item(row, 2).text()
            phone = self.table.item(row, 3).text()
            self.id_input.setText(patient_id)
            self.name_input_u.setText(name)
            self.dob_input_u.setText(dob)
            self.phone_input_u.setText(phone)
        except AttributeError:
            self.id_input.clear()
            self.name_input_u.clear()
            self.dob_input_u.clear()
            self.phone_input_u.clear()

    def update_patient(self):
        patient_id = self.id_input.text().strip()
        name = self.name_input_u.text().strip()
        dob = self.dob_input_u.text().strip()
        phone = self.phone_input_u.text().strip()
        if not patient_id or not name or not phone:
            QMessageBox.warning(self, " ⚠️  Input Error", "Please select a patient and fill in Name and Phone.")
            return
        if self.db.update_patient(int(patient_id), name, dob, phone):
            QMessageBox.information(self, " ✅  Success", f"Patient ID {patient_id} updated successfully!")
            self.load_patients()
        else:
            QMessageBox.critical(self, " ❌  Error",
                                 "Update failed. Phone number might already exist or data is invalid.")

    def delete_patient(self):
        patient_id_str = self.id_input.text().strip()
        if not patient_id_str:
            QMessageBox.warning(self, " ⚠️  Selection Error", "Please select a patient from the table to delete.")
            return
        reply = QMessageBox.question(self, ' 🗑️  Confirm Delete',
                                     f"Are you sure you want to delete Patient ID **{patient_id_str}** and all their treatments?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.db.delete_patient(int(patient_id_str)):
                QMessageBox.information(self, " ✅  Success", f"Patient ID {patient_id_str} deleted.")
                self.load_patients()
                self.id_input.clear()
                self.name_input_u.clear()
                self.dob_input_u.clear()
                self.phone_input_u.clear()
            else:
                QMessageBox.critical(self, " ❌  Error", "Deletion failed.")

    def search_patients(self):
        query = self.search_input.text().strip()
        if not query:
            self.load_patients()
            return
        patients = self.db.search_patients(query)
        self._populate_table(patients)

    def load_patients(self):
        patients = self.db.fetch_all_patients()
        self._populate_table(patients)

    def _populate_table(self, patients):
        self.table.setRowCount(len(patients))
        for row_num, row_data in enumerate(patients):
            for col_num, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                item.setFont(QFont("Arial", 12))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_num, col_num, item)
        if not patients and self.search_input.text():
            QMessageBox.information(self, " ℹ️  Info", "No matching patients found.")


class AddTreatmentTab(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.init_ui()
        self.load_patient_list()

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
            QPushButton {
                background-color: #9C27B0;
                color: white;
                border: none;
                padding: 20px;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #7B1FA2;
            }
        """)
        add_btn.clicked.connect(self.record_treatment)
        layout.addWidget(add_btn)
        layout.addStretch(1)
        self.setLayout(layout)

    def load_patient_list(self):
        self.patient_combo.clear()
        self.patient_data = self.db.fetch_all_patients()
        if not self.patient_data:
            self.patient_combo.addItem(" ❌  No Patients Found")
            return
        for pid, name, _, phone in self.patient_data:
            self.patient_combo.addItem(f" 👤 {name} - 🆔 {pid} ({phone})", userData=pid)

    def record_treatment(self):
        patient_id = self.patient_combo.currentData()
        date = self.date_input.date().toString("yyyy-MM-dd")
        description = self.desc_combo.currentText()
        cost_str = self.cost_input.text().strip()
        if patient_id is None or not description or not cost_str:
            QMessageBox.warning(self, " ⚠️  Input Error", "Please select a patient, a description, and enter a cost.")
            return
        try:
            cost = float(cost_str)
        except ValueError:
            QMessageBox.critical(self, " ⚠️  Input Error", "Cost must be a valid number.")
            return
        if self.db.insert_treatment(patient_id, date, description, cost):
            QMessageBox.information(self, " ✅  Success",
                                    f"Treatment recorded: **{description}** for Patient ID {patient_id}.")
            self.cost_input.clear()
        else:
            QMessageBox.critical(self, " ❌  Error", "Failed to record treatment.")


class HistoryReportTab(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(25)
        title_label = QLabel(" 📊  Patient Reports & History")
        title_font = QFont("Arial", 28, QFont.Bold)
        title_label.setFont(title_font)
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
            QPushButton {
                background-color: #607D8B;
                color: white;
                border: none;
                padding: 20px;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #455A64;
            }
        """)
        lookup_btn.clicked.connect(self.lookup_history)
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

    def lookup_history(self):
        patient_id_str = self.patient_lookup_input.text().strip()
        if not patient_id_str:
            QMessageBox.warning(self, " ⚠️  Input Error", "Please enter a Patient ID.")
            return
        try:
            patient_id = int(patient_id_str)
        except ValueError:
            QMessageBox.critical(self, " ⚠️  Input Error", "Patient ID must be a number.")
            return
        history = self.db.fetch_patient_history(patient_id)
        self.history_table.setRowCount(len(history))
        if not history:
            QMessageBox.information(self, " ℹ️  Info", f"No treatment history found for Patient ID {patient_id}.")
            return
        for row_num, row_data in enumerate(history):
            for col_num, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                item.setFont(QFont("Arial", 12))
                item.setTextAlignment(Qt.AlignCenter)
                self.history_table.setItem(row_num, col_num, item)


class DashboardTab(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
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

        # --- Month Filter and Bar Chart ---
        filter_group = QHBoxLayout()
        filter_label = QLabel(" 📅 Filter by Month:")
        filter_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.month_combo = QComboBox()
        self.month_combo.setFont(QFont("Arial", 16))
        self.month_combo.setMinimumHeight(50)
        self.month_combo.setStyleSheet("color: black;")
        self.month_combo.currentIndexChanged.connect(self.update_charts)
        filter_group.addWidget(filter_label)
        filter_group.addWidget(self.month_combo)
        filter_group.addStretch(1)
        main_layout.addLayout(filter_group)

        # --- Chart Area (Horizontal Layout) ---
        chart_area = QHBoxLayout()

        # Bar Chart Container
        bar_container = QVBoxLayout()
        bar_title = QLabel("Treatments Performed (Count)")
        bar_title.setFont(QFont("Arial", 20, QFont.Bold))
        bar_title.setAlignment(Qt.AlignCenter)
        bar_container.addWidget(bar_title)
        bar_container.addWidget(self.canvas_bar)
        chart_area.addLayout(bar_container, 1)

        # Pie Chart Container
        pie_container = QVBoxLayout()
        pie_title = QLabel("Service Revenue Distribution (Monthly)")
        pie_title.setFont(QFont("Arial", 20, QFont.Bold))
        pie_title.setAlignment(Qt.AlignCenter)
        pie_container.addWidget(pie_title)
        pie_container.addWidget(self.canvas_pie)
        chart_area.addLayout(pie_container, 1)

        main_layout.addLayout(chart_area)
        self.setLayout(main_layout)

    def load_data_and_filters(self):
        """Populates the month filter and draws initial charts."""
        self.month_combo.blockSignals(True)
        self.month_combo.clear()

        months = self.db.fetch_available_months()
        if not months:
            self.month_combo.addItem("No data available")
            self.draw_empty_charts()
            return

        self.month_combo.addItems(months)
        self.month_combo.blockSignals(False)
        self.update_charts()

    def update_charts(self):
        """Called when month filter changes or tab opens."""
        selected_month = self.month_combo.currentText()
        if selected_month == "No data available":
            self.draw_empty_charts()
            return

        # 1. Bar Chart Data (Treatments Count per month)
        count_data = self.db.fetch_treatment_counts_by_month(selected_month)
        self.draw_bar_chart(count_data, selected_month)

        # 2. Pie Chart Data (Total Revenue Distribution)
        revenue_data = self.db.fetch_treatment_revenue_by_month(selected_month)
        self.draw_pie_chart(revenue_data, selected_month)

    def draw_bar_chart(self, data, month):
        """Draws the vertical bar graph for treatment counts."""
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
        """Draws the pie chart for revenue distribution for a specific month."""
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
        self.ax_bar.text(0.5, 0.5, 'No Data Available to Plot', ha='center', va='center',
                         transform=self.ax_bar.transAxes, fontsize=16)
        self.canvas_bar.draw()

        self.ax_pie.clear()
        self.ax_pie.text(0.5, 0.5, 'No Data Available to Plot', ha='center', va='center',
                         transform=self.ax_pie.transAxes, fontsize=16)
        self.canvas_pie.draw()


# --- Main Application Controller ---
class DentalClinicApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.should_restart = False
        self.db_manager = DatabaseManager() # Initialized the database manager
        self.setWindowTitle(" 🦷  Dental Clinic Management System")
        self.setGeometry(100, 100, 1800, 1000)

        app_font = QFont("Arial", 14)
        QApplication.setFont(app_font)

        # Main layout structure (Horizontal for Sidebar + Content)
        main_content = QWidget()
        main_layout = QHBoxLayout(main_content)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # --- 1. Sidebar Menu (Blue Theme) ---
        sidebar = QFrame()
        sidebar.setFixedWidth(280)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #1976D2;
                border-right: 2px solid #0D47A1;
            }
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                padding: 25px 15px;
                text-align: left;
                font-size: 18px;
                font-weight: bold;
                border-left: 5px solid transparent;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
            QPushButton:checked {
                background-color: #2196F3;
                border-left: 5px solid #FFC107;
            }
        """)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setAlignment(Qt.AlignTop)

        # Clinic Title/Logo in Sidebar
        logo_label = QLabel("DENTAL CLINIC")
        logo_label.setFont(QFont("Arial", 22, QFont.Bold))
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet("color: white; padding: 20px; margin-bottom: 20px;")
        sidebar_layout.addWidget(logo_label)

        # Define buttons and their target indexes
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
            btn.clicked.connect(lambda checked, idx=index: self.switch_tab(idx))
            self.tab_buttons[index] = btn
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch(1)

        # --- LOGOUT Button ---
        logout_btn = QPushButton(" 🚪  LOGOUT")
        logout_btn.setFont(QFont("Arial", 18, QFont.Bold))
        logout_btn.setMinimumHeight(60)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #D32F2F;
                color: white;
                border: none;
                padding: 15px;
                border-radius: 10px;
                margin: 20px 10px 10px 10px;
            }
            QPushButton:hover {
                background-color: #C62828;
            }
        """)
        logout_btn.clicked.connect(self.logout)
        sidebar_layout.addWidget(logout_btn)

        # Add sidebar to the main layout
        main_layout.addWidget(sidebar)

        # --- 2. Content Area (Stacked Widget) ---
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("""
            QStackedWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #F5F8FF, stop:1 #E6F3FF);
                border: none;
                padding: 20px;
            }
        """)

        # Create tab instances and add them to the stacked widget
        self.home_tab = HomeTab() # From view.py
        self.register_patient_tab = RegisterPatientTab(self.db_manager)
        self.view_patients_tab = ViewPatientsTab(self.db_manager)
        self.add_treatment_tab = AddTreatmentTab(self.db_manager)
        self.dashboard_tab = DashboardTab(self.db_manager)
        self.history_report_tab = HistoryReportTab(self.db_manager)

        self.stacked_widget.addWidget(self.home_tab)
        self.stacked_widget.addWidget(self.register_patient_tab)
        self.stacked_widget.addWidget(self.view_patients_tab)
        self.stacked_widget.addWidget(self.add_treatment_tab)
        self.stacked_widget.addWidget(self.dashboard_tab)
        self.stacked_widget.addWidget(self.history_report_tab)

        main_layout.addWidget(self.stacked_widget, 1)

        self.setCentralWidget(main_content)

        # Set initial tab to HOME (Index 0)
        self.switch_tab(0)

    def switch_tab(self, index):
        """Switches the view in the stacked widget and updates data/button state."""
        # Update button state
        for idx, btn in self.tab_buttons.items():
            btn.setChecked(idx == index)

        self.stacked_widget.setCurrentIndex(index)

        # Reload data based on the new tab
        widget = self.stacked_widget.widget(index)

        if widget == self.add_treatment_tab:
            self.add_treatment_tab.load_patient_list()
        elif widget == self.view_patients_tab:
            self.view_patients_tab.load_patients()
        elif widget == self.dashboard_tab:
            self.dashboard_tab.load_data_and_filters()

    def logout(self):
        """Handles the logout action: confirms and closes the application, signals re-login."""
        reply = QMessageBox.question(self, ' 🚪  Confirm Logout',
                                     "Are you sure you want to log out and return to the login screen?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.should_restart = True
            self.close()

    def closeEvent(self, event):
        """Closes the database connection when the application closes."""
        self.db_manager.close()
        event.accept()