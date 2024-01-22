import subprocess
import schedule,time
import threading
from datetime import datetime
from modules.add_functions.msg import push_msg_fast
json_config_file_path=''

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

def Touch_Head(json_config_file_path):
    try:
        print("摸头"+json_config_file_path+datetime.now().strftime('%Y年%m月%d日%H时%M分%S秒'))
        baah_path = "main.py "
        command = f"python {baah_path} {json_config_file_path}" 
        log_file = f"./log/{datetime.now().strftime('%Y年%m月%d日%H时%M分%S秒')}-{str(json_config_file_path)}.txt"
        # 执行命令并将输出重定向到日志文件
        subprocess.run(command, shell=True, stdout=open(log_file, "w"), stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print(f"命令执行错误，退出码：{e.returncode}")
        print(f"命令输出：{e.output}")

def Touch_Head1(xx=['bilibili_只摸头.json','日服_只摸头.json','国际服_只摸头.json'],wait_time=30):
    '''多线程'''
    push_msg_fast('碧蓝档案，摸头开始')
    threads = []
    for x in range(len(xx)):
        thread = threading.Thread(target=Touch_Head, args=(xx[x],))
        threads.append(thread)
        thread.start()
        time.sleep(wait_time)  # 控制线程之间的间隔

    # 等待所有线程完成
    for thread in threads:
        thread.join()
    push_msg_fast('碧蓝档案，摸头完成')
    print('碧蓝档案，摸头完成')

def daily_loop():
    schedule.every().day.at("04:00").do(Touch_Head1) # 4点全部刷新
    schedule.every().day.at("07:00").do(daily) 
    schedule.every().day.at("11:00").do(Touch_Head1)
    schedule.every().day.at("14:30").do(Touch_Head1)
    schedule.every().day.at("16:00").do(Touch_Head1)
    schedule.every().day.at("19:30").do(daily) # 领取体力进行日常
    schedule.every().day.at("23:00").do(Touch_Head1)
    schedule.every().day.at("02:30").do(Touch_Head1) # 刷新前摸一次头

if __name__ == '__main__':

    Touch_Head1()
    # daily() # 日常清体力用，使用默认的config
    daily_loop()

    while True:
        schedule.run_pending()
        time.sleep(30)