# #!/usr/bin/env python
# # -*- coding: UTF-8 -*-
# import requests
#
# from config import bind_api
#
#
# class Bind:
#     # def __init__(self, credit):
#     #     self.meta = credit.meta
#     #     self.api_root_url = credit.api_root_url
#     #     self.client = credit.client
#     #     self.product_code = credit.product_code
#
#     def __init__(self, api_root_url, meta, session=None, ):
#         self.api_root_url = api_root_url
#         self.meta = meta
#         self.session = session if session is not None else requests.Session()
#
#     def get_usable_card(self, node_type, flow_no=None, apply_req_no=None, loan_no=None, fund_code=None):
#         # 获取可用卡
#         url = bind_api.get("query")
#         json_data = {
#             "data": {
#                 "nodeType":   node_type,
#                 "flowNo":     flow_no,
#                 "applyReqNo": apply_req_no,
#                 "loanNo":     loan_no,
#                 "fundCode":   fund_code
#             },
#             "meta": self.meta
#         }
#         return self.session.post(self.api_root_url+url, json=json_data)
#
#     def get_usable_card2(self, node_type, flow_no=None, apply_req_no=None, loan_no=None, fund_code=None):
#         # 获取可用卡
#         url = bind_api.get("query")
#         json_data = {
#             "data": {
#                 "nodeType":   node_type,
#                 "flowNo":     flow_no,
#                 "processVersion": 1,
#                 "applyReqNo": apply_req_no,
#                 "loanNo":     loan_no,
#                 "fundCode":   fund_code
#             },
#             "meta": self.meta
#         }
#         return self.session.post(self.api_root_url+url, json=json_data)
#
#     def four_factor_bind(self, card_no, bank_code, bank_name, mobile, bind_flow_no, node_type):
#         """
#         四要素绑卡
#         Args:
#             "data": {
#                 "cardNo": "string",
#                 "bankCode": "string",
#                 "bankName": "string",
#                 "mobileNo": "string",
#                 "nodeType": "string",
#                 "bindFlowNo": "string",
#                 "flowNo": "string"
#                 }
#         Returns:
#         """
#         url = bind_api.get("four")
#         json_data = {
#             "data": {
#                 "cardNo":     card_no,
#                 "bankCode":   bank_code,
#                 "bankName":   bank_name,
#                 "mobileNo":   mobile,
#                 "nodeType":   node_type,
#                 "bindFlowNo": bind_flow_no,
#                 "flowNo":     self.flow_no
#             },
#             "meta": self.meta
#         }
#         return self.session.post(self.api_root_url+url, json=json_data)
#
#     def fund_bind(self, fund_code, card_source, card_no, mobile, bank_code, bank_name, bind_flow_no,
#                   node_type, flow_no=None, apply_req_no=None):
#         """"""
#         url = bind_api.get("fund")
#         json_data = {
#             "data": {
#                 "fundCode":   fund_code,
#                 "cardNo":     card_no,
#                 "bankCode":   bank_code,
#                 "bankName":   bank_name,
#                 "mobileNo":   mobile,
#                 "nodeType":   node_type,
#                 "bindFlowNo": bind_flow_no,
#                 "cardSource": card_source,
#                 "flowNo":     flow_no,
#                 "applyReqNo": apply_req_no
#             },
#             "meta": self.meta}
#         return self.session.post(self.api_root_url+url, json=json_data)
#
#     def verify_code(self, code, bind_flow_no, flow_no=None, apply_req_no=None, loan_no=None):
#         """
#         验证绑卡验证码
#         Args:
#
#         Returns:
#
#         """
#         url = bind_api.get("verify")
#         json_data = {
#             "data": {
#                 "verifyCode": code,
#                 "bindFlowNo": bind_flow_no,
#                 "flowNo":     flow_no,
#                 "applyReqNo": apply_req_no,
#                 "loanNo": loan_no
#             },
#             "meta": self.meta
#         }
#         return self.session.post(self.api_root_url+url, json=json_data)
#
#     def skip_bind(self, flow_no, fund_code):
#         """
#         跳过绑卡
#         Args:
#             flow_no:
#             fund_code:
#
#         Returns:
#
#         """
#         url = bind_api.get("skip")
#         json_data = {
#             "data": {
#                 "fundCode": fund_code,
#                 "flowNo":   flow_no
#             },
#             "meta": self.meta
#         }
#         return self.session.post(self.api_root_url+url, json=json_data)
