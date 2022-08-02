# -*- coding: utf-8 -*-
# @Time   : 2022/8/2 10:45
# @Author : qiuzonghang
# @File   : Request.py

import os
import random
import requests
import json
from retrying import retry


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

        except requests.RequestException as e:
            print('%s%s' % ('RequestException url: ', url))
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

        response_json = json.loads(response.text)
        return response_json

