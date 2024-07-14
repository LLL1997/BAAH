from modules.utils import match, page_pic

from modules.configs.MyConfig import config

class Page:
    CENTER = (1280/2, 720/2)
    """
    Center of the screen
    """
    MAGICPOINT = (300, 2)
    """
    Magicpoint is the point that never contains any activable item
    """
    HOMEPOINT = (1236, 25)
    """
    Most of the time, the home icon on the top right corner
    """
    TOPLEFTBACK = (56, 28)
    """
    The circle back icon on the top left corner
    """

    COLOR_WHITE = ((240, 240, 240), (255, 255, 255))
    COLOR_RED = ((24, 70, 250), (26, 72, 252))
    COLOR_BUTTON_WHITE = ((220, 220, 220), (255, 255, 255))

    COLOR_PINK = ((190, 145,255 ), (200, 155,255 ))

    """
    用于交战时右上角暂停按钮的像素识别，按钮有时半透明，受到游戏内交战环境影响，阈值可以低点
    """
    COLOR_BUTTON_GRAY = ((200, 200, 200), (230, 230, 230))
    # 父类
    def __init__(self, pagename) -> None:
        self.name = pagename
        self.topages = dict()
    
    def add_topage(self, pagename, item):
        """
        添加从这一页面到另一页面的链接
        
        page: 另一页面的Page名
        item: 图片地址或坐标元组
        """
        self.topages[pagename]=item
    
    def is_this_page(self) -> bool:
        """
        确定当前截图是否是这一页面
        
        return: 如果是这一页面，返回True，否则返回False
        """
        return match(page_pic(self.name))
    
    @staticmethod
    def is_page(pagename) -> bool:
        """
        确定当前截图是否是指定页面
        
        Parameters
        ----------
        pagename: 
            PageName下的页面名
        
        Return
        ------
        如果是指定页面，返回True，否则返回False
        """
        return match(page_pic(pagename))