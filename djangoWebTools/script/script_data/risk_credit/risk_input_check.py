#!/usr/bin/env python
# -*- coding: UTF-8 -*-


"""
record_no 查询关联的输入项
1、生成查询sql语句
2、执行sql语句，获取落表资信的值
3、将映射关系中存在的资信值转化为输入项预期值
4、对比预期值与widek实际获取的值，存在差异则输出到文件中
"""

import json
import os

import requests

from config import db_conn
from utils.file_util import read_file
# from config import widek_token

headers = {
    "Accept":          "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection":      "keep-alive",
    "Content-Type":    "application/json;charset=UTF-8",
    "Origin":          "http://widek-sit.xurongwl.com",
    "Referer":         "http://widek-sit.xurongwl.com/strategy-manager/risk-manager/RuleTest",
    "User-Agent":      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
}

intf_table_mapping = {
    "": ""
}

#
# def get_widek_risk_input(module, biz_type, rule_set_no, biz_no, input_widek_token=None):
#     # 获取 widek：策略-风险管理-规则测试，所获取的输入项
#     url = 'http://widek-sit.xurongwl.com/widek-api/manage/des/decision/inputjson/query2'
#     # BM URL
#     url = 'http://widek-bm-sit.xurongwl.com/widek-api/manage/des/decision/inputjson/query2'
#     admin_token = widek_token
#     if input_widek_token:
#         admin_token = input_widek_token
#     cookies = {"Admin-Token": admin_token, }
#     data = {
#         "module":    module,
#         "bizType":   biz_type,
#         "ruleSetNo": rule_set_no,
#         "bizNo":     biz_no
#     }
#     data = json.dumps(data, separators=(',', ':'))
#
#     # 发送GET请求
#     response = requests.post(url, headers=headers, cookies=cookies, data=data)
#     if response.status_code != 200:
#         return {"code": "999", "msg": "接口调用失败，错误信息", "error": response.json()}
#     if response.json().get("code") != 200:
#         return {"code":  "998", "msg": f"接口返回失败，token失效，获取对应环境widek登录状态下的admin-token传递",
#                 "error": response.json()}
#
#     risk_res = json.loads(json.loads(response.text).get("data"))
#     return {"code": "000", "data": risk_res.get("commonModel")}


def generate_join_sql(_record_no, table_names, db_name='crs'):
    # 生成关联查询的SQL
    first_table = table_names[0]
    join_sql = f"SELECT * FROM {db_name}.{first_table}"

    for table in table_names[1:]:
        join_sql += f" LEFT JOIN {db_name}.{table} ON {db_name}.{table}.record_no = {db_name}.{first_table}.record_no"
    join_sql += f" WHERE {db_name}.{first_table}.record_no = {_record_no} ;"
    return join_sql


def replace_db_credit_to_mapping_keys(mapping, db_credit_dict):
    # 将数据库中资信的字段名替换为输入项的字段名，并进行过滤，将替换后的结果和缺失的字段返回
    expect_data = {}
    missing_data = []
    print(f"数据库中查询的输入项为：{db_credit_dict}")
    for key, value in mapping.items():
        if key in db_credit_dict:
            expect_data[mapping[key]] = db_credit_dict[key]
        else:
            missing_data.append([mapping[key]])
    # print(f"查询落表资信中缺失映射字段或值，检查excel文件:{missing_data}")

    return {"expect_data": expect_data, "missing_data": missing_data}


def compare_input_value(expect_dict: dict, input_dict: dict):
    # 预期输入项值与实际输入项值对比，返回不一致的键值对
    result = {}

    for key, value in expect_dict.items():
        if key not in input_dict or input_dict[key] != value:
            result[key] = value

    return result


def run_compare(env, record_no, table_list_path, mapping_path, mapping_page, widek_input_json, is_return_expect):
    # 输入项对比
    # 获取当前文件的绝对路径
    compare_result = {}
    base_dir = os.path.dirname(os.path.abspath(__file__))
    table_list_path = f"{base_dir}/{table_list_path}"
    print(f"run_compare::table_list_path:'{table_list_path}'")
    table_list = read_file(table_list_path, "line")
    sql = generate_join_sql(record_no, table_list)
    print(f"generate_join_sql:'{sql}'")
    exec_sql_result = db_conn(env).select_one(sql)
    print(f"exec_sql_result::'{exec_sql_result}'")
    if exec_sql_result.get("code") != "0":
        return {"error": f"执行数据库资信查询语句异常：{exec_sql_result}"}
    if exec_sql_result.get("data") == 0:
        return {"error": f"数据库查询结果为空，请检查输入项记录号是否正确，record_no:'{record_no}'"}

    # 获取对标资信表列表，查询的结果合集
    db_credit_dict = exec_sql_result.get("data")
    print(f"db_credit_dict：{db_credit_dict}")

    mapping_path = f"{base_dir}/{mapping_path}"
    print(f"run_compare::mapping_path:'{mapping_path}'")
    mapping_data = read_file(mapping_path)
    # 读取映射关系，从需求中提取为输入项变量名：input_key、表中字段名/资信变量名：credit_key 两列，放到Sheet1页
    # 验证res是否为字典且包含'Sheet1'
    if not isinstance(mapping_data, dict) or mapping_page not in mapping_data:
        # raise ValueError("Invalid data structure or missing 'Sheet1' sheet.")
        return {f"映射关系excel文件:'{mapping_path}'中不存在页:'{mapping_page}' "}

    key_mapping = {item['credit_key']: item['input_key'] for item in mapping_data[mapping_page]}

    replace_data = replace_db_credit_to_mapping_keys(key_mapping, db_credit_dict)
    expect_input = replace_data.get("expect_data")
    missing_data = replace_data.get("missing_data")
    # print(f"期望输入项:{expect_input}")
    # print(f"缺失映射关系或值:{missing_data}")

    # 现输入项的值
    # widek_input = read_file(widek_input_json_path).get("commonModel")
    difference_data = compare_input_value(expect_input, widek_input_json)
    print(f"widek获取的输入项与数据库中差异：{difference_data}")
    compare_result["差异项"] = difference_data
    compare_result["缺失映射关系或值"] = missing_data
    if is_return_expect == "1":
        compare_result["期望输入项"] = expect_input
    return compare_result


def main_tc_mix():
    # 信用司南mix 输入项测试启动点
    env = "SIT"
    record_no = "0771907924023476224"
    widek_input_json_path = "input_20240425/widek-240424-input-tds-301.json"
    mapping_path = "input_20240425/input-240424-mapping.xlsx"

    tc_mix_table_list_path = "input_20240425/天创-信用司南mix-credit_table_list-240424.txt"
    tc_mix_mapping_page = "天创-信用司南mix"  # 天创-信用司南mix  百融-反欺诈-特殊名单  百融-特殊名单
    tc_mix_res = run_compare(env, record_no, tc_mix_table_list_path, mapping_path, widek_input_json_path,
                             tc_mix_mapping_page)
    print(f"天创-信用司南mix对比输入项执行结果，存在差异的输入项::{tc_mix_res}")


def main_br_special():
    # 百融-特殊名单 输入项测试启动点
    env = "SIT"
    record_no = "0743923906093842432"
    widek_input_json_path = "input_20240425/widek-240424-input-tds-301.json"
    mapping_path = "input_20240425/input-240424-mapping.xlsx"

    br_special_table_list_path = "input_20240425/百融-特殊名单-credit_table_list-240424.txt"
    br_special_mapping_page = "BrSpecial"  # 天创-信用司南mix  百融-反欺诈-特殊名单  百融-特殊名单
    br_special_res = run_compare(env, record_no, br_special_table_list_path, mapping_path,
                                 widek_input_json_path, br_special_mapping_page)
    print(f"百融-特殊名单对比输入项执行结果，存在差异的输入项::{br_special_res}")


def main_br_hx():
    # 百融-特殊名单 输入项测试启动点
    env = "SIT"
    record_no = "0743358064553689088"
    widek_input_json_path = "input_20240425/widek-240424-input-tds-301.json"
    mapping_path = "input_20240425/input-240424-mapping.xlsx"

    br_hx_table_list_path = "input_20240425/百融-特殊名单-credit_table_list-240424.txt"
    br_hx_mapping_page = "BrSpecial_order"  # 天创-信用司南mix  百融-反欺诈-特殊名单  百融-特殊名单
    br_special_res = run_compare(env, record_no, br_hx_table_list_path, mapping_path,
                                 widek_input_json_path, br_hx_mapping_page)
    print(f"百融-反欺诈-特殊名单对比输入项执行结果，存在差异的输入项::{br_special_res}")

#
# def check_input_data(env, biz_no, intf_type, module="TDS", biz_type="DIST", rule_set_no="TDS-301",
#                      widek_token="", is_return_expect="0"):
#     # 根据 biz_no （appl_no）查询数据库中数据，对比输入项，返回差异项
#     # 输入项映射关系excel配置
#     mapping_path = "input_20240425/input-240424-mapping.xlsx"
#     table_list_path_mapping = {
#         "TcCreditMix": "script_data/input_20240425/天创-信用司南mix-credit_table_list-240424.txt",
#         "BrSpecial": "script_data/input_20240425/百融-特殊名单-credit_table_list-240424.txt",
#         "BrHxStrategy": "script_data/input_20240425/百融-借贷意向-credit_table_list-20240521.txt",
#         "HuaRongPcr": "./input_20240425/华融-人行征信-table.txt",
#     }
#     check_result = {}
#     print(f"biz_no:'{biz_no}'")
#     record_no_sql = f"SELECT record_no FROM crs.cr_query_info WHERE appl_no = '{biz_no}' AND intf_type = '{intf_type}' "
#     print(f"record_no_sql:'{record_no_sql}'")
#     exec_sql_result = db_conn(env).select_one(record_no_sql)
#     print(f"exec_sql_result:'{exec_sql_result}'")
#
#     if exec_sql_result.get("code") != "0":
#         return {"error": f"执行数据库查询语句异常：{exec_sql_result}"}
#     if exec_sql_result.get("data") == 0:
#         return {"error": f"数据库中不存在 {biz_no} 对应 {intf_type} 的记录"}
#
#     record_no = exec_sql_result.get("data").get("record_no")
#     print(f"record_no:'{record_no}'")
#     widek_input_res = get_widek_risk_input(
#         module=module, biz_type=biz_type, rule_set_no=rule_set_no, biz_no=biz_no, input_widek_token=widek_token)
#     print(f"widek获取的输入项code：{widek_input_res.get('code')}")
#     if widek_input_res.get("code") != "000":
#         check_result["获取widek输入项异常"] = widek_input_res
#         return check_result
#     widek_input = widek_input_res.get("data")
#     print(f"widek获取的输入项data：{widek_input}")
#
#     if intf_type in table_list_path_mapping:
#         table_list_path = table_list_path_mapping[intf_type]
#     else:
#         check_result["无该资信配置"] = intf_type
#         return check_result
#     print(f"table_list_path::{table_list_path}")
#     compare_res = run_compare(env, record_no, table_list_path, mapping_path, intf_type, widek_input, is_return_expect)
#     check_result["输入项对比结果"] = compare_res
#     return check_result


# if __name__ == '__main__':
    # input_data = get_widek_risk_input(
    #     module="TDS", biz_type="DIST", rule_set_no="TDS-301", biz_no="202404090000000004",
    #     input_widek_token="eyJhbGciOiJSUzI1NiJ9.eyJ1c2VyTmFtZSI6InppeXVhbiIsImV4cCI6MTczMDc5NjA1NiwibG9naW5fdXNlcl9rZXkiOiJhZjNhYzJhZi1mODAxLTRhYjgtOTE4NC00NWIyMzU0NmNiZTYifQ.Pv4RKPfP5LGrf6M4db8MB9OSFKJTfRhKeHhOuG-1z-2OyMJMfvo06xHqUXc3sL4BT3CC42dk-OWwi6h3ZtXQkRsqRs8PJA9stKDvO3xvsF3Z-BmitD7j6cAou5IrtTfQagP6OyrAUGCcVM3dQ2d3bMeNzlbORTj8wRUkRYEvoUzh4mkwPUEWEUz9PLRUnEwVn70QWJkxZGIYdoASS8j3LPz6Jx4p_YDqCp4MY79uwXlvc6jnu2Db7XTs3NZQnkPWKhfpaN_Voy25KIT6qo5oSiVCU7dj8hOlEXAoIW6myGYwJPB_0lRfa1vdqlJJ74E0ki-bwBoloiguwt4-nWqtRg"
    # )
    # print(f"input_data::{input_data}")
    # check_res = check_input_data("SIT", "202404090000000004", "TcCreditMix")
    # print(f"check_res::{check_res}")
    # token_1008 = "eyJhbGciOiJSUzI1NiJ9.eyJ1c2VyTmFtZSI6InppeXVhbiIsImV4cCI6MTc0MzIzMDQxNCwibG9naW5fdXNlcl9rZXkiOiJlODE3YzZiMy1lOGQ1LTQzOGQtODk4MS1hMDRiOWMyNWE2NWUifQ.dum9woksZ7h5AzL0NiZ4vSLYWU7GwjcHC2-xPzGvynJyNq-D2sTZisxRYcT9QvouTFzxfd2431Rv54SWd97kB3Q6Kye8_3_8f-7V6wlkXu8K4GbaLt9zXzAAvEowsI7t7VXp_I7bFM674RDz2edw3TOFe6oActxyiezj92OCwFuL-1N9Dftfai6JAmnxIGHVTsrH6bT_jQj0ahh1QSC7LhES8ZKAreQZ7E9INSLlZuUvnvldyB_gq8ihHXv33M8NOTWquFleDdU2OcmapT2iU2dzagVGp978auuerEIIjLrAxRYvX7FDV9VTNFu7OYUANt6PcuwYmEI0rhgSG1Y7CQ; Refresh-Token=eyJhbGciOiJIUzUxMiJ9.eyJ1c2VyTmFtZSI6InppeXVhbiIsImV4cCI6MTc0MzIzMDQxNCwibG9naW5fdXNlcl9rZXkiOiJlODE3YzZiMy1lOGQ1LTQzOGQtODk4MS1hMDRiOWMyNWE2NWUifQ.TpkVO7TA4ERrmzXNGFOxYOpIjRssYFnGwtxjb14onMEPlVGxZEtdTKKLNdc75o-IldLBys7A-65Zg3OEZAnTSQ"
    #
    # # check_res = check_input_data("BM_SIT", "202409260000000009", "HuaRongPcr",
    # #                              "APV", "DRAW", "ZD-701", widek_token=token_1008, is_return_expect="1"
    # #                              )
    #
    # check_res = check_input_data("BM_SIT", "JT202410080000000003", "HuaRongPcr",
    #                              "APV", "DRAW", "ZD-701", widek_token=token_1008,
    #                              )
    # print(f"check_res::{check_res}")
    # ...
