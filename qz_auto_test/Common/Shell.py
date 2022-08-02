# -*- coding: utf-8 -*-
# @Time   : 2022/8/2 16:09
# @Author : qiuzonghang
# @File   : Shell.py

import subprocess


class Shell:
    @staticmethod
    def invoke(cmd):
        output, errors = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        o = output.decode("utf-8")
        return o
