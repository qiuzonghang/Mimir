# -*- coding: utf-8 -*-
# @Time   : 2022/8/2 10:40
# @Author : qiuzonghang
# @File   : conftest.py

from Mimir.qz_auto_test.Params.params import get_param_data
from qz_auto_test.Common.Func import remove_dir
from Mimir.qz_auto_test.Conf.Config import Config
import pytest
import os
import pymssql

conf = Config()


@pytest.fixture(scope='class')
def get_JYZZ_param():
    # return get_param_data(uri_type='JYZZ', user=conf.wangye_username, pw=conf.wangye_password)
    return get_param_data(uri_type='JYZZ', user=conf.wangye_username, pw=conf.wangye_password)


@pytest.fixture(scope='class')
def get_dev_sql_server():
    conn = pymssql.connect('118.178.93.112', 'cx', '1qaz2wsx!QAZ@WSX', 'GSMDB')
    cur = conn.cursor()
    yield cur
    conn.commit()
    cur.close()
    conn.close()
