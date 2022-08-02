# -*- coding: utf-8 -*-
# @Time   : 2022/7/31 16:15
# @Author : qiuzonghang
# @File   : Func.py

import time

import selenium.common.exceptions
from selenium.webdriver.common.by import By
# from selenium import webdriver
from qz_auto_test.Common.Log import MyLog
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver
from qz_auto_test.Conf.Config import Config
import os
import requests
import re
import shutil

log = MyLog()
project_path = os.path.abspath(os.path.dirname(
                                 os.path.dirname(__file__)))
conf = Config()


class Driver:
    def __init__(self):
        self.username = (By.ID, 'i0116')
        self.password = (By.ID, 'i0118')
        self.username_next = (By.ID, 'idSIButton9')
        self.sign_in = (By.XPATH, '//*[@id="idSIButton9"]')
        self.whether = (By.ID, 'idBtn_Back')

    def start_dr(self, url, driver_name, over_time=30):
        """
        :param url:     # 登录网址
        :param driver_name:     # 需要调用的浏览器（chrome/firefox)
        :return:
        """
        if driver_name == 'chrome':
            self.dr = webdriver.Chrome()
            log.info('open chrome...')
        elif driver_name == 'firefox':
            self.dr = webdriver.Firefox()
            log.info('open firefox')
        else:
            log.error('目前仅支持Chrome/Firefox')
            raise
        self.dr.get(url)
        self.dr.maximize_window()
        # self.dr.implicitly_wait(over_time)
        log.info('打开url，窗口最大化，隐式等待%ss' % over_time)
        return self.dr

    # 显式等待
    def base_find(self, loc, timeout=30, poll=0.5, dr=None):
        log.info('正在定位:{}元素'.format(loc))
        if dr is None:
            dr = self.dr
        try:
            location = WebDriverWait(dr, timeout=timeout, poll_frequency=poll).until(EC.presence_of_element_located(loc))
            return location
        except selenium.common.exceptions.TimeoutException:
            log.error('元素定位超时！')
        except selenium.common.exceptions.StaleElementReferenceException:
            log.error('未定位到元素！')

    # 点击元素方法
    def base_click(self, loc):
        log.info("正在对:{} 元素实行点击事件".format(loc))
        el = self.base_find(loc)
        time.sleep(3)
        el.click()

    # 输入元素方法
    def base_input(self, loc, value):
        log.info("正在对:{} 元素输入{}".format(loc, value))
        el = self.base_find(loc)
        # el.clear()
        el.send_keys(value)

    # 获取文本信息
    def base_get_text(self, loc):
        log.info("正在获取:{} 元素文本值".format(loc))
        a = self.base_find(loc).text
        return a

    # 登录
    def user_login(self, username, password):
        self.base_input(loc=self.username, value=username)
        self.base_click(loc=self.username_next)
        self.base_input(loc=self.password, value=password)
        time.sleep(3)
        self.base_click(loc=self.sign_in)
        self.base_click(loc=self.whether)


base = Driver()

"""
class LoginClass:
    def __int__(self):
        pass
        
    def set_username(self, driver, username):
        driver.send_keys(username)
        driver.find_element(*Driver.LoginClass.username_next).click()

    def set_password(self, driver, password):
        driver.find_element(*Driver.LoginClass.password).send_keys(password)
        time.sleep(5)
        driver.find_element(*Driver.LoginClass.sign_in).click()
        time.sleep(5)
        driver.find_element(*Driver.LoginClass.whether).click()
    
    def user_login(self, username, password):
        base.base_input(loc=self.username, value=username)
        base.base_click(loc=self.username_next)
        base.base_input(loc=self.password, value=password)
        base.base_click(loc=self.sign_in)
        base.base_click(loc=self.whether)

"""


# 写txt文件
def write_txt(text):
    with open(project_path + '/Data/token.txt', 'a', encoding='utf-8') as f:
        f.writelines(text + '\n')
        f.close()


# 读txt文件
def read_txt(file_path=project_path + '/Data/token.txt'):
    with open(file_path, 'r', encoding='utf-8') as f:
        txt_result = f.readlines()
        return txt_result


# 检查token是否过期、是否与登录账号一致
def check_token(access_token, user, host):
    """
    :param access_token:    # 需要验证的token
    :param user:    # token对应的用户名
    :param host:    # 对应的环境
    :return:
    """
    url = 'https://' + host + '/api/user/info'
    header = {'authorization': access_token}
    r = requests.get(url=url, headers=header)
    try:
        if r.status_code == 200 and r.json().get('data').get('email') == user:
            return True
        else:
            return False
    except:
        return False


# 登录token获取
def get_access_token(username, password, url, env):
    """
    :param username:    # 登录用户名
    :param password:    # 用户密码
    :param url:     # 登录网址
    :param env:     # 登录环境
    :return:    # 返回token+host
    """
    if env == 'dev':
        host = conf.host_dev
    elif env == 'uat':
        host = ''
    elif env == 'release':
        host = ''
    else:
        raise
    if check_token(re.sub('\n', '', read_txt()[-1]), username, host) is False:      # 检查token是否正确
        dr = base.start_dr(url=url, driver_name='chrome')   # open chrome
        base.user_login(username, password)     # login
        time.sleep(5)
        for request in dr.requests:     # 登录后获取token
            if request.response:
                if 'Bearer' in str(request.headers['authorization']):
                    write_txt(str(request.headers['authorization']))
                    break
        log.info('获取token，退出浏览器...')
        dr.quit()
        if check_token(re.sub('\n', '', read_txt()[-1]), username, host):   # 登录后获取的token是否正确
            return re.sub('\n', '', read_txt()[-1]), host
        else:
            raise 'Get Token Error!'
    else:
        return re.sub('\n', '', read_txt()[-1]), host       # 文件中的token


def remove_dir(filepath):
    log.info('对上一次测试报告进行清理')
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)

# print(get_access_token(username='tester1@qynet.onmicrosoft.com', password='Qz123456.'))