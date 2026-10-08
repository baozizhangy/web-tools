#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import random
from enum import Enum

from api.channel._base_requests import BaseRequest
from utils.cryption_util import md5_encrypt
from utils.personal_util import get_person_name, get_mobile_no, get_id_no


class HaoJie58MethodsEnum(Enum):
    # 渠道方法枚举，
    # ("渠道方法名", "方法中文名", "对应的数据模板方法")
    CHECK = ("check", "准入", "get_check_data")
    SUBMIT = ("submit", "授信申请", "get_submit_data")
    CONCLUSION = ("conclusion", "授信结果查询", "get_conclusion_data")
    CONTRACT = ("contract", "获取合同", "get_contract_data")


class HaoJie58(BaseRequest):
    # 天冕（我来贷）
    def __init__(self, ):
        super().__init__(channel_id="HUB_58HAOJIE", channel_name="58好借",
                         channel_method_enum=HaoJie58MethodsEnum, channel_uid="21844", py_code="58haojie")

    def get_check_data(self, data):
        mobile = data.get("mobile")
        id_no = data.get("inputIdNo")
        name = data.get("name")
        check_data = {
            "phoneIdCard": md5_encrypt(mobile) + "_" + md5_encrypt(id_no),
            "userName":    name,
            "productId":   mobile
        }
        return self.data_model(HaoJie58MethodsEnum.CHECK.value[0], check_data)

    def get_submit_data(self, data):
        mobile = data.get("channelMobile")
        id_no = data.get("channelIdNo")
        name = data.get("channelCustName")
        channel_credit_no = data.get("channelCreditNo")
        req_data = {
            "orderId":   channel_credit_no,
            "orderInfo": {
                "createTime": 1550643177,
                "idCard":     id_no,
                "phone":      mobile,
                "product":    "XXX",
                "productId":  1024,
                "userName":   name
            },
            "addInfo":   {
                "userInfo":   {
                    "education": "3",
                    "income":    "4",
                    "nature":    "1",
                    "purpose":   "0",
                    "province":  "北京",
                    "city":      "北京",
                    "area":      "朝阳",
                    "address":   "望京地区",
                    "marriage":  1,
                    "relation":  [
                        {
                            "relationShip":  "0",
                            "relationName":  "张三",
                            "relationPhone": "123131313"
                        },
                        {
                            "relationShip":  "6",
                            "relationName":  "李四",
                            "relationPhone": "1231313123"
                        }
                    ],
                    "company":   "58金融"
                },
                "livingInfo": {
                    "attackResult":    "false",
                    "attackScore":     "5.5358732E-6",
                    "attackThreshold": "0.5",
                    "attack_result":   {
                        "result":    "false",
                        "score":     "5.5358732E-6",
                        "threshold": "0.5"
                    },
                    "confidence":      "78.74538",
                    "creditResult":    "1",
                    "livingPhoto":     "http://pic.58.com/bodyauth/n_v269e969ebe45543de80ad17d735759d6a.jpg",
                    "livingScore":     "78.74538",
                    "oneE3":           "62.168713",
                    "oneE4":           "69.31534",
                    "oneE5":           "74.39926",
                    "oneE6":           "78.038055",
                    "result_code":     "1000",
                    "thresholds":      {
                        "1e-6": "78.038055",
                        "1e-5": "74.39926",
                        "1e-4": "69.31534",
                        "1e-3": "62.168713"
                    }
                },
                "idcardInfo": {
                    "idFront":           "https://pic1.58cdn.com.cn/mobile/big/x.jpg",
                    "idBack":            "https://pic1.58cdn.com.cn/mobile/big/xx.jpg",
                    "frontCompleteness": "1",
                    "ocrGender":         {
                        "result":  "男",
                        "rect":    {
                            "rb": {
                                "x": 126,
                                "y": 244
                            },
                            "rt": {
                                "x": 125,
                                "y": 214
                            },
                            "lb": {
                                "x": 97,
                                "y": 245
                            },
                            "lt": {
                                "x": 96,
                                "y": 215
                            }
                        },
                        "logic":   0,
                        "quality": 0.884
                    },
                    "ocrAddress":        {
                        "result":  "XX市龙XX路19号",
                        "rect":    {
                            "rb": {
                                "x": 453,
                                "y": 403
                            },
                            "rt": {
                                "x": 449,
                                "y": 331
                            },
                            "lb": {
                                "x": 96,
                                "y": 417
                            },
                            "lt": {
                                "x": 94,
                                "y": 344
                            }
                        },
                        "logic":   0,
                        "quality": 0.802
                    },
                    "frontLegality":     {
                        "Screen":             0.001,
                        "Edited":             0,
                        "ID_Photo_Threshold": 0.8,
                        "Temporary_ID_Photo": 0,
                        "Photocopy":          0,
                        "ID_Photo":           0.999
                    },
                    "ocrNationality":    {
                        "result":  "汉",
                        "rect":    {
                            "rb": {
                                "x": 300,
                                "y": 235
                            },
                            "rt": {
                                "x": 299,
                                "y": 207
                            },
                            "lb": {
                                "x": 271,
                                "y": 236
                            },
                            "lt": {
                                "x": 269,
                                "y": 208
                            }
                        },
                        "logic":   0,
                        "quality": 0.914
                    },
                    "backCardRect":      {
                        "rb": {
                            "x": 792,
                            "y": 595
                        },
                        "rt": {
                            "x": 765,
                            "y": 96
                        },
                        "lb": {
                            "x": -8,
                            "y": 593
                        },
                        "lt": {
                            "x": -8,
                            "y": 101
                        }
                    },
                    "ocrIdcardNo":       {
                        "result":  id_no,
                        "rect":    {
                            "rb": {
                                "x": 712,
                                "y": 529
                            },
                            "rt": {
                                "x": 710,
                                "y": 497
                            },
                            "lb": {
                                "x": 228,
                                "y": 549
                            },
                            "lt": {
                                "x": 227,
                                "y": 517
                            }
                        },
                        "logic":   0,
                        "quality": 0.389
                    },
                    "ocrName":           {
                        "result":  "张健",
                        "rect":    {
                            "rb": {
                                "x": 198,
                                "y": 173
                            },
                            "rt": {
                                "x": 196,
                                "y": 139
                            },
                            "lb": {
                                "x": 101,
                                "y": 176
                            },
                            "lt": {
                                "x": 100,
                                "y": 142
                            }
                        },
                        "logic":   0,
                        "quality": 0.895
                    },
                    "ocrIssuedBy":       {
                        "result":  "XX市公安局XX分局",
                        "rect":    {
                            "rb": {
                                "x": 619,
                                "y": 480
                            },
                            "rt": {
                                "x": 618,
                                "y": 450
                            },
                            "lb": {
                                "x": 317,
                                "y": 480
                            },
                            "lt": {
                                "x": 317,
                                "y": 450
                            }
                        },
                        "logic":   0,
                        "quality": 0.66
                    },
                    "ocrValidDateEnd":   {
                        "result":  "20340928",
                        "rect":    {
                            "rb": {
                                "x": 640,
                                "y": 546
                            },
                            "rt": {
                                "x": 638,
                                "y": 518
                            },
                            "lb": {
                                "x": 318,
                                "y": 545
                            },
                            "lt": {
                                "x": 317,
                                "y": 517
                            }
                        },
                        "logic":   0,
                        "quality": 0.676
                    },
                    "backLegality":      {
                        "Screen":             0,
                        "Edited":             0,
                        "ID_Photo_Threshold": 0.8,
                        "Temporary_ID_Photo": 0,
                        "Photocopy":          0.009,
                        "ID_Photo":           0.991
                    },
                    "ocrValidDateStart": {
                        "result":  "20140928",
                        "rect":    {
                            "rb": {
                                "x": 640,
                                "y": 546
                            },
                            "rt": {
                                "x": 638,
                                "y": 518
                            },
                            "lb": {
                                "x": 318,
                                "y": 545
                            },
                            "lt": {
                                "x": 317,
                                "y": 517
                            }
                        },
                        "logic":   0,
                        "quality": 0.676
                    },
                    "frontCardRect":     {
                        "rb": {
                            "x": 825,
                            "y": 585
                        },
                        "rt": {
                            "x": 772,
                            "y": 55
                        },
                        "lb": {
                            "x": -87,
                            "y": 625
                        },
                        "lt": {
                            "x": -95,
                            "y": 82
                        }
                    },
                    "backCompleteness":  "1"
                },
                "device":     {
                    "brand":           "OPPOR11sPlus",
                    "deviceId":        "dDaIwkLISrOAjEk4fWJWW1ZMaM2Bs3iNbhoC3BUmDH4q+N3Utz6IRfXISWGuONwJ",
                    "imei":            "868400038082692",
                    "ip":              "36.162.211.79",
                    "lat":             "29.647763",
                    "lon":             "91.074864",
                    "mac":             "",
                    "model":           "",
                    "networkType":     "NETWORK_WIFI",
                    "os":              "android",
                    "osVersion":       "25",
                    "resolutionRatio": "1080x2160",
                    "ua":              "Mozilla / 5.0(Linux; Android 7.1 .1; OPPO R11s Plus Build / NMF26X; wv)"
                },
                "wbScore":    {
                    "wbScore": "90"
                },
                "extendInfo": {
                    "jddScore": "90"
                }
            }
        }
        return self.data_model(HaoJie58MethodsEnum.SUBMIT.value[0], req_data)

    def get_conclusion_data(self, data):
        channel_user_no = data.get("channelUserNo", f"default_value_{random.randint(1, 1000)}")
        req_data = {
            "orderId": channel_user_no
        }
        return self.data_model(HaoJie58MethodsEnum.CONCLUSION.value[0], req_data)

    def get_contract_data(self, data):
        channel_user_no = data.get("channelUserNo", f"default_value_{random.randint(1, 1000)}")
        req_data = {
            "orderId": channel_user_no,
            "contractType": 1
        }
        return self.data_model(HaoJie58MethodsEnum.CONTRACT.value[0], req_data)
