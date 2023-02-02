# -*- coding: utf-8 -*-
# @Time   : 2023/1/31 15:00
# @Author : qiuzonghang
# @File   : test_apply_emba_login.py


from qz_auto_test.Common.Log import MyLog
from qz_auto_test.Common.Assert import Assertions
from qz_auto_test.Params.params import arr_sql_param, arr_sql_title
import allure
import pytest
import time

log = MyLog()
test = Assertions()


@pytest.mark.parametrize('open_apply')
class TestCase:

    def test_apply(self, open_apply):
        test = open_apply


if __name__ == '__main__':
    pytest.main(['-v', '-s'])