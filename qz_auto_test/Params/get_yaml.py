# -*- coding: utf-8 -*-
# @Time   : 2022/8/1 11:17
# @Author : qiuzonghang
# @File   : get_yaml.py

import yaml
import os.path


def parse():
    path_ya = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))) + '/Params/YAML_DATA'
    # print(path_ya)
    pages = {}
    for root, dirs, files in os.walk(path_ya):
        for name in files:
            watch_file_path = os.path.join(root, name)
            with open(watch_file_path, 'r', encoding='utf-8') as f:
                page = yaml.safe_load(f)
                pages.update(page)
        # print(pages)
        return pages


class GetPages:
    @staticmethod
    def get_page_list():
        _page_list = {}
        pages = parse()
        for page, value in pages.items():
            parameters = value['parameters']
            data_list = []

            for parameter in parameters:
                data_list.append(parameter)
            _page_list[page] = data_list
        # print(_page_list)
        return _page_list

# test = GetPages
# print(test.get_page_list())