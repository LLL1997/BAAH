import os,datetime,subprocess,time
import functools
from datetime import datetime
import logging

# 用来检查是否在限定时间，否则不执行
def time_restriction(*args:tuple[int,int,int,int]):
    '''参考调用@time_restriction((12, 00, 00, 50),(12, 00, 16, 50))'''
    times = args
    if len(args)==0:
        return False    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = datetime.now()
            # 获取当前的小时和分钟
            current_hour , current_minute = now.hour , now.minute
            # 检查当前时间是否在限定时间内
            def _check_time():
                for x in times:
                    start_hour, start_minute, end_hour, end_minute = int(x[0]), int(x[1]), int(x[2]), int(x[3])
                    if 0 <= start_hour < 24 and 0 < end_hour < 24 and 0 <= start_minute < 60 and 0 <= end_minute < 60: # 检测时间格式
                        pass
                    else:
                        logging.info("时间参数不正确")
                        return False
                    if start_hour <= current_hour < end_hour or (start_hour == current_hour and current_minute >= start_minute) or (current_hour == end_hour and current_minute <= end_minute):
                        logging.info(f"Function {func.__name__} 在限定时间内{start_hour}:{start_minute} 到 {end_hour}:{end_minute}，执行")
                        return True
                    else:
                        logging.info(f"Function {func.__name__} 不在限定时间内{start_hour}:{start_minute} 到 {end_hour}:{end_minute}，不执行")
                return False
            if _check_time():
                return func(*args, **kwargs)  # 在限定时间内，执行函数
            else:
                return None
        return wrapper
    return decorator
@time_restriction((12, 00, 23, 50),(12, 00, 19, 50))
def Daily_loop_control():
    print("asdasf")
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
    
    #用来做每日报告（
    def __init__(self) -> None:
        pass
    
        #res = ocr_area((901, 88), (989, 123))
        #print("Tab栏识别结果: ", res)
    #         ocr_str = ocr_area((122, 179), (165, 211))[0]
    # if ocr_str == "":
    #     return False
    # # 如果字符串无法识别为数字，返回false
    # try:
    #     now_num = int(ocr_str)
    # except ValueError:
    #     return False
    


if __name__ == '__main__':
    pass
    Daily_loop_control()
    # os._exit(0)
    #close_emulator('D:/Program Files/Netease/MuMuPlayer-12.0/shell/','MuMuPlayer.exe' , 3)