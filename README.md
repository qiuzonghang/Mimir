# 接口自动化介绍:
-ApiTestCase：接口测试用例    
-Common：封装方法（例：断言、requests、log等等）    
-Conf：环境变量配置  
-Data：数据（暂时由webdriver调用浏览器获取token，目前只储存了token）  
-Log：log日志  
-Params：储存接口参数及测试数据、读取数据方法等  
-Report：储存测试报告，采用allure生成测试报告  
-run.py：执行脚本（若调试某个用例脚本也可采用pytest.mian())

