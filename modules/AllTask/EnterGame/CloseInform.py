 

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, screenshot
from modules.configs.MyConfig import config
class CloseInform(Task):
    def __init__(self, name="CloseInform", pre_times = 3, post_times = 3) -> None:
        super().__init__(name, pre_times, post_times)

     
    def pre_condition(self) -> bool:
        sleep(1)
        screenshot()
        if not match(popup_pic(PopupName.POPUP_LOGIN_FORM)):
            if config.userconfigdict['SERVER_TYPE']  not in ["CN", "CN_BILI"]:
                click(Page.MAGICPOINT, 3) #
            return False
        return True
    
     
    def on_run(self) -> None:
        click(Page.MAGICPOINT)
        click((1226, 56))
        click(Page.MAGICPOINT)


     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)