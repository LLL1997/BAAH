from nicegui import ui
from gui.components.list_edit_area import list_edit_area

def set_normal(config):
    with ui.row():
        ui.link_target("NORMAL")
        ui.label(config.get_text("task_normal")).style('font-size: x-large')
    
    ui.label(config.get_text("config_desc_times"))
    
    list_edit_area(
        config.userconfigdict["NORMAL"], 
        [
            config.get_text("config_day"), 
            "",
            [
                config.get_text("config_location"),
                config.get_text("config_level"),
                config.get_text("config_times"),
                "switch"
            ],""
        ], '''        t1 1图 t2-4 t3-7图 t4-10图 t5-13图 t6-16图 t7-19图 t8-22图 H图不是按这个,只是有装备
                装备能开始刷的对应关系 帽子第一章一图 发卡二章二图 手表二章四图'''
        #config.get_text("config_desc_list_edit")
    )
    