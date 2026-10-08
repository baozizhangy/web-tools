# #!/usr/bin/env python
# # -*- coding: UTF-8 -*-
# import requests
#
# from config import get_urls
# from djangoWebTools.tools.collect_info import get_contact_list
# from utils.logger_util import web_logger
# import secrets
# import string
#
#
# def generate_random_string(length=16):
#     # 定义用于生成随机字符串的字符集
#     characters = string.ascii_letters + string.digits
#
#     # 使用secrets模块生成指定长度的随机字符串
#     random_string = ''.join(secrets.choice(characters) for _ in range(length))
#
#     return random_string
#
#
# def get_791_meta():
#     meta_module = {
#         'device_version': '8.1.0',
#         # 'duid':              generate_random_string(24),
#         'duid': "XLlvoYr3dTsDACs5fR3vLHME",
#         'os': 'android',
#         'device_model': 'vivo X20A',
#         'channel': 'jenkins_channel',
#         'sign': 'com.lightpalm.fenqia:jenkins_channel:215a756f259c9aea98c9ea386b9ecccf',
#         'with_sim': '0',
#         'branch': 'com.lightpalm.fenqia',
#         'version': '7.9.1',
#         'device_brand': 'vivo',
#         'device_resolution': '1080x2034',
#         'root': '0',
#         'android_id': '36d9bbaf1258427d',
#         'token_uid': '981095d9-fb87-44df-a374-3bfa98b28fec',
#     }
#     return meta_module
#
#
# def get_793_meta():
#     meta_module = {
#         'device_version': '12',
#         'duid': "Y3ygAZS80CsDABanwd21GeV8",
#         'os': 'android',
#         'device_model': 'PEQM00',
#         'channel': 'jenkins_channel',
#         'sign': 'com.lightpalm.fenqia:Ajenkins_channel:A16d087d44a9a797d6ad3b17ffc7c0924',
#         'with_sim': '0',
#         'branch': 'com.lightpalm.fenqia',
#         'version': '7.9.3',
#         'device_brand': 'OPPO',
#         'device_resolution': '1080x2237',
#         'root': '0',
#         'android_id': '79d1e171d3df4b24',
#         'token_uid': '06b63fbb-be70-4c4b-a96b-d622c9b25dbd',
#     }
#     meta_data = 'device_version=12&duid=Y3ygAZS80CsDABanwd21GeV8&os=android&device_model=PEQM00&channel=jenkins_channel&sign=com.lightpalm.fenqia%3Ajenkins_channel%3A16d087d44a9a797d6ad3b17ffc7c0924&with_sim=0&branch=com.lightpalm.fenqia&version=7.9.3&device_brand=OPPO&device_resolution=1080x2237&root=0&android_id=79d1e171d3df4b24&token_uid=06b63fbb-be70-4c4b-a96b-d622c9b25dbd'
#     return meta_data
#
#
# def get_by_app_meta():
#     """贝赢APP init接口meta参数"""
#     meta = {
#         "device_version=8.1.0",
#         "duid=XLlvoYr3dTsDACs5fR3vLHME",
#         "os=android",
#         "device_model=vivo%20X20A",
#         "channel=40000",
#         "sign=com.hrbytxd.byfq%3A40000%3A6d9f3980484f0dc635a91ddd46501622",
#         "with_sim=0",
#         "branch=com.hrbytxd.byfq",
#         "version=1.0.1",
#         "device_brand=vivo",
#         "device_resolution=1080x2034",
#         "root=0",
#         "android_id=d16254b7770859ac",
#         "oaid=cc4cd80f294dc9f32e099bf17c2a94d8e9e136889f3e4a695f803497be043283",
#         "token_uid=63d61ba3-b1dc-458d-bb91-c0f3299f04e3"
#     }
#     meta = 'device_version=8.1.0&duid=XLlvoYr3dTsDACs5fR3vLHME&os=android&device_model=vivo%20X20A&channel=40000&sign=com.hrbytxd.byfq%3A40000%3A6d9f3980484f0dc635a91ddd46501622&with_sim=0&branch=com.hrbytxd.byfq&version=1.0.1&device_brand=vivo&device_resolution=1080x2034&root=0&android_id=d16254b7770859ac&oaid=cc4cd80f294dc9f32e099bf17c2a94d8e9e136889f3e4a695f803497be043283&token_uid=63d61ba3-b1dc-458d-bb91-c0f3299f04e3'
#     return meta
#
#
# class UserApi:
#     """
#     User用户类，用于实现登录和其他用户相关功能。
#     """
#
#     def __init__(self, env, mobile, app="LXJ_APP"):
#         self.name = None
#         self.id_no = None
#         self.credit = None
#         self.mobile = mobile
#         self.app = app
#         web_logger.info(f"UserApi::init::{env}")
#         self.api_root_url = get_urls(env).get("ROOT_URL")
#         web_logger.info(f"UserApi::root::{self.api_root_url}")
#         self.session = requests.Session()
#         # self.vision = "8.9.1"
#         # self.client = RestClient(self.api_root_url)
#         self._init()
#
#     def _init(self, meta=None):
#         # 初始化C-Token
#         meta_data = get_791_meta()
#         if self.app == "LXJ_APP":
#             pass
#         elif self.app == "BY_APP":
#             meta_data = get_by_app_meta()
#         elif self.app == "Loan_app":
#             meta_data = get_791_meta()
#             self.session.headers[
#                 "Cookie"] = "ctoken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ2aXNpdHMiOjIsImR1aWQiOiJYTGx2b1lyM2RUc0RBQ3M1ZlIzdkxITUUiLCJkaWQiOjgsImFwcGlkIjo4LCJicmFuY2giOiJjb20ubGlnaHRwYWxtLmZlbnFpYSIsInZlcnNpb24iOiI3LjkuMSIsImNoYW5uZWwiOiJqZW5raW5zX2NoYW5uZWwiLCJwaWQiOiJmZW5xaSIsInBkIjoiZmVucWkiLCJncm91cCI6ImRlZmF1bHQiLCJ0YWdzIjpbXSwibGFzdCI6NjI4LCJpbml0IjoxNzM5NDk3MjU4LCJvcyI6Im90aGVyIiwicXVlcnlfb3MiOiJvdGhlciIsImFwcF9vcyI6Im90aGVyIiwiYXBwX3ZlcnNpb24iOiI3LjkuMSIsInF1ZXJ5X3ZlcnNpb24iOiI2LjcuNSIsInhyX3NpZCI6IlNXcFpNMWxYVlRWYWFrcHBXVzFhYUUweVRteFplbEV3VGtSVmVFMXFWVEpQUTBrNk1YUnBhMmhRT21WcWRIWkJaRGxuVEdZMmNXMVFaekJSTkZOS2NFRXRXRjl6Y3ciLCJwcmV2aWV3X3NpZCI6IjY3YWU5ZjJiYmZhM2NlYzQ0NDUxMjU2OCJ9.LREI2UfsE9OdzaMmaJmBJxE0-5nYUPPtCiKeGBzf-0U"
#         if meta is not None:
#             meta_data = meta
#         content_type = "application/x-www-form-urlencoded"
#         init_response = self._post("/init/init", data=meta_data, content_type=content_type)
#         print(f"UserApi::init::init_response:{init_response}, request_data:{meta_data},header:{init_response.headers}")
#         self.home_page_url = init_response.json().get('tabbar')[0].get('url')
#         c_token = init_response.cookies.get_dict().get("ctoken")
#         print(f"UserApi::init::ctoken:{c_token}")
#         self.session.headers["C-Token"] = c_token
#
#     def _post(self, path, json=None, data=None, content_type=None, ):
#         print(f"UserApi::root::{self.api_root_url}, path::{path}, json::{json}")
#         return self.session.post(self.api_root_url + path, json=json, data=data, headers={"Content-Type": content_type},
#                                  verify=False)
#
#     def login_pwd(self, mobile: str, password: str):
#         # 使用密码登录
#         login_data = {
#             'number': mobile,
#             'password': password,
#         }
#         return self._post("/users/loginpwd", json=login_data)
#
#     def send_code(self, number, code_type="login"):
#         # 发送验证码case参数为：login：登陆、update_pwd：更新密码、update_info：注销
#         json_data = {
#             "case": code_type,
#             "number": number
#         }
#         return self._post("/code/code", json=json_data)
#
#     def get_code(self, number):
#         # 直接从业务服务端获取测试账号验证码
#         json_data = {"number": number}
#         return self._post("/code/get_sms_code", json=json_data)
#
#     def login_code(self, mobile, code):
#         # 使用验证码登录
#         json_data = {
#             "code": code,
#             "number": mobile
#         }
#         res = self._post("/users/logincode", json=json_data)
#         # print(f"res::{res}")
#         return res
#
#     def clear_tds_cache(self):
#         # 清除tds缓存
#         res = self.session.post("/clg/tds-service/api/cache/clear")
#         # print(f"res::{res}")
#         return res
#
#     def collect_device(self, device_no):
#         # 收集设备信息
#         json_data = {
#             "data": {
#                 "scene": "home",
#                 "data": {
#                     "storage": 31549,
#                     "sim_list": [
#                         {
#                             "allowsVOIP": 1,
#                             "isoCountryCode": "cn",
#                             "mobileCountryCode": 460,
#                             "mobileNetworkCode": 0,
#                             "carrierName": "cmcc"
#                         }
#                     ],
#                     "branch": "com.lightpalm.fenqia",
#                     "duid": device_no,
#                     "device_resolution": "1080x1920",
#                     "is_use_wifi": 1,
#                     "imei": "862170158616712",
#                     "version": "7.9.5",
#                     "channel": "20001",
#                     "imsi": "460008037747331",
#                     "android_id": "1b8c82ef70722c1b",
#                     "tele_num": "涓浗绉诲姩",
#                     "mac": "00:00:00:00:82:5c",
#                     "with_sim": 1,
#                     "sn": "89860036593735226557",
#                     "memory": 5963,
#                     "debug_state": 0,
#                     "is_vpn": 0,
#                     "unuse_storage": 29952,
#                     "os": "android",
#                     "is_simulator": 1,
#                     "network": 1,
#                     "bettary": 0,
#                     "is_usb_debug": 0,
#                     "is_root": 1,
#                     "device_model": "LENOVO L79031",
#                     "os_version": "7.1.2",
#                     "device_brand": "LENOVO",
#                     "device_ua": "Mozilla/5.0 (Linux; Android 7.1.2; LENOVO L79031 Build/N2G48H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36;webank/h5face;webank/1.0;netType:NETWORK_WIFI;appVersion:141;packageName:com.lightpalm.fenqia"
#                 }
#             }
#         }
#         res = self._post("/clg/lps/api/p/device/collectDevice?version=10.0.5", json=json_data)
#         return res
#
#     def collect_contacts(self, agent_nums=0, cash_nums=20, loan_nums=0, dunning_nums=0, pyramid_nums=0, gamble_nums=0,
#                          drug_nums=0, yellow_nums=0, black_nums=0):
#         # 收集通讯录信息
#         json_data = {
#             "data": {
#                 "scene": "home",
#                 "data": get_contact_list(
#                     agent_nums, cash_nums, loan_nums, dunning_nums, pyramid_nums, gamble_nums, drug_nums,
#                     yellow_nums, black_nums
#                 )
#             }
#         }
#         print(f"collect_contacts::json_data::{json_data}")
#         res = self._post("/clg/lps/api/u/device/collectContacts", json=json_data)
#         return res
#
#
# # #
# if __name__ == '__main__':
#     user = UserApi('SIT', '13112340003', 'Loan_app')
#     print(user.send_code('13112340008'))
