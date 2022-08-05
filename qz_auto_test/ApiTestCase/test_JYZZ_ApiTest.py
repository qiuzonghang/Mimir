# -*- coding: utf-8 -*-
# @Time   : 2022/8/2 10:46
# @Author : qiuzonghang
# @File   : test_JYZZ_ApiTest.py

import pytest
import allure
import requests
import random

from Mimir.qz_auto_test.Common.Request import Request
from Mimir.qz_auto_test.Common.Log import MyLog
from Mimir.qz_auto_test.Common.Assert import Assertions
from Mimir.qz_auto_test.Conf.Config import Config
from Mimir.qz_auto_test.Params.params import get_JYZZ_apply_param, check_sort

request = Request()
log = MyLog()
test = Assertions()
assert_dict = {}


@pytest.mark.usefixtures('get_JYZZ_param', 'get_dev_sql_server')
class TestCase:

    @allure.title('讲义制作-开课名称')
    @allure.feature('JYZZ_start-class')
    @allure.severity('critical')
    @allure.story('JYZZ_start-class')
    @allure.step("JYZZ_start-class")
    def test_start_class(self, get_JYZZ_param):
        host = get_JYZZ_param.get('url') + get_JYZZ_param.get('data').get('start_class_url')
        start_class_data = get_JYZZ_param.get('data').get('start_class_data')
        data_list = []
        [data_list.append(k + '=' + str(v)) for k, v in start_class_data.items()]
        case = random.choice(['测试', '课程'])
        url = host + '&'.join(data_list) + case
        header = {'authorization': get_JYZZ_param['token']}
        r = request.get_request(url=url, header=header)
        log.info(str(r))
        class_info_list = r.get('body').get('data')
        random_class_info = random.choice(class_info_list)
        assert_dict['className'] = random_class_info.get('courseName')
        assert_dict['classTeacher'] = random_class_info.get('teacherName')
        # assert_dict['random_start_class_id'] = random_class_info.get('id')
        with allure.step('校验结果'):
            allure.attach(str(class_info_list), '实际结果')
            allure.attach('含有“%s”关键词的开课名称及对应教师' % case, '预期结果')
        test.assert_code(200, r['code'])
        for class_info in class_info_list:
            test.assert_in_text(class_info.get('courseName'), case)
            test.assert_not_is_body(class_info.get('teacherName'), '')

    @allure.title('讲义制作-开课班级')
    @allure.feature('JYZZ_school_roll_class')
    @allure.severity('critical')
    @allure.story('JYZZ_school_roll_class')
    @allure.step("JYZZ_school_roll_class")
    def test_school_roll_class(self, get_JYZZ_param):
        host = get_JYZZ_param.get('url') + get_JYZZ_param.get('data').get('school_roll_class_url')
        school_roll_class_data = get_JYZZ_param.get('data').get('school_roll_class_data')
        data_list = []
        [data_list.append(k + '=' + str(v)) for k, v in school_roll_class_data.items()]
        case = random.choice(['班级', '测试'])
        url = host + '&'.join(data_list) + case
        header = {'authorization': get_JYZZ_param['token']}
        r = request.get_request(url=url, header=header)
        log.info(str(r))
        class_info_list = r.get('body').get('data')
        random_school_class_info = random.choice(class_info_list)
        assert_dict['startClassName'] = random_school_class_info.get('studendtClassName')
        assert_dict['startClassId'] = random_school_class_info.get('id')
        with allure.step('校验结果'):
            allure.attach(str(class_info_list), '实际结果')
            allure.attach('含有“%s”关键词' % case, '预期结果')
        test.assert_code(200, r['code'])
        for class_info in class_info_list:
            test.assert_in_text(class_info.get('studendtClassName'), case)

    @allure.title('讲义制作-新建讲义')
    @allure.feature('JYZZ_apply')
    @allure.severity('critical')
    @allure.story('JYZZ_apply')
    @allure.step("JYZZ_apply")
    def test_apply(self, get_JYZZ_param, get_dev_sql_server):
        url = get_JYZZ_param.get('url') + get_JYZZ_param.get('data').get('apply_url')
        apply_data = get_JYZZ_param.get('data').get('apply_data')
        header = {'authorization': get_JYZZ_param['token'], 'content-type': 'application/json'}
        data = get_JYZZ_apply_param(origin_param=apply_data, result_param=assert_dict)
        random_depInfo = random.choice(get_JYZZ_param.get('user_info').get('data').get('depInfo'))
        data['departmentName'] = random_depInfo.get('departmentName')
        data['departmentId'] = random_depInfo.get('departmentId')
        data['applyCount'] = random.randrange(10, 100, 10)
        assert_dict['apply_data'] = data
        r = request.post_request(url=url, header=header, data=data)
        log.info(str(r))
        # sql_server = get_dev_sql_server
        # sql = 'select * from GSM_JYZZ_Apply order by id desc'
        # sql_server.execute(sql)
        # sql_result = sql_server.fetchall()[0]
        with allure.step('校验结果'):
            allure.attach(str(r), '实际结果')
            allure.attach('验证创建正常，数据库数据正确', '预期结果')
        test.assert_code(r.get('code'), 200)
        test.assert_code(r.get('body').get('statusCode'), 200)
        # print(data)
        # print(sql_result)
        # for k, v in data.items():
        #     if k == 'applyNo' or k == 'id':
        #         continue
        #     test.assert_in_text(str(v), sql_result)

    @allure.title('讲义制作-讲义列表')
    @allure.feature('JYZZ_get_list')
    @allure.severity('critical')
    @allure.story('JYZZ_get_list')
    @allure.step("JYZZ_get_list")
    def test_get_list(self, get_JYZZ_param):
        url = get_JYZZ_param.get('url') + get_JYZZ_param.get('data').get('get_list_url')
        get_list_data = get_JYZZ_param.get('data').get('get_list_data')
        get_list_data['conModels'][0]['fieldValue'] = get_JYZZ_param.get('user_info').get('data').get('userID')
        header = {'authorization': get_JYZZ_param['token'], 'content-type': 'application/json'}
        response = request.post_request(url=url, data=get_list_data, header=header)
        log.info(str(response))
        data_info = response.get('body').get('data').get('data')
        with allure.step('校验结果'):
            allure.attach(str(response), '实际结果')
            allure.attach('1、创建时间倒序排序\n2、创建信息展示', '预期结果')
        test.assert_type(data_info, '排序不正确')
        for k, v in assert_dict['apply_data'].items():
            if k == 'applyNo' or k == 'id':
                continue
            test.assert_text(str(data_info[0][k]), str(v))

    @allure.title('讲义制作-讲义管理列表')
    @allure.feature('JYZZ_admin_get_list')
    @allure.severity('critical')
    @allure.story('JYZZ_admin_get_list')
    @allure.step("JYZZ_admin_get_list")
    def test_admin_get_list(self, get_JYZZ_param):
        url = get_JYZZ_param.get('url') + get_JYZZ_param.get('data').get('get_list_url')
        get_list_data = get_JYZZ_param.get('data').get('get_list_data')
        get_list_data['conModels'][0]['fieldName'] = 'currentActive'
        get_list_data['conModels'][0]['fieldValue'] = '1,2,3'
        get_list_data['conModels'][0]['conditionalType'] = 6
        header = {'authorization': get_JYZZ_param['token'], 'content-type': 'application/json'}
        response = request.post_request(url=url, data=get_list_data, header=header)
        log.info(str(response))
        data_result = response.get('body').get('data').get('data')
        with allure.step('校验结果'):
            allure.attach(str(response), '实际结果')
            allure.attach('1、创建时间倒序排序\n2、创建信息展示', '预期结果')
        test.assert_type(data_result, '排序不正确')
        for k, v in assert_dict['apply_data'].items():
            if k == 'applyNo' or k == 'id':
                continue
            test.assert_text(str(data_result[0][k]), str(v))

    @allure.title('讲义制作-新增纸张克重定义')
    @allure.feature('JYZZ_add_paper_weight')
    @allure.severity('critical')
    @allure.story('JYZZ_add_paper_weight')
    @allure.step("JYZZ_add_paper_weight")
    def test_add_paper_weight(self, get_JYZZ_param, get_dev_sql_server):
        url = get_JYZZ_param.get('url') + get_JYZZ_param.get('data').get('add_paper_url')
        data = get_JYZZ_param.get('data').get('add_paper_data')
        weight_value = random.randint(1, 1000)
        data['value'] = weight_value
        data['type'] = 'PapaerWeight'
        header = {'authorization': get_JYZZ_param['token'], 'content-type': 'application/json'}
        response = request.post_request(url=url, data=data, header=header)
        log.info('Response:' + str(response))
        sql_server = get_dev_sql_server
        sql = "select * from GSM_JYZZ_Dic where Type = 'PapaerWeight' order by DId desc "
        sql_server.execute(sql)
        sql_result = sql_server.fetchall()[0]
        assert_dict['new_paper_weight'] = sql_result
        log.info('Sql_result:' + str(sql_result))
        with allure.step('校验结果'):
            allure.attach(str(response) + '\n' + str(sql_result), '实际结果')
            allure.attach('1、创建成功\n2、数据库查验', '预期结果')
        test.assert_code(response.get('body').get('statusCode'), 200)
        test.assert_text(sql_result[3], str(weight_value))

    @allure.title('讲义制作-获取纸张克重定义')
    @allure.feature('JYZZ_query_paper_weight')
    @allure.severity('critical')
    @allure.story('JYZZ_query_paper_weight')
    @allure.step("JYZZ_query_paper_weight")
    def test_query_paper_weight(self, get_JYZZ_param, get_dev_sql_server):
        # pytest.xfail('排序错误，已知问题')
        uri = get_JYZZ_param.get('url') + get_JYZZ_param.get('data').get('add_paper_url')
        data = get_JYZZ_param.get('data').get('query_paper_data')
        data['type'] = 'PapaerWeight'
        header = {'authorization': get_JYZZ_param['token'], 'content-type': 'application/json'}
        data_list = []
        [data_list.append(k + '=' + str(v)) for k, v in data.items()]
        url = uri + '?' + '&'.join(data_list)
        response = request.get_request(url=url, header=header)
        log.info('Response:' + str(response))
        sql_server = get_dev_sql_server
        sql = "select * from GSM_JYZZ_Dic where Type = 'PapaerWeight' order by DId "
        sql_server.execute(sql)
        sql_result = sql_server.fetchall()
        log.info('Sql_result:' + str(sql_result))
        query_paper = response.get('body').get('data').get('data')
        # assert_dict['query_paper_weight'] = random.choice(query_paper)
        with allure.step('校验结果'):
            allure.attach(str(response) + '\n' + str(sql_result), '实际结果')
            allure.attach('1、正确返回数据\n2、数据库查验', '预期结果')
        test.assert_code(response.get('body').get('statusCode'), 200)
        for query_num in range(len(query_paper)):
            test.assert_in_text(str(sql_result[query_num][0]), str(query_paper[query_num]['dId']))
            test.assert_in_text(str(sql_result[query_num][3]), str(query_paper[query_num]['value']))

    @allure.title('讲义制作-编辑纸张克重定义')
    @allure.feature('JYZZ_update_paper_weight')
    @allure.severity('critical')
    @allure.story('JYZZ_update_paper_weight')
    @allure.step("JYZZ_update_paper_weight")
    def test_update_paper_weight(self, get_JYZZ_param, get_dev_sql_server):
        url = get_JYZZ_param.get('url') + get_JYZZ_param.get('data').get('add_paper_url') + '/%s' % assert_dict['new_paper_weight'][0]
        data = get_JYZZ_param.get('data').get('add_paper_data')
        data['type'] = 'PapaerWeight'
        data['value'] = random.randint(1, 100)
        data['dId'] = data.pop('id')
        data['dId'] = assert_dict['new_paper_weight'][0]
        data['extraProperties'] = 'null'
        header = {'authorization': get_JYZZ_param['token'], 'content-type': 'application/json'}
        response = request.put_request(url=url, header=header, data=data)
        log.info('Response:' + str(response))
        sql_server = get_dev_sql_server
        sql = "select * from GSM_JYZZ_Dic where Type = 'PapaerWeight' order by DId desc "
        sql_server.execute(sql)
        sql_result = sql_server.fetchall()
        log.info('Sql_result:' + str(sql_result))
        with allure.step('校验结果'):
            allure.attach(str(response) + '\n' + str(sql_result), '实际结果')
            allure.attach('1、正确编辑\n2、数据库查验:%s' % str(sql_result[0]), '预期结果')
        test.assert_code(response.get('body').get('statusCode'), 200)
        test.assert_text(str(data['value']), str(sql_result[0][3]))

    @allure.title('讲义制作-删除纸张克重定义')
    @allure.feature('JYZZ_delete_paper_weight')
    @allure.severity('critical')
    @allure.story('JYZZ_delete_paper_weight')
    @allure.step("JYZZ_delete_paper_weight")
    def test_delete_paper_weight(self, get_JYZZ_param, get_dev_sql_server):
        url = get_JYZZ_param.get('url') + get_JYZZ_param.get('data').get('add_paper_url') + '/%s' % assert_dict['new_paper_weight'][0]
        header = {'authorization': get_JYZZ_param['token'], 'content-type': 'application/json'}
        response = request.delete_request(url=url, header=header)
        log.info('Response:' + str(response))
        sql_server = get_dev_sql_server
        sql = "select * from GSM_JYZZ_Dic where Type = 'PapaerWeight' order by DId desc "
        sql_server.execute(sql)
        sql_result = sql_server.fetchall()
        log.info('Sql_result:' + str(sql_result))
        with allure.step('校验结果'):
            allure.attach(str(response) + '\n' + str(sql_result), '实际结果')
            allure.attach('1、正确删除\n2、数据库查验:{}'.format(sql_result), '预期结果')
        test.assert_not_is_body(sql_result[0][0], assert_dict['new_paper_weight'][0])


if __name__ == '__main__':
    pytest.main(['-s', '-v'])
