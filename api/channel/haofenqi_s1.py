#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from enum import Enum

from api.channel._base_requests import BaseRequest
from api.channel.haofenqi import HaoFenQi


class HaoFenQiS1MethodsEnum(Enum):
    # 渠道方法枚举，
    # ("渠道方法名", "方法中文名", "对应的数据模板方法")
    CHECK = ("check", "准入", "get_check_data")
    REGISTER = ("register", "注册", "get_register_data")
    SUBMIT_CHECK = ("submit_check", "授信前检查", "get_submit_check_data")
    SUBMIT = ("submit", "授信申请", "get_submit_data")
    SUBMIT_RESULT = ("submit_result", "授信结果查询", "get_submit_result_data")
    BANK_INFO = ("bank_info", "银行卡信息", "get_bank_info_data")
    BANK_LIST = ("bank_list", "获取银行卡列表", "get_bank_list_data")
    BIND_CARD = ("bind_card", "绑定银行卡", "get_bind_card_data")
    BIND_VERIFY = ("bind_verify", "银行卡验证", "get_bind_verify_data")
    SCENE_URL = ("scene_url", "获取URL", "get_scene_url_data")
    REPAY_INFO = ("repay_info", "获取还款信息", "get_repay_info_data")
    BASE_CONTRACT = ("contract", "基本信息页合同", "get_base_contract_data")
    DRAW_CONTRACT = ("contract", "确认借款页合同", "get_draw_contract_data")
    BIND_CONTRACT = ("contract", "绑卡页面合同", "get_bind_contract_data")
    LOAN_CONTRACT = ("contract", "账单页面合同", "get_loan_contract_data")
    AUTH_CONTRACT = ("contract", "授信页面合同", "get_auth_contract_data")
    USER_CONTRACT = ("contract", "用户隐私协议", "get_user_contract_data")


class HaoFenQiS1(HaoFenQi, BaseRequest):
    def __init__(self,):
        super().__init__(channel_id="HUB_HAOFENQI_S1", channel_name="好分期S1",
                         channel_method_enum=HaoFenQiS1MethodsEnum, channel_uid="20602", py_code="haofenqi_s1")
