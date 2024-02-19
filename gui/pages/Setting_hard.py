from nicegui import ui
from gui.components.list_edit_area import list_edit_area

def set_hard(config):
    with ui.row():
        ui.link_target("HARD")
        ui.label(config.get_text("task_hard")).style('font-size: x-large')
    
    ui.label(config.get_text("config_desc_times"))
    ui.image('DATA/assets/hard_strategy.jpg')
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
         '''
         '''

    )# config.get_text("config_desc_list_edit")
   
    # explore
    ui.label(config.get_text("push_hard")).style('font-size: x-large')
    
    ui.label(config.get_text("config_explore_attention"))
    
    with ui.card():
        ui.checkbox(config.get_text("config_rainbow_teams_desc")).bind_value(config.userconfigdict, "EXPLORE_RAINBOW_TEAMS")
        ui.number(config.get_text("config_push_hard_desc"), min=0, precision=0, step=1).bind_value(config.userconfigdict, "PUSH_HARD_QUEST", forward=lambda x: int(x)).style("width: 300px")
        ui.number(config.get_text("config_level"), min=1, precision=0, step=1).bind_value(config.userconfigdict, "PUSH_HARD_QUEST_LEVEL", forward=lambda x:int(x)).style("width: 300px")
    