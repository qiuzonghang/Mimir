# -*- coding: utf-8 -*-
# @Time   : 2022/8/2 10:46
# @Author : qiuzonghang
# @File   : test_JYZZ_ApiTest.py

import pytest
import allure
import requests

from Mimir.qz_auto_test.Common.Request import Request
from Mimir.qz_auto_test.Common.Log import MyLog
from Mimir.qz_auto_test.Common.Assert import Assertions

request = Request()
log = MyLog()
test = Assertions()


@pytest.mark.usefixtures('get_JYZZ_param')
class TestCase:

    @allure.title('讲义制作-开课名称')
    @allure.feature('JYZZ-start-class')
    @allure.severity('critical')
    @allure.story('JYZZ-start-class')
    @allure.step("JYZZ-start-class")
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
        with allure.step('校验结果'):
            allure.attach(str(r.get('body').get('data')), '实际结果')
            allure.attach('含有“测试”关键词的开课名称及对应教师', '预期结果')
        test.assert_code(200, r['code'])
        for class_info in class_info_list:
            test.assert_in_text(class_info.get('courseName'), '测试')


if __name__ == '__main__':
    pytest.main(['-s', '-v'])
