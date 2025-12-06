import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QDialog

# Local Imports
from controller import DentalClinicApp
from view import LoginDialog

if __name__ == '__main__':
    # Fix for matplotlib/Qt conflict if using certain backends
    plt.ion()
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # Main loop for the application
    while True:
        # 1. Login attempt
        login_dialog = LoginDialog()

        # Show the login dialog
        if login_dialog.exec_() == QDialog.Accepted:
            # 2. Login successful, start Main Application
            window = DentalClinicApp()
            window.show()

            # Start the event loop for the main window
            app.exec_()

            # 3. Check if we need to restart (re-login)
            if window.should_restart:
                del window
                continue
            else:
                # Window closed via X button, exit
                break
        else:
            # Login cancelled or failed
            break

    sys.exit(0)