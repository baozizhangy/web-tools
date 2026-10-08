import json
from collections import defaultdict

from utils.file_util import read_file

# 定义数据
data = read_file("easymock-sit-gos.json")

# 处理三个表的 insert 语句
interface_values = defaultdict(list)
method_values = []
data_values = []
project_id = "64eed9a6802f2b00233fa9cb"
system = "sit_gos"

for mock in data["data"]["mocks"]:
    point_split = mock["url"].split(".")
    if len(point_split) < 3:
        continue
    group = point_split[-2]
    interface_class = point_split[-1].split("/")[0]
    method = point_split[-1].split("/")[1]

    key = (project_id, system, group, interface_class)
    if key not in interface_values:
        interface_values[key].append((interface_class, project_id, system, group, ))

    method_id = mock["_id"]
    type = mock["method"]
    method = mock["url"].split("/")[-1]
    url = mock["url"]
    method_description = mock["description"] or ""
    method_values.append((method_id, interface_class, type, method, url, method_description))

    mock_data = mock["mode"]
    data_values.append((method_id, mock_data, "初始模板"))

# 生成 insert 语句
interface_insert_sql = """INSERT INTO web_tools.easymock_interface (interface_class, project_id, sys, `group`, ) VALUES """
interface_insert_sql += ",".join(["%s"] * len(interface_values))

interface_values_tuple = tuple(
    sum([tuple(v) for v in interface_values.values()], ())
)

# print("easymock_interface 表 insert 语句:")
print(interface_insert_sql % interface_values_tuple + ";")

method_insert_sql = "INSERT INTO web_tools.easymock_method (method_id, interface_class, `type`, `method`, url, description) VALUES "
method_insert_sql += ",".join(["%s"] * len(method_values))
# print("easymock_method 表 insert 语句:")
print(method_insert_sql % tuple(method_values) + ";")

data_insert_sql = "INSERT INTO web_tools.easymock_data (method_id, mock_data, description) VALUES "
data_insert_sql += ",".join(["%s"] * len(data_values))
# print("easymock_data 表 insert 语句:")
print(data_insert_sql % tuple(data_values) + ";")