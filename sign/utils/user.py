from dataclasses import dataclass


@dataclass
class User:
    """用户账户信息"""
    email: str
    password: str
