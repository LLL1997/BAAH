from nicegui import ui
from modules.configs.MyConfig import config

def list_edit_area(datadict, linedesc, blockdesc=""):
    """
    datadict: 要修改的二维或三维列表，长度代表列表维度
        [str1, str2] 或 [str1, str2, [str3, str4]] 或 [str1, str2, [str3, str4, str5]]
    linedesc: 二维或三维列表的描述，长度代表列表维度
    blockdesc: 对于这个块的描述
    """
    dim = len(linedesc)# 判断gui里有多少行
    subdim = 0
    if dim >= 3: # 列表有三行数据（描述文本）
        subdim = len(linedesc[2]) #获取参数数量
    @ui.refreshable
    def item_list():
        '''

        i 一共有多少个数据,读取config里的大列表一共有多少数据 
        j 数 日期
        k I里面的数据有多少个参
        '''
        for blocklinedesc in blockdesc.split('\n'):
            ui.label(f'{blocklinedesc}')
        # 遍历data字典中的每一行
        for i in range(len(datadict)):# 遍历config里的大列表
            line_item = datadict[i] #第二维列表
            # 打印第i行
            ui.label(f'{config.get_text("config_nth")} {i+1} {linedesc[0]}: ')
            with ui.row():
                # 遍历每一行中的每一列
                for j in range(len(line_item)):
                    # 如果linedesc的长度为2，则表示第几个教室
                    if len(linedesc) == 2:
                        # 第几个教室
                        ui.number(f'{linedesc[1]}',
                                    min=1,
                                    step=1,
                                    precision=0,
                                    format="%.0f",
                                    value=line_item[j],
                                    on_change=lambda v,i=i,j=j: datadict[i].__setitem__(j, int(v.value)),
                                    ).style('width: 60px')
                    # 如果linedesc的长度为3，则表示关卡和次数
                    elif len(linedesc) == 3:
                        ui.label(f'{linedesc[1]}:')
                        with ui.row():
                            with ui.card():
                                for k in range(len(line_item[j])):
                                    #  遍历关卡和次数
                                    min_value = 1
                                    if k == subdim-1:
                                        min_value = -99
                                    ui.number(f'{linedesc[2][k]}',
                                                min=min_value,
                                                step=1,
                                                precision=0,
                                                format="%.0f",
                                                value=line_item[j][k],
                                                on_change=lambda v,i=i,j=j,k=k: datadict[i][j].__setitem__(k, int(v.value)),
                                                ).style('width: 60px')
                    elif len(linedesc) == 4:
                        ui.label(f'{linedesc[1]}:')
                        with ui.row():
                            with ui.card():
                                # 遍历每一列中的每一关和次数
                                for k in range(len(line_item[j])):
                                    #  遍历关卡和次数
                                    # 获取最小值
                                    min_value = 1
                                    if k == len(linedesc)-2:
                                        min_value = -99
                                    if k == 3:
                                        ui.switch(value=line_item[j][k],on_change=lambda v,i=i,j=j:datadict[i][j].__setitem__(k, v.value))
                                        continue
                                    ui.number(f'{linedesc[2][k]}',
                                                min=min_value,
                                                step=1,
                                                precision=0,
                                                format="%.0f",
                                                value=line_item[j][k],
                                                on_change=lambda v,i=i,j=j,k=k: datadict[i][j].__setitem__(k, int(v.value)),
                                                ).style('width: 60px')
                                
                            
                with ui.column():
                    ui.button(f"{config.get_text('button_add')} {linedesc[1]}", on_click=lambda i=i: add_item_item(i))
                    if len(datadict[i]) > 0:
                        ui.button(f"{config.get_text('button_delete')} {linedesc[1]}", on_click=lambda i=i: del_item_item(i), color="red")
        with ui.row():
            ui.button(f"{config.get_text('button_add')} {linedesc[0]}", on_click=add_item)
            if len(datadict) > 0:
                ui.button(f"{config.get_text('button_delete')} {linedesc[0]}", on_click=del_item, color="red")
    
    def add_item():
        datadict.append([])
        item_list.refresh()
    
    def del_item():
        datadict.pop()
        item_list.refresh()
    
    def add_item_item(item_ind):
        if dim == 2:
            datadict[item_ind].append(1)
        elif dim == 3:
            if subdim == 2:
                datadict[item_ind].append([1, 1])
            elif subdim == 3:
                datadict[item_ind].append([1, 1, 1])
        if dim > 3 and subdim == 4:
            datadict[item_ind].append([1, 1, 1,True])
            
        item_list.refresh()
    
    def del_item_item(item_ind):
        datadict[item_ind].pop()
        item_list.refresh()

    item_list()