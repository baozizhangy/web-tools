#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import random
from enum import Enum

from api.channel._base_requests import BaseRequest
from api.channel.channel_api_config import ChannelMethodsEnum
from utils.cryption_util import md5_encrypt
from utils.personal_util import get_person_name, get_id_no, get_mobile_no

# 2407 homo 新增接口
# homoMethodMap.put("trial", MethodEnum.TRIAL.getCode());
# homoMethodMap.put("drawSubmit", MethodEnum.CONFIRM_ORDER.getCode());
# homoMethodMap.put("reSend", MethodEnum.CONFIRM_CODE.getCode());
# homoMethodMap.put("verifyCode", MethodEnum.CONFIRM_VCODE.getCode());
# homoMethodMap.put("bank_list", MethodEnum.BANK_LIST.getCode());
# homoMethodMap.put("bind_list", MethodEnum.BIND_LIST.getCode());
# homoMethodMap.put("bind_card", MethodEnum.BIND_CARD.getCode());
# homoMethodMap.put("bind_verify", MethodEnum.BIND_VERIFY.getCode());


class HoMoMethodsEnum(Enum):
    # homo相关渠道方法枚举，
    # ("渠道方法名", "方法中文名", "对应的数据模板方法")
    CHECK = ("check", "准入", "get_check_data")
    REGISTER = ("register", "注册", "get_register_data")
    SUBMIT_CHECK = ("submit_check", "授信前检查", "get_submit_check_data")
    SEND_DATA = ("send_data", "授信申请", "get_send_data")
    ORDER_STATUS = ("order_status", "获取订单状态", "get_order_status_data")
    CONCLUSION = ("conclusion", "授信结果/额度", "get_conclusion_data")
    # GET_URL = ("scene_url", "获取下载URL", "get_url_data")
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
    BASE_CONTRACT = ("contract", "基本信息页合同", "get_base_contract_data")
    DRAW_CONTRACT = ("contract", "确认借款页合同", "get_draw_contract_data")
    BIND_CONTRACT = ("contract", "绑卡页面合同", "get_bind_contract_data")
    LOAN_CONTRACT = ("contract", "账单页面合同", "get_loan_contract_data")
    AUTH_CONTRACT = ("contract", "授权页面合同", "get_auth_contract_data")
    # 2407 新增接口
    TRIAL = ("trial", "借款试算", "get_trial_data")
    DRAW_SUBMIT = ("drawSubmit", "借款提交", "get_draw_submit_data")
    CONFIRM_CODE = ("reSend", "发送借款验证码", "get_re_send_data")
    DRAW_VERIFY = ("verifyCode", "借款验证", "get_verify_code_data")
    # 银行卡
    BANK_LIST = ("bank_list", "支持的银行卡列表", "get_bank_list_data")
    BIND_LIST = ("bind_list", "已绑卡列表", "get_bind_list_data")
    BIND_CARD = ("bind_card", "绑卡提交", "get_bind_card_data")
    BIND_VERIFY = ("bind_verify", "绑卡验证", "get_bind_verify_data")


class HoMo(BaseRequest):
    # 云宝宝
    def __init__(self, channel_id="HUB_HoMo", channel_name="homo渠道", channel_method_enum=HoMoMethodsEnum,
                 channel_uid=None, py_code="homo"):
        super().__init__(channel_id, channel_name, channel_method_enum, channel_uid, py_code)

    @BaseRequest.non_empty(["channelMobile", "channelIdNo", "channelCustName"])
    def get_check_data(self, data):
        # 返回准入信息模板
        mobile_no = data.get("channelMobile")
        id_no = data.get("channelIdNo")
        name = data.get("channelCustName")

        check_data = {
            "md5_phone":       md5_encrypt(mobile_no),
            "md5_phone_id_no": md5_encrypt(mobile_no + id_no),
            "md5_id_no":       md5_encrypt(id_no),
            "pre_id_no":       id_no[:6],
            "name":            name
        }
        return self.data_model(HoMoMethodsEnum.CHECK.value[0], check_data)

    @BaseRequest.non_empty(["channelMobile", "channelIdNo", "channelCustName", "channelUserNo"])
    def get_register_data(self, data):
        # 返回注册信息模板
        mobile = data.get("channelMobile")
        input_id_no = data.get("channelIdNo")
        name = data.get("channelCustName")
        channel_user_no = data.get("channelUserNo")
        req_data = {
            "address":           "上海市浦东新区北汽真65弄",
            "valid_date":        "2017.04.06-2037.04.06",
            "channel_unique_id": channel_user_no,
            "name":              name,
            "issued_by":         "苏州市公安局",
            "id_card_front":     "https://pic.rmb.bdstatic.com/bjh/news/5b7a02495b6cc335de55b7445a7f0545.png",
            "id_card_back":      "https://pic.rmb.bdstatic.com/bjh/news/5b7a02495b6cc335de55b7445a7f0545.png",
            "phone":             mobile,
            "os":                "android",
            "id_no":             input_id_no,
            "ip":           "39.128.44.138",
            "race":              "侗"
        }
        return self.data_model(HoMoMethodsEnum.REGISTER.value[0], req_data)

    @BaseRequest.non_empty(["channelUserNo"])
    def get_submit_check_data(self, data):
        # 返回授信前检查信息模板
        channel_user_no = data.get("channelUserNo")
        req_data = {"channel_unique_id": channel_user_no}
        return self.data_model(HoMoMethodsEnum.SUBMIT_CHECK.value[0], req_data)

    @BaseRequest.non_empty(["channelUserNo", "channelCreditNo"])
    def get_send_data(self, data):
        # 返回授信申请信息模板
        channel_user_no = data.get("channelUserNo")
        channel_credit_no = data.get("channelCreditNo")
        req_data = {
            "channel_unique_id": channel_user_no,
            "channel_order_uid": channel_credit_no,
            "submit":            True,
            "contact_list":      [
                {
                    "name":     get_person_name(),
                    "phone":    get_mobile_no(),
                    "relation": 1
                },
                {
                    "name":     get_person_name(),
                    "phone":    get_mobile_no(),
                    "relation": 2
                }
            ],
            "profile_dict":      {
                "standard_loan_purpose":   1,
                "standard_debt_situation": 1,
                "employed_date":           "2023-11-08",
                "standard_education":      1,
                "standard_company_nature": 5,
                "local_hk":                1,
                "standard_job":            1,
                "company_name":            "公司名称地址",
                "company_phone":           "02139382723",
                "company_address":         "上海市-上海市-徐汇区",
                "company_address_detail":  "上海市徐汇区云锦路东航滨江中心T1-1701",
                "address_type":            1,
                "standard_industry":       1,
                "standard_marriage":       2,
                "standard_income":         1,
                "city":                    "安徽省-合肥市-瑶海区",
                "address":                 "亭湖区天山路东方绿苑"
            },
            "live_info":         {
                "face_service":    "kuangshi",
                "best_face_image": "https://pic.rmb.bdstatic.com/bjh/news/5b7a02495b6cc335de55b7445a7f0545.png",
                "photo_source":    "kuangshi",
                "is_verify":       "2",
                "live_data":       {
                    "face_score": 80
                }
            },
            "device_info":       {
                "os":            "android",
                "ip":            "182.23.12.32",
                "duid":          "EJIEIMFKEFMIEFEF",
                "is_root":       0,
                "mac":           "FEEG-WEFF-FERG-WEFG",
                "device_model":  "vivo X21A",
                "device_brand":  "iphone",
                "memory":        9874.34,
                "storage":       155874.34,
                "unuse_storage": 5874.34,
                "wifi":          0,
                "wifi_name":     "xurong",
                "bettary":       63,
                "is_simulator":  1,
                "tele_num":      "46003",
                "android_id":    "android",
                "os_version":    "12.9"
            }
        }
        return self.data_model(HoMoMethodsEnum.SEND_DATA.value[0], req_data)

    @BaseRequest.non_empty(["channelUserNo", "channelCreditNo"])
    def get_conclusion_data(self, data):
        order_no = data.get("hubOrderNo")
        sub_order_no = data.get("hubSubOrderNo")
        channel_user_no = data.get("channelUserNo")
        channel_credit_no = data.get("channelCreditNo")
        req_data = {
            "sub_no": sub_order_no,  # 我方子订单号
            "parent_no": order_no,  # 乐享借的母订单号
            "channel_unique_id": channel_user_no,
            "channel_order_uid": channel_credit_no,
        }
        return self.data_model(HoMoMethodsEnum.CONCLUSION.value[0], req_data)

    @BaseRequest.non_empty(["hubOrderNo", "hubSubOrderNo", "channelUserNo"])
    def get_bank_list_data(self, data):
        order_no = data.get("hubOrderNo")
        sub_order_no = data.get("hubSubOrderNo")
        channel_user_no = data.get("channelUserNo")
        req_data = {
            "sub_no": sub_order_no,  # 我方子订单号
            "parent_no": order_no,  # 乐享借的母订单号
            "channel_unique_id": channel_user_no,
        }
        return self.data_model(HoMoMethodsEnum.BANK_LIST.value[0], req_data)

    @BaseRequest.non_empty(["hubOrderNo", "hubSubOrderNo", "channelUserNo"])
    def get_bind_list_data(self, data):
        order_no = data.get("hubOrderNo")
        sub_order_no = data.get("hubSubOrderNo")
        channel_user_no = data.get("channelUserNo")
        req_data = {
            "sub_no": sub_order_no,  # 我方子订单号
            "parent_no": order_no,  # 乐享借的母订单号
            "channel_unique_id": channel_user_no,
        }
        return self.data_model(HoMoMethodsEnum.BIND_LIST.value[0], req_data)

    @BaseRequest.non_empty(["hubOrderNo", "hubSubOrderNo", "channelUserNo", "channelMobile", "channelBankCardNo"])
    def get_bind_card_data(self, data):
        order_no = data.get("hubOrderNo")
        sub_order_no = data.get("hubSubOrderNo")
        channel_user_no = data.get("channelUserNo")
        mobile = data.get("channelMobile")
        bank_card = data.get("channelBankCardNo")

        req_data = {
            "sub_no": sub_order_no,  # 我方子订单号
            "parent_no": order_no,  # 乐享借的母订单号
            "channel_unique_id": channel_user_no,
            "mobile_no": mobile,
            "card_no": bank_card,
            "bank_code": "0003",
            "bank_name": "工商银行",
        }
        return self.data_model(HoMoMethodsEnum.BIND_CARD.value[0], req_data)

    @BaseRequest.non_empty(["hubOrderNo", "hubSubOrderNo", "channelUserNo", "hubBindCardSerialNo"])
    def get_bind_verify_data(self, data):
        order_no = data.get("hubOrderNo")
        sub_order_no = data.get("hubSubOrderNo")
        channel_user_no = data.get("channelUserNo")
        bind_serial_no = data.get("hubBindCardSerialNo")

        req_data = {
            "sub_no": sub_order_no,  # 我方子订单号
            "parent_no": order_no,  # 乐享借的母订单号
            "channel_unique_id": channel_user_no,
            "bind_serial_no": bind_serial_no,
            "verify_code": "123456",
        }
        return self.data_model(HoMoMethodsEnum.BIND_VERIFY.value[0], req_data)

    @BaseRequest.non_empty(["hubOrderNo", "hubSubOrderNo", "channelUserNo", "channelCreditNo"])
    def get_trial_data(self, data):
        order_no = data.get("hubOrderNo")
        sub_order_no = data.get("hubSubOrderNo")
        channel_user_no = data.get("channelUserNo")
        channel_credit_no = data.get("channelCreditNo")
        req_data = {
            "sub_no": sub_order_no,  # 我方子订单号
            "parent_no": order_no,  # 乐享借的母订单号
            "channel_unique_id": channel_user_no,
            "channel_order_uid": channel_credit_no,
            "trial_amt": 300000,
            "loan_term": 12
        }
        return self.data_model(HoMoMethodsEnum.TRIAL.value[0], req_data)

    @BaseRequest.non_empty(["hubOrderNo", "hubSubOrderNo", "hubBindCardSerialNo", "channelDrawNo"])
    def get_draw_submit_data(self, data):
        order_no = data.get("hubOrderNo")
        bind_card_id = data.get("hubBindRelationId")
        sub_order_no = data.get("hubSubOrderNo")
        channel_draw_no = data.get("channelDrawNo")
        req_data = {
            "sub_no": sub_order_no,  # 我方子订单号
            "parent_no": order_no,  # 乐享借的母订单号
            "channel_loan_id": channel_draw_no,
            "loan_amt": 300000,
            "loan_term": 12,
            "bind_relation_id": bind_card_id
        }
        return self.data_model(HoMoMethodsEnum.DRAW_SUBMIT.value[0], req_data)

    @BaseRequest.non_empty(["hubOrderNo", "hubSubOrderNo", "channelDrawNo"])
    def get_re_send_data(self, data):
        order_no = data.get("hubOrderNo")
        sub_order_no = data.get("hubSubOrderNo")
        channel_draw_no = data.get("channelDrawNo")
        req_data = {
            "sub_no": sub_order_no,  # 我方子订单号
            "parent_no": order_no,  # 乐享借的母订单号
            "channel_loan_id": channel_draw_no,
        }
        return self.data_model(HoMoMethodsEnum.CONFIRM_CODE.value[0], req_data)

    @BaseRequest.non_empty(["hubOrderNo", "hubSubOrderNo", "channelDrawNo"])
    def get_verify_code_data(self, data):
        order_no = data.get("hubOrderNo")
        sub_order_no = data.get("hubSubOrderNo")
        channel_draw_no = data.get("channelDrawNo")
        req_data = {
            "sub_no": sub_order_no,  # 我方子订单号
            "parent_no": order_no,  # 乐享借的母订单号
            "channel_loan_id": channel_draw_no,
            "sms_code": "123456",
            "serial_number": "2024010101",
        }
        return self.data_model(HoMoMethodsEnum.DRAW_VERIFY.value[0], req_data)

    @staticmethod
    def get_url_data(data, scene_type):
        channel_draw_no = data.get("channelDrawNo")
        channel_user_no = data.get("channelUserNo")
        sub_no = data.get("hubSubOrderNo")

        url_data = {
            "channel_unique_id": channel_user_no,
            "channel_loan_uid": channel_draw_no,
            "sub_no": sub_no,
            "scene_type": scene_type,
            "callback_url": "https://www.baidu.com"}
        return url_data

    @BaseRequest.non_empty(["channelDrawNo", "channelUserNo", "hubSubOrderNo"])
    def get_home_url_data(self, data):
        req_data = self.get_url_data(data, 1)
        return self.data_model(HoMoMethodsEnum.GET_HOME_URL.value[0], req_data)

    @BaseRequest.non_empty(["channelDrawNo", "channelUserNo", "hubSubOrderNo"])
    def get_draw_url_data(self, data):
        req_data = self.get_url_data(data, 2)
        return self.data_model(HoMoMethodsEnum.GET_DRAW_URL.value[0], req_data)

    @BaseRequest.non_empty(["channelDrawNo", "channelUserNo", "hubSubOrderNo"])
    def get_repay_url_data(self, data):
        req_data = self.get_url_data(data, 3)
        return self.data_model(HoMoMethodsEnum.GET_REPAY_URL.value[0], req_data)

    @BaseRequest.non_empty(["channelDrawNo", "channelUserNo", "hubSubOrderNo"])
    def get_bind_url_data(self, data):
        req_data = self.get_url_data(data, 4)
        return self.data_model(HoMoMethodsEnum.GET_BIND_URL.value[0], req_data)

    @BaseRequest.non_empty(["channelDrawNo", "channelUserNo", "hubSubOrderNo"])
    def get_download_url_data(self, data):
        req_data = self.get_url_data(data, 5)
        return self.data_model(HoMoMethodsEnum.GET_DOWNLOAD_URL.value[0], req_data)

    @BaseRequest.non_empty(["channelDrawNo", "channelUserNo", "hubSubOrderNo"])
    def get_supply_url_data(self, data):
        req_data = self.get_url_data(data, 6)
        return self.data_model(HoMoMethodsEnum.GET_SUPPLY_URL.value[0], req_data)

    @BaseRequest.non_empty(["channelDrawNo", "channelUserNo", "hubSubOrderNo"])
    def get_h5_url_data(self, data):
        req_data = self.get_url_data(data, 7)
        return self.data_model(HoMoMethodsEnum.GET_H5_URL.value[0], req_data)

    @BaseRequest.non_empty(["channelDrawNo", "hubOrderNo"])
    def get_order_status_data(self, data):
        order_no = data.get("hubOrderNo")
        sub_order_no = data.get("hubSubOrderNo")
        channel_draw_no = data.get("channelDrawNo")
        req_data = {
            "sub_no": sub_order_no,  # 我方子订单号
            "parent_no": order_no,  # 乐享借的母订单号
            "channel_loan_uid": channel_draw_no,
        }
        return self.data_model(HoMoMethodsEnum.ORDER_STATUS.value[0], req_data)

    @BaseRequest.non_empty(["channelDrawNo", "hubSubOrderNo"])
    def get_repay_info_data(self, data):
        sub_order_no = data.get("hubSubOrderNo")
        channel_draw_no = data.get("channelDrawNo")
        req_data = {
            "sub_no": sub_order_no,  # 我方子订单号
            "channel_loan_uid": channel_draw_no,
        }
        return self.data_model(HoMoMethodsEnum.REPAY_INFO.value[0], req_data)

    @staticmethod
    def get_contract_data(data, contract_type):
        channel_user_no = data.get("channelUserNo")
        sub_no = data.get("hubSubOrderNo")
        contract_data = {
            "channel_unique_id": channel_user_no,
            "sub_no": sub_no,
            "contract_type": contract_type
        }
        return contract_data

    @BaseRequest.non_empty(["channelUserNo", "hubSubOrderNo"])
    def get_base_contract_data(self, data):
        req_data = self.get_contract_data(data, 1)
        return self.data_model(HoMoMethodsEnum.BASE_CONTRACT.value[0], req_data)

    @BaseRequest.non_empty(["channelUserNo", "hubSubOrderNo"])
    def get_draw_contract_data(self, data):
        req_data = self.get_contract_data(data, 2)
        return self.data_model(HoMoMethodsEnum.DRAW_CONTRACT.value[0], req_data)

    @BaseRequest.non_empty(["channelUserNo", "hubSubOrderNo"])
    def get_bind_contract_data(self, data):
        req_data = self.get_contract_data(data, 3)
        return self.data_model(HoMoMethodsEnum.BIND_CONTRACT.value[0], req_data)

    @BaseRequest.non_empty(["channelUserNo", "hubSubOrderNo"])
    def get_loan_contract_data(self, data):
        req_data = self.get_contract_data(data, 4)
        return self.data_model(HoMoMethodsEnum.LOAN_CONTRACT.value[0], req_data)

    @BaseRequest.non_empty(["channelUserNo", "hubSubOrderNo"])
    def get_auth_contract_data(self, data):
        req_data = self.get_contract_data(data, 5)
        return self.data_model(HoMoMethodsEnum.AUTH_CONTRACT.value[0], req_data)
