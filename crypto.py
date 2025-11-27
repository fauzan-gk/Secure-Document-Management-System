import os
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64


class CryptoManager:
    def __init__(self):
        self.key_size = 2048  # RSA key size

    def generate_rsa_keypair(self):
        """Generate RSA public-private key pair"""
        key = RSA.generate(self.key_size)
        private_key = key.export_key()
        public_key = key.publickey().export_key()

        return public_key, private_key

    def encrypt_with_rsa(self, public_key, data):
        """Encrypt data using RSA public key"""
        rsa_key = RSA.import_key(public_key)
        cipher = PKCS1_OAEP.new(rsa_key)
        encrypted_data = cipher.encrypt(data)
        return encrypted_data

    def decrypt_with_rsa(self, private_key, encrypted_data):
        """Decrypt data using RSA private key"""
        rsa_key = RSA.import_key(private_key)
        cipher = PKCS1_OAEP.new(rsa_key)
        decrypted_data = cipher.decrypt(encrypted_data)
        return decrypted_data

    def generate_aes_key(self):
        """Generate a random AES key (32 bytes for AES-256)"""
        return get_random_bytes(32)

    def encrypt_with_aes(self, data, aes_key):
        """Encrypt data using AES in CBC mode"""
        iv = get_random_bytes(16)  # Initialization vector
        cipher = AES.new(aes_key, AES.MODE_CBC, iv)

        # Pad data to be multiple of 16 bytes
        padded_data = pad(data, AES.block_size)
        encrypted_data = cipher.encrypt(padded_data)

        return iv + encrypted_data  # Prepend IV for decryption

    def decrypt_with_aes(self, encrypted_data, aes_key):
        """Decrypt data using AES"""
        iv = encrypted_data[:16]  # Extract IV
        actual_encrypted_data = encrypted_data[16:]

        cipher = AES.new(aes_key, AES.MODE_CBC, iv)
        decrypted_padded_data = cipher.decrypt(actual_encrypted_data)
        decrypted_data = unpad(decrypted_padded_data, AES.block_size)

        return decrypted_data

    def calculate_file_hash(self, file_path):
        """Calculate SHA-256 hash of a file"""
        sha256_hash = hashlib.sha256()

        with open(file_path, "rb") as f:
            # Read file in chunks to handle large files
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        return sha256_hash.hexdigest()

    def calculate_data_hash(self, data):
        """Calculate SHA-256 hash of data"""
        return hashlib.sha256(data).hexdigest()