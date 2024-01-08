 

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

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
        else:
            # 活动弹窗
            click((1250, 40))

    def open_app_error(self,i):
        print("打开app失败，尝试重新运行")
        if i >=500:
            pass
     
    def on_run(self) -> None:
        # 因为涉及到签到页面什么的，所以这里点多次魔法点
        # 因为涉及到活动页面什么的，所以这里还要尝试识别左下角的不再显示
        self.run_until(self.try_jump_useless_pages, 
                      lambda: match(popup_pic(PopupName.POPUP_LOGIN_FORM)) or Page.is_page(PageName.PAGE_HOME), 
                      times = 999,
                      sleeptime = 1.5)
        # error_handling = open_app_error

     
    def post_condition(self) -> bool:
        return match(popup_pic(PopupName.POPUP_LOGIN_FORM)) or Page.is_page(PageName.PAGE_HOME)