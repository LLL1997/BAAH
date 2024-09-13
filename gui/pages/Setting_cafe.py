from nicegui import ui
from datetime import datetime
def set_cafe(config):
    # 创建一个行
    with ui.row():
        # 创建一个链接，链接到CAFE
        ui.link_target("CAFE")
        # 创建一个标签，标签内容为config.get_text("task_cafe")，样式为font-size: x-large
        ui.label(config.get_text("task_cafe")).style('font-size: x-large')
    
    # 创建一个标签，标签内容为config.get_text("config_cafe_attention")
    ui.label(config.get_text("config_cafe_attention"))
    
    # 创建一个行
    with ui.row():
<<<<<<< HEAD
        ui.checkbox(config.get_text("config_camera_full")).bind_value(config.userconfigdict, "CAFE_CAMERA_FULL")
=======
        ui.checkbox(config.get_text("cafe_collect_desc")).bind_value(config.userconfigdict, "CAFE_COLLECT")
        
    with ui.row():
        ui.checkbox(config.get_text("cafe_touch_desc")).bind_value(config.userconfigdict, "CAFE_TOUCH")
        full_camera = ui.checkbox(config.get_text("config_camera_full")).bind_value(config.userconfigdict, "CAFE_CAMERA_FULL").bind_visibility_from(config.userconfigdict, "CAFE_TOUCH")
        full_camera.set_value(True)
        full_camera.set_enabled(False)
>>>>>>> e7da5a2baec6560ca7c05328828f6d271b96d187
        ui.checkbox(config.get_text("config_cafe_exhaustivity_touch_head")).bind_value(config.userconfigdict, "CAFE_EXHAUSTIVITY_TOUCH_HEAD")
        
        Invite_time_switch = ui.switch('是否只在限定时间执行邀请')
        ui.time(value='12:00').bind_visibility_from(Invite_time_switch,'value')
<<<<<<< HEAD
       
=======
       
        ui.checkbox(config.get_text("enable_diff_touch")).bind_value(config.userconfigdict, "CAFE_TOUCH_WAY_DIFF").bind_visibility_from(config.userconfigdict, "CAFE_TOUCH")
        
    with ui.row():
        ui.checkbox(config.get_text("cafe_invite_desc")).bind_value(config.userconfigdict, "CAFE_INVITE").bind_visibility_from(config.userconfigdict, "CAFE_TOUCH")
>>>>>>> e7da5a2baec6560ca7c05328828f6d271b96d187
