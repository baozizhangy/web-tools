#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import random
from enum import Enum

from api.channel._base_requests import BaseRequest
from api.channel.channel_api_config import ChannelMethodsEnum
from utils.cryption_util import md5_encrypt
from utils.personal_util import get_person_name, get_id_no, get_mobile_no, fake


class ShiGuangFenQiMethodsEnum(Enum):
    # 渠道方法枚举，
    # ("渠道方法名", "方法中文名", "对应的数据模板方法")
    CHECK = ("prefilter", "准入", "get_check_data")
    CREDIT_APPLY = ("pushUserInfo", "授信申请", "get_credit_data")
    CREDIT_QUERY = ("getCreditInfo", "授信结果查询", "get_credit_query_data")
    CONTRACT = ("getContract", "合同查询", "get_contract_data")


class ShiGuangFenQi(BaseRequest):
    # 玖富v2
    def __init__(self, ):
        super().__init__(channel_id="HUB_SHIGUANGFENQI", channel_name="时光分期",
                         channel_method_enum=ShiGuangFenQiMethodsEnum, channel_uid="20566", py_code="shiguangfenqi")

    def get_check_data(self, data):
        # 返回准入信息模板
        mobile = data.get("channelMobile")
        input_id_no = data.get("channelIdNo")
        input_check_no = data.get("channelCheckNo")
        name = data.get("channelCustName")
        # 返回准入信息模板
        user_name = name if name else get_person_name()
        mobile_no = mobile if mobile else get_mobile_no()
        id_no = input_id_no if input_id_no else get_id_no()
        req_data = {
            "mobileMD5": md5_encrypt(mobile_no),
            "idCardMD5": md5_encrypt(id_no),
            "moIdMD5":   md5_encrypt(mobile_no + id_no),
            "nameIDMD5": md5_encrypt(user_name + mobile_no + id_no),
        }
        return self.data_model(ShiGuangFenQiMethodsEnum.CHECK.value[0], req_data)

    # def check(self, data):
    #     """
    #     调用准入
    #     :param data = {
    #         "userName":        "",
    #         "md5Phone":        "",
    #         "md5IdNo":         "",
    #         "md5PhoneAndIdNo": "",
    #         "partnerId":       "",
    #         "openId":          "",
    #     }
    #     :return:
    #     """
    #     method = "check"  # 准入
    #     res = self._request(method, data).json()
    #     return res

    def get_credit_data(self, data):
        """
        获取授信报文
        """
        # {"channelId": "HUB_SHIGUANGFENQI",
        #     "method":    "pushUserInfo",
        #     "bizData": {}}

        mobile = data.get("channelMobile")
        input_id_no = data.get("channelIdNo")
        name = data.get("channelCustName")

        user_name = name if name else get_person_name()
        mobile_no = mobile if mobile else get_mobile_no()
        id_no = input_id_no if input_id_no else get_id_no()

        gender = 0 if id_no[-2] in ['0', '2', '4', '6', '8', 'X'] else 1
        birthDay = id_no[6:10] + "-" + id_no[10:12] + "-" + id_no[12:14]

        # 随机选择紧急联系人关系
        # relation_values = [0, 1, 2, 3, 4, 6, 7, 8]
        relation_values = [3, 4, 6]
        random_relation = random.choice(relation_values)

        # 直系紧急联系人关系
        immediate_relation_values = [0, 1, 2, 7, 8]
        immediate = random.choice(immediate_relation_values)

        # 随机选择用户职业
        profession_values = ["0", "1", "3", "4", "5", "6", "X"]
        random_profession = random.choice(profession_values)

        # 随机选择学历
        edu_background_values = ["10", "20", "30", "60", "91"]
        random_edu_background = random.choice(edu_background_values)

        # 随机选择婚姻状况
        marriage_status_values = ["10", "20", "21", "40"]
        random_marriage_status = random.choice(marriage_status_values)

        # 随机选择职业性质
        work_type_values = [1, 2, 3, 4, 5, 6]
        random_work_type = random.choice(work_type_values)

        # 随机选择所属行业
        industry_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15]
        random_industry = random.choice(industry_values)

        # 随机选择月收入
        monthly_income_values = [1, 2, 3, 4, 5]
        random_monthly_income = random.choice(monthly_income_values)

        # 随机选择用户类型
        customer_type_value = [1, 3, 4]
        customer_type = random.choice(customer_type_value)

        # 随机选择用户类型
        company_type_value = [1, 2, 3, 4, 5, 6]
        company_type = random.choice(company_type_value)

        base64_data = "iVBORw0KGgoAAAANSUhEUgAAAjkAAAFBCAYAAACVcr5cAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAFiUAABYlAUlSJPAAAAWZSURBVHhe7dYxEQAgEMCwB/+egQEVvWSpha7zDABAzP4FAEgxOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABBMxeXJgZ+f2mLWgAAAABJRU5ErkJggg=="

        credit_data = {
                "uid":           fake.uuid4().replace("-", ""),
                "applyId":       fake.uuid4().replace("-", ""),
                "userName":      user_name,
                "mobile":        mobile_no,
                "readforced":    "yes",
                "marriage":      1,
                "education":     2,
                "email":         "734668978@qq.com",
                "monthIncome":   "1000000",
                "moneyFunction": "1",
                "loanPurpose":   "1",
                "addressInfo":   {
                    "province": "北京市",
                    "city":     "市辖区",
                    "district": "东城区",
                    "detail":   "中国北京市海淀区海淀南路乙15号"
                },
                "contactInfo":   [
                    {
                        "relation": 1,
                        "name":     "张三",
                        "mobile":   "13184616309"
                    },
                    {
                        "relation": 3,
                        "name":     "李四",
                        "mobile":   "17695932069"
                    }
                ],
                "occupation":    {
                    "companyName":    "工体挺开心就行了",
                    "workNature":     5,
                    "position":       1,
                    "occupationType": "13"
                },
                "bankcard":      {
                    "bankcardNo":    "6227002049037409926",
                    "bankcardPhone": "13873506609"
                },
                "idcardInfo":    {
                    "idcardNo":     id_no,
                    "validBegin":   "20200928",
                    "validEnd":     "20330928",
                    "gender":       gender,
                    "nation":       "汉",
                    "birthday":     birthDay,
                    "address":      "河南省林州市三区22号",
                    "issuedby":     "北京市公安局",
                    "frontPicture": base64_data,
                    "backPicture":  base64_data
                },
                "facePicture":   base64_data,
            }

        # return credit_data
        return self.data_model(ShiGuangFenQiMethodsEnum.CREDIT_APPLY.value[0], credit_data)

    def get_contract_data(self, data):
        req_data = {
            "uid":           fake.uuid4().replace("-", ""),
            "applyId":       fake.uuid4().replace("-", ""),
            "userName":      get_person_name(),
            "scene":         "1",
        }
        return self.data_model(ShiGuangFenQiMethodsEnum.CONTRACT.value[0], req_data)