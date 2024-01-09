import json
import logging
import os
import time
from modules.configs.defaultSettings import defaultUserDict, defaultSoftwareDict

class MyConfigger:
    """
    维护一个config字典，同时将config.json的配置项作为实例属性
    """
    NOWVERSION="1.1.13"
    USER_CONFIG_FOLDER="./BAAH_CONFIGS"
    SOFTWARE_CONFIG_FOLDER="./DATA/CONFIGS"
    # 读取config这个py里面的配置
    def __init__(self):
        # 软件的config
        self.softwareconfigdict = {}
        # 软件的语言包
        self.languageconfigdict = {}
        # 一次区服任务的config
        self.userconfigdict = {}
        # 一次区服任务运行的session
        self.sessiondict = {}
        # 读取软件的config
        self.parse_software_config("software_config.json")

    def parse_user_config(self, file_name):
        """
        读取config文件并解析
        同时会清空sessiondict
        """
        # 绝对路径
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, self.USER_CONFIG_FOLDER, file_name)
        # 字典新值
        self.userconfigdict = self._read_config_file(file_path)
        self.sessiondict = {}
        
        logging.debug("user config字典内容: "+ ",".join([k for k in self.userconfigdict]))
        # 检查缺失的配置
        self._check_user_config()
    
    def parse_software_config(self, file_name):
        """
        读取config文件并解析，
        同时加载语言包
        """
        # 绝对路径
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, self.SOFTWARE_CONFIG_FOLDER, file_name)
        # 字典新值
        self.softwareconfigdict = self._read_config_file(file_path)
        logging.debug("software config字典内容: "+ ",".join([k for k in self.softwareconfigdict]))
        # 检查缺失的配置
        self._check_software_config()
        # 加载语言包

    def _read_config_file(self, file_path):
        """
        读取文件，返回字典
        """
        try:
            with open(file_path, 'r', encoding="utf8") as f:
                dictconfig = json.load(f)
                print("读取{}文件成功, 读取了{}个配置".format(file_path, len(dictconfig)))
                return dictconfig
        except Exception as e:
            raise Exception(f'读取{file_path}文件时发生错误，请检查{file_path}文件: {str(e)}')

    def _fill_by_map_or_default(self, defaultmap, selfmap, key):
        """
        尝试用defaultmap里的map和default值填充某个key
        """
        # 使用对应关系查找
        if "m" in defaultmap[key]:
            mapdict = defaultmap[key]["m"]
            fromkey = mapdict["from"]
            mapfunc = mapdict["map"]
            if fromkey in selfmap:
                # 能用对应关系就用对应关系
                selfmap[key] = mapfunc(selfmap[fromkey])
            else:
                # 对应关系的键不在，那就只能用默认值
                selfmap[key] = defaultmap[key]["d"]
        else:
            # 没有对应关系就只能默认值
            selfmap[key] = defaultmap[key]["d"]

    def _check_user_config(self):
        """
        检查用户的config内的值是否有缺少，如果有，按照对应关系查找，如果没有，就用默认值
        """
        # 先处理SERVER_TYPE
        if "SERVER_TYPE" not in self.userconfigdict:
            # 使用对应关系查找
            mapdict = defaultUserDict["SERVER_TYPE"]["m"]
            fromkey = mapdict["from"]
            mapfunc = mapdict["map"]
            if fromkey in self.userconfigdict:
                self.userconfigdict["SERVER_TYPE"] = mapfunc(self.userconfigdict[fromkey])
            else:
                self.userconfigdict["SERVER_TYPE"] = defaultUserDict["SERVER_TYPE"]["d"]
        for shouldKey in defaultUserDict:
            # 如果用户的config里没有这个值
            if shouldKey not in self.userconfigdict:
                self._fill_by_map_or_default(defaultUserDict, self.userconfigdict, shouldKey)

    def _check_software_config(self):
        """
        检查软件的config内的值是否有缺少，如果有，按照对应关系查找，如果没有，就用默认值
        """
        # 处理VERSION
        self.softwareconfigdict["NOWVERSION"] = self.NOWVERSION
        for shouldKey in defaultSoftwareDict:
            # 如果用户的config里没有这个值
            if shouldKey not in self.softwareconfigdict:
                self._fill_by_map_or_default(defaultSoftwareDict, self.softwareconfigdict, shouldKey)

    def save_config(self, file_path):
        with open(file_path, 'w', encoding="utf8") as f:
            json.dump(self.userconfigdict, f, indent=4, ensure_ascii=False)



config=MyConfigger()
"""
单例，导入后使用parse_user_config方法解析某个config
"""