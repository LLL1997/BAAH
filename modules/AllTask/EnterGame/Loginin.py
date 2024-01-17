 

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep

# =====

class Loginin(Task):
    def __init__(self, name="Loginin", pre_times = 3, post_times = 10) -> None:
        super().__init__(name, pre_times, post_times)

     
    def pre_condition(self) -> bool:
        if(self.post_condition()):
            return False
        return True
    

    @staticmethod
    def try_jump_useless_pages():
        # 点掉确认按钮
        if match(button_pic(ButtonName.BUTTON_CONFIRMB)):
            click(button_pic(ButtonName.BUTTON_CONFIRMB))
        elif match(button_pic(ButtonName.BUTTON_CONFIRMB)):# TODO 增加识别维护
            pass
            # raise
        else:
            # 活动弹窗
            click((1250, 40))

        import logging
        from modules.utils.adb_utils import open_app,check_app_running
        from modules.configs.MyConfig import config
        
        if not check_app_running(config.userconfigdict['ACTIVITY_PATH']):
            open_app(config.userconfigdict['ACTIVITY_PATH'])
            logging.info("可能app闪退了，正常不应该出现这条，尝试重新打开游戏...")
            sleep(20)
    
    
    def on_run(self) -> None:
        # 因为涉及到签到页面什么的，所以这里点多次魔法点
        # 因为涉及到活动页面什么的，所以这里还要尝试识别左下角的不再显示
        if self.run_until(self.try_jump_useless_pages, 
                      lambda: match(popup_pic(PopupName.POPUP_LOGIN_FORM)) or Page.is_page(PageName.PAGE_HOME), 
                      times = 300,
                      sleeptime = 2)==False:
            from modules.add_functions.msg import push_msg_fast
            push_msg_fast(f'碧蓝档案游戏，游戏登录，无法进入主页可能要更新app或服务器维护，程序退出{format(self.name)}')
            raise Exception("游戏登录，无法进入主页可能要更新app或服务器维护，程序退出".format(self.name))

     
    def post_condition(self) -> bool:
        return match(popup_pic(PopupName.POPUP_LOGIN_FORM)) or Page.is_page(PageName.PAGE_HOME)