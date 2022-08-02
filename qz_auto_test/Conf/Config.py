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
    # TITLE_Pre = "public_pre"

    # values:
    # [debug\release]
    VALUE_TESTER = "tester"
    VALUE_ENVIRONMENT = "environment"
    VALUE_VERSION_CODE = "versionCode"
    VALUE_HOST = "host"
    # VALUE_LOGIN_HOST = "loginHost"
    # VALUE_LOGIN_INFO = "loginInfo"
    # # [mail]
    # VALUE_SMTP_SERVER = "smtpserver"
    # VALUE_SENDER = "sender"
    # VALUE_RECEIVER = "receiver"
    # VALUE_USERNAME = "username"
    # VALUE_PASSWORD = "password"

    # path
    path_dir = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

    def __init__(self):
        """
        初始化
        """
        self.config = ConfigParser()
        self.log = Log.MyLog()
        self.conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
        self.xml_report_path = Config.path_dir+'/Report/xml'
        self.html_report_path = Config.path_dir+'/Report/html'

        if not os.path.exists(self.conf_path):
            raise FileNotFoundError("请确保配置文件存在！")

        self.config.read(self.conf_path, encoding='utf-8')

        self.tester_dev = self.get_conf(Config.TITLE_DEV, Config.VALUE_TESTER)
        self.environment_dev = self.get_conf(Config.TITLE_DEV, Config.VALUE_ENVIRONMENT)
        self.versionCode_dev = self.get_conf(Config.TITLE_DEV, Config.VALUE_VERSION_CODE)
        self.host_dev = self.get_conf(Config.TITLE_DEV, Config.VALUE_HOST)
        #self.loginHost_debug = self.get_conf(Config.TITLE_DEBUG, Config.VALUE_LOGIN_HOST)
        #self.loginInfo_debug = self.get_conf(Config.TITLE_DEBUG, Config.VALUE_LOGIN_INFO)

        # self.tester_release = self.get_conf(Config.TITLE_RELEASE, Config.VALUE_TESTER)
        # self.environment_release = self.get_conf(Config.TITLE_RELEASE, Config.VALUE_ENVIRONMENT)
        # self.versionCode_release = self.get_conf(Config.TITLE_RELEASE, Config.VALUE_VERSION_CODE)
        # self.host_release = self.get_conf(Config.TITLE_RELEASE, Config.VALUE_HOST)
        # #self.loginHost_release = self.get_conf(Config.TITLE_RELEASE, Config.VALUE_LOGIN_HOST)
        # #self.loginInfo_release = self.get_conf(Config.TITLE_RELEASE, Config.VALUE_LOGIN_INFO)
        #
        # self.tester_pre = self.get_conf(Config.TITLE_Pre,Config.VALUE_TESTER)
        # self.environment_pre = self.get_conf(Config.TITLE_Pre,Config.VALUE_ENVIRONMENT)
        # self.versionCode_pre = self.get_conf(Config.TITLE_Pre,Config.VALUE_VERSION_CODE)
        # self.host_pre = self.get_conf(Config.TITLE_Pre,Config.VALUE_HOST)
        #
        # self.tester_release_lineC = self.get_conf(Config.TITLE_RELEASE_LINEC, Config.VALUE_TESTER)
        # self.environment_release_lineC = self.get_conf(Config.TITLE_RELEASE_LINEC, Config.VALUE_ENVIRONMENT)
        # self.versionCode_release_lineC = self.get_conf(Config.TITLE_RELEASE_LINEC, Config.VALUE_VERSION_CODE)
        # self.host_release_lineC = self.get_conf(Config.TITLE_RELEASE_LINEC, Config.VALUE_HOST)
        #
        # self.smtpserver = self.get_conf(Config.TITLE_EMAIL, Config.VALUE_SMTP_SERVER)
        # self.sender = self.get_conf(Config.TITLE_EMAIL, Config.VALUE_SENDER)
        # self.receiver = self.get_conf(Config.TITLE_EMAIL, Config.VALUE_RECEIVER)
        # self.username = self.get_conf(Config.TITLE_EMAIL, Config.VALUE_USERNAME)
        # self.password = self.get_conf(Config.TITLE_EMAIL, Config.VALUE_PASSWORD)

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

