# -*- coding: utf-8 -*-
# @Time   : 2022/8/1 11:36
# @Author : qiuzonghang
# @File   : params.py

from Mimir.qz_auto_test.Common.Func import get_access_token, read_txt, project_path
from Mimir.qz_auto_test.Common.Log import MyLog
from Mimir.qz_auto_test.Conf.Config import Config
from Mimir.qz_auto_test.Params.get_yaml import GetPages
from Mimir.qz_auto_test.Common.Request import Request
import time
import requests
import re

log = MyLog()
conf = Config()
get_data = GetPages()
request = Request()


def get_param_data(uri_type, user, pw, env='dev', get_token=True):
    if get_token:
        token, host, user_info = get_access_token(username=user, password=pw, env=env)
    else:
        token, host, user_info = '', '', {}
    total_param = get_data.get_page_list()
    # print(total_param)
    if '-' in uri_type:
        one_class, two_class = uri_type.split('-')
        uri = total_param.get(one_class)[0].get(two_class + "_url")
        param_data = total_param.get(one_class)[0].get(two_class + '_data')
        return {'url': host + uri, 'data': param_data, 'token': token, 'user_info': user_info}
    else:
        # print('----------------')
        return {'url': host, 'data': total_param.get(uri_type)[0], 'token': token, 'user_info': user_info}


def get_JYZZ_apply_param(origin_param, result_param):
    for origin_k, origin_v in origin_param.items():
        for result_k, result_v in result_param.items():
            if origin_k == result_k:
                origin_param[origin_k] = result_param[result_k]
    origin_param['startClassDate'] = time.strftime('%Y-%m-%d', time.localtime())
    origin_param['endClassDate'] = time.strftime('%Y-%m-%d', time.localtime())
    return origin_param


def check_sort(results):
    for num in range(len(results)):
        if re.sub('JYZZ', '', results[num].get('applyNo')) == re.sub('JYZZ', '', results[-1].get('applyNo')):
            break
        elif int(re.sub('JYZZ', '', results[num].get('applyNo'))) < int(
                re.sub('JYZZ', '', results[num + 1].get('applyNo'))):
            return False
    return True


def get_user_info(username_text, token):
    url = 'https://devsite.qintelligence.cn/api/GSMHRUserInfos/Search'
    data = {"pageNo": 0, "pageSize": 10, "queryText": username_text}
    r = request.post_request(url=url, data=data, token=token)


# token, host, user_info = get_access_token(username=conf.wangye_username, password=conf.wangye_password, env='dev', url='https://devsite.qintelligence.cn/#/work')
# print(get_user_info(username_text='王野', token=token))
# print(check_sort(a))
# parameter = get_param_data(uri_type='JYZZ', user='wangye@qynet.onmicrosoft.com', pw='Welcome@1')
# print(parameter)
