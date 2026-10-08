import datetime
import json
import random
import re


from utils.logger_util import web_logger
from utils.personal_util import get_id_no, get_person_name, get_gender, get_birthday, get_address, get_mobile_no, fake


class ResultBase:
    """
    返回结果基类
    """
    pass


#
# def generate_ocr_info(id_no=None, name=None, ocr_mode=None, ocr_type=0,
#                       upload_type=1, ocr_partner="weizhong", flow_no="", ocr_info=None, card_image=None):
#     # 生成OCR信息，身份证正反面标识（0-正面 1-反面）
#     """
#     ocr_mode:身份证正反面标识（0-正面 1-反面）
#     ocr_partner: 1-扫描 2-照片
#     ocr_type: 上传类型 1-正常上传 2-补传"""
#     # if id_no is None or len(id_no) < 18:
#     #     id_no = get_id_no()
#     # if name is None:
#     #     name = get_person_name()
#     card_front_image = "http://private-sit.oss-cn-shanghai.aliyuncs.com/private-sit/ocr/ks/5784/1726277925893/JdexwC/id_image.jpg"
#     card_back_image = "http://private-sit.oss-cn-shanghai.aliyuncs.com/private-sit/ocr/ks/5784/1726277933311/Bf0d9f/id_image_back.jpg"
#     print(f"generate_ocr_info::id_no:{id_no}")
#     if ocr_mode == 0:
#         # 身份证正面信息
#         ocr_front_info = {
#             "name":        name,
#             "gender":      get_gender(id_no),
#             "nationality": "汉",
#             "birth":       get_birthday(id_no),
#             "idCard":      id_no,
#             "address":     "上海市浦东新区陆家嘴街道双子大楼911号",
#         }
#         if ocr_info is None:
#             ocr_info = ocr_front_info
#         if card_image is None:
#             card_image = card_front_image
#     if ocr_mode == 1:
#         # 身份证反面信息
#         ocr_back_info = {
#             "authority": "上海公安局",
#             "validDate": "20221001-20421001"
#         }
#         if ocr_info is None:
#             ocr_info = ocr_back_info
#         if card_image is None:
#             card_image = card_back_image
#     return {
#         "ocrImageUrl": card_image,
#         "ocrType":     ocr_type,
#         "ocrMode":     ocr_mode,
#         "uploadType":  upload_type,
#         "ocrPartner":  ocr_partner,
#         "flowNo":      flow_no,
#         "ocrInfo":     json.dumps(ocr_info, ensure_ascii=False)
#     }


def generate_contact_info(standard_marriage=None, relation_1=None, relation_2=None):
    # 定义直系联系人关系
    # relationship_1_options对应key 已婚无子女 = 04, 已婚有子女 = 03, 未婚 = 01, 离异 = 02
    # 对应value:'父亲'01, '母亲'02, '配偶'03, '儿子'04, '女儿'04,朋友06
    relationship_1_options = {
        '04': ['01', '02', '03'],
        '03': ['01', '02', '03', '04', '05'],
        '01': ['01', '02'],
        '02': ['01', '02', '03', '04', '05']
    }
    if standard_marriage is None:
        standard_marriage = random.choice(list(relationship_1_options.keys()))

    contact_1_relation = random.choice(relationship_1_options[standard_marriage])
    contact_2_relation_list = relationship_1_options[standard_marriage] + ['06']
    if relation_1:
        contact_1_relation = relation_1

    contact_2_relation_list.remove(contact_1_relation)
    contact_2_relation = random.choice(contact_2_relation_list)
    if relation_2:
        contact_2_relation = relation_2

    contact_default = {
        "standardMarriage": standard_marriage,
        "contactInfos": {
            "contactOneRel": contact_1_relation,
            "contactOneTel": get_mobile_no(),
            "contactOneName": "测试一",
            "contactTwoName": "测试二",
            "contactTwoRel": contact_2_relation,
            "contactTwoTel": "17712344321"  # get_mobile_no()
        }
    }
    return contact_default

#
# def generate_profile_info(has_list: list = None):
#     company_nature_list = ["政府或企事业单位", "国企央企", "外资企业", "上市公司", "普通民营企业", "个体工商户",
#                            "其他"]
#     standard_job_list = ["上班", "兼职", "企业主", "个体户", "无业"]
#     standard_debt_situation_list = ["无负债", "0-3000", "3000-6000", "6000-10000", "10000-15000", "15000-20000",
#                                     "20000"]
#     income_list = ["3000以下", "3000-6000", "6000-10000", "10000-30000", "30000以上"]
#     address_type_list = ["租房", "产权房产", "公司宿舍", "和家人同住", "其他"]
#     standard_industry_list = ["信息传输/软件/信息技术服务业", "金融业", "建筑业", "房地产", "批发/零售业", "教育",
#                               "文化/体育/娱乐业", "卫生/社会工作", "电力/热力/燃气/水生产/供应业", "农业", "制造业",
#                               "居民服务/修理/其他服务业", "公共管理/社会保障/社会组织/国际组织", "住宿/餐饮业", "其他"]
#     standard_loan_purpose_list = ["购物", "装修", "旅游", "买车", "教育", "结婚", "医疗", "其他"]
#     education_list = ["研究生或以上", "大学专科", "大学本科", "初中及以下", "高中或中专"]
#     HkType_list = ["本地城市户口", "外地城市户口", "本地农村户口", "外地农村户口"]
#     repay_source_list = ["工资"]
#     loan_term = [3, 6, 9, 12]
#     autoAddress= "上海市-上海市辖区-浦东新区"
#     addressDetail = "上海市浦东新区花木街道杨高南路辅路中国石化上海浦东科研信息办公综合基地"
#
#     # address = f"{fake.province()}-{fake.city_name()}-{fake.district()}"
#     address = "浙江省-杭州市-西湖区"
#     # address1 = fake.address().replace(' ', '')
#     standard_company_nature = random.choice(company_nature_list)
#     # company_name = fake.company()
#     # standard_job = random.choice(standard_job_list)
#     # standard_debt_situation = random.choice(standard_debt_situation_list)
#     # address2 = re.sub(r'[^\u4e00-\u9fa5\s]', '', address1)
#     # addressDetail = re.sub(r'[^\u4e00-\u9fa5\s]', '', address2)
#     # company_address = f"{fake.province()}-{fake.city_name()}-{fake.district()}"
#     company_address = address
#
#     # company_address_detail = f"{company_address}{fake.street_address()}"
#     # company_address_detail = re.sub(r'[^\w\s]', '', f"{company_address}{fake.street_address()}")
#
#     # company_address_detail = f"{company_address}{fake.street_address()}".replace('-', '')
#     standard_income = random.choice(income_list)
#     address_type = random.choice(address_type_list)
#     # standard_telephone = f"021-{fake.phone_number()}"
#     standard_telephone = f"052112345678"
#     standard_industry = random.choice(standard_industry_list)
#     standard_loan_purpose = random.choice(standard_loan_purpose_list)
#     education = random.choice(education_list)
#     # email = fake.email()
#     # employed_date = fake.date()
#     hk_type = random.choice(HkType_list)
#     repay_source = random.choice(repay_source_list)
#
#     profile_default = {
#         "address": address,
#         "companyNature": standard_company_nature,
#         "companyName": company_name,
#         "job": standard_job,
#         "debtSituation": standard_debt_situation,
#         "addressDetail": addressDetail,
#         "companyAddress": company_address,
#         "companyAddressDetail": company_address_detail,
#         "income": standard_income,
#         "repaySource": repay_source,
#         "companyTelephone": standard_telephone,
#         "industry": standard_industry,
#         "employedDate": employed_date,
#         "loanPurpose": standard_loan_purpose,
#         "education": education,
#         "email": email,
#         "residenceCity": address,
#         "residenceStatus": address_type,
#         "localHkType": hk_type
#     }
#     profile_info = {}
#     if has_list:
#         for key in has_list:
#             if key in profile_default:
#                 profile_info[key] = profile_default[key]
#             else:
#                 web_logger.info("意外的输入项")
#         return profile_info
#     else:
#         return profile_default


def insert_face(db_conn, user_no, channel_id):
    print(f"db_conn: {db_conn}, user_no: {user_no}, channel_id: {channel_id}")
    # user_no = "UR056596"
    detect_no = f"DT_test_{random.randrange(1000000, 9999999)}"
    his_no = f"HIS{detect_no}"
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    by = "auto_test"
    face_image = "http://private-sit.oss-cn-shanghai.aliyuncs.com/private-sit/live/ks/UR0678422985435332608/1698736513281/zuS2t4/1.jpeg"
    face_detect_basic_data = '{"attackResult":{"result":false,"score":0.26,"threshold":0.5},"bizNo":"","images":{"imageBest":"xxxxxxxxxxx"},"requestId":"1531397565,39b19451-393c-4fc4-8fae-6dc74b2b00d7","resultCode":1000,"resultMessage":"SUCCESS","riskInfo":{"deviceInfoLevel":"2","deviceInfoTags":{"isHook":1,"isInjection":1,"isRoot":0,"isVirtualEnvironment":1}},"timeUsed":1448,"verification":{"idcard":{"confidence":86.63057,"thresholds":{"1e-3":62.168713,"1e-4":69.31534,"1e-5":74.39926,"1e-6":78.038055}}}}'
    u_face_detect_sql = """
        INSERT INTO cis.u_face_detect (
            detect_no, user_no, face_package, face_image, face_feature,
            start_time, end_time, detect_type, rel_flow_no, detect_state, fail_code,
            fail_msg, face_partner, date_created, created_by, date_updated, updated_by,
            score, channel_id, face_detect_basic_data, extention
        )
        VALUES ('{detect_no}', '{user_no}','',
         '{face_image}', 
         '88', '{now_time}', '{now_time}', 'APPL',
         '', 'S', '1000', 'SUCCESS', 'kuangshi', '{now_time}', '{by}', '{now_time}', '{by}', '99', '{channel_id}', 
         '{face_detect_basic_data}', '')
    """.format(detect_no=detect_no, user_no=user_no, face_image=face_image, now_time=now_time, by=by,
               channel_id=channel_id,
               face_detect_basic_data=face_detect_basic_data)
    print(f"u_face_detect_sql:{u_face_detect_sql}")
    # print(f"cis_conn::{cis_conn}")
    detect_res = db_conn.exec_one(u_face_detect_sql)
    assert detect_res.get("code") == "0"
    # print(f"detect_res::{detect_res}")

    his_sql = """
        INSERT INTO cis.u_face_detect_his (
            detect_his_no, detect_no, user_no, face_package, face_image, face_feature,
            start_time, end_time, detect_type, rel_flow_no, detect_state, fail_code,
            fail_msg, face_partner, date_created, created_by, date_updated, updated_by,
            score, channel_id, face_detect_basic_data, extention
        )
        VALUES (
            '{his_no}', '{detect_no}', '{user_no}', NULL, '{face_image}', '78.038055', '{now_time}', '{now_time}', 'APPL',
             NULL, 'S', '1000', 'SUCCESS', 'kuangshi', '{now_time}', '{by}', '{now_time}', '{by}', '88', '{channel_id}',
            '{basic_data}', NULL
        )
    """.format(his_no=his_no, detect_no=detect_no, user_no=user_no, face_image=face_image, now_time=now_time, by=by,
               channel_id=channel_id,
               basic_data=face_detect_basic_data)
    his_res = db_conn.exec_one(his_sql)
    print(f"his_res::{his_res}")
    return detect_res


if __name__ == '__main__':
    print(generate_contact_info())
