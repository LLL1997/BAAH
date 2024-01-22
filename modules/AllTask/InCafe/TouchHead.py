 

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName
from modules.configs.MyConfig import config
from modules.AllPage.Page import Page
from modules.AllTask.Task import Task
import logging
from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, screenshot, match_pixel
import asyncio

class TouchHead(Task):
    # 安全的可点击边界，排除了下方按钮区域
    SAFE_X_LEFT = 1
    SAFE_X_RIGHT = 1279
    SAFE_Y_TOP = 74
    SAFE_Y_BOTTOM = 598
    def __init__(self, name="TouchHead") -> None:
        super().__init__(name)

     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_CAFE)
    
    def click_head_and_magic(self):
        # 清除可能的好感度弹窗
        click(Page.MAGICPOINT)
        self.run_until(
            lambda: click(Page.MAGICPOINT),
            lambda: Page.is_page(PageName.PAGE_CAFE) and match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE),
        )
        canmatchRes = match(button_pic(ButtonName.BUTTON_STU_NOTICE), threshold=0.95, returnpos=True, rotate_trans=True)
        if(canmatchRes[0]):
            logging.info("匹配到注意力符号，点击头部")
            # 中心点
            self.safe_click((canmatchRes[1][0]+50, canmatchRes[1][1]+30), sleeptime=0.1)
            # 四个角
            for offsetx in [-20, 20]:
                for offsety in [-30, 30]:
                    self.safe_click((canmatchRes[1][0]+50+offsetx, canmatchRes[1][1]+30+offsety), sleeptime=0.1)
            # 等待羁绊弹窗
            sleep(1)
        self.run_until(
            lambda: click(Page.MAGICPOINT),
            lambda: Page.is_page(PageName.PAGE_CAFE),
        )

    def safe_click(self, pos, sleeptime=1):
        x=pos[0]
        y=pos[1]
        if x<self.SAFE_X_LEFT or x>self.SAFE_X_RIGHT or y<self.SAFE_Y_TOP or y>self.SAFE_Y_BOTTOM:
            logging.warn("点击坐标不在安全范围内，不点击")
        else:
            click(pos, sleeptime=sleeptime)
            
    def swipeRight(self):
        swipe((1116, 129), (431, 129), 0.3)
    
    def swipeLeft(self):
        swipe((431, 129), (1116, 129), 0.3)
    
    def swipeDown(self):
        swipe((751, 420), (431, 129), 0.3)
    
    def swipeUp(self):
        swipe((431, 129), (751, 420), 0.3)
    def exhaustion_touch_head(self): #待实现
        # TODO 地毯式摸头
        '''地毯式摸头'''
        async def async_swipe(x1,y1,x2,y2,time=5):
            swipe((x1, y1), (x2, y2), time)
        def scaling():
            # from modules.utils.adb_utils import send_adb_keyevent
            # send_adb_keyevent()
            [swipe((167, 540), (1132, 172), 0.2) for x in range(3)]
            return
            # 无效果 后续看怎么实现
            asyncio.run(async_swipe(320,180,1180,530)
                                   )
            asyncio.run(async_swipe(1180,530,320,180)
                                   )
        def Touch_head():
            click((75,650))
            sleep(1)
            click((1145,95)) # 重新排序
            for x in range(0,1280,40):
                for y in range(138,600,30):
                    click((x,y),sleeptime=0.01)
            for y in range(138,600,30):
                for x in range(0,1280,40):
                    click((x,y),sleeptime=0.01)

        # 清除可能的好感度弹窗
        click(Page.MAGICPOINT)
        self.run_until(
            lambda: click(Page.MAGICPOINT),
            lambda: Page.is_page(PageName.PAGE_CAFE) and match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE),
        )
        # 先缩放再居中再地毯式摸头
        scaling()# 缩放 
        Touch_head() # 地毯摸头
        self.run_until(
            lambda: click(Page.MAGICPOINT),
            lambda: Page.is_page(PageName.PAGE_CAFE),
        )
    
    def on_run(self) -> None:
        if config.userconfigdict["CAFE_CAMERA_FULL"]:
            # 视角最高直接点
            totalruns = 3
            times_in_run = 3
            for i in range(totalruns):
                # sometimes a speak will cover the NOTICE icon, so we need to double check
                click(Page.MAGICPOINT)
                click((75,650))# 重新排序
                sleep(1)# 重新排序
                click((1145,95)) # 重新排序
                self.run_until(
                    lambda: self.click_head_and_magic(),
                    lambda: not match(button_pic(ButtonName.BUTTON_STU_NOTICE), threshold = 0.95, rotate_trans=True),
                    times = times_in_run, # 直到找不到注意力符号
                    sleeptime=1
                )
                logging.info(f"第{i+1}/{totalruns}轮摸头结束")
                sleep(3)
        elif config.userconfigdict["CAFE_EXHAUSTIVITY_TOUCH_HEAD"] :
            #click(Page.MAGICPOINT) CAFE_EXHAUSTIVITY_TOUCH_HEAD
            self.exhaustion_touch_head()
            logging.info(f"地毯式摸头结束")
            sleep(3)
        else:
            # 左右拖动换视角摸头
            TO_POS_LEFT = [self.swipeLeft, self.swipeLeft, self.swipeLeft]
            TO_POS_BOTTOM = [self.swipeDown, self.swipeDown, self.swipeDown]
            TO_POS_RIGHT = [self.swipeRight, self.swipeRight]
            TO_POS_RIGHT_SIDE = [self.swipeRight, self.swipeRight]
            TO_POS_CENTER = [self.swipeLeft, self.swipeUp, self.swipeUp, self.swipeUp]
            all_pos = [TO_POS_LEFT, TO_POS_BOTTOM, TO_POS_RIGHT,TO_POS_RIGHT_SIDE, TO_POS_CENTER]
            
            for movefuncs in all_pos:
                # 先摸再变视角
                # 这个画面里有多少次没有匹配到注意力符号
                times_not_match = 0
                for tt in range(8):
                    # 清除可能的好感度弹窗
                    self.run_until(
                        lambda: click(Page.MAGICPOINT),
                        lambda: Page.is_page(PageName.PAGE_CAFE) and match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE),
                    )
                    screenshot()
                    if (match(button_pic(ButtonName.BUTTON_STU_NOTICE), threshold = 0.95, rotate_trans=True)):
                        self.click_head_and_magic()
                    else:
                        # 失败次数超过3次就不再尝试
                        times_not_match += 1
                        if times_not_match == 3:
                            break
                # 变换视角前再次确认关闭弹窗回到咖啡厅页面
                self.run_until(
                    lambda: click(Page.MAGICPOINT),
                    lambda: Page.is_page(PageName.PAGE_CAFE) and match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE),
                )
                logging.info("变换视角")
                for func in movefuncs:
                    func()
    
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_CAFE)
    