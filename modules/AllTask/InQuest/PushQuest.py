<<<<<<< HEAD
 
<<<<<<< HEAD
import logging
=======
=======
>>>>>>> 2ce304c89d22027e0bae9d555458b66424e15646
from modules.utils.log_utils import logging
>>>>>>> e7da5a2baec6560ca7c05328828f6d271b96d187

from DATA.assets.PageName import PageName
from DATA.assets.ButtonName import ButtonName
from DATA.assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.Task import Task

from modules.AllTask.SubTask.ScrollSelect import ScrollSelect
from modules.AllTask.SubTask.FightQuest import FightQuest
from modules.AllTask.SubTask.GridQuest import GridQuest

from modules.utils import (click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area, config, screenshot,
                           match_pixel)
from modules.utils.grid_analyze import GridAnalyzer
from .Questhelper import (jump_to_page, close_popup_until_see, judge_whether_3star, quest_has_easy_tab, easy_tab_pos_R, center_tab_pos_L)


class PushQuest(Task):
    """
    从进入关卡选择页面开始托管推图

    通过page_ind和level_ind定位到起始关卡，随后每成功推一张图就让level_ind+1，向右多翻一次后，用ocr来更新确切的page_ind和level_ind

    Parameters
    ----------
    quest_type : str
        任务类型，normal/hard

    page_ind : int
        开始推图的章节下标
    """

    def __init__(self, quest_type, page_ind, level_ind=0, name="PushQuest") -> None:
        super().__init__(name)
        self.is_normal = quest_type == "normal"
        self.page_ind = page_ind  # 初始聚焦章节下标
        self.level_ind = level_ind  # 初始聚焦关卡下标
        self.require_type_ind = 0  # 当前需要完成的任务类型下标

    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_QUEST_SEL)

    def on_run(self) -> None:
        if self.is_normal:
            logging.info({"zh_CN": "切换到普通关卡", "en_US": "switch to normal quest"})
            self.run_until(
                lambda: click((798, 159)),
                lambda: match(button_pic(ButtonName.BUTTON_NORMAL))
            )
        else:
            logging.info({"zh_CN": "切换到困难任务", "en_US": "switch to hard quest"})
            self.run_until(
                lambda: click((1064, 161)),
                lambda: match(button_pic(ButtonName.BUTTON_HARD))
            )
        while 1:
            # ===========尝试定位要推图的章节和关卡===================
            # 跳转到相应地区
            logging.info({"zh_CN": "尝试跳转至页面 {}".format(self.page_ind + 1),
                          "en_US": "Try jumping to page {}".format(self.page_ind + 1)})
            jumpres = jump_to_page(self.page_ind + 1)  # 下标加1为实际页号数字
            if not jumpres:
                logging.error({"zh_CN": "跳转至页面 {} 失败，结束此任务".format(self.page_ind + 1),
                               "en_US": "Cannot jump to page {}, end this task".format(self.page_ind + 1)})
                return
            click(Page.MAGICPOINT, sleeptime=1)
            self.scroll_right_up()
<<<<<<< HEAD
            sleep(0.5)
=======
            sleep(3)
            # 清除弹窗
            self.run_until(
                lambda: click(Page.MAGICPOINT),
                lambda: match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE)
            )
>>>>>>> e7da5a2baec6560ca7c05328828f6d271b96d187
            # 点击第一个关卡
            self.run_until(
                lambda: click((1118, 240)),
                lambda: not match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE)
            )
            # 此时应该看到扫荡弹窗
            # 判断是否有简易攻略tab

            # 向右翻self.level_ind次
            logging.info({"zh_CN": "尝试翻到关卡 {}".format(self.level_ind + 1),
                          "en_US": "Try flipping to level {}".format(self.level_ind + 1)})
            for i in range(self.level_ind):
                click((1171, 359), sleeptime=1)
            screenshot()
            # 如果匹配到弹窗消失
            if match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE):
                logging.info({"zh_CN": "关卡弹窗消失，结束此任务","en_US": "Level popup disappears, end this task"})
                return
            # 此时判断是否有简易攻略tab
            has_easy_tab = quest_has_easy_tab()
            # 当前关卡就是这次需要推图的关卡
            # 国服弹窗往右偏移了50
            offsetx = 0
<<<<<<< HEAD
<<<<<<< HEAD
            if config.userconfigdict["SERVER_TYPE"] == "CN":
                offsetx = 50
            left_up = ocr_area((139+offsetx, 197), (216+offsetx, 232))
            page_level = left_up[0].split(" ")[0].replace("|","").replace("[","").replace("]","").strip().split("-")
            try:
=======
            # 日服弹窗往下偏移了30，由于简易攻略tab
=======
            # 往下偏移了30，由于简易攻略tab
>>>>>>> 2ce304c89d22027e0bae9d555458b66424e15646
            offsety = 0
            if config.userconfigdict["SERVER_TYPE"] == "CN" or config.userconfigdict["SERVER_TYPE"] == "CN_BILI":
                offsetx = 50
            if has_easy_tab:
                logging.info({"zh_CN": "存在简易攻略", "en_US": "There is a short guide"})
                offsety = 30
            # 识别关卡序号，更新最新的page_ind和level_ind
            left_up = ocr_area((139 + offsetx, 197 + offsety), (216 + offsetx, 232 + offsety))
            page_level = left_up[0].split(" ")[0].replace("|", "").replace("[", "").replace("]", "").strip().split("-")
            try:
<<<<<<< HEAD
                logging.info(f"分割后的关卡序号：{page_level}")
>>>>>>> e7da5a2baec6560ca7c05328828f6d271b96d187
=======
                logging.info({"zh_CN": f"分割后的关卡序号：{page_level}",
                              "en_US": f"Split Level Sequence: {page_level}"})
>>>>>>> 2ce304c89d22027e0bae9d555458b66424e15646
                # 这一步更新这次推图的实际章节和关卡下标
                page_num = int(page_level[0])
                self.page_ind = page_num - 1
                if page_level[1] == "A" or page_level[1] == "B" or page_level[1] == "C":
                    # 如果为A/B/C关卡，就直接把来到这里的这一次的level作为这次的level
                    # 一般来说关卡号为A的关卡都是一章节的最后一关，且为普通关，打完后不会消失
<<<<<<< HEAD
                    pass
=======
                    # 最后self.level_ind+1，前往下一关
<<<<<<< HEAD
                    logging.info("战斗关卡 {}-{}，开始推图".format(page_num, page_level[1]))
>>>>>>> e7da5a2baec6560ca7c05328828f6d271b96d187
=======
                    logging.info({"zh_CN": "战斗关卡 {}-{}，开始推图".format(page_num, page_level[1]),
                                  "en_US": "Battle level {} - {}, start thumbnail".format(page_num, page_level[1])})
>>>>>>> 2ce304c89d22027e0bae9d555458b66424e15646
                else:
                    level_num = int(page_level[1])
                    # 否则将识别到的关卡序号-1作为这次的level下标
                    self.level_ind = level_num - 1
<<<<<<< HEAD
<<<<<<< HEAD
                logging.info("关卡：{}-{}，开始推图".format(page_num, level_num))
            except:
                logging.warn(f"OCR关卡序号识别失败({left_up[0]})")
                if not match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE):
                    # 如果匹配到开始任务，说明是支线关卡，打完就会消失
                    logging.info("判断为支线关卡")
                    # 这里将level_ind-1，因为支线关卡打完后会消失，让后面打完后的level_ind+1刚好抵消
                    self.level_ind -= 1
                else:
                    logging.error(f"OCR关卡序号识别失败({left_up[0]}), 且未匹配到开始任务按钮，结束此任务")
                    return
            # ===========正式开始推图===================
            # 看到弹窗，ocr是否有S
            ocr_s = ocr_area((327+offsetx, 257), (353+offsetx, 288))
=======
                    logging.info("格子关卡：{}-{}，开始推图".format(page_num, level_num))
=======
                    logging.info({"zh_CN": "格子关卡：{}-{}，开始推图".format(page_num, level_num),
                                  "en_US": "Grid level: {} - {}, start thumbnail".format(page_num, level_num)})
>>>>>>> 2ce304c89d22027e0bae9d555458b66424e15646
            except:
                logging.warn({"zh_CN": f"OCR关卡序号识别失败({left_up[0]})",
                              "en_US": f"Failing to recognize the level number({left_up[0]})"})
                if not match_pixel(Page.MAGICPOINT, Page.COLOR_WHITE):
                    if "A" in left_up[0] or "B" in left_up[0] or "C" in left_up[0]:
                        # 如果匹配到数字A,B,C，说明是章节末尾关卡，打完后不会消失
                        logging.info({"zh_CN": "判断为章节末尾关卡",
                                      "en_US": "Judged as a level at the end of the chapter"})
                    else:
                        # 如果没有匹配A,B,C，说明是支线关卡，打完就会消失
                        logging.info({"zh_CN": "判断为支线关卡", "en_US": "Judged as Side Stage"})
                        # 这里将level_ind-1，因为支线关卡打完后会消失，后面的关相当于自动往前进一格，让后面打完后的level_ind+1刚好抵消
                        self.level_ind -= 1
                else:
                    logging.error({"zh_CN": f"OCR关卡序号识别失败({left_up[0]}), 且未匹配到开始任务弹窗，结束此任务",
                                   "en_US": f"Cannnot recognize the level number({left_up[0]}), "
                                            f"and not match the start task popup, end this task"})
                    return
            # ===========正式开始推图===================
            # 看到弹窗，ocr是否有S
<<<<<<< HEAD
            ocr_s = ocr_area((327+offsetx, 257+offsety), (353+offsetx, 288+offsety))
            # 如果是日服，推图点击简易攻略
            if config.userconfigdict["SERVER_TYPE"] == "JP":
                logging.info("日服：使用简易攻略")
                click((891, 185))
                click((891, 185))
                ocr_s = "easy"
>>>>>>> e7da5a2baec6560ca7c05328828f6d271b96d187
=======
            ocr_s = ocr_area((327 + offsetx, 257 + offsety), (370 + offsetx, 288 + offsety))
            # 如果有简易攻略tab，有简易攻略tab存在，这个图肯定默认是格子图
            if has_easy_tab:
                if (self.is_normal and config.userconfigdict["PUSH_NORMAL_USE_SIMPLE"]) or (not self.is_normal and config.userconfigdict["PUSH_HARD_USE_SIMPLE"]):
                    logging.info({"zh_CN": "使用简易攻略", "en_US": "Use simple explore"})
                    click(easy_tab_pos_R)
                    click(easy_tab_pos_R)
                    # 简易攻略的话，把ocr_s设为_，让后面不要走格子(no "S")
                    ocr_s = ["_", 1.0]
                else:
                    logging.info({"zh_CN": "不使用简易攻略",
                                  "en_US": "Do not use simple explore"})
                    click(center_tab_pos_L)
                    click(center_tab_pos_L)
                    # 切换到集中指挥tab后，才会出现s标签，没有必要再次识别
                    ocr_s = ["S", 1.0]


>>>>>>> 2ce304c89d22027e0bae9d555458b66424e15646
            walk_grid = None
            logging.info("OCR: "+ocr_s[0].upper())
            if "S" not in ocr_s[0].upper():
                logging.info({"zh_CN": "未识别到S等级，判断为普通战斗",
                              "en_US": "S grade not recognized, judged as normal battle"})
                walk_grid = False
            else:
                logging.info({"zh_CN": "识别到S标签，判断为走格子战斗",
                              "en_US": "Identified the S tag and judged it to be a grid fight"})
                walk_grid = True
            if not walk_grid:
                enteredit = self.run_until(
                    lambda: click(button_pic(ButtonName.BUTTON_TASK_START)),
                    lambda: match(page_pic(PageName.PAGE_EDIT_QUEST_TEAM))
                )
                # 识别不到大的开始任务按钮，可能是支线任务
                if not enteredit:
                    # 支线任务的开始任务按钮在中间，且比较小
                    self.run_until(
                        lambda: click((639, 516)),
                        lambda: match(page_pic(PageName.PAGE_EDIT_QUEST_TEAM))
                    )
                FightQuest(backtopic=lambda: match(page_pic(PageName.PAGE_QUEST_SEL))).run()
<<<<<<< HEAD
                # 普通任务完成后，level下标直接+1
=======
                # 普通任务完成后，level下标直接+1。如果是支线关卡，由于之前减过一了，这里直接+1就行
>>>>>>> e7da5a2baec6560ca7c05328828f6d271b96d187
                self.level_ind += 1
            else:
                jsonname = f"{self.page_ind + 1}-{self.level_ind + 1}.json"
                if not self.is_normal:
                    jsonname = f"H{jsonname}"
                grider = GridAnalyzer("quest", jsonfilename=jsonname)
<<<<<<< HEAD
=======
                click(button_pic(ButtonName.BUTTON_TASK_START), sleeptime=2)
>>>>>>> e7da5a2baec6560ca7c05328828f6d271b96d187
                self.run_until(
                    lambda: click(button_pic(ButtonName.BUTTON_TASK_START)),
                    lambda: match(page_pic(PageName.PAGE_GRID_FIGHT))
                )
                # 需求列表
                require_types = list(grider.get_requires_list().keys())
                GridQuest(grider=grider, backtopic=lambda: match(page_pic(PageName.PAGE_QUEST_SEL)),
                          require_type=require_types[self.require_type_ind]).run()
                # 任务完成后，往后切换需求类型下标，如果超出了需求类型列表，就回到0，且level下标+1
                self.require_type_ind += 1
                if self.require_type_ind >= len(require_types):
                    self.require_type_ind = 0
                    self.level_ind += 1
            logging.info({"zh_CN": f"一个战斗完成，更新关卡下标为{self.level_ind}",
                          "en_US": f"One battle completed, update level subscript to {self.level_ind}"})
            sleep(6) # 等待6秒：可能的新章节解锁动画

    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_QUEST_SEL)