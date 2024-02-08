from nicegui import ui
from gui.components.list_edit_area import list_edit_area

def set_normal(config):
    with ui.row():
        ui.link_target("NORMAL")
        ui.label(config.get_text("task_normal")).style('font-size: x-large')
    
    num_map = {1:4, 2:0, 3:0} # 跳过中间1，2，3
    
    ui.number(config.get_text("config_push_normal_desc"), min=0, precision=0, step=1).bind_value(config.userconfigdict, "PUSH_NORMAL_QUEST", forward=lambda x: num_map[x] if x in num_map else int(x)).style("width: 300px")
    
    ui.label(config.get_text("config_desc_times"))
    
    list_edit_area(
        config.userconfigdict["NORMAL"], 
        [
            config.get_text("config_day"), 
            "",
            [
                config.get_text("config_location"),
                config.get_text("config_level"),
                config.get_text("config_times")
            ]
        ], 
        config.get_text("config_desc_list_edit")
    )
    