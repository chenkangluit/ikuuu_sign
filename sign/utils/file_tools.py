import json
import logging
import os

from config.setting import data_path, key_path
from utils.crypto_tools import CryptoTools


class FileTools:
    """文件操作工具类"""

    def __init__(self, data_path: str = data_path, key_path: str = key_path):
        self.data_path = data_path
        self.key_path = key_path

    def read_file(self) -> dict:
        """读取配置文件并解密密码"""
        if not self.check_file_empty(self.data_path):
            try:
                with open(self.data_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                # 解密密码
                key = CryptoTools.load_key(self.key_path)
                for email, encrypted_password in data.items():
                    data[email] = CryptoTools.decrypt_password(encrypted_password, key)

                return data
            except FileNotFoundError:
                logging.error("文件不存在，返回空字典")
                return {}

    def write_file(self, user_data: dict):
        """将加密的用户数据写入 JSON 文件"""
        try:
            key = CryptoTools.load_key(self.key_path)
            encrypted_data = {
                email: CryptoTools.encrypt_password(password, key)
                for email, password in user_data.items()
            }

            with open(self.data_path, 'w', encoding='utf-8') as file:
                json.dump(encrypted_data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            logging.error(f"写入文件时出错: {e}")

    @staticmethod
    def check_file_exists(file_path: str) -> object:
        """
        检查文件是否存在
        :return:
            True - 文件存在
            False - 文件不存在
        """
        if os.path.exists(file_path):
            return True  # 文件不存在
        else:
            return False  # 文件存在

    @staticmethod
    def check_file_empty(file_path: str) -> object:
        """
        检查文件是否为空
        :return:
            True - 文件为空
            False - 文件不为空
        """
        if os.path.getsize(file_path) == 0:
            return True  # 文件为空
        else:
            return False  # 文件非空
