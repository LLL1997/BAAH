 
import logging

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.SubTask.RaidQuest import RaidQuest
from modules.AllTask.SubTask.ScrollSelect import ScrollSelect
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area
from .Questhelper import jump_to_page, close_popup_until_see
import numpy as np

class NormalQuest(Task):
    def __init__(self, questlist, name="NormalQuest") -> None:
        super().__init__(name)
        self.questlist = questlist

     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_QUEST_SEL)
    
     
    def on_run(self) -> None:
        logging.info("switch to normal quest")
        self.run_until(
            lambda: click((798, 159)),
            lambda: match(button_pic(ButtonName.BUTTON_NORMAL))
        )
        if not match(page_pic(PageName.PAGE_IN_PROGRESS),threshold=0.95):
            #界面复杂，需要找新方法，放在最后执行，这个不想，先占位 # TODO Normal判断是否在活动中
            logging.info(f"NormalQuest设置为不在活动时间不刷取,未检测到横幅{PageName.PAGE_IN_PROGRESS}，忽略")
            return
        else:
            logging.info(f"NormalQuest设置为仅在活动中（双倍三倍）执行，且检测到横幅{PageName.PAGE_IN_PROGRESS}")
        # after switch to normal, go to the page
        for each_quest in self.questlist:
            to_page_num = each_quest[0]+1
            level_ind = each_quest[1]
            repeat_times = each_quest[2]
            if each_quest[-1] == 'false' or each_quest[-1] == False or each_quest[-1] == 0 : # 开关关闭
                logging.info(f"{to_page_num}-{level_ind+1}设置为关, 忽略这关扫荡")
                continue
            if repeat_times == 0:
                # if repeat_times == 0, means this quest is not required to do
                continue
            jumpres = jump_to_page(to_page_num)
            if not jumpres:
                logging.error("go to page {} failed, ignore this quest".format(to_page_num))
                continue
            click(Page.MAGICPOINT)
            ScrollSelect(level_ind, 190, 288, 628, 1115, lambda: match(popup_pic(PopupName.POPUP_TASK_INFO))).run()
            # 扫荡
            RaidQuest(repeat_times).run()
            # 清除所有弹窗
            close_popup_until_see(button_pic(ButtonName.BUTTON_NORMAL))
        # 清除所有弹窗
        close_popup_until_see(button_pic(ButtonName.BUTTON_NORMAL))
            
     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_QUEST_SEL)