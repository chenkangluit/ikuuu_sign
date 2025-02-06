import json
import logging
from crypto_tools import CryptoTools


class FileTools:
    """文件操作工具类"""

    def __init__(self, file_path: str = 'data.json', key_path: str = 'secret.key'):
        self.file_path = file_path
        self.key_path = key_path

    def read_file(self) -> dict:
        """读取配置文件并解密密码"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # 解密密码
            key = CryptoTools.load_key(self.key_path)
            for email, encrypted_password in data.items():
                data[email] = CryptoTools.decrypt_password(encrypted_password, key)

            return data
        except FileNotFoundError:
            logging.warning("文件不存在，返回空字典")
            return {}
        except Exception as e:
            logging.error(f"读取文件时发生错误: {e}")
            return {}

    def create_file(self, user_data: dict):
        """将加密的用户数据写入 JSON 文件"""
        try:
            key = CryptoTools.load_key(self.key_path)
            encrypted_data = {
                email: CryptoTools.encrypt_password(password, key)
                for email, password in user_data.items()
            }

            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(encrypted_data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            logging.error(f"写入文件时出错: {e}")
