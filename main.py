import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget, QLabel, QStackedWidget, QMainWindow
from PyQt5.QtCore import Qt

from db import init_db
from login import LoginForm
from register import Registration

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IRCTC")
        self.setGeometry(100, 100, 400, 200)
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.InitUI()

    def InitUI(self):
        self.LogInButton = QPushButton("Log In")
        self.SignUpButton = QPushButton("Sign Up")

        self.Title = QLabel("Welcome to IRCTC")
        self.Title.setAlignment(Qt.AlignCenter)

        self.LogInButton.clicked.connect(self.open_login_form)
        self.SignUpButton.clicked.connect(self.open_registration_form)

        vbox = QVBoxLayout()
        vbox.addWidget(self.Title)
        vbox.addWidget(self.LogInButton)
        vbox.addWidget(self.SignUpButton)

        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.stacked_widget.addWidget(central_widget)

        self.Title.setStyleSheet("""
        QLabel {
            font-size: 100px;
            font-weight: bold;
            color: #333;
            margin-bottom: 20px;
        } """)
        self.setStyleSheet("""QPushButton {
            font-size: 24px;
            font-weight: bold;
            color: #fff;
            background-color: gray;
            border: none;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 10px;
        }
        QPushButton:hover {
            background-color: #333;
        }
        """)

    def open_login_form(self):
        login_form = LoginForm(self.stacked_widget)
        self.stacked_widget.addWidget(login_form)
        self.stacked_widget.setCurrentWidget(login_form)

    def open_registration_form(self):
        registration_form = Registration(self.stacked_widget)
        self.stacked_widget.addWidget(registration_form)
        self.stacked_widget.setCurrentWidget(registration_form)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    init_db()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())