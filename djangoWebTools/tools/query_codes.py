# -*- coding: utf-8 -*-
# @Time    : 2023/6/29 15:34
# @Author  : zhangzhengchuan
import json
from urllib.parse import urljoin

import requests
# from config import widek_token,widek_host,widek_port
from utils.logger_util import web_logger
#本地配置
headers = {
    "Accept":"application/json, text/plain, */*",
    "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
    "Connection":"keep-alive",
    "Content-Type":"application/json;charset=UTF-8",
    # "Origin":"http://widek-sit.xurongwl.com",
    # "Referer":"http://widek-sit.xurongwl.com/strategy-manager/risk-manager/RuleTest",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
}
# # sit配置
# headers = {
#     "Accept":"application/json, text/plain, */*",
#     "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
#     "Connection":"keep-alive",
#     "Content-Type":"application/json;charset=UTF-8",
#     "Origin":"http://widek-svc-svc.sit:8090",
#     "Referer":"http://widek-svc-svc.sit:8090/strategy-manager/risk-manager/RuleTest",
#     "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
# }

'''
1、返回手机号加密内容
2、查询数据库里的验证码
'''


# def check_phone_registration_mobile(mobile,admin_token):
#     print(widek_host)
#     widek_host1 = widek_host
#     widek_port1 = widek_port
#     # path = '/widek-api/manage/gdpr/api/identification'
#     path = 'manage/gdpr/api/identification'
#     # 使用 urljoin 进行拼接
#     url = urljoin(f'http://{widek_host1}:{widek_port1}/',path)
#     # url = f'http://{widek_host}/widek-api/manage/gdpr/api/identification'
#     # url = 'http://widek-svc-svc.sit:8090/manage/gdpr/api/identification'
#     cookies = {"Admin-Token":admin_token}
#     data = {
#         "identifyType":"DEIDENTIFIED",
#         "identifyTargetType":"MOBILE",
#         "identifyContent":mobile
#     }
#     data_json = json.dumps(data,separators=(',',':'))
#
#     try:
#         response = requests.post(url,headers=headers,cookies=cookies,data=data_json)
#         response.raise_for_status()
#         result = response.json()
#
#         web_logger.info(f"查询加密后手机号结果:{result['data']['targetContent'][0]}")
#         if result.get("code") != 200:
#             return {
#                 "code":"998",
#                 "msg":"接口返回失败，token失效，获取对应环境widek登录状态下的admin-token传递",
#                 "error":result
#             }
#         return result["data"]["targetContent"][0]
#     except requests.exceptions.RequestException as e:
#         return {
#             "code":"999",
#             "msg":"接口调用失败，错误信息",
#             "error":str(e)
#         }
#

# def query_login_code(env, mobile, event_code=None, input_widek_token=None):
#
#     try:
#         mobile = int(mobile)
#     except ValueError:
#         return {
#             "code": 1,
#             "message": "参数类型必须为整数类型",
#             "data": None
#         }
#     web_logger.info(f"query_login_code 获取token值:{widek_token}")
#
#     admin_token = input_widek_token if input_widek_token else widek_token
#
#     web_logger.info(f"admin_token:{admin_token}")
#
#     if event_code and event_code in ['event_login_verify_code', 'event_register_verify_code']:
#         target_content = check_phone_registration_mobile(mobile, admin_token)
#         code_record_sql = (
#             f"SELECT send_time, content "
#             f"FROM cns.p_sms_record "
#             f"WHERE cns.p_sms_record.mobile = '{target_content}' "
#             f"AND cns.p_sms_record.event_code = '{event_code}' "
#             f"ORDER BY date_created DESC "
#         )
#     # else:
#     #     mobile_aes = check_phone_registration_aes(mobile, admin_token)
#     #     code_record_sql = (
#     #         f"SELECT date_created, code "
#     #         f"FROM bcs.t_sms_code_record "
#     #         f"WHERE bcs.t_sms_code_record.phone = '{mobile_aes}' "
#     #         f"ORDER BY date_created DESC"
#     #
#     #     )
#     # if event_code:
#     #     code_record_sql += " LIMIT 1"
#
#     # try:
#     #     # print(code_record_sql,"----1")
#     #     result_codes = db_conn(env).get_all(code_record_sql)
#     #     print(result_codes,"-----2")
#     # except Exception as e:
#     #     return {
#     #         "code": 1,
#     #         "message": f"数据库查询错误: {str(e)}",
#     #         "data": None
#     #     }
#     #
#     # if not result_codes:
#     #     return {
#     #         "code": 1,
#     #         "message": "没有获取到发送记录，请重新获取验证码",
#     #         "data": None
#     #     }
#     # else:
#     #     formatted_results = []
#     #     for record in result_codes:
#     #         if 'send_time' in record:
#     #             formatted_send_time = record['send_time'].strftime('%Y-%m-%d %H:%M:%S')
#     #             formatted_content = record['content']
#     #             formatted_results.append({
#     #                 'send_time': formatted_send_time,
#     #                 'code_content': formatted_content
#     #             })
#     #         else:
#     #             formatted_send_time = record['date_created'].strftime('%Y-%m-%d %H:%M:%S')
#     #             formatted_content = record['code']
#     #             formatted_results.append({
#     #                 'send_time': formatted_send_time,
#     #                 'code_content': formatted_content
#     #             })
#     #
#     #     return {
#     #         "code": 0,
#     #         "message": "获取短信记录成功",
#     #         "data": formatted_results
#     #     }

# if __name__ == "__main__":
#     # phone_numbers = random_get_phone(10, 'sit')
#     admin_token1 = "eyJhbGciOiJSUzI1NiJ9.eyJ1c2VyTmFtZSI6InppeXVhbiIsImV4cCI6MTczMzc0ODUwNywibG9naW5fdXNlcl9rZXkiOiJlODMxNDU5MC00ZjQ0LTRkMWItODNkNy1iMzBhMTg2ZTU3YTYifQ.tOb6qzbJyTqfHsHdRjStdWzeEW6EAc7Zz0HYfDLGxkUxWXh4uc2ZNvH9DlrcFFTpBMp6HzOh_QwZmi4OTHaKwJYOdxTbZZfF3c9crgJ9awp92AscmprqTja-YHc5R-nqLOwcmrrW2VKZCWN_S_x_tCpLYidN2CaP_YiX07cYKtO8H4syf0m26zvJSJbyXhSTiWEEpjNhJgsepDEK4pwYwKWd1rs4dPULlYdI5_Srzq55ooLMh5renW22zvx8LqoI8YbIc1NcQZ8ryPELktpMAzfuGiS6S2FHdrZtHOdBGFSqyn5RKHFZ_EpHPFacV9nXdN5vcRpwkLhKeXzgdg0GCw"
#     # mobile_md2 = check_phone_registration_mobile("18621038621",admin_token=admin_token1)
#     # md5_number =  md5_encrypt("15860784555")
#     # print(md5_number)
#
#     result_code = query_login_code("sit","19831616434",event_code='event_login_verify_code',
#                                    input_widek_token=admin_token1)
#
#     print(result_code)
