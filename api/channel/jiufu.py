#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from api.channel._base_requests import BaseRequest
from api.channel.channel_api_config import ChannelMethodsEnum
from utils.cryption_util import md5_encrypt
from utils.personal_util import get_person_name, get_mobile_no, get_id_no


class JiuFu(BaseRequest):
    # 玖富  已下线，不维护
    def __init__(self, ):
        super().__init__("HUB_JIUFU")

    @staticmethod
    def get_check_data(data):
        # 返回准入信息模板
        mobile = data.get("mobile")
        input_id_no = data.get("inputIdNo")
        name = data.get("name")
        # 返回准入信息模板
        user_name = name if name else get_person_name()
        mobile_no = mobile if mobile else get_mobile_no()
        id_no = input_id_no if input_id_no else get_id_no()
        return {
            "md5_phone":       md5_encrypt(mobile_no),
            "md5_phone_id_no": md5_encrypt(mobile_no + id_no),
            "md5_id_no":       md5_encrypt(id_no),
            "pre_id_no":       id_no[:6],
            "name":            user_name
        }

    # def check(self, data):
    #     """
    #     调用准入
    #     :param data = {
    #         "userName":        "",
    #         "md5Phone":        "",
    #         "md5IdNo":         "",
    #         "md5PhoneAndIdNo": "",
    #         "partnerId":       "",
    #         "openId":          "",
    #     }
    #     :return:
    #     """
    #     method = "check"  # 准入
    #     res = self._request(method, data).json()
    #     return res
