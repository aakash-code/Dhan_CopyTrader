import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

class EncryptionManager:
    """Manages encryption and decryption of API tokens"""
    
    def __init__(self):
        load_dotenv()
        key = os.environ.get('key')
        if key:
            self.fernet = Fernet(key.encode())
        else:
            raise Exception("Encryption key not found in environment variables")
    
    def encrypt_token(self, token):
        """Encrypt a token"""
        if isinstance(token, str):
            token = token.encode()
        return self.fernet.encrypt(token).decode()
    
    def decrypt_token(self, encrypted_token):
        """Decrypt a token"""
        if isinstance(encrypted_token, str):
            encrypted_token = encrypted_token.encode()
        return self.fernet.decrypt(encrypted_token).decode()