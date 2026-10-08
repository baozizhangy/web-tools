# # -*- coding: utf-8 -*-
# # @Time    : 2023/6/29 15:34
# # @Author  : zhangzhengchuan
# import time
#
# import requests
#
# from config import get_urls,help_submit_api
# from utils.logger_util import web_logger
# import secrets
# import string
#
# class Meta:
#     def __init__(self, os="ios", appVersion="10.0", version="8.9",
#                  branch="com.lightpalm.fenqia", duid="De32123", channel_id="LXJ_APP", product_code="PILOT_APP",
#                  channel="app", cid="20160"):
#         self.os = os
#         self.appVersion = appVersion
#         self.version = version
#         self.branch = branch
#         self.duid = duid
#         self.timestamp = str(int(time.time()))
#         self.channelId = channel_id
#         self.channel = channel
#         self.cid = cid
#         self.product_code = product_code
#
#     def to_dict(self,user_no=None):
#         return {
#             "os":          self.os,
#             "appVersion":  self.appVersion,
#             "version":     self.version,
#             "branch":      self.branch,
#             "duid":        self.duid,
#             "timestamp":   self.timestamp,
#             "channel":     self.channel,
#             "cid":         self.cid,
#             "channelId":   self.channelId,
#             "productCode": "PILOT_APP",
#             "channelId":   self.channel,
#             "productCode": self.product_code,
#             "pd":          self.product_code,
#             "pid":         self.product_code,
#             "clientIp":    "101.226.168.228",
#             "userNo":      user_no
#         }
# class HelpCenter:
#     def __init__(self,api_root_url,session=None,user_no=None):
#         self.api_root_url = api_root_url
#         self.session = session
#         self.meta = Meta().to_dict(user_no)
#
#     def _post_data(self,path,data):
#         """
#         提交数据
#         :param data:
#         :return:
#         """
#         json_data = {
#             "meta":self.meta,
#             "data":data
#         }
#         print(f"_post_data::url::{path}\n::json_data::{json_data}")
#         return self.session.post(self.api_root_url + path,json=json_data,verify=False)
#
#     def help_center_question_submit(self,content,questiontype,productname,imageurl):
#             url = help_submit_api['helpsubmit']
#             web_logger.info(f"url_path:{url}")
#             data={
#                 "category":questiontype,
#                 "content":content,
#                 "imageList":["string"],
#                 "productName":productname
#             }
#             return self._post_data(url,data)
#
#
#
