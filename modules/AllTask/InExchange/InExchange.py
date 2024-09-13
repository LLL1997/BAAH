from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area_0, match_pixel, screenshot
from modules.utils.log_utils import logging
import time
import numpy as np

from modules.configs.MyConfig import config
from .RunExchangeFight import RunExchangeFight


class InExchange(Task):
    def __init__(self, name="InExchange") -> None:
        super().__init__(name)

    def pre_condition(self) -> bool:
        if not config.userconfigdict['EXCHANGE_HIGHEST_LEVEL'] or len \
                (config.userconfigdict['EXCHANGE_HIGHEST_LEVEL']) == 0:
            logging.warn({"zh_CN": "没有配置学院交流会的level", "en_US":"Didn't set the level of exchange meeting"})
            return False
        return Page.is_page(PageName.PAGE_HOME)

    def on_run(self) -> None:
        # 得到今天是几号
        today = time.localtime().tm_mday
        # 选择一个location的下标
        target_loc = today % len(config.userconfigdict['EXCHANGE_HIGHEST_LEVEL'])
        target_info = config.userconfigdict['EXCHANGE_HIGHEST_LEVEL'][target_loc]
        # 判断这一天是否设置有交流会关卡
        if len(target_info) == 0:
            logging.warn({"zh_CN": "今天轮次中无学院交流会关卡，跳过",
                          "en_US" :"No exchange level in today's round, skip"})
            return
<<<<<<< HEAD
        # 这之后target_info是一个list，内部会有多个关卡扫荡
        # 序号转下标
<<<<<<< HEAD
        
        # target_info = [[each[0]-1, each[1]-1, each[2]] for each in target_info]
        def _generator(target_info):
            for  x in target_info:
                if len(x)==4:
                    yield  [x[0]-1,x[1]-1,x[2],x[3]]
                else: # 兼容老版3个参数的config
                    yield  [x[0]-1,x[1]-1,x[2]]
        target_info=(_generator(_target_info))
=======

>>>>>>> e7da5a2baec6560ca7c05328828f6d271b96d187
=======
        target_info = [[each[0]-1, each[1]-1, *each[2:]] for each in target_info]
>>>>>>> 2ce304c89d22027e0bae9d555458b66424e15646
        # 从主页进入战斗池页面
        self.run_until(
            lambda: click((1196, 567)),
            lambda: Page.is_page(PageName.PAGE_FIGHT_CENTER),
            sleeptime=4
        )
        # 进入学院交流会页面
        caninexchange = self.run_until(
            lambda: click((712, 592)),
            lambda: Page.is_page(PageName.PAGE_EXCHANGE),
        )
<<<<<<< HEAD
        # TODO 后期加个判断是否双倍或者三倍，实现可能为判断是否为三倍双倍横幅位置是否为空白的（没有横幅），
=======
        time.sleep(3)
        if config.userconfigdict["SERVER_TYPE"] in ["CN","CN_BILI"]:
            click((963, 544))
            sleep(2)
        # TODO 后期加个判断是否双倍或者三倍，实现可能为判断是否为三倍双倍横幅位置是否为空白的（没有横幅），左上角的按钮和出击页面的按钮不同，无法匹配，这里用左上角的
        # logging.info(match(page_pic(PageName.PAGE_IN_PROGRESS),threshold=0.86,returnpos=True))
        screenshot()
        if  match(page_pic(PageName.PAGE_IN_PROGRESS),threshold=0.86):
            logging.info(f"学院交流会为仅在活动中（双倍三倍）执行，且检测到横幅{PageName.PAGE_IN_PROGRESS}")
        else:
            logging.info("学院交流会设置为不在活动时间不刷取,未检测到横幅{PageName.PAGE_IN_PROGRESS}，忽略")
            # 回到主页
            self.back_to_home()
            return
        if config.userconfigdict["SERVER_TYPE"] in ["CN","CN_BILI",]:
            click(Page.TOPLEFTBACK)
            sleep(2)
        # 这之后target_info是一个list，内部会有多个关卡扫荡
        # 15-Feb-24 15:27:37 - INFO - (True, (1209, 164), inf)
        logging.info(match(page_pic(PageName.PAGE_IN_PROGRESS),threshold=0.92,returnpos=True))
        # 序号转下标
        # target_info = [[each[0]-1, each[1]-1, each[2]] for each in target_info]
        def _generator(target_info):
            for  x in target_info:
                if len(x)==4:
                    yield  [x[0]-1,x[1]-1,x[2],x[3]]
                else: # 兼容老版3个参数的config
                    yield  [x[0]-1,x[1]-1,x[2]]
        target_info=(_generator(_target_info))
        if not caninexchange:
            logging.warn({"zh_CN": "无法打开交换页面，任务退出", "en_US": "Can't open exchange page, task quit"})
            self.back_to_home()
            return
>>>>>>> e7da5a2baec6560ca7c05328828f6d271b96d187
        for each_target in target_info:
            # check whether there is a ticket
            if each_target[-1] == 'false' or each_target[-1] == False or each_target[-1] == 0 : # 开关关闭
                logging.info(f"{each_target[0]}-{each_target[1]}设置为关, 忽略这关扫荡")
                continue
<<<<<<< HEAD
            if ocr_area_0((72, 85), (322, 114)):
                logging.warn("没有学院交流会券")
            else:
                # 使用PageName.PAGE_EXCHANGE的坐标判断是国服还是其他服
                if match(page_pic(PageName.PAGE_EXCHANGE), returnpos=True)[1][1]>133:
                    # 如果右侧Title较低，说明是老版本的国服
                    logging.info("点击较低的三个定位点")
                    points = np.linspace(265, 544, 3)
                else:
                    # 可点击的一列点
                    points = np.linspace(206, 422, 3)
                # 点击location
                self.run_until(
                    lambda: click((963, points[each_target[0]])),
                    lambda: Page.is_page(PageName.PAGE_EXCHANGE_SUB),
                )
                # 扫荡对应的level
                RunExchangeFight(levelnum = each_target[1], runtimes = each_target[2]).run()
                # 如果是回到SUB界面之后，点击一下返回，如果是回到EXCHANGE界面，就不用点击了
                self.run_until(
                    lambda: click(Page.TOPLEFTBACK),
                    lambda: not Page.is_page(PageName.PAGE_EXCHANGE_SUB),
                    sleeptime=3
                )
=======
            # 使用PageName.PAGE_EXCHANGE的坐标判断是国服还是其他服
            if each_target[-1] == 'false' or each_target[-1] == False or each_target[-1] == 0 : # 开关关闭
                logging.info(f"交流会{each_target}设置为关, 忽略这关扫荡")
                continue
            if match(page_pic(PageName.PAGE_EXCHANGE), returnpos=True)[1][1]>133:
                # 如果右侧Title较低，说明是老版本的国服
                logging.info({"zh_CN": "点击较低的三个定位点", "en_US": "Click on the three lower anchor points"})
                points = np.linspace(265, 544, 3)
            else:
                # 可点击的一列点
                points = np.linspace(206, 422, 3)
            # 点击location
            self.run_until(
                lambda: click((963, points[each_target[0]])),
                lambda: Page.is_page(PageName.PAGE_EXCHANGE_SUB),
            )
            # 判断是否在活动开启期间
            if config.userconfigdict["EXCHANGE_EVENT_STATUS"] and each_target == target_info[0] and not ( match_pixel((195, 221), Page.COLOR_PINK,printit=True) or
                                                                                                         match_pixel((113, 252), Page.COLOR_PINK,printit=True) or
                                                                                                         match_pixel((195, 251), Page.COLOR_PINK,printit=True)):

                logging.warn({"zh_CN": "设置为没有活动不进行，跳过", "en_US":"event is not open, skip"})
                break
     

            # 扫荡对应的level
            RunExchangeFight(levelnum = each_target[1], runtimes = each_target[2]).run()
            # 如果是回到SUB界面之后，点击一下返回，如果是回到EXCHANGE界面，就不用点击了
            self.run_until(
                lambda: click(Page.TOPLEFTBACK),
                lambda: not Page.is_page(PageName.PAGE_EXCHANGE_SUB),
                sleeptime=3
            )
>>>>>>> e7da5a2baec6560ca7c05328828f6d271b96d187
        self.back_to_home()

    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_HOME)
