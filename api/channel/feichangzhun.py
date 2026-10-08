#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import random
from enum import Enum

from api.channel._base_requests import BaseRequest
from api.channel.channel_api_config import ChannelMethodsEnum
from utils.cryption_util import md5_encrypt
from utils.personal_util import get_person_name, get_id_no, get_mobile_no, fake, get_bank_card


# feiChangZhunMethodMap.put("check", MethodEnum.CHECK.getCode());
# feiChangZhunMethodMap.put("send_data", MethodEnum.SEND_DATA.getCode());
# feiChangZhunMethodMap.put("scene_url", MethodEnum.SCENE_URL.getCode());
# feiChangZhunMethodMap.put("order_status", MethodEnum.ORDER_STATUS.getCode());
# feiChangZhunMethodMap.put("repay_info", MethodEnum.REPAY_INFO.getCode());


class FeiChangZhunMethodsEnum(Enum):
    # ("渠道方法名", "方法中文名", "对应的数据模板方法")
    CHECK = ("check", "准入", "get_check_data")
    CREDIT = ("send_data", "授信", "get_credit_data")
    GET_URL = ("scene_url", "获取url", "get_url_data")
    ORDER_STATUS = ("order_status", "订单状态", "get_order_status_data")
    REPAY_INFO = ("repay_info", "还款信息", "get_repay_info_data")


class FeiChangZhun(BaseRequest):
    # 非常准
    def __init__(self, ):
        super().__init__(channel_id="HUB_FEICHANGZHUN", channel_name="非常准",
                         channel_method_enum=FeiChangZhunMethodsEnum, channel_uid="20983", py_code="feichangzhun")

    @BaseRequest.non_empty(["channelMobile", "channelIdNo", "channelCustName"])
    def get_check_data(self, data):
        # 返回准入信息模板
        mobile = data.get("channelMobile")
        id_no = data.get("channelIdNo")
        name = data.get("channelCustName")

        req_data = {
            "md5_phone":       md5_encrypt(mobile),
            "md5_phone_id_no": md5_encrypt(mobile + id_no),
            "md5_id_no":       md5_encrypt(id_no),
            "pre_id_no":       id_no[:6],
            "name":            name
        }
        return self.data_model(FeiChangZhunMethodsEnum.CHECK.value[0], req_data)

    @BaseRequest.non_empty(["channelMobile", "channelBankCardNo", "channelUserNo", "channelCreditNo"])
    def get_credit_data(self, data):
        mobile = data.get("channelMobile")
        bank_card = data.get("channelBankCardNo")
        channel_user_no = data.get("channelUserNo")
        channel_credit_no = data.get("channelCreditNo")
        bank_codes = {
            "BOB":    "北京银行",
            "ICBC":   "中国工商银行",
            "ABC":    "中国农业银行",
            "CCB":    "中国建设银行",
            "BOC":    "中国银行",
            "PSBC":   "邮储银行",
            "CEB":    "光大银行",
            "PINGAN": "平安银行",
            "BCM":    "交通银行",
            "HXB":    "华夏银行",
            "CMB":    "招商银行",
            "GDB":    "广发银行",
            "CMBC":   "民生银行",
            "SPDB":   "浦发银行",
            "BOS":    "上海银行",
            "CIB":    "兴业银行",
            "ECITIC": "中信银行",
            "GCB":    "广州银行",
            "CU":     "农村信用社",
            "NBCB":   "宁波银行",
            "JSBANK": "江苏银行"
        }

        random_bank_code = random.choice(list(bank_codes.keys()))
        print("随机银行编码:", random_bank_code)
        print("对应银行名称:", bank_codes[random_bank_code])

        face_service = random.choice(["tencent", "shangtang", "ali", "ali"])
        req_data = {
            "phone":                   mobile,
            "channel_unique_id": channel_user_no,
            "channel_order_uid": channel_credit_no,
            "contact_list":      [
                {
                    "name":     get_person_name(),
                    "phone":    f"{get_mobile_no()}",
                    "relation": random.randint(1, 2)
                },
                {
                    "name":     get_person_name(),
                    "phone":    f"{get_mobile_no()}",
                    "relation": random.randint(3, 6)
                }
            ],
            "profile_dict":      {
                "request_amount":          f"{random.randint(5, 500) * 100}",
                "request_num":             f"{random.choice([3, 6, 9, 12])}个月",
                "standard_loan_purpose":   random.randint(1, 8),
                "standard_debt_situation": random.randint(1, 7),
                "standard_marriage":       random.randint(1, 4),
                "standard_job":            random.randint(1, 5),
                "employed_date":           "2021-01-01",
                "standard_education":      random.randint(1, 5),
                "address_type":            random.randint(1, 5),
                "local_hk":                random.randint(1, 4),
                "city":                    "广东省-深圳市-龙华区",
                "address":                 "上海市徐汇区云锦路东航滨江中心",
                "standard_company_nature": random.randint(1, 7),
                "standard_industry":       random.randint(1, 15),
                "company_name":            fake.company(),
                "company_phone":           "052112345678",
                "company_address":         "上海市-上海市-徐汇区",
                "company_address_detail":  fake.address().replace(" ", ""),
                "standard_income":         random.randint(1, 5),
                "bank_code":               random_bank_code,
                "card_no":                 bank_card,
                "phone":                   mobile,
                "area":                    "上海",
                "email":                   "john.doe@example.com",
            },
            "live_info":         {
                "face_service":    face_service,
                "best_face_image": "https://pic.rmb.bdstatic.com/bjh/news/5b7a02495b6cc335de55b7445a7f0545.png",
                "photo_source":    f"{random.randint(1, 3)}",
                "is_verify":       random.randint(1, 2),
                "live_data":       {
                    "face_score": "98.12345"
                }
            },
            "device_info":       {
                "duid":          "XdYE2kR6gKIDAM88syEJhcTB",
                "os":            "ios",
                "ip":            "192.139.23.68",
                "is_root":       f"{random.randint(1, 2)}",
                "mac":           "92:57:A4:8A:91:93",
                "device_model":  "iPhone X",
                "device_brand":  "Apple",
                "memory":        "4048",
                "storage":       "64000",
                "unuse_storage": "20000",
                "wifi":          f"{random.randint(1, 2)}",
                "wifi_name":     "MyWiFi",
                "battery":       "80",
                "is_simulator":  f"{random.randint(1, 2)}",
                "tele_num":      "46003",
                "android_id":    "1414018f7f456ba6",
                "os_version":    "15.0"
            },
            "longitude":         "123.456",
            "latitude":          "78.901",
            "submit":            True
        }
        return self.data_model(FeiChangZhunMethodsEnum.CREDIT.value[0], req_data)

    @BaseRequest.non_empty(["channelUserNo"])
    def get_url_data(self, data):
        channel_user_no = data.get("channelUserNo")

        # h5地址类型：联登=1、借款=2、还款=3、绑卡=4、下载=5、授信中=6
        req_data = {
            "channel_unique_id": channel_user_no,
            "scene_type":        1
        }
        return self.data_model(FeiChangZhunMethodsEnum.GET_URL.value[0], req_data)

    @BaseRequest.non_empty(["channelUserNo", "hubOrderNo", "hubSubOrderNo"])
    def get_order_status_data(self, data):
        # 订单状态
        channel_user_no = data.get("channelUserNo")
        hub_order_no = data.get("hubOrderNo") if data.get("hubOrderNo") else "HUB母订单号未填写，应取我方 channelApplyNo"
        hub_sub_order_no = data.get("hubSubOrderNo") if data.get("hubSubOrderNo") else "HUB子订单号未填写，应取我方 fundApplyNo"
        req_data = {
            "channel_unique_id": channel_user_no,
            "parent_no": hub_order_no,
            "sub_no": hub_sub_order_no
        }
        return self.data_model(FeiChangZhunMethodsEnum.ORDER_STATUS.value[0], req_data)

    @BaseRequest.non_empty(["channelDrawNo", "hubSubOrderNo"])
    def get_repay_info_data(self, data):
        channel_draw_no = data.get("channelDrawNo")
        hub_sub_order_no = data.get("hubSubOrderNo") if data.get("hubSubOrderNo") else "HUB子订单号未填写，应取我方 fundApplyNo"
        req_data = {
            "channel_loan_uid": channel_draw_no,
            "sub_no": hub_sub_order_no
        }
        return self.data_model(FeiChangZhunMethodsEnum.REPAY_INFO.value[0], req_data)


