# -*- coding: utf-8 -*-
# @Time   : 2022/8/2 10:40
# @Author : qiuzonghang
# @File   : conftest.py

from Mimir.qz_auto_test.Params.params import get_param_data
from qz_auto_test.Common.Func import remove_dir
from Mimir.qz_auto_test.Conf.Config import Config
from Mimir.qz_auto_test.Common.Func import get_access_token
import pytest
import os
import pymssql

conf = Config()
env = 'uat'
if env == 'dev':
    username = conf.tester3_username_dev
    password = conf.tester3_password_dev
    username_emba = conf.wangye_username_dev
    password_emba = conf.wangye_password_dev
    sql_server_host = conf.sql_server_host_dev
    sql_server_database = conf.sql_server_database_dev
    sql_server_username = conf.sql_server_username_dev
    sql_server_password = conf.sql_server_password_dev
elif env == 'uat':
    username = conf.ITtest2_username_uat
    password = conf.ITtest2_password_uat
    username_emba = conf.ITtest3_username_uat
    password_emba = conf.ITtest3_password_uat
    sql_server_host = conf.sql_server_host_uat
    sql_server_database = conf.sql_server_database_uat
    sql_server_username = conf.sql_server_username_uat
    sql_server_password = conf.sql_server_password_uat


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
