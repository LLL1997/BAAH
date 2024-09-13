from nicegui import ui, run
from gui.components.list_edit_area import list_edit_area
import os

<<<<<<< HEAD
=======
from modules.utils import screencut_tool, connect_to_device, screen_shot_to_global

>>>>>>> e7da5a2baec6560ca7c05328828f6d271b96d187
def set_other(config, load_jsonname):
    with ui.row():
        ui.link_target("TOOL_PATH")
        ui.label(config.get_text("setting_other")).style('font-size: x-large')

    ui.label(config.get_text("config_warn_change")).style('color: red')
    
    with ui.row():
        ui.number(config.get_text("config_run_until_try_times"),
                  step=1,
                  min=3,
                  precision=0).bind_value(config.userconfigdict, 'RUN_UNTIL_TRY_TIMES', forward=lambda x:int(x), backward=lambda x:int(x))
        
    with ui.row():
        ui.number(config.get_text("config_run_until_wait_time"),
                  suffix="s",
                  step=0.1,
                  min=0.1,
                  precision=1
                  ).bind_value(config.userconfigdict, 'RUN_UNTIL_WAIT_TIME')
    
    with ui.row():
        ui.number(config.get_text("config_wait_time_after_click"),
                    suffix="s",
                    step=0.1,
                    precision=1).bind_value(config.userconfigdict, 'TIME_AFTER_CLICK')
    
    ui.label(config.get_text("config_desc_response_y"))
    with ui.row():
        ui.number(config.get_text("config_response_y"),
                    step=1,
                    min=1,
                    precision=0).bind_value(config.userconfigdict, 'RESPOND_Y', forward=lambda x:int(x), backward=lambda x:int(x)).bind_enabled(config.userconfigdict, 'LOCK_SERVER_TO_RESPOND_Y', forward=lambda v: not v, backward=lambda v: not v)
        ui.checkbox(config.get_text("config_bind_response_to_server")).bind_value(config.userconfigdict, 'LOCK_SERVER_TO_RESPOND_Y')
        
    with ui.row():
        # IP+端口
        ui.input(config.get_text("config_ip_root")).bind_value(config.userconfigdict, 'TARGET_IP_PATH',forward=lambda v: v.replace("\\", "/")).style('width: 400px').bind_visibility_from(config.userconfigdict, "ADB_DIRECT_USE_SERIAL_NUMBER", lambda v: not v)
        
        # 序列号
        ui.input(config.get_text("adb_serial")).bind_value(config.userconfigdict, 'ADB_SEIAL_NUMBER').style('width: 400px').bind_visibility_from(config.userconfigdict, "ADB_DIRECT_USE_SERIAL_NUMBER", lambda v: v)
        
        # 切换使用序列号还是IP+端口
        ui.checkbox(config.get_text("adb_direct_use_serial")).bind_value(config.userconfigdict, 'ADB_DIRECT_USE_SERIAL_NUMBER')
    
    with ui.row():
        ui.input(config.get_text("config_adb_path")).bind_value(config.userconfigdict, 'ADB_PATH',forward=lambda v: v.replace("\\", "/")).style('width: 400px')
    
    with ui.row():
        ui.input(config.get_text("config_screenshot_name")).bind_value(config.userconfigdict, 'SCREENSHOT_NAME',forward=lambda v: v.replace("\\", "/")).style('width: 400px').set_enabled(False)
    
    # 测试/开发使用
    # 检查当前文件夹下有没有screencut.exe文件
<<<<<<< HEAD
    whethercut = os.path.exists("./screencut.exe")
    if whethercut:
        with ui.row():
            ui.button("测试截图/screencut test", on_click=lambda: os.system(f'start screencut.exe "{load_jsonname}"'))
=======
    # whethercut = os.path.exists("./screencut.exe")
    # if whethercut:
    #     with ui.row():
    #         ui.button("测试截图/screencut test", on_click=lambda: os.system(f'start screencut.exe "{load_jsonname}"'))
    
    async def test_screencut():
        connect_to_device(use_config=config)
        screen_shot_to_global(use_config=config)
        screenshotname = config.userconfigdict['SCREENSHOT_NAME']
        await run.io_bound(
            screencut_tool,
            left_click=True,
            right_click=True,
            img_path=screenshotname
        )
    
    # 将截图功能内嵌进GUI
    with ui.row():
        ui.button("测试截图/screencut test", on_click=test_screencut)
>>>>>>> e7da5a2baec6560ca7c05328828f6d271b96d187
