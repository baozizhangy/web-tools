#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import random
from datetime import datetime

from api.sys_inner.sys_interface import get_user_check_by_mobile_md5
from config import db_conn
from utils.cryption_util import md5_encrypt
from utils.logger_util import web_logger
from utils.personal_util import get_mobile_no, get_id_no, get_person_name, fake, get_bank_card, generate_valid_bank_card


def query_user_info_by_mobile(env, mobile=None, user_no=None):
    if not mobile and not user_no:
        return {"err": "手机号和user_no不能同时为空"}
    
    if user_no:
        user_sql = f"select mobile_no_md5 from cis.u_user where user_no = '{user_no}' limit 1;"
        mobile_md5_1 = db_conn(env).select_one(user_sql)['data']['mobile_no_md5']
        mobile_md5 = mobile_md5_1
    elif mobile:
        # 查询用户信息
        # 用手机号md5查询用户号user_no
        web_logger.info(f"用手机号md5查询用户号user_no入参::{env, mobile}")
        mobile_md5_1 = md5_encrypt(mobile)
        mobile_md5 = mobile_md5_1

    sql = f"SELECT user_no, cust_no, mobile_no, duid, mobile_no_crypt FROM cis.u_user WHERE mobile_no_md5 = '{mobile_md5}' LIMIT 1"
    get_user_res = db_conn(env).get_all(sql)
    web_logger.info(f"查询手机号md5:{mobile_md5},对应的user_no：{get_user_res}")

    default_values = {
        "user_no": "cis.u_user不存在手机号md5对应的user_no",
        "cust_no": "cis.u_user不存在手机号md5对应的cust_no",
        "duid": "cis.u_user不存在手机号md5对应的duid",
        "mobile_no": "cis.u_user不存在手机号md5对应的mobile_no",
        "mobile_no_crypt": "cis.u_user不存在手机号md5对应的mobile_no_crypt",
    }

    # 如果查询有结果，则取第一条，否则使用默认值
    user_data = get_user_res[0] if get_user_res else default_values
    # 解构字段
    user_no = user_data["user_no"]
    cust_no = user_data["cust_no"]
    duid = user_data["duid"]
    mobile_no = user_data["mobile_no"]
    mobile_no_crypt = user_data["mobile_no_crypt"]
    apply_sql = f"select partner_user_no,partner_channel_apply_no from hub.hub_channel_bm_apply where user_no = '{user_no}';"
    get_apply_res = db_conn(env).select_one(apply_sql)
    apply_data = get_apply_res['data']
    # # if user_no != "不存在手机号md5对应的user_no":
    # check_result = get_user_check_by_mobile_md5(mobile_md5, user_no)
    # if check_result.get("flag", "") != "S":
    #     return {"err": "/clg/test/hub/test/channel/table接口异常"}
    # check_table = check_result.get("data")
    # web_logger.info(f"调用准入落表查询::mobile_md5::{mobile_md5},user_no::{user_no},结果::{check_result}")
    partner_user_no = apply_data['partner_user_no']
    partner_channel_apply_no = apply_data['partner_channel_apply_no']
    res = {
        "手机号MD5": mobile_md5,
        "手机号加密": mobile_no,
        "手机号md5AES加密": mobile_no_crypt,
        "user_no": user_no,
        "cust_no": cust_no,
        "duid": duid,
        "渠道方user_no":partner_user_no,
        "渠道方授信流水":partner_channel_apply_no

        # "准入分表/加密结果": check_table,
    }
    return res


def generate_random_user_info():
    # 生成虚拟用户信息
    res = {
        "channelMobile": get_mobile_no(),
        "channelIdNo": get_id_no(),
        "channelCustName": get_person_name(),
        "channelBankCardNo": generate_valid_bank_card('62020017'),
        "channelUserNo": int(datetime.now().strftime('%m%d%H%f')[:-3]),
        "channelCheckNo": random.randint(100000, 999999),
        "channelCreditNo": random.randint(100000, 999999),
        "channelDrawNo": random.randint(100000, 999999),
        "channelRepayNo": random.randint(100000, 999999)
    }
    return res


def random_user_info(**kwargs):
    def get_param_value(key, value=None):
        if key == "name":
            return get_person_name() if value is None else value
        elif key == "mobile":
            return get_mobile_no() if value is None else value
        elif key == "id_no":
            return get_id_no() if value is None else value
        elif key == "card_no":
            return fake.credit_card_number() if value is None else value
        elif key == "email":
            return fake.email() if value is None else value
        elif key == "education":
            return fake.job() if value is None else value
        elif key == "marital_status":
            return random.choice(["已婚有子女", "已婚无子女", "未婚", "离异"]) if value is None else value
        elif key == "income":
            return random.choice(["3000以下", "3000-6000", "6000-10000", "10000-30000", "30000以上"]) \
                if value is None else value
        elif key == "loan_usage":
            return random.choice(["购物", "装修", "旅游", "买车", "教育", "结婚", "医疗", "其他"]) \
                if value is None else value
        elif key == "debt_situation":
            return random.choice(["无负债", "0-3000", "3000-6000", "6000-10000", "10000-15000", "15000-20000", "20000"]) \
                if value is None else value
        elif key == "local_hk_type":
            return random.choice(
                ["本地城市户口", "外地城市户口", "本地农村户口", "外地农村户口"]) if value is None else value
        elif key == "address":
            return "浙江省-杭州市-西湖区" if value is None else value
        elif key == "address_type":
            return random.choice(["租房", "产权房产", "公司宿舍", "和家人同住", "其他"]) if value is None else value
        elif key == "address_detail":
            return fake.address().replace(" ", "") if value is None else value
        elif key == "longitude":
            return round(random.uniform(73.66, 135.05), 6) if value is None else value
        elif key == "latitude":
            return round(random.uniform(18.16, 53.56), 6) if value is None else value
        elif key == "company_name":
            return fake.company() if value is None else value
        elif key == "company_address":
            return "浙江省-杭州市-西湖区" if value is None else value
        elif key == "company_address_detail":
            return fake.address().replace(" ", "") if value is None else value
        elif key == "company_nature":
            return random.choice(
                ["政府或企事业单位", "国企央企", "外资企业", "上市公司", "普通民营企业", "个体工商户", "其他"]) \
                if value is None else value
        elif key == "job_industry":
            return random.choice(
                ["信息传输/软件/信息技术服务业", "金融业", "建筑业", "房地产", "批发/零售业", "教育",
                 "文化/体育/娱乐业",
                 "卫生/社会工作", "电力/热力/燃气/水生产/供应业", "农业", "制造业", "居民服务/修理/其他服务业",
                 "公共管理/社会保障/社会组织/国际组织", "住宿/餐饮业", "其他"])
        elif key == "job_category":
            return random.choice(["上班", "企业主", "个体户", "兼职", "无业"]) if value is None else value
        elif key == "company_phone":
            # 021+9位数字
            return f"021-{random.randint(100000000, 999999999)}" if value is None else value
        elif key == "residence_status":
            return random.choice(["租房", "产权房产", "公司宿舍", "和家人同住", "其他"]) if value is None else value
        elif key == "rent":
            return random.randint(100, 99999) if value is None else value
        elif key == "loan_purpose":
            return random.choice(
                ["购物", "装修", "旅游", "买车", "教育", "结婚", "医疗", "其他"]) if value is None else value
        elif key == "expected_loan_period":
            return random.choice(["3", "6", "9", "12", "24", "32"]) if value is None else value
        elif key == "expected_loan_amount":
            return random.randint(10000, 999999) if value is None else value
        elif key == "repay_source":
            return random.choice(["工资", "经营收入", "投资收入", "房租收入", "其他"]) if value is None else value
        elif key == "contact_1_name":
            return fake.name() if value is None else value
        elif key == "contact_1_mobile":
            return get_mobile_no() if value is None else value
        elif key == "contact_2_name":
            return fake.name() if value is None else value
        elif key == "contact_2_mobile":
            return get_mobile_no() if value is None else value
        elif key == "channel_user_no":
            return int(datetime.now().strftime('%m%d%H%f')[:-3]) if value is None else value
        elif key == "channel_check_no":
            return random.randint(100000, 999999) if value is None else value
        elif key == "channel_register_no":
            return random.randint(100000, 999999) if value is None else value
        elif key == "channel_credit_no":
            return random.randint(100000, 999999) if value is None else value
        elif key == "channel_draw_no":
            return random.randint(100000, 999999) if value is None else value
        elif key == "channel_reapy_no":
            return random.randint(100000, 999999) if value is None else value
        # 若无需处理的参数，则生成时间戳
        else:
            return int(datetime.now().strftime('%m%d%H%f')[:-3])

    if kwargs:
        return {key: get_param_value(key, value) for key, value in kwargs.items()}

    # 如果没有传入参数，返回所有默认参数的值
    all_params = [
        "name", "mobile", "id_no", "card_no", "email", "education", "marital_status", "income", "loan_usage",
        "debt_situation", "local_hk_type", "address", "address_type", "address_detail", "longitude", "latitude",
        "company_name", "company_address", "company_address_detail", "company_nature", "job_industry", "job_category",
        "company_phone", "residence_status", "rent", "loan_purpose", "expected_loan_period", "expected_loan_amount",
        "repay_source", "contact_1_name", "contact_1_mobile", "contact_2_name", "contact_2_mobile", "channel_user_no",
        "channel_check_no", "channel_register_no", "channel_credit_no", "channel_draw_no", "channel_reapy_no"]
    return {param: get_param_value(param) for param in all_params}


if __name__ == '__main__':
    print(query_user_info_by_mobile('BM_SIT','13083666916', user_no='UR0963686838071996416'))
