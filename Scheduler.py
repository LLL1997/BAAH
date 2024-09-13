import os,time
import schedule
import threading
import subprocess 
import concurrent.futures
import glob

from datetime import datetime

from modules.add_functions.msg import push_msg_fast
from modules.utils.move_window import move_windows, window_in_virtual_desktop_and_move_to


def daily_task(): 
    '''
    需要在congfig.json里设置下一个json,单线程链式运行config,输出状态到cli
    '''
    try:
        print("每日日常任务,单线程执行")
        push_msg_fast('碧蓝档案，每日日常开始')
        script_path = "main.py"
        process=subprocess.Popen(["python", script_path])
        process.wait() # 等待完成
        print("执行成功")
    except subprocess.CalledProcessError as e:
        print(f"命令输出：{e.output}")
        print(f"命令执行错误，退出码：{e.returncode}")
    else:
        print("执行成功")
        push_msg_fast('碧蓝档案，每日日常结束')

def start_script_and_load_json(json_config_file_path,task_name):
    try:
        this_time=datetime.now().strftime('%Y年%m月%d日%H时%M分%S秒')
        print('运行'+json_config_file_path+'配置文件，在'+this_time+'任务类型: '+task_name)
        baah_path = "main.py "
        command = f"python {baah_path} {json_config_file_path}" 
        log_file = f"./log/{this_time}-{str(json_config_file_path)}_运行中.txt"
        # 执行命令并将输出重定向到日志文件
        result =subprocess.run(command, shell=True, stdout=open(log_file, "w"), stderr=subprocess.STDOUT)
        if result.returncode != 0:
            raise Exception(f"Python脚本执行出错，返回码：{result.returncode}")
    except subprocess.CalledProcessError as e:
        print(f"命令执行错误，退出码：{e.returncode}")
        print(f"命令输出：{e.output}")
    except Exception as e:
        # 捕捉到异常后的处理逻辑
        print(f"发生异常：{e}")
        try:
            error_log_file=f"./log/{this_time}-{str(json_config_file_path)}_运行错误.txt"
            os.rename(log_file, error_log_file)
            print(f'捕捉到异常的错误日志，保存为'+error_log_file)
        except OSError as e:
            print(f"修改日志名时发生错误：{e}")
    else: # 未报错用os命令删除掉log文件
        remove_file(log_file)
def remove_file(file_path):
    try:
        os.remove(file_path)
        print(f"{file_path}运行完成")
    except OSError as e:
        print(f"删除文件时发生错误：{e}")

def multi_threaded_task(config_list:list=["config.json",],max_threads:int=2,task_name:str=None):
    '''多线程运行config ,错误日志保存到/log 同模拟器设置链式防止错误(在config里设置下一个运行的json配置文件)'''

    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
        [executor.submit(lambda :start_script_and_load_json(x,task_name)) for x in config_list]

    push_msg_fast(f'碧蓝档案，{task_name}完成')
    print(f'碧蓝档案，{task_name}完成')

    files_to_delete = glob.glob(os.path.join('/log', '*"运行中"*'))
    # 遍历文件列表并删除每个文件包含运行中字段的文件
    for file_path in files_to_delete:
        try:
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        except OSError as e:
            print(f"Error: {file_path} - {e.strerror}")
def multi_daily_task(config_tuple:tuple):
    '''清体力和其他'''
    push_msg_fast('碧蓝档案，每日日常开始')
    print("每日清体力和其他 in "+datetime.now().strftime('%Y年%m月%d日%H时%M分'))
    multi_threaded_task(config_tuple,task_name='每日')

def multi_threaded_touch_head_task(config_tuple):
    '''摸头'''
    push_msg_fast('碧蓝档案，摸头开始')
    print("执行摸头 in "+datetime.now().strftime('%Y年%m月%d日%H时%M分'))
    multi_threaded_task(config_tuple,task_name='摸头')

def setup_daily_tasks(fun,time:tuple,config:tuple | list):
    [schedule.every().day.at(x).do(fun,tuple(config)) for x in time]
def check_emulator_VD():
    '''检查模拟器所在的桌面，不在桌面3就移动到桌面3'''
    while True:
        move_windows()
        move_windows('MAA')
        move_windows('py.exe')
        # window_in_virtual_desktop_and_move_to('MAA')
        # window_in_virtual_desktop_and_move_to('py.exe')
        # window_in_virtual_desktop_and_move_to('模拟器')
        time.sleep(20)

if __name__ == '__main__':
    # 定义一个子线程，用来检测模拟器所在的桌面，发现不在桌面3就移动到桌面3
    t0 = threading.Thread(target=check_emulator_VD)
    t0.start()
    # multi_daily_task()
    multi_daily_task(('config.json','config_JP.json','config_EN.json'))
    #multi_threaded_touch_head_task(('bilibili_只摸头.json','日服_只摸头.json','国际服_只摸头.json'))
    setup_daily_tasks(fun=multi_daily_task,
                      time=['04:30','20:30'],
                      config=['config.json','config_JP.json','config_EN.json'],
                      )
    setup_daily_tasks(fun=multi_threaded_touch_head_task,
                      time=['04:00','07:30','11:00','14:30','16:00','19:30','23:00','02:30'],
                      config=('bilibili_只摸头.json','日服_只摸头.json','国际服_只摸头.json'),
                      )

    while True:
        # if not t0.is_alive():t0.start()
        schedule.run_pending()
        time.sleep(60)
