
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt
from db import fetch_query, execute_query
import re


class UserVerify(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.init_ui()

    def init_ui(self):
        title = QLabel("Reset Password")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 30px; font-weight: bold; color: #333;")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username (email)")
        self.verify_button = QPushButton("Verify")
        self.verify_button.clicked.connect(self.verify_email)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(self.username_input)
        layout.addWidget(self.verify_button)
        self.setLayout(layout)

    def verify_email(self):
        username = self.username_input.text()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", username):
            QMessageBox.warning(self, "Invalid Email", "Please enter a valid email address.")
            return

        user = fetch_query("SELECT * FROM users WHERE username = ?", (username,))
        if not user:
            QMessageBox.warning(self, "Not Found", "Email not found.")
            return

        auth_verify = AuthVerify(self.stacked_widget, username)
        self.stacked_widget.addWidget(auth_verify)
        self.stacked_widget.setCurrentWidget(auth_verify)


class AuthVerify(QWidget):
    def __init__(self, stacked_widget, username):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.username = username
        self.init_ui()

    def init_ui(self):
        user = fetch_query("SELECT auth_question FROM users WHERE username = ?", (self.username,))
        if not user:
            QMessageBox.critical(self, "Error", "User not found.")
            return
        self.security_question = user[0]

        title = QLabel("Security Question")
        question_label = QLabel(f"What is your {self.security_question}?")
        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText("Enter your answer")

        verify_button = QPushButton("Verify")
        verify_button.clicked.connect(self.verify_answer)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(question_label)
        layout.addWidget(self.answer_input)
        layout.addWidget(verify_button)
        self.setLayout(layout)

    def verify_answer(self):
        answer = self.answer_input.text()
        user = fetch_query("SELECT * FROM users WHERE username = ? AND auth_answer = ?", (self.username, answer))
        if not user:
            QMessageBox.warning(self, "Incorrect", "Invalid answer.")
            return

        reset_password = ResetPassword(self.stacked_widget, self.username)
        self.stacked_widget.addWidget(reset_password)
        self.stacked_widget.setCurrentWidget(reset_password)


class ResetPassword(QWidget):
    def __init__(self, stacked_widget, username):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.username = username
        self.init_ui()

    def init_ui(self):
        title = QLabel("Reset Your Password")
        self.new_password = QLineEdit()
        self.new_password.setPlaceholderText("Enter new password")
        self.confirm_password = QLineEdit()
        self.confirm_password.setPlaceholderText("Confirm new password")

        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset_password)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(self.new_password)
        layout.addWidget(self.confirm_password)
        layout.addWidget(reset_button)
        self.setLayout(layout)


    def reset_password(self):
        password = fetch_query("SELECT password FROM users WHERE username = ?",(self.username,) )

        if password[0] == self.new_password.text():
            QMessageBox.information(self, "Failed", "New password cannot be the same as the previous password.")
            return

        if self.new_password.text() != self.confirm_password.text():
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return

        if len(self.new_password.text()) < 6:
            QMessageBox.warning(self, "Error", "Password should be at least 6 characters long.")
            return

        execute_query("UPDATE users SET password = ? WHERE username = ?", (self.new_password.text(), self.username))
        QMessageBox.information(self, "Success", "Password updated successfully.")
        self.stacked_widget.setCurrentIndex(0)




        
