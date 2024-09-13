# 一个用户config的GUI显示
from nicegui import ui, run
import requests

import os
from gui.pages.Setting_BAAH import set_BAAH
from gui.pages.Setting_cafe import set_cafe
from gui.pages.Setting_emulator import set_emulator
from gui.pages.Setting_event import set_event
from gui.pages.Setting_exchange import set_exchange
from gui.pages.Setting_hard import set_hard
from gui.pages.Setting_normal import set_normal
from gui.pages.Setting_other import set_other
from gui.pages.Setting_server import set_server
from gui.pages.Setting_shop import set_shop
from gui.pages.Setting_special import set_special
from gui.pages.Setting_task_order import set_task_order
from gui.pages.Setting_timetable import set_timetable
from gui.pages.Setting_wanted import set_wanted
from gui.pages.Setting_notification import set_notification
from gui.pages.Setting_vpn import set_vpn
from gui.pages.Setting_Assault import set_assault

@ui.refreshable
def show_GUI(load_jsonname, config, shared_softwareconfig):
    
    # 如果是example.json，则大字提醒
    if load_jsonname == "example.json":
        ui.label(config.get_text("notice_example_json")).style("font-size: 30px; color: red;")
        
    config.parse_user_config(load_jsonname)

    # myAllTask里面的key与GUI显示的key的映射
    real_taskname_to_show_taskname = {
        "登录游戏":config.get_text("task_login_game"),
        "清momotalk":config.get_text("task_clear_momotalk"),
        "咖啡馆":config.get_text("task_cafe"),
        "咖啡馆只摸头":config.get_text("task_cafe_deprecated"), # 为了兼容以前的配置里的咖啡馆只摸头，这里只改显示名
        "课程表":config.get_text("task_timetable"),
        "社团":config.get_text("task_club"),
        "商店":config.get_text("task_shop"),
        "悬赏通缉":config.get_text("task_wanted"),
        "特殊任务":config.get_text("task_special"),
        "学园交流会":config.get_text("task_exchange"),
        "战术大赛":config.get_text("task_contest"),
        "困难关卡":config.get_text("task_hard"),
        "活动关卡":config.get_text("task_event"),
        "总力战":config.get_text("task_assault"),
        "每日任务":config.get_text("task_daily"),
        "邮件":config.get_text("task_mail"),
        "普通关卡":config.get_text("task_normal"),
        "普通推图":config.get_text("push_normal"),
        "困难推图":config.get_text("push_hard"),
        "主线剧情":config.get_text("push_main_story"),
    }

    # =============================================

    # =============================================

# 定义一个函数，用于渲染设置页面，参数为ui
    with ui.row().style('min-width: 800px; display: flex; flex-direction: row;flex-wrap: nowrap;'):
<<<<<<< HEAD
        with ui.column().style('min-width: 200px; overflow: auto;flex-grow: 1;position: sticky; top: 0px;'):
            with ui.card():
                # 添加一个链接，链接到BAAH页面
=======
        with ui.column().style('height:80vh;min-width: 200px; overflow: auto;flex-grow: 1; position: sticky; top: 0px;'):
            with ui.card().style('overflow: auto;'):
>>>>>>> e7da5a2baec6560ca7c05328828f6d271b96d187
                ui.link("BAAH", '#BAAH')
                # 添加一个链接，链接到设置页面
                ui.link(config.get_text("setting_emulator"), '#EMULATOR')
                # 添加一个链接，链接到设置页面
                ui.link(config.get_text("setting_server"), '#SERVER')
<<<<<<< HEAD
                # 添加一个链接，链接到设置页面
                ui.link(config.get_text("setting_task_order"), '#TASK_ORDER')
=======
                ui.link(config.get_text("setting_vpn"), '#VPN')
                # 添加一个链接，链接到设置页面
                ui.link(config.get_text("setting_task_order"), '#TASK_ORDER')
                ui.link(config.get_text("setting_notification"), '#NOTIFICATION')
>>>>>>> e7da5a2baec6560ca7c05328828f6d271b96d187
                # 添加一个链接，链接到设置页面
                ui.link(config.get_text("setting_next_config"), '#NEXT_CONFIG')
                # 添加一个链接，链接到任务页面
                ui.link(config.get_text("task_cafe"), '#CAFE')
                # 添加一个链接，链接到任务页面
                ui.link(config.get_text("task_timetable"), '#TIME_TABLE')
                # 添加一个链接，链接到任务页面
                ui.link(config.get_text("task_shop"), '#SHOP_NORMAL')
                # 添加一个链接，链接到任务页面
                ui.link(config.get_text("task_wanted"), '#WANTED')
                # 添加一个链接，链接到任务页面
                ui.link(config.get_text("task_special"), '#SPECIAL_TASK')
                # 添加一个链接，链接到任务页面
                ui.link(config.get_text("task_exchange"), '#EXCHANGE')
                # 添加一个链接，链接到任务页面
                ui.link(config.get_text("task_event"), '#ACTIVITY')
<<<<<<< HEAD
                # 添加一个链接，链接到任务页面
=======
                ui.link(config.get_text("task_assault"), '#ASSAULT')
>>>>>>> e7da5a2baec6560ca7c05328828f6d271b96d187
                ui.link(config.get_text("task_hard"), '#HARD')
                # 添加一个链接，链接到任务页面
                ui.link(config.get_text("task_normal"), '#NORMAL')
                # 添加一个链接，链接到工具页面
                ui.link(config.get_text("setting_other"), '#TOOL_PATH')

        with ui.column().style('flex-grow: 4;'):
            
            set_BAAH(config, shared_softwareconfig)
            
            # 模拟器配置
            set_emulator(config)
            
            # 服务器配置
            set_server(config)
            
            # 自己的加速器配置
            set_vpn(config)
            
            # 任务执行顺序，后续配置文件
            set_task_order(config, real_taskname_to_show_taskname)
            
            # 通知
            set_notification(config, shared_softwareconfig)
            
            # 咖啡馆
            set_cafe(config)
            
            # 课程表
            set_timetable(config)
                
            # 商店
            set_shop(config)
            
            # 悬赏通缉
            set_wanted(config)
            
            # 特殊任务
            set_special(config)
            
            # 学园交流会
            set_exchange(config)

            # 活动关卡
            set_event(config)
            
            # 总力战
            set_assault(config)
                
            # 困难关卡
            set_hard(config)
            
            # 普通关卡
            set_normal(config)
            
            # 其他设置
            set_other(config, load_jsonname)
        
        with ui.column().style('width: 10vw; overflow: auto; position: fixed; bottom: 40px; right: 20px;min-width: 150px;'):
            
            def save_and_alert():
                config.save_user_config(load_jsonname)
                config.save_software_config()
                shared_softwareconfig.save_software_config()
                ui.notify(config.get_text("notice_save_success"))
            ui.button(config.get_text("button_save"), on_click=save_and_alert)

            def save_and_alert_and_run():
                config.save_user_config(load_jsonname)
                config.save_software_config()
                shared_softwareconfig.save_software_config()
                ui.notify(config.get_text("notice_save_success"))
                ui.notify(config.get_text("notice_start_run"))
                # 判断BAAH.exe是否存在于目录中,否则打开同目录中的main.py，传入当前config的json文件名
                if os.path.exists("BAAH.exe"):
                    os.system(f'start BAAH.py "{load_jsonname}"')
                else:
<<<<<<< HEAD
                    os.system(f'start main.py "{load_jsonname}"')
=======
                    os.system(f'start python main.py "{load_jsonname}"')
>>>>>>> e7da5a2baec6560ca7c05328828f6d271b96d187
                
                
            ui.button(config.get_text("button_save_and_run"), on_click=save_and_alert_and_run)
        
    # 加载完毕保存一下config，应用最新的对config的更改
    config.save_user_config(load_jsonname)
    config.save_software_config()