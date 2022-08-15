# -*- coding: utf-8 -*-
# @Time   : 2022/8/5 11:50
# @Author : qiuzonghang
# @File   : test_add_GWYC.py
import random

from Mimir.qz_auto_test.Common.Request import Request
from Mimir.qz_auto_test.Common.Log import MyLog
from Mimir.qz_auto_test.Common.Assert import Assertions
import allure
import pytest
import uuid
import time

log = MyLog()
request = Request()
test = Assertions()
assert_dict = {}


@pytest.mark.usefixtures('get_GWYC_param', 'get_sql_server')
@pytest.mark.GWYC
class TestCase:

    @allure.title('公务用车-获取user信息')
    @allure.feature('GWYC_user_info')
    @allure.severity('critical')
    @allure.story('GWYC_user_info')
    @allure.step("GWYC_user_info")
    def test_user_info(self, get_GWYC_param):
        """
            数据依赖，校验关键词结果
        """
        url = get_GWYC_param.get('url') + get_GWYC_param.get('data').get('get_user_url')
        data = get_GWYC_param.get('data').get('get_user_data')
        token = get_GWYC_param.get('token')
        # print(get_GWYC_param)
        data['queryText'] = get_GWYC_param.get('user_info').get('data').get('hrCname')
        r = request.post_request(url=url, data=data, token=token)
        random_dt = random.choice(r.get('body').get('data').get('data'))
        assert_dict['user_dt'] = {'user_id': str(random_dt.get('id')), 'cname': random_dt.get('cname'), 'dt': random_dt.get('departmentName'), 'dt_id': str(random_dt.get('departmentId')), 'email': random_dt.get('email')}
        log.info(str(r))
        with allure.step('校验结果'):
            allure.attach(str(r), '实际结果')
            allure.attach('username关键词为%s' % get_GWYC_param.get('user_info').get('data').get('hrCname'), '预期结果')
        test.assert_code(r.get('body').get('statusCode'), 200)
        for user_dt in r.get('body').get('data').get('data'):
            test.assert_text(user_dt.get('cname').casefold(), data['queryText'].casefold())

    @allure.title('公务用车-发起工单')
    @allure.feature('GWYC_apply')
    @allure.severity('critical')
    @allure.story('GWYC_apply')
    @allure.step('GWYC_apply')
    def test_apply(self, get_GWYC_param, get_sql_server):
        """
            校验新增公务用车，依赖 test_user_info case信息
        """
        url = get_GWYC_param.get('url') + get_GWYC_param.get('data').get('apply_GWYC_url')
        apply_data = get_GWYC_param.get('data').get('apply_GWYC_data')
        apply_data['userDepartmentId'] = assert_dict['user_dt']['dt_id']
        apply_data['userDepartmentName'] = assert_dict['user_dt']['dt']
        apply_data['userName'] = assert_dict['user_dt']['cname']
        apply_data['userId'] = assert_dict['user_dt']['user_id']
        apply_data['costTotal'] = random.randrange(10, 100, 10)
        apply_data['financialNumber'] = str(uuid.uuid1())
        r = request.post_request(url=url, data=apply_data, token=get_GWYC_param.get('token'))
        sql_server = get_sql_server
        sql = "select * from GSMOfficialVehiclesApply order by Id desc"
        sql_server.execute(sql)
        apply_sql_result = sql_server.fetchall()[0]
        assert_dict['creation_time'] = apply_sql_result[2]
        assert_dict['user_name'] = apply_sql_result[9]
        log.info('Response:%s\nSQL check:%s' % (str(r), apply_sql_result))
        assert_data = apply_sql_result[7:12]
        with allure.step('校验结果'):
            allure.attach(str(r), '实际结果')
            allure.attach('验证创建正常，数据库数据正确，具体看下方log', '预期结果')
        test.assert_code(r.get('body').get('statusCode'), 200)
        test.assert_text(r.get('body').get('data').get('applicationNo'), assert_data[0])
        test.assert_three_text(r.get('body').get('data').get('userId'), assert_data[1], assert_dict['user_dt']['user_id'])
        test.assert_three_text(r.get('body').get('data').get('userName'), assert_data[2], assert_dict['user_dt']['cname'])
        test.assert_three_text(r.get('body').get('data').get('userDepartmentId'), assert_data[3], assert_dict['user_dt']['dt_id'])
        test.assert_three_text(r.get('body').get('data').get('userDepartmentName'), assert_data[4], assert_dict['user_dt']['dt'])

    @allure.title('公务用车-check邮件')
    @allure.feature('GWYC_send_email')
    @allure.severity('critical')
    @allure.story('GWYC_send_email')
    @allure.step('GWYC_send_email')
    def test_send_email(self, get_sql_server, get_GWYC_param):
        """
            校验新增公务用车后是否会发送邮件，依赖 test_apply case 创建，发送邮件会有延迟，验证时会有60s等待时间
        """
        time.sleep(60)          # 接受邮件有延迟
        sql_server = get_sql_server
        sql = "select * from GsmPkuMailLog order by Id desc"
        sql_server.execute(sql)
        email_sql_result = sql_server.fetchall()[0]
        log.info(str(email_sql_result))
        with allure.step('校验结果'):
            allure.attach(str(email_sql_result), '实际结果')
            allure.attach('数据库数据正确，具体看下方log', '预期结果')
        test.assert_text(str(email_sql_result[1])[0:16], str(assert_dict['creation_time'])[0:16])
        test.assert_text(email_sql_result[4], '%s的公务用车申请' % assert_dict['user_name'])
        test.assert_text(email_sql_result[3], get_GWYC_param.get('user_info').get('data').get('email'))


if __name__ == '__main__':
    pytest.main(['-s', '-v'])