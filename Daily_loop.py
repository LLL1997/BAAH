from main import *
import subprocess
import schedule,time
def _daily():
    print("每日")
    with open("main.py", "r",encoding="utf-8") as file:
        script_code = file.read()
        exec(script_code)
    # 指定要运行的 Python 脚本
    # script_path = "main.py"

    # # 使用 subprocess 运行脚本
    # subprocess.run(["python", script_path])


def daily_loop():
    schedule.every().day.at("02:00").do(_daily)
    # schedule.every().day.at("04:00").do(Touch_Head)
    schedule.every().day.at("07:00").do(_daily)
    # schedule.every().day.at("11:00").do(Touch_Head)
    # schedule.every().day.at("14:00").do(Touch_Head)
    # schedule.every().day.at("16:00").do(Touch_Head)
    schedule.every().day.at("19:00").do(_daily)
    # schedule.every().day.at("23:00").do(Touch_Head)
if __name__ == '__main__':
    # os._exit(0)
    # close_emulator('D:/Program Files/Netease/MuMuPlayer-12.0/shell/','MuMuPlayer.exe' , 3)

    # daily,Touch_Head=''

    _daily()


    while True:
        schedule.run_pending()
        time.sleep(600)