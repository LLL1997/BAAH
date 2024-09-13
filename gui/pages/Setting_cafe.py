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
        ui.checkbox(config.get_text("config_camera_full")).bind_value(config.userconfigdict, "CAFE_CAMERA_FULL")
        ui.checkbox(config.get_text("config_cafe_exhaustivity_touch_head")).bind_value(config.userconfigdict, "CAFE_EXHAUSTIVITY_TOUCH_HEAD")
        
        Invite_time_switch = ui.switch('是否只在限定时间执行邀请')
        ui.time(value='12:00').bind_visibility_from(Invite_time_switch,'value')
       