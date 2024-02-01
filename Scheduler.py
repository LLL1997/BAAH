import subprocess
import schedule,time
from datetime import datetime
from modules.add_functions.msg import push_msg_fast
import concurrent.futures
import os
def daily(): # 顺序执行
    print("每日")
    push_msg_fast('碧蓝档案，每日日常开始')
    # 指定要运行的 Python 脚本
    try:
        script_path = "main.py"
        process=subprocess.Popen(["python", script_path])
        process.wait()
    except subprocess.CalledProcessError as e:
        print(f"命令执行错误，退出码：{e.returncode}")
        print(f"命令输出：{e.output}")
    else:
        print("执行成功")
        push_msg_fast('碧蓝档案，每日日常结束')

def touch_Head(json_config_file_path):
    try:
        print("摸头"+json_config_file_path+datetime.now().strftime('%Y年%m月%d日%H时%M分%S秒'))
        baah_path = "main.py "
        command = f"python {baah_path} {json_config_file_path}" 
        log_file = f"./log/{datetime.now().strftime('%Y年%m月%d日%H时%M分%S秒')}-{str(json_config_file_path)}.txt"
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
    else: # 未报错用os命令删除掉log文件
        try:
            os.remove(log_file)
            print(f"运行未报错，删除文件 {log_file} 。")
        except OSError as e:
            print(f"删除文件时发生错误：{e}")


def process_touch_Head(xx=['bilibili_只摸头.json','日服_只摸头.json','国际服_只摸头.json'],max_threads=2):
    '''多线程'''
    push_msg_fast('碧蓝档案，摸头开始')
    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
        futures = {executor.submit(lambda x: touch_Head(x), x): x for x in xx}
        concurrent.futures.wait(futures)
    push_msg_fast('碧蓝档案，摸头完成')
    print('碧蓝档案，摸头完成')

def daily_loop():
    schedule.every().day.at("04:00").do(process_touch_Head) # 4点全部刷新
    schedule.every().day.at("04:30").do(daily) 
    schedule.every().day.at("07:30").do(process_touch_Head) 
    schedule.every().day.at("11:00").do(process_touch_Head)
    schedule.every().day.at("14:30").do(process_touch_Head)
    schedule.every().day.at("16:00").do(process_touch_Head)
    schedule.every().day.at("19:30").do(process_touch_Head)
    schedule.every().day.at("20:30").do(daily) # 领取体力进行日常
    schedule.every().day.at("23:00").do(process_touch_Head)
    schedule.every().day.at("02:30").do(process_touch_Head) # 刷新前摸一次头

if __name__ == '__main__':

    process_touch_Head() # 摸头
    # daily() # 日常清体力用，使用默认的config
    daily_loop()

    while True:
        schedule.run_pending()
        time.sleep(30)