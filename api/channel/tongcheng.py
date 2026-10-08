#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time
from enum import Enum

from api.channel._base_requests import BaseRequest
from utils.cryption_util import md5_encrypt
from utils.personal_util import fake, get_person_name, get_mobile_no, get_id_no


class TongChengMethodsEnum(Enum):
    # 宜享花渠道方法枚举，
    # ("渠道方法名", "方法中文名", "对应的数据模板方法")
    CHECK = ("creditAccess", "准入", "get_check_data")
    CREDIT_APPLY = ("creditApply", "授信申请", "get_credit_data")
    CREDIT_QUERY = ("creditQuery", "授信结果查询", "get_credit_query_data")
    ACCOUNT_QUERY = ("accountQuery", "额度查询", "get_account_query_data")
    QUERY_CONTRACT = ("queryContracts", "获取合同", "get_contract_data")
    GET_URL = ("getAppDownloadUrl", "获取下载URL", "get_credit_apply_data")


class TongCheng(BaseRequest):
    # 同程
    def __init__(self, ):
        super().__init__(channel_id="HUB_TONGCHENG", channel_name="同程",
                         channel_method_enum=TongChengMethodsEnum, channel_uid="22357", py_code="tongcheng")

    def get_check_data(self, data):
        # 获取准入数据
        mobile = data.get("channelMobile")
        input_id_no = data.get("channelIdNo")
        input_check_no = data.get("channelCheckNo")
        # 返回准入信息模板
        # user_name = name if name else get_person_name()
        mobile_no = mobile if mobile else get_mobile_no()
        id_no = input_id_no if input_id_no else get_id_no()
        check_no = input_check_no if input_check_no else fake.uuid4()
        check_data = {
            "requestNo":          check_no,
            "mobileMd5":          md5_encrypt(mobile_no),
            "idCardMd5":          md5_encrypt(id_no),
            "mobileAndIdCardMd5": md5_encrypt(mobile_no + id_no)
        }
        return self.data_model(TongChengMethodsEnum.CHECK.value[0], check_data)

    def get_credit_data(self, data):
        mobile = data.get("channelMobile")
        input_id_no = data.get("channelMobilechannelIdNo")
        input_check_no = data.get("channelCheckNo")
        name = data.get("channelCustName")
        channel_user_no = data.get("channelUserNo")
        channel_credit_no = data.get("channelCreditNo")

        user_name = name if name else get_person_name()
        mobile_no = mobile if mobile else get_mobile_no()
        id_no = input_id_no if input_id_no else get_id_no()

        check_no = input_check_no if input_check_no else fake.uuid4()
        base64_data = "iVBORw0KGgoAAAANSUhEUgAAAjkAAAFBCAYAAACVcr5cAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAFiUAABYlAUlSJPAAAAWZSURBVHhe7dYxEQAgEMCwB/+egQEVvWSpha7zDABAzP4FAEgxOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABBMxeXJgZ+f2mLWgAAAABJRU5ErkJggg=="

        credit_data = {
            "requestNo":        channel_credit_no,  # 授信流水号
            "prepApprovalNo":   check_no,  # 准入流水号
            "userInfo":         {
                "userIdCard": id_no,
                "mobile":     mobile_no,
                "userName":   user_name
            },
            "bankInfo":         {
                "bizMobile":  mobile_no,
                "bankCode":   "ICBC",
                "bankCardNo": "9558273491900766882",
                "bankName":   "工商银行"
            },
            "userBaseInfo":     {
                "companyCityName":         "驻马店市",
                "education":               "00",
                "annualIncome":            "210000",
                "homeCityCode":            "411700",
                "companyDistrictName":     "确山县",
                "companyName":             "韵达快运武汉分公司",
                "emergencyContactMobile1": "15836781863",
                "emergencyContactMobile2": "18858300598",
                "emergencyContact1":       "杨仕丽",
                "emergencyContact2":       "刘正友",
                "homeProvinceCode":        "410000",
                "homeDistrictName":        "确山县",
                "marriage":                "1",
                "companyProvinceCode":     "410000",
                "companyDetailAddress":    "确山县李新店镇",
                "companyMobile":           "18211700027",
                "homeCityName":            "驻马店市",
                "homeDetailAddress":       "确山县李新店镇",
                "companyProvinceName":     "河南省",
                "homeProvinceName":        "河南省",
                "companyDistrictCode":     "411725",
                "homeDistrictCode":        "411725",
                "companyCityCode":         "411700",
                "job":                     "01",
                "relation2":               "08",
                "relation1":               "06"
            },
            "userFaceInfo":     {
                "faceImgRemotePath": "http://gips3.baidu.com/it/u=3886271102,3123389489&fm=3028&app=3028&f=JPEG&fmt=auto?w=1280&h=960",
                "liveRate":          "90.0",
                "confidence":        "90.0"
            },
            "deviceInfo":       {
                "appAmt":              "0",
                "isRoot":              "0",
                "soc":                 "0.46",
                "cityId":              "192",
                "deviceId":            "18cccf670aa4a146",
                "deviceName":          "V2156FA",
                "freeRAM":             "1399404",
                "screenSize":          "1080x2216",
                "appNotifySwitch":     "1",
                "appOutVersionNumber": "10.8.0",
                "refid":               "42930908",
                "lat":                 "30.64920825864611",
                "ip":                  "223.104.122.119",
                "viewMode":            "1",
                "extend":              "4^11,5^V2156FA,6^0",
                "systemNotifySwitch":  "1",
                "systemDate":          "2024-05-29",
                "appVersionNumber":    "10.8.0",
                "pushInfo":            "v2-CQS4wWadp7s8sD6p_BeYrymnBr2LilNs4Ey6FR1dDMSTZtzbqNyq",
                "appVersionType":      "android",
                "gravityCommit":       "{\"x\":\"0.66705\",\"y\":\"7.806\",\"z\":\"5.79195\"}",
                "lon":                 "114.04291422396552",
                "systemTime":          "13:54:28",
                "navBarHeightPx":      "156",
                "cityName":            "武汉",
                "osVersion":           "11",
                "osType":              "android",
                "gravityInit":         "{\"x\":\"1.00995\",\"y\":\"7.6840506\",\"z\":\"5.754\"}",
                "colorDepth":          "32",
                "systemTimezone":      "Asia/Shanghai(GMT+8)offset28800"
            },
            "userIdentityInfo": {
                "identityFrontPhotoRemotePath": "https://img1.baidu.com/it/u=4182503233,1810287678&fm=253&fmt=auto&app=120&f=JPEG?w=417&h=292",
                "identityNo":                   id_no,
                "birthMonth":                   "1",
                "birthDay":                     "24",
                "address":                      "河南省确山县李新店乡杨湾村委涂庄",
                "nation":                       "汉",
                "birthYear":                    "1983",
                "identityBackPhotoRemotePath":  "https://bkimg.cdn.bcebos.com/pic/f9198618367adab4e40e7a8587d4b31c8601e41e",
                "sex":                          "M",
                "issuedBy":                     "确山县公安局",
                "userName":                     "涂红波",
                "validDateSection":             "2012.05.09-2032.05.09"
            }
        }
        return self.data_model(TongChengMethodsEnum.CREDIT_APPLY.value[0], credit_data)


    def get_credit_query_data(self, data):
        #授信结果查询
        channel_id = data.get("channelCreditNo")
        query_data = {
            "requestNo":  channel_id,
        }
        return self.data_model(TongChengMethodsEnum.CREDIT_QUERY.value[0], query_data)


    def get_account_query_data(self , data):
        channel_create_id = data.get("channelCreditNo")
        user_id = data.get("channelUserNo")

        query_data = {
            "requestNo": channel_create_id,
            "userId": user_id
        }
        return self.data_model(TongChengMethodsEnum.ACCOUNT_QUERY.value[0], query_data)

    def get_contract_data(self,data):
    #获取下载合同
        channel_create_id = data.get("channelCreditNo")

        query_data = {
            "requestNo": channel_create_id,
            "scene": 1
        }
        return self.data_model(TongChengMethodsEnum.QUERY_CONTRACT.value[0], query_data)

    def get_credit_apply_data(self,data):
        #获取下载链接
        channel_creaqte_id = data.get("channelCreditNo")
        query_data = {
            "requestNo" : channel_creaqte_id,
        }
        return self.data_model(TongChengMethodsEnum.GET_URL.value[0], query_data)



