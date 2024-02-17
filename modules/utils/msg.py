import configparser
import os
import asyncio
import smtplib
from email.mime.text import MIMEText

def read_ini_file(file_path):
    config = configparser.ConfigParser()

    # 检查配置文件是否存在，如果不存在则创建
    if not os.path.exists(file_path):
        print(f"{file_path} not found. Creating a new one.")
        create_ini_file(file_path)

    # 读取配置文件
    config.read(file_path)
    return config

def create_ini_file(file_path):
    config = configparser.ConfigParser()
    
    # 获取用户输入
    url = input("输入bot链接: ")
    if url == "":
        url = input("输入bot链接: ")

    at_phone_number = input("@手机号（包含才发送,可回车跳过")
    # 设置配置项
    config['Message'] = {'url': url,
                         '@手机号': at_phone_number
                         }
    # 写入配置文件
    with open(file_path, 'w') as config_file:
        config.write(config_file)
        print(f"Configuration file {file_path} created.")
def smtp_m(smtp_server, smtp_port, email, password):
    pass
async def push_msg(url, content, phone_number=''):
    '''发送钉钉bot消息
        asyncio.run(push_msg())
        https://open.dingtalk.com/document/robots/custom-robot-access'''
    import requests
    from datetime import datetime
    headers = {
        'Content-Type': 'application/json',
    }
    json_data = {
        'msgtype': 'text',
        'text': {
            'content': f'时间：{datetime.now()}\n' + content,
        },
        "at": {
            "atMobiles": [
                phone_number
            ],
        },
    }
    try:
        response = requests.post(url, json=json_data, headers=headers, timeout=10)
        html_str = response.text
        print(html_str)
        return html_str
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: {e}")
    except requests.exceptions.Timeout as e:
        print("The request timed out.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def push_msg_fast(text):

    ini_file_path = "msg.ini"
    config = read_ini_file(ini_file_path)

    # 从配置文件中获取消息
    url = config.get('Message', 'url', fallback=None)
    at_phone_number = config.get('Message', '@手机号', fallback=None)

    asyncio.run(push_msg(url,text,at_phone_number))
def push_mail():
    # TODO 待实现整合到代码中 ，1，分离数据和逻辑 2.整合到gui中
    # 邮件有点慢，需要10秒左右来发送
    
    # server

    smtp_server = 'smtp.qq.com'
    smtp_port = 587
    smtp_user = '297278093@qq.com'
    smtp_password = ''

    # 设置发件人、收件人和邮件主题
    sender = '297278093@qq.com'
    receiver = '297278093@qq.com'
    subject = '测试' # 标题
    body = '测试文本.'

    # 创建MIMEText对象
    msg = MIMEText(body, 'plain')
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject

    # 连接SMTP服务器并发送邮件
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # 启用安全传输模式
        server.login(smtp_user, smtp_password)
        server.sendmail(sender, receiver, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        server.quit()

if __name__ == "__main__":
    #push_msg_fast("游戏，grewgw")
    push_mail()
