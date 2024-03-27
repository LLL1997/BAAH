import subprocess
from modules.configs.MyConfig import config
import logging
from modules.utils.subprocess_helper import subprocess_run
import time
import numpy as np
import cv2

def getNewestSeialNumber(use_config=None):
    # 如果传入指定的配置文件，就使用指定的配置文件
    target_config = config
    if use_config:
        target_config = use_config
    # 从配置文件里得到最新的模拟器IP和端口
    if target_config.userconfigdict["TARGET_PORT"] and target_config.userconfigdict["TARGET_IP_PATH"]:
        return "{}:{}".format(target_config.userconfigdict["TARGET_IP_PATH"],target_config.userconfigdict["TARGET_PORT"])
    else:
        logging.error("TARGET_IP_PATH或TARGET_PORT未设置")
        logging.warn("使用默认值：127.0.0.1:5555")
        return "127.0.0.1:5555"
    
def get_config_adb_path(use_config=None):
    target_config = config
    # 如果传入指定的配置文件，就使用指定的配置文件
    if use_config:
        target_config = use_config
    return target_config.userconfigdict['ADB_PATH']

# 判断是否有TARGET_PORT这个配置项
def disconnect_this_device():
    """Disconnect this device."""
    subprocess_run([get_config_adb_path(), "disconnect", getNewestSeialNumber()])
    
def kill_adb_server():
    """Kill the adb server."""
    subprocess_run([get_config_adb_path(), "kill-server"])
    subprocess_run([get_config_adb_path(), "start-server"])

def connect_to_device(use_config=None):
    """Connect to a device with the given device port."""
    if use_config:
        subprocess_run([get_config_adb_path(use_config), "connect", getNewestSeialNumber(use_config)])
    else:
        subprocess_run([get_config_adb_path(), "connect", getNewestSeialNumber()])
    
def click_on_screen(x, y):
    """Click on the given coordinates."""
    subprocess_run([get_config_adb_path(), "-s", getNewestSeialNumber(), "shell", "input", "tap", str(int(x)), str(int(y))])

def swipe_on_screen(x1, y1, x2, y2, ms):
    """Swipe from the given coordinates to the other given coordinates."""
    subprocess_run([get_config_adb_path(), "-s", getNewestSeialNumber(), "shell", "input", "swipe", str(int(x1)), str(int(y1)), str(int(x2)), str(int(y2)), str(int(ms))])

def convert_img(path):
    with open(path, "rb") as f:
        bys = f.read()
        bys_ = bys.replace(b"\r\n",b"\n")  # 二进制流中的"\r\n" 替换为"\n"
    with open(path, "wb") as f:
        f.write(bys_)

def screen_shot_to_global(use_config=None):
    """Take a screenshot and save it to the GlobalState."""
    target_config = config
    if use_config:
        target_config = use_config
    # 方法一，重定向输出到文件
    filename = target_config.userconfigdict['SCREENSHOT_NAME']
    with open("./{}".format(filename),"wb") as out:
       subprocess_run([get_config_adb_path(target_config), "-s", getNewestSeialNumber(target_config), "shell", "screencap", "-p"], stdout=out)
    #adb 命令有时直接截图保存到电脑出错的解决办法-加下面一段即可
    convert_img("./{}".format(filename))
    
    # 方法二，使用cv2提取PIPE管道中的数据
    
    # # 使用subprocess的Popen调用adb shell命令，并将结果保存到PIPE管道中
    # process = subprocess.run([get_config_adb_path(), "-s", getNewestSeialNumber(), "shell", "screencap", "-p"], stdout=subprocess.PIPE)
    # # 读取管道中的数据
    # screenshot = process.stdout
    # # 将读取的字节流数据的回车换行替换成'\n'
    # binary_screenshot = screenshot.replace(b'\r\n', b'\n')
    # # 使用numpy和imdecode将二进制数据转换成cv2的mat图片格式
    # img_screenshot = cv2.imdecode(np.frombuffer(binary_screenshot, np.uint8), cv2.IMREAD_COLOR)
    # cv2.imwrite("./{}".format(config.userconfigdict['SCREENSHOT_NAME']), img_screenshot)
    
def get_now_running_app(use_config=None):
    """
    获取当前运行的app
    """
    if use_config:
        output = subprocess_run([get_config_adb_path(use_config), "-s", getNewestSeialNumber(use_config), 'shell', 'dumpsys', 'window']).stdout
    else:
        output = subprocess_run([get_config_adb_path(), "-s", getNewestSeialNumber(), 'shell', 'dumpsys', 'window']).stdout
    # adb shell "dumpsys window | grep mCurrentFocus"
    for sentence in output.split("\n"):
        if "mCurrentFocus" in sentence:
            # 找到当前运行的app那行
            output = sentence
            if "null" in output:
                #logging.warn("MUMU模拟器需要设置里关闭保活！")
                return output
            break
    # 截取app activity
    try:
        app_activity = output.split(" ")[-1].split("}")[0]
    except Exception as e:
        logging.warn("截取当前运行的app名失败：{}".format(output))
        return output
    return app_activity

def check_app_running(activity_path:str) -> bool:
    """
    检查app是否在运行
    """
    try:
        app_name = activity_path.split("/")[0]
    except Exception as e:
        logging.error("activity_path格式错误")
        return False
    # 获取当前运行的app
    output = get_now_running_app()
    logging.info("当前运行的app是：{}".format(output))
    if app_name in output:
        return True
    else:
        return False
    
def open_app(activity_path:str):
    """
    使用adb打开app
    """
    subprocess_run([get_config_adb_path(), "-s", getNewestSeialNumber(), 'shell', 'am', 'start', activity_path], isasync=True)
    appname = activity_path.split("/")[0]
    subprocess_run([get_config_adb_path(), "-s", getNewestSeialNumber(), 'shell', 'monkey', '-p', appname, '1'], isasync=True)

def close_app(activity_path:str):
    """
    使用adb关闭app
    """
    subprocess_run([get_config_adb_path(), "-s", getNewestSeialNumber(), 'shell', 'am', 'start', '-s',activity_path])
    time.sleep(2)
    subprocess_run([get_config_adb_path(), "-s", getNewestSeialNumber(), 'shell', 'am', 'force-stop', activity_path], isasync=True)
    time.sleep(2)
    appname = activity_path.split("/")[0]
    subprocess_run([get_config_adb_path(), "-s", getNewestSeialNumber(), 'shell', 'force-stop', appname])
    time.sleep(2)
    subprocess_run([get_config_adb_path(), "-s", getNewestSeialNumber(), 'shell', 'am', 'kill', appname])
    time.sleep(2)
    subprocess_run([get_config_adb_path(), "-s", getNewestSeialNumber(), 'shell', 'am', 'kill-all'])