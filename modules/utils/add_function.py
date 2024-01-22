import os,datetime,subprocess,time

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
    # os._exit(0)
    #close_emulator('D:/Program Files/Netease/MuMuPlayer-12.0/shell/','MuMuPlayer.exe' , 3)