# -*- coding: utf-8 -*-
# @Time   : 2022/7/28 11:37
# @Author : qiuzonghang
# @File   : func.py
import time

from selenium.webdriver.common.by import By
from selenium import webdriver
from qz_web_autoTest.Common.Log import MyLog
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

log = MyLog()


class Driver:
    def __init__(self):
        pass

    def start_dr(self, url, driver_name, over_time=15):
        """
        :param url:
        :param driver_name:
        :return:
        """
        if driver_name == 'chrome':
            dr = webdriver.Chrome()
            log.info('open chrome...')
        elif driver_name == 'firefox':
            dr = webdriver.Firefox()
            log.info('open firefox')
        else:
            log.error('目前仅支持Chrome/Firefox')
            raise
        dr.get(url)
        dr.maximize_window()
        dr.implicitly_wait(over_time)
        log.info('打开url，窗口最大化，隐式等待%ss' % over_time)
        return dr

    def base_find(self, loc, driver, timeout=20, poll=0.5):
        log.info('正在定位:%s元素' % loc)
        return WebDriverWait(driver, timeout=timeout, poll_frequency=poll).until(lambda x: x.find_element(*loc))

    def base_click(self, loc):
        pass

    class LoginClass:
        # def __int__(self):
        username = (By.ID, 'i0116')
        password = (By.ID, 'i0118')
        username_next = (By.ID, 'idSIButton9')
        sign_in = (By.XPATH, '//*[@id="idSIButton9"]')
        whether = (By.ID, 'idBtn_Back')

        def set_username(self, driver, username):
            driver.find_element(*Driver.LoginClass.username).send_keys(username)
            driver.find_element(*Driver.LoginClass.username_next).click()

        def set_password(self, driver, password):
            driver.find_element(*Driver.LoginClass.password).send_keys(password)
            time.sleep(3)
            driver.find_element(*Driver.LoginClass.sign_in).click()
            time.sleep(3)
            driver.find_element(*Driver.LoginClass.whether).click()
