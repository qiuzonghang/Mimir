# -*- coding: utf-8 -*-
# @Time   : 2022/7/28 11:02
# @Author : qiuzonghang
# @File   : conftest.py

import pytest
import time
import os
import re
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from qz_web_autoTest.Common.func import Driver
from qz_web_autoTest.Common.Log import MyLog

log = MyLog()
driver_class = Driver()
login = driver_class.LoginClass()


@pytest.fixture(scope='function')
def start_off_web():
    log.info('------------start-----------')
    dr = driver_class.start_dr(url='https://devsite.qintelligence.cn/#/work', driver_name='firefox')
    login.set_username(driver=dr, username='wangye@qynet.onmicrosoft.com')
    login.set_password(driver=dr, password='Welcome@1')
    yield dr, driver_class
    time.sleep(5)
    dr.quit()
    log.info('-------------end-------------')


@pytest.fixture(scope='function')
def test():
    return 1


# @pytest.fixture(scope='function')





