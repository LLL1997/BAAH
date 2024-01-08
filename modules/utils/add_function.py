import os,datetime,subprocess,time
from typing import Any
from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area

def close_emulator(path,file_name,mumu_num=None)->None:
    ''' 关闭模拟器'''
    # 烦死了 只用mumu算了
    current_dir = os.getcwd()
    def CallCMD(cmd_command):
        try:
            completed_process = subprocess.check_output(
                cmd_command, 
                shell=True,
                text=True  # 让输出以文本形式返回而不是字节形式
            )

            return completed_process
        except subprocess.CalledProcessError as e:
            print("命令执行失败:", e)
            return "error"
    

    path=str(path)
    file_name=str(file_name)
    os.chdir(path)
    callable('ls')
    print(mumu_num,'mumu_num')
    if file_name=='MuMuPlayer.exe':
        if mumu_num !=None:
            cmd3 = f"MuMuManager.exe api -v {mumu_num}  shutdown_player "
            CallCMD(cmd3)
            print(cmd3)
            time.sleep(5)
            os.chdir(current_dir)
            callable('ls')
            return
        else:
            cmd3 = "MuMuManager.exe api -v 0 shutdown_player "
            CallCMD(cmd3)
            print(cmd3)
            time.sleep(5)
            os.chdir(current_dir)
            callable('ls')
            return
    # cmdStr = "cd /d "+ path + f" & {file_name} quitall"
    # # cmdStr = "cd /d "+"LeiDianDir"+" & dnconsole.exe quitall"
    # # print("cmdstr",cmdStr)
    # os.system(cmdStr)
        
    os.chdir(current_dir)


async def push_msg(url, content, phone_number=''):
    '''发送钉钉bot消息
    asyncio.run(push_msg())
    https://open.dingtalk.com/document/robots/custom-robot-access
    '''
    import datetime,json,requests,urllib
    from urllib.error import URLError, HTTPError

    no_proxy_handler = urllib.request.ProxyHandler({})
    opener = urllib.request.build_opener(no_proxy_handler)
    headers = {
    'Content-Type': 'application/json',
}
    
    try:
        now = datetime.datetime.now()
        json_data = {
            'msgtype': 'text',
            'text': {
                'content': f'时间：{now}\n' + content,
            },
            "at": {
                "atMobiles": [
                    phone_number
                ],
            },
        }
        data = json.dumps(json_data).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers)
        response = opener.open(req, timeout=10)
        html_str = response.read().decode('utf-8')
        print(html_str)
        return html_str
    except HTTPError as e:
        print(f"HTTP Error: {e.code}")
    except URLError as e:
        print(f"URL Error: {e.reason}")
    except TimeoutError:
        print("The request timed out.")
        push_msg(url, content, phone_number)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def Daily_loop_control():
    pass
# 用携程来运行代码，通过时间来判断是否出错，超时触发TimeoutError异常

# 错误日志
def log_error(message):
    log_file_path = "error_log.txt"

    # 检查日志文件是否存在，如果不存在则创建
    if not os.path.exists(log_file_path):
        with open(log_file_path, 'w') as file:
            file.write("Error Log created on {}\n".format(datetime.now()))

    # 在日志文件中写入数据
    with open(log_file_path, 'a') as file:
        file.write("{}: {}\n".format(datetime.now(), message))
class _:
    pass
class ocr_store:
    ''' ocr资源数量'''
    def __init__(self) -> None:
        pass
    
        res = ocr_area((901, 88), (989, 123))
        print("Tab栏识别结果: ", res)

if __name__ == '__main__':
    pass
    # os._exit(0)
    close_emulator('D:/Program Files/Netease/MuMuPlayer-12.0/shell/','MuMuPlayer.exe' , 3)