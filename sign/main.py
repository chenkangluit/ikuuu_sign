import argparse
import logging
import time
import config
import schedule

from login_checkin import LoginCheckin, User
from file_tools import FileTools


def main():
    parser = argparse.ArgumentParser(description="自动登录和签到程序")
    parser.add_argument("--time", type=str, help="指定签到时间，例如 '22:00'。不指定则立即签到。")
    parser.add_argument("--config", action="store_true", help="写入用户配置到 JSON 文件")
    parser.add_argument("--email", type=str, help="用户邮箱")
    parser.add_argument("--password", type=str, help="用户密码")
    args = parser.parse_args()

    if args.config:
        if not args.email or not args.password:
            print("请提供用户邮箱和密码！")
            return

        # 保存到配置文件
        file_tools = FileTools()
        user_data = file_tools.read_file()

        # 如果文件中没有这个用户，则添加
        if args.email not in user_data:
            user_data[args.email] = args.password
            file_tools.create_file(user_data)
            print(f"{args.email} 配置已保存到文件")
        else:
            print(f"{args.email} 已存在于配置文件中")

    # 读取配置文件中的用户信息
    file_tools = FileTools()
    user_data = file_tools.read_file()

    if not user_data:
        print("配置文件为空，请先添加用户！")
        return

    for email, password in user_data.items():
        user = User(email=email, password=password)
        processor = LoginCheckin()

        if args.time:
            # 设置定时任务
            schedule.every().day.at(args.time).do(lambda: processor.execute(user))
            print(f"已设置每日 {args.time} 自动签到")

        else:
            # 立即签到
            result = processor.execute(user)
            if "msg" in result:
                print(f"{email} 签到结果: {result['msg']}")
            elif "error" in result:
                print(f"{email} 操作失败: {result['error']}")
            else:
                print(f"{email} 收到未知响应: {result}")


if __name__ == "__main__":
    main()
