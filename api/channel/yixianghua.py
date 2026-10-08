#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import random
from enum import Enum

from api.channel._base_requests import BaseRequest
from utils.cryption_util import md5_encrypt
from utils.personal_util import get_person_name, get_id_no, get_mobile_no, fake


class YiXiangHuaMethodsEnum(Enum):
    # 宜享花渠道方法枚举，
    # ("渠道方法名", "方法中文名", "对应的数据模板方法")
    CHECK = ("user.access", "准入", "get_check_data")
    # REGISTER = ("user.regist", "注册", "get_register_data")
    CREDIT_SUPPLEMENT = ("credit.supplement", "信息补充", "get_credit_supplement_data")
    CREDIT_APPLY = ("credit.apply", "授信提交", "get_credit_apply_data")
    CREDIT_APPLY_RESULT = ("credit.apply.result", "授信提交结果", "get_credit_apply_result_data")
    USER_CREDIT_INFO = ("user.credit.info", "额度查询", "get_user_credit_info_data")
    SEMI_LOAN_APPLY = ("semi.loan.apply", "半流程借款申请", "get_semi_loan_apply_data")
    REPAY_URL = ("repay.url", "还款URL获取", "get_repay_url_data")
    CARD_BIND = ("card.bind", "绑卡申请", "get_card_bind_data")
    CARD_VERIFY = ("card.verify", "绑卡短信验证", "get_card_verify_data")
    CARD_LIST = ("card.list", "用户绑卡列表", "get_card_list_data")
    CREDIT_CHECK_INFO = ("loan.checkInfo", "授信是否增验", "get_credit_check_info_data")
    LOAN_CHECK_INFO = ("loan.checkInfo", "借款是否增验", "get_loan_check_info_data")
    REPAY_CHECK_INFO = ("loan.checkInfo", "还款是否增验", "get_repay_check_info_data")
    # USER_EXTRA = ("user.extra", "获取用户准入后流程参数", "get_user_extra_data")
    LOAN_APPLY_RESULT = ("loan.apply.result", "贷款信息查询", "get_loan_apply_result_data")
    REPAY_PLAN_QUERY = ("repay.plan.query", "还款计划查询", "get_repay_plan_data")
    REGISTER_AGREEMENT = ("agreement.query", "注册协议", "get_register_agreement_data")
    PRE_AGREEMENT = ("agreement.query", "贷前协议", "get_pre_agreement_data")
    CREDIT_AGREEMENT = ("agreement.query", "授信协议", "get_credit_agreement_data")
    BIND_AGREEMENT = ("agreement.query", "绑卡协议", "get_bind_agreement_data")
    LOAN_AGREEMENT = ("agreement.query", "借款协议", "get_loan_agreement_data")


class YiXiangHua(BaseRequest):
    # 玖富v2
    def __init__(self, ):
        super().__init__(channel_id="HUB_YIXIANGHUA", channel_name="宜享花",
                         channel_method_enum=YiXiangHuaMethodsEnum, channel_uid="20818", py_code="yixianghua")

    def get_check_data(self, data):
        # 返回准入信息模板
        print(f"get_check_data:data:{data}")
        mobile = data.get("channelMobile")
        input_id_no = data.get("channelIdNo")
        check_no = data.get("channelCheckNo")
        name = data.get("channelCustName")
        # 返回准入信息模板
        check_no = check_no if check_no else fake.uuid4()
        mobile_no = mobile if mobile else get_mobile_no()
        id_no = input_id_no if input_id_no else get_id_no()
        check_data = {
            "openId":                check_no,
            "phoneMD5":              md5_encrypt(mobile_no),
            "identityIdMD5":         md5_encrypt(id_no),
            "phoneAndIdentityIdMd5": md5_encrypt(mobile_no + id_no),
            "identityIdPrefix":      id_no[:6],
        }
        return self.data_model(YiXiangHuaMethodsEnum.CHECK.value[0], check_data)

    def get_credit_supplement_data(self, data):
        # 返回详细资料信息模板
        mobile = data.get("channelMobile")
        input_id_no = data.get("channelIdNo")
        name = data.get("channelCustName")
        bank_card = data.get("channelBankCardNo")
        channel_user_no = data.get("channelUserNo")
        input_check_no = data.get("channelCheckNo")
        channel_credit_no = data.get("channelCreditNo")
        channel_draw_no = data.get("channelDrawNo")
        channel_repay_no = data.get("channelRepayNo")
        profile_data = {
            "openId":                 channel_user_no,
            "name":                   name,
            "identityId":             input_id_no,
            "phone":                  mobile,
            "degree":                 50,
            "education":              20,
            "salaryFix":              10000,
            "ocrAddress":             "上海市普陀区真华路",
            "contactAddress":         "我们没有",
            "contactAddressPostCode": "我们没有",
            "maritalStatus":          20,
            "houseType":              10,
            "address":                "时代峰峻上岛咖啡",
            "provinceCode":           "121212",
            "cityCode":               "12122",
            "email":                  "zzc213@126.com",
            "companyName":            "单位名称",
            "industryType":           "A",
            "position":               20,
            "title":                  10,
            "occupation":             10,
            "amount":                 10000,
            "termNum":                6,
            "loanUse":                10,
            "contactItemList":        [
                {
                    "contactName":          "李测",
                    "contactMobile":        "18625325210",
                    "contactRelation":      1,
                    "contactRelationLevel": 1
                },
                {
                    "contactName":          "李测试服",
                    "contactMobile":        "18625325216",
                    "contactRelation":      6,
                    "contactRelationLevel": 0
                }
            ],
            "cardInfo":               {
                "cardNo":   bank_card,
                "phone":    mobile,
                "bankName": "工商银行",
                "bankCode": "ICBC",
                "cardType": "0002"
            }
        }
        return self.data_model(YiXiangHuaMethodsEnum.CREDIT_SUPPLEMENT.value[0], profile_data)

    def get_credit_apply_data(self, data):
        # 返回授信信息模板
        mobile = data.get("channelMobile")
        input_id_no = data.get("channelIdNo")
        name = data.get("channelCustName")
        bank_card = data.get("channelBankCardNo")
        channel_user_no = data.get("channelUserNo")
        input_check_no = data.get("channelCheckNo")
        channel_credit_no = data.get("channelCreditNo")
        channel_draw_no = data.get("channelDrawNo")
        channel_repay_no = data.get("channelRepayNo")

        user_name = name if name else get_person_name()
        mobile_no = mobile if mobile else get_mobile_no()
        id_no = input_id_no if input_id_no else get_id_no()
        base64_data = "iVBORw0KGgoAAAANSUhEUgAAAjkAAAFBCAYAAACVcr5cAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAFiUAABYlAUlSJPAAAAWZSURBVHhe7dYxEQAgEMCwB/+egQEVvWSpha7zDABAzP4FAEgxOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABBMxeXJgZ+f2mLWgAAAABJRU5ErkJggg=="

        credit_data = {
            "openId":        channel_user_no,
            "orderNo":       channel_credit_no,
            "name":          user_name,
            "identityId":    id_no,
            "phone":         mobile_no,
            "os":            1,
            "ocrResult":     {
                "provider":                 "旷世",
                "idCardFrontPhoto":         base64_data,
                "idCardBackPhoto":          base64_data,
                "identifyInvalidDateStart": "2023-09-12",
                "identifyInvalidDateEnd":   "2043-10-12",
                "ocrAddress":               "上海市普陀区真华路",
                "gender":                   "男",
                "authority":                "上海普陀公安局",
                "nation":                   "汉"
            },
            "faceCmpResult": {
                "faceCmpScore": "80",
                "livePhoto":    base64_data,
                "provider":     "旷世"
            },
            "deviceInfo":    {
                "deviceId":  None,
                "deviceIp":  "192.132.12.3",
                "latitude":  None,
                "longitude": None,
                "os":        "ios"
            }
        }
        return self.data_model(YiXiangHuaMethodsEnum.CREDIT_APPLY.value[0], credit_data)

    def get_credit_apply_result_data(self, data):
        # 返回额度查询信息模板
        open_id = data.get("channelUserNo")
        order_no = data.get("channelCreditNo")
        # 返回准入信息模板
        req_data = {
            "openId":                open_id,
            "orderNo":               order_no,
        }
        return self.data_model(YiXiangHuaMethodsEnum.CREDIT_APPLY_RESULT.value[0], req_data)

    def get_repay_url_data(self, data):
        # 获取还款url
        open_id = data.get("channelUserNo")
        mobile = data.get("channelMobile")
        apply_no = data.get("channelDrawNo")
        # 返回准入信息模板
        req_data = {
            "openId":                open_id,
            "phone":               mobile,
            "applyNo":               apply_no,
        }
        return self.data_model(YiXiangHuaMethodsEnum.REPAY_URL.value[0], req_data)

    @staticmethod
    def get_check_info_data(data, biz_type, biz_no=None, loan_amount=None, term_num=None):
        # 是否需要增验
        open_id = data.get("channelUserNo")
        bank_card = data.get("channelBankCardNo")

        req_data = {
            "openId":               open_id,
            "bizType":                biz_type,  # 授信:credit  借款:loan  还款:repay
            "bizNo":               biz_no,  # BizType=loan时必传借款单号
            "loanAmount":               loan_amount,  # BizType=loan时必传
            "termNum":               term_num,  # BizType=loan时必传
            "cardNo":               bank_card,
        }
        return req_data

    def get_credit_check_info_data(self, data):
        req_data = self.get_check_info_data(data, "credit")
        return self.data_model(YiXiangHuaMethodsEnum.CREDIT_CHECK_INFO.value[0], req_data)

    def get_loan_check_info_data(self, data):
        apply_no = data.get("channelDrawNo")
        req_data = self.get_check_info_data(data, "loan", apply_no, "12000", "6")
        return self.data_model(YiXiangHuaMethodsEnum.LOAN_CHECK_INFO.value[0], req_data)

    def get_repay_check_info_data(self, data):
        req_data = self.get_check_info_data(data, "repay")
        return self.data_model(YiXiangHuaMethodsEnum.REPAY_CHECK_INFO.value[0], req_data)

    def get_loan_apply_result_data(self, data):
        open_id = data.get("channelUserNo")
        hub_sub_order_no = data.get("hubSubOrderNo")
        order_no = data.get("channelCreditNo")
        apply_no = data.get("channelDrawNo")
        req_data = {
            "openId":               open_id,
            "applyNo":                apply_no,
            "orderNo":              order_no,
            "batchNo":               hub_sub_order_no
        }
        return self.data_model(YiXiangHuaMethodsEnum.LOAN_APPLY_RESULT.value[0], req_data)

    def get_repay_plan_data(self, data):
        open_id = data.get("channelUserNo")
        apply_no = data.get("channelDrawNo")
        req_data = {
            "openId":               open_id,
            "applyNo":                apply_no,
        }
        return self.data_model(YiXiangHuaMethodsEnum.REPAY_PLAN_QUERY.value[0], req_data)


    def get_user_credit_info_data(self, data):
        # 返回额度查询信息模板
        open_id = data.get("channelUserNo")
        order_no = data.get("channelCreditNo")
        check_no = data.get("channelCheckNo")
        # 返回准入信息模板
        open_id = open_id if open_id else fake.uuid4()
        order_no = order_no if order_no else fake.uuid4()
        check_data = {
            "openId":                open_id,
            "orderNo":               order_no,
        }
        return self.data_model(YiXiangHuaMethodsEnum.USER_CREDIT_INFO.value[0], check_data)

    def get_semi_loan_apply_data(self, data):
        # 返回借款信息模板
        open_id = data.get("channelUserNo")
        apply_no = data.get("channelDrawNo")
        mobile = data.get("channelMobile")

        # 返回准入信息模板
        open_id = open_id if open_id else fake.uuid4()
        apply_no = apply_no if apply_no else fake.uuid4()
        check_data = {
            "openId":                open_id,
            "applyNo":               apply_no,
            "phone": mobile
        }
        return self.data_model(YiXiangHuaMethodsEnum.SEMI_LOAN_APPLY.value[0], check_data)

    @staticmethod
    def get_contract_data(data, contract_type):
        channel_user_no = data.get("channelUserNo", f"default_value_{random.randint(1, 1000)}")
        channel_credit_no = data.get("channelCreditNo", f"default_value_{random.randint(1, 1000)}")
        contract_data = {
            "openId": channel_user_no,
            "flowId": channel_credit_no,
            "agreementType": contract_type
        }
        return contract_data

    def get_register_agreement_data(self, data):
        req_data = self.get_contract_data(data, "REGISTER")
        return self.data_model(YiXiangHuaMethodsEnum.REGISTER_AGREEMENT.value[0], req_data)

    def get_pre_agreement_data(self, data):
        req_data = self.get_contract_data(data, "PRE_LOAN")
        return self.data_model(YiXiangHuaMethodsEnum.PRE_AGREEMENT.value[0], req_data)

    def get_credit_agreement_data(self, data):
        req_data = self.get_contract_data(data, "CREDIT")
        return self.data_model(YiXiangHuaMethodsEnum.CREDIT_AGREEMENT.value[0], req_data)

    def get_bind_agreement_data(self, data):
        req_data = self.get_contract_data(data, "BIND")
        return self.data_model(YiXiangHuaMethodsEnum.BIND_AGREEMENT.value[0], req_data)

    def get_loan_agreement_data(self, data):
        req_data = self.get_contract_data(data, "LOAN")
        return self.data_model(YiXiangHuaMethodsEnum.LOAN_AGREEMENT.value[0], req_data)



if __name__ == '__main__':
    # result = [
    #     {"inner_method": member.value[0], "method_name": member.value[1], "method": member.value[2]}
    #     for member in YiXiangHuaMethodsEnum
    # ]

    print(YiXiangHuaMethodsEnum.CHECK.value[0])
