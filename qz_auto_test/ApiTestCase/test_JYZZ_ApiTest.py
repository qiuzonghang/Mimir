# -*- coding: utf-8 -*-
# @Time   : 2022/8/2 10:46
# @Author : qiuzonghang
# @File   : test_JYZZ_ApiTest.py

import pytest
import allure
import requests

from qz_auto_test.Common.Request import Request

request = Request()


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
        print(r)


if __name__ == '__main__':
    pytest.main(['-s', '-v'])
