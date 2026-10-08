#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
import time
from enum import Enum

from api.channel._base_requests import BaseRequest
from utils.cryption_util import md5_encrypt, Base64Utils
from utils.personal_util import fake, get_person_name, get_mobile_no, get_id_no


# xieChengV2MethodMap.put("unionCheckUser.do", MethodEnum.CHECK.getCode());
# xieChengV2MethodMap.put("unionCreditApply.do", MethodEnum.SEND_DATA.getCode());
# xieChengV2MethodMap.put("getProtocols.do", MethodEnum.CONTRACT.getCode());
# xieChengV2MethodMap.put("unionRegister.do", MethodEnum.REGISTER.getCode());
# xieChengV2MethodMap.put("unionCreditQuery.do", MethodEnum.CONCLUSION.getCode());


class XieChengV2MethodsEnum(Enum):
    # 携程v2渠道方法枚举，
    # ("渠道方法名", "方法中文名", "对应的数据模板方法")
    CHECK = ("unionCheckUser.do", "准入", "get_check_data")
    REGISTER = ("unionRegister.do", "注册", "get_register_data")
    CREDIT_APPLY = ("unionCreditApply.do", "授信申请", "get_credit_data")
    ACCOUNT_QUERY = ("unionCreditQuery.do", "额度查询", "get_credit_query_data")
    CONTRACT = ("getProtocols.do", "获取合同", "get_contract_data")


class XieChengV2(BaseRequest):
    # 携程
    def __init__(self, channel_id="HUB_XIECHENG_V2", channel_name="携程V2",
                 channel_method_enum=XieChengV2MethodsEnum, channel_uid="21157", py_code="xiecheng_v2"):
        super().__init__(channel_id=channel_id, channel_name=channel_name,
                         channel_method_enum=channel_method_enum, channel_uid=channel_uid, py_code=py_code)

    def get_check_data(self, data):
        # 获取准入数据
        mobile = data.get("channelMobile")
        input_id_no = data.get("channelIdNo")
        # 返回准入信息模板
        check_data = {
            "mobileMd5": md5_encrypt(mobile),
            "idCodeMd5": md5_encrypt(input_id_no),
        }
        return self.data_model(XieChengV2MethodsEnum.CHECK.value[0], check_data)

    def get_register_data(self, data):
        # 获取注册数据
        mobile = data.get("channelMobile")
        id_no = data.get("channelIdNo")
        channel_user_no = data.get("channelUserNo")
        channel_credit_no = data.get("channelCreditNo")

        # 返回准入信息模板
        check_data = {
            "mobile":       mobile,
            "orderNo":      channel_credit_no,
            "openId":       channel_user_no,
            "identityCode": id_no
        }
        return self.data_model(XieChengV2MethodsEnum.REGISTER.value[0], check_data)

    def get_credit_data(self, data):
        mobile = data.get("channelMobile")
        id_no = data.get("channelIdNo")
        input_check_no = data.get("channelCheckNo")
        name = data.get("channelCustName")
        channel_user_no = data.get("channelUserNo")
        channel_credit_no = data.get("channelCreditNo")

        check_no = input_check_no if input_check_no else fake.uuid4()
        base64_data = "iVBORw0KGgoAAAANSUhEUgAAAjkAAAFBCAYAAACVcr5cAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAFiUAABYlAUlSJPAAAAWZSURBVHhe7dYxEQAgEMCwB/+egQEVvWSpha7zDABAzP4FAEgxOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABBMxeXJgZ+f2mLWgAAAABJRU5ErkJggg=="
        address = fake.address().replace(" ", "")
        user_info = {
            "userName":       name,
            "identityType":   "IDENTITYCARD",
            "identityCode":   id_no,
            "registerMobile": mobile
        }

        character_data = {
            "face_image":              base64_data,
            "identity_card_image_2":   base64_data,
            "identity_card_image_1":   base64_data,
            "contact_relate":          "配偶",
            "occupation":              "农林牧渔从业人员",
            "idcard_ocr_birthday":     19901004,
            "idcard_ocr_race":         "汉",
            "contacts_mobile":         get_mobile_no(),
            "contact_relate_2":        "朋友",
            "company_detailedAddress": "携程",
            "idcard_ocr_validity":     "2016.07.14-2026.07.14",
            "contact_name":            get_person_name(),
            "idcard_ocr_addr":         Base64Utils.encode(address),
            "idcard_ocr_gender":       "F",
            "domicile_place":          Base64Utils.encode(address),
            "workAreaStr":             "吉林省,松原市,扶余市",
            "idcard_ocr_authority":    "商城县公安局",
            "contact_name_2":          get_person_name(),
            "req_mobile":              get_mobile_no(),
            "homeAreaStr":             "吉林省,松原市,扶余市",
            "marital":                 "已婚有子女",
            "homeAreaDetail":          "吉林省,松原市,扶余市",
            "company_name":            "携程金融",
            "month_income":            "5万以上",
            "liveProvinceCode":        "465350",
            "liveCityCode":            "465351",
            "liveDistrictCode":        "465352",
            "education":               "大学本科",
            "contacts_mobile_2":       get_mobile_no(),
            "face_confidence":         "99",
            "face_channel":            "微众"
        }

        credit_data = {
            "orderNo":       channel_credit_no,
            "openId":        channel_user_no,
            "occurTime":     "20241617125050",
            "userInfo":      json.dumps(user_info, ensure_ascii=False),
            "characterData": json.dumps(character_data, ensure_ascii=False)
        }
        print(f"credit_data: {credit_data}")
        return self.data_model(XieChengV2MethodsEnum.CREDIT_APPLY.value[0], credit_data)

    def get_credit_query_data(self, data):
        # 获取授信查询数据
        channel_user_no = data.get("channelUserNo")
        channel_credit_no = data.get("channelCreditNo")

        # 返回准入信息模板
        check_data = {
            "orderNo": channel_credit_no,
            "openId":  channel_user_no
        }
        return self.data_model(XieChengV2MethodsEnum.ACCOUNT_QUERY.value[0], check_data)

    def get_contract_data(self, data):
        # 获取协议数据

        # 返回准入信息模板
        check_data = {
            "scene": "5"
        }
        return self.data_model(XieChengV2MethodsEnum.CONTRACT.value[0], check_data)
