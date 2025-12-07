from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QDialog
from model import DatabaseManager
from view import (
    DentalClinicMainView,
    LoginDialog,
    AboutDialog,
    ServicesDialog
)

class AppController:
    def __init__(self, model: DatabaseManager, main_view: DentalClinicMainView):
        self.model = model
        self.view = main_view

        # flag for logout/restart
        self.should_restart = False

        # Connect sidebar buttons to tab switching
        for idx, btn in self.view.tab_buttons.items():
            btn.clicked.connect(lambda checked, i=idx: self.switch_tab(i))

        # Connect logout button
        self.view.logout_btn.clicked.connect(self.logout)

        # Home tab actions
        self.view.home_tab.about_btn.clicked.connect(self.show_about)
        self.view.home_tab.services_btn.clicked.connect(self.show_services)

        # Register patient tab
        self.view.register_tab.register_btn.clicked.connect(self.handle_register_patient)

        # View patients tab
        self.view.view_tab.refresh_btn.clicked.connect(self.load_patients_into_table)
        self.view.view_tab.search_btn.clicked.connect(self.handle_search_patients)
        self.view.view_tab.table.cellClicked.connect(self.handle_table_click)
        self.view.view_tab.update_btn.clicked.connect(self.handle_update_patient)
        self.view.view_tab.delete_btn.clicked.connect(self.handle_delete_patient)

        # Add treatment tab
        self.view.add_treatment_tab.add_btn.clicked.connect(self.handle_record_treatment)

        # History tab
        self.view.history_tab.lookup_btn.clicked.connect(self.handle_lookup_history)

        # Dashboard tab
        self.view.dashboard_tab.month_combo.currentIndexChanged.connect(self.update_dashboard_charts)

        # Show initial tab
        self.switch_tab(0)

    # ---------------- Tab Switching -----------------
    def switch_tab(self, index):
        for idx, btn in self.view.tab_buttons.items():
            btn.setChecked(idx == index)
        self.view.stacked_widget.setCurrentIndex(index)

        widget = self.view.stacked_widget.widget(index)
        if widget == self.view.add_treatment_tab:
            self.load_patients_for_add_treatment()
        elif widget == self.view.view_tab:
            self.load_patients_into_table()
        elif widget == self.view.dashboard_tab:
            self.load_dashboard_filters()

    # ---------------- Home Dialogs -----------------
    def show_about(self):
        dlg = AboutDialog(self.view)
        dlg.close_btn.clicked.connect(dlg.accept)
        dlg.exec_()

    def show_services(self):
        dlg = ServicesDialog(self.view)
        dlg.close_btn.clicked.connect(dlg.accept)
        dlg.exec_()

    # ---------------- Register Patient -----------------
    def handle_register_patient(self):
        name = self.view.register_tab.name_input.text().strip()
        dob = self.view.register_tab.dob_input.date().toString("yyyy-MM-dd")
        phone = self.view.register_tab.phone_input.text().strip()

        if not name or not phone:
            QMessageBox.warning(self.view, "Input Error", "Name and Phone are required fields.")
            return

        if self.model.insert_patient(name, dob, phone):
            QMessageBox.information(self.view, "Success", f"Patient {name} registered successfully!")
            self.view.register_tab.name_input.clear()
            self.view.register_tab.dob_input.setDate(QDate(2000, 1, 1))
            self.view.register_tab.phone_input.clear()
            # Refresh dependent tabs
            self.load_patients_into_table()
            self.load_patients_for_add_treatment()
        else:
            QMessageBox.critical(self.view, "Error", "Registration failed. Phone number might already exist.")

    # ---------------- View/Search Patients -----------------
    def load_patients_into_table(self):
        patients = self.model.fetch_all_patients()
        table = self.view.view_tab.table
        table.setRowCount(len(patients))
        for row_num, row_data in enumerate(patients):
            for col_num, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(row_num, col_num, item)
        self.clear_patient_details_inputs()

    def handle_search_patients(self):
        query = self.view.view_tab.search_input.text().strip()
        if not query:
            self.load_patients_into_table()
            return
        patients = self.model.search_patients(query)
        table = self.view.view_tab.table
        table.setRowCount(len(patients))
        for row_num, row_data in enumerate(patients):
            for col_num, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(row_num, col_num, item)
        if not patients:
            QMessageBox.information(self.view, "Info", "No matching patients found.")
            self.clear_patient_details_inputs()

    def handle_table_click(self, row, column):
        table = self.view.view_tab.table
        try:
            patient_id = table.item(row, 0).text()
            name = table.item(row, 1).text()
            dob = table.item(row, 2).text()
            phone = table.item(row, 3).text()
            self.view.view_tab.id_input.setText(patient_id)
            self.view.view_tab.name_input_u.setText(name)
            self.view.view_tab.dob_input_u.setText(dob)
            self.view.view_tab.phone_input_u.setText(phone)
        except Exception:
            self.clear_patient_details_inputs()

    def clear_patient_details_inputs(self):
        self.view.view_tab.id_input.clear()
        self.view.view_tab.name_input_u.clear()
        self.view.view_tab.dob_input_u.clear()
        self.view.view_tab.phone_input_u.clear()

    def handle_update_patient(self):
        pid_str = self.view.view_tab.id_input.text().strip()
        name = self.view.view_tab.name_input_u.text().strip()
        dob = self.view.view_tab.dob_input_u.text().strip()
        phone = self.view.view_tab.phone_input_u.text().strip()

        if not pid_str or not name or not phone:
            QMessageBox.warning(self.view, "Input Error", "Select a patient and fill Name & Phone.")
            return

        if self.model.update_patient(int(pid_str), name, dob, phone):
            QMessageBox.information(self.view, "Success", f"Patient ID {pid_str} updated successfully!")
            self.load_patients_into_table()
            self.load_patients_for_add_treatment()
        else:
            QMessageBox.critical(self.view, "Error", "Update failed. Phone might already exist.")

    def handle_delete_patient(self):
        pid_str = self.view.view_tab.id_input.text().strip()
        if not pid_str:
            QMessageBox.warning(self.view, "Selection Error", "Select a patient from the table to delete.")
            return
        reply = QMessageBox.question(self.view, "Confirm Delete",
                                     f"Are you sure you want to delete Patient ID {pid_str}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.model.delete_patient(int(pid_str)):
                QMessageBox.information(self.view, "Success", f"Patient ID {pid_str} deleted.")
                self.load_patients_into_table()
                self.load_patients_for_add_treatment()
                self.clear_patient_details_inputs()
            else:
                QMessageBox.critical(self.view, "Error", "Deletion failed.")

    # ---------------- Add Treatment -----------------
    def load_patients_for_add_treatment(self):
        patients = self.model.fetch_all_patients()
        self.view.add_treatment_tab.load_patient_list(patients)

    def handle_record_treatment(self):
        patient_id = self.view.add_treatment_tab.patient_combo.currentData()
        date = self.view.add_treatment_tab.date_input.date().toString("yyyy-MM-dd")
        description = self.view.add_treatment_tab.desc_combo.currentText()
        cost_str = self.view.add_treatment_tab.cost_input.text().strip()

        if patient_id is None or not description or not cost_str:
            QMessageBox.warning(self.view, "Input Error", "Select patient, description, and enter cost.")
            return
        try:
            cost = float(cost_str)
        except ValueError:
            QMessageBox.critical(self.view, "Input Error", "Cost must be a valid number.")
            return
        if self.model.insert_treatment(patient_id, date, description, cost):
            QMessageBox.information(self.view, "Success", f"Treatment recorded for Patient ID {patient_id}.")
            self.view.add_treatment_tab.cost_input.clear()
        else:
            QMessageBox.critical(self.view, "Error", "Failed to record treatment.")

    # ---------------- History -----------------
    def handle_lookup_history(self):
        pid_str = self.view.history_tab.patient_lookup_input.text().strip()
        if not pid_str:
            QMessageBox.warning(self.view, "Input Error", "Enter a Patient ID.")
            return
        try:
            pid = int(pid_str)
        except ValueError:
            QMessageBox.critical(self.view, "Input Error", "Patient ID must be a number.")
            return

        history = self.model.fetch_patient_history(pid)
        table = self.view.history_tab.history_table
        table.setRowCount(len(history))
        if not history:
            QMessageBox.information(self.view, "Info", f"No history for Patient ID {pid}.")
            return

        for row_num, row_data in enumerate(history):
            for col_num, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(row_num, col_num, item)

    # ---------------- Dashboard -----------------
    def load_dashboard_filters(self):
        combo = self.view.dashboard_tab.month_combo
        combo.blockSignals(True)
        combo.clear()
        months = self.model.fetch_available_months()
        if not months:
            combo.addItem("No data available")
            self.view.dashboard_tab.draw_empty_charts()
            combo.blockSignals(False)
            return
        combo.addItems(months)
        combo.blockSignals(False)
        self.update_dashboard_charts()

    def update_dashboard_charts(self):
        selected_month = self.view.dashboard_tab.month_combo.currentText()
        if not selected_month or selected_month == "No data available":
            self.view.dashboard_tab.draw_empty_charts()
            return
        counts = self.model.fetch_treatment_counts_by_month(selected_month)
        revenue = self.model.fetch_treatment_revenue_by_month(selected_month)
        self.view.dashboard_tab.draw_bar_chart(counts, selected_month)
        self.view.dashboard_tab.draw_pie_chart(revenue, selected_month)

    # ---------------- Logout -----------------
    def logout(self):
        reply = QMessageBox.question(self.view, "Confirm Logout",
                                     "Log out and return to login screen?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.should_restart = True
            self.view.close()
