#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from enum import Enum

from api.channel._base_requests import BaseRequest
from api.channel.channel_api_config import ChannelMethodsEnum
from utils.cryption_util import md5_encrypt
from utils.personal_util import get_person_name, get_id_no, get_mobile_no

# minShengMethodMap.put("user.access", MethodEnum.CHECK.getCode());
# minShengMethodMap.put("user.registe", MethodEnum.REGISTER.getCode());
# minShengMethodMap.put("support.bankcard.list", MethodEnum.BANK_LIST.getCode());
# minShengMethodMap.put("bind.bankcard", MethodEnum.BIND_CARD.getCode());
# minShengMethodMap.put("bind.sms.verify", MethodEnum.BIND_VERIFY.getCode());
# minShengMethodMap.put("user.message.collection", MethodEnum.GET_PROFILE.getCode());
# minShengMethodMap.put("user.message.push", MethodEnum.SEND_DATA.getCode());
# minShengMethodMap.put("credit.apply", MethodEnum.SUBMIT.getCode());
# minShengMethodMap.put("credit.apply.result", MethodEnum.CONCLUSION.getCode());
# minShengMethodMap.put("user.credit.info", MethodEnum.CONCLUSION_DETAIL.getCode());
# minShengMethodMap.put("agreement.query", MethodEnum.CONTRACT.getCode());
# minShengMethodMap.put("third.jump.link", MethodEnum.SCENE_URL.getCode());


class MinShengMethodsEnum(Enum):
    # homo相关渠道方法枚举，
    # ("渠道方法名", "方法中文名", "对应的数据模板方法")
    CHECK = ("user.access", "准入", "get_check_data")
    REGISTER = ("user.registe", "注册", "get_register_data")
    MESSAGE_PUSH = ("user.message.push", "信息上送", "get_message_push_data")
    CREDIT = ("credit.apply", "授信申请", "get_credit_data")
    CREDIT_RESULT = ("credit.apply.result", "授信结果查询", "get_credit_result_data")
    CREDIT_INFO = ("user.credit.info", "授信额度查询", "get_credit_info_data")
    GET_LOAN_URL = ("third.jump.link", "获取借款链接", "get_loan_url_data")
    GET_REPAY_URL = ("third.jump.link", "获取还款链接", "get_repay_url_data")
    # 绑卡 接口未使用
    # BIND_CARD = ("bind.bankcard", "绑卡", "get_bind_card_data")
    # BIND_VERIFY = ("bind.sms.verify", "绑卡验证", "get_bind_verify_data")
    # BANK_LIST = ("support.bankcard.list", "支持的银行卡列表", "get_bank_list_data")
    # 合同
    CREDIT_CONTRACT = ("agreement.query", "授信合同", "get_credit_contract_data")
    BIND_CONTRACT = ("agreement.query", "绑卡合同", "get_bind_contract_data")
    LOAN_CONTRACT = ("agreement.query", "借款合同", "get_loan_contract_data")


class MinSheng(BaseRequest):
    # 民生
    def __init__(self, ):
        super().__init__(channel_id="HUB_MINSHENG", channel_name="民生", channel_method_enum=MinShengMethodsEnum,
                         channel_uid="20820", py_code="minsheng")

    def get_check_data(self, data):
        # 返回准入信息模板
        mobile = data.get("channelMobile")
        input_id_no = data.get("channelIdNo")

        mobile_no = mobile if mobile else get_mobile_no()
        id_no = input_id_no if input_id_no else get_id_no()
        req_data = {
            "mobileNoMd5":  md5_encrypt(mobile_no),
            "idNoMd5":      md5_encrypt(id_no),
            "compositeMd5": md5_encrypt(mobile_no + id_no),
        }
        return self.data_model(MinShengMethodsEnum.CHECK.value[0], req_data)

    def get_register_data(self, data):
        # 返回注册信息模板
        mobile = data.get("channelMobile")
        input_id_no = data.get("channelIdNo")
        name = data.get("channelCustName")
        channel_user_no = data.get("channelUserNo")
        req_data = {
            "mobileNo":     mobile,
            "idNo":         input_id_no,
            "name":         name,
            "userId":       channel_user_no
        }
        return self.data_model(MinShengMethodsEnum.REGISTER.value[0], req_data)


    def get_message_push_data(self, data):
        input_id_no = data.get("channelIdNo")
        name = data.get("channelCustName")
        hub_user_id = data.get("hubUserId")
        base64_data = "iVBORw0KGgoAAAANSUhEUgAAAjkAAAFBCAYAAACVcr5cAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAFiUAABYlAUlSJPAAAAWZSURBVHhe7dYxEQAgEMCwB/+egQEVvWSpha7zDABAzP4FAEgxOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABBMxeXJgZ+f2mLWgAAAABJRU5ErkJggg=="

        req_data = {
            "businessType": "CREDIT",
            "openId":       hub_user_id,
            "message":      {
                "riskInfo": {
                    "FACE_CHECK":  [{
                        "faceCmpScore":   "99",
                        "liveSource":     "1",
                        "type":           "ALIVE_PHOTO",
                        "value":          base64_data,
                        "collectionTime": "2023-11-17 09:00:01"
                    },
                        {
                            "type":  "CARD_FRONT_PHOTO",
                            "value": base64_data
                        },
                        {
                            "type":  "CARD_BACK_PHOTO",
                            "value": base64_data
                        }
                    ],
                    "ID_CARD_OCR": {
                        "APIgender":         "男",
                        "APInationality":    "汉族",
                        "APIissuedBy":       "商城县公安局",
                        "APIidcardNumber":   input_id_no,
                        "APIname":           name,
                        "APIvalidDateEnd":   "2026-07-14",
                        "APIBirthDay":       "1996-11-04",
                        "APIvalidDateStart": "2016-07-14",
                        "APIaddress":        "河南省商城县上石桥镇南竹园村蔡店组"
                    },
                    "DEVICE_INFO": {
                        "deviceType":        "APP",
                        "deviceBrand":       "苹果11",
                        "usingNetMac":       "4G",
                        "mobileNetworkType": "4G",
                        "wifi":              "4G",
                        "networkOperator":   "CMCC",
                        "networkType ":      "WiFi",
                        "idfa":              "dzw7e0fr-37qo-4xek-9qzr-lq92ve1bthul",
                        "latitude":          "31.52157",
                        "ip":                "49.93.228.83",
                        "imsi":              "4G",
                        "isJailBreak":       "N",
                        "totalMemory":       "16GB",
                        "osVersion":         "1.0",
                        "hasRoot":           "N",
                        "sim":               "4G",
                        "idfv":              "ukpk3wpr-ojcb-3mzz-6o76-g3pgu4tjarx6",
                        "model":             "iPhone 11",
                        "isIos":             "Y",
                        "isSimulator":       "0",
                        "longitude":         "120.454895"
                    }
                },
                "userInfo": {
                    "relationInfos":   [{
                        "relName":     "大月亮",
                        "relMobile":   "13921208896",
                        "relRelation": "05"
                    },
                        {
                            "relName":     "大星星",
                            "relMobile":   "13921209965",
                            "relRelation": "01"
                        }
                    ],
                    "residentialInfo": {
                        "liveAddr": "河南省信阳市平桥区武功山路118号",
                        "liveArea": "450000,464000,464100",
                        "liveInfo": "10"
                    },
                    "companyInfo":     {
                        "indivOccu":    "A",
                        "indivMthInc":  "05",
                        "indivEmpAddr": "武功山路55号",
                        "indivEmpName": "威能无锡供热设备有限公司",
                        "indivEmpArea": "450000,464000,464100",
                        "indivEmpTel":  "15243226975"
                    },
                    "individualInfo":  {
                        "indivEdu":     "10",
                        "indivMarital": "10"

                    }
                }
            }
        }
        return self.data_model(MinShengMethodsEnum.MESSAGE_PUSH.value[0], req_data)

    def get_credit_data(self, data):
        bank_card = data.get("channelBankCardNo")
        hub_user_id = data.get("hubUserId")
        mobile = data.get("channelMobile")

        channel_credit_no = data.get("channelCreditNo")

        req_data = {
            "applyNo": channel_credit_no,
            "openId": hub_user_id,
            "bank_card_info": {
                "cardNo": bank_card,
                "bankCode": "2345",
                "phoneNo": mobile
            }
        }
        return self.data_model(MinShengMethodsEnum.CREDIT.value[0], req_data)

    def get_credit_result_data(self, data):
        hub_order_no = data.get("hubOrderNo")

        req_data = {
            "outCreditOrderNo": hub_order_no,
        }
        return self.data_model(MinShengMethodsEnum.CREDIT_RESULT.value[0], req_data)

    def get_credit_info_data(self, data):
        hub_order_no = data.get("hubOrderNo")
        hub_user_id = data.get("hubUserId")
        channel_user_no = data.get("channelUserNo")

        req_data = {
            "userId": channel_user_no,
            "openId": hub_user_id,
            "outCreditOrderNo": hub_order_no,
        }
        return self.data_model(MinShengMethodsEnum.CREDIT_INFO.value[0], req_data)

    @staticmethod
    def get_url_data( data, link_type):
        #     LOAN("LOAN", "2"),
        #     REPAY("REPAY", "3"),;
        hub_user_id = data.get("hubUserId")
        req_data = {
            "linkType": link_type,
            "openId": hub_user_id,
            "callBackUrl": "baidu.com",
        }
        return req_data

    def get_loan_url_data(self, data):
        req_data = self.get_url_data(data, "LOAN")
        return self.data_model(MinShengMethodsEnum.GET_LOAN_URL.value[0], req_data)

    def get_repay_url_data(self, data):
        req_data = self.get_url_data(data, "REPAY")
        return self.data_model(MinShengMethodsEnum.GET_REPAY_URL.value[0], req_data)

    @staticmethod
    def get_contract_data(data, type):
        hub_user_id = data.get("hubUserId")
        channel_user_no = data.get("channelUserNo")
        req_data = {
            "openId":   hub_user_id,
            "userId":   channel_user_no,
            "busiType": type  # CREDIT\BIND\LOAN
        }
        return req_data

    def get_credit_contract_data(self, data=None):
        req_data = self.get_contract_data(data, "CREDIT")
        return self.data_model(MinShengMethodsEnum.CREDIT_CONTRACT.value[0], req_data)

    def get_bind_contract_data(self, data=None):
        req_data = self.get_contract_data(data, "BIND")
        return self.data_model(MinShengMethodsEnum.BIND_CONTRACT.value[0], req_data)

    def get_loan_contract_data(self, data=None):
        req_data = self.get_contract_data(data, "LOAN")
        return self.data_model(MinShengMethodsEnum.LOAN_CONTRACT.value[0], req_data)