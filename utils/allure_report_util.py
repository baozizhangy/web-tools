# #!/usr/bin/env python
# # -*- coding: UTF-8 -*-
# """
# Allure报告推送企业微信工具类
# """
#
# import requests
# import json
# import os
# import sys
# import subprocess
#
# # 添加项目根目录到Python路径
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
#
# from utils.logger_util import auto_logger
#
#
# class AllureReportUtil:
#     """Allure报告推送工具类"""
#
#     def __init__(self, webhook_url):
#         """
#         初始化
#         :param webhook_url: 企业微信机器人webhook地址
#         """
#         self.webhook_url = webhook_url
#
#     def generate_allure_report(self, results_dir="./reports/allure_results", report_dir="./reports/allure-reports"):
#         """
#         生成allure报告
#         :param results_dir: allure结果目录
#         :param report_dir: allure报告目录
#         :return: 是否生成成功
#         """
#         try:
#             # 检查结果目录是否存在
#             if not os.path.exists(results_dir):
#                 auto_logger.error(f"Allure结果目录不存在: {results_dir}")
#                 return False
#
#             # 创建报告目录
#             if not os.path.exists(report_dir):
#                 os.makedirs(report_dir)
#
#             # 生成报告命令
#             cmd = f"allure generate {results_dir} -o {report_dir} --clean"
#             result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
#
#             if result.returncode == 0:
#                 auto_logger.info("Allure报告生成成功")
#                 return True
#             else:
#                 auto_logger.error(f"Allure报告生成失败: {result.stderr}")
#                 return False
#         except Exception as e:
#             auto_logger.error(f"生成Allure报告异常: {e}")
#             return False
#
#     def send_report_to_wechat(self, report_title="接口自动化测试报告", report_url=None,
#                               summary=None, report_dir="./reports/allure-reports"):
#         """
#         推送报告到企业微信
#         :param report_title: 报告标题
#         :param report_url: 报告访问地址
#         :param summary: 报告摘要信息
#         :param report_dir: 报告目录
#         :return: 是否推送成功
#         """
#         try:
#             # 构造消息内容
#             message_data = {
#                 "msgtype": "markdown",
#                 "markdown": {
#                     "content": f"## {report_title}\n"
#                 }
#             }
#
#             # 添加报告链接
#             if report_url:
#                 message_data["markdown"]["content"] += f"[查看详细报告]({report_url})\n"
#
#             # 添加摘要信息
#             if summary:
#                 message_data["markdown"]["content"] += f"\n**测试摘要:**\n{summary}\n"
#
#             # 发送消息
#             response = requests.post(self.webhook_url, json=message_data)
#
#             if response.status_code == 200:
#                 result = response.json()
#                 if result.get("errcode") == 0:
#                     auto_logger.info("报告推送企业微信成功")
#                     return True
#                 else:
#                     auto_logger.error(f"报告推送企业微信失败: {result}")
#                     return False
#             else:
#                 auto_logger.error(f"报告推送企业微信请求失败，状态码: {response.status_code}")
#                 return False
#
#         except Exception as e:
#             auto_logger.error(f"推送报告到企业微信异常: {e}")
#             return False
#
#     def send_test_result_to_wechat(self, report_title="接口自动化测试报告",
#                                    passed_count=0, failed_count=0, error_count=0,
#                                    duration=0, report_url=None):
#         """
#         发送测试结果统计到企业微信
#         :param report_title: 报告标题
#         :param passed_count: 通过用例数
#         :param failed_count: 失败用例数
#         :param error_count: 错误用例数
#         :param duration: 执行时长(秒)
#         :param report_url: 报告访问地址
#         :return: 是否推送成功
#         """
#         try:
#             total_count = passed_count + failed_count + error_count
#             pass_rate = (passed_count / total_count * 100) if total_count > 0 else 0
#
#             # 构造消息内容
#             content = f"## {report_title}\n"
#             content += f"**测试结果统计:**\n"
#             content += f"- 总用例数: {total_count}\n"
#             content += f"- 通过: {passed_count}\n"
#             content += f"- 失败: {failed_count}\n"
#             content += f"- 错误: {error_count}\n"
#             content += f"- 通过率: {pass_rate:.2f}%\n"
#             content += f"- 执行时长: {duration:.2f}秒\n"
#
#             # 添加报告链接
#             if report_url:
#                 content += f"\n[查看详细报告]({report_url})\n"
#
#             message_data = {
#                 "msgtype": "markdown",
#                 "markdown": {
#                     "content": content
#                 }
#             }
#
#             # 发送消息
#             response = requests.post(self.webhook_url, json=message_data)
#
#             if response.status_code == 200:
#                 result = response.json()
#                 if result.get("errcode") == 0:
#                     auto_logger.info("测试结果推送企业微信成功")
#                     return True
#                 else:
#                     auto_logger.error(f"测试结果推送企业微信失败: {result}")
#                     return False
#             else:
#                 auto_logger.error(f"测试结果推送企业微信请求失败，状态码: {response.status_code}")
#                 return False
#
#         except Exception as e:
#             auto_logger.error(f"推送测试结果到企业微信异常: {e}")
#             return False
#
#
# # 创建全局实例
# wechat_webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=2cbcecaf-53aa-4367-aba5-1aac2005222d"
# allure_report_util = AllureReportUtil(wechat_webhook_url)

# !/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Allure报告推送企业微信工具类
"""

import requests
import json
import os
import sys
import subprocess

# 添加项目根目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.logger_util import auto_logger


class AllureReportUtil:
    """Allure报告推送工具类"""

    def __init__(self, webhook_url):
        """
        初始化
        :param webhook_url: 企业微信机器人webhook地址
        """
        self.webhook_url = webhook_url

    def generate_allure_report(self, results_dir="./reports/allure_results", report_dir="./reports/allure-reports"):
        """
        生成allure报告
        :param results_dir: allure结果目录
        :param report_dir: allure报告目录
        :return: 是否生成成功
        """
        try:
            # 检查结果目录是否存在
            if not os.path.exists(results_dir):
                auto_logger.error(f"Allure结果目录不存在: {results_dir}")
                return False

            # 创建报告目录
            if not os.path.exists(report_dir):
                os.makedirs(report_dir)

            # 生成报告命令
            cmd = f"allure generate {results_dir} -o {report_dir} --clean"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

            if result.returncode == 0:
                auto_logger.info("Allure报告生成成功")
                return True
            else:
                auto_logger.error(f"Allure报告生成失败: {result.stderr}")
                return False
        except Exception as e:
            auto_logger.error(f"生成Allure报告异常: {e}")
            return False

    def send_report_to_wechat(self, report_title="接口自动化测试报告", report_url=None,
                              summary=None, report_dir="./reports/allure-reports"):
        """
        推送报告到企业微信
        :param report_title: 报告标题
        :param report_url: 报告访问地址
        :param summary: 报告摘要信息
        :param report_dir: 报告目录
        :return: 是否推送成功
        """
        try:
            # 无可用 webhook 时直接跳过
            if not self.webhook_url:
                auto_logger.info("未配置 WECHAT_WEBHOOK_URL，跳过报告推送")
                return False

            # 构造消息内容
            message_data = {
                "msgtype": "markdown",
                "markdown": {
                    "content": f"## {report_title}\n"
                }
            }

            # 添加报告链接
            if report_url:
                message_data["markdown"]["content"] += f"[查看详细报告]({report_url})\n"

            # 添加摘要信息
            if summary:
                message_data["markdown"]["content"] += f"\n**测试摘要:**\n{summary}\n"

            # 发送消息
            response = requests.post(self.webhook_url, json=message_data)

            if response.status_code == 200:
                result = response.json()
                if result.get("errcode") == 0:
                    auto_logger.info("报告推送企业微信成功")
                    return True
                else:
                    auto_logger.error(f"报告推送企业微信失败: {result}")
                    return False
            else:
                auto_logger.error(f"报告推送企业微信请求失败，状态码: {response.status_code}")
                return False

        except Exception as e:
            auto_logger.error(f"推送报告到企业微信异常: {e}")
            return False

    def send_test_result_to_wechat(self, report_title="接口自动化测试报告",
                                   passed_count=0, failed_count=0, error_count=0,
                                   duration=0, report_url=None):
        """
        发送测试结果统计到企业微信
        :param report_title: 报告标题
        :param passed_count: 通过用例数
        :param failed_count: 失败用例数
        :param error_count: 错误用例数
        :param duration: 执行时长(秒)
        :param report_url: 报告访问地址
        :return: 是否推送成功
        """
        try:
            # 无可用 webhook 时直接跳过
            if not self.webhook_url:
                auto_logger.info("未配置 WECHAT_WEBHOOK_URL，跳过测试结果推送")
                return False

            total_count = passed_count + failed_count + error_count
            pass_rate = (passed_count / total_count * 100) if total_count > 0 else 0

            # 构造消息内容
            content = f"## {report_title}\n"
            content += f"**测试结果统计:**\n"
            content += f"- 总用例数: {total_count}\n"
            content += f"- 通过: {passed_count}\n"
            content += f"- 失败: {failed_count}\n"
            content += f"- 错误: {error_count}\n"
            content += f"- 通过率: {pass_rate:.2f}%\n"
            content += f"- 执行时长: {duration:.2f}秒\n"

            # 添加报告链接
            if report_url:
                content += f"\n[查看详细报告]({report_url})\n"

            message_data = {
                "msgtype": "markdown",
                "markdown": {
                    "content": content
                }
            }

            # 发送消息
            response = requests.post(self.webhook_url, json=message_data)

            if response.status_code == 200:
                result = response.json()
                if result.get("errcode") == 0:
                    auto_logger.info("测试结果推送企业微信成功")
                    return True
                else:
                    auto_logger.error(f"测试结果推送企业微信失败: {result}")
                    return False
            else:
                auto_logger.error(f"测试结果推送企业微信请求失败，状态码: {response.status_code}")
                return False

        except Exception as e:
            auto_logger.error(f"推送测试结果到企业微信异常: {e}")
            return False


# 创建全局实例（从环境变量读取，缺省则不推送）
wechat_webhook_url = os.environ.get("WECHAT_WEBHOOK_URL")
allure_report_util = AllureReportUtil(wechat_webhook_url)