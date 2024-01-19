import subprocess
import schedule,time
def daily():
    print("每日")
    # 指定要运行的 Python 脚本
    try:
        script_path = "main.py"
        process=subprocess.Popen(["python", script_path])
        process.wait()
    except subprocess.CalledProcessError as e:
        print(f"命令执行错误，退出码：{e.returncode}")
        print(f"命令输出：{e.output}")
def Touch_Head(config_file_path):
    try:
        print("摸头")
        baah_path = "main.py "
        command = f"python {baah_path} {config_file_path}"
        subprocess.run(command)
    except subprocess.CalledProcessError as e:
        print(f"命令执行错误，退出码：{e.returncode}")
        print(f"命令输出：{e.output}")

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
    json_config_file_path = 'config_only_touch_head.json'# 专门用来摸头，参数填写只摸头的json配置文件名
    
    Touch_Head1=Touch_Head(json_config_file_path) 
    #daily() # 日常清体力用，使用默认的config
    daily_loop()

    while True:
        schedule.run_pending()
        time.sleep(30)