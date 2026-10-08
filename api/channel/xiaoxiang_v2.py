#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from enum import Enum

from api.channel._base_requests import BaseRequest
from utils.cryption_util import md5_encrypt
from utils.personal_util import get_person_name, get_mobile_no


# xiaoXiangV2MethodMap.put("check", MethodEnum.CHECK.getCode());
# xiaoXiangV2MethodMap.put("submit", MethodEnum.SUBMIT.getCode());
# xiaoXiangV2MethodMap.put("scene_url", MethodEnum.SCENE_URL.getCode());
# xiaoXiangV2MethodMap.put("conclusion", MethodEnum.CONCLUSION.getCode());
# xiaoXiangV2MethodMap.put("fund_result", MethodEnum.FUNDED_RESULT.getCode());
# xiaoXiangV2MethodMap.put("repay_info", MethodEnum.REPAY_INFO.getCode());


class XiaoXiangV2MethodsEnum(Enum):
    # ("渠道方法名", "方法中文名", "对应的数据模板方法")
    CHECK = ("check", "准入", "get_check_data")
    CREDIT = ("submit", "授信", "get_credit_data")
    CREDIT_RESULT = ("conclusion", "授信结果", "get_credit_result_data")
    GET_URL = ("scene_url", "获取首页url", "get_url_data")
    DRAW_RESULT = ("fund_result", "放款结果", "get_draw_result_data")
    REPAY_INFO = ("repay_info", "还款信息", "get_repay_info_data")


class XiaoXiangV2(BaseRequest):
    # 玖富v2
    def __init__(self, ):
        super().__init__(channel_id="HUB_XIAOXIANG_V2", channel_name="小象V2",
                         channel_method_enum=XiaoXiangV2MethodsEnum, channel_uid="20541", py_code="xiaoxiang_v2")

    def get_check_data(self, data):
        # 返回准入信息模板
        mobile = data.get("channelMobile")
        id_no = data.get("channelIdNo")
        name = data.get("channelCustName")

        req_data = {
            "phoneMD5":    md5_encrypt(mobile),
            "cidPhoneMD5": md5_encrypt(mobile + id_no),
            "cidMD5":      md5_encrypt(id_no),
            "cidUp6":      id_no[:6],
            "name":        name
        }
        return self.data_model(XiaoXiangV2MethodsEnum.CHECK.value[0], req_data)

    def get_credit_data(self, data):
        mobile = data.get("channelMobile")
        id_no = data.get("channelIdNo")
        name = data.get("channelCustName")

        req_data = {
            "userId":         123456,
            "agentName":      "小象",
            "basicInfo":      {
                "phone":             mobile,
                "companyAddress":    "广东省佛山市南海市XXXXXX",
                "companyCity":       "佛山市",
                "companyCityId":     "4406",
                "companyDistrict":   "南海市",
                "companyDistrictId": "440682",
                "companyName":       "佛山市恒瑞交通发展有限公司",
                "companyProvince":   "广东省",
                "companyProvinceId": "44",
                "degree":            "30003",
                "houseAddress":      "广东省佛山市南海市XXXXXX",
                "houseCity":         "佛山市",
                "houseCityId":       "4406",
                "houseDistrict":     "南海市",
                "houseDistrictId":   "440682",
                "houseProvince":     "广东省",
                "houseProvinceId":   "44",
                "marriage":          "50001",
            },
            "idInfo":         {
                "address":             "广东省佛山市南海市XXXXXX",
                "cid":                 id_no,
                "gender":              1,
                "issuedBy":            "佛山市公安局南海分局",
                "name":                name,
                "nation":              "汉",
                "validEndDate":        "2033.11.27",
                "validStartDate":      "2013.11.27",
                "verifiedIdBackPath":  "https://lmg.jj20.com/up/allimg/tp08/24041224115258-lp.jpg",
                "verifiedIdFrontPath": "https://lmg.jj20.com/up/allimg/tp08/24041224115258-lp.jpg"
            },
            "livingInfo":     {
                "checkScore": "99.99",
                "natureFile": "https://lmg.jj20.com/up/allimg/tp08/24041224115258-lp.jpg"
            },
            "supplementInfo": {
                "income":     "40005",
                "industry":   "10017",
                "occupation": "20008"
            },
            "contactInfo":    [
                {
                    "name":     get_person_name(),
                    "phone":    get_mobile_no(),
                    "relation": "80001",
                    "sort":     1
                },
                {
                    "name":     get_person_name(),
                    "phone":    get_mobile_no(),
                    "relation": "80001",
                    "sort":     1
                }
            ],
            "deviceInfo":     {
                "androidId":         "",
                "gps":               {
                    "x": 123.232,
                    "y": 76.232
                },
                "hasRoot":           "",
                "idfa":              "",
                "idfv":              "",
                "imei":              "",
                "imsi":              "",
                "ip":                "",
                "isIos":             False,
                "isJailBreak":       False,
                "isSimulator":       "",
                "mobileNetworkType": "",
                "model":             "",
                "networkOperator":   "",
                "networkType":       "",
                "oAID":              "",
                "osVersion":         "",
                "sim":               "",
                "totalMemory":       "",
                "totalStorage":      "",
                "usingNetMac":       ""
            },
        }
        return self.data_model(XiaoXiangV2MethodsEnum.CREDIT.value[0], req_data)

    def get_credit_result_data(self, data):
        channel_user_no = data.get("channelUserNo")
        req_data = {
            "userId": channel_user_no
        }
        return self.data_model(XiaoXiangV2MethodsEnum.CREDIT_RESULT.value[0], req_data)

    def get_url_data(self, data):
        mobile = data.get("channelMobile")
        req_data = {
            "phone": mobile,
            "sceneType": 1
        }
        return self.data_model(XiaoXiangV2MethodsEnum.GET_URL.value[0], req_data)

    def get_draw_result_data(self, data):
        channel_user_no = data.get("channelUserNo")
        channel_draw_no = data.get("channelDrawNo")

        req_data = {
            "userId": channel_user_no,
            "loanId": channel_draw_no
        }
        return self.data_model(XiaoXiangV2MethodsEnum.DRAW_RESULT.value[0], req_data)

    def get_repay_info_data(self, data):
        channel_user_no = data.get("channelUserNo")
        channel_draw_no = data.get("channelDrawNo")

        req_data = {
            "userId": channel_user_no,
            "loanId": channel_draw_no
        }
        return self.data_model(XiaoXiangV2MethodsEnum.REPAY_INFO.value[0], req_data)
