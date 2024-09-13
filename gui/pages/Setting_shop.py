from nicegui import ui
from gui.components.list_edit_area import list_edit_area

def set_shop(config):
    with ui.row():
        ui.link_target("SHOP_NORMAL")
        ui.label(config.get_text("config_shop_normal")).style('font-size: x-large')
    
    
    ui.number(
            f'{config.get_text("config_shop_normal")} {config.get_text("config_refresh")} {config.get_text("config_times")}',
            step=1,
            precision=0,
            min=0,
            max=3
            ).bind_value(config.userconfigdict, 'SHOP_NORMAL_REFRESH_TIME', forward=lambda v: int(v)).style('width: 400px')
    
    list_edit_area(config.userconfigdict["SHOP_NORMAL"], [config.get_text("config_row"), config.get_text("config_column")], config.get_text("config_desc_shop_edit"))
    
    with ui.row():
        ui.link_target("SHOPCONTEST")
        ui.label(config.get_text("config_shop_contest")).style('font-size: x-large')
        
    ui.number(
            f'{config.get_text("config_shop_contest")} {config.get_text("config_refresh")} {config.get_text("config_times")}',
            step=1,
            precision=0,
            min=0,
            max=3
            ).bind_value(config.userconfigdict, 'SHOP_CONTEST_REFRESH_TIME', forward=lambda v: int(v)).style('width: 400px')
    with ui.row():
        ui.switch('战术商店是否开启购买').bind_value(config.userconfigdict, "SHOP_CONTEST_SWITCH")
        #ui.checkbox('战术商店是否开启购买').bind_value(config.userconfigdict, "SHOP_CONTEST_SWITCH")
    list_edit_area(config.userconfigdict["SHOP_CONTEST"], [config.get_text("config_row"), config.get_text("config_column")], config.get_text("config_desc_shop_edit"))