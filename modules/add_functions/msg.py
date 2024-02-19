import configparser
import os
import requests
from datetime import datetime

class IniFile:

    def __init__(self, file_path):
        self.file_path = file_path
        self.config = configparser.ConfigParser()
        if not os.path.exists(file_path):
            self.create_ini_file()
        else:
            with open(file_path, 'r', encoding='utf-8') as config_file:
                self.config.read_file(config_file)
        #self.config.read(file_path)

    def create_ini_file(self):
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
        with open(self.file_path, 'w') as config_file:
            config.write(config_file)
            print(f"Configuration file {self.file_path} created.")

    def get_value(self, section, option):
        '''
        获取配置文件中指定节和选项的值
        :param section: 节
        :param option: 选项
        :return: 值
        '''
        return self.config.get(section, option,fallback=None)

    # 设置数据
    def set_value(self, section, option, value, save_to_file=True):
        # 设置指定节、指定选项的值
        self.config.set(section, option, value)
        # 如果save_to_file为True，则保存到文件
        if save_to_file:
            with open(self.file_path, 'w',encoding='utf-8') as file:
                self.config.write(file)

    def add_section(self, section):
        '''
        添加新的section
        :param section: section名称
        :return:
        '''
        self.config.add_section(section)
        with open(self.file_path, 'w',encoding='utf-8') as file:
            self.config.write(file)

    def remove_section(self, section):
        # 移除指定section
        self.config.remove_section(section)
        # 打开文件
        with open(self.file_path, 'w',encoding='utf-8') as file:
            # 将配置写入文件
            self.config.write(file)

    def remove_option(self, section, option):
        # 移除指定节和选项的配置
        self.config.remove_option(section, option)
        # 打开文件，写入配置
        with open(self.file_path, 'w',encoding='utf-8') as file:
            self.config.write(file)


async def push_msg(url, content, title=None,phone_number=''):
    '''
    :param url：要推送的网站
    :param content：要推送的消息内容
    :param phone_number：要推送的电话号码，默认为空,钉钉才有
    :param title:微信息知用
    '''
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
    if title is not None:
        json_data =  {
         'title': title,
        'content': content
    }
    try:
        response = requests.post(url, json=json_data, headers=headers, timeout=10)
        html_str = response.text
        return html_str
    
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: {e}")
    except requests.exceptions.Timeout as e:
        print("The request timed out.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return False

def push_msg_fast_Dingtalk(text):
    '''钉钉消息'''
    import asyncio
    # 从配置文件中获取消息
    try:
        Myini=IniFile('BAAH_CONFIGS\config.ini')
        url = Myini.get_value('Message', 'url')
        at_phone_number = Myini.get_value('Message', '@手机号',)
        asyncio.run(push_msg(url,text,phone_number=at_phone_number))
        return True
    except Exception as e:
        print(e)
        return False

def push_msg_fast_xizhi(text):
    '''微信息知'''
    import asyncio
    # 从配置文件中获取消息
    try:
        Myini=IniFile('BAAH_CONFIGS\config.ini')
        url = Myini.get_value('Message', 'xizhi_url')
        text = str(text)

        asyncio.run(push_msg(url,text,title=text))
        return True
    except Exception as e:
        print(e)
        return False
def push_msg_fast(text):
    return push_msg_fast_Dingtalk(text) and push_msg_fast_xizhi(text)
    
if __name__ == "__main__":
    push_msg_fast_Dingtalk("已经在运行了")
    push_msg_fast_xizhi("BAAH🥰，已经在运行了😊")
    push_msg_fast("游戏 2222")
