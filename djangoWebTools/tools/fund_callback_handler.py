#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import functools

import requests

# from api.fund.tongcheng_callback import Tongcheng
from utils.logger_util import web_logger
#
# fund_mapping = {
#     "tongcheng": Tongcheng,
# }


# class FundCallbackHandler(object):
#     def __init__(self, **kwargs):
#         self.kwargs = kwargs
#
#     @staticmethod
#     def get_fund_list():
#         fund_list = []
#         for fund_code, fund_class in fund_mapping.items():
#             fund_instance = fund_class()
#             fund_list.append({
#                 "fund_code": fund_code,
#                 "fund_name": fund_instance.fund_name
#             })
#         return fund_list
#
#     @classmethod
#     def submit_fund_request(cls, fund, method, **kwargs):
#         if fund in fund_mapping:
#             fund_class = fund_mapping[fund]
#             fund_instance = fund_class()
#             if hasattr(fund_class, method):
#                 # 调用渠道方法
#                 fund_method = getattr(fund_instance, method)
#                 partial_method = functools.partial(fund_method, **kwargs)
#                 res = partial_method()
#                 web_logger.info(f"提交机构回调请求返回::{res}")
#                 return res
#             else:
#                 web_logger.info(f"机构类{fund_class.__name__}不包含方法{method}")
#                 return f"机构类{fund_class.__name__}不包含方法{method}，暂未实现或异常"
#         else:
#             web_logger.info("submit_channel_request异常")
#             return "未知机构"

    # @staticmethod
    # def post_data(url, data):
    #     response = requests.post(url, json=data)
    #     return response.json()

    #
    # def fund_structure_data(self):
    #     cascade_options = []
    #     fund_list = self.get_fund_list()
    #
    #     for fund in fund_list:
    #         fund_code = fund.get('fund_code')
    #         fund_name = fund.get('fund_name')
    #
    #         children = []
    #         method_list = self.submit_fund_request(fund_code, "get_marked_methods")
    #         for method_code, method_name in method_list:
    #             children.append({
    #                 'value': method_code,
    #                 'label': method_name
    #             })
    #
    #         cascade_options.append({
    #             'value': fund_code,
    #             'label': fund_name,
    #             'children': children
    #         })
    #
    #     return cascade_options


# if __name__ == '__main__':
    # print("机构列表",FundCallbackHandler.get_fund_list())
    # methods = FundCallbackHandler.submit_fund_request("tongcheng", "get_marked_methods")
    # print("方法列表", methods)

    # print(FundCallbackHandler().fund_structure_data())

    # res = FundCallbackHandler.submit_fund_request(
    #     "tongcheng", "credit_callback_data", user_no="你方user_no", channel_apply_no="你方applyNo",)
    # print(res)
    # post_res = FundCallbackHandler.post_data(res.get("method_url"), res.get("method_data"))
    # print(post_res)