from nicegui import ui
from gui.components.list_edit_area import list_edit_area

def set_exchange(config):
    with ui.row():
        ui.link_target("EXCHANGE")
        ui.label(config.get_text("task_exchange")).style('font-size: x-large')
    
    ui.label(config.get_text("config_desc_times"))
    
    list_edit_area(
        config.userconfigdict["EXCHANGE_HIGHEST_LEVEL"], 
        [
            config.get_text("config_day"), 
            "",
            [
                config.get_text("config_academy"),
                config.get_text("config_level"),
                config.get_text("config_times"),
                "开关"
            ],""
        ], 
        config.get_text("config_desc_list_edit")
    )