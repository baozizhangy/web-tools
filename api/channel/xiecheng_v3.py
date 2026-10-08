#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from enum import Enum

from api.channel._base_requests import BaseRequest
from api.channel.xiecheng_v2 import XieChengV2


class XieChengV3MethodsEnum(Enum):
    # 渠道方法枚举，
    # ("渠道方法名", "方法中文名", "对应的数据模板方法")
    CHECK = ("unionCheckUser.do", "准入", "get_check_data")
    REGISTER = ("unionRegister.do", "注册", "get_register_data")
    CREDIT_APPLY = ("unionCreditApply.do", "授信申请", "get_credit_data")
    ACCOUNT_QUERY = ("unionCreditQuery.do", "额度查询", "get_credit_query_data")
    CONTRACT = ("getProtocols.do", "获取合同", "get_contract_data")


class XieChengV3(XieChengV2):
    # 携程
    def __init__(self, ):
        super().__init__(channel_id="HUB_XIECHENG_V3", channel_name="携程V3",
                         channel_method_enum=XieChengV3MethodsEnum, channel_uid="40080", py_code="xiecheng_v3")
