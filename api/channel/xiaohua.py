#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import random
from enum import Enum

from api.channel._base_requests import BaseRequest
from api.channel.channel_api_config import ChannelMethodsEnum
from utils.cryption_util import md5_encrypt
from utils.personal_util import get_person_name, get_id_no, get_mobile_no


# xiaoHuaMethodMap.put("check", MethodEnum.CHECK.getCode());
# xiaoHuaMethodMap.put("grantCredit", MethodEnum.SEND_DATA.getCode());
# xiaoHuaMethodMap.put("getScenceUrl", MethodEnum.SCENE_URL.getCode());
# xiaoHuaMethodMap.put("bindCardExt", MethodEnum.LOGIN_URL.getCode());
# xiaoHuaMethodMap.put("applyAmount", MethodEnum.CONFIRM_URL.getCode());
# xiaoHuaMethodMap.put("getLoanInfo", MethodEnum.LOAN_INFO.getCode());
# xiaoHuaMethodMap.put("getRepayPlan", MethodEnum.REPAY_INFO.getCode());
# xiaoHuaMethodMap.put("getContract", MethodEnum.CONTRACT.getCode());
# xiaoHuaMethodMap.put("getCreditInfo", MethodEnum.CONCLUSION.getCode());


class XiaoHuaMethodsEnum(Enum):
    # homo相关渠道方法枚举，
    # ("渠道方法名", "方法中文名", "对应的数据模板方法")
    CHECK = ("check", "准入", "get_check_data")
    CREDIT = ("grantCredit", "授信", "get_credit_data")
    CONCLUSION = ("getCreditInfo", "查询授信结果", "get_conclusion_data")
    # BIND_CARD = ("bindCardExt", "绑卡", "bind_card")  # 未使用
    DRAW_URL = ("applyAmount", "获取借款URL", "get_draw_url")
    LOAN_INFO = ("getLoanInfo", "借款结果", "get_loan_info")
    # REPAY_INFO = ("getRepayPlan", "还款计划", "get_repay_info")  # 未使用
    # 获取我方页面
    LOGIN_PAGE = ("getScenceUrl", "联登页", "get_login_url")
    REPAY_LIST_PAGE = ("getScenceUrl", "还款列表页", "get_repay_list_url")
    LOAN_PAGE_PAGE = ("getScenceUrl", "借据信息页", "get_loan_page_url")
    # 合同
    CONTRACT = ("getContract", "合同", "get_contract_data")


class XiaoHua(BaseRequest):
    # 小花
    def __init__(self, ):
        super().__init__(channel_id="HUB_XIAOHUA", channel_name="小花", channel_method_enum=XiaoHuaMethodsEnum,
                         channel_uid="20366", py_code="xiaohua")

    def get_check_data(self, data):
        # 返回准入信息模板
        mobile = data.get("channelMobile")
        input_id_no = data.get("channelIdNo")
        name = data.get("channelCustName")
        # 返回准入信息模板
        user_name = name if name else get_person_name()
        mobile_no = mobile if mobile else get_mobile_no()
        id_no = input_id_no if input_id_no else get_id_no()
        req_data = {
            "mobile":        md5_encrypt(mobile_no),
            "identityNo":    md5_encrypt(id_no),
            "mobileNo":      md5_encrypt(mobile_no + id_no),
            "name":          user_name,
            "encryptType":   "MD5",
            "accessElement": [{
                "elementType": "0",
                "elementName": "gps（经度,纬度）",
            }, {
                "elementType": "1",
                "elementName": "地域编码（省）",
            }]
        }
        return self.data_model(XiaoHuaMethodsEnum.CHECK.value[0], req_data)

    def get_credit_data(self, data):
        # 当前小花授信提交时，图片校验失败
        mobile = data.get("channelMobile")
        input_id_no = data.get("channelIdNo")
        name = data.get("channelCustName")
        channel_user_no = data.get("channelUserNo")
        channel_credit_no = data.get("channelCreditNo")

        # 返回授信申请信息模板
        degree_values = ["DOCTOR"]
        identity_type_values = ['身份证', '护照', '驾驶证']
        nation_values = ['汉族', '满族', '藏族']
        picture_type_values = ['正面照', '背面照', '手持照']
        relationship_values = ['亲属', '朋友', '同事']
        os_type_values = ['Android', 'iOS']

        userId = channel_user_no
        orderId = channel_credit_no
        phone = mobile
        degree = random.choice(degree_values)
        idNumber = input_id_no
        identityType = random.choice(identity_type_values)
        name = name
        gender = '男'
        nation = random.choice(nation_values)
        address = 'Some Address'
        issuedBy = 'Government'
        validityDate = '2022.01.01-2027.01.01'
        birthDate = '1990.01.01'
        pictureType = random.choice(picture_type_values)
        photoSuffix = 'jpg'
        base64_url = "http://web-tools-svc.sit:8000/api/mock/get_base64"

        linkmanList = [
            {
                'name':         get_person_name(),
                'phone':        get_mobile_no(),
                'relationship': random.choice(relationship_values)
            },
            {
                'name':         get_person_name(),
                'phone':        get_mobile_no(),
                'relationship': random.choice(relationship_values)
            }
        ]
        companyName = 'ABC Company'
        companyPhone = '0123456789'
        osType = random.choice(os_type_values)
        gpsLongitude = '123.456'
        gpsLatitude = '78.90'
        deviceId = 'device123'
        isCrossDomain = True
        macId = 'mac123'
        phoneType = 'iPhone X'
        phoneMaker = 'Apple'
        ipAddress = 'abcd:1234:aCA9:123:4567:089:0:0000'
        memory = 4048
        storage = 64000
        unStorage = 20000
        electricity = 0.8
        dns = '8.8.8.8'
        deviceCode = 'code123'
        sysType = 'Android 10'
        operateCode = '123456'
        androidId = 'android123'
        identificationCode = 'IMC123'
        creditLevel = random.choice(['A', 'B', 'C', 'D'])
        picture_url = "https://test1.xiaohuaai.com/lanaya-front-in/guide/api/downloadPicFile?fileMes=9145642252106e1eae46d183e117dd1c8a818012ff7656636b9c9ae78724fd5ee76fc77d6728c8e302083e1aa7fa9bb44e01115f117a9bdaf28f8b34d83f691a8de1680fb76ba19b8549610558bd994e1156397f1dd5a20e1d8febfb1f26f19929c7384fe52111734266ac33e3be6dec3024e0b3258a010b7fff6782c56c4cff0ebb9673aa1bdde883516b11cbad5ebaa1c8adc59cf01da75e5e5c43eefa774e"
        picture_url = base64_url
        # Construct the JSON template
        req_data = {
            'userId':        userId,
            'orderId':       orderId,
            'phone':         phone,
            'degree':        degree,
            "maritalStatus": "1",
            "purpose":       "CONSUME",
            "city":          "常德市",
            "province":      "湖南省",
            "area":          "汉寿县西湖管理区",
            "income":        "B",
            "liveAddress":   "湖南省汉寿县西湖管理区东洲办事处梨园村1组",
            'idInfo':        {
                'idNumber':     idNumber,
                'identityType': identityType,
                'name':         name,
                'gender':       gender,
                'nation':       nation,
                'address':      address,
                'issuedBy':     issuedBy,
                'validityDate': validityDate,
                'birthDate':    birthDate
            },
            'pictureInfo':   [
                {
                    "pictureType":    "ID_FRONT_FILE",
                    'pictureContent': picture_url,
                    'photoSuffix':    picture_url,
                    'faceChannel':    "TXFQ",
                    'faceScore':      88,
                    'isActive':       True
                },
                {
                    "pictureType":    "ID_BACK_FILE",
                    'pictureContent': picture_url,
                    'photoSuffix':    picture_url,
                    'faceChannel':    "TXFQ",
                    'faceScore':      99,
                    'isActive':       True
                },
                {
                    "pictureType":    "ACTIVE_BODY",
                    'pictureContent': picture_url,
                    'photoSuffix':    picture_url,
                    'faceChannel':    "TXFQ",
                    'faceScore':      99,
                    'isActive':       True
                },
            ],
            'linkmanList':   linkmanList,
            'companyInfo':   {
                'companyName':  companyName,
                'companyPhone': companyPhone
            },
            'deviceInfo':    {
                'osType':             osType,
                'gpsLongitude':       gpsLongitude,
                'gpsLatitude':        gpsLatitude,
                'deviceId':           deviceId,
                'isCrossDomain':      isCrossDomain,
                'macId':              macId,
                'phoneType':          phoneType,
                'phoneMaker':         phoneMaker,
                'ipAddress':          ipAddress,
                'memory':             memory,
                'storage':            storage,
                'unStorage':          unStorage,
                'electricity':        electricity,
                'dns':                dns,
                'deviceCode':         deviceCode,
                'sysType':            sysType,
                'operateCode':        operateCode,
                'androidId':          androidId,
                'IdentificationCode': identificationCode
            },
            'creditLevel':   creditLevel
        }

        return self.data_model(XiaoHuaMethodsEnum.CREDIT.value[0], req_data)

    def get_conclusion_data(self, data):
        channel_credit_no = data.get("channelCreditNo")

        req_data = {
            'orderId':    channel_credit_no,
        }
        return self.data_model(XiaoHuaMethodsEnum.CONCLUSION.value[0], req_data)

    def get_draw_url(self, data):
        channel_user_no = data.get("channelUserNo")
        channel_credit_no = data.get("channelCreditNo")

        req_data = {
            'userId':     channel_user_no,
            'orderId':    channel_credit_no,
            'successUrl': "www.baidu.com",
            'failUrl':    "www.google.com",
            "xhLoanUrl":  "www.bing.com"
        }
        return self.data_model(XiaoHuaMethodsEnum.DRAW_URL.value[0], req_data)

    def get_loan_info(self, data):
        channel_credit_no = data.get("channelCreditNo")

        req_data = {
            'orderId':    channel_credit_no,
        }
        return self.data_model(XiaoHuaMethodsEnum.LOAN_INFO.value[0], req_data)

    @staticmethod
    def get_scene_url(order_id, page_type, back_url="mockjs.com"):
        data = {
            "orderId": order_id,
            "type": page_type,
            "backUrl": back_url
        }
        return data

    def get_login_url(self, data):
        channel_credit_no = data.get("channelCreditNo")
        req_data = self.get_scene_url(channel_credit_no, "1")
        return self.data_model(XiaoHuaMethodsEnum.LOGIN_PAGE.value[0], req_data)

    def get_repay_list_url(self, data):
        channel_credit_no = data.get("channelCreditNo")
        req_data = self.get_scene_url(channel_credit_no, "2")
        return self.data_model(XiaoHuaMethodsEnum.LOGIN_PAGE.value[0], req_data)

    def get_loan_page_url(self, data):
        channel_credit_no = data.get("channelCreditNo")
        req_data = self.get_scene_url(channel_credit_no, "3")
        return self.data_model(XiaoHuaMethodsEnum.LOGIN_PAGE.value[0], req_data)

    def get_contract_data(self, data):
        channel_credit_no = data.get("channelCreditNo")

        req_data = {
            'orderId':    channel_credit_no,
        }
        return self.data_model(XiaoHuaMethodsEnum.CONTRACT.value[0], req_data)

