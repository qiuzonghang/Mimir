# -*- coding: utf-8 -*-
# @Time   : 2022/8/2 10:46
# @Author : qiuzonghang
# @File   : test_JYZZ_api.py

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

    @allure.title('讲义制作-课程名称-EMBA')
    @allure.feature('JYZZ_start_class_emba')
    @allure.severity('critical')
    @allure.story('JYZZ_start_class_emba')
    @allure.step("JYZZ_start_class_emba")
    def test_start_class_emba(self, get_JYZZ_param, get_sql_server, get_emba_token):
        """
            课程名称，数据依赖，用于test_apply创建讲义，校验关键词并对比数据库，EMBA账号
        """
        token, none_data01, none_data02 = get_emba_token
        host = get_JYZZ_param.get('url') + get_JYZZ_param.get('data').get('start_class_url')
        start_class_data = get_JYZZ_param.get('data').get('start_class_data')
        data_list = []
        [data_list.append(k + '=' + str(v)) for k, v in start_class_data.items()]
        if 'uat' in host:
            case = random.choice(['测试', '课程'])
        else:
            case = random.choice(['管理', '工商'])
        url = host + '&'.join(data_list) + case
        r = request.get_request(url=url, token=token)
        sql_server = get_sql_server
        sql = "select * from GSMStartClass where PageType = 'emba' and CourseNameCN like '%{}%' order by Id desc ".format(case)
        sql_server.execute(sql)
        start_class_sql_result = sql_server.fetchall()
        sql_title = arr_sql_title(sql_server.description)
        sql_result = arr_sql_param(sql_title, start_class_sql_result)
        log.info('Response:%s\nSQL:%s' % (str(r), str(start_class_sql_result)))
        class_info_list = param_id_desc(r.get('body').get('data'))
        random_class_info = random.choice(class_info_list)
        assert_dict['emba_className'] = random_class_info.get('courseName')
        assert_dict['emba_classTeacher'] = random_class_info.get('teacherName')
        with allure.step('校验结果'):
            allure.attach(str(class_info_list), '实际结果')
            allure.attach('含有“%s”关键词的开课名称及对应教师' % case, '预期结果')
        test.assert_code(r.get('body').get('statusCode'), 200)
        for rsp_num in range(len(class_info_list)):
            test.assert_in_text(class_info_list[rsp_num].get('courseName'), case)
            test.assert_not_is_body(class_info_list[rsp_num].get('teacherName'), '')
            for rsp_k, rsp_v in class_info_list[rsp_num].items():
                for sql_k, sql_v in sql_result[rsp_num].items():
                    if rsp_k.casefold() == sql_k.casefold():
                        test.assert_text(str(rsp_v).split('.')[0], str(sql_v).split('.')[0])

    @allure.title('讲义制作-开课班级-EMBA')
    @allure.feature('JYZZ_school_roll_class_emba')
    @allure.severity('critical')
    @allure.story('JYZZ_school_roll_class_emba')
    @allure.step("JYZZ_school_roll_class_emba")
    def test_school_roll_class(self, get_JYZZ_param, get_sql_server, get_emba_token):
        """
            开课班级，数据依赖，用于test_apply创建讲义，校验关键词并对比数据库，EMBA账号
        """
        token, none_data01, none_data02 = get_emba_token
        host = get_JYZZ_param.get('url') + get_JYZZ_param.get('data').get('school_roll_class_url')
        school_roll_class_data = get_JYZZ_param.get('data').get('school_roll_class_data')
        data_list = []
        [data_list.append(k + '=' + str(v)) for k, v in school_roll_class_data.items()]
        case = random.choice(['测试'])
        url = host + '&'.join(data_list) + case
        header = {'authorization': token}
        r = request.get_request(url=url, header=header)
        sql = "select * from GSMSchoolRollClass where PageType = 'emba' and StudendtClassName like '%{}%' order by Id desc ".format(case)
        get_sql_server.execute(sql)
        sql_result = arr_sql_param(sql_title=arr_sql_title(get_sql_server.description), sql_data_list=get_sql_server.fetchall())
        log.info('Response:%s\nSql Result:%s' % (r, sql_result))
        class_info_list = param_id_desc(r.get('body').get('data'))
        random_school_class_info = random.choice(class_info_list)
        assert_dict['emba_startClassName'] = random_school_class_info.get('studendtClassName')
        assert_dict['emba_startClassId'] = random_school_class_info.get('id')
        with allure.step('校验结果'):
            allure.attach(str(class_info_list), '实际结果')
            allure.attach('含有“%s”关键词' % case, '预期结果')
        test.assert_code(r.get('body').get('statusCode'), 200)
        for rsp_num in range(len(class_info_list)):
            test.assert_in_text(class_info_list[rsp_num].get('studendtClassName'), case)
            for rsp_k, rsp_v in class_info_list[rsp_num].items():
                for sql_k, sql_v in sql_result[rsp_num].items():
                    if rsp_k.casefold() == sql_k.casefold():
                        test.assert_text(str(rsp_v).split('.')[0], str(sql_v).split('.')[0])

    @allure.title('讲义制作-课程名称-ExEd')
    @allure.feature('JYZZ_start_class_exed')
    @allure.severity('critical')
    @allure.story('JYZZ_start_class_exed')
    @allure.step("JYZZ_start_class_exed")
    def test_start_class_exed(self, get_JYZZ_param, get_sql_server):
        """
            课程名称，数据依赖，用于test_apply创建讲义，校验关键词并对比数据库，ExEd账号
        """
        host = get_JYZZ_param.get('url') + get_JYZZ_param.get('data').get('start_class_url')
        start_class_data = get_JYZZ_param.get('data').get('start_class_data')
        data_list = []
        [data_list.append(k + '=' + str(v)) for k, v in start_class_data.items()]
        case = random.choice(['测试', '课程'])
        url = host + '&'.join(data_list) + case
        r = request.get_request(url=url, token=get_JYZZ_param.get('token'))
        sql_server = get_sql_server
        sql = "select top 10 * from GSMEducationExEdCourse where CourseName like '%{}%' order by Id desc ".format(case)
        sql_server.execute(sql)
        start_class_sql_result = sql_server.fetchall()
        sql_title = arr_sql_title(sql_server.description)
        sql_result = arr_sql_param(sql_title, start_class_sql_result)
        log.info('Response:%s\nSQL:%s' % (str(r), str(start_class_sql_result)))
        class_info_list = param_id_desc(r.get('body').get('data'))
        random_class_info = random.choice(class_info_list)
        assert_dict['exed_className'] = random_class_info.get('courseName')
        assert_dict['exed_classTeacher'] = random_class_info.get('teacherName')
        with allure.step('校验结果'):
            allure.attach(str(class_info_list), '实际结果')
            allure.attach('含有“%s”关键词的开课名称及对应教师' % case, '预期结果')
        test.assert_code(r.get('body').get('statusCode'), 200)
        test.assert_text(len(class_info_list), len(sql_result))
        for rsp_num in range(len(class_info_list)):
            test.assert_in_text(class_info_list[rsp_num].get('courseName'), case)
            test.assert_not_is_body(class_info_list[rsp_num].get('teacherName'), '')
            # for rsp_k, rsp_v in class_info_list[rsp_num].items():
            #     for sql_k, sql_v in sql_result[rsp_num].items():
            #         if rsp_k.casefold() == sql_k.casefold():
            #             test.assert_text(str(rsp_v).split('.')[0], str(sql_v).split('.')[0])

    @allure.title('讲义制作-新建讲义-EMBA')
    @allure.feature('JYZZ_apply_emba')
    @allure.severity('critical')
    @allure.story('JYZZ_apply_emba')
    @allure.step("JYZZ_apply_emba")
    def test_apply_emba(self, get_JYZZ_param, get_sql_server, get_emba_token):
        """
            校验ExEd部门新增讲义制作，判断statusCode、数据库
        """
        token, host, user_info = get_emba_token
        url = get_JYZZ_param.get('url') + get_JYZZ_param.get('data').get('apply_url')
        apply_data = get_JYZZ_param.get('data').get('apply_data')
        random_depInfo = random.choice(user_info.get('data').get('depInfo'))
        apply_data['departmentName'] = random_depInfo.get('departmentName')
        apply_data['departmentId'] = random_depInfo.get('departmentId')
        apply_data['applyCount'] = random.randrange(10, 100, 10)
        apply_data['classTeacher'] = assert_dict['emba_classTeacher']
        apply_data['className'] = assert_dict['emba_className']
        apply_data['startClassId'] = assert_dict['emba_startClassId']
        apply_data['startClassName'] = assert_dict['emba_startClassName']
        apply_data['startClassDate'] = time.strftime('%Y-%m-%d', time.localtime())
        apply_data['endClassDate'] = time.strftime('%Y-%m-%d', time.localtime())
        # assert_dict['apply_data_emba'] = apply_data
        r = request.post_request(url=url, token=token, data=apply_data)
        sql = "select * from GSM_JYZZ_Apply order by Id desc"
        get_sql_server.execute(sql)
        apply_sql_result = get_sql_server.fetchall()[0]
        sql_title = arr_sql_title(get_sql_server.description)
        sql_result = arr_sql_param(sql_title, apply_sql_result)
        log.info('Response:%s\nSQL:%s' % (str(r), str(apply_sql_result)))
        with allure.step('校验结果'):
            allure.attach(str(r), '实际结果')
            allure.attach('验证创建正常，数据库数据正确', '预期结果')
        test.assert_code(r.get('body').get('statusCode'), 200)
        for data_k, data_v in apply_data.items():
            for sql_k, sql_v in sql_result.items():
                if data_k.casefold() == 'applyNo'.casefold() or data_k.casefold() == 'id'.casefold():
                    continue
                elif data_k.casefold() == sql_k.casefold():
                    test.assert_text(str(sql_v).split('.')[0], str(data_v).split('.')[0])


    @allure.title('讲义制作-新建讲义-ExEd')
    @allure.feature('JYZZ_apply_exed')
    @allure.severity('critical')
    @allure.story('JYZZ_apply_exed')
    @allure.step("JYZZ_apply_exed")
    def test_apply_exed(self, get_JYZZ_param, get_sql_server):
        """
            校验ExEd部门新增讲义制作，判断statusCode、数据库
        """
        url = get_JYZZ_param.get('url') + get_JYZZ_param.get('data').get('apply_url')
        apply_data = get_JYZZ_param.get('data').get('apply_data')
        random_depInfo = random.choice(get_JYZZ_param.get('user_info').get('data').get('depInfo'))
        apply_data['departmentName'] = random_depInfo.get('departmentName')
        apply_data['departmentId'] = random_depInfo.get('departmentId')
        apply_data['applyCount'] = random.randrange(10, 100, 10)
        apply_data['classTeacher'] = assert_dict['exed_classTeacher']
        apply_data['className'] = assert_dict['exed_className']
        apply_data['startClassDate'] = time.strftime('%Y-%m-%d', time.localtime())
        apply_data['endClassDate'] = time.strftime('%Y-%m-%d', time.localtime())
        assert_dict['exed_apply_data'] = apply_data
        r = request.post_request(url=url, token=get_JYZZ_param['token'], data=apply_data)
        sql = "select * from GSM_JYZZ_Apply order by Id desc"
        get_sql_server.execute(sql)
        apply_sql_result = get_sql_server.fetchall()[0]
        sql_title = arr_sql_title(get_sql_server.description)
        sql_result = arr_sql_param(sql_title, apply_sql_result)
        log.info('Response:%s\nSQL:%s' % (str(r), str(apply_sql_result)))
        with allure.step('校验结果'):
            allure.attach(str(r), '实际结果')
            allure.attach('验证创建正常，数据库数据正确', '预期结果')
        test.assert_code(r.get('body').get('statusCode'), 200)
        for data_k, data_v in apply_data.items():
            for sql_k, sql_v in sql_result.items():
                if data_k.casefold() == 'applyNo'.casefold() or data_k.casefold() == 'id'.casefold():
                    continue
                elif data_k.casefold() == sql_k.casefold():
                    test.assert_text(str(sql_v).split('.')[0], str(data_v).split('.')[0])

    @allure.title('讲义制作-讲义列表')
    @allure.feature('JYZZ_get_list')
    @allure.severity('critical')
    @allure.story('JYZZ_get_list')
    @allure.step("JYZZ_get_list")
    def test_get_list(self, get_JYZZ_param, get_sql_server):
        """
            获取当前账号已添加讲义列表，校验statusCode、数据库、test_apply添加
        """
        url = get_JYZZ_param.get('url') + get_JYZZ_param.get('data').get('get_list_url')
        get_list_data = get_JYZZ_param.get('data').get('get_list_data')
        page_size = random.randrange(10, 100, 10)
        get_list_data['conModels'][0]['fieldValue'] = get_JYZZ_param.get('user_info').get('data').get('userID')
        get_list_data['pageSize'] = page_size
        response = request.post_request(url=url, data=get_list_data, token=get_JYZZ_param.get('token'))
        sql = "select top {} * from GSM_JYZZ_Apply where IsDelete = 0 and Creator = '{}' order by Id desc".format(page_size, get_JYZZ_param.get('user_info').get('data').get('name'))
        get_sql_server.execute(sql)
        apply_sql_result = get_sql_server.fetchall()
        sql_title = arr_sql_title(get_sql_server.description)
        sql_result = arr_sql_param(sql_title, apply_sql_result)
        log.info('Response:%s\nSQL:%s' % (str(response), str(apply_sql_result)))
        data_info = response.get('body').get('data').get('data')
        with allure.step('校验结果'):
            allure.attach(str(response), '实际结果')
            allure.attach('1、创建时间倒序排序\n2、创建信息展示', '预期结果')
        test.assert_code(response.get('body').get('statusCode'), 200)
        test.assert_text(len(data_info), len(sql_result))
        for k, v in assert_dict['exed_apply_data'].items():
            if k == 'applyNo' or k == 'id':
                continue
            test.assert_text(str(data_info[0][k]), str(v))      # 判断添加后是否正返回
        for rsp_num in range(len(data_info)):
            for rsp_k, rsp_v in data_info[rsp_num].items():
                for sql_k, sql_v in sql_result[rsp_num].items():
                    if rsp_k.casefold() == sql_k.casefold():
                        test.assert_text(str(rsp_v).split('.')[0], str(sql_v).split('.')[0])    # 和数据库对比

    @allure.title('讲义制作-讲义管理列表')
    @allure.feature('JYZZ_admin_get_list')
    @allure.severity('critical')
    @allure.story('JYZZ_admin_get_list')
    @allure.step("JYZZ_admin_get_list")
    def test_admin_get_list(self, get_JYZZ_param, get_sql_server):
        """
            获取管理端讲义列表，校验statusCode、数据库、test_apply添加
        """
        url = get_JYZZ_param.get('url') + get_JYZZ_param.get('data').get('get_list_url')
        get_list_data = get_JYZZ_param.get('data').get('get_list_data')
        get_list_data['conModels'][0]['fieldName'] = 'currentActive'
        get_list_data['conModels'][0]['fieldValue'] = '1,2,3'
        get_list_data['conModels'][0]['conditionalType'] = 6
        page_size = random.randrange(10, 100, 10)
        get_list_data['pageSize'] = page_size
        response = request.post_request(url=url, data=get_list_data, token=get_JYZZ_param.get('token'))
        sql = "select top {} * from GSM_JYZZ_Apply where IsDelete = 0 and CurrentActive != 0 order by Id desc".format(
            page_size)
        get_sql_server.execute(sql)
        apply_sql_result = get_sql_server.fetchall()
        sql_title = arr_sql_title(get_sql_server.description)
        sql_result = arr_sql_param(sql_title, apply_sql_result)
        log.info('Response:%s\nSQL:%s' % (str(response), str(apply_sql_result)))
        data_result = response.get('body').get('data').get('data')
        with allure.step('校验结果'):
            allure.attach(str(response), '实际结果')
            allure.attach('1、创建时间倒序排序\n2、创建信息展示', '预期结果')
        test.assert_code(response.get('body').get('statusCode'), 200)
        test.assert_text(len(data_result), len(sql_result))
        for k, v in assert_dict['exed_apply_data'].items():
            if k == 'applyNo' or k == 'id':
                continue
            test.assert_text(str(data_result[0][k]), str(v))
        for rsp_num in range(len(data_result)):
            for rsp_k, rsp_v in data_result[rsp_num].items():
                for sql_k, sql_v in sql_result[rsp_num].items():
                    if rsp_k.casefold() == sql_k.casefold():
                        test.assert_text(str(rsp_v).split('.')[0], str(sql_v).split('.')[0])    # 和数据库对比


if __name__ == '__main__':
    pytest.main(['-s', '-v'])
