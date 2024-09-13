from nicegui import ui
from modules.configs.MyConfig import config

def list_edit_area(datadict, linedesc, blockdesc="", has_switch=False):
    """
    datadict: 要修改的二维或三维列表，长度代表列表维度
        [str1, str2] 或 [str1, str2, [str3, str4]] 或 [str1, str2, [str3, str4, str5]]
    linedesc: 二维或三维列表的描述，长度代表列表维度
    blockdesc: 对于这个块的描述
    has_switch: 是否有单个元素的功能开关，有功能开关的话，二维列表会升三维，三维列表的最后一维会多一个值 表示开关
    """
    dim = len(linedesc)
    subdim = 0
    if dim == 3:
        subdim = len(linedesc[2])
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
                        # 第i个地区的第j个教室, or 商店里的第i行第j个物品
                        if isinstance(datadict[i][j], tuple) or isinstance(datadict[i][j], list):
                            # 如果该元素是个元组或者列表，那么该元素应当包含一个开关
                            # [值，开关boolean]
                            with ui.card():
                                ui.number(f'{linedesc[1]}',
                                    min=1,
                                    step=1,
                                    precision=0,
                                    format="%.0f",
                                    value=line_item[j][0],
                                    on_change=lambda v,i=i,j=j: datadict[i][j].__setitem__(0, int(v.value)),
                                    ).style('width: 60px')
                                if len(line_item[j]) == 2 and has_switch:
                                    ui.label(config.get_text("button_enable"))
                                    ui.switch(value=line_item[j][1],on_change=lambda v,i=i,j=j:datadict[i][j].__setitem__(1, bool(v.value)))
                        else:
                            # 否则就按照单个数字渲染
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
                                    # 如果一个元素的数据量超出了给定的文字描述的数量，而且是有开关的
                                    # 那么最后那个'多出来的'数据就是开关
                                    if k >= subdim: # 多出来的数据下标continue掉，没有对应的渲染文字
                                        if k == subdim and has_switch: # 如果刚好多一个数据而且has_switch就渲染个开关
                                            ui.label(config.get_text("button_enable"))
                                            ui.switch(value=line_item[j][k],on_change=lambda v,i=i,j=j:datadict[i][j].__setitem__(k, bool(v.value)))
                                        continue
                                    #  遍历地区, 关卡和次数
                                    min_value = 1
                                    # 如果数据的位置就是最后一个文字描述的位置，代表的数据是扫荡次数，最小值为-99
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
        
    def get_num_of_last_item(mylist):
        """
        给定一个列表，返回最后一个元素的实际值
        
        如果该元素为number类型，返回number。如果该元素为list类型，返回list的第一个元素
        """
        if len(mylist) == 0:
            return 0
        item = mylist[-1]
        if isinstance(item, list) or isinstance(item, tuple):
            return item[0]
        else:
            return item
    
    def add_item_item(item_ind):
        if dim == 2: 
            if has_switch:
                # 有单个元素的开关的话，升维
                datadict[item_ind].append([int(get_num_of_last_item(datadict[item_ind]) + 1), True])
            else:
                datadict[item_ind].append(int(get_num_of_last_item(datadict[item_ind]) + 1))
        elif dim == 3:
            if subdim == 2:
                datadict[item_ind].append([1, 1])
            elif subdim == 3:
                datadict[item_ind].append([1, 1, 1])
            
        item_list.refresh()
    
    def del_item_item(item_ind):
        datadict[item_ind].pop()
        item_list.refresh()

    item_list()