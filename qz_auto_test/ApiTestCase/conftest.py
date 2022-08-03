# -*- coding: utf-8 -*-
# @Time   : 2022/8/2 10:40
# @Author : qiuzonghang
# @File   : conftest.py

from Mimir.qz_auto_test.Params.params import get_param_data
from qz_auto_test.Common.Func import remove_dir
import pytest
import os


@pytest.fixture(scope='class')
def get_JYZZ_param():
    return get_param_data(uri_type='JYZZ', user='wangye@qynet.onmicrosoft.com', pw='Welcome@1')
    # user_info = get_user_info(host=JYZZ_param.get('url'))
    # JYZZ_param['user_id'] = user_info.get('data').get('userID')
    # JYZZ_param['depInfo'] = user_info.get('data').get('depInfo')
    # return JYZZ_param


