#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from config import db_conn
from utils.file_util import read_file

table_list = ["br_hx_at_d7_cell_orgnum", "br_hx_at_d7_cell_orgnum_g", "br_hx_at_d7_id_orgnum", "br_hx_at_d7_id_orgnum_g", "br_hx_at_d7_p7_cell_allnum", "br_hx_at_d7_p7_cell_orgnum", "br_hx_at_d7_p7_id_allnum", "br_hx_at_d7_p7_id_orgnum", "br_hx_at_d15_cell_orgnum", "br_hx_at_d15_cell_orgnum_g", "br_hx_at_d15_id_orgnum", "br_hx_at_d15_id_orgnum_g", "br_hx_at_d15_p15_cell_allnum", "br_hx_at_d15_p15_cell_orgnum", "br_hx_at_d15_p15_id_allnum", "br_hx_at_d15_p15_id_orgnum", "br_hx_at_m1_cell_orgnum", "br_hx_at_m1_cell_orgnum_g", "br_hx_at_m1_id_orgnum", "br_hx_at_m1_id_orgnum_g", "br_hx_at_m1_p1_cell_allnum", "br_hx_at_m1_p1_cell_orgnum", "br_hx_at_m1_p1_id_allnum", "br_hx_at_m1_p1_id_orgnum", "br_hx_at_m3_cell_orgnum", "br_hx_at_m3_cell_orgnum_g", "br_hx_at_m3_id_orgnum", "br_hx_at_m3_id_orgnum_g", "br_hx_at_m3_p3_cell_allnum", "br_hx_at_m3_p3_cell_orgnum", "br_hx_at_m3_p3_id_allnum", "br_hx_at_m3_p3_id_orgnum", "br_hx_at_m6_cell_orgnum", "br_hx_at_m6_id_orgnum", "br_hx_at_m6_p6_cell_allnum", "br_hx_at_m6_p6_cell_orgnum", "br_hx_at_m6_p6_id_allnum", "br_hx_at_m6_p6_id_orgnum"]


def generate_join_sql(table_list, _record_no, db_name='crs'):
    # 生成关联查询的SQL
    first_table = table_list[0]
    join_sql = f"SELECT * FROM {db_name}.{first_table}"

    for table in table_list[1:]:
        join_sql += f" LEFT JOIN {db_name}.{table} ON {db_name}.{table}.record_no = {db_name}.{first_table}.record_no"
    join_sql += f" WHERE {db_name}.{first_table}.record_no = {_record_no} ;"
    return join_sql


def get_origin_data():
    file_data = read_file("百融_借贷意向_0905.json")
    return file_data


def compare_run():
    sql = generate_join_sql(table_list, "0857036890371723264")
    exec_sql_result = db_conn(env="SIT").select_one(sql)
    table_data = exec_sql_result.get("data", {})

    origin_data = get_origin_data()
    print(f"origin_data::\n{origin_data}")

    # 获取两个数据源的键集合
    table_keys = set(table_data.keys())
    origin_keys = set(origin_data.keys())

    # 共同的键
    common_keys = table_keys.intersection(origin_keys)

    # 独有的键
    table_unique_keys = table_keys - origin_keys
    origin_unique_keys = origin_keys - table_keys

    # 存储值不同的键
    differing_values = []
    table_unique_values = {}
    origin_unique_values = []

    # 比较共同的键
    for key in common_keys:
        if table_data[key] != origin_data[key]:
            differing_values.append({
                "key": key,
                "origin_data": origin_data[key],
                "table_data": table_data[key]
            })

    # 收集独有的键
    for key in table_unique_keys:
        table_unique_values[key] = table_data[key]

    for key in origin_unique_keys:
        origin_unique_values.append({
            "key": key,
            "value": origin_data[key]
        })

    # 输出不同的部分
    if differing_values:
        print("Differing values:")
        for item in differing_values:
            print(item)
    else:
        print("No differing values found.")

    def filter_dict(original_dict, filter_list):
        return {key: value for key, value in original_dict.items() if not any(f in key for f in filter_list)}

    filter_list = ['record_no', 'created_by', 'date_updated', 'updated_by', 'date_created', 'id']

    # 输出独有的键
    if table_unique_values:
        print(f"table_unique_values:\n{filter_dict(table_unique_values, filter_list)}")

    if origin_unique_values:
        print(f"origin_unique_values:\n{origin_unique_values}")


if __name__ == '__main__':
    compare_run()