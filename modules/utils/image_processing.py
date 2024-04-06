import cv2
from modules.utils.log_utils import logging
import math
from modules.configs.MyConfig import config
import numpy as np
from typing import Tuple
from pponnxcr import TextSystem
import time

ZHT = TextSystem('en')

def rotate_image_with_transparency(image_mat, angle):
    """
    给定一个包含透明层的图像Mat，将其旋转angle角度，返回旋转后的图像Mat

    """
    # 获取到图像的对角线长度
    diagonal = int(math.sqrt(pow(image_mat.shape[0], 2) + pow(image_mat.shape[1], 2)))
    # 创建一个diagonal * diagonal的空白含透明度的图像Mat
    rotated_image = np.zeros((diagonal, diagonal, 4), dtype=np.uint8)
    # 将原图像复制到新图像的中心
    x_offset = (diagonal - image_mat.shape[1]) // 2
    y_offset = (diagonal - image_mat.shape[0]) // 2
    rotated_image[y_offset:y_offset+image_mat.shape[0], x_offset:x_offset+image_mat.shape[1]] = image_mat
    # 获取rotated_image的高度、宽度和中心点
    center = (diagonal // 2, diagonal // 2)

    # 定义旋转矩阵
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    # 执行旋转，多出来的部分全透明
    rotated_image = cv2.warpAffine(rotated_image, rotation_matrix, (diagonal, diagonal), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_TRANSPARENT)
    # 返回中心和原图一样大小的区域
    return rotated_image[y_offset:y_offset+image_mat.shape[0], x_offset:x_offset+image_mat.shape[1]]


def match_pattern(sourcepic: str, patternpic: str,threshold: float = 0.9, show_result:bool = False, auto_rotate_if_trans = False) -> Tuple[bool, Tuple[float, float], float]:
    """
    Match the pattern picture in the source picture.
    
    If the pattern picture is a transparent picture, it will be rotated to match the source picture.
    """
    try:
        logging.debug("Matching pattern {} in {}".format(patternpic, sourcepic))
        screenshot = cv2.imread(sourcepic)
        
        pattern = cv2.imread(patternpic, cv2.IMREAD_UNCHANGED)  # 读取包含透明通道的模板图像
        have_alpha=False
        if(pattern.shape[2] == 4 and auto_rotate_if_trans):
            # 有透明度通道且开启了旋转匹配
            have_alpha = True
            best_max_val = -1
            best_max_loc = (0, 0)
            for i in range(-3, 4):
                degree = i
                # 旋转
                rotate_pattern = rotate_image_with_transparency(pattern, degree)
                # 以透明部分作为mask
                rotate_mask = rotate_pattern[:, :, 3]  # 透明通道
                rotate_mask[rotate_mask>0] = 255
                rotate_pattern = rotate_pattern[:, :, :3] # 去除透明通道
                # https://www.cnblogs.com/FHC1994/p/9123393.html
                result = cv2.matchTemplate(screenshot, rotate_pattern, cv2.TM_CCORR_NORMED, mask=rotate_mask)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                # print("角度为{}时，最大匹配值为{}".format(degree, max_val))
                if max_val>best_max_val:
                    best_max_val = max_val
                    best_max_loc = max_loc
            min_val, max_val, min_loc, max_loc = 0, best_max_val, 0, best_max_loc
        else:
            # 无旋转匹配
            # TODO： 多点匹配：https://pyimagesearch.com/2021/03/29/multi-template-matching-with-opencv/
            if pattern.shape[2] == 4:
                # 有透明度通道
                # 以透明部分作为mask
                pattern_mask = pattern[:, :, 3]  # 透明通道
                pattern_mask[pattern_mask>0] = 255
                pattern = pattern[:, :, :3] # 去除透明通道
                result = cv2.matchTemplate(screenshot, pattern, cv2.TM_CCOEFF_NORMED, mask=pattern_mask)
            else:
                # 无透明度通道
                result = cv2.matchTemplate(screenshot, pattern[:,:,:3], cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        h, w, _ = pattern.shape
        top_left = max_loc
        # get the center of the pattern
        center_x = top_left[0] + int(w / 2)
        center_y = top_left[1] + int(h / 2)
        if (show_result):
            bottom_right = (top_left[0] + w, top_left[1] + h)
            # draw a rectangle on the screenshot
            cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)
            # draw a circle on the center of the pattern
            cv2.circle(screenshot, (center_x, center_y), 10, (0, 0, 255), -1)
            print("max_val: ", max_val)
            cv2.imshow('Matched Screenshot', screenshot)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        if(max_val >= threshold  and max_val <=1 ):
            logging.debug("Pattern of {} and {} matched ({}). Center: ({}, {})".format(sourcepic, patternpic, max_val, center_x, center_y))
            return (True, (center_x, center_y), max_val)
        return (False, (0, 0), max_val)
    except cv2.error as e:
        logging.error(f"OpenCV 错误: {e}")
        raise  Exception # TODO 考虑增加全局错误计数器，统计严重错误和一般错误
        return (False, (0, 0), 0.01)
    except FileNotFoundError as e:
        logging.error(f'文件打开错误{e}')
        return (False, (0, 0), 0.01)
    except ValueError as e:
        logging.error(f"ValueError: {e}")
        return (False, (0, 0), 0.01)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        from BAAH import BAAH_check_adb_connect # 尝试解决和别的脚本冲突的问题
        BAAH_check_adb_connect()
        return (False, (0, 0), 0.01)
def ocr_pic_area(imageurl, fromx, fromy, tox, toy, multi_lines = False):
    """
    get the string in the image area
    
    axis in image is x: from left to right, y: from top to bottom
    
    """
    def replace_mis(ocr_text):
        """
        替换容易识别错误的字符
        """
        ocr_text = ocr_text.strip()
        ocr_text = ocr_text.replace("９", "9")
        return ocr_text

    rawImage = cv2.imread(imageurl)
    # cv2.imshow('Matched Screenshot', rawImage[fromy:toy, fromx:tox])
    # cv2.waitKey(0)
    if rawImage is None:
        if not multi_lines:
            return ["",0]
        else:
            return [["",0]]
    else:
        rawImage = rawImage[fromy:toy, fromx:tox]
        if not multi_lines:
            # 图像识别单行
            resstring = ZHT.ocr_single_line(rawImage)
            return [replace_mis(resstring[0]), resstring[1]]
        else:
            # 图像识别多行
            resstring_list = ZHT.detect_and_ocr(rawImage)
            return [[replace_mis(res.ocr_text), res.score] for res in resstring_list]
    
def match_pixel_color_range(imageurl, x, y, low_range, high_range, printit = False):
    """
    match whether the color at that location is between the range
    
    x, y: the location of the pixel in the cv image
    low_range: (120, 120, 120) bgr of a color
    high_range: (125, 125, 125) bgr of a color
    
    return True if the color is between the range
    """
    img = cv2.imread(imageurl)
    if img is None:
        if not img:
            return False
        else:
            return False
    pixel = img[y, x][:3]
    if printit:
        print("Pixel color at ({}, {}): {}".format(x, y, pixel))
    # logging.info(f"Pixel color at ({x}, {y}): {pixel}")
    if (pixel[0] >= low_range[0] and pixel[0] <= high_range[0] and pixel[1] >= low_range[1] and pixel[1] <= high_range[1] and pixel[2] >= low_range[2] and pixel[2] <= high_range[2]):
        return True
    return False
    
def compare_diff(img1, img2, xfocus, yfocus):
    """
    比较img1和img2的不同，返回这些不同的元素的中心点坐标列表
    
    Parameters
    ----------
    img1 : np.ndarray
        图片1
    img2 : np.ndarray
        图片2
    xignore : List[int]
        关注的x范围, 图片坐标
    yignore : List[int]
        关注的y范围, 图片坐标
    """
    # 忽略UI部分
    # xs = [1, 1279]
    # ys = [124, 568]
    xs=xfocus
    ys=yfocus
    
    img1 = img1[ys[0]:ys[1], xs[0]:xs[1]]
    img2 = img2[ys[0]:ys[1], xs[0]:xs[1]]
    # img3为差异图
    img3 = cv2.bitwise_xor(img1, img2)
    img3[img3 != 0] = 255
    # 缩横着的影子
    kernel = np.ones((20, 5), np.uint8)
    img4 = cv2.erode(img3, kernel)
    # 再缩5x5
    kernel = np.ones((5, 5), np.uint8)
    img4 = cv2.erode(img4, kernel)
    
    
    # 转换为gray灰度图
    gray = cv2.cvtColor(img4, cv2.COLOR_BGR2GRAY)
    # 寻找轮廓
    contours, hier = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    final_positions = []
    # 这里得到的contours是一个list，每个元素都是一个ndarray，是轮廓的坐标
    for cidx,cnt in enumerate(contours):
        # 其中，x是轮廓的左上角x坐标，y是轮廓的左上角y坐标，w是轮廓的宽度，h是轮廓的高度
        (x, y, w, h) = cv2.boundingRect(cnt)
        # print('RECT: x={}, y={}, w={}, h={}'.format(x, y, w, h))
        # 如果面积比100小，就忽略
        if cv2.contourArea(cnt) < 300:
            continue
        # 原图绘制圆形
        # cv2.rectangle(originimg2, pt1=(x+xs[0], y+ys[0]), pt2=(x+w+xs[0], y+h+ys[0]),color=(255, 0, 0), thickness=3)
        # 添加中心点到final_positions
        final_positions.append((x+xs[0]+w//2, y+ys[0]+h//2))
    return final_positions


drawing = False  # 检查是否正在绘制
start_x, start_y = -1, -1
quick_return_data = None
def screencut_tool(left_click = True, right_click = True, img_path = None, quick_return = False):
    """
    截图工具
    
    Parameters
    ----------
    left_click : bool
        是否开启左键点击事件
    right_click : bool
        是否开启右键点击事件
    img_data : np.ndarray
        图片数据
    quick_return : bool
        是否开启快速返回, 如果开启，点击右键后会返回坐标
    """
    global start_x, start_y, drawing, quick_return_data
    drawing = False  # 检查是否正在绘制
    start_x, start_y = -1, -1
    quick_return_data = None
    # 读取透明度层
    if not img_path:
        screenshot = cv2.imread("./{}".format(config.userconfigdict['SCREENSHOT_NAME']))
    else:
        screenshot = cv2.imread(img_path)
    # 平均最大最小bgr
    bgr_result = [[],[],[]]
    def mouse_callback_s(event, x, y, flags, param):
        # 截图
        global start_x, start_y, drawing, quick_return_data
        if right_click and event == cv2.EVENT_RBUTTONDOWN:  # 检查是否是鼠标右键键点击事件
            print(f"点击位置: ({x}, {y})", f"BGR 数组: {screenshot[y, x]}")
            bgr_result[0].append(screenshot[y, x][0])
            bgr_result[1].append(screenshot[y, x][1])
            bgr_result[2].append(screenshot[y, x][2])
            print("min max avg bgr: ", np.min(bgr_result, axis=1), np.max(bgr_result, axis=1), np.mean(bgr_result, axis=1))
            
            if quick_return:
                quick_return_data = [x, y]
                cv2.destroyAllWindows()
            
        if left_click and event == cv2.EVENT_LBUTTONDOWN:  # 检查是否是鼠标左键按下事件
            drawing = True
            start_x, start_y = x, y
        elif left_click and event == cv2.EVENT_MOUSEMOVE:  # 检查是否是鼠标移动事件
            if drawing:
                screenshot_copy = screenshot.copy()  # 创建截图的副本
                cv2.rectangle(screenshot_copy, (start_x, start_y), (x, y), (0, 255, 0), 2)
                cv2.imshow('Matched Screenshot', screenshot_copy)
        elif event == cv2.EVENT_LBUTTONUP:  # 检查是否是鼠标左键释放事件
            drawing = False
            end_x, end_y = x, y
            # cv2.rectangle(screenshot, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
            cv2.imshow('Matched Screenshot', screenshot)

            # 保存截取的区域到当前目录
            selected_region = screenshot[min(start_y,end_y):max(start_y,end_y), min(start_x,end_x):max(start_x,end_x)]
            nowstr = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
            filename = "selected_"+nowstr+".png"
            cv2.imwrite(filename, selected_region)
            print(f"选定区域已被保存为/Saved as {filename}")
            
            if quick_return:
                quick_return_data = filename
                cv2.destroyAllWindows()

    cv2.imshow('Matched Screenshot', screenshot)
    cv2.setMouseCallback("Matched Screenshot", mouse_callback_s)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    if quick_return:
        return quick_return_data