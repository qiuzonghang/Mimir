# -*- coding: utf-8 -*-
# @Time   : 2022/7/31 20:52
# @Author : qiuzonghang
# @File   : base.py


import time
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

"""

class Base:

    def __init__(self, driver):
        self.driver = driver
        log.info("[base]: 正在获取初始化driver对象:{}".format(driver))

    # 查找元素方法 封装
    def base_find(self, loc,  timeout=20, poll=0.5):
        log.info("[base]: 正在定位:{} 元素".format(loc))
        # 使用显示等待查找元素
        return WebDriverWait(self.driver,
                             timeout=timeout,
                             poll_frequency=poll).until(lambda x:x.find_element(*loc))

    # 点击元素方法
    def base_click(self, loc):
        log.info("[base]: 正在对:{} 元素实行点击事件".format(loc))
        el = self.base_find(loc)
        el.click()

    # 输入元素方法
    def base_input(self, loc, value):
        log.info("[base]: 正在对:{} 元素输入{}".format(loc,value))
        # 获取元素
        el = self.base_find(loc)
        # 清空
        el.clear()
        # 输入
        el.send_keys(value)

    # 获取文本信息
    def base_get_text(self, loc):
        log.info("[base]: 正在获取:{} 元素文本值".format(loc))
        a = self.base_find(loc).text
        return a

    # 截图方法
    def base_get_image(self):
        log.info("[base]: 程序出错，调用截图")
        self.driver.get_screenshot_as_file(path + "/截图{}.png".format(time.strftime("%Y_%m_%d %H_%M_%S")))

    # 判断元素是否存方法
    def base_element_is_exist(self, loc):
        try:
            self.base_find(loc)
            log.info("[base]: {} 元素查找成功，存在页面".format(loc))
            return True # 代表元素存在
        except:
            log.info("[base]: {} 元素查找失败，不存在当前页面".format(loc))
            return False # 代表元素不存在


    # 切换到新的页面
    def base_handle(self):
        sleep(1)
        log.info("[base]:  切换到新的页面")
        h = self.driver.current_window_handle
        hs = self.driver.window_handles
        for newh in hs:
            if newh != h:
                self.driver.switch_to.window(newh)

    # 获取所有句柄并调换到第一个句柄页
    def base_get_handle(self):
        self.driver.switch_to.window(self.driver.window_handles[0])

    # 获取alert错误提示
    def base_cuowutishi(self):
        tishi = self.driver.switch_to.alert.text
        return tishi

    # 跳过alert错误提示
    def base_tiaoguotishi(self):
        self.driver.switch_to.alert.dismiss()

    # 鼠标悬停
    def base_shubiao_xuanting(self,loc):
        log.info("[base]: 鼠标悬停{}元素 ".format(loc))
        el = self.base_find(loc)
        ActionChains(self.driver).move_to_element(el).perform()

    # 鼠标移动元素-坐标
    def base_shubiao_yidong(self, loc,x,y):
        log.info("[base]: 鼠标悬停{}元素 ".format(loc))
        el = self.base_find(loc)
        ActionChains(self.driver).drag_and_drop_by_offset(el,x,y).perform()


    # 切换frame表单方法
    def base_switch_frame(self,loc):
        log.info("[base]: 切换到 {} frame表单".format(loc))
        el = self.driver.base_find(loc)
        self.driver.switch_to.frame(el)

    # 回到默认目录方法
    def base_default_content(self):
        log.info("[base]: 回到默认目录")
        self.driver.switch_to.default_content()


    # 上传文件-用于批导功能，输入绝对路径 "E:\q.xlsx""E:\a.xlsx"
    def base_send_dump(self,loc, browser_type="chrome"):
        log.info("[base]: 正在通过win32上传文件")
        if browser_type == "chrome":
            title = "打开"
        else:
            title = ""
        # 找元素
        # 一级窗口"#32770","打开"
        dialog = win32gui.FindWindow("#32770", title)
        #
        ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, "ComboBoxEx32", None)  # 二级
        comboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, "ComboBox", None)  # 三级
        # 编辑按钮
        edit = win32gui.FindWindowEx(comboBox, 0, 'Edit', None)  # 四级
        # 打开按钮
        button = win32gui.FindWindowEx(dialog, 0, 'Button', "打开(&O)")  # 四级
        # 往编辑当中，输入文件路径 。
        win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, loc)  # 发送文件路径
        win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 点击打开按钮

    # 聚焦元素-跳转到指定元素处
    def base_jump_target(self,loc):
        log.info("[base]: 跳转到-{}-元素位置".format(loc))
        a = self.driver.base_find(loc)
        self.driver.execute_script("arguments[0].scrollIntoView();", a)

"""