#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import random
from enum import Enum

from api.channel._base_requests import BaseRequest
from api.channel.channel_api_config import ChannelMethodsEnum
from api.channel.homo import HoMo
from utils.cryption_util import md5_encrypt
from utils.personal_util import get_person_name, get_id_no, get_mobile_no


class ZhongMiMethodsEnum(Enum):
    # 渠道方法枚举，
    # ("渠道方法名", "方法中文名", "对应的数据模板方法")
    CHECK = ("check", "准入", "get_check_data")
    REGISTER = ("register", "注册", "get_register_data")
    SUBMIT_CHECK = ("submit_check", "授信前检查", "get_submit_check_data")
    SEND_DATA = ("send_data", "授信申请", "get_send_data")
    ORDER_STATUS = ("order_status", "获取订单状态", "get_order_status_data")
    CONCLUSION = ("conclusion", "额度查询", "get_conclusion_data")

    GET_HOME_URL = ("scene_url", "获取联登后首页URL", "get_home_url_data")
    # GET_DOWNLOAD_URL = ("scene_url", "获取下载URL", "get_download_url_data")
    # GET_DRAW_URL = ("scene_url", "获取借款URL", "get_draw_url_data")
    # GET_REPAY_URL = ("scene_url", "获取还款URL", "get_repay_url_data")

    BASE_CONTRACT = ("contract", "基本信息页合同", "get_base_contract_data")
    DRAW_CONTRACT = ("contract", "确认借款页合同", "get_draw_contract_data")
    BIND_CONTRACT = ("contract", "绑卡页面合同", "get_bind_contract_data")
    LOAN_CONTRACT = ("contract", "账单页面合同", "get_loan_contract_data")
    AUTH_CONTRACT = ("contract", "授权页面合同", "get_auth_contract_data")


class ZhongMi(HoMo):
    # 云宝宝
    def __init__(self, ):
        super().__init__(channel_id="HUB_ZHONGMI", channel_name="众米", channel_method_enum=ZhongMiMethodsEnum,
                         channel_uid="21127", py_code="zhongmi")

    def get_home_url_data(self, data):
        # channel_draw_no = data.get("channelDrawNo")
        channel_user_no = data.get("channelUserNo")
        # sub_no = data.get("hubSubOrderNo")

        req_data = {
            "channel_unique_id": channel_user_no,
            # "channel_loan_uid": channel_draw_no,
            # "sub_no": sub_no,
            "scene_type": "1",
            "callback_url": "https://www.baidu.com"}
        return self.data_model(ZhongMiMethodsEnum.GET_HOME_URL.value[0], req_data)
