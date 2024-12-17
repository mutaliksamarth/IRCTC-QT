import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
# from login import LoginWindow
# from register import RegisterWindow
# from reset_password import ResetPasswordWindow

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IRCTC User System")
        self.setGeometry(100, 100, 400, 300)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.open_login_window)

        register_button = QPushButton("Register")
        register_button.clicked.connect(self.open_register_window)

        reset_password_button = QPushButton("Forgot Password")
        reset_password_button.clicked.connect(self.open_reset_password_window)

        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.close)

        layout.addWidget(login_button)
        layout.addWidget(register_button)
        layout.addWidget(reset_password_button)
        layout.addWidget(exit_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_login_window(self):

        self.login_window.show()

    def open_register_window(self):

        self.register_window.show()

    def open_reset_password_window(self):
        
        self.reset_password_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
