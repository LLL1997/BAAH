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
        
        configname = "config.json"
        from modules.utils.MyConfig import config
        logging.info("读取默认config文件: "+configname)
        if len(sys.argv) > 1:
            configname = sys.argv[1]
<<<<<<< HEAD
            config.parse_config(configname)
            logging.info("重新读取指定的config文件: "+configname)
        logging.info(f"模拟器:{config.configdict['TARGET_EMULATOR_PATH']}")
        logging.info(f"端口:{config.configdict['TARGET_PORT']}")

        import base64
        import traceback
        from BAAH import BAAH_main
        from modules.AllTask.myAllTask import my_AllTask
        
        # 打印BAAH信息
        print("+"+"BAAH".center(80, "="), "+")
        print("||"+f"Version: {config.NOWVERSION}".center(80, " ")+"||")
        print("||"+"Bilibili: https://space.bilibili.com/7331920".center(80, " ")+"||")
        print("||"+"Github: https://github.com/sanmusen214/BAAH".center(80, " ")+"||")
        print("||" + "QQ群: 441069156".center(80, " ") + "||")
        print("||"+"".center(80, " ")+"||")
        print("+"+"".center(80, "=")+"+")
    
=======
            logging.info("读取指定的config文件: "+configname)
            config.parse_user_config(configname)
        else:
            configname = "config.json"
            logging.info("读取默认config文件: "+configname)
            config.parse_user_config(configname)

        from BAAH import BAAH_main, my_AllTask, create_notificationer
        
        # 打印BAAH信息
        print_BAAH_start()
        
        # 打印config信息
        logging.info(f"读取的config文件: {configname}")
        logging.info(f"模拟器:{config.userconfigdict['TARGET_EMULATOR_PATH']}")
        logging.info(f"端口:{config.userconfigdict['TARGET_PORT']}")
        logging.info(f"区服:{config.userconfigdict['SERVER_TYPE']}")
>>>>>>> e7da5a2baec6560ca7c05328828f6d271b96d187

        # 不带GUI运行
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
        # 打印完整的错误信息
        traceback.print_exc()
        print_BAAH_finish()
<<<<<<< HEAD
        # input("按回车键继续:")
=======
        # 发送错误通知邮件
        if config.userconfigdict["ENABLE_MAIL_NOTI"]:
            logging.info("发送错误通知邮件")
            try:
                # 构造通知对象
                notificationer = create_notificationer()
                # 构造邮件内容
                content = []
                content.append("BAAH任务出现错误")
                content.append("配置文件名称: "+config.nowuserconfigname)
                content.append("游戏区服: "+config.userconfigdict["SERVER_TYPE"])
                content.append("错误信息: "+str(e))
                print(notificationer.send("\n".join(content)))
                logging.info("邮件发送结束")
            except Exception as eagain:
                logging.error("发送邮件失败")
                logging.error(eagain)
        # input("出现错误，按回车键退出:")
>>>>>>> e7da5a2baec6560ca7c05328828f6d271b96d187
        raise Exception("运行出错")
    # 运行结束后，删除截图文件
    try:
        # 如果截图文件存在，删除截图文件
        if os.path.exists(f"./{config.SCREENSHOT_NAME}"):
            os.remove(f"./{config.SCREENSHOT_NAME}")
    except:
        pass
    print("程序运行结束，如有问题请加群(441069156)反馈，在Github上检查下是否有版本更新")
    print("https://github.com/sanmusen214/BAAH")


    from modules.utils.msg import push_msg_fast
    push_msg_fast(f"所有游戏，BAAH运行结束,")
    # input("按回车键退出BAAH:")
