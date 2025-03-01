import logging
from typing import Optional, Dict, Any

import requests

from config.setting import login_url, checkin_url, default_headers
from utils.user import User


class LoginCheckin:
    """登录签到处理器"""

    def __init__(
            self,
            login_url: str = login_url,
            checkin_url: str = checkin_url,
            headers: Optional[Dict[str, str]] = None
    ):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.LOGIN_URL = login_url
        self.CHECKIN_URL = checkin_url
        self.HEADERS = headers or self._default_headers()

    @staticmethod
    def _default_headers() -> Dict[str, str]:
        """返回默认请求头"""
        return default_headers

    def _create_session(self) -> requests.Session:
        """创建并配置会话对象"""
        session = requests.Session()
        session.headers.update(self.HEADERS)
        return session

    def login(self, user: User) -> Optional[requests.Session]:
        """执行登录操作"""
        session = self._create_session()
        try:
            payload = {
                "email": user.email,
                "passwd": user.password,
                "code": ""
            }

            self.logger.debug("尝试登录用户: %s", user.email)
            response = session.post(
                self.LOGIN_URL,
                data=payload,
                timeout=15
            )
            response.raise_for_status()

            if not self._validate_login(session):
                self.logger.error("登录验证失败")
                return None

            self.logger.info("%s 登录成功", user.email)
            return session

        except requests.exceptions.RequestException as e:
            self.logger.error("登录请求失败: %s", str(e))
        except Exception as e:
            self.logger.exception("登录时发生意外错误: %s", str(e))
        return None

    @staticmethod
    def _validate_login(session: requests.Session) -> bool:
        """验证登录是否成功"""
        return "uid" in session.cookies.get_dict()

    def checkin(self, session: requests.Session) -> Dict[str, Any]:
        """执行签到操作"""
        try:
            self.logger.debug("开始签到流程")
            response = session.post(
                self.CHECKIN_URL,
                timeout=15
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error("签到请求失败: %s", str(e))
            return {"error": str(e)}
        except ValueError:
            self.logger.error("响应解析失败，原始内容: %s", response.text)
            return {"error": "Invalid JSON response"}
        except Exception as e:
            self.logger.exception("签到时发生意外错误: %s", str(e))
            return {"error": str(e)}

    def execute(self, user: User) -> Dict[str, Any]:
        """完整执行登录+签到流程"""
        if session := self.login(user):
            if result := self.checkin(session):
                return result
        return {"error": "流程执行失败"}
