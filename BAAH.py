import sys
import os


# 将当前脚本所在目录添加到模块搜索路径
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_dir)

import logging
from modules.configs.MyConfig import config
from modules.utils import *
from modules.AllTask.myAllTask import my_AllTask
from modules.add_functions.add_function import *
from modules.add_functions.msg import push_msg_fast
def BAAH_release_adb_port(justDoIt=False):
    """
    释放adb端口，通常被一个后台进程占用
    """
    if config.userconfigdict["KILL_PORT_IF_EXIST"] or justDoIt:
        try:
            # 确保端口未被占用
            res=subprocess_run(["netstat", "-ano"], encoding="gbk").stdout
            for line in res.split("\n"):
                if ":"+str(config.userconfigdict["TARGET_PORT"]) in line : # 有假占用，去除掉试试 and "LISTENING" in line
                    logging.info(line)
                    logging.info("端口被占用，正在释放")
                    pid=line.split()[-1]
                    subprocess_run(["taskkill", "/T", "/F", "/PID", pid], encoding="gbk")
                    logging.info("端口被占用，已释放")
                    config.sessiondict["PORT_IS_USED"]=True
                    break
        except Exception as e:
            logging.error("释放端口失败，请关闭模拟器后重试")
            logging.error(e)
def _check_process_exist(pid):
    """
    检查进程是否存在
    """
    try:
        tasks = subprocess_run(["tasklist"], encoding="gbk").stdout
        tasklist = tasks.split("\n")
        for task in tasklist:
            wordlist = task.strip().split()
            if len(wordlist) > 1 and wordlist[1] == str(pid):
                logging.info(" | ".join(wordlist))
                return True
        return False
    except Exception as e:
        logging.error(e)
        return False

def BAAH_start_emulator():
    """
    启动模拟器
    """
    if config.userconfigdict["TARGET_EMULATOR_PATH"] and config.userconfigdict["TARGET_EMULATOR_PATH"] != "":
        try:
            # 以列表形式传命令行参数
            logging.info("启动模拟器")
            emulator_process = subprocess_run(config.userconfigdict['TARGET_EMULATOR_PATH'].split(" "), isasync=True)
            logging.info("模拟器pid: "+str(emulator_process.pid))
            time.sleep(5)
            # 检查pid是否存在
            if not _check_process_exist(emulator_process.pid):
                logging.warn("模拟器启动进程已结束，可能是启动失败，或者是模拟器已经在运行")
            else:
                # 存进session，这样最后根据需要按照这个pid杀掉模拟器
                config.sessiondict["EMULATOR_PROCESS_PID"]=emulator_process.pid
        except Exception as e:
            logging.error("启动模拟器失败, 可能是没有以管理员模式运行 或 配置的模拟器路径有误")
            logging.error(e)
    else:
        logging.info("未配置模拟器路径，跳过启动模拟器")

def BAAH_check_adb_connect():
    """
    检查adb连接
    """
    # 检查adb连接
    
    disconnect_this_device()
    for i in range(1, 20):
        sleep(i)
        if check_connect():
            logging.info("adb连接成功")
            return True
        elif i == 8 or i == 16:
            if i==16:
                kill_adb_server()
            BAAH_restart_emulator()
        else:
            logging.info("未检测到设备连接, 重试...")
    if config.sessiondict["PORT_IS_USED"]:
        # 连接失败，并且出现端口被占用的情况，现在模拟器的用户可见进程的端口估计是配置文件里的后一个端口
        # 提醒用户启动BAAH时，不要启动模拟器
        raise Exception("检测到启动BAAH前 端口已被占用，但BAAH无法连接至该端口。上次模拟器可能未被正常关闭，请在启动BAAH前关闭模拟器")
    raise Exception("adb连接失败, 请检查配置里的adb端口")

def BAAH_open_target_app():
    """
    打开游戏
    """
    if check_app_running(config.userconfigdict['ACTIVITY_PATH']):
        logging.info("检测到游戏已经在运行")
        return True
    open_app(config.userconfigdict['ACTIVITY_PATH'])
    time.sleep(30)
    if check_app_running(config.userconfigdict['ACTIVITY_PATH']):
        logging.info("检测到游戏已经在运行")
        return True
    for i in range(10,87):
        logging.info("打开游戏")
        open_app(config.userconfigdict['ACTIVITY_PATH'])
        sleep(i)
        if check_app_running(config.userconfigdict['ACTIVITY_PATH']) == False:
            open_app(config.userconfigdict['ACTIVITY_PATH'])
            time.sleep(i)
        else:
            return True
        # 处理打开闪退的问题，尝试重启模拟器
        if i%22==0:
            BAAH_restart_emulator()
            BAAH_check_adb_connect()
    raise Exception("未检测到游戏打开，请检查区服设置 以及 如果使用的是MuMu模拟器，请关闭后台保活")

def BAAH_kill_emulator():
    """
    杀掉模拟器的用户可见窗口进程
    """
    if config.userconfigdict["TARGET_EMULATOR_PATH"] and config.userconfigdict["TARGET_EMULATOR_PATH"] != "" and config.userconfigdict["CLOSE_EMULATOR_BAAH"]:
        try:
            if not config.sessiondict["EMULATOR_PROCESS_PID"]:
                logging.error("未能获取到模拟器进程，跳过关闭模拟器")
                from modules.add_functions.msg import push_msg_fast
                push_msg_fast("碧蓝档案,BAAH未能获取到模拟器进程"+config.userconfigdict['SERVER_TYPE'])
                return
            # 提取出模拟器的exe名字
            full_path = config.userconfigdict['TARGET_EMULATOR_PATH']
            emulator_exe=os.path.basename(full_path).split(".exe")[0]+".exe"
            subprocess_run(["taskkill", "/T", "/F", "/PID", str(config.sessiondict["EMULATOR_PROCESS_PID"])], encoding="gbk")
            # 杀掉模拟器可见窗口进程后，可能残留后台进程，这里根据adb端口再杀一次
            BAAH_release_adb_port(justDoIt=True)
        except Exception as e:
            logging.error("关闭模拟器失败, 可能是没有以管理员模式运行 或 配置的模拟器路径有误")
            logging.error(e)
            from modules.add_functions.msg import push_msg_fast
            push_msg_fast("碧蓝档案,BAAH关闭模拟器失败"+config.userconfigdict['SERVER_TYPE'])
    else:
        logging.info("跳过关闭模拟器")

def BAAH_restart_emulator():
    '''
    重启模拟器
    '''
    BAAH_kill_emulator()
    sleep(5)
    BAAH_release_adb_port()
    sleep(5)
    BAAH_start_emulator()
    sleep(30)

def BAAH_main():
    try:
        if check_connect(): 
            logging.info("检测到设备已连接，跳过连接设备")
        else:
            BAAH_release_adb_port()
            BAAH_start_emulator()
            time.sleep(30)# 考虑渣机，稍微等下          
            BAAH_check_adb_connect()
        BAAH_open_target_app()
        # 运行任务
        logging.info("运行任务")
        my_AllTask.run()
    except Exception as e:
        from modules.add_functions.msg import push_msg_fast
        if e.args[0] == "找到维护弹窗，退出":
            push_msg_fast("碧蓝档案,"+config.userconfigdict['SERVER_TYPE']+'服务器维护')
            # raise Exception("找到维护弹窗，退出")
        else:
            push_msg_fast("碧蓝档案,BAAH运行出错"+config.userconfigdict['SERVER_TYPE'])
            print(e)
            # input("运行出错，按回车退出")
            raise Exception("运行出错")
            
    finally:
        time.sleep(3)
        BAAH_kill_emulator()
        logging.info(f"{config.userconfigdict['SERVER_TYPE']}任务结束")


if __name__ in ["__main__", "__mp_main__"]:
    # 不带GUI运行
    BAAH_main()