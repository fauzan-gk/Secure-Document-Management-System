import os
from auth import AuthManager
from document_manager import DocumentManager
from crypto import CryptoManager
from database import Database


class CLI:
    def __init__(self):
        self.auth = AuthManager()
        self.doc_manager = DocumentManager()
        self.crypto = CryptoManager()
        self.db = Database()
        self.current_user = None

    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self, title):
        """Print formatted header"""
        print("\n" + "=" * 50)
        print(f" {title}")
        print("=" * 50)

    def register(self):
        """User registration"""
        self.print_header("USER REGISTRATION")

        username = input("Username: ")
        password = input("Password: ")  # Changed from getpass
        confirm_password = input("Confirm Password: ")  # Changed from getpass

        if password != confirm_password:
            print("Error: Passwords do not match!")
            return

        success, message = self.auth.register_user(username, password)
        print(f"\n{message}")

        if success:
            # Generate RSA keys for new user
            public_key, private_key = self.crypto.generate_rsa_keypair()
            self.db.update_user_keys(username, public_key.decode('utf-8'), private_key.decode('utf-8'))
            print("RSA key pair generated successfully!")

    def login(self):
        """User login"""
        self.print_header("USER LOGIN")

        username = input("Username: ")
        password = input("Password: ") 

        success, message, user_data = self.auth.login_user(username, password)

        if success:
            self.current_user = user_data
            print(f"\n{message}")
            print(f"Welcome, {username}!")
            if self.auth.is_admin(user_data):
                print("You have admin privileges.")
        else:
            print(f"\n{message}")

        if success:
            # Generate RSA keys for new user
            public_key, private_key = self.crypto.generate_rsa_keypair()
            self.db.update_user_keys(username, public_key.decode('utf-8'), private_key.decode('utf-8'))
            print("RSA key pair generated successfully!")

    def login(self):
        """User login"""
        self.print_header("USER LOGIN")

        username = input("Username: ")
        password = input("Password: ")

        success, message, user_data = self.auth.login_user(username, password)

        if success:
            self.current_user = user_data
            print(f"\n{message}")
            print(f"Welcome, {username}!")
            if self.auth.is_admin(user_data):
                print("You have admin privileges.")
        else:
            print(f"\n{message}")

    def upload_document(self):
        """Upload a document"""
        if not self.current_user:
            print("Please login first!")
            return

        self.print_header("UPLOAD DOCUMENT")

        file_path = input("Enter file path: ")

        if not os.path.exists(file_path):
            print("Error: File not found!")
            return

        success, message = self.doc_manager.upload_document(
            file_path,
            self.current_user['id'],
            self.current_user['public_key'].encode('utf-8')
        )

        print(f"\n{message}")

    def download_document(self):
        """Download a document"""
        if not self.current_user:
            print("Please login first!")
            return

        self.print_header("DOWNLOAD DOCUMENT")

        # List user's documents
        documents = self.doc_manager.list_user_documents(self.current_user['id'])
        shared_docs = self.doc_manager.list_shared_documents(self.current_user['id'])

        if not documents and not shared_docs:
            print("No documents available for download.")
            return

        print("\nYour Documents:")
        for doc in documents:
            print(f"ID: {doc[0]}, Filename: {doc[1]}, Uploaded: {doc[6]}")

        print("\nShared Documents:")
        for doc in shared_docs:
            print(f"ID: {doc[0]}, Filename: {doc[1]}, Owner: {doc[7]}, Shared: {doc[6]}")

        try:
            doc_id = int(input("\nEnter Document ID to download: "))
            success, message = self.doc_manager.download_document(
                doc_id,
                self.current_user['private_key'].encode('utf-8')
            )
            print(f"\n{message}")
        except ValueError:
            print("Error: Please enter a valid Document ID!")

    def share_document(self):
        """Share a document with another user"""
        if not self.current_user:
            print("Please login first!")
            return

        self.print_header("SHARE DOCUMENT")

        documents = self.doc_manager.list_user_documents(self.current_user['id'])

        if not documents:
            print("You have no documents to share.")
            return

        print("\nYour Documents:")
        for doc in documents:
            print(f"ID: {doc[0]}, Filename: {doc[1]}")

        try:
            doc_id = int(input("\nEnter Document ID to share: "))
            target_user = input("Enter username to share with: ")

            success, message = self.doc_manager.share_document_with_user(
                doc_id, self.current_user['id'], target_user
            )
            print(f"\n{message}")
        except ValueError:
            print("Error: Please enter a valid Document ID!")

    def list_documents(self):
        """List user's documents"""
        if not self.current_user:
            print("Please login first!")
            return

        self.print_header("MY DOCUMENTS")

        documents = self.doc_manager.list_user_documents(self.current_user['id'])
        shared_docs = self.doc_manager.list_shared_documents(self.current_user['id'])

        print("\nDocuments You Own:")
        if documents:
            for doc in documents:
                print(f"ID: {doc[0]}, Filename: {doc[1]}, Hash: {doc[3][:16]}..., Uploaded: {doc[6]}")
        else:
            print("No documents found.")

        print("\nDocuments Shared With You:")
        if shared_docs:
            for doc in shared_docs:
                print(f"ID: {doc[0]}, Filename: {doc[1]}, Owner: {doc[7]}, Shared: {doc[6]}")
        else:
            print("No shared documents.")

    def admin_panel(self):
        """Admin functionality"""
        if not self.current_user or not self.auth.is_admin(self.current_user):
            print("Access denied: Admin privileges required!")
            return

        self.print_header("ADMIN PANEL")

        print("1. List All Users")
        print("2. List All Documents")
        print("3. Back to Main Menu")

        choice = input("\nEnter your choice: ")

        if choice == '1':
            self.list_all_users()
        elif choice == '2':
            self.list_all_documents()

    def list_all_users(self):
        """List all users (admin only)"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT id, username, role, created_at FROM users')
        users = cursor.fetchall()
        conn.close()

        print("\nAll Users:")
        for user in users:
            print(f"ID: {user[0]}, Username: {user[1]}, Role: {user[2]}, Created: {user[3]}")

    def list_all_documents(self):
        """List all documents (admin only)"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT d.id, d.filename, u.username, d.uploaded_at 
            FROM documents d 
            JOIN users u ON d.owner_id = u.id
            ORDER BY d.uploaded_at DESC
        ''')
        documents = cursor.fetchall()
        conn.close()

        print("\nAll Documents:")
        for doc in documents:
            print(f"ID: {doc[0]}, Filename: {doc[1]}, Owner: {doc[2]}, Uploaded: {doc[3]}")

    def logout(self):
        """Logout current user"""
        if self.current_user:
            print(f"Goodbye, {self.current_user['username']}!")
            self.current_user = None
        else:
            print("No user is currently logged in!")

    def run(self):
        """Main CLI loop"""
        while True:
            self.clear_screen()
            self.print_header("""SECURE DOCUMENT MANAGEMENT SYSTEM
                              Developed by: 
                                - Urooj Fatima [FA23-BCS-028]
                                - Dania Kazmi [FA23-BCS-032]
                                - Fauzan Gauhar Khan [FA23-BCS-037]""")

            if self.current_user:
                print(f"Logged in as: {self.current_user['username']} ({self.current_user['role']})")
                print("\n1. Upload Document")
                print("2. Download Document")
                print("3. Share Document")
                print("4. List My Documents")
                if self.auth.is_admin(self.current_user):
                    print("5. Admin Panel")
                print("6. Logout")
                print("7. Exit")
            else:
                print("1. Register")
                print("2. Login")
                print("3. Exit")

            choice = input("\nEnter your choice: ")

            if self.current_user:
                if choice == '1':
                    self.upload_document()
                elif choice == '2':
                    self.download_document()
                elif choice == '3':
                    self.share_document()
                elif choice == '4':
                    self.list_documents()
                elif choice == '5' and self.auth.is_admin(self.current_user):
                    self.admin_panel()
                elif choice == '6':
                    self.logout()
                elif choice == '7':
                    print("Thank you for using SDMS!")
                    break
                else:
                    print("Invalid choice!")
            else:
                if choice == '1':
                    self.register()
                elif choice == '2':
                    self.login()
                elif choice == '3':
                    print("Thank you for using SDMS!")
                    break
                else:
                    print("Invalid choice!")

            input("\nPress Enter to continue...")