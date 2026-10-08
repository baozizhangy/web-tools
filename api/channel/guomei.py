#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from calendar import c
from enum import Enum

from api.channel._base_requests import BaseRequest
from utils.cryption_util import md5_encrypt
from utils.personal_util import get_mobile_no, get_id_no, fake, get_person_name


class GuoMeiMethodsEnum(Enum):
    # 宜享花渠道方法枚举，
    # ("渠道方法名", "方法中文名", "对应的数据模板方法")
    CHECK = ("check", "准入", "get_check_data")
    CREDIT_APPLY = ("submit", "授信申请", "get_credit_data")
    CREDIT_QUERY = ("conclusion", "授信结果查询", "get_credit_query_data")
    CONTRACT = ("contract", "协议查询", "get_contract_data")


class GuoMei(BaseRequest):
    # 国美
    def __init__(self, ):
        super().__init__(channel_id="HUB_GUOMEI", channel_name="国美", channel_method_enum=GuoMeiMethodsEnum,
                         channel_uid="22379", py_code="guomei")

    @BaseRequest.non_empty(["channelMobile", "channelIdNo", "channelCustName"])
    def get_check_data(self, data):
        # 获取准入数据
        mobile = data.get("channelMobile")
        id_no = data.get("channelIdNo")
        name = data.get("channelCustName")
        check_data = {
            "phoneNo":      md5_encrypt(mobile),
            "idNo":         md5_encrypt(id_no),
            "customerName": md5_encrypt(name)
        }
        return self.data_model(GuoMeiMethodsEnum.CHECK.value[0], check_data)

    @BaseRequest.non_empty(["channelMobile", "channelIdNo", "channelCustName", "channelBankCardNo", "channelCreditNo"])
    def get_credit_data(self, data):
        mobile_no = data.get("channelMobile")
        id_no = data.get("channelIdNo")
        name = data.get("channelCustName")
        bank_card = data.get("channelBankCardNo")
        credit_no = data.get("channelCreditNo")

        base64_data = "iVBORw0KGgoAAAANSUhEUgAAAjkAAAFBCAYAAACVcr5cAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAFiUAABYlAUlSJPAAAAWZSURBVHhe7dYxEQAgEMCwB/+egQEVvWSpha7zDABAzP4FAEgxOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABBMxeXJgZ+f2mLWgAAAABJRU5ErkJggg=="

        credit_data = {
            "creditApplyNo":  credit_no,
            "applyLmt":       12000.0,
            "applicationDto": {
                "birthday":             "1996-08-24",
                "linkmanList":          [
                    {
                        "phone":         get_mobile_no(),
                        "name":          get_person_name(),
                        "relationLevel": "2",
                        "relation":      "F"
                    },
                    {
                        "phone":         get_mobile_no(),
                        "name":          get_person_name(),
                        "relationLevel": "1",
                        "relation":      "Y"
                    }],
                "education":            "university",
                "occupation":           "D",
                "companyArea":          "东城区",
                "nation":               "汉",
                "loanUsage":            "PN07",
                "companyName":          "鹏润大厦",
                "idCardBank":           base64_data,
                "idNo":                 id_no,
                "phoneNo":              mobile_no,
                "issuer":               "许昌县公安局",
                "liveCity":             "许昌市",
                "liveProvinceCode":     "410000",
                "companyProvinceCode":  "110000",
                "idEffectDate":         1412006400000,
                "companyNature":        "J",
                "companyProvince":      "北京市",
                "idDueDate":            1727625600000,
                "companyCity":          "北京市市辖区",
                "idType":               "1",
                "liveAddress":          "河南省许昌市建安区河南省许昌县小召乡天王寺村",
                "bankCardNo":           bank_card,
                "sex":                  "M",
                "borrower":             base64_data,
                "liveProvince":         "河南省",
                "bankPhoneNo":          mobile_no,
                "customerName":         name,
                "companyAreaCode":      "110101",
                "liveCityCode":         "411000",
                "liveDistrict":         "建安区",
                "idCardFace":           base64_data,
                "photoType":            "png",
                "companyCityCode":      "110100",
                "idCardAddress":        "河南省许昌县小召乡天王寺村",
                "detailCompanyAddress": "北京市朝阳区",
                "maritalStatus":        "1",
                "liveDistrictCode":     "411003"
            },
            "applyTime":      1718785684516,
            "callBackUrl":    "https://static-sit1.gomemyf.com/gmcf-cmc-sit-0-38/gmcf-cmc/rejection/riskCallBack",
            "capitalCode":    "R0025",
        }
        return self.data_model(GuoMeiMethodsEnum.CREDIT_APPLY.value[0], credit_data)

    @BaseRequest.non_empty(["channelCreditNo"])
    def get_credit_query_data(self, data):
        channel_credit_no = data.get("channelCreditNo")
        query_data = {
            "creditApplyNo": channel_credit_no,
        }
        return self.data_model(GuoMeiMethodsEnum.CREDIT_QUERY.value[0], query_data)

    def get_contract_data(self, data):
        """拉取协议数据"""
        repay_data = {
            "capitalCode": "001"
        }
        return self.data_model(GuoMeiMethodsEnum.CONTRACT.value[0], repay_data)
