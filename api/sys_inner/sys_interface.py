#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import requests

# from api.app.user_api import UserApi


def get_user_check_by_mobile_md5(mobile_md5, user_no):
    # 用手机号md5获取准入落表结果
    url = f"https://test3.xurongwl.com/clg/test/hub/test/channel/table"
    print("get_user_check_by_mobile_md5::", url)
    params = {
        'phoneMD5': mobile_md5,
        'userNo':   user_no,
    }
    response = requests.get(url, params=params,verify=False)
    print("get_user_check_by_mobile_md5::response::", response.json())
    return response.json()


# def get_login_code(env, mobile_no):
#     # 用手机号获取登录验证码
#     user = UserApi(env, mobile_no)
#     # 获取验证码
#     # get_code_res = user.get_code(user.mobile).json()
#     res = user.get_code(user.mobile)
#     if res.status_code != 200:
#         return f"获取登录验证码接口/code/get_sms_code调用失败::{res}"
#     get_code_res = res.json()
#     print(f"get_login_code::{get_code_res}")
#     if get_code_res.get("code", '') != 0:
#         return f"获取登录验证码调用失败::{get_code_res}"
#     if get_code_res.get("data", {}).get("code", "") is not None:
#         return get_code_res.get("data", {}).get("code")
#     else:
#         return "无有效验证码"
#
# if __name__ == '__main__':
#     res = get_login_code("SIT", "14926627865")
#     print(res)
