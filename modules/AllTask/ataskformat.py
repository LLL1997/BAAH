
from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

<<<<<<< HEAD
from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config, screenshot, match_pixel
<<<<<<< HEAD
=======
=======
from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config, screenshot, match_pixel, istr, CN, EN, JP
>>>>>>> 2ce304c89d22027e0bae9d555458b66424e15646
from modules.utils.log_utils import logging
>>>>>>> e7da5a2baec6560ca7c05328828f6d271b96d187

class NameOfTask(Task):
    def __init__(self, name="NameOfTask") -> None:
        super().__init__(name)

     
    def pre_condition(self) -> bool:
        return super().pre_condition()
    
     
    def on_run(self) -> None:
        super().on_run()

     
    def post_condition(self) -> bool:
        return super().post_condition()