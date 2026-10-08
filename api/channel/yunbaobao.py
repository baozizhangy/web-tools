#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from api.channel._base_requests import BaseRequest
from api.channel.channel_api_config import ChannelMethodsEnum
from utils.cryption_util import md5_encrypt
from utils.personal_util import get_person_name, get_id_no, get_mobile_no


class YunBaoBao(BaseRequest):
    # 云宝宝  暂不开发
    def __init__(self, ):
        super().__init__("HUB_YUNBAOBAO")

    @staticmethod
    def get_check_data(data):
        # 返回准入信息模板
        mobile = data.get("channelMobile")
        input_id_no = data.get("channelIdNo")
        input_check_no = data.get("channelCheckNo")
        name = data.get("channelCustName")
        channel_user_no = data.get("channelUserNo")
        channel_credit_no = data.get("channelCreditNo")
        # 返回准入信息模板
        user_name = name if name else get_person_name()
        mobile_no = mobile if mobile else get_mobile_no()
        id_no = input_id_no if input_id_no else get_id_no()
        return {
            "name":        user_name,
            "md5_phone":        md5_encrypt(mobile_no),
            "md5_id_no":         md5_encrypt(id_no),
            "md5_phone_id_no": md5_encrypt(mobile_no + id_no),
        }

