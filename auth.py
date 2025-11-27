import hashlib
from database import Database


class AuthManager:
    def __init__(self):
        self.db = Database()

    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password, role='user'):
        """Register a new user"""
        if self.db.get_user(username):
            return False, "Username already exists"

        password_hash = self.hash_password(password)

        if self.db.add_user(username, password_hash, role):
            return True, "User registered successfully"
        else:
            return False, "Registration failed"

    def login_user(self, username, password):
        """Authenticate user"""
        user = self.db.get_user(username)
        if not user:
            return False, "User not found", None

        password_hash = self.hash_password(password)

        if user[2] == password_hash:  # password_hash is at index 2
            user_data = {
                'id': user[0],
                'username': user[1],
                'role': user[3],
                'public_key': user[4],
                'private_key': user[5]
            }
            return True, "Login successful", user_data
        else:
            return False, "Invalid password", None

    def is_admin(self, user_data):
        """Check if user is admin"""
        return user_data and user_data.get('role') == 'admin'