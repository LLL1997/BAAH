from nicegui import ui
from gui.components.list_edit_area import list_edit_area

def set_normal(config):
    
    with ui.row():
        ui.link_target("NORMAL")
        ui.label(config.get_text("task_normal")).style('font-size: x-large')
    
    num_map = {1:4, 2:0, 3:0} # 跳过中间1，2，3
    
    with ui.card():
        ui.number(config.get_text("config_push_normal_desc"), min=0, precision=0, step=1).bind_value(config.userconfigdict, "PUSH_NORMAL_QUEST", forward=lambda x: num_map[x] if x in num_map else int(x)).style("width: 300px")
        ui.number(config.get_text("config_level"), min=1, precision=0, step=1).bind_value(config.userconfigdict, "PUSH_NORMAL_QUEST_LEVEL").style("width: 300px")
    
    ui.label(config.get_text("config_desc_times"))
    ui.switch(config.get_text("config_event_status")).bind_value(config.userconfigdict, "NORMAL_QUEST_EVENT_STATUS") 
    list_edit_area(
        config.userconfigdict["NORMAL"], 
        [
            config.get_text("config_day"), 
            "",
            [
                config.get_text("config_location"),
                config.get_text("config_level"),
<<<<<<< HEAD
                config.get_text("config_times"),
                "switch"
<<<<<<< HEAD
            ],""
        ], '''        t1 1图 t2-4 t3-7图 t4-10图 t5-13图 t6-16图 t7-19图 t8-22图 H图不是按这个,只是有装备
                装备能开始刷的对应关系 帽子第一章一图 发卡二章二图 手表二章四图'''
=======
            ],config.get_text("config_desc_list_edit")+""
        ], config.get_text("config_desc_list_edit")+'''        
        t1 1图 t2-4 t3-7图 t4-10图 t5-13图 t6-16图 t7-19图 t8-22图
        装备能开始刷的对应关系 帽子第一章一图 发卡二章二图 手表二章四图
        '''
>>>>>>> e7da5a2baec6560ca7c05328828f6d271b96d187
        #config.get_text("config_desc_list_edit")
=======
                config.get_text("config_times")
            ]
        ], 
        config.get_text("config_desc_list_edit"),
        has_switch=True
>>>>>>> 2ce304c89d22027e0bae9d555458b66424e15646
    )
    # explore
    ui.label(config.get_text("push_normal")).style('font-size: x-large')
    
    ui.label(config.get_text("config_explore_attention"))
    
    with ui.card():
        ui.checkbox(config.get_text("config_use_simple_explore")).bind_value(config.userconfigdict, "PUSH_NORMAL_USE_SIMPLE")
        ui.checkbox(config.get_text("config_rainbow_teams_desc")).bind_value(config.userconfigdict, "EXPLORE_RAINBOW_TEAMS")
        ui.number(config.get_text("config_push_normal_desc"), min=4, precision=0, step=1).bind_value(config.userconfigdict, "PUSH_NORMAL_QUEST", forward=lambda x: int(x)).style("width: 300px")
        ui.number(config.get_text("config_level"), min=1, precision=0, step=1).bind_value(config.userconfigdict, "PUSH_NORMAL_QUEST_LEVEL", forward=lambda x:int(x)).style("width: 300px")
    