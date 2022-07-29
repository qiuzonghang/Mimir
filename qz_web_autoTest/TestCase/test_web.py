# -*- coding: utf-8 -*-
# @Time   : 2022/7/28 11:05
# @Author : qiuzonghang
# @File   : test_web.py


import pytest
import allure
import time
import seleniumbase
from selenium.webdriver.common.by import By
from qz_web_autoTest.Common.func import Driver


@pytest.mark.usefixtures('start_off_web')
class TestCase:

    def test_case(self, start_off_web):
        print(start_off_web)


if __name__ == '__main__':
    pytest.main(['-s', '-v'])

