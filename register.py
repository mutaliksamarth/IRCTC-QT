from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
import sys
from db import fetch_query, execute_query
import re
from login import LoginForm

class Registration(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setWindowTitle("Sign Up")
        self.init_ui()

    def init_ui(self):
        title = QLabel("Sign Up to IRCTC")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 100px; font-weight: bold; color: #333; margin-bottom: 20px;")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your email")
        self.username_input.setStyleSheet("padding: 20px; font-size: 26px;")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 20px; font-size: 26px;")

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm your password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet("padding: 20px; font-size: 26px;")

        self.auth_question_input = QLineEdit()
        self.auth_question_input.setPlaceholderText("Enter your security question")
        self.auth_question_input.setStyleSheet("padding: 20px; font-size: 26px;")

        self.auth_answer_input = QLineEdit()
        self.auth_answer_input.setPlaceholderText("Enter your security answer")
        self.auth_answer_input.setStyleSheet("padding: 20px; font-size: 26px;")

        signup_button = QPushButton("Sign Up")
        signup_button.clicked.connect(self.handle_signup)
        signup_button.setStyleSheet("""
        font-size: 30px;
        font-weight: bold;
        color: #fff;
        background-color: black;
        border: none;
        border-radius: 5px;
        padding: 10px;
        margin-top: 20px;
        """)
        signup_button.setCursor(Qt.PointingHandCursor)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.go_back)
        back_button.setStyleSheet("""
        font-size: 20px;
        font-weight: bold;
        color: #fff;
        background-color: gray;
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
        layout.addWidget(QLabel("Confirm Password:"))
        layout.addWidget(self.confirm_password_input)
        layout.addWidget(QLabel("Security Question:"))
        layout.addWidget(self.auth_question_input)
        layout.addWidget(QLabel("Security Answer:"))
        layout.addWidget(self.auth_answer_input)
        layout.addWidget(signup_button)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def handle_signup(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        auth_question = self.auth_question_input.text()
        auth_answer = self.auth_answer_input.text()

        if not re.match(r"[^@]+@[^@]+\.[^@]+", username):
            QMessageBox.critical(self, "Error", "Invalid email address")
            return

        if len(password) < 8:
            QMessageBox.critical(self, "Error", "Password must be at least 8 characters long")
            return

        if password != confirm_password:
            QMessageBox.critical(self, "Error", "Passwords do not match")
            return

        if len(auth_question) == 0:
            QMessageBox.critical(self, "Error", "Security question cannot be empty")
            return

        if len(auth_answer) == 0:
            QMessageBox.critical(self, "Error", "Security answer cannot be empty")
            return

        user = fetch_query("SELECT * FROM users WHERE username=?", (username,))
        if user:
            QMessageBox.critical(self, "Error", "User already exists")
            self.reset_form()
            return

        try:
            execute_query("INSERT INTO users (username, password, auth_question, auth_answer) VALUES (?, ?, ?, ?)", (username, password, auth_question, auth_answer))
            QMessageBox.information(self, "Success", "User registered successfully")
            self.stacked_widget.setCurrentIndex(0)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self.reset_form()

    def go_back(self):
        self.stacked_widget.setCurrentIndex(0)

    def reset_form(self):
        self.username_input.setText("")
        self.password_input.setText("")
        self.confirm_password_input.setText("")
        self.auth_question_input.setText("")
        self.auth_answer_input.setText("")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Registration()
    window.show()
    app.exec_()