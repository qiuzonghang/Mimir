# -*- coding: utf-8 -*-
# @Time   : 2022/7/31 16:15
# @Author : qiuzonghang
# @File   : Func.py

import time

import selenium.common.exceptions
from selenium.webdriver.common.by import By
# from selenium import webdriver
from Mimir.qz_auto_test.Common.Log import MyLog
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver
from Mimir.qz_auto_test.Conf.Config import Config
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
def write_txt(text, user_name='', env='dev'):
    file_path = project_path + '/Data/token.txt'
    if user_name != '':
        user = user_name.split('@')
        file_path = project_path + '/Data/%s_%s_token.txt' % (env, user[0])
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(text + '\n')
        f.close()


# 读txt文件
def read_txt(file_path=project_path + '/Data/token.txt', user_name='', env='dev'):
    if user_name != '':
        user = user_name.split('@')
        file_path = project_path + '/Data/%s_%s_token.txt' % (env, user[0].lower())
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            txt_result = f.readlines()
            return txt_result
    except FileNotFoundError:
        write_txt(text='test', user_name=user_name, env=env)
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
        if r.status_code == 200 and r.json().get('data').get('email').casefold() == user.casefold():
            return True, r.json()
        else:
            return False, {}
    except:
        return False, {}


# 登录token获取
def get_access_token(username, password, env):
    """
    :param username:    # 登录用户名
    :param password:    # 用户密码
    :param url:     # 登录网址
    :param env:     # 登录环境
    :return:    # 返回token+host
    """
    if env == 'dev':
        host = conf.host_dev
        url = 'https://' + host + '/#/work'
    elif env == 'uat':
        host = conf.host_uat
        url = 'https://' + host + '/#/work'
    elif env == 'release':
        host = ''
    else:
        raise

    run_type, user_info = check_token(re.sub('\n', '', read_txt(user_name=username, env=env)[-1]), username, host)
    if run_type is False:      # 检查token是否正确
        dr = base.start_dr(url=re.sub('api', '', url), driver_name='chrome')   # open chrome
        base.user_login(username, password)     # login
        time.sleep(10)
        for request in dr.requests:     # 登录后获取token
            if request.response:
                if 'Bearer' in str(request.headers['authorization']):
                    write_txt(str(request.headers['authorization']), user_name=username, env=env)
                    break
        log.info('获取token，退出浏览器...')
        dr.quit()
        run_type, user_info = check_token(re.sub('\n', '', read_txt(user_name=username, env=env)[-1]), username, host)
        if run_type:   # 登录后获取的token是否正确
            return re.sub('\n', '', read_txt(user_name=username, env=env)[-1]), host, user_info
        else:
            raise EOFError
    else:
        return re.sub('\n', '', read_txt(user_name=username, env=env)[-1]), host, user_info      # 文件中的token


def remove_dir(filepath):
    log.info('对上一次测试报告进行清理')
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)

