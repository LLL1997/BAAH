import subprocess
import schedule,time
def daily():
    print("每日")
    # with open("main.py", "r",encoding="utf-8") as file:
    #     script_code = file.read()
    #     exec(script_code)

    # 指定要运行的 Python 脚本
    script_path = "main.py"
    
    # for x in args:
    #     print(x)
    process=subprocess.Popen(["python", script_path])
    # config1="config.ini"
    # 使用 subprocess 运行脚本
    # process=subprocess.Popen(["python", script_path,config1])
    #process=subprocess.Popen(["python", script_path])
    process.wait()
def Touch_Head():
    print("摸头")
    script_path = "main.py "
    process=subprocess.Popen(["python", script_path, 'BAAH_CONFIGS/config_only_touch_head.json'],shell=True)
    process.wait()
def daily_loop():
    schedule.every().day.at("02:00").do(daily)
    # schedule.every().day.at("04:00").do(Touch_Head)
    schedule.every().day.at("07:00").do(daily)
    # schedule.every().day.at("11:00").do(Touch_Head)
    # schedule.every().day.at("14:00").do(Touch_Head)
    # schedule.every().day.at("16:00").do(Touch_Head)
    schedule.every().day.at("19:00").do(daily)
    schedule.every().day.at("22:00").do(daily)
    # schedule.every().day.at("23:00").do(Touch_Head)
if __name__ == '__main__':
    # Touch_Head()
    daily()
    daily_loop()


    while True:
        schedule.run_pending()
        time.sleep(30)