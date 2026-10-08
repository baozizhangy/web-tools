# #!/usr/bin/env python
# # -*- coding: UTF-8 -*-
# import inspect
#
# import requests
#
#
# class FundBaseRequest:
#     def __init__(self, fund_code=None, fund_name=None):
#         self.fund_code = fund_code
#         self.fund_name = fund_name
#         # self.fund_methods_enum = fund_methods_enum
#
#
#     @classmethod
#     def marked_method(cls, func):
#         func.is_marked = True
#         return func
#
#     @classmethod
#     def get_marked_methods(cls):
#         methods = []
#         for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
#             if getattr(method, 'is_marked', False):
#                 doc = inspect.getdoc(method)
#                 methods.append((name, doc))
#         return methods
#
#     def fund_res_model(self, method_name, method_url, method_data):
#         """
#         :param method_data:
#         :param method_name: 方法名
#         :param method_url: 方法路径
#         :return:
#         """
#
#         url = r"https://test3.xurongwl.com/cbg/goa/api/p/" + method_url
#         return {
#             "fundCode": self.fund_code,
#             "fundName": self.fund_name,
#             "method_url": url,
#             "method_name": method_name,
#             "method_data": method_data
#         }
#
