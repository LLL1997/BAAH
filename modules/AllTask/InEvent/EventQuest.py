 
import logging
import time
from modules.AllTask.SubTask.RaidQuest import RaidQuest
from modules.AllTask.SubTask.FightQuest import FightQuest
from modules.AllTask.SubTask.ScrollSelect import ScrollSelect
from modules.configs.MyConfig import config
import numpy as np

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, match_pixel, screenshot

class EventQuest(Task):
    def __init__(self, level_list, name="EventQuest") -> None:
        super().__init__(name)
        self.level_list = level_list
        # 记录上次自动推图的关卡下标
        self.last_fight_level_ind = -1

     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_EVENT)
    
    def judge_whether_and_do_fight(self, this_level_ind):
        """
        观察下标为this_level_ind的关卡是否可扫荡，如果不可扫荡就打一次
        """
        screenshot()
        if not match(popup_pic(PopupName.POPUP_TASK_INFO)) and not match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE):
            logging.info("触发推图任务")
            # 判断推图是否刚才打了一次，但是没三星或打不过去
            if this_level_ind == self.last_fight_level_ind:
                raise Exception(f"活动自动推图第{this_level_ind+1}关刚才打了一次，但是没三星或打不过去，请配置更好的队伍配置")
            # 点击任务开始按钮
            click(button_pic(ButtonName.BUTTON_TASK_START))
            # 如果体力不够
            screenshot()
            if match(popup_pic(PopupName.POPUP_TOTAL_PRICE)):
                logging.warn("体力不够，结束")
                return "noap"
            # 单次战斗
            FightQuest(backtopic=lambda: match(page_pic(PageName.PAGE_EVENT))).run()
            # 更新上次自动推图的关卡下标
            self.last_fight_level_ind = this_level_ind
            return "yes"
        return "no"
    
    def on_run(self) -> None:
        # 按level执行
        for level in self.level_list:
            level_ind = level[0]
            repeat_times = level[1]
            while(1):
                # 可能触发推图任务，触发推图的话就重新滑到顶部再往右选
                sleep(3)
                # 视角会自动滚动到顶部，等3秒
                click(Page.MAGICPOINT)
                # 点击Quest标签
                click((965, 98))
                self.scroll_right_up(times=5)
                # 点击第一个level
                click((1130, 200), sleeptime=3)
                logging.info(f"尝试跳转到第{level_ind+1}个level")
                # 向右挪到第level_ind个level
                # 判断是否要推图并推图
                res=self.judge_whether_and_do_fight(0)
                if res=="yes":
                    # 继续从头滑动
                    continue
                elif res=="noap":
                    self.run_until(
                        lambda: click(Page.MAGICPOINT),
                        lambda: match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE)
                    )
                    logging.info("返回到根页面")
                    return
                hasfight_newlevel = False
                for i in range(level_ind):
                    click((1171, 359), sleeptime=1)
                    # 判断是否要推图并推图
                    res=self.judge_whether_and_do_fight(1+i)
                    if res=="yes":
                        # 设置继续从头滑动
                        hasfight_newlevel = True
                        break
                    elif res=="noap":
                        self.run_until(
                            lambda: click(Page.MAGICPOINT),
                            lambda: match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE)
                        )
                        logging.info("返回到根页面")
                        return
                if hasfight_newlevel:
                    # 继续从头滑动
                    continue
                # 结束自动推图，或不用推图：扫荡
                RaidQuest(repeat_times).run()
                # 关闭任务咨询弹窗
                logging.info("关闭任务咨询弹窗")
                Task.run_until(
                    lambda: click(Page.MAGICPOINT),
                    lambda: match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE)
                )
                break
        Task.run_until(
            lambda: click(Page.MAGICPOINT),
            lambda: match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE)
        )
        

     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_EVENT)