from pyvda import AppView, VirtualDesktop
import win32gui,win32con,ctypes
import pyvda

def get_all_window_hwmd():
    '''获取所有窗体'''
    windows = []
    def enum_window_callback(hwnd, windows):
        windows.append(hwnd)
        return True
    win32gui.EnumWindows(enum_window_callback, windows)
    return windows
def find_window_by_keyword(keyword)->list[tuple[int,str] | None]:
    # 获取最顶层的窗口句柄
    #hwnd = win32gui.GetForegroundWindow()
    hwnd = get_all_window_hwmd()
    # 存储匹配窗口句柄的列表
    matched_hwnds = []
    # 遍历所有顶层窗口
    if hwnd:
        for x in hwnd:
            # 获取窗口标题
            window_title = win32gui.GetWindowText(x)
            # 如果窗口标题包含关键词，则将其句柄添加到列表中
            if keyword in window_title.lower():  # 转换为小写进行匹配，忽略大小写
                matched_hwnds.append((x, window_title))
            # # 获取下一个顶层窗口句柄
            # hwnd = win32gui.GetWindow(hwnd, win32con.GW_HWNDNEXT)
    return matched_hwnds

def window_in_virtual_desktop_and_move_to(window_name:str='模拟器',v_desktop:int=3)->bool|None:
    """
    获取指定窗口所在的虚拟桌面索引，并移动窗口到目标窗口
    :param window_name: 窗口的句柄
    :paramv_desktop: 虚拟桌面索引
    :return 如果窗口不在任何虚拟桌面上，则返回 None
    """
    hwnds=find_window_by_keyword(window_name)
    target_vd=VirtualDesktop(v_desktop)
    
    if hwnds:
        for x in hwnds:
            app=AppView(x[0])
            if app.is_on_desktop(target_vd)==False:
                try:
                    app.move(target_vd)
                except Exception as e:
                    print('移动窗口发生错误')
                    print(e)
                    return False
        return True
    return None



    current_vd = pyvda.VirtualDesktop.get_current()
    AppView.is_shown_in_switchers
    AppView.is_on_desktop

def move_windows(window_name:str='模拟器',v_desktop:int=3):
    '''
    移动含有所有的字符串的窗口到目标虚拟桌面

    windows的虚拟桌面从1开始数数

    只适用于win10和win11
    '''
    try:
        for x in find_window_by_keyword(window_name):
            AppView(x[0]).move(VirtualDesktop(v_desktop))
    except Exception as e:
        print('移动窗口发生错误')
        print(e)
if __name__ == '__main__':
    #move_windows()
    window_in_virtual_desktop_and_move_to(window_name='模拟器',v_desktop=3)