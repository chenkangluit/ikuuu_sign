import requests
import schedule
import time
import argparse


# URL 和请求头
LOGIN_URL = "https://ikuuu.one/auth/login"
CHECKIN_URL = "https://ikuuu.one/user/checkin"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://ikuuu.one",
    "Referer": "https://ikuuu.one/auth/login",
}


def login_and_checkin(email, password):
    """
    登录并签到函数
    :param email: 用户邮箱
    :param password: 用户密码
    """
    session = requests.Session()
    try:
        # 登录请求
        print("正在登录...")
        user_credentials = {
            "email": email,
            "passwd": password,
            "code": ""  # 验证码（如果不需要可以留空）
        }
        login_response = session.post(LOGIN_URL, data=user_credentials, headers=HEADERS)
        if login_response.status_code == 200 and "uid" in login_response.cookies:
            print("登录成功！")
        else:
            print("登录失败，请检查账号和密码！")
            return

        # 签到请求
        print("正在签到...")
        checkin_response = session.post(CHECKIN_URL, headers=HEADERS, cookies=login_response.cookies)
        if checkin_response.status_code == 200:
            result = checkin_response.json()
            print("签到结果:", result.get("msg", "未知结果"))
        else:
            print("签到失败，请稍后重试。")
    except Exception as e:
        print(f"发生错误: {e}")


def main():
    # 命令行参数解析
    parser = argparse.ArgumentParser(description="Ikuuu 自动签到程序")
    parser.add_argument("--email", required=True, help="登录用的邮箱地址")
    parser.add_argument("--password", required=True, help="登录用的密码")
    parser.add_argument("--time", default="22:00", help="签到时间（默认每天晚上 22:00）")
    args = parser.parse_args()

    # 添加定时任务
    schedule.every().day.at(args.time).do(login_and_checkin, email=args.email, password=args.password)

    # 主循环
    print(f"自动签到程序已启动，签到时间为每天 {args.time}...")
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
