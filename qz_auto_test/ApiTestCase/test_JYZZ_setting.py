# -*- coding: utf-8 -*-
# @Time   : 2022/8/18 16:28
# @Author : qiuzonghang
# @File   : test_JYZZ_setting.py

import pytest
import allure
import requests
import random
import json
import time

from qz_auto_test.Common.Request import Request
from qz_auto_test.Common.Log import MyLog
from qz_auto_test.Common.Assert import Assertions
from qz_auto_test.Conf.Config import Config
from qz_auto_test.Params.params import get_JYZZ_apply_param, check_sort, arr_sql_param, arr_sql_title, param_id_desc

request = Request()
log = MyLog()
test = Assertions()
assert_dict = {}


@pytest.mark.usefixtures('get_JYZZ_param', 'get_sql_server', 'get_emba_token')
@pytest.mark.site
@pytest.mark.JYZZ
class TestCase:

    @allure.title('讲义制作-新增纸张克重定义')
    @allure.feature('JYZZ_add_paper_weight')
    @allure.severity('critical')
    @allure.story('JYZZ_add_paper_weight')
    @allure.step("JYZZ_add_paper_weight")
    def test_add_paper_weight(self, get_JYZZ_param, get_sql_server):
        """
            新增纸张克重，校验数据库、statusCode。数据依赖
        """
        url = get_JYZZ_param.get('url') + get_JYZZ_param.get('data').get('add_paper_url')
        data = get_JYZZ_param.get('data').get('add_paper_data')
        weight_value = random.randint(1, 1000)
        data['value'] = weight_value
        data['type'] = 'PapaerWeight'
        response = request.post_request(url=url, data=data, token=get_JYZZ_param.get('token'))
        sql = "select * from GSM_JYZZ_Dic where Type = 'PapaerWeight' order by DId desc "
        get_sql_server.execute(sql)
        sql_result = arr_sql_param(sql_title=arr_sql_title(get_sql_server.description), sql_data_list=get_sql_server.fetchall()[0])
        log.info('Response:%s\nSql Result:%s' % (str(response), sql_result))
        assert_dict['new_paper_weight'] = sql_result
        log.info('Sql_result:' + str(sql_result))
        with allure.step('校验结果'):
            allure.attach(str(response) + '\n' + str(sql_result), '实际结果')
            allure.attach('1、创建成功\n2、数据库查验', '预期结果')
        test.assert_code(response.get('body').get('statusCode'), 200)
        for data_k, data_v in data.items():
            for sql_k, sql_v in sql_result.items():
                if data_k.casefold() == sql_k.casefold():
                    test.assert_text(str(data_v).split('.')[0], str(sql_v).split('.')[0])

    @allure.title('讲义制作-获取纸张克重定义')
    @allure.feature('JYZZ_query_paper_weight')
    @allure.severity('critical')
    @allure.story('JYZZ_query_paper_weight')
    @allure.step("JYZZ_query_paper_weight")
    def test_query_paper_weight(self, get_JYZZ_param, get_sql_server):
        """
            查询纸张克重定义数据，校验数据库、statusCode、add_paper_weight数据
        :param get_JYZZ_param:
        :param get_sql_server:
        :return:
        """
        # pytest.xfail('排序错误，已知问题')
        uri = get_JYZZ_param.get('url') + get_JYZZ_param.get('data').get('add_paper_url')
        data = get_JYZZ_param.get('data').get('query_paper_data')
        data['type'] = 'PapaerWeight'
        data_list = []
        [data_list.append(k + '=' + str(v)) for k, v in data.items()]
        url = uri + '?' + '&'.join(data_list)
        response = request.get_request(url=url, token=get_JYZZ_param.get('token'))
        sql = "select * from GSM_JYZZ_Dic where Type = 'PapaerWeight' order by DId desc "
        get_sql_server.execute(sql)
        sql_result = arr_sql_param(sql_title=arr_sql_title(get_sql_server.description),
                                   sql_data_list=get_sql_server.fetchall())
        log.info('Response:%s\nSql Result:%s' % (str(response), sql_result))
        query_paper = response.get('body').get('data').get('data')
        query_paper_desc = param_id_desc(query_paper, sort_param='dId')
        with allure.step('校验结果'):
            allure.attach(str(response) + '\n' + str(sql_result), '实际结果')
            allure.attach('1、正确返回数据\n2、数据库查验', '预期结果')
        test.assert_code(response.get('body').get('statusCode'), 200)
        test.assert_text(query_paper_desc[0].get('dId'), assert_dict['new_paper_weight']['DId'])
        test.assert_text(len(query_paper_desc), len(sql_result))
        for data_num in range(len(query_paper_desc)):
            for data_k, data_v in query_paper_desc[data_num].items():
                for sql_k, sql_v in sql_result[data_num].items():
                    if data_k.casefold() == sql_k.casefold():
                        test.assert_text(str(data_v).split('.')[0], str(sql_v).split('.')[0])

    @allure.title('讲义制作-编辑纸张克重定义')
    @allure.feature('JYZZ_update_paper_weight')
    @allure.severity('critical')
    @allure.story('JYZZ_update_paper_weight')
    @allure.step("JYZZ_update_paper_weight")
    def test_update_paper_weight(self, get_JYZZ_param, get_sql_server):
        """
            修改纸张克重定义，校验数据库、statusCode
        """
        url = get_JYZZ_param.get('url') + get_JYZZ_param.get('data').get('add_paper_url') + '/%s' % \
              assert_dict['new_paper_weight']['DId']
        data = get_JYZZ_param.get('data').get('add_paper_data')
        data['type'] = 'PapaerWeight'
        data['value'] = random.randint(1, 100)
        data['dId'] = data.pop('id')
        data['dId'] = assert_dict['new_paper_weight']['DId']
        data['extraProperties'] = 'null'
        response = request.put_request(url=url, token=get_JYZZ_param.get('token'), data=data)
        sql = "select * from GSM_JYZZ_Dic where Type = 'PapaerWeight' order by DId desc "
        get_sql_server.execute(sql)
        sql_result = arr_sql_param(sql_title=arr_sql_title(get_sql_server.description),
                                   sql_data_list=get_sql_server.fetchall()[0])
        log.info('Response:%s\nSql Result:%s' % (str(response), sql_result))
        with allure.step('校验结果'):
            allure.attach(str(response) + '\n' + str(sql_result), '实际结果')
            allure.attach('1、正确编辑\n2、数据库查验:%s' % str(sql_result), '预期结果')
        test.assert_code(response.get('body').get('statusCode'), 200)
        for data_k, data_v in data.items():
            for sql_k, sql_v in sql_result.items():
                if data_k.casefold() == sql_k.casefold():
                    test.assert_text(str(data_v).split('.')[0], str(sql_v).split('.')[0])

    @allure.title('讲义制作-删除纸张克重定义')
    @allure.feature('JYZZ_delete_paper_weight')
    @allure.severity('critical')
    @allure.story('JYZZ_delete_paper_weight')
    @allure.step("JYZZ_delete_paper_weight")
    def test_delete_paper_weight(self, get_JYZZ_param, get_sql_server):
        url = get_JYZZ_param.get('url') + get_JYZZ_param.get('data').get('add_paper_url') + '/%s' % \
              assert_dict['new_paper_weight']['DId']
        response = request.delete_request(url=url, token=get_JYZZ_param.get('token'))
        sql = "select * from GSM_JYZZ_Dic where Type = 'PapaerWeight' order by DId desc "
        get_sql_server.execute(sql)
        sql_result = arr_sql_param(sql_title=arr_sql_title(get_sql_server.description),
                                   sql_data_list=get_sql_server.fetchall()[0])
        log.info('Response:%s\nSql Result:%s' % (str(response), sql_result))
        with allure.step('校验结果'):
            allure.attach(str(response) + '\n' + str(sql_result), '实际结果')
            allure.attach('1、正确删除\n2、数据库查验:{}'.format(sql_result), '预期结果')
        test.assert_code(response.get('body').get('statusCode'), 200)
        test.assert_not_is_body(sql_result['DId'], assert_dict['new_paper_weight']['DId'])


if __name__ == '__main__':
    pytest.main(['-s', '-v'])