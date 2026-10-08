#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from api.channel._base_requests import BaseRequest
from api.channel.channel_api_config import ChannelMethodsEnum
from utils.cryption_util import md5_encrypt
from utils.personal_util import get_person_name, get_id_no, get_mobile_no


class JiuFuV2(BaseRequest):
    # 玖富v2  已下线，不维护
    def __init__(self, ):
        super().__init__("HUB_JIUFU_V2")

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
            "hashType":"2",
            "name":            user_name,
            "mobile": mobile_no,
            "certId":         id_no,
            "mobileMd5":       md5_encrypt(mobile_no),
            "certIdMd5":       md5_encrypt(id_no),
            "mobileAndCertIdMd5": md5_encrypt(mobile_no + id_no),
            "certIdAndMobileMd5":   md5_encrypt(id_no + mobile_no),
        }