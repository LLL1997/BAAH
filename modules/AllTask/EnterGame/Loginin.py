 

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName


from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

<<<<<<< HEAD
from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep

import logging
=======
from modules.utils.log_utils import logging
from modules.utils.adb_utils import close_app
from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, check_app_running, open_app, config, screenshot
from modules.configs.MyConfig import config
>>>>>>> e7da5a2baec6560ca7c05328828f6d271b96d187
# =====

class Loginin(Task):
    def __init__(self, name="Loginin", pre_times = 3, post_times = 10) -> None:
        super().__init__(name, pre_times, post_times)

     
    def pre_condition(self) -> bool:
        if(self.post_condition()):
            click(Page.MAGICPOINT, 3)
            return False
        return True
    

    @staticmethod
<<<<<<< HEAD
    def try_jump_useless_pages(i=None,times=1):
        # 点掉确认按钮
=======
    def try_jump_useless_pages(i=None,times=0):
        # 确认处在游戏界面
        if not check_app_running(config.userconfigdict['ACTIVITY_PATH']):
            open_app(config.userconfigdict['ACTIVITY_PATH'])
            logging.warn({"zh_CN": "游戏未在前台，尝试打开游戏", "en_US":"The game is not in the foreground, try to open the game"})
            sleep(2)
            screenshot()
        
>>>>>>> e7da5a2baec6560ca7c05328828f6d271b96d187
            
        if match(popup_pic(PopupName.POPUP_MAINTENACE_NOTICE)) and match(popup_pic(PopupName.POPUP_NOTICE)):# TODO 增加识别维护
            logging.info("服务器维护")
            raise Exception("找到维护弹窗，退出")
        elif match(button_pic(ButtonName.BUTTON_CONFIRMB)):
<<<<<<< HEAD
            click(button_pic(ButtonName.BUTTON_CONFIRMB))   
=======
            # 点掉确认按钮
            click(button_pic(ButtonName.BUTTON_CONFIRMB))   
        elif match(button_pic(ButtonName.BUTTON_USER_AGREEMENT)):
            # 用户协议
            click(button_pic(ButtonName.BUTTON_USER_AGREEMENT))
        elif match(button_pic(ButtonName.BUTTON_QUIT_LAST)):
            # 点掉放弃上次战斗进度按钮
            click(button_pic(ButtonName.BUTTON_QUIT_LAST))
>>>>>>> e7da5a2baec6560ca7c05328828f6d271b96d187
        else:
            # 活动弹窗
            if config.userconfigdict['SERVER_TYPE']  not in ["CN", "CN_BILI"]:
                click(Page.MAGICPOINT, 3) #
            click((1250, 40))


<<<<<<< HEAD
        from modules.utils.adb_utils import open_app,check_app_running,close_app
        from modules.configs.MyConfig import config
=======
        
>>>>>>> e7da5a2baec6560ca7c05328828f6d271b96d187
        if i != None and i%10==0 and not check_app_running(config.userconfigdict['ACTIVITY_PATH']) :
            sleep(5)
            open_app(config.userconfigdict['ACTIVITY_PATH'])
            logging.info("可能app闪退了，正常不应该出现这条，尝试重新打开游戏...")
            sleep(20)

        # 超过一半的运行时间,尝试重启app一次来解决卡登录问题
<<<<<<< HEAD
        if i == int(times*0.5): 
=======
        if i == int(times*0.2): 
>>>>>>> e7da5a2baec6560ca7c05328828f6d271b96d187
            # 关闭app,
            logging.info("可能app卡登录,尝试重启app来解决")
            close_app(config.userconfigdict['ACTIVITY_PATH'])
            sleep(10)
            open_app(config.userconfigdict['ACTIVITY_PATH'])


    def on_run(self) -> None:
        # 因为涉及到签到页面什么的，所以这里点多次魔法点
<<<<<<< HEAD
        # 因为涉及到活动页面什么的，所以这里还要尝试识别左下角的不再显示
        if self.run_until(self.try_jump_useless_pages, 
                      lambda: match(popup_pic(PopupName.POPUP_LOGIN_FORM)) or Page.is_page(PageName.PAGE_HOME), 
                      times = 300,
                      sleeptime = 1.5)==False:
            from modules.add_functions.msg import push_msg_fast
            push_msg_fast(f"碧蓝档案游戏，游戏登录，无法进入主页可能要更新app或服务器维护，程序退出{self.name}")
            raise Exception("游戏登录，无法进入主页可能要更新app或服务器维护，程序退出原因{}".format(self.name))
=======
        if not self.run_until(self.try_jump_useless_pages, 
                      lambda: match(popup_pic(PopupName.POPUP_LOGIN_FORM)) or Page.is_page(PageName.PAGE_HOME), 
                      times = 200,
                      sleeptime = 4):
            from modules.add_functions.msg import push_msg_fast
            push_msg_fast(f"碧蓝档案游戏，游戏登录，无法进入主页可能要更新app或服务器维护，程序退出{self.name}")
            raise Exception("游戏登录，无法进入主页可能要更新app或服务器维护，程序退出原因{}".format(self.name))
        if config.userconfigdict['SERVER_TYPE']  not in ["GLOBAL", ]:
                click(Page.MAGICPOINT)
                sleep(10)
                click(Page.MAGICPOINT) # 有时候公告加载慢了 卡识别，国际服加载公告慢
>>>>>>> e7da5a2baec6560ca7c05328828f6d271b96d187

     
    def post_condition(self) -> bool:
        return match(popup_pic(PopupName.POPUP_LOGIN_FORM)) or Page.is_page(PageName.PAGE_HOME)