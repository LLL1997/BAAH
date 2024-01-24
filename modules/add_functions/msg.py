import configparser
import os

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
            'content': f'时间：{datetime.now().strftime("%Y年%m月%d日%H时%M分%S秒")}\n' + content,
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
        if 'ok' in html_str:
            print('钉钉BOT消息发送成功')
            return True
        else:
            print('钉钉BOT消息发送失败')
            return False
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: {e}")
    except requests.exceptions.Timeout as e:
        print("The request timed out.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return False
def push_msg_fast(text):
    import asyncio
    ini_file_path = "BAAH_CONFIGS\msg.ini"
    config = read_ini_file(ini_file_path)

    # 从配置文件中获取消息
    url = config.get('Message', 'url', fallback=None)
    at_phone_number = config.get('Message', '@手机号', fallback=None)

    asyncio.run(push_msg(url,text,at_phone_number))
if __name__ == "__main__":
    push_msg_fast("游戏，grewgw")

