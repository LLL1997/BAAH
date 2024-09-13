import sys
import os
<<<<<<< HEAD
=======
from time import sleep, strftime
>>>>>>> e7da5a2baec6560ca7c05328828f6d271b96d187

# 将当前脚本所在目录添加到模块搜索路径
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_dir)


if __name__ in ["__main__", "__mp_main__"]:
    try:
        # config logging before all imports
        from modules.utils.log_utils import logging
        # 从命令行参数获取要运行的config文件名，并将config实例parse为那个config文件
        from modules.configs.MyConfig import config

        logging.info({"zh_CN": f"当前运行目录: {os.getcwd()}", "en_US": f"Current running directory: {os.getcwd()}"})
        now_config_files = config.get_all_user_config_names()
        logging.info({"zh_CN": "BAAH_CONFIGS可用的配置文件: " + ", ".join(now_config_files), "en_US": "Available BAAH_CONFIGS config files: " + ", ".join(now_config_files)})

        if len(sys.argv) > 1:
            config_name = sys.argv[1]
            logging.info({"zh_CN": f"读取指定的配置文件: {config_name}", "en_US": f"loading config from {config_name}"})
            if config_name not in now_config_files:
                logging.error({"zh_CN": "输入的配置文件名不在可用配置文件列表中", "en_US": "The entered config file name is not in the list of available config files"})
                raise FileNotFoundError(f"config file {config_name} not found")

            config.parse_user_config(config_name)
        else:
            logging.warn({"zh_CN": "启动程序时没有指定配置文件", "en_US": "No config file specified when starting the program"})
            if len(now_config_files) == 1:
                logging.info({"zh_CN": "自动读取唯一的配置文件", "en_US": "Automatically read the only config file"})
                config_name = now_config_files[0]
            else:
                while(1):
                    logging.info({"zh_CN": "请手动输入要运行的配置文件名(包含.json后缀)", "en_US": "Please enter the config file name to run (including .json suffix)"})
                    config_name = input(": ")
                    if config_name in now_config_files:
                        break
                    else:
                        logging.warn({"zh_CN": "输入的配置文件名不在可用配置文件列表中", "en_US": "The entered config file name is not in the list of available config files"})
            logging.info({"zh_CN": f"读取指定的配置文件: {config_name}", "en_US": f"loading config from {config_name}"})
            config.parse_user_config(config_name)
        # 按照该配置文件，运行BAAH
        # 加载my_AllTask，BAAH_main，create_notificationer
        # 以这时的config构建任务列表
        from BAAH import BAAH_main, my_AllTask, create_notificationer

        # 不带GUI运行
        BAAH_main()
    
        # config历史列表
        config_history = [configname]
        while True:
            logging.debug("config历史列表: "+ ",".join(config_history))

            #开始前发送钉钉 
            from modules.utils.msg import push_msg_fast
            push_msg_fast(f"游戏，{config.configdict['ACTIVITY_PATH']},BAAH运行")


            BAAH_main()

            # 添加退出模拟器
            from modules.utils.add_function import close_emulator
            import re
            configname = "config.json"
            from modules.utils.MyConfig import config
            # 从config里得到路径
            emulator_path=config.configdict['TARGET_EMULATOR_PATH']
            print('print(emulator_path)',emulator_path)
            emulator_path=str(emulator_path)
            print('print(emulator_path)1',emulator_path)

            # 文件名
            emulator_file_name = re.search(r'/([^/]+\.exe)', emulator_path)
            print(emulator_file_name)
            emulator_file_name = emulator_file_name.group(1)
            print(emulator_file_name)
            # 地址
            # emulator_path = re.search(r'/(.+)\.exe', emulator_path)
            emulator_path = re.search(r'^(.*?/)MuMuPlayer\.exe', emulator_path)
            print(emulator_path)
            emulator_path=emulator_path.group(1)
            print(emulator_path)

            # 尝试提取多开的模拟器编号 
            # 使用正则表达式匹配 -v 后的数字
            # 从config里得到路径 后面再优化
            full_value=config.configdict['TARGET_EMULATOR_PATH']
            print('print(emulator_path)',full_value)
            match = re.search(r'-v\s+(\d+)', full_value)

            if match:
                try:
                    emulator_number = int(match.group(1))
                    print(emulator_path)
                    print(emulator_file_name)
                    print(f"找到多开的模拟器编号：{emulator_number}")
                    close_emulator(emulator_path,emulator_file_name,emulator_number)
                except Exception:
                    pass
            else:
                print(emulator_path)
                print(emulator_file_name)
                close_emulator(emulator_path,emulator_file_name)
            push_msg_fast(f"游戏，{config.configdict['ACTIVITY_PATH']},BAAH运行结束,")
            # 判断config里是否有next_config文件
            if hasattr(config, 'NEXT_CONFIG') and len(config.NEXT_CONFIG) > 0:
                # 有的话，更新配置项目
                logging.debug("检测到next_config文件: "+config.NEXT_CONFIG)
                if config.NEXT_CONFIG in config_history:
                    raise Exception("检测到循环运行，请避免config死循环嵌套")
                # 将新的config文件加入config_history, 防止死循环
                config_history.append(config.NEXT_CONFIG)
                # 清空config实例,读取next_config文件，再次运行BAAH_main()
                config.parse_config(config.NEXT_CONFIG)
                # 清空my_AllTask实例，通过新的config构造新的my_AllTask
                my_AllTask.parse_task()
            else:
                break
    except Exception as e:
        import traceback
        traceback.print_exc()
        # 用于GUI识别是否结束的关键字
        print("GUI_BAAH_TASK_END")
        input("Error, Enter to exit/错误，回车退出:")
