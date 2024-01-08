 
import logging
import random
import time
import requests
from modules.utils.MyConfig import config

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.InEvent.EventQuest import EventQuest
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, screenshot

class InEvent(Task):
    def __init__(self, name="InEvent") -> None:
        super().__init__(name)
        self.try_enter_times = 5
        self.next_sleep_time = 0.1

     
    def pre_condition(self) -> bool:
        # 通过get请求https://arona.diyigemt.com/api/v2/image?name=%E5%9B%BD%E9%99%85%E6%9C%8D%E6%B4%BB%E5%8A%A8
        # 获取国际服活动，判断是否有活动
        
        # request_url = "https://arona.diyigemt.com/api/v2/image?name=%E5%9B%BD%E9%99%85%E6%9C%8D%E6%B4%BB%E5%8A%A8"
        # response = requests.get(request_url)
        # if response.status_code == 200:
        #     if len(response.json()['data']) != 0:
        #         logging.info("存在国际服活动")
        #         self.try_enter_times = 20
        #         return Page.is_page(PageName.PAGE_HOME)
        #     else:
        #         logging.warn("不存在国际服活动")
        #         self.try_enter_times = 0
        #         return False
        return Page.is_page(PageName.PAGE_HOME)
    
    def try_goto_event(self):
        """
        点击滚动栏，前往活动页面
        """
        if Page.is_page(PageName.PAGE_FIGHT_CENTER):
            # 尝试前往活动页面
            logging.info("尝试前往活动页面")
            self.run_until(
                lambda: click((105, 162), sleeptime=1.5),
                lambda: not Page.is_page(PageName.PAGE_FIGHT_CENTER)
            )
        else:
            # 如果不在Fight Center页面，返回主页然后来到Fight Center页面
            logging.warn("页面发生未知偏移，尝试修正")
            self.back_to_home()
            self.run_until(
                lambda: click((1196, 567)),
                lambda: Page.is_page(PageName.PAGE_FIGHT_CENTER),
            )
            # 睡眠一段时间
            sleep(self.next_sleep_time)
            self.next_sleep_time += 2
            logging.info("尝试前往活动页面")
            self.run_until(
                lambda: click((105, 162), sleeptime=1.5),
                lambda: not Page.is_page(PageName.PAGE_FIGHT_CENTER)
            )
            
    
    def judge_whether_available_event(self):
        """
        判断页面是否是一个有效的活动页面
        """
        # 判断左上角标题
        if not Page.is_page(PageName.PAGE_EVENT):
            return False
        # 判断这个活动是否有Quest
        res = ocr_area((901, 88), (989, 123))
        logging.info(f"Tab栏识别结果: {res}, {'Quest' in res[0] or '任' in res[0]}")
        # 图片匹配深色的QUEST标签
        matchres = self.run_until(
            lambda: click((965, 98)),
            lambda: match(button_pic(ButtonName.BUTTON_EVENT_QUEST_SELLECTED)),
            times=2
        )
        logging.info(f"QUEST按钮匹配结果: {matchres}")
        if res[0] != "Quest" and "任" not in res[0] and not matchres:
            logging.warn("此页面不存在活动Quest")
            return False
        # 判断左下角时间
        time_res = ocr_area((175, 566), (552, 593))
        if len(time_res[0])==0:
            return False
        # '2023-12-2603:00~2024-01-0902:59'
        logging.info(f"识别活动时间: {time_res}")
        # 分割出结束时间
        if "~" in time_res[0]:
            time_split = time_res[0].split("~")
        else:
            # 如果没有识别出~分隔符，就直接取最后15个字符
            if len(time_res[0]) < 15:
                logging.error("活动时间字符串长度不足15")
                return False
            time_split = [time_res[0][-15:]]

        # 判断活动是否已结束
        end_time = time_split[-1]
        if len(end_time) != 15:
            logging.error("活动时间字符串长度不足15")
            return False
        # 将这个时间转成时间对象
        try:
            end_time_struct = time.strptime(end_time, "%Y-%m-%d%H:%M")
        except ValueError:
            end_time_struct = time.strptime(end_time, "%Y.%m.%d%H:%M")
        logging.info(f'结束时间: {time.strftime("%Y-%m-%d %H:%M:%S", end_time_struct)}')
        # 获取本地时间
        local_time_struct = time.localtime()
        # 输出字符串
        logging.info(f'本地时间: {time.strftime("%Y-%m-%d %H:%M:%S", local_time_struct)}')
        # 检测local_time_struct是否在end_time_struct之前
        if local_time_struct > end_time_struct:
            logging.info("此活动已结束")
            return False
        return True

    
    def on_run(self) -> None:
        # 进入Fight Center
        self.run_until(
            lambda: click((1196, 567)),
            lambda: Page.is_page(PageName.PAGE_FIGHT_CENTER),
        )
        # 狂点活动标
        for i in range(10):
            click((35, 110), sleeptime=0.2)
        click(Page.MAGICPOINT)
        click(Page.MAGICPOINT)
        # 尝试进入Event
        enter_event = self.run_until(
            lambda: self.try_goto_event(),
            lambda: self.judge_whether_available_event(),
            times=self.try_enter_times
        )
        
        if not enter_event:
            logging.warn("未能成功进入活动Event页面")
            return
        else:
            logging.info("成功进入Event页面")
        today = time.localtime().tm_mday
        # 跳到Quest标签
        click((965, 98))
        click((965, 98))
        
        if hasattr(config, "EVENT_QUEST_LEVEL") and len(config.EVENT_QUEST_LEVEL) != 0:
            # 可选任务队列不为空时
            quest_loc = today%len(config.EVENT_QUEST_LEVEL)
            # 得到要执行的QUEST LIST
            # [[10, -1],[11, -1]]
            quest_list = config.EVENT_QUEST_LEVEL[quest_loc]
            # 序号转下标
            quest_list_2 = [[x[0]-1,x[1]] for x in quest_list]
            # do Event QUEST
            EventQuest(quest_list_2).run()

     
    def post_condition(self) -> bool:
        return self.back_to_home()