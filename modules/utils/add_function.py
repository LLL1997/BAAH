from DATA.assets.PageName import PageName
import os,datetime,subprocess,time
import functools
from datetime import datetime
import logging
from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, match_pixel,ocr_area
from modules.AllPage.Page import Page
from modules.AllTask.Task import Task
from modules.configs.MyConfig import config

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


    

class daily_report(Task):
    ''' 
    ocr资源数量
    通过检查红点和黄点和ocr实现
    '''
    YELLOW_POINT = ((8, 160, 250), (25, 200, 255))
    RED_POINT = ((15, 60, 250), (23, 72, 255))
    def __init__(self, name="daily_report") -> None:
        # super().__init__(name)
        self.on_run()
    #用来做每日报告（
    # def __init__(self) -> None:
    #     logging.info(self.ap_num())
    #     logging.info(self.gold_coins_num())
    #     logging.info(self.diamonds_num())

    # 用来执行其他函数，并统计返回
    def pre_condition(self) -> bool:
        return super().pre_condition()
    def on_run(self):
        # 创建一个字典，用来统计数据
        logging.info("开始执行统计")
        Task.back_to_home()
        data = {"ap":self.ap_num(),
                "gold_coins_num":self.gold_coins_num(),
                "diamonds_num":self.diamonds_num(),
                "total_assault":self.total_assault()
                
                }
        from modules.add_functions.msg import push_msg_fast
        from modules.configs.MyConfig import config
        push_msg_fast("碧蓝档案,BAAH"+'配置文件'+config.userconfigdict['SERVER_TYPE']+f'''
剩余体力{data["ap"]}

信用点{data["gold_coins_num"]}

清辉石{data["diamonds_num"]}

总力开启状态:{data["total_assault"][0]}
        
总力票数:+{data["total_assault"][1]}

总力开启时间:{data["total_assault"][2]}

                        ''')
        return data
    def post_condition(self) -> bool:
        return super().post_condition()
    def ocr(self,upper_left_point:tuple,lower_right_point:tuple)->str:
        ocr_str = ocr_area(upper_left_point, lower_right_point)[0]# str num
        return ocr_str
    def ap_num(self):
        '''体力'''
        num= self.ocr((512,21),(604,51))
        return num.split('/')[0] if '/' in num else num
    
    def gold_coins_num(self):
        '''信用点'''
        return self.ocr((702,25),(818,51))#.replace(",","")
    def diamonds_num(self):
        '''清辉石'''
        return self.ocr((871,25),(965,54))#.replace(",","")
    def total_assault(self)->tuple:
        '''总力''' # 1016 391   票 940 108 978 129 time 1140 109 1249 131
        self.on_fight_center_page()
        if not  match_pixel((1016,391),self.YELLOW_POINT):
            return ('关闭',0,0)
        else:
            click((919,423))
            sleep(3)
            click(Page.MAGICPOINT)
            num = self.ocr((940,110),(990,140))
            #num.split('/')[0] if '/' in num else num
            # 开启时间
            open_time = self.ocr((1140,112),(1240,131))
        
        if num !="":
            return ("开启",num,open_time)
        else:
            return ("开启",-1,0)
    def on_fight_center_page(self):
        if Page.is_page(PageName.PAGE_FIGHT_CENTER):
            return
        else:
            self.back_to_home()
            self.run_until(
            lambda: click((1196, 567)),
            lambda: Page.is_page(PageName.PAGE_FIGHT_CENTER),
            sleeptime=4
            )
    def grand_assault_status(self):
        '''大决战''' #  893 600time 964 665 1060 690
        if config.userconfigdict["SERVER_TYPE"]=="CN" or config.userconfigdict["SERVER_TYPE"]=="CN_BILI":
            return ('没有',0)

        if not  match_pixel((994,518),self.YELLOW_POINT):
            return ('关闭',0)
        else:
            click((893,600))
            sleep(3)
            click(Page.MAGICPOINT)
            num = self.ocr((871,25),(965,54))
            num.split('/')[0] if '/' in num else num
        if num !="":
            return ("开启",num)
        else:
            return ("开启",-1)
def is_progress_Event():
    '''活力演习''' # 1197 391
    pass

def red_point_status(point:tuple):
    return match_pixel(point, Page.COLOR_RED)
def daily_tasks_status():
    '''每日任务完成情况'''# 红点 日服 111 255  国际服en 94 256 
    pass
def cafe_status():
    '''咖啡厅''' #黄点 国服 126 676 百分比 1105 640
    pass
def invite_status():
    '''咖啡厅是否可邀请'''
    pass

def contest_status():
    '''战术演习''' # 日服 1174 517 红点能领取钻石，黄点还有票 国服在 1197 397   国际服红点 1174  518
    pass
def wanted_status():
    '''悬赏'''
    pass

def lesson_status():
    '''课表'''
    pass
def progress_status():
    '''检查什么开启了双倍三倍活动'''
    pass

def exchange_status():
    ''' 学院交流会黄点'''

if __name__ == '__main__':
    pass
    Daily_loop_control()
    # os._exit(0)
    #close_emulator('D:/Program Files/Netease/MuMuPlayer-12.0/shell/','MuMuPlayer.exe' , 3)