#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import random
from enum import Enum

from api.channel._base_requests import BaseRequest
from api.channel.channel_api_config import ChannelMethodsEnum
from utils.cryption_util import md5_encrypt
from utils.personal_util import get_person_name, get_id_no, get_mobile_no

# Map < String, String > juZiMethodMap = new
# HashMap <> ();
# juZiMethodMap.put("qualifyMd5", MethodEnum.CHECK.getCode());
# juZiMethodMap.put("submitUserBaseInfo", MethodEnum.SUBMIT.getCode());
# juZiMethodMap.put("supportBank", MethodEnum.BANK_LIST.getCode());
# juZiMethodMap.put("queryBindCardList", MethodEnum.BIND_LIST.getCode());
# juZiMethodMap.put("bindCard", MethodEnum.BIND_CARD.getCode());
# juZiMethodMap.put("confirmBindCard", MethodEnum.BIND_VERIFY.getCode());
# juZiMethodMap.put("trial", MethodEnum.TRIAL.getCode());
# juZiMethodMap.put("queryCreditResult", MethodEnum.CONCLUSION.getCode());
# juZiMethodMap.put("queryOrder", MethodEnum.STATUS.getCode());
# juZiMethodMap.put("submitLoanOrder", MethodEnum.CONFIRM_ORDER.getCode());
# juZiMethodMap.put("getContract", MethodEnum.CONTRACT.getCode());
# juZiMethodMap.put("queryRepayPlans", MethodEnum.REPAY_INFO.getCode());
# juZiMethodMap.put("getSignContract", MethodEnum.CONTRACT.getCode());
# juZiMethodMap.put("queryPaymentResult", MethodEnum.REPAY_RESULT.getCode());
# juZiMethodMap.put("repay", MethodEnum.REPAY.getCode());
# juZiMethodMap.put("confirmRepay", MethodEnum.REPAY_VCODE.getCode());
# juZiMethodMap.put("sendVerifyCode", MethodEnum.CONFIRM_CODE.getCode());
# juZiMethodMap.put("confirmVerifyCode", MethodEnum.CONFIRM_VCODE.getCode());
# channelMethodMappingMap.put(ChannelEnum.JU_ZI.getCode(), juZiMethodMap);
# channelMethodMappingMap.put(ChannelEnum.JU_ZI_S1.getCode(), juZiMethodMap);


class JuZiMethodsEnum(Enum):
    # 宜享花渠道方法枚举，
    # ("渠道方法名", "方法中文名", "对应的数据模板方法")
    CHECK = ("check", "准入", "get_check_data")
    PROFILE = ("submitUserBaseInfo", "信息采集", "get_profile_data")
    CREDIT_AGREEMENT = ("getSignContract", "授信协议", "get_credit_agreement_data")
    DRAW_AGREEMENT = ("getSignContract", "借款协议", "get_draw_agreement_data")


class JuZi(BaseRequest):
    # JuZi
    def __init__(self, ):
        super().__init__(channel_id="HUB_JUZI", channel_name="桔子", channel_method_enum=JuZiMethodsEnum,
                         channel_uid="20404", py_code="juzi")

    def get_check_data(self, data):
        # 返回准入信息模板
        mobile = data.get("channelMobile")
        input_id_no = data.get("channelIdNo")
        name = data.get("channelCustName")
        # 返回准入信息模板
        user_name = name if name else get_person_name()
        mobile_no = mobile if mobile else get_mobile_no()
        id_no = input_id_no if input_id_no else get_id_no()
        req_data = {
            "name":        user_name,
            "mobile":        md5_encrypt(mobile_no),
            "idCard":         md5_encrypt(id_no),
            "mobileAndIdCard": md5_encrypt(mobile_no + id_no),
        }
        return self.data_model(JuZiMethodsEnum.CHECK.value[0], req_data)

    @staticmethod
    def get_contract_data(data, contract_type):
        channel_user_no = data.get("channelUserNo", f"default_value_{random.randint(1, 1000)}")
        channel_credit_no = data.get("channelCreditNo", f"default_value_{random.randint(1, 1000)}")
        contract_data = {
            "jzUserId": channel_user_no,
            "creditId": channel_credit_no,
            "type": contract_type
        }
        return contract_data

    def get_credit_agreement_data(self, data):
        req_data = self.get_contract_data(data, "1")
        return self.data_model(JuZiMethodsEnum.CREDIT_AGREEMENT.value[0], req_data)

    def get_draw_agreement_data(self, data):
        req_data = self.get_contract_data(data, "2")
        return self.data_model(JuZiMethodsEnum.DRAW_AGREEMENT.value[0], req_data)

