iKuuu VPN 自动签到工具
Python Version
License

一款安全可靠的自动化签到工具，支持iKuuu VPN服务的定时批量签到操作。

官网登录 | 问题反馈

🌟 功能亮点
自动化签到：支持指定时间自动执行签到任务
批量操作：可同时管理多个账户的签到流程
安全存储：采用AES加密技术保护账户凭证
灵活配置：支持即时执行或定时任务模式
跨平台：兼容Windows/Linux/macOS系统
📦 安装指南
克隆仓库：
bash
git clone https://github.com/yourusername/ikuuu-auto-sign.git
cd ikuuu-auto-sign
安装依赖：
bash
pip install -r requirements.txt
🚀 快速开始
单次签到模式
bash
python main.py --email your@email.com --password your_password
定时任务模式（每天22:00执行）
bash
python main.py --time 22:00
配置账户信息（加密存储）
bash
python main.py --config --email your@email.com --password your_password
⚙️ 参数说明
参数	说明	示例值
--time	设置定时执行时间（HH:MM格式）	22:00
--config	进入账户配置模式	无
--email	登录邮箱地址	user@domain.com
--password	账户密码	********
🔒 安全机制
账户凭证使用AES-256-CBC加密存储
配置文件路径：configs/user_config.json
密钥独立存储在系统安全区域
🔄 定时任务配置
Linux/macOS（crontab）
bash
0 22 * * * cd /path/to/ikuuu-auto-sign && /usr/bin/python3 main.py --time 22:00
Windows任务计划
创建基本任务
设置每日触发时间
操作配置：
程序：pythonw.exe
参数：main.py --time 22:00
📌 注意事项
首次使用请先执行配置命令
确保系统时间与所在时区一致
Python 3.7+ 运行环境要求
保持网络连接正常
建议在服务器环境下运行长期任务
🤝 贡献指南
欢迎通过Issue提交问题或PR贡献代码：

Fork本项目
创建功能分支（git checkout -b feature/AmazingFeature）
提交修改（git commit -m 'Add some AmazingFeature'）
推送分支（git push origin feature/AmazingFeature）
发起Pull Request
📧 技术支持：your-support@example.com
🔗 项目地址：https://github.com/yourusername/ikuuu-auto-sign
📄 许可协议：MIT LICENSE

请勿将本工具用于任何违反服务条款的用途，使用前请确认iKuuu VPN的相关政策。