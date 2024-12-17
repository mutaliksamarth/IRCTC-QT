from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
import sys
from db import fetch_query, execute_query
import re
from reset_password import ResetPassword, UserVerify


class LoginForm(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.init_ui()

    def init_ui(self):

        title = QLabel("Log In to IRCTC")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 36px; font-weight: bold; color: #333; margin-bottom: 20px;")


        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your email")
        self.username_input.setStyleSheet("padding: 10px; font-size: 18px;")


        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 10px; font-size: 18px;")


        forgot_password_button = QPushButton("Forgot Password?")
        forgot_password_button.clicked.connect(self.reset_password)  # Corrected this line
        forgot_password_button.setStyleSheet("""
        font-size: 16px;
        font-weight: bold;
        color: #333;
        background-color: transparent;
        border: none;
        padding: 5px;
        margin-top: 10px;
        """)
        forgot_password_button.setCursor(Qt.PointingHandCursor)


        login_button = QPushButton("Log In")
        login_button.clicked.connect(self.handle_login)
        login_button.setStyleSheet("""
        font-size: 20px;
        font-weight: bold;
        color: #fff;
        background-color: black;
        border: none;
        border-radius: 5px;
        padding: 10px;
        margin-top: 20px;
        """)
        login_button.setCursor(Qt.PointingHandCursor)


        back_button = QPushButton("Back")
        back_button.clicked.connect(self.go_back)
        back_button.setStyleSheet("""
        font-size: 20px;
        font-weight: bold;
        color: #fff;
        background-color: black;
        border: none;
        border-radius: 5px;
        padding: 10px;
        margin-top: 10px;
        """)
        back_button.setCursor(Qt.PointingHandCursor)


        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(QLabel("Username (Email):"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)
        layout.addWidget(forgot_password_button)
        layout.addWidget(login_button)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()


        valid_username = re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', username)
        if not valid_username:
            QMessageBox.warning(self, "Invalid Input", "Invalid username. Please try again.")
            return


        user = fetch_query("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))

        if user:
            QMessageBox.information(self, "Login Successful", f"Welcome back, {username}!")
        else:
            QMessageBox.critical(self, "Login Failed", "Invalid username or password. Please try again.")

    def go_back(self):
        self.stacked_widget.setCurrentIndex(0)

    def reset_password(self):
        reset_password = UserVerify(self.stacked_widget)
        self.stacked_widget.addWidget(reset_password)
        self.stacked_widget.setCurrentWidget(reset_password)



