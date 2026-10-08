#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import random
from enum import Enum

from api.channel._base_requests import BaseRequest
from api.channel.channel_api_config import ChannelMethodsEnum
from api.channel.homo import HoMo, HoMoMethodsEnum
from utils.cryption_util import md5_encrypt
from utils.personal_util import get_person_name, get_mobile_no, get_id_no, fake, get_bank_card


# from api import BaseRequest
# from api import ChannelMethodsEnum
# from utils.cryption import md5_encrypt
# from utils.personal_info import get_person_name, get_mobile_no, get_id_no, fake, get_bank_card


class FuYuanHuiMethodsEnum(Enum):
    # 渠道方法枚举，
    # ("渠道方法名", "方法中文名", "对应的数据模板方法")
    CHECK = ("check", "准入", "get_check_data")
    REGISTER = ("register", "注册", "get_register_data")
    CONCLUSION = ("conclusion", "授信结果/额度", "get_conclusion_data")
    SUBMIT_CHECK = ("submit_check", "授信前检查", "get_submit_check_data")
    SEND_DATA = ("send_data", "授信申请", "get_send_data")
    GET_URL = ("scene_url", "获取下载URL", "get_url_data")
    #  1-联登后首页；2-借款页面; 3-还款页面; 4-前置绑卡页; 5-下载页; 6-补充资料页，7-h5兜底地址
    GET_HOME_URL = ("scene_url", "获取联登后首页URL", "get_home_url_data")
    GET_DRAW_URL = ("scene_url", "获取借款URL", "get_draw_url_data")
    GET_REPAY_URL = ("scene_url", "获取还款URL", "get_repay_url_data")
    GET_BIND_URL = ("scene_url", "获取前置绑卡URL", "get_bind_url_data")
    GET_DOWNLOAD_URL = ("scene_url", "获取下载URL", "get_download_url_data")
    GET_SUPPLY_URL = ("scene_url", "获取补充资料URL", "get_supply_url_data")
    GET_H5_URL = ("scene_url", "获取h5兜底地址", "get_h5_url_data")
    # 还款
    REPAY_INFO = ("repay_info", "还款信息查询", "get_repay_info_data")
    # 合同
    ORDER_STATUS = ("order_status", "获取订单状态", "get_order_status_data")
    BASE_CONTRACT = ("contract", "基本信息页合同", "get_base_contract_data")
    DRAW_CONTRACT = ("contract", "确认借款页合同", "get_draw_contract_data")
    BIND_CONTRACT = ("contract", "绑卡页面合同", "get_bind_contract_data")
    LOAN_CONTRACT = ("contract", "账单页面合同", "get_loan_contract_data")
    AUTH_CONTRACT = ("contract", "授权页面合同", "get_auth_contract_data")


class FuYuanHui(HoMo):
    # 富元汇
    def __init__(self, ):
        super().__init__(channel_id="HUB_FUYUANHUI", channel_name="富元汇-富宝贷", channel_method_enum=FuYuanHuiMethodsEnum,
                         channel_uid="21113", py_code="fuyuanhui")

