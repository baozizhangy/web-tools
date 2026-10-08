#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
import random
from enum import Enum

from api.channel._base_requests import BaseRequest
# from config import xr_sftp_client, BASE_DIR
from utils.cryption_util import md5_encrypt
from utils.personal_util import get_person_name, get_id_no, get_mobile_no, fake

# yiJieSuDaiV2MethodMap.put("check", MethodEnum.CHECK.getCode());
# yiJieSuDaiV2MethodMap.put("send_data", MethodEnum.SEND_DATA.getCode());
# yiJieSuDaiV2MethodMap.put("conclusion", MethodEnum.CONCLUSION.getCode());
# yiJieSuDaiV2MethodMap.put("trial", MethodEnum.TRIAL.getCode());
# yiJieSuDaiV2MethodMap.put("confirm_sign", MethodEnum.CONFIRM_SIGN.getCode());
# yiJieSuDaiV2MethodMap.put("confirm_order", MethodEnum.CONFIRM_ORDER.getCode());
# yiJieSuDaiV2MethodMap.put("loan_info", MethodEnum.LOAN_INFO.getCode());
# yiJieSuDaiV2MethodMap.put("scene_url", MethodEnum.SCENE_URL.getCode());
# yiJieSuDaiV2MethodMap.put("repay_info", MethodEnum.REPAY_INFO.getCode());
# yiJieSuDaiV2MethodMap.put("bind_info", MethodEnum.BIND_LIST.getCode());
# yiJieSuDaiV2MethodMap.put("bank_list", MethodEnum.BANK_LIST.getCode());
# yiJieSuDaiV2MethodMap.put("bind_card", MethodEnum.BIND_CARD.getCode());
# yiJieSuDaiV2MethodMap.put("bind_verify", MethodEnum.BIND_VERIFY.getCode());


class YiJieSuDaiV2MethodsEnum(Enum):
    # 渠道方法枚举，
    # ("渠道方法名", "方法中文名", "对应的数据模板方法")
    CHECK = ("check", "准入", "get_check_data")
    SUBMIT = ("send_data", "授信申请", "get_credit_data")
    CONCLUSION = ("conclusion", "授信结果查询", "get_conclusion_data")
    # 银行卡
    H5_BIND = ("bind_url", "H5绑卡", "get_h5_bind_data")
    BIND_CARD = ("bind_card", "API绑卡", "get_bind_card_data")
    BIND_VERIFY = ("bind_verify", "API绑卡验证", "get_bind_verify_data")
    BIND_INFO = ("bind_info", "API绑卡信息", "get_bind_info_data")
    BANK_LIST = ("bank_list", "API银行卡列表", "get_bank_list_data")
    # 借款
    TRIAL = ("trial", "借款试算", "get_trial_data")
    CONFIRM_ORDER = ("confirm_order", "借款短信发送", "get_confirm_order_data")
    CONFIRM_SIGN = ("confirm_sign", "借款提交", "get_confirm_sign_data")
    LOAN_INFO = ("loan_info", "贷款信息查询", "get_loan_info_data")
    # 还款
    GET_URL = ("scene_url", "获取还款URL", "get_url_data")
    REPAY_INFO = ("repay_info", "还款信息查询", "get_repay_info_data")
    # 合同
    BASE_CONTRACT = ("contract", "产品详情页合同", "get_base_contract_data")
    BIND_CONTRACT = ("contract", "绑卡页面合同", "get_bind_contract_data")
    DRAW_CONTRACT = ("contract", "确认借款页合同-授信", "get_draw_contract_data")
    LOAN_CONTRACT = ("contract", "贷款详情页面合同-借款", "get_loan_contract_data")


class YiJieSuDaiV2(BaseRequest):
    def __init__(self, ):
        super().__init__(channel_id="HUB_YIJIESUDAI_V2", channel_name="易借速贷V2",
                         channel_method_enum=YiJieSuDaiV2MethodsEnum, channel_uid="21146", py_code="yijiesudai_v2")
    #
    # @staticmethod
    # def upload_jpg(id_no):
    #     # 上传身份证、人脸图片到FTP服务器
    #
    #     error_msgs = []
    #     try:
    #         # 上传人脸图片
    #         upload_face_res = xr_sftp_client.upload_dir(
    #             f'{BASE_DIR}/mock_data/channel/yijiesudai_v2/',
    #             f'/upload/{id_no}/')
    #         print(f"易借速贷上传图片结果:{upload_face_res}")
    #     except Exception as e:
    #         error_msgs.append(str(e))
    #
    #     if error_msgs:
    #         # error_msg = '\n'.join(error_msgs)
    #         return {"code": "999", "msg": f"图片文件上传失败, ID号: {id_no}：{error_msgs}"}
    #     else:
    #         return {"code": "0", "msg": "文件上传成功"}

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
            "phoneMd5":         md5_encrypt(mobile_no),
            "idNumberMd5":      md5_encrypt(id_no),
            "phoneIdNumberMd5": md5_encrypt(mobile_no + id_no),
        }
        return self.data_model(YiJieSuDaiV2MethodsEnum.CHECK.value[0], req_data)

    def get_credit_data(self, data):
        # 返回授信信息模板
        mobile = data.get("channelMobile")
        input_id_no = data.get("channelIdNo")
        name = data.get("channelCustName")
        channel_credit_no = data.get("channelCreditNo")

        user_name = name if name else get_person_name()
        mobile_no = mobile if mobile else get_mobile_no()
        id_no = input_id_no if input_id_no else get_id_no()
        gender = 0 if id_no[-2] in ['0', '2', '4', '6', '8', 'X'] else 1
        birthDay = id_no[6:10] + "." + id_no[10:12] + "." + id_no[12:14]

        # 上传图片
        res = self.upload_jpg(input_id_no)
        if res["code"] != "0":
            return {"code": res["code"], "msg": res["msg"]}

        # 随机选择紧急联系人关系
        relation_values = [0, 1, 2, 3, 4, 6, 7, 8]
        random_relation = random.choice(relation_values)

        # 直系紧急联系人关系
        immediate_relation_values = [0, 1, 2, 7, 8]
        immediate = random.choice(immediate_relation_values)

        # 随机选择用户职业
        profession_values = ["0", "1", "3", "4", "5", "6", "X"]
        random_profession = random.choice(profession_values)

        # 随机选择学历
        edu_background_values = ["10", "20", "30", "50", "60", "70", "80", "90", "99"]
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
        customer_type_value = [1, 3]
        customer_type = random.choice(customer_type_value)

        # 随机选择用户类型
        company_type_value = [1, 2, 3, 4, 5, 6]
        company_type = random.choice(company_type_value)
        base64_data = "iVBORw0KGgoAAAANSUhEUgAAAjkAAAFBCAYAAACVcr5cAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAFiUAABYlAUlSJPAAAAWZSURBVHhe7dYxEQAgEMCwB/+egQEVvWSpha7zDABAzP4FAEgxOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABBMxeXJgZ+f2mLWgAAAABJRU5ErkJggg=="
        id_card_front_base64 = "/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAMCAgMCAgMDAwMEAwMEBQgFBQQEBQoHBwYIDAoMDAsKCwsNDhIQDQ4RDgsLEBYQERMUFRUVDA8XGBYUGBIUFRT/2wBDAQMEBAUEBQkFBQkUDQsNFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBT/wAARCA/AC9ADASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwDyhmdWzH99hz9Kr3ELyRqz/eXjA6Hscj6UksblvmfCHoRnj2pIrqJUJG4tg53fNntX5qz7MaGUxybN2zqV6Gpm2yCMhvkYcr2xTN8TRjygJR7nBx7etQuoLjHToARyKQEwCBmIwQzAc03jcYCMuc4HqPekRxcv5RQe5HT8aR2A2kphk"
        id_card_backend_base64 = "/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAMCAgMCAgMDAwMEAwMEBQgFBQQEBQoHBwYIDAoMDAsKCwsNDhIQDQ4RDgsLEBYQERMUFRUVDA8XGBYUGBIUFRT/2wBDAQMEBAUEBQkFBQkUDQsNFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBT/wAARCA/AC9ADASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwDxhrd7YsSzc/dPapt7tGolB3H5XHtUmoZWBQimQbsYPGDSyWx8tZS3lM3BA5r8xufajXs3miB3AgDhjUQh8yMozbQOm09TUxiztG7O0emM0kYieT5G2lf4T60rgUpGCLhj8g4YYycd6lWOLc22fbFjI479xVuSQrIHSIM7cORyMd6RW"

        live_base64 = "iVBORw0KGgoAAAANSUhEUgAAAeYAAAKFCAYAAAAZG0qmAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAEqLSURBVHhe7d0HmBTl/cBxEcESjcaSGP9iYi+gYNez94gtGjEmxn8s5BJj4j+xxJLEChZUOHrvYEGUoh4IIr0ISFPq0Y9ylOPgKscd9/u/7+zs3e7e75bj2NmZhe+b5/Ps7uzc7szkefzyzs7tHbQie5PsDw466CAAAFKfFrlUpO4cAACpRotcKlJ3DgCAVKNFLhWpOwcAQKrRIpeK1J0DACDVaJFLRerOAQCQarTIpSJ15wKi9TvvyejxU+T/nntRzjz7HHUdAAAcWuRSkbpzAXHdLbfLb1/pKu9mdJQPPxtJpAEANdMil4rUnQuIG2+/S24fI3JXZrG06DVDHnqtG5EGAOi0yKUidecC4iYT5ru+FrlnnMi9xq+tUcVyf6/p8qCZSb/Ttj2RBgCEaJFLhDZtO8i0WfPV5yz7nF1He64u1J0LiJua3+UEucV4kQcMe3ufeXyPifWdY0Xu+LJY7u42Ve7/T2d56712RBoADmRa5BJh6qx58s57GTJ99oJqz9llbd5vrz5XV+rOBYQN8/3fiPx2gsjvJoZu7WMb67tNnO8wcf7VGJFbvhK5eWSR3NZpstzzYgdp9c57RBoADjRa5BJFi7NdlugoW+rOBURlmM1M+UETZRtmZ9ZsltnT23bWfLtxmw3zaJEbRolcmylyzbAiuSFjgtzxr3by2lttiDQAHAi0yCVSZJzjzaL3lbpzAWE/Y7Zhtqexw+xjG2b7ebP9/Dly1nyjifP1NsxfiqQZV3wuctnQQrnyvXFy69Pvy8ut3iLSALC/0iKXaJO/nSNvtnlf3n6vnRNnbZ19pe5cQNx4+53yGxNhO0sOiwxz+HS2vXL71phZ89UmzFd+IXK5ifMlI0UuHCHS5KNCOff10XLVk2/LS"
        req_ext = {
                "latitude": "12.43214",
                "longitude": "12.43214",
                "ipAddr": "222.71.89.50",
                "devOs": "Android"
            }
        req_data = {
            "applyNo":          channel_credit_no,
            "phone":            mobile_no,
            "idCard":           id_no,
            "name":             user_name,
            "address":          fake.address().replace(" ", ""),
            "gender":           gender,
            "nation":           "汉",
            "validBegin":       "2017-09-29",
            "validEnd":         "2037-09-29",
            "birthday":         birthDay,
            "agency":           "崇明区公安局",
            "expectAmount":     6000,
            "expectNper":       12,
            "liabilitieAmount": 0.0,
            "reqExt":           json.dumps(req_ext, ensure_ascii=False),
            "userInfo":         {
                "educationalBackground": random_edu_background,
                "houseType":             "1",
                "income":                8000.0,
                "maritalStatus":         "20",
                "residenceAddr":         "北京市,北京市,东城区宗女生吗啡",
                "residenceAddrArea":     "北京市,北京市,东城区"
            },
            "companyInfo":      {
                "addrDetail":      "山西省,太原市,小店区接我日子你在",
                "company":         "金沙洲科技",
                "companyAddrArea": "山西省,太原市,小店区",
                "companyMobile":   "0572-5563989",
                "companyNature":   "1",
                "inductionTime":   "2023-11-08",
                "industry":        "1"
            },
            "linkmanInfoList":  [{
                "mobileEn": "15785496887",
                "relation": "1",
                "nameEn":   "儿子的"
            },
                {
                    "mobileEn": "15785492887",
                    "relation": "2",
                    "nameEn":   "儿的"
                }]
        }
        if random_work_type == 3:
            req_data["companyInformation"] = {
                "companyName":    "公司名称",
                "companyType":    company_type,  # 普通民营企业
                "companyAddress": "广东省-深圳市-龙华区-民治街道榕树苑11栋"
            }
        return self.data_model(YiJieSuDaiV2MethodsEnum.SUBMIT.value[0], req_data)

    def get_conclusion_data(self, data):
        """
        :param
        :return:
        """
        hub_user_id = data.get("hubUserId")
        channel_credit_no = data.get("channelCreditNo")

        req_data = {
            "userId": hub_user_id,
            "applyNo": channel_credit_no
        }
        return self.data_model(YiJieSuDaiV2MethodsEnum.CONCLUSION.value[0], req_data)

    def get_bind_card_data(self, data):
        mobile = data.get("channelMobile")
        hub_user_id = data.get("hubUserId")
        bank_card = data.get("channelBankCardNo")
        req_data = {
            "userId": hub_user_id,
            "bankPreMobileNo": mobile,
            "bankCardNum": bank_card,
            "bankCode": "ABC",
            "bankName": "招商银行"
        }
        return self.data_model(YiJieSuDaiV2MethodsEnum.BIND_CARD.value[0], req_data)

    def get_h5_bind_data(self, data):
        hub_user_id = data.get("hubUserId")
        req_data = {
            "userId": hub_user_id,
            "callbackUrl": "http://www.baidu.com",
            "type": "BINDCARD"
        }
        return self.data_model(YiJieSuDaiV2MethodsEnum.H5_BIND.value[0], req_data)

    def get_bind_verify_data(self, data):
        mobile = data.get("channelMobile")
        hub_user_id = data.get("hubUserId")
        bank_card = data.get("channelBankCardNo")
        serial_no = data.get("hubBindCardSerialNo")
        req_data = {
            "userId": hub_user_id,
            "serialNumber": serial_no,
            "verifyCode": "123456",
            "bankCardNum": bank_card
        }
        return self.data_model(YiJieSuDaiV2MethodsEnum.BIND_VERIFY.value[0], req_data)

    def get_bind_info_data(self, data):
        # 用户绑卡列表
        hub_user_id = data.get("hubUserId")
        req_data = {
            "userId": hub_user_id,
        }
        return self.data_model(YiJieSuDaiV2MethodsEnum.BIND_INFO.value[0], req_data)

    def get_bank_list_data(self, data):
        # 银行列表
        hub_user_id = data.get("hubUserId")
        req_data = {
            "userId": hub_user_id,
        }
        return self.data_model(YiJieSuDaiV2MethodsEnum.BANK_LIST.value[0], req_data)

    def get_trial_data(self, data):
        # 借款试算
        hub_user_id = data.get("hubUserId")
        req_data = {
            "userId": hub_user_id,
            "borrowAmount": 1200.00,
            "borrowNper": 12
        }
        return self.data_model(YiJieSuDaiV2MethodsEnum.TRIAL.value[0], req_data)

    def get_confirm_order_data(self, data):
        hub_user_id = data.get("hubUserId")
        bank_card = data.get("channelBankCardNo")
        req_data = {
            "userId": hub_user_id,
            "amount": 1200.00,
            "borrowNper": 12,
            "bankCardNum": bank_card
        }
        return self.data_model(YiJieSuDaiV2MethodsEnum.CONFIRM_ORDER.value[0], req_data)

    def get_confirm_sign_data(self, data):
        hub_user_id = data.get("hubUserId")
        bank_card = data.get("channelBankCardNo")
        channel_draw_no = data.get("channelDrawNo")

        req_data = {
            "userId": hub_user_id,
            "borrowNo": channel_draw_no,
            "amount": 1200.00,
            "borrowNper": 12,
            "bankCardNum": bank_card,
            "verifyCode": "123456",
            "borrowUse": "5"
        }
        return self.data_model(YiJieSuDaiV2MethodsEnum.CONFIRM_SIGN.value[0], req_data)

    def get_loan_info_data(self, data):
        hub_user_id = data.get("hubUserId")
        draw_no = data.get("hubDrawSerialNo")
        channel_draw_no = data.get("channelDrawNo")
        req_data = {
            "userId": hub_user_id,
            "thirdBorrowNo": draw_no,
            "borrowNo": channel_draw_no
        }
        return self.data_model(YiJieSuDaiV2MethodsEnum.LOAN_INFO.value[0], req_data)

    def get_url_data(self, data):
        draw_no = data.get("hubDrawSerialNo")
        req_data = {
            "thirdBorrowNo": draw_no,  # hub放款流水号
        }
        return self.data_model(YiJieSuDaiV2MethodsEnum.GET_URL.value[0], req_data)

    def get_repay_info_data(self, data):
        draw_no = data.get("hubDrawSerialNo")
        req_data = {
            "thirdBorrowNo": draw_no,  # hub放款流水号
        }
        return self.data_model(YiJieSuDaiV2MethodsEnum.REPAY_INFO.value[0], req_data)


    @staticmethod
    def get_contract_data(data, contract_type):
        channel_user_no = data.get("channelUserNo", f"default_value_{random.randint(1, 1000)}")
        sub_no = data.get("hubSubOrderNo", f"default_value_{random.randint(1, 1000)}")
        contract_data = {
            "optType":       contract_type,
            "thirdBorrowNo": sub_no,
            "userId":        channel_user_no
        }
        return contract_data

    def get_base_contract_data(self, data):
        req_data = self.get_contract_data(data, 1)
        return self.data_model(YiJieSuDaiV2MethodsEnum.BASE_CONTRACT.value[0], req_data)

    def get_bind_contract_data(self, data):
        req_data = self.get_contract_data(data, 2)
        return self.data_model(YiJieSuDaiV2MethodsEnum.BASE_CONTRACT.value[0], req_data)

    def get_draw_contract_data(self, data):
        req_data = self.get_contract_data(data, 3)
        return self.data_model(YiJieSuDaiV2MethodsEnum.BASE_CONTRACT.value[0], req_data)

    def get_loan_contract_data(self, data):
        req_data = self.get_contract_data(data, 4)
        return self.data_model(YiJieSuDaiV2MethodsEnum.BASE_CONTRACT.value[0], req_data)
