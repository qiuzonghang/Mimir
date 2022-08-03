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
from Mimir.qz_auto_test.Params.params import get_JYZZ_apply_param

request = Request()
log = MyLog()
test = Assertions()
assert_dict = {}


@pytest.mark.usefixtures('get_JYZZ_param')
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
        url = host + '&'.join(data_list) + '测试'
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
            allure.attach('含有“测试”关键词的开课名称及对应教师', '预期结果')
        test.assert_code(200, r['code'])
        for class_info in class_info_list:
            test.assert_in_text(class_info.get('courseName'), '测试')
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
        url = host + '&'.join(data_list) + '测试'
        header = {'authorization': get_JYZZ_param['token']}
        r = request.get_request(url=url, header=header)
        log.info(str(r))
        class_info_list = r.get('body').get('data')
        random_school_class_info = random.choice(class_info_list)
        assert_dict['startClassName'] = random_school_class_info.get('studendtClassName')
        assert_dict['startClassId'] = random_school_class_info.get('id')
        with allure.step('校验结果'):
            allure.attach(str(class_info_list), '实际结果')
            allure.attach('含有“测试”关键词', '预期结果')
        test.assert_code(200, r['code'])
        for class_info in class_info_list:
            test.assert_in_text(class_info.get('studendtClassName'), '测试')

    @allure.title('讲义制作-新建讲义')
    @allure.feature('JYZZ_apply')
    @allure.severity('critical')
    @allure.story('JYZZ_apply')
    @allure.step("JYZZ_apply")
    def test_apply(self, get_JYZZ_param):
        url = get_JYZZ_param.get('url') + get_JYZZ_param.get('data').get('apply_url')
        apply_data = get_JYZZ_param.get('data').get('apply_data')
        header = {'authorization': get_JYZZ_param['token'], 'content-type': 'application/json'}
        data = get_JYZZ_apply_param(origin_param=apply_data, result_param=assert_dict)
        random_depInfo = random.choice(get_JYZZ_param.get('user_info').get('data').get('depInfo'))
        data['departmentName'] = random_depInfo.get('departmentName')
        data['departmentId'] = random_depInfo.get('departmentId')
        assert_dict['apply_data'] = data
        r = request.post_request(url=url, header=header, data=data)
        log.info(str(r))
        with allure.step('校验结果'):
            allure.attach(str(r), '实际结果')
            allure.attach('验证创建正常，下个case验证创建后数据是否正确', '预期结果')
        test.assert_code(r.get('code'), 200)
        test.assert_code(r.get('body').get('statusCode'), 200)

    @allure.title('讲义制作-开课班级')
    @allure.feature('JYZZ_apply')
    @allure.severity('critical')
    @allure.story('JYZZ_apply')
    @allure.step("JYZZ_apply")
    def test_get_list(self):
        pass


if __name__ == '__main__':
    pytest.main(['-s', '-v'])
