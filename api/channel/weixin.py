#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from enum import Enum

from api.channel._base_requests import BaseRequest
from utils.cryption_util import md5_encrypt
from utils.personal_util import get_mobile_no, get_person_name


class WeiXinMethodsEnum(Enum):
    # 维信渠道方法枚举
    CHECK = ("check", "准入", "get_check_data")
    CREDIT_APPLY = ("submit", "授信申请", "get_credit_data")
    CREDIT_QUERY = ("conclusion", "授信结果查询", "get_conclusion_data")
    ACCOUNT_QUERY = ("conclusion_detail", "额度查询", "get_account_query_data")
    GET_URL = ("scene_url", "获取下载URL", "get_scene_url_data")
    CONTRACT = ("contract", "获取合同", "get_contract_data")


class WeiXin(BaseRequest):
    # 维信
    def __init__(self, ):
        super().__init__(channel_id="HUB_WEIXIN", channel_name="维信",
                         channel_method_enum=WeiXinMethodsEnum, channel_uid="22357", py_code="weixin")

    def get_check_data(self, data):
        # 准入
        mobile = data.get("channelMobile")
        id_no = data.get("channelIdNo")
        check_data = {
            "phoneNoMd5": md5_encrypt(mobile),
            "cardNoMd5": md5_encrypt(id_no),
            "phoneNoCardNoMd5": md5_encrypt(mobile + id_no)
        }
        return self.data_model(WeiXinMethodsEnum.CHECK.value[0], check_data)

    def get_credit_data(self, data):
        # 授信申请
        mobile = data.get("channelMobile")
        id_no = data.get("channelIdNo")
        check_no = data.get("channelCheckNo")
        name = data.get("channelCustName")
        channel_user_no = data.get("channelUserNo")
        channel_credit_no = data.get("channelCreditNo")
        bank_card = data.get("channelBankCardNo")

        credit_data = {
            "registerId": channel_user_no,
            "transactionId": channel_credit_no,
            "personalBasicInfo": {
                "birthDay": "1995-08-04",
                "idType": "CETP000001",
                "address": "广东省东莞市寮步镇向西村创业新街044号",
                "education": "EDBK000003",
                "gender": "女",
                "nation": "汉",
                "idCardNo": id_no,
                "idValidStart": "20180803",
                "idValidEnd": "20280803",
                "customerName": name,
                "phoneNo": mobile,
                "marriage": "MAST000003",
                "signOrg": "东莞市公安局"
            },
            "bankCardInfo": {
                "bindPhoneNo": mobile,
                "bankCardNo": bank_card,
                "bankName": "建设银行"
            },
            "contactsInfo": [
                {
                    "contactRelation": "RELA000008",
                    "contactName": get_person_name(),
                    "contactPhoneNo": get_mobile_no()
                },
                {
                    "contactRelation": "RELA000006",
                    "contactName": get_person_name(),
                    "contactPhoneNo": get_mobile_no()
                }
            ],
            "personalJobInfo": {
                "occupation": "OCCU000001",
                "corporationName": "一般普通公司",
                "industry": "INDU000002"
            },
            "extensions": {
                "liveCityName": "北京市",
                "liveAddress": "北京市北京市东城区",
                "liveAreaName": "东城区",
                "liveProvinceName": "北京市",
                "faceRecognitionScores": "80.8165",
                "workProvinceName": "广东省",
                "osType": "android",
                "workAreaName": "寮步镇",
                "workAddress": "广东省东莞市寮步镇向西村创业新街044号",
                "workCityName": "东莞市"
            },
            "idCardImageInfo": {
                "idBackImage": "http://211.95.59.229:6443/http-feeder/common/lxjhapi/file/IMTP000002/1826929786337857536/a3beb5e5f7fc45f4a417ab47d6bd8b44",
                "livingBodyImage": "http://211.95.59.229:6443/http-feeder/common/lxjhapi/file/IMTP000037/1826929786337857536/a3beb5e5f7fc45f4a417ab47d6bd8b44",
                "idFrontImage": "http://211.95.59.229:6443/http-feeder/common/lxjhapi/file/IMTP000001/1826929786337857536/a3beb5e5f7fc45f4a417ab47d6bd8b44"
            },
            "loanInfo": {
                "purposeArea": "LUCS000015"
            }
        }
        return self.data_model(WeiXinMethodsEnum.CREDIT_APPLY.value[0], credit_data)

    def get_conclusion_data(self, data):
        # 授信结果查询
        channel_user_no = data.get("channelUserNo")
        channel_credit_no = data.get("channelCreditNo")
        hub_order_no = data.get("hubOrderNo")
        conclusion_data = {
            "applyNo": hub_order_no,
            "transactionId": channel_credit_no
        }
        return self.data_model(WeiXinMethodsEnum.CREDIT_QUERY.value[0], conclusion_data)

    def get_account_query_data(self, data):
        channel_user_no = data.get("channelUserNo")
        channel_credit_no = data.get("channelCreditNo")
        hub_order_no = data.get("hubOrderNo")
        account_query_data = {
            "registerId": channel_user_no,
            "transactionId": channel_credit_no,
            "applyNo": hub_order_no
        }
        return self.data_model(WeiXinMethodsEnum.ACCOUNT_QUERY.value[0], account_query_data)

    def get_scene_url_data(self, data):
        # 获取下载URL
        hub_order_no = data.get("hubOrderNo")
        url_data = {
            "callbackUrl": "http://www.baidu.com",
            "applyNo": hub_order_no,
            "scene":"WITHDRAW"
        }
        return self.data_model(WeiXinMethodsEnum.GET_URL.value[0], url_data)

    def get_contract_data(self, data):
        contract_data = {
            "currentNode": 1
        }
        return self.data_model(WeiXinMethodsEnum.CONTRACT.value[0], contract_data)