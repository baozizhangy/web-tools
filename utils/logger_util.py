# #!/usr/bin/env python
# # -*- coding: UTF-8 -*-
# import logging
# import os
#
# BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# # 定义日志文件路径
# LOG_PATH = os.path.join(BASE_PATH, "logs")
# if not os.path.exists(LOG_PATH):
#     os.mkdir(LOG_PATH)
#
#
# class Logger:
#     def __init__(self, log_name, log_level=logging.DEBUG, log_format=None, log_path=LOG_PATH):
#         self.log_name = os.path.join(log_path, log_name)
#         # 为每个日志实例赋予一个唯一的logger名称，可以结合log_name生成
#         self.logger = logging.getLogger(f"{__name__}.{log_name}")
#         self.logger.setLevel(log_level)
#
#         self.formatter = logging.Formatter(
#             log_format or '[%(asctime)s][%(filename)s %(lineno)d][%(levelname)s]: %(message)s')
#
#         self.filelogger = logging.FileHandler(self.log_name, mode='a', encoding="UTF-8")
#         self.console = logging.StreamHandler()
#         self.console.setLevel(log_level)
#         self.filelogger.setLevel(log_level)
#         self.filelogger.setFormatter(self.formatter)
#         self.console.setFormatter(self.formatter)
#         self.logger.addHandler(self.filelogger)
#         self.logger.addHandler(self.console)
#
#
# # web工具及后端日志对象
# web_logger = Logger("webtools.log").logger
#
# # 自动化测试执行日志对象
# auto_logger = Logger("autotest.log").logger
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import logging
import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# 定义日志文件路径
LOG_PATH = os.path.join(BASE_PATH, "logs")
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)


class Logger:
    def __init__(self, log_name, log_level=logging.DEBUG, log_format=None, log_path=LOG_PATH):
        self.log_name = os.path.join(log_path, log_name)
        # 为每个日志实例赋予一个唯一的logger名称，可以结合log_name生成
        self.logger = logging.getLogger(f"{__name__}.{log_name}")
        self.logger.setLevel(log_level)

        self.formatter = logging.Formatter(
            log_format or '[%(asctime)s][%(filename)s %(lineno)d][%(levelname)s]: %(message)s')

        # 避免重复添加 handler
        if not self.logger.handlers:
            self.filelogger = logging.FileHandler(self.log_name, mode='a', encoding="UTF-8")
            self.console = logging.StreamHandler()
            self.console.setLevel(log_level)
            self.filelogger.setLevel(log_level)
            self.filelogger.setFormatter(self.formatter)
            self.console.setFormatter(self.formatter)
            self.logger.addHandler(self.filelogger)
            self.logger.addHandler(self.console)


# web工具及后端日志对象
web_logger = Logger("webtools.log").logger

# 自动化测试执行日志对象
auto_logger = Logger("autotest.log").logger
