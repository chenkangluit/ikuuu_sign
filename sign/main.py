import argparse

from apscheduler.schedulers.blocking import BlockingScheduler

from config import log_config
from config.setting import data_path, key_path
from utils import create_key, task
from utils.file_tools import FileTools


def main():
    parser = argparse.ArgumentParser(description="自动登录和签到程序")
    parser.add_argument("--time", type=str, help="指定签到时间（格式 'HH:MM' 例如 '22:00'），不指定则立即执行")
    parser.add_argument("--config", action="store_true", help="写入用户配置到 JSON 文件")
    parser.add_argument("--email", type=str, help="用户邮箱")
    parser.add_argument("--password", type=str, help="用户密码")
    args = parser.parse_args()

    # 初始化日志
    logger = log_config.set_logger()

    # 生成密钥（仅在首次运行时创建）
    if FileTools.check_file_empty(key_path):
        create_key.create_key()

    # 全局调度器实例
    scheduler = BlockingScheduler()

    # 处理配置写入
    if args.config:
        if not args.email or not args.password:
            logger.error("必须提供 --email 和 --password 参数！")
            return

        try:
            file_tools = FileTools()
            user_data = {}
            if not file_tools.check_file_empty(data_path):
                user_data = file_tools.read_file()

                if args.email in user_data:
                    logger.warning(f"用户已存在: {args.email}")
                    return

            user_data[args.email] = args.password
            file_tools.write_file(user_data)
            logger.info(f"用户配置已保存: {args.email}")
        except Exception as e:
            logger.error(f"配置文件操作失败: {str(e)}")
            return

    # 执行签到逻辑
    if args.time:
        try:
            hour, minute = map(int, args.time.split(':'))
            scheduler.add_job(task.batch_checkin, 'cron', hour=hour, minute=minute)
            logger.info(f"定时任务已设置，每天 {args.time} 执行签到")
            scheduler.start()
        except ValueError:
            logger.error("时间格式错误，请使用 'HH:MM' 格式（例如 '08:30'）")
        except Exception as e:
            logger.error(f"定时任务设置失败: {str(e)}")
    else:
        if not FileTools.check_file_empty(data_path):
            task.batch_checkin()
        else:
            logger.info("还没有添加用户")


if __name__ == "__main__":
    main()
