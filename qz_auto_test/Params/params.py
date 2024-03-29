# -*- coding: utf-8 -*-
# @Time   : 2022/8/1 11:36
# @Author : qiuzonghang
# @File   : params.py
import random

from qz_auto_test.Common.Func import get_access_token, read_txt, project_path
from qz_auto_test.Common.Log import MyLog
from qz_auto_test.Conf.Config import Config
from qz_auto_test.Params.get_yaml import GetPages
from qz_auto_test.Common.Request import Request
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
        return {'url': host, 'data': total_param.get(uri_type)[0], 'token': token, 'user_info': user_info, 'env': env}


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


def arr_sql_param(sql_title, sql_data_list):
    arr_result = []
    try:
        for sql_data in sql_data_list:
            arr_dict = {}
            for sql_num in range(len(sql_data)):
                arr_dict[sql_title[sql_num]] = sql_data[sql_num]
            arr_result.append(arr_dict)
        return arr_result
    except TypeError:
        arr_dict = {}
        for sql_num in range(len(sql_data_list)):
            arr_dict[sql_title[sql_num]] = sql_data_list[sql_num]
        return arr_dict


def arr_sql_title(sql_title):
    sql_title_list = []
    [sql_title_list.append(title[0]) for title in sql_title]
    return sql_title_list


def param_id_desc(list_data, sort_param='id'):
    for num1 in range(len(list_data)):
        for num2 in range(len(list_data) - num1 - 1):
            if list_data[num2][sort_param] < list_data[num2 + 1][sort_param]:
                list_data[num2], list_data[num2 + 1] = list_data[num2 + 1], list_data[num2]
    return list_data


# print(get_access_token(username='tester3@qynet.onmicrosoft.com', password='Qz123456.', env='test'))
