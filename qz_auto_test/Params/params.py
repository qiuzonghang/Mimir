# -*- coding: utf-8 -*-
# @Time   : 2022/8/1 11:36
# @Author : qiuzonghang
# @File   : params.py

from qz_auto_test.Common.Func import get_access_token
from qz_auto_test.Common.Log import MyLog
from qz_auto_test.Conf.Config import Config
from qz_auto_test.Params.get_yaml import GetPages

log = MyLog()
conf = Config()
get_data = GetPages()


def get_param_data(uri_type, user, pw, env='dev', get_token_url='https://devsite.qintelligence.cn/#/work', get_token=True):
    if get_token:
        token, host = get_access_token(username=user, password=pw, env=env, url=get_token_url)
    else:
        token, host = '', ''
    total_param = get_data.get_page_list()
    # print(total_param)
    if '-' in uri_type:
        one_class, two_class = uri_type.split('-')
        uri = total_param.get(one_class)[0].get(two_class + "_url")
        param_data = total_param.get(one_class)[0].get(two_class + '_data')
        return {'url': host + uri, 'data': param_data, 'token': token}
    else:
        return {'url': host, 'data': total_param.get(uri_type)[0], 'token': token}


# parameter = get_param_data(uri_type='JYZZ-start_class', user='tester1@qynet.onmicrosoft.com', pw='Qz123456.')
# print(parameter)
