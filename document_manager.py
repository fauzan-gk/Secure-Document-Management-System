import os
import base64
from database import Database
from crypto import CryptoManager


class DocumentManager:
    def __init__(self):
        self.db = Database()
        self.crypto = CryptoManager()
        self.upload_dir = "uploads"
        self.ensure_upload_dir()

    def ensure_upload_dir(self):
        """Create upload directory if it doesn't exist"""
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir)

    def upload_document(self, file_path, owner_id, owner_public_key):
        """Upload and encrypt a document"""
        if not os.path.exists(file_path):
            return False, "File not found"

        try:
            # Generate AES key for document encryption
            aes_key = self.crypto.generate_aes_key()

            # Read file content
            with open(file_path, 'rb') as f:
                file_data = f.read()

            # Encrypt file content with AES
            encrypted_data = self.crypto.encrypt_with_aes(file_data, aes_key)

            # Encrypt AES key with owner's RSA public key
            encrypted_aes_key = self.crypto.encrypt_with_rsa(owner_public_key, aes_key)

            # Calculate file hash for integrity verification
            file_hash = self.crypto.calculate_data_hash(file_data)

            # Save encrypted file
            filename = os.path.basename(file_path)
            encrypted_filename = f"encrypted_{filename}"
            encrypted_file_path = os.path.join(self.upload_dir, encrypted_filename)

            with open(encrypted_file_path, 'wb') as f:
                f.write(encrypted_data)

            # Store document metadata in database
            encrypted_key_b64 = base64.b64encode(encrypted_aes_key).decode('utf-8')
            document_id = self.db.add_document(
                filename, encrypted_file_path, file_hash, encrypted_key_b64, owner_id
            )

            return True, f"Document uploaded successfully (ID: {document_id})"

        except Exception as e:
            return False, f"Upload failed: {str(e)}"

    def download_document(self, document_id, user_private_key):
        """Download and decrypt a document"""
        document = self.db.get_document(document_id)
        if not document:
            return False, "Document not found"

        try:
            # Extract document data
            encrypted_file_path = document[2]  # file_path
            encrypted_key_b64 = document[4]  # encrypted_key
            original_filename = document[1]  # filename

            # Decode encrypted AES key
            encrypted_aes_key = base64.b64decode(encrypted_key_b64)

            # Decrypt AES key with user's RSA private key
            aes_key = self.crypto.decrypt_with_rsa(user_private_key, encrypted_aes_key)

            # Read encrypted file content
            with open(encrypted_file_path, 'rb') as f:
                encrypted_data = f.read()

            # Decrypt file content with AES
            decrypted_data = self.crypto.decrypt_with_aes(encrypted_data, aes_key)

            # Verify integrity
            calculated_hash = self.crypto.calculate_data_hash(decrypted_data)
            stored_hash = document[3]  # file_hash

            if calculated_hash != stored_hash:
                return False, "Integrity check failed: File may have been tampered with"

            # Save decrypted file to downloads directory
            download_dir = "downloads"
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)

            download_path = os.path.join(download_dir, f"decrypted_{original_filename}")
            with open(download_path, 'wb') as f:
                f.write(decrypted_data)

            return True, f"Document downloaded to: {download_path}"

        except Exception as e:
            return False, f"Download failed: {str(e)}"

    def share_document_with_user(self, document_id, owner_id, target_username):
        """Share a document with another user"""
        # Check if document exists and belongs to owner
        document = self.db.get_document(document_id)
        if not document or document[5] != owner_id:  # owner_id is at index 5
            return False, "Document not found or access denied"

        # Get target user
        target_user = self.db.get_user(target_username)
        if not target_user:
            return False, "Target user not found"

        # Share document
        if self.db.share_document(document_id, target_user[0]):  # user_id is at index 0
            return True, f"Document shared successfully with {target_username}"
        else:
            return False, "Document already shared with this user"

    def list_user_documents(self, user_id):
        """List all documents owned by user"""
        return self.db.get_user_documents(user_id)

    def list_shared_documents(self, user_id):
        """List all documents shared with user"""
        return self.db.get_shared_documents(user_id)