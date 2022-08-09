# -*- coding: utf-8 -*-
# @Time   : 2022/8/5 11:50
# @Author : qiuzonghang
# @File   : test_add_GWYC.py

import allure
import pytest


@pytest.mark.usefixtures('get_JYZZ_param')
class TestCase:

    pass


if __name__ == '__main__':
    pytest.main(['-s', '-v'])