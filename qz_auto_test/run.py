# -*- coding: utf-8 -*-
# @Time   : 2022/8/2 16:08
# @Author : qiuzonghang
# @File   : run.py

import pytest
import sys
import os
# curPath = os.path.abspath(os.path.dirname(__file__))
# rootPath = os.path.split(curPath)[0]
# sys.path.append(rootPath)
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from qz_auto_test.Common import Log, Shell
from qz_auto_test.Conf import Config
from qz_auto_test.Common.Func import remove_dir

if __name__ == '__main__':
    conf = Config.Config()
    log = Log.MyLog()
    log.info('初始化配置文件,path=' + conf.conf_path)
    project_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    shell = Shell.Shell()
    xml_report_path = conf.xml_report_path
    html_report_path = conf.html_report_path
    log.info('清理上一次测试报告')
    remove_dir(xml_report_path)
    remove_dir(html_report_path)
    # 定义测试集
    args = ['-s', '-v', '-m=site', '--alluredir', xml_report_path]
    log.info('执行测试...')
    pytest.main(args)
    # 生成测试报告，将前提步骤中的xml文件生成报告保存在指定目录下
    # allure generate 测试结果数据所在目录 -o 测试报告保存的目录 --clean
    log.info('生成报告...')
    cmd = 'allure generate %s -o %s' % (xml_report_path, html_report_path)

    try:
        shell.invoke(cmd)
    except Exception:
        log.error('执行用例失败,请检查环境配置')
        raise