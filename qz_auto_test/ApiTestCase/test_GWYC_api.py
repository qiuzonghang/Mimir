# -*- coding: utf-8 -*-
# @Time   : 2022/8/5 11:50
# @Author : qiuzonghang
# @File   : test_GWYC_api.py
import random

from qz_auto_test.Common.Request import Request
from qz_auto_test.Common.Log import MyLog
from qz_auto_test.Common.Assert import Assertions
from qz_auto_test.Params.params import arr_sql_param, arr_sql_title
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
@pytest.mark.site
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
        assert_dict['new_application_no'] = r.get('body').get('data').get('applicationNo')
        assert_dict['new_id'] = r.get('body').get('data').get('id')
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
        # time.sleep(60)          # 接受邮件有延迟
        sql_server = get_sql_server
        sql = "select * from GsmPkuMail order by Id desc"
        sql_server.execute(sql)
        email_sql_result = sql_server.fetchall()[0]
        log.info(str(email_sql_result))
        with allure.step('校验结果'):
            allure.attach(str(email_sql_result), '实际结果')
            allure.attach('数据库数据正确，具体看下方log', '预期结果')
        test.assert_text(str(email_sql_result[1])[0:16], str(assert_dict['creation_time'])[0:16])
        test.assert_text(email_sql_result[4], '%s的公务用车申请' % assert_dict['user_name'])
        test.assert_text(email_sql_result[3], get_GWYC_param.get('user_info').get('data').get('email'))

    @allure.title('公务用车-获取管理端工单列表')
    @allure.feature('GWYC_get_list')
    @allure.severity('critical')
    @allure.story('GWYC_get_list')
    @allure.step('GWYC_get_list')
    def test_get_list(self, get_GWYC_param, get_sql_server):
        """
            校验管理端工单列表，依赖test_apply case 创建，验证数据库、test_apply工单号、排序等
        """
        url = get_GWYC_param.get('url') + get_GWYC_param.get('data').get('get_list_url')
        data = get_GWYC_param.get('data').get('get_list_data')
        random_page_size = random.randrange(10, 100, 10)
        data['pageSize'] = random_page_size
        r = request.post_request(url=url, data=data, token=get_GWYC_param.get('token'))
        sql = 'select top {} * from GSMOfficialVehiclesApply order by Id desc '.format(random_page_size)
        get_sql_server.execute(sql)
        sql_data_list = get_sql_server.fetchall()
        sql_title = arr_sql_title(get_sql_server.description)
        sql_result = arr_sql_param(sql_title=sql_title, sql_data_list=sql_data_list)
        response_result = r.get('body').get('data').get('data')
        log.info('Response:%s\nSql Result:%s' % (str(r), sql_data_list))
        with allure.step('校验结果'):
            allure.attach(str(response_result), '实际结果')
            allure.attach('数据库数据、排序、test_apply单号正确，具体看下方log', '预期结果')
        test.assert_code(r.get('body').get('statusCode'), 200)
        test.assert_three_text(response_result[0]['applicationNo'], sql_result[0]['ApplicationNo'], assert_dict['new_application_no'])
        test.assert_text(len(response_result), len(sql_result))
        for rsp_num in range(len(response_result)):
            for rsp_k, rsp_v in response_result[rsp_num].items():
                for sql_k, sql_v in sql_result[rsp_num].items():
                    if rsp_k.casefold() == sql_k.casefold():
                        test.assert_text(str(rsp_v).split('.')[0], str(sql_v).split('.')[0])

    @allure.title('公务用车-我的待办')
    @allure.feature('GWYC_my_dealt')
    @allure.severity('critical')
    @allure.story('GWYC_my_dealt')
    @allure.step('GWYC_my_dealt')
    def test_my_dealt(self, get_GWYC_param, get_sql_server):
        """
            校验工单是否发送我的待办，验证待办数据+数据库数据+test_apply创建工单是否一致
        """
        url = get_GWYC_param.get('url') + get_GWYC_param.get('data').get('get_my_dealt_url')
        my_dealt_data = get_GWYC_param.get('data').get('get_my_dealt_data')
        random_page_size = random.randrange(10, 100, 10)
        my_dealt_data['pageSize'] = random_page_size
        my_dealt_data_list = []
        [my_dealt_data_list.append(k + '=' + str(v)) for k, v in my_dealt_data.items()]
        r = request.get_request(url=url + '&'.join(my_dealt_data_list), token=get_GWYC_param.get('token'))
        sql = 'select top {} * from GSMProess where IsDelete = 0 order by ID desc'.format(random_page_size)
        get_sql_server.execute(sql)
        sql_data_list = get_sql_server.fetchall()[0]
        sql_title = arr_sql_title(get_sql_server.description)
        sql_result = arr_sql_param(sql_title, sql_data_list)
        my_dealt_response = r.get('body').get('data').get('data')[0]
        with allure.step('校验结果'):
            allure.attach(str(my_dealt_response), '实际结果')
            allure.attach('数据库数据、test_apply数据同步，具体看下方log', '预期结果')
        test.assert_code(r.get('body').get('statusCode'), 200)
        test.assert_three_text(my_dealt_response['processCode'], sql_result['ProcessCode'], str(assert_dict['new_id']))

    @allure.title('公务用车-无待办明细')
    @allure.feature('GWYC_dealt_noData')
    @allure.severity('critical')
    @allure.story('GWYC_dealt_noData')
    @allure.step('GWYC_dealt_noData')
    def test_get_dealt_noData(self, get_GWYC_param, get_sql_server):
        """
            （无数据）获取待办审核明细、申请信息、审核日志，校验数据库
        """
        approve_dealt_url = get_GWYC_param.get('url') + get_GWYC_param.get('data').get('apply_GWYC_url') + '/ApproveDetail?approveID=%s&readOnly=false' % assert_dict['new_id']
        base_info_url = get_GWYC_param.get('url') + get_GWYC_param.get('data').get('apply_GWYC_url') + '/%s' % assert_dict['new_id']
        approve_dealt_rsp = request.get_request(url=approve_dealt_url, token=get_GWYC_param.get('token'))
        base_info_rsp = request.get_request(url=base_info_url, token=get_GWYC_param.get('token'))
        sql = 'select * from GSMOfficialVehiclesApply order by Id desc '
        get_sql_server.execute(sql)
        sql_data_list = get_sql_server.fetchall()[0]
        sql_title = arr_sql_title(get_sql_server.description)
        sql_result = arr_sql_param(sql_title=sql_title, sql_data_list=sql_data_list)
        user_apply_info = base_info_rsp.get('body').get('data').get('baseInfo').get('gsmVacationApplyInfo')[0]
        # user_apply_info.update(base_info_rsp.get('body').get('data').get('baseInfo').get('loginfo')[0])
        log_info = base_info_rsp.get('body').get('data').get('baseInfo').get('loginfo')[0]
        with allure.step('校验结果'):
            allure.attach('ApproveDealt:%s\nBaseIndo:%s' % (approve_dealt_rsp, base_info_rsp), '实际结果')
            allure.attach('数据库数据、test_apply数据同步，具体看下方log', '预期结果')
        test.assert_code(approve_dealt_rsp.get('body').get('statusCode'), 200)
        test.assert_code(base_info_rsp.get('body').get('statusCode'), 200)
        test.assert_text(approve_dealt_rsp.get('body').get('data'), None)
        test.assert_text(base_info_rsp.get('body').get('data').get('id'), assert_dict['new_id'])
        for rsp_k, rsp_v in user_apply_info.items():
            for sql_k, sql_v in sql_result.items():
                if rsp_k.casefold() == sql_k.casefold():
                    test.assert_text(str(rsp_v).split('.')[0], str(sql_v).split('.')[0])
        test.assert_text(log_info.get('applicant'), sql_result.get('ApplyName'))
        test.assert_text(log_info.get('applicationCreateTime'), str(sql_result.get('CreationTime')).split('.')[0])
        test.assert_text(log_info.get('lastModifierName'), sql_result.get('LastModifierName'))
        test.assert_text(log_info.get('lastModifiyTime'), str(sql_result.get('LastModificationTime')).split('.')[0])

    @allure.title('公务用车-我的待办保存明细')
    @allure.feature('GWYC_dealt_save')
    @allure.severity('critical')
    @allure.story('GWYC_dealt_save')
    @allure.step('GWYC_dealt_save')
    def test_dealt_save_data(self, get_GWYC_param, get_sql_server):
        pass


if __name__ == '__main__':
    pytest.main(['-s', '-v'])