#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import random
from enum import Enum

from api.channel._base_requests import BaseRequest
from api.channel.channel_api_config import ChannelMethodsEnum
from utils.cryption_util import md5_encrypt
from utils.personal_util import get_person_name, get_id_no, get_mobile_no


class HaoFenQiMethodsEnum(Enum):
    # 渠道方法枚举，
    # ("渠道方法名", "方法中文名", "对应的数据模板方法")
    CHECK = ("check", "准入", "get_check_data")
    REGISTER = ("register", "注册", "get_register_data")
    SUBMIT_CHECK = ("submit_check", "授信前检查", "get_submit_check_data")
    SUBMIT = ("submit", "授信申请", "get_submit_data")
    SUBMIT_RESULT = ("submit_result", "授信结果查询", "get_submit_result_data")
    # BANK_INFO = ("bank_info", "银行卡信息", "get_bank_info_data")
    # BANK_LIST = ("bank_list", "获取银行卡列表", "get_bank_list_data")
    # BIND_CARD = ("bind_card", "绑定银行卡", "get_bind_card_data")
    # BIND_VERIFY = ("bind_verify", "银行卡验证", "get_bind_verify_data")
    DRAW_URL = ("scene_url", "获取URL", "get_draw_url_data")
    REPAY_URL = ("repay_url", "还款URL", "get_repay_url_data")
    REPAY_INFO = ("repay_info", "获取还款信息", "get_repay_info_data")
    BASE_CONTRACT = ("contract", "基本信息页合同", "get_base_contract_data")
    DRAW_CONTRACT = ("contract", "确认借款页合同", "get_draw_contract_data")
    BIND_CONTRACT = ("contract", "绑卡页面合同", "get_bind_contract_data")
    LOAN_CONTRACT = ("contract", "账单页面合同", "get_loan_contract_data")
    AUTH_CONTRACT = ("contract", "授信页面合同", "get_auth_contract_data")
    USER_CONTRACT = ("contract", "用户隐私协议", "get_user_contract_data")


class HaoFenQi(BaseRequest):
    # 好分期
    def __init__(self, ):
        super().__init__(channel_id="HUB_HAOFENQI", channel_name="好分期",
                         channel_method_enum=HaoFenQiMethodsEnum, channel_uid="20512", py_code="haofenqi")

    def get_check_data(self, data):
        # 返回准入信息模板
        mobile = data.get("channelMobile")
        id_no = data.get("channelIdNo")
        name = data.get("channelCustName")
        req_data = {
            "md5_phone":       md5_encrypt(mobile),
            "md5_id_no":       md5_encrypt(id_no),
            "md5_phone_id_no": md5_encrypt(mobile + id_no),
            "name":             name,
        }
        return self.data_model(HaoFenQiMethodsEnum.CHECK.value[0], req_data)

    def get_register_data(self, data):
        """
        获取注册信息模板
        :param data:
        :return:
        """

        mobile = data.get("channelMobile")
        id_no = data.get("channelIdNo")
        name = data.get("channelCustName")
        register_data = {
            "phone": mobile,
            "id_no": id_no,
            "name": name,
            "id_card_front": "https://img-operation.csdnimg.cn/csdn/silkroad/img/1699871630383.jpg",
            "id_card_back": "https://img-operation.csdnimg.cn/csdn/silkroad/img/1699871630383.jpg",
            "ip": "192.133.12.31",
            "race": "汉族",
            "issued_by": "公安局",
            "valid_date": "2018.12.31-2028.12.31",
            "address": "北京市",
            "longitude": "116.4074",
            "latitude": "39.9042",
            "os": "Android"
            }
        return self.data_model(HaoFenQiMethodsEnum.REGISTER.value[0], register_data)

    def get_submit_check_data(self, data):
        # 进件资格检查
        hub_user_id = data.get("hubUserId")
        return self.data_model(HaoFenQiMethodsEnum.SUBMIT_CHECK.value[0], {"user_id": hub_user_id})

    def get_submit_data(self, data):
        mobile = data.get("channelMobile")
        bank_card = data.get("channelBankCardNo")
        channel_user_no = data.get("channelUserNo")
        channel_credit_no = data.get("channelCreditNo")
        hub_user_id = data.get("hubUserId")
        data = {
            "hfq_order": channel_credit_no,
            "user_id": hub_user_id,
            "profile_dict": {
                "phone": mobile,
                "card_no": bank_card,
                "address": "徐汇区云锦路111号",
                "address_type": "租房",
                "city": "上海市-上海市-徐汇区",
                "company_address": "上海市-上海市-徐汇区",
                "company_address_detail": "徐汇区云锦路222号",
                "company_name": "上海徐汇房产有限公司",
                "local_hk": "外地城市户口",
                "request_amount": "20000",
                "request_num": "12个月",
                "standard_company_nature": "普通民营企业",
                "standard_education": "大学本科",
                "standard_income": "10000-30000",
                "standard_industry": "房地产",
                "standard_job": "上班",
                "standard_loan_purpose": "购物",
                "standard_marriage": "未婚"
            },
            "contact_list": [{
                "name": "张三",
                "phone": "13888888888",
                "relation": "朋友"
            }, {
                "name": "李四",
                "phone": "13888888889",
                "relation": "朋友"
            }],
            "device_info": {
                "ip": "112.224.194.160",
                "os": "android"
            },
            "live_info": {
                "best_face_image": "https://img-operation.csdnimg.cn/csdn/silkroad/img/1699871630383.jpg",
                "face_service": "kuangshi",
                "live_data": {
                    "face_score": "100.00000"
                }
            },
            "latitude": "36.072829",
            "longitude": "120.435007",
        }
        return self.data_model(HaoFenQiMethodsEnum.SUBMIT.value[0], data)

    def get_submit_result_data(self, data):
        hub_user_id = data.get("hubUserId")
        hub_order_no = data.get("hubOrderNo")
        req_data = {
            "order_no": hub_order_no,
            "user_id": hub_user_id
        }
        return self.data_model(HaoFenQiMethodsEnum.SUBMIT_RESULT.value[0], req_data)

    @staticmethod
    def get_h5_url(user_id, scene_type, callback_url="http://www.baidu.com"):
        # 获取跳转url
        # scene_type 1.借款页面 2.还款页面
        data = {
            "user_id": user_id,
            "scene_type":        scene_type,
            "redirect_url":   callback_url
        }
        return data

    def get_draw_url_data(self, data):
        hub_user_id = data.get("hubUserId")
        req_data = self.get_h5_url(hub_user_id, 1)
        return self.data_model(HaoFenQiMethodsEnum.DRAW_URL.value[0], req_data)

    def get_repay_url_data(self, data):
        hub_user_id = data.get("hubUserId")
        req_data = self.get_h5_url(hub_user_id, 2)
        return self.data_model(HaoFenQiMethodsEnum.REPAY_URL.value[0], req_data)

    def get_repay_info_data(self, data):
        hub_order_no = data.get("hubOrderNo")
        req_data = {
            "order_no": hub_order_no,
        }
        return self.data_model(HaoFenQiMethodsEnum.REPAY_INFO.value[0], req_data)

    # def get_bank_info_data(self, data):
    #     hub_user_id = data.get("hubUserId")
    #     req_data = {
    #         "user_id": hub_user_id
    #     }
    #     return self.data_model(HaoFenQiMethodsEnum.BANK_INFO.value[0], req_data)
    #
    # def get_bank_list_data(self, data):
    #     hub_user_id = data.get("hubUserId")
    #     req_data = {
    #         "user_id": hub_user_id
    #     }
    #     return self.data_model(HaoFenQiMethodsEnum.BANK_LIST.value[0], req_data)
    #
    # def get_bind_card_data(self, data):
    #     return self.data_model(HaoFenQiMethodsEnum.BIND_CARD.value[0], {})


    @staticmethod
    def get_contract_data(data, contract_type):
        channel_user_no = data.get("channelUserNo", f"default_value_{random.randint(1, 1000)}")
        contract_data = {
            "user_id": channel_user_no,
            "contract_name": contract_type
        }
        return contract_data

    def get_base_contract_data(self, data):
        req_data = self.get_contract_data(data, 1)
        return self.data_model(HaoFenQiMethodsEnum.BASE_CONTRACT.value[0], req_data)

    def get_draw_contract_data(self, data):
        req_data = self.get_contract_data(data, 2)
        return self.data_model(HaoFenQiMethodsEnum.DRAW_CONTRACT.value[0], req_data)

    def get_bind_contract_data(self, data):
        req_data = self.get_contract_data(data, 3)
        return self.data_model(HaoFenQiMethodsEnum.BIND_CONTRACT.value[0], req_data)

    def get_loan_contract_data(self, data):
        req_data = self.get_contract_data(data, 4)
        return self.data_model(HaoFenQiMethodsEnum.LOAN_CONTRACT.value[0], req_data)

    def get_auth_contract_data(self, data):
        req_data = self.get_contract_data(data, 5)
        return self.data_model(HaoFenQiMethodsEnum.AUTH_CONTRACT.value[0], req_data)

    def get_user_contract_data(self, data):
        req_data = self.get_contract_data(data, 6)
        return self.data_model(HaoFenQiMethodsEnum.AUTH_CONTRACT.value[0], req_data)