from config import log_config
from utils.crypto_tools import CryptoTools


def create_key():
    key_logger = log_config.set_logger()
    key = CryptoTools.generate_key()
    CryptoTools.save_key(key)
    key_logger.info('密钥创建成功。')
