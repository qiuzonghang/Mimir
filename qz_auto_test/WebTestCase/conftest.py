# -*- coding: utf-8 -*-
# @Time   : 2023/1/31 14:19
# @Author : qiuzonghang
# @File   : conftest.py

import sys
import os
import re
import time

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from qz_auto_test.Params.params import get_param_data
from qz_auto_test.Common.Func import remove_dir
from qz_auto_test.Conf.Config import Config
from qz_auto_test.Common.Func import get_access_token, get_conf_info, Driver
import pytest
import pymssql


conf = Config()


@pytest.fixture(scope='class')
def work_login():
    pass


@pytest.fixture(scope='class')
def open_apply():
    base = Driver()
    apply_url = 'https://' + conf.test_apply_host + '/#/'
    test = base.start_dr(url=apply_url, driver_name='edge', type='web')
    yield test
    time.sleep(10)
    test.quit()


