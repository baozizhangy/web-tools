#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os

from config import db_conn
from djangoWebTools.script.script_data.risk_credit.risk_input_check import generate_join_sql
from utils.file_util import read_file


def pcr_input_check():
    record_no = "0870252161883181056"
    table_list_path = "../input_20240425/华融-人行征信-table.txt"
    # base_dir = os.path.dirname(os.path.abspath(__file__))
    # table_list_path = f"{base_dir}/{table_list_path}"
    # print(f"pcr_input_check::table_list_path:'{table_list_path}'")
    table_list = read_file(table_list_path, "line")
    sql = generate_join_sql(record_no, table_list)
    print(sql)
    exec_sql_result = db_conn("BM_SIT").select_one(sql)
    if exec_sql_result.get("code") != "0":
        return {"error": f"执行数据库资信查询语句异常：{exec_sql_result}"}
    if exec_sql_result.get("data") == 0:
        return {"error": f"数据库查询结果为空，请检查输入项记录号是否正确，record_no:'{record_no}'"}

    source_value = exec_sql_result.get("data")
    print(source_value)
    input_value = read_file(r"input_ZD301_202409260000000009.json").get("commonModel")
    print(input_value)


if __name__ == '__main__':
    res = pcr_input_check()
    print(res)