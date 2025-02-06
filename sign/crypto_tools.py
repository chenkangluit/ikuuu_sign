from cryptography.fernet import Fernet
import base64
import os


class CryptoTools:
    """用于密码加密和解密"""

    @staticmethod
    def generate_key() -> bytes:
        """生成加密密钥并保存"""
        return Fernet.generate_key()

    @staticmethod
    def save_key(key: bytes, key_path: str = 'secret.key'):
        """保存密钥到文件"""
        with open(key_path, 'wb') as key_file:
            key_file.write(key)

    @staticmethod
    def load_key(key_path: str = 'secret.key') -> bytes:
        """从文件加载密钥"""
        return open(key_path, 'rb').read()

    @staticmethod
    def encrypt_password(password: str, key: bytes) -> str:
        """加密密码"""
        fernet = Fernet(key)
        encrypted_password = fernet.encrypt(password.encode())
        return encrypted_password.decode()

    @staticmethod
    def decrypt_password(encrypted_password: str, key: bytes) -> str:
        """解密密码"""
        fernet = Fernet(key)
        decrypted_password = fernet.decrypt(encrypted_password.encode())
        return decrypted_password.decode()
