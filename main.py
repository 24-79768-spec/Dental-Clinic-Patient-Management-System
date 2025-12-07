import sys
from PyQt5.QtWidgets import QApplication, QMessageBox, QDialog
from model import DatabaseManager
from view import LoginDialog, DentalClinicMainView
from controller import AppController

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    model = DatabaseManager()

    while True:
        login = LoginDialog()
        def attempt_login():
            username = login.username_input.text().strip()
            password = login.password_input.text().strip()
            if model.verify_user(username, password):
                login.accept()
            else:
                QMessageBox.warning(login, "Login Failed", "Invalid username or password!")
        login.login_btn.clicked.connect(attempt_login)

        if login.exec_() == QDialog.Accepted:
            main_view = DentalClinicMainView()
            controller = AppController(model, main_view)
            main_view.show()
            app.exec_()
            if controller.should_restart:
                continue
            else:
                break
        else:
            break

    model.close()
    sys.exit(0)

if __name__ == "__main__":
    main()
