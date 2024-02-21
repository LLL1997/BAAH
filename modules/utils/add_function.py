from DATA.assets.PageName import PageName
import os,datetime,subprocess,time
import functools
from datetime import datetime
import logging
from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, match_pixel,ocr_area,screenshot,ocr_area_0
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
    ORANGE_POINT = ((8, 160, 250), (25, 200, 255)) # 橙色小点
    YELLOW_BANNER = ((64, 222, 234), (84, 242, 254)) # 总力战开启牌子（在作战中心）
    RED_POINT = ((15, 60, 250), (23, 72, 255)) # 红色小点

    def __init__(self, name="daily_report") -> None:
        super().__init__(name)

    def pre_condition(self) -> bool:
        return super().pre_condition()
    
    def set_sessiondict(self,key,value):
        config.sessiondict[key]=value

    def get_sessiondict_value(self,key):
        if key in config.sessiondict:
            return config.sessiondict[key]
        else:
            return False
        
    def start(self) -> None:
        '''开始时统计一次资源'''
        logging.info("开始执行开始时统计")
        Task.back_to_home()
        # global report_dict
        # report_dict={"ap":self.ap_num(),"gold_coins":self.gold_coins_num(),"diamonds":self.diamonds_num()}
        # logging.info("结束时统计")
        # self.set_sessiondict("ap",self.ap_num())
        self.set_sessiondict("gold_coins_num",self.gold_coins_num())
        self.set_sessiondict("diamonds_num",self.diamonds_num())

    def on_run(self):
        # 创建一个字典，用来统计数据
        logging.info("开始执行统计")
        Task.back_to_home()
        data = {"ap":self.ap_num(),
                "gold_coins_num":self.gold_coins_num(),
                "diamonds_num":self.diamonds_num(),
                'lesson_status':self.lesson_status(),
                "progress_Event":self.is_progress_Event(),
                "contest_status":self.contest_status(),
                'wanted_status':self.wanted_status(),
                "total_assault":self.total_assault(),
                "grand_assault":self.grand_assault_status(),
                }
        text = (
            "碧蓝档案,BAAH"
            + "服务器"
            + config.userconfigdict["SERVER_TYPE"]
            + f'\n剩余体力:{data["ap"]}\n'
        )
        # if  'report_dict' in globals() and   report_dict["gold_coins"] !='' :
        if self.get_sessiondict_value("gold_coins_num") not in ["",None,False]:
            try:
                #last_num=str(report_dict["gold_coins"])
                last_num=str(self.get_sessiondict_value("gold_coins_num"))
                now_num=str(data["gold_coins_num"])
                change_num=int(now_num.replace(",",""))-int(last_num.replace(",",""))
                text =text+f'信用点:{data["gold_coins_num"]},\t变化:{str(change_num)}\n'
            except Exception as e:
                logging.info(e)
                text=text+f'信用点:{data["gold_coins_num"]}\n'
        else:

            text=text+f'信用点:{data["gold_coins_num"]}\n'

        #if 'report_dict' in globals() and   report_dict["diamonds"] !='' :
        if self.get_sessiondict_value("diamonds_num") not in ["",None,False]:
            try:
                #last_num=str(report_dict["diamonds"])
                last_num=str(self.get_sessiondict_value("diamonds_num"))
                now_num=str(data["diamonds_num"])
                change_num=int(now_num.replace(",",""))-int(last_num.replace(",",""))
                text=text+f'青辉石:{data["diamonds_num"]},\t变化:{str(change_num)}\n'
            except Exception as e:
                logging.info(e)
                text=text+f'青辉石:{data["diamonds_num"]}\n'
        else:
            text=text+f'青辉石:{data["diamonds_num"]}\n' 
        if data["lesson_status"] not in ['完成',]:
            text=text+f'课程表:\t{data["lesson_status"]}\n'
        if data["wanted_status"] not in ['完成',]:
            text=text+f'悬赏任务:\t{data["wanted_status"]}\n'
        if data["contest_status"] not in ['完成',]:
            text=text+f'战术演习:\t{data["contest_status"]}\n'
        if data["total_assault"][0]=="开启":
            text=text+f'总力:{data["total_assault"][0]},\t票:{data["total_assault"][1]}\n总力结束:{data["total_assault"][2]}\n'
        if data["grand_assault"][0]=="开启":
            text=text+f'大决战:{data["grand_assault"][0]}\t结束:{data["grand_assault"][1]}\n剩余:{data["grand_assault"][2]}'
        # 火力演习状态:{data["progress_Event"]}
        from modules.add_functions.msg import push_msg_fast
        push_msg_fast(text)
        return data
    
    def post_condition(self) -> bool:
        return super().post_condition()
    
    def red_point_status(self,point:tuple):
        return match_pixel(point, self.RED_POINT)
    
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
    
    def total_assault(self)->tuple:# 
        '''总力''' # 黄色横幅 855 388 1016 391   票 940 108 978 129 time 1140 109 1249 131
        self.on_fight_center_page()
        if not  match_pixel((1015,392),self.ORANGE_POINT) or not  match_pixel((855,388),self.YELLOW_BANNER) :
            if match_pixel((1015,392),self.RED_POINT):
                return ('可领取',0,0)

            return ('关闭',0,0) # 
        elif match_pixel((1015,392),self.ORANGE_POINT) or  match_pixel((855,388),self.YELLOW_BANNER):
            click((919,423))
            sleep(3)
            click(Page.MAGICPOINT)
            screenshot()
            num = self.ocr((940,110),(975,132))
            # num.split('/')[0] if '/' in num else num
            # 开启时间
            open_time = self.ocr((1140,110),(1250,132))
            click(Page.TOPLEFTBACK,1)
            return ("开启",num,open_time)
        else:
            return ('关闭',0,0)

    def on_fight_center_page(self):
        screenshot()
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
        '''大决战''' #  893 600 time 964 665 1060 690 hs 960 511
        self.on_fight_center_page()
        if config.userconfigdict["SERVER_TYPE"]=="CN" or config.userconfigdict["SERVER_TYPE"]=="CN_BILI":
            return ('没有',0)

        if not  match_pixel((994,518),self.ORANGE_POINT) or not match_pixel((888,511),self.YELLOW_BANNER) : 
            return ('关闭',0)
        else:
            click((893,600))
            sleep(3)
            click(Page.MAGICPOINT)
            screenshot()
            # 开启时间 
            open_time = ''.join([ch for ch in self.ocr((857,666),(1060,690)) if ch.isdigit() or ch in ['/','~','-',' ',':']])
            open_time = open_time.replace("-", "~")
            try:
                parts = open_time.split("~")
                now_time_str =  datetime.now().strftime("%m/%d %H:%M") # parts[0].strip()
                end_time_str = parts[1].strip()
                # 定义日期和时间的格式
                format_str = "%m/%d %H:%M"
                # 将字符串转换为datetime对象
                start_time = datetime.strptime(now_time_str, format_str)
                end_time = datetime.strptime(end_time_str, format_str)
                # 计算两个时间之间的差异
                time_difference = end_time - start_time
                click(Page.TOPLEFTBACK,1)
                return ("开启",end_time_str,time_difference)
            except Exception:
                return ("开启",open_time,'error')
        
    def is_progress_Event(self):
        '''火力演习''' # 1197 391
        self.on_fight_center_page()
        if config.userconfigdict["SERVER_TYPE"]=="CN" or config.userconfigdict["SERVER_TYPE"]=="CN_BILI":
            return '没有'

        if  match_pixel((1197,391),self.ORANGE_POINT):
            return '未刷'
        
    def contest_status(self):
        '''战术演习''' # 日服 1174 517 红点能领取钻石，黄点还有票 国服在 1197 397   国际服红点 1174  518
        self.on_fight_center_page()
        sleep(3)
        if config.userconfigdict["SERVER_TYPE"]=="CN" or config.userconfigdict["SERVER_TYPE"]=="CN_BILI":
            point=(1195,392)
        else: # 日服  国际服 
            point=(1175,518)
        if match_pixel(point,self.RED_POINT):
            return '未领取工资'
        elif match_pixel(point,self.ORANGE_POINT):
            return '有剩余jjc票'
        else:
            return '完成'
        
    def wanted_status(self): #833 393
        '''悬赏'''
        self.on_fight_center_page()
        if  match_pixel((833,393),self.ORANGE_POINT):
            return '有票'
        else:
            return '完成'
    def lesson_status(self): # TODO 不好用，待后续优化
        '''课表'''
        Task.back_to_home()
        self.run_until(
            lambda: click((212, 669)),
            lambda: Page.is_page(PageName.PAGE_TIMETABLE)
        )
        try: 
            nolefttickets= ''.join([ch for ch in self.ocr((213, 81), (264, 116)) if ch.isdigit() or ch =='/'])
            print(nolefttickets)
            if int(nolefttickets[0])==0:
                return '完成'
            else:
                return '未完成',nolefttickets[0]
        except Exception:
            return ''

def daily_tasks_status():
    '''每日任务完成情况'''# 红点 日服 111 255  国际服en 94 256 
    pass
def cafe_status():
    '''咖啡厅''' #黄点 国服 126 676 百分比 1105 640
    pass
def invite_status():
    '''咖啡厅是否可邀请'''
    pass

def progress_status():
    '''检查什么开启了双倍三倍活动'''
    pass


if __name__ == '__main__':
    pass
    Daily_loop_control()
    # os._exit(0)
    #close_emulator('D:/Program Files/Netease/MuMuPlayer-12.0/shell/','MuMuPlayer.exe' , 3)
