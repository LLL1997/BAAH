from nicegui import ui
from gui.components.list_edit_area import list_edit_area

def set_hard(config, shared_softwareconfig):
    with ui.row():
        ui.link_target("HARD")
        ui.label(config.get_text("task_hard")).style('font-size: x-large')

    with ui.card():
        ui.number(config.get_text("config_push_hard_desc"), min=0, precision=0, step=1).bind_value(config.userconfigdict, "PUSH_HARD_QUEST", forward=lambda x: int(x)).style("width: 300px")
        ui.number(config.get_text("config_level"), min=1, precision=0, step=1).bind_value(config.userconfigdict, "PUSH_HARD_QUEST_LEVEL").style("width: 300px")
    
    ui.label(config.get_text("config_desc_times"))
    ui.switch(config.get_text("config_event_status")).bind_value(config.userconfigdict, "HARD_QUEST_EVENT_STATUS") 
    
    show_note = {"val": False}
    ui.switch(config.get_text("button_show")+config.get_text("desc_note")).bind_value(show_note, "val")
    ui.textarea().bind_value(shared_softwareconfig.softwareconfigdict["NOTE"], "HARD_NOTE").style("width: 70%").bind_visibility_from(show_note, "val")
    
    list_edit_area(
        config.userconfigdict["HARD"], 
        [
            config.get_text("config_day"), 
            "",
            [
                config.get_text("config_location"),
                config.get_text("config_level"),
                config.get_text("config_times"),
                "开关"
            ]
            ,""
        ], 
<<<<<<< HEAD
<<<<<<< HEAD
         '''优香 1-1/4-3/12-2------------------------------阿露 18-3------------------------------伊织 14-3/20-3------------------------------泉奈 19-3------------------------------晴奈 8-3/12-3
            遥香 13-1/15-1------------------------------睦月 13-2/16-2------------------------------佳代子 14-1/21-2------------------------------尼禄 15-3------------------------------
            莲见 3-2/8-2/11-2------------------------------芹娜 20-1/24-1------------------------------芹香  1-3/7-2/9-2------------------------------白子 3-3/9-3------------------------------椿 15-2/23-2
            明日奈4-1/7-1/16-1------------------------------日富美 5-3/10-3------------------------------淳子 2-3/5-2/6-3------------------------------尼禄 15-3
            千世 14-2/17-2------------------------------花凛 17-3------------------------------响 22-3------------------------------明里 2-2/5-1/9-1/11-1 
            爱丽丝 23-3------------------------------星野 7-3/11-3------------------------------日奈 16-3/24-3 
            t1 1图 t2-4 t3-7图 t4-10图 t5-13图 t6-16图 t7-19图 t8-22图 H图不是按这个,只是有装备
            装备能开始刷的对应关系 帽子第一章一图 发卡二章二图 手表二章四图
         '''

    )# config.get_text("config_desc_list_edit")
=======
         '''
         '''

    )# config.get_text("config_desc_list_edit")
   
=======
        config.get_text("config_desc_list_edit"),
        has_switch=True
    )
    
>>>>>>> 2ce304c89d22027e0bae9d555458b66424e15646
    # explore
    ui.label(config.get_text("push_hard")).style('font-size: x-large')
    
    ui.label(config.get_text("config_explore_attention"))
    
    with ui.card():
        ui.checkbox(config.get_text("config_use_simple_explore")).bind_value(config.userconfigdict, "PUSH_HARD_USE_SIMPLE")
        ui.checkbox(config.get_text("config_rainbow_teams_desc")).bind_value(config.userconfigdict, "EXPLORE_RAINBOW_TEAMS")
        ui.number(config.get_text("config_push_hard_desc"), min=1, precision=0, step=1).bind_value(config.userconfigdict, "PUSH_HARD_QUEST", forward=lambda x: int(x)).style("width: 300px")
        ui.number(config.get_text("config_level"), min=1, precision=0, step=1).bind_value(config.userconfigdict, "PUSH_HARD_QUEST_LEVEL", forward=lambda x:int(x)).style("width: 300px")
    
>>>>>>> e7da5a2baec6560ca7c05328828f6d271b96d187
