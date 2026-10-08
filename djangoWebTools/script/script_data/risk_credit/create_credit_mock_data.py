#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
import os
import random

from utils.file_util import read_file


def update_json_with_random_values(input_file, output_file, encoding='utf-8'):
    try:
        # 读取输入 JSON 文件
        # with open(input_file, 'r') as file:
        #     data = json.load(file)

        data = read_file(input_file)

        # 遍历数据字典,并将键值赋为随机数
        for key, _ in data.items():
            data[key] = str(random.randint(1, 100))

        # 将更新后的数据写入输出 JSON 文件
        with open(output_file, 'w') as file:
            json.dump(data, file, indent=4)

        print(f"mock数据成功生成至:{output_file}")
    except FileNotFoundError:
        print(f"Error: {input_file} or {output_file} 文件未找到.")
    except json.JSONDecodeError:
        print(f"Error: {input_file} Json文件异常")
    except Exception as e:
        print(f"执行异常: {e}")


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    source_json_path = "百融-借贷意向-mock-20240521.json"
    input_path = f"{base_dir}/{source_json_path}"

    output_path = f"{base_dir}/script_data/credit_mock_data/百融-借贷意向-mock-20240521.json"
    update_json_with_random_values(input_path, output_path)
