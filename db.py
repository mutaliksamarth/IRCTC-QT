import sqlite3

class Database:
    def __init__(self):
        # Connect to the database
        self.conn = sqlite3.connect("auth.db")
        self.create_user_table()

    def create_user_table(self):
        # Create a table to store user data
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            auth_question TEXT NOT NULL,
            auth_answer TEXT NOT NULL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def register_user(self, username, password, question, answer):
        try:
            query = "INSERT INTO users (username, password, auth_question, auth_answer) VALUES (?, ?, ?, ?)"
            self.conn.execute(query, (username, password, question, answer))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def validate_login(self, username, password):
        query = "SELECT * FROM users WHERE username=? AND password=?"
        cursor = self.conn.execute(query, (username, password))
        return cursor.fetchone()

    def get_auth_question(self, username):
        query = "SELECT auth_question FROM users WHERE username=?"
        cursor = self.conn.execute(query, (username,))
        result = cursor.fetchone()
        return result[0] if result else None

    def validate_auth_answer(self, username, answer):
        query = "SELECT * FROM users WHERE username=? AND auth_answer=?"
        cursor = self.conn.execute(query, (username, answer))
        return cursor.fetchone()

    def change_password(self, username, new_password):
        query = "UPDATE users SET password=? WHERE username=?"
        self.conn.execute(query, (new_password, username))
        self.conn.commit()
