# test_controller.py
import unittest
from PyQt5.QtWidgets import QMessageBox
from unittest.mock import MagicMock, patch
from controller import AppController

class TestAppController(unittest.TestCase):
    def setUp(self):
        # Mock the model
        self.mock_model = MagicMock()
        self.mock_model.insert_patient.return_value = True
        self.mock_model.fetch_all_patients.return_value = [
            (1, "John Doe", "2000-01-01", "1234567890")
        ]
        self.mock_model.update_patient.return_value = True
        self.mock_model.delete_patient.return_value = True
        self.mock_model.insert_treatment.return_value = True
        self.mock_model.fetch_patient_history.return_value = [
            (1, "2000-01-01", "Checkup", 50.0)
        ]
        self.mock_model.fetch_available_months.return_value = ["2025-12"]

        # Mock the view and its widgets
        self.mock_view = MagicMock()
        self.mock_view.tab_buttons = {0: MagicMock(), 1: MagicMock()}
        self.mock_view.stacked_widget = MagicMock()
        self.mock_view.register_tab.name_input.text.return_value = "John Doe"
        self.mock_view.register_tab.dob_input.date.return_value.toString.return_value = "2000-01-01"
        self.mock_view.register_tab.phone_input.text.return_value = "1234567890"
        self.mock_view.view_tab.table = MagicMock()
        self.mock_view.view_tab.id_input.text.return_value = "1"
        self.mock_view.view_tab.name_input_u.text.return_value = "John Doe"
        self.mock_view.view_tab.dob_input_u.text.return_value = "2000-01-01"
        self.mock_view.view_tab.phone_input_u.text.return_value = "1234567890"
        self.mock_view.add_treatment_tab.patient_combo.currentData.return_value = 1
        self.mock_view.add_treatment_tab.desc_combo.currentText.return_value = "Cleaning"
        self.mock_view.add_treatment_tab.cost_input.text.return_value = "50"
        self.mock_view.history_tab.patient_lookup_input.text.return_value = "1"

        # Initialize controller
        self.controller = AppController(self.mock_model, self.mock_view)

    @patch('PyQt5.QtWidgets.QMessageBox.information')
    @patch('PyQt5.QtWidgets.QMessageBox.warning')
    @patch('PyQt5.QtWidgets.QMessageBox.critical')
    def test_register_patient_success(self, mock_critical, mock_warning, mock_info):
        self.controller.handle_register_patient()
        self.mock_model.insert_patient.assert_called_with("John Doe", "2000-01-01", "1234567890")
        self.mock_view.register_tab.name_input.clear.assert_called()
        self.mock_view.register_tab.phone_input.clear.assert_called()
        mock_info.assert_called()  # QMessageBox.information should be called

    @patch('PyQt5.QtWidgets.QMessageBox.information')
    def test_update_patient_success(self, mock_info):
        self.controller.handle_update_patient()
        self.mock_model.update_patient.assert_called_with(1, "John Doe", "2000-01-01", "1234567890")
        mock_info.assert_called()

    @patch('PyQt5.QtWidgets.QMessageBox.question', return_value=QMessageBox.Yes)
    @patch('PyQt5.QtWidgets.QMessageBox.information')
    def test_delete_patient_success(self, mock_info, mock_question):
        self.controller.handle_delete_patient()
        self.mock_model.delete_patient.assert_called_with(1)
        mock_info.assert_called()

    @patch('PyQt5.QtWidgets.QMessageBox.information')
    @patch('PyQt5.QtWidgets.QMessageBox.warning')
    @patch('PyQt5.QtWidgets.QMessageBox.critical')
    def test_record_treatment_success(self, mock_critical, mock_warning, mock_info):
        self.controller.handle_record_treatment()
        self.mock_model.insert_treatment.assert_called_with(
            1,
            self.mock_view.add_treatment_tab.date_input.date().toString.return_value,
            "Cleaning",
            50.0
        )
        mock_info.assert_called()

    @patch('PyQt5.QtWidgets.QMessageBox.information')
    def test_lookup_history_success(self, mock_info):
        self.controller.handle_lookup_history()
        self.mock_model.fetch_patient_history.assert_called_with(1)

if __name__ == "__main__":
    unittest.main()
