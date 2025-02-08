import argparse
import logging
import time
import config
import schedule

from login_checkin import LoginCheckin, User
from file_tools import FileTools

# # 配置全局日志格式
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S"
# )
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="自动登录和签到程序")
    parser.add_argument("--time", type=str, help="指定签到时间，例如 '22:00'。不指定则立即签到。")
    parser.add_argument("--config", action="store_true", help="写入用户配置到 JSON 文件")
    parser.add_argument("--email", type=str, help="用户邮箱")
    parser.add_argument("--password", type=str, help="用户密码")
    args = parser.parse_args()

    if args.config:
        if not args.email or not args.password:
            logger.error("必须提供用户邮箱和密码！")
            return

        try:
            file_tools = FileTools()
            user_data = file_tools.read_file()

            if args.email not in user_data:
                user_data[args.email] = args.password
                file_tools.create_file(user_data)
                logger.info(f"用户配置已保存 - Email: {args.email}")
            else:
                logger.warning(f"用户已存在 - Email: {args.email}")
        except Exception as e:
            logger.error(f"配置文件操作失败: {str(e)}")
            return

    try:
        file_tools = FileTools()
        user_data = file_tools.read_file()

        if not user_data:
            logger.error("配置文件为空，请先添加用户！")
            return

        logger.info(f"发现 {len(user_data)} 个待处理用户")

        for email, password in user_data.items():
            user = User(email=email, password=password)
            processor = LoginCheckin()

            if args.time:
                schedule.every().day.at(args.time).do(lambda: processor.execute(user))
                logger.info(f"定时任务已设置 - 时间: {args.time} - 用户: {email}")
            else:
                result = processor.execute(user)
                if "msg" in result:
                    logger.info(f"签到成功 - 用户: {email} - 消息: {result['msg']}")
                elif "error" in result:
                    logger.error(f"操作失败 - 用户: {email} - 错误: {result['error']}")
                else:
                    logger.warning(f"未知响应 - 用户: {email} - 响应内容: {result}")

    except Exception as e:
        logger.error(f"主程序运行异常: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()