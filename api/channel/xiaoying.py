#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from enum import Enum

from api.channel._base_requests import BaseRequest
from api.channel.channel_api_config import ChannelMethodsEnum
from utils.cryption_util import md5_encrypt
from utils.personal_util import get_person_name, get_id_no, get_mobile_no

# Map < String, String > xiaoYingMethodMap = new HashMap <> ();
# xiaoYingMethodMap.put("queryRepay", MethodEnum.REPAY_INFO.getCode());
# xiaoYingMethodMap.put("getRepayUrl", MethodEnum.REPAY.getCode());
# xiaoYingMethodMap.put("orderStatusQuery", MethodEnum.STATUS.getCode());
# channelMethodMappingMap.put(ChannelEnum.XIAO_YING.getCode(), xiaoYingMethodMap);


class XiaoYingMethodsEnum(Enum):
    # 渠道方法枚举，
    # ("渠道方法名", "方法中文名", "对应的数据模板方法")
    CHECK = ("check", "准入", "get_check_data")
    # QUERY_REPAY = ("queryRepay", "还款信息", "get_repay_info_data")
    GET_REPAY_URL = ("getRepayUrl", "还款", "get_repay_data")
    # ORDER_STATUS = ("orderStatusQuery", "订单状态", "get_order_status_data")


class XiaoYing(BaseRequest):
    # 小赢
    def __init__(self, ):
        super().__init__(channel_id="XiaoYing", channel_name="小赢", channel_method_enum=XiaoYingMethodsEnum,
                         channel_uid="20389", py_code="xiaoying")

    @BaseRequest.non_empty(["channelMobile", "channelIdNo", "channelCustName"])
    def get_check_data(self, data):
        # 返回准入信息模板
        mobile_no = data.get("channelMobile")
        id_no = data.get("channelIdNo")
        name = data.get("channelCustName")
        req_data = {
            "mobileMd5":       md5_encrypt(mobile_no),
            "mobileIdentityMd5": md5_encrypt(mobile_no + id_no),
            "identityMd5":       md5_encrypt(id_no),
            "identityTop6":       id_no[:6],
            "name":            name
        }
        return self.data_model(XiaoYingMethodsEnum.CHECK.value[0], req_data)

    @BaseRequest.non_empty(["hubOrderNo"])
    def get_repay_data(self, data):
        hub_order_no = data.get("hubOrderNo")
        req_data = {
            "loanOrderId":  hub_order_no,
            "redirectUrl": "baidu.com"
        }
        return self.data_model(XiaoYingMethodsEnum.GET_REPAY_URL.value[0], req_data)