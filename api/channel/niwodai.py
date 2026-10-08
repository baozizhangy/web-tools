#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from enum import Enum

from api.channel._base_requests import BaseRequest
from api.channel.channel_api_config import ChannelMethodsEnum
from utils.cryption_util import md5_encrypt
from utils.personal_util import get_person_name, get_id_no, get_mobile_no


# niWoDaiMethodMap.put("entry", MethodEnum.CHECK.getCode());
# niWoDaiMethodMap.put("contract", MethodEnum.CONTRACT.getCode());
# niWoDaiMethodMap.put("apply", MethodEnum.SEND_DATA.getCode());
# niWoDaiMethodMap.put("apply-result", MethodEnum.SUBMIT_RESULT.getCode());
# niWoDaiMethodMap.put("repayment-result", MethodEnum.FUNDED_RESULT.getCode());
# niWoDaiMethodMap.put("url", MethodEnum.SCENE_URL.getCode());


class NiWoDaiMethodsEnum(Enum):
    # homo相关渠道方法枚举，
    # ("渠道方法名", "方法中文名", "对应的数据模板方法")
    CHECK = ("entry", "准入", "get_check_data")
    CREDIT = ("apply", "授信", "get_credit_data")
    CREDIT_RESULT = ("apply-result", "授信结果", "get_credit_result_data")
    # GET_BIND_CARD_URL = ("url", "获取绑卡页url", "get_bind_card_url_data")  # 未使用
    GET_CONFIRM_LOAN_URL = ("url", "获取确认借款页url", "get_confirm_loan_url_data")
    GET_REPAYMENT_URL = ("url", "获取还款页url", "get_repayment_url_data")
    REPAYMENT_RESULT = ("repayment-result", "还款信息", "get_repayment_result_data")
    # 合同
    APPLY_CONTRACT = ("contract", "借款申请类合同", "get_apply_contract_data")
    LOAN_CONTRACT = ("contract", "借款类合同", "get_loan_contract_data")
    REGISTER_CONTRACT = ("contract", "注册类合同", "get_register_contract_data")
    CONFIRM_LOAN_CONTRACT = ("contract", "确认借款类合同", "get_confirm_loan_contract_data")
    WITHHOLD_CONTRACT = ("contract", "绑卡类合同", "get_withhold_contract_data")
    AUTHORIZE_CONTRACT = ("contract", "授权类合同", "get_authorize_contract_data")
    CREDIT_CONTRACT = ("contract", "征信查询授权类合同", "get_credit_contract_data")
    PRIVACY_CONTRACT = ("contract", "隐私政策类合同", "get_privacy_contract_data")


class NiWoDai(BaseRequest):
    # 你我贷
    def __init__(self, channel_id="HUB_NIWODAI", channel_name="你我贷",
                 channel_method_enum=NiWoDaiMethodsEnum, channel_uid="20572", py_code="niwodai"):
        super().__init__(channel_id=channel_id, channel_name=channel_name,
                         channel_method_enum=channel_method_enum, channel_uid=channel_uid, py_code=py_code)

    def get_check_data(self, data):
        # 返回准入信息模板
        mobile = data.get("channelMobile")
        input_id_no = data.get("channelIdNo")
        req_data = {
            "type":  "1,2,3",
            "value": f"{md5_encrypt(mobile)},{md5_encrypt(input_id_no)},{md5_encrypt(mobile + input_id_no)},"
        }
        return self.data_model(NiWoDaiMethodsEnum.CHECK.value[0], req_data)

    def get_credit_data(self, data):
        mobile = data.get("channelMobile")
        id_no = data.get("channelIdNo")
        name = data.get("channelCustName")
        channel_credit_no = data.get("channelCreditNo")
        base64_data = "iVBORw0KGgoAAAANSUhEUgAAAjkAAAFBCAYAAACVcr5cAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAFiUAABYlAUlSJPAAAAWZSURBVHhe7dYxEQAgEMCwB/+egQEVvWSpha7zDABAzP4FAEgxOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABBMxeXJgZ+f2mLWgAAAABJRU5ErkJggg=="

        req_data = {
            "orderId":     channel_credit_no,
            "userInfo":    {
                "realName":        name,
                "idcardNumber":    id_no,
                "phone":           mobile,
                "gender":          "男",
                "nation":          "汉",
                "idcardAddress":   "上海市浦东新区北蔡镇北艾路",
                "maritalStatus":   "1",
                "education":       "0",
                "occupation":      "3",
                "industry":        "101",
                "idcardFront":     base64_data,
                "idcardBack":      base64_data,
                "bioPhoto":        base64_data,
                "imageType":       "BASE64",
                "province":        "湖南省",
                "city":            "长沙市",
                "district":        "岳麓区",
                "address":         "梅溪湖大学中路",
                "income":          "50000",
                "debt":            "0",
                "idcardAuthority": "湖南省长沙市望城区",
                "idcardValidity":  "2019.08.16-2029.08.16",
                "purposeNote":     "1",
                "faceSource":      "2",
                "score":           "90",
                "email":           "129298920@qq.com"
            },
            "companyInfo": {
                "name":        "卡拉卡拉有限公司",
                "workP":       "湖南省",
                "workC":       "长沙市",
                "workA":       "岳麓区",
                "workAddress": "望江古美格嘻嘻"
            },
            "contacts":    {
                "nameA":         get_person_name(),
                "phoneA":        get_mobile_no(),
                "relationshipA": "2",
                "nameB":         get_person_name(),
                "phoneB":        get_mobile_no(),
                "relationshipB": "11"
            },
            "deviceInfo": {
                "breakOut":  "",
                "deviceId":  "",
                "idfa":      "",
                "idfv":      "",
                "imei2":     "",
                "ip":        "183.210.48.128",
                "latitude":  "31.53661",
                "longitude": "120.292383",
                "mac":       "",
                "model":     "",
                "osVersion": "MIUI",
                "src":       "android"
            }
        }
        return self.data_model(NiWoDaiMethodsEnum.CREDIT.value[0], req_data)

    def get_credit_result_data(self, data):
        req_data = {
            "orderId": data.get("channelCreditNo")
        }
        return self.data_model(NiWoDaiMethodsEnum.CREDIT_RESULT.value[0], req_data)

    @staticmethod
    def get_url_data(data, url_type):
        #     @ApiModelProperty("页面类型；BINDCARD ：绑卡页CONFIRMLOAN:确认借款页；REPAYMENT：还款页；")
        url_data = {
            "orderId":     data.get("channelCreditNo"),
            "type":        url_type,
            "callbackUrl": "baidu.com"
        }
        return url_data

    def get_bind_card_url_data(self, data):
        req_data = self.get_url_data(data, "BINDCARD")
        return self.data_model(NiWoDaiMethodsEnum.GET_BIND_CARD_URL.value[0], req_data)

    def get_confirm_loan_url_data(self, data):
        req_data = self.get_url_data(data, "CONFIRMLOAN")
        return self.data_model(NiWoDaiMethodsEnum.GET_CONFIRM_LOAN_URL.value[0], req_data)

    def get_repayment_url_data(self, data):
        req_data = self.get_url_data(data, "REPAYMENT")
        return self.data_model(NiWoDaiMethodsEnum.GET_REPAYMENT_URL.value[0], req_data)

    def get_repayment_result_data(self, data):
        req_data = {
            "orderId": data.get("channelCreditNo")
        }
        return self.data_model(NiWoDaiMethodsEnum.REPAYMENT_RESULT.value[0], req_data)

    @staticmethod
    def get_contact_data(data, contract_type):
        #     @ApiModelProperty("合同类型；APPLY：借款申请类合同；LOAN：借款类合同；REGISTER：注册类合同；WITHHOLD：
        #     绑卡类合同；（主要是代扣合同）AUTHORIZE:授权类合同；CREDIT：征信查询授权类合同；PRIVACY：隐私政策类合同；")
        contract_data = {
            "orderId": data.get("channelCreditNo"),
            "type":    contract_type
        }
        return contract_data

    def get_apply_contract_data(self, data):
        req_data = self.get_contact_data(data, "APPLY")
        return self.data_model(NiWoDaiMethodsEnum.APPLY_CONTRACT.value[0], req_data)

    def get_loan_contract_data(self, data):
        req_data = self.get_contact_data(data, "LOAN")
        return self.data_model(NiWoDaiMethodsEnum.LOAN_CONTRACT.value[0], req_data)

    def get_register_contract_data(self, data):
        req_data = self.get_contact_data(data, "REGISTER")
        return self.data_model(NiWoDaiMethodsEnum.REGISTER_CONTRACT.value[0], req_data)

    def get_withhold_contract_data(self, data):
        req_data = self.get_contact_data(data, "WITHHOLD")
        return self.data_model(NiWoDaiMethodsEnum.WITHHOLD_CONTRACT.value[0], req_data)

    def get_authorize_contract_data(self, data):
        req_data = self.get_contact_data(data, "AUTHORIZE")
        return self.data_model(NiWoDaiMethodsEnum.AUTHORIZE_CONTRACT.value[0], req_data)

    def get_credit_contract_data(self, data):
        req_data = self.get_contact_data(data, "CREDIT")
        return self.data_model(NiWoDaiMethodsEnum.CREDIT_CONTRACT.value[0], req_data)

    def get_privacy_contract_data(self, data):
        req_data = self.get_contact_data(data, "PRIVACY")
        return self.data_model(NiWoDaiMethodsEnum.PRIVACY_CONTRACT.value[0], req_data)
