from concurrent.futures import ThreadPoolExecutor

from apscheduler.schedulers.blocking import BlockingScheduler

from config import log_config
from core.login_checkin import LoginCheckin
from utils.file_tools import FileTools
from utils.user import User

logger = log_config.set_logger()


def batch_checkin():
    """批量并发执行所有用户的签到任务"""
    try:
        file_tools = FileTools()
        user_data = file_tools.read_file()

        if not user_data:
            logger.info("无可用用户，请先添加用户！")
            return

        logger.info(f"开始处理 {len(user_data)} 个用户的签到任务")

        # 使用线程池控制并发数
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for email, password in user_data.items():
                user = User(email=email, password=password)
                processor = LoginCheckin()
                futures.append(executor.submit(processor.execute, user))

            # 收集结果并记录日志
            for future in futures:
                result = future.result()
                email = result.get('email', '未知用户')  # 安全获取 email
                if 'msg' in result:
                    logger.info(f"签到成功 - 用户: {email} - 消息: {result['msg']}")
                elif 'error' in result:
                    logger.error(f"签到失败 - 用户: {email} - 错误: {result['error']}")
                else:
                    logger.warning(f"未知响应 - 用户: {email} - 响应内容: {result}")

    except Exception as e:
        logger.error(f"批量签到异常: {str(e)}", exc_info=True)


scheduler = BlockingScheduler()
