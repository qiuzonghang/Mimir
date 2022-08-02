# -*- coding: utf-8 -*-
# @Time   : 2022/8/2 16:17
# @Author : qiuzonghang
# @File   : Assert.py

from qz_auto_test.Common import Log
from qz_auto_test.Common import Consts
import json


class Assertions:
    def __init__(self):
        self.log = Log.MyLog()

    def assert_code(self, code, expected_code):
        """
        验证response状态码
        :param code:
        :param expected_code:
        :return:
        """
        try:
            assert code == expected_code
            return True
        except:
            self.log.error("statusCode error, expected_code is %s, statusCode is %s " % (expected_code, code))
            Consts.RESULT_LIST.append('fail')

            raise

    def assert_body(self, body, body_msg, expected_msg):
        """
        验证response body中任意属性的值
        :param body:
        :param body_msg:
        :param expected_msg:为喂！
        :return:
        """
        try:
            msg = body[body_msg]
            assert msg == expected_msg
            return True

        except:
            self.log.error("Response body msg != expected_msg, expected_msg is %s, body_msg is %s" % (expected_msg, msg))
            Consts.RESULT_LIST.append('fail')

            raise

    def assert_body_message_random(self, body, expected_msg):
        try:
            assert body in expected_msg
            return True

        except:
            self.log.error("Response body isn't in expected_msg, expected_msg is %s, body_msg is %s" % (expected_msg, body))
            Consts.RESULT_LIST.append('fail')

            raise

    def assert_in_text(self, body, expected_msg):
        """
        验证response body中是否包含预期字符串
        :param body:
        :param expected_msg:
        :return:
        """
        try:
            text = json.dumps(body, ensure_ascii=False)
            # print(text)
            assert expected_msg in body
            return True

        except:
            self.log.error("Response body Does not contain expected_msg, expected_msg is %s, body is %s" % (expected_msg, body))
            Consts.RESULT_LIST.append('fail')

            raise

    def assert_in_expected_msg(self, body, expected_msg):
        """
        验证response body中是否包含预期字符串
        :param body:
        :param expected_msg:
        :return:
        """
        try:
            assert body in expected_msg
            return True

        except:
            self.log.error("Expected_msg Does not contain response body, expected_msg is %s, body is %s" % (expected_msg, body))
            Consts.RESULT_LIST.append('fail')

            raise

    def assert_text(self, body, expected_msg):
        """
        验证response body中是否等于预期字符串
        :param body:
        :param expected_msg:
        :return:
        """
        try:
            assert body == expected_msg
            return True

        except:
            self.log.error("Response body != expected_msg, expected_msg is %s, body is %s" % (expected_msg, body))
            Consts.RESULT_LIST.append('fail')

            raise

    def assert_time(self, time, expected_time):
        """
        验证response body响应时间小于预期最大响应时间,单位：毫秒
        :param body:
        :param expected_time:
        :return:
        """
        try:
            assert time < expected_time
            return True

        except:
            self.log.error("Response time > expected_time, expected_time is %s, time is %s" % (expected_time, time))
            Consts.RESULT_LIST.append('fail')

            raise

    def assert_in_response(self, body, expected_msg):
        """
        验证response body中是否包含预期字符串
        :param body:
        :param expected_msg:
        :return:
        """
        try:
            text = json.dumps(body, ensure_ascii=False)
            assert expected_msg in text
            return True

        except:
            self.log.error("Response body Does not contain expected_msg, expected_msg is %s" % expected_msg)
            Consts.RESULT_LIST.append('fail')

            raise

    def assert_not_is_body(self, body, expected_msg):
        """
                验证response body中是否不等于预期字符串
                :param body:
                :param expected_msg:
                :return:
                """
        try:
            assert body != expected_msg
            return True

        except:
            self.log.error("Response body == expected_msg, expected_msg is %s, body is %s" % (expected_msg, body))
            Consts.RESULT_LIST.append('fail')

            raise

    def assert_not_in_text(self, body, expected_msg):
        """
                验证response body中是否期字符串
                :param body:
                :param expected_msg:
                :return:
                """
        try:
            assert expected_msg not in body
            return True

        except:
            self.log.error("Response expected_msg not in body, expected_msg is %s, body is %s" % (expected_msg, body))
            Consts.RESULT_LIST.append('fail')

            raise

    def assert_slots_text(self, body, expected_msg):
        """
                验证response body中是否期字符串
                :param body:
                :param expected_msg:
                :return:
                """
        try:
            expected_msg_list = expected_msg.split('|')
            body_list = body.split('|')
            for body_str in body_list:
                if body_str in expected_msg_list:
                    pass
                else:
                    raise
            # assert expected_msg not in body
            return True

        except:
            self.log.error("Response expected_msg not in body, expected_msg is %s, body is %s" % (expected_msg, body))
            Consts.RESULT_LIST.append('fail')

            raise
