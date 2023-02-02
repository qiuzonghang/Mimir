# -*- coding: utf-8 -*-
# @Time   : 2022/7/31 16:15
# @Author : qiuzonghang
# @File   : Func.py

import time
import zipfile

import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium import webdriver as wd
from selenium.webdriver.chrome.service import Service as chromeService
from selenium.webdriver.firefox.service import Service as firefoxService
from selenium.webdriver.edge.service import Service as edgeService
from qz_auto_test.Common.Log import MyLog
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver as wd_wire
from qz_auto_test.Conf.Config import Config
from qz_auto_test.Params.get_yaml import GetPages
import os
import requests
import re
import shutil

log = MyLog()
project_path = os.path.abspath(os.path.dirname(
                                 os.path.dirname(__file__)))
conf = Config()
get_data = GetPages()


class Driver:
    def __init__(self):
        self.username = (By.ID, 'i0116')
        self.password = (By.ID, 'i0118')
        self.username_next = (By.ID, 'idSIButton9')
        self.sign_in = (By.XPATH, '//*[@id="idSIButton9"]')
        self.whether = (By.ID, 'idBtn_Back')

    def start_dr(self, url, driver_name, over_time=30, type='api'):
        """
        :param url:     # 登录网址
        :param driver_name:     # 需要调用的浏览器（chrome/firefox)
        :return:
        """
        if type == 'api':
            if driver_name == 'chrome':
                self.dr = wd_wire.Chrome()
                log.info('open chrome...')
            elif driver_name == 'firefox':
                self.dr = wd_wire.Firefox()
                log.info('open firefox')
            else:
                log.error('api框架目前仅支持Chrome/Firefox')
                raise
        elif type == 'web':
            driver_path = os.path.abspath(os.path.join(os.getcwd(), "..")) + '/WebDriver/'
            if driver_name == 'chrome':
                self.dr = wd.Chrome(service=chromeService(driver_path + 'chromedriver.exe'))
                log.info('open chrome...')
            elif driver_name == 'firefox':
                self.dr = wd.Firefox(service=firefoxService(driver_path + 'geckodriver.exe'))
                log.info('open firefox...')
            elif driver_name == 'edge':
                self.dr = wd.Edge(service=edgeService(driver_path + 'msedgedriver.exe'))
                log.info('open edge...')
            else:
                log.error('web框架目前仅支持Chrome/Firefox/Edge')
                raise
        else:
            log.error('请正确填写应用框架api/web')
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
        # time.sleep(3)
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
        time.sleep(3)
        self.base_click(loc=self.username_next)
        time.sleep(3)
        self.base_input(loc=self.password, value=password)
        time.sleep(3)
        self.base_click(loc=self.sign_in)
        self.base_click(loc=self.whether)


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
    print(header)
    r = requests.get(url=url, headers=header)
    print(r.json())
    try:
        if r.status_code == 200 and r.json().get('data').get('email').casefold() == user.casefold():
            return True, r.json()
        else:
            return False, {}
    except:
        return False, {}


# 登录token获取
def get_access_token(username, password, env, get_mode='api'):
    """
    :param username:    # 登录用户名
    :param password:    # 用户密码
    :param url:     # 登录网址
    :param env:     # 登录环境
    :return:    # 返回token+host
    """
    base = Driver()
    if env == 'dev':
        host = conf.host_dev
        web_url = 'https://' + host + '/#/work'
    elif env == 'test':
        host = conf.host_test
        web_url = 'https://' + host + '/#/work'
    elif env == 'uat':
        host = conf.host_uat
        web_url = 'https://' + host + '/#/work'
    elif env == 'release':
        host = ''
    else:
        raise

    run_type, user_info = check_token(re.sub('\n', '', read_txt(user_name=username, env=env)[-1]), username, host)
    if run_type is False:      # 检查token是否正确
        if get_mode == 'web':
            dr = base.start_dr(url=re.sub('api', '', web_url), driver_name='chrome')   # open chrome
            base.user_login(username, password)     # login
            time.sleep(10)
            for request in dr.requests:     # 登录后获取token
                if request.response:
                    if 'Bearer' in str(request.headers['authorization']):
                        write_txt(str(request.headers['authorization']), user_name=username, env=env)
                        break
            log.info('获取token，退出浏览器...')
            dr.quit()
        elif get_mode == 'api':     # 仅支持 test&dev环境接口获取token
            token_param = get_data.get_page_list()['Token'][0]
            token_url = token_param['token_url']
            if env == 'dev' or env == 'test':
                token_data = token_param['dev_token_data']
            else:
                raise
            token_data['username'] = username
            token_data['password'] = password
            r = requests.post(url=token_url, data=token_data)
            if r.status_code != 200:
                raise
            else:
                token_response = r.json()
                write_txt('%s %s' % (token_response.get('token_type'), token_response.get('access_token')), user_name=username, env=env)
        run_type, user_info = check_token(re.sub('\n', '', read_txt(user_name=username, env=env)[-1]), username, host)
        print(run_type)
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


def zipDir(dirpath, outFullName):
    zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        # fpath = path.replace(dirpath, '')
        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(filename))
    zip.close()


def get_conf_info(env):
    if env == 'dev' or env == 'test':
        username = conf.tester3_username_dev  # ExEd
        password = conf.tester3_password_dev
        username_emba = conf.wangye_username_dev  # EMBA
        password_emba = conf.wangye_password_dev
        if env == 'dev':
            sql_server_host = conf.sql_server_host_dev
            sql_server_database = conf.sql_server_database_dev
            sql_server_username = conf.sql_server_username_dev
            sql_server_password = conf.sql_server_password_dev
        elif env == 'test':
            sql_server_host = conf.sql_server_host_test
            sql_server_database = conf.sql_server_database_test
            sql_server_username = conf.sql_server_username_test
            sql_server_password = conf.sql_server_password_test
    elif env == 'uat':
        username = conf.ITtest2_username_uat  # ExEd
        password = conf.ITtest2_password_uat
        username_emba = conf.ITtest3_username_uat  # EMBA
        password_emba = conf.ITtest3_password_uat
        sql_server_host = conf.sql_server_host_uat
        sql_server_database = conf.sql_server_database_uat
        sql_server_username = conf.sql_server_username_uat
        sql_server_password = conf.sql_server_password_uat
    return (username, password, username_emba, password_emba, sql_server_host, sql_server_database, sql_server_username, sql_server_password)


# base = Driver()
# test = base.start_dr(url='https://testsite.qintelligence.cn/#/work', driver_name='edge', type='web')
# user_info = get_conf_info(env='test')
# base.user_login(username=user_info[2], password=user_info[3])
# time.sleep(10)
# test.quit()

