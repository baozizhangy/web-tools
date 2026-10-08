#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import random
from enum import Enum

from api.channel._base_requests import BaseRequest
from utils.cryption_util import md5_encrypt
from utils.logger_util import web_logger
from utils.personal_util import get_person_name, get_mobile_no, fake


class HuoLaLaMethodsEnum(Enum):
    # 渠道方法枚举，
    # ("渠道方法名", "方法中文名", "对应的数据模板方法")
    CHECK = ("prefiltering", "准入", "get_check_data")
    CREDIT_APPLY = ("creditApply", "授信申请", "get_credit_data")
    CREDIT_QUERY = ("getCreditResult", "授信结果查询", "get_credit_query_data")
    ACCOUNT_QUERY = ("queryUserCreditAmountAPI", "额度查询", "get_account_query_data")
    GET_DRAW_URL = ("redirectH5", "获取借款URL", "get_draw_url_data")
    GET_REPAY_URL = ("redirectH5", "获取还款URL", "get_repay_url_data")
    QUERY_CONTRACT = ("getAgreementTemplate", "获取合同", "get_contract_data")
    GET_REPAY_PLAN = ("getRepayPlan", "查询还款计划", "get_repay_plan")


class HuoLaLa(BaseRequest):
    def __init__(self, ):
        super().__init__("HUB_HUOLALA", "货拉拉", channel_method_enum=HuoLaLaMethodsEnum,
                         channel_uid="20893", py_code="huolala")

    @BaseRequest.non_empty(["channelMobile", "channelIdNo", "channelCustName", "channelUserNo"])
    def get_check_data(self, data):
        # 返回准入信息模板
        mobile = data.get("channelMobile")
        id_no = data.get("channelIdNo")
        name = data.get("channelCustName")
        channel_user_no = data.get("channelUserNo")

        check_data = {
            "userName":        name,
            "md5Phone":        md5_encrypt(mobile),
            "md5IdNo":         md5_encrypt(id_no),
            "md5PhoneAndIdNo": md5_encrypt(mobile + id_no),
            "partnerId":       fake.uuid4().replace("-", ""),
            "openId":          channel_user_no,
        }
        return self.data_model(HuoLaLaMethodsEnum.CHECK.value[0], check_data)

    @BaseRequest.non_empty(["channelMobile", "channelIdNo", "channelCustName", "channelUserNo", "channelCreditNo"])
    def get_credit_data(self, data):
        # 返回授信信息模板
        mobile = data.get("channelMobile")
        id_no = data.get("channelIdNo")
        name = data.get("channelCustName")
        channel_user_no = data.get("channelUserNo")
        channel_credit_no = data.get("channelCreditNo")

        gender = 0 if id_no[-2] in ['0', '2', '4', '6', '8', 'X'] else 1
        birthDay = id_no[6:10] + "/" + id_no[10:12] + "/" + id_no[12:14]

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
        id_card_front_base64 = "/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAMCAgMCAgMDAwMEAwMEBQgFBQQEBQoHBwYIDAoMDAsKCwsNDhIQDQ4RDgsLEBYQERMUFRUVDA8XGBYUGBIUFRT/2wBDAQMEBAUEBQkFBQkUDQsNFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBT/wAARCA/AC9ADASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwDyhmdWzH99hz9Kr3ELyRqz/eXjA6Hscj6UksblvmfCHoRnj2pIrqJUJG4tg53fNntX5qz7MaGUxybN2zqV6Gpm2yCMhvkYcr2xTN8TRjygJR7nBx7etQuoLjHToARyKQEwCBmIwQzAc03jcYCMuc4HqPekRxcv5RQe5HT8aR2A2kphk"
        id_card_backend_base64 = "/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAMCAgMCAgMDAwMEAwMEBQgFBQQEBQoHBwYIDAoMDAsKCwsNDhIQDQ4RDgsLEBYQERMUFRUVDA8XGBYUGBIUFRT/2wBDAQMEBAUEBQkFBQkUDQsNFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBT/wAARCA/AC9ADASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwDxhrd7YsSzc/dPapt7tGolB3H5XHtUmoZWBQimQbsYPGDSyWx8tZS3lM3BA5r8xufajXs3miB3AgDhjUQh8yMozbQOm09TUxiztG7O0emM0kYieT5G2lf4T60rgUpGCLhj8g4YYycd6lWOLc22fbFjI479xVuSQrIHSIM7cORyMd6RW"

        live_base64 = "iVBORw0KGgoAAAANSUhEUgAAAeYAAAKFCAYAAAAZG0qmAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAEqLSURBVHhe7d0HmBTl/cBxEcESjcaSGP9iYi+gYNez94gtGjEmxn8s5BJj4j+xxJLEChZUOHrvYEGUoh4IIr0ISFPq0Y9ylOPgKscd9/u/7+zs3e7e75bj2NmZhe+b5/Ps7uzc7szkefzyzs7tHbQie5PsDw466CAAAFKfFrlUpO4cAACpRotcKlJ3DgCAVKNFLhWpOwcAQKrRIpeK1J0DACDVaJFLRerOAQCQarTIpSJ15wKi9TvvyejxU+T/nntRzjz7HHUdAAAcWuRSkbpzAXHdLbfLb1/pKu9mdJQPPxtJpAEANdMil4rUnQuIG2+/S24fI3JXZrG06DVDHnqtG5EGAOi0yKUidecC4iYT5ru+FrlnnMi9xq+tUcVyf6/p8qCZSb/Ttj2RBgCEaJFLhDZtO8i0WfPV5yz7nF1He64u1J0LiJua3+UEucV4kQcMe3ufeXyPifWdY0Xu+LJY7u42Ve7/T2d56712RBoADmRa5BJh6qx58s57GTJ99oJqz9llbd5vrz5XV+rOBYQN8/3fiPx2gsjvJoZu7WMb67tNnO8wcf7VGJFbvhK5eWSR3NZpstzzYgdp9c57RBoADjRa5BJFi7NdlugoW+rOBURlmM1M+UETZRtmZ9ZsltnT23bWfLtxmw3zaJEbRolcmylyzbAiuSFjgtzxr3by2lttiDQAHAi0yCVSZJzjzaL3lbpzAWE/Y7Zhtqexw+xjG2b7ebP9/Dly1nyjifP1NsxfiqQZV3wuctnQQrnyvXFy69Pvy8ut3iLSALC/0iKXaJO/nSNvtnlf3n6vnRNnbZ19pe5cQNx4+53yGxNhO0sOiwxz+HS2vXL71phZ89UmzFd+IXK5ifMlI0UuHCHS5KNCOff10XLVk2/LS"

        credit_data = {
            "creditNo":           channel_credit_no,
            "name":               name,
            "idCardNo":           id_no,
            "mobile":             mobile,
            "partnerId":          fake.uuid4().replace("-", ""),
            "openId":             channel_user_no,
            "homeLocation":       "广东省-深圳市-龙华区-民治街道榕树苑11栋",
            "contactInfos":       [
                {
                    "name":     get_person_name(),
                    "relation": random_relation,  # 父亲
                    "phone":    get_mobile_no(),
                    "flag":     "0"  # 直系
                },
                {
                    "name":     get_person_name(),
                    "relation": immediate,  # 亲属
                    "phone":    get_mobile_no(),
                    "flag":     "1"  # 非直系
                }
            ],
            "profession":         random_profession,
            "creditAgain":        "0",  # 否
            "positiveBase64Str":  base64_data,
            "negativeBase64Str":  base64_data,
            "faceBase64Str":      base64_data,
            "livingScore":        "99",
            "issuedBy":           "上海市公安局",
            "gender":             gender,
            "nation":             "汉",
            "birthDay":           birthDay,  # 身份证出生日期
            "validityPeriod":     "2016.07.13-2036.07.13",  # 身份证有效期
            "idAddress":          "广东省-深圳市-龙华区-民治街道榕树苑11栋",
            "eduBackgroundCode":  random_edu_background,  # 大学本科
            "marriageStatusCode": random_marriage_status,  # 未婚
            "workType":           random_work_type,  # 工薪族
            "industry":           random_industry,  # 信息传输/软件/信息技术服务业
            "monthlyIncome":      random_monthly_income,  # 3000-6000
            "customerType":       customer_type  # 司机
        }
        if random_work_type == 3:
            credit_data["companyInformation"] = {
                "companyName":    "公司名称",
                "companyType":    company_type,  # 普通民营企业
                "companyAddress": "广东省-深圳市-龙华区-民治街道榕树苑11栋"
            }
        return self.data_model(HuoLaLaMethodsEnum.CREDIT_APPLY.value[0], credit_data)

    @BaseRequest.non_empty(["channelMobile", "channelUserNo", "channelCreditNo"])
    def get_credit_query_data(self, data):
        """
        调用授信结果查询
        :param
        :return:
        """
        mobile = data.get("channelMobile")
        channel_user_no = data.get("channelUserNo")
        channel_credit_no = data.get("channelCreditNo")

        credit_result_data = {
            "creditNo": channel_credit_no,
            "openId":   channel_user_no,
            "mobile":   mobile
        }
        return self.data_model(HuoLaLaMethodsEnum.CREDIT_QUERY.value[0], credit_result_data)

    @BaseRequest.non_empty(["channelMobile", "channelUserNo"])
    def get_account_query_data(self, data):
        # 查询用户额度信息
        # method = "conclusion_detail"
        mobile = data.get("channelMobile")
        channel_user_no = data.get("channelUserNo")
        data = {
            "partnerId": fake.uuid4().replace("-", ""),
            "openId":    channel_user_no,
            "mobile":    mobile
        }
        web_logger.info(f"credit_result::入参::{data}")
        # res = self._request(method, data).json()
        return self.data_model(HuoLaLaMethodsEnum.ACCOUNT_QUERY.value[0], data)

    @staticmethod
    def get_h5_url(access_scene_id, open_id, mobile, receipt_no=None, callback_url="http://www.baidu.com"):
        # 获取跳转url
        # access_scene_id: 3.还款 7.借款
        data = {
            "accessSceneId": access_scene_id,
            "openId":        open_id,
            "receiptNo":     receipt_no,
            "mobile":        mobile,
            "callbackUrl":   callback_url
        }
        return data

    @BaseRequest.non_empty(["channelMobile", "channelUserNo"])
    def get_draw_url_data(self, data):
        mobile = data.get("channelMobile")
        channel_user_no = data.get("channelUserNo")
        access_scene_id = "7"
        data = self.get_h5_url(access_scene_id, channel_user_no, mobile)
        return self.data_model(HuoLaLaMethodsEnum.GET_DRAW_URL.value[0], data)

    @BaseRequest.non_empty(["channelMobile", "channelUserNo", "channelDrawNo"])
    def get_repay_url_data(self, data):
        mobile = data.get("channelMobile")
        channel_user_no = data.get("channelUserNo")
        channel_draw_no = data.get("channelDrawNo")
        access_scene_id = "3"
        data = self.get_h5_url(access_scene_id, channel_user_no, mobile, channel_draw_no)
        return self.data_model(HuoLaLaMethodsEnum.GET_REPAY_URL.value[0], data)

    @BaseRequest.non_empty(["channelMobile", "channelUserNo", "channelDrawNo"])
    def get_repay_plan(self, data):
        # 分期还款计划同步（原还款结果查询）
        mobile = data.get("channelMobile")
        channel_user_no = data.get("channelUserNo")
        channel_draw_no = data.get("channelDrawNo")
        data = {
            "openId":    channel_user_no,
            "partnerId": fake.uuid4().replace("-", ""),
            "mobile":    mobile,
            "receiptNo": channel_draw_no
        }
        web_logger.info(f"credit_result::入参::{data}")
        return self.data_model(HuoLaLaMethodsEnum.GET_REPAY_PLAN.value[0], data)

    @BaseRequest.non_empty(["channelUserNo"])
    def get_contract_data(self, data):
        """
        调用协议查询
        :param
        :return:
        """
        channel_user_no = data.get("channelUserNo")
        data = {
            "partnerId": fake.uuid4().replace("-", ""),
            "openId":    channel_user_no,
            "type":      "ccs_8"
        }
        return self.data_model(HuoLaLaMethodsEnum.QUERY_CONTRACT.value[0], data)

    def query_loan_record(self, open_id_list):
        # 批量查询借据列表
        data = {
            "openIdList": open_id_list,
        }
        web_logger.info(f"credit_result::入参::{data}")
        return self.data_model(HuoLaLaMethodsEnum.GET_REPAY_PLAN.value[0], data)
