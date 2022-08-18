# -*- coding: utf-8 -*-
# @Time   : 2022/8/1 11:03
# @Author : qiuzonghang
# @File   : Config.py

import os
import sys

from configparser import ConfigParser
from qz_auto_test.Common import Log


class Config:
    # titles:
    TITLE_DEV = "env_dev"
    # TITLE_RELEASE = "online_release"
    TITLE_UAT = "env_uat"
    TITLE_USER_WANGYE_DEV = 'user_wangye_dev'
    TITLE_USER_ITTEST2_UAT = 'user_ITtest2_uat'
    TITLE_USER_ITTEST3_UAT = 'user_ITtest3_uat'
    TITLE_USER_TESTER3_DEV = 'user_tester3_dev'
    TITLE_SQL_SERVER_DEV = 'sql_server_dev'
    TITLE_SQL_SERVER_UAT = 'sql_server_uat'

    # values:
    # [debug\release]
    VALUE_TESTER = "tester"
    VALUE_ENVIRONMENT = "environment"
    VALUE_VERSION_CODE = "versionCode"
    VALUE_HOST = "host"
    VALUE_USERNAME = 'username'
    VALUE_PASSWORD = 'password'
    VALUE_DATABASE = 'database'

    # path
    path_dir = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

    def __init__(self):
        """
        初始化
        """
        self.config = ConfigParser()
        self.log = Log.MyLog()
        self.conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
        self.xml_report_path = Config.path_dir + '/Report/xml'
        self.html_report_path = Config.path_dir + '/Report/html'

        if not os.path.exists(self.conf_path):
            raise FileNotFoundError("请确保配置文件存在！")

        self.config.read(self.conf_path, encoding='utf-8')

        self.tester_dev = self.get_conf(Config.TITLE_DEV, Config.VALUE_TESTER)
        self.environment_dev = self.get_conf(Config.TITLE_DEV, Config.VALUE_ENVIRONMENT)
        self.versionCode_dev = self.get_conf(Config.TITLE_DEV, Config.VALUE_VERSION_CODE)
        self.host_dev = self.get_conf(Config.TITLE_DEV, Config.VALUE_HOST)

        self.tester_uat = self.get_conf(Config.TITLE_UAT, Config.VALUE_TESTER)
        self.environment_uat = self.get_conf(Config.TITLE_UAT, Config.VALUE_ENVIRONMENT)
        self.versionCode_uat = self.get_conf(Config.TITLE_UAT, Config.VALUE_VERSION_CODE)
        self.host_uat = self.get_conf(Config.TITLE_UAT, Config.VALUE_HOST)

        self.wangye_username_dev = self.get_conf(Config.TITLE_USER_WANGYE_DEV, Config.VALUE_USERNAME)
        self.wangye_password_dev = self.get_conf(Config.TITLE_USER_WANGYE_DEV, Config.VALUE_PASSWORD)
        self.tester3_username_dev = self.get_conf(Config.TITLE_USER_TESTER3_DEV, Config.VALUE_USERNAME)
        self.tester3_password_dev = self.get_conf(Config.TITLE_USER_TESTER3_DEV, Config.VALUE_PASSWORD)
        self.ITtest2_username_uat = self.get_conf(Config.TITLE_USER_ITTEST2_UAT, Config.VALUE_USERNAME)
        self.ITtest2_password_uat = self.get_conf(Config.TITLE_USER_ITTEST2_UAT, Config.VALUE_PASSWORD)
        self.ITtest3_username_uat = self.get_conf(Config.TITLE_USER_ITTEST3_UAT, Config.VALUE_USERNAME)
        self.ITtest3_password_uat = self.get_conf(Config.TITLE_USER_ITTEST3_UAT, Config.VALUE_PASSWORD)
        self.sql_server_host_dev = self.get_conf(Config.TITLE_SQL_SERVER_DEV, Config.VALUE_HOST)
        self.sql_server_database_dev = self.get_conf(Config.TITLE_SQL_SERVER_DEV, Config.VALUE_DATABASE)
        self.sql_server_username_dev = self.get_conf(Config.TITLE_SQL_SERVER_DEV, Config.VALUE_USERNAME)
        self.sql_server_password_dev = self.get_conf(Config.TITLE_SQL_SERVER_DEV, Config.VALUE_PASSWORD)
        self.sql_server_host_uat = self.get_conf(Config.TITLE_SQL_SERVER_UAT, Config.VALUE_HOST)
        self.sql_server_database_uat = self.get_conf(Config.TITLE_SQL_SERVER_UAT, Config.VALUE_DATABASE)
        self.sql_server_username_uat = self.get_conf(Config.TITLE_SQL_SERVER_UAT, Config.VALUE_USERNAME)
        self.sql_server_password_uat = self.get_conf(Config.TITLE_SQL_SERVER_UAT, Config.VALUE_PASSWORD)

    def get_conf(self, title, value):
        """
        配置文件读取
        :param title:
        :param value:
        :return:
        """
        return self.config.get(title, value)

    def set_conf(self, title, value, text):
        """
        配置文件修改
        :param title:
        :param value:
        :param text:
        :return:
        """
        self.config.set(title, value, text)
        with open(self.conf_path, "w+") as f:
            return self.config.write(f)

    def add_conf(self, title):
        """
        配置文件添加
        :param title:
        :return:
        """
        self.config.add_section(title)
        with open(self.conf_path, "w+") as f:
            return self.config.write(f)
