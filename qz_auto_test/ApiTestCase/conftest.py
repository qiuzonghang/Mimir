# -*- coding: utf-8 -*-
# @Time   : 2022/8/2 10:40
# @Author : qiuzonghang
# @File   : conftest.py

import sys
import os
import re
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from qz_auto_test.Params.params import get_param_data
from qz_auto_test.Common.Func import remove_dir
from qz_auto_test.Conf.Config import Config
from qz_auto_test.Common.Func import get_access_token, get_conf_info
import pytest
import pymssql

env = 'test'
username, password, username_emba, password_emba, sql_server_host, sql_server_database, sql_server_username, sql_server_password = get_conf_info(env=env)


@pytest.fixture(scope='class')
def get_JYZZ_param():       # 默认是ExEd账号
    return get_param_data(uri_type='JYZZ', user=username, pw=password, env=env)


@pytest.fixture(scope='class')
def get_GWYC_param():
    return get_param_data(uri_type='GWYC', user=username, pw=password, env=env)


@pytest.fixture(scope='class')
def get_emba_token():       # EMBA账号
    return get_access_token(username=username_emba, password=password_emba, env=env)


@pytest.fixture(scope='class')
def get_sql_server():
    # print(sql_server_host, sql_server_username, sql_server_password, sql_server_database)
    conn = pymssql.connect(sql_server_host, sql_server_username, sql_server_password, sql_server_database)
    cur = conn.cursor()
    yield cur
    conn.commit()
    cur.close()
    conn.close()

