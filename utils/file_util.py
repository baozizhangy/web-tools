#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""

"""
import json
import os
import csv
from configparser import ConfigParser
import pandas as pd
import openpyxl
import requests
import yaml
import xml.etree.ElementTree as ET


class MyConfigParser(ConfigParser):
    # 重写 configparser 中的 optionxform 函数，解决 .ini 文件中的 键option 自动转为小写的问题
    def __init__(self, defaults=None):
        ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, options_tr):
        return options_tr


def read_file(file_path, mode=None):
    """
    读取指定路径的各种文件内容
    :param mode: 各文件类型的不同处理模式，不同文件类型 mode 可能不同
    :param file_path:
    :return:
    """
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    if file_extension == '.ini':
        print(f"type::{file_extension}")
        _config = MyConfigParser()
        _config.read(file_path, encoding="UTF-8")
        data = dict(_config._sections)
        return data

    if file_extension == '.csv':
        with open(file_path, 'r', encoding='utf-8') as f:
            return list(csv.reader(f))

    elif file_extension == '.txt':
        if mode == 'line':
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()  # 读取所有行
                cleaned_lines = [line.strip() for line in lines]  # 使用列表推导式去除每行末尾的换行符
                return cleaned_lines
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()

    elif file_extension == '.tsv':
        with open(file_path, 'r', encoding='utf-8') as f:
            return list(csv.reader(f, delimiter='\t'))
    elif file_extension in ['.xlsx', '.xlsm', '.xltx', '.xltm']:
        sheets_dict = pd.read_excel(file_path, sheet_name=None)
        file_data = {}
        for sheet_name, df in sheets_dict.items():
            file_data[sheet_name] = df.fillna('').to_dict(orient='records')
        return file_data
    elif file_extension in ['.yaml', '.yml']:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    elif file_extension == '.xml':
        return ET.parse(file_path)
    elif file_extension == '.json':
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()


def write_to_file(file_path, file_data, encoding='utf-8'):
    """将字典或列表数据处理为Excel、文本、CSV、YAML、XML、YML和JSON文件

    Args:
        file_data (dict or list): 要处理的数据
        file_path (str): 要保存的文件路径，包括文件名和扩展名

    Returns:
        bool: 操作是否成功
    """
    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension == '':
        print("Invalid file path: {}".format(file_path))
        return False
    if file_extension not in ['.xlsx', '.txt', '.csv', '.yaml', '.yml', '.xml', '.json']:
        print("Unsupported file type: {}".format(file_extension))
        return False

    file_type = file_extension[1:]

    try:
        if file_type == 'excel':
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            for row in file_data:
                sheet.append(row)
            workbook.save(file_path)
        elif file_type == 'txt':
            with open(file_path, 'w', encoding=encoding) as file:
                for row in file_data:
                    file.write(str(row) + '\n')
        elif file_type == 'csv':
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                for row in file_data:
                    writer.writerow(row)
        elif file_type in ['yaml', 'yml']:
            with open(file_path, 'w') as file:
                yaml.dump(file_data, file)
        elif file_type == 'xml':
            root = ET.Element('root')
            for row in file_data:
                item = ET.SubElement(root, 'item')
                for key, value in row.items():
                    ET.SubElement(item, key).text = str(value)
            tree = ET.ElementTree(root)
            tree.write(file_path)
        elif file_type == 'json':
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(file_data, file)
    except Exception as e:
        print("Failed to write data to file: {}".format(str(e)))
        return False

    return True


def read_ol_file(_url):
    response = requests.get(_url)
    print("====response:", response)
    html_content = response.text
    print("====html_content:", html_content)
    return html_content


# if __name__ == '__main__':
#     path = r"D:\Script\testcase\src\app_new\data\case_data.xlsx"
#     data = pd_read_file(path)
#     print(data)
