from pyvda import AppView, VirtualDesktop
import win32gui,win32con

def find_window_by_keyword(keyword)->list[tuple[int,str] | None]:
    # 获取最顶层的窗口句柄
    hwnd = win32gui.GetForegroundWindow()
    # 存储匹配窗口句柄的列表
    matched_hwnds = []
    # 遍历所有顶层窗口
    while hwnd:
        # 获取窗口标题
        window_title = win32gui.GetWindowText(hwnd)
        # 如果窗口标题包含关键词，则将其句柄添加到列表中
        if keyword in window_title.lower():  # 转换为小写进行匹配，忽略大小写
            matched_hwnds.append((hwnd, window_title))
        # 获取下一个顶层窗口句柄
        hwnd = win32gui.GetWindow(hwnd, win32con.GW_HWNDNEXT)
    return matched_hwnds

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
    move_windows()