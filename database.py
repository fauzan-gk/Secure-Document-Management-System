import sqlite3
import os
from datetime import datetime


class Database:
    def __init__(self, db_name="sdms.db"):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        """Create and return database connection"""
        return sqlite3.connect(self.db_name)

    def init_db(self):
        """Initialize database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                public_key TEXT,
                private_key TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Documents table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_hash TEXT NOT NULL,
                encrypted_key TEXT NOT NULL,
                owner_id INTEGER NOT NULL,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (owner_id) REFERENCES users (id)
            )
        ''')

        # Document shares table for access control
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS document_shares (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                shared_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (document_id) REFERENCES documents (id),
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(document_id, user_id)
            )
        ''')

        conn.commit()
        conn.close()

    def add_user(self, username, password_hash, role='user', public_key=None, private_key=None):
        """Add a new user to the database"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO users (username, password_hash, role, public_key, private_key)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, password_hash, role, public_key, private_key))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def get_user(self, username):
        """Get user by username"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        return user

    def get_user_by_id(self, user_id):
        """Get user by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()

        return user

    def add_document(self, filename, file_path, file_hash, encrypted_key, owner_id):
        """Add a new document to the database"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO documents (filename, file_path, file_hash, encrypted_key, owner_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (filename, file_path, file_hash, encrypted_key, owner_id))

        document_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return document_id

    def get_document(self, document_id):
        """Get document by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM documents WHERE id = ?', (document_id,))
        document = cursor.fetchone()
        conn.close()

        return document

    def get_user_documents(self, user_id):
        """Get all documents owned by a user"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM documents 
            WHERE owner_id = ? 
            ORDER BY uploaded_at DESC
        ''', (user_id,))

        documents = cursor.fetchall()
        conn.close()

        return documents

    def share_document(self, document_id, user_id):
        """Share a document with another user"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO document_shares (document_id, user_id)
                VALUES (?, ?)
            ''', (document_id, user_id))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def get_shared_documents(self, user_id):
        """Get documents shared with a user"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT d.*, u.username as owner_name 
            FROM documents d
            JOIN document_shares ds ON d.id = ds.document_id
            JOIN users u ON d.owner_id = u.id
            WHERE ds.user_id = ?
            ORDER BY ds.shared_at DESC
        ''', (user_id,))

        documents = cursor.fetchall()
        conn.close()

        return documents

    def update_user_keys(self, username, public_key, private_key):
        """Update user's RSA keys"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE users 
            SET public_key = ?, private_key = ? 
            WHERE username = ?
        ''', (public_key, private_key, username))

        conn.commit()
        conn.close()