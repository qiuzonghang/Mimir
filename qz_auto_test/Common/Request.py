# -*- coding: utf-8 -*-
# @Time   : 2022/8/2 10:45
# @Author : qiuzonghang
# @File   : Request.py

import os
import random
import requests
import json
from retrying import retry
from Mimir.qz_auto_test.Common.Log import MyLog

log = MyLog()


class Request:
    def __init__(self):
        """
        :param env:
        """
        pass

    @retry()
    def get_request(self, url, header, result_type='normal'):    # result_type对特定的结果做一些处理
        """
        Get请求
        :param url:
        :param data:
        :param header:
        :return:
        """
        if not url.startswith('https://'):
            url = '%s%s' % ('https://', url)
        # print(url)
        try:
            response = requests.get(url=url, headers=header)
            log.info('url：{}\nheaders：{}'.format(url, header))
        except requests.RequestException as e:
            log.error('%s%s' % ('RequestException url: ', url))
            print(e)
            return ()

        except Exception as e:
            print('%s%s' % ('Exception url: ', url))
            print(e)
            return ()
        if response.status_code != 200:
            print('status code %s!!!' % response.status_code)
            return ()
        time_consuming = response.elapsed.microseconds / 1000
        time_total = response.elapsed.total_seconds()
        response_dict = {}
        response_json = json.loads(response.text)
        response_dict['body'] = response_json
        response_dict['code'] = response.status_code
        # response_dict['jyzz_start_class'] = response_json.get
        return response_dict

    def post_request(self, url, header, data):
        if not url.startswith('https://'):
            url = '%s%s' % ('https://', url)
        data_json = json.dumps(data)
        # print(data_json)
        # print(url)
        try:
            response = requests.post(url=url, data=data_json, headers=header)
            log.info('url：{}\ndata：{}\nheaders：{}'.format(url, data_json, header))
        except requests.RequestException as e:
            log.error('%s%s' % ('RequestException url: ', url))
            print(e)
            return False

        except Exception as e:
            print('%s%s' % ('Exception url: ', url))
            print(e)
            raise
        if response.status_code != 200:
            print('status code %s!!!' % response.status_code)
            log.info('status code %s!!!' % response.status_code)
            raise
        time_consuming = response.elapsed.microseconds / 1000
        time_total = response.elapsed.total_seconds()
        response_dict = {}
        response_json = json.loads(response.text)
        response_dict['body'] = response_json
        response_dict['code'] = response.status_code
        # response_dict['jyzz_start_class'] = response_json.get
        return response_dict

    def put_request(self, url, header, data):
        if not url.startswith('https://'):
            url = '%s%s' % ('https://', url)
        data_json = json.dumps(data)
        # print(data_json)
        # print(url)
        try:
            response = requests.put(url=url, data=data_json, headers=header)
            log.info('url：{}\ndata：{}\nheaders：{}'.format(url, data_json, header))
        except requests.RequestException as e:
            log.error('%s%s' % ('RequestException url: ', url))
            print(e)
            return False

        except Exception as e:
            print('%s%s' % ('Exception url: ', url))
            print(e)
            raise
        if response.status_code != 200:
            print('status code %s!!!' % response.status_code)
            log.info('status code %s!!!' % response.status_code)
            raise
        time_consuming = response.elapsed.microseconds / 1000
        time_total = response.elapsed.total_seconds()
        response_dict = {}
        response_json = json.loads(response.text)
        response_dict['body'] = response_json
        response_dict['code'] = response.status_code
        # response_dict['jyzz_start_class'] = response_json.get
        return response_dict

    def delete_request(self, url, header):    # result_type对特定的结果做一些处理
        """
        Get请求
        :param url:
        :param data:
        :param header:
        :return:
        """
        if not url.startswith('https://'):
            url = '%s%s' % ('https://', url)
        # print(url)
        try:
            response = requests.delete(url=url, headers=header)
            log.info('url：{}\nheaders：{}'.format(url, header))
        except requests.RequestException as e:
            log.error('%s%s' % ('RequestException url: ', url))
            print(e)
            return ()

        except Exception as e:
            print('%s%s' % ('Exception url: ', url))
            print(e)
            return ()
        if response.status_code != 200:
            print('status code %s!!!' % response.status_code)
            return ()
        time_consuming = response.elapsed.microseconds / 1000
        time_total = response.elapsed.total_seconds()
        response_dict = {}
        response_json = json.loads(response.text)
        response_dict['body'] = response_json
        response_dict['code'] = response.status_code
        # response_dict['jyzz_start_class'] = response_json.get
        return response_dict

