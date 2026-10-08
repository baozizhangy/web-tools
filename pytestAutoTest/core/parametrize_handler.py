#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
参数化数据处理模块
支持从YAML、JSON、Excel、数据库等多种数据源加载测试数据
"""

import json, yaml, pytest
import os
from pathlib import Path
from typing import List, Dict, Any, Union
from utils.logger_util import auto_logger
from utils.mysql_util import MySQL


class ParametrizeHandler:
    """参数化数据处理器"""

    def __init__(self):
        self.logger = auto_logger

    @staticmethod
    def _resolve_file_path(file_path: str) -> str:
        """
        解析文件路径，处理相对路径问题
        
        Args:
            file_path: 原始文件路径
            
        Returns:
            解析后的绝对路径
        """
        # 如果已经是绝对路径且文件存在，直接返回
        if os.path.isabs(file_path) and os.path.exists(file_path):
            return file_path

        # 如果是相对路径且文件存在，转换为绝对路径返回
        if not os.path.isabs(file_path) and os.path.exists(file_path):
            return os.path.abspath(file_path)

        # 尝试在脚本所在目录的上级目录中查找
        script_dir = os.path.dirname(os.path.abspath(__file__))
        possible_path = os.path.join(script_dir, '..', '..', file_path)
        if os.path.exists(possible_path):
            return os.path.abspath(possible_path)

        # 尝试在项目根目录中查找
        project_root = os.path.join(script_dir, '..', '..')
        possible_path = os.path.join(project_root, file_path)
        if os.path.exists(possible_path):
            return os.path.abspath(possible_path)

        # 如果都找不到，返回原始路径，让后续处理报错
        return file_path

    @staticmethod
    def load_yaml(file_path: str) -> Union[Dict, List]:
        """
        从YAML文件加载测试数据

        Args:
            file_path: YAML文件路径

        Returns:
            解析后的数据（字典或列表）
        """
        try:
            resolved_path = ParametrizeHandler._resolve_file_path(file_path)
            with open(resolved_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            auto_logger.info(f"成功加载YAML文件: {resolved_path}")
            return data
        except Exception as e:
            auto_logger.error(f"加载YAML文件失败: {file_path}, 错误: {str(e)}")
            raise

    @staticmethod
    def load_json(file_path: str) -> Union[Dict, List]:
        """
        从JSON文件加载测试数据

        Args:
            file_path: JSON文件路径

        Returns:
            解析后的数据（字典或列表）
        """
        try:
            resolved_path = ParametrizeHandler._resolve_file_path(file_path)
            with open(resolved_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            auto_logger.info(f"成功加载JSON文件: {resolved_path}")
            return data
        except Exception as e:
            auto_logger.error(f"加载JSON文件失败: {file_path}, 错误: {str(e)}")
            raise

    @staticmethod
    def load_from_db(sql: str, db_config: Dict[str, Any] = None) -> List[Dict]:
        """
        从数据库加载测试数据

        Args:
            sql: SQL查询语句
            db_config: 数据库配置（可选）

        Returns:
            查询结果列表
        """
        try:
            db = MySQL(**db_config)
            res = db.get_all(sql)
            auto_logger.info(f"从数据库加载数据成功，共 {len(res)} 条")
            return res
        except Exception as e:
            auto_logger.error(f"从数据库加载数据失败: {str(e)}")
            raise

    @staticmethod
    def build_test_cases(test_data: List[Dict], id_field: str = "case_id") -> List[tuple]:
        """
        构建pytest参数化测试用例

        Args:
            test_data: 测试数据列表
            id_field: 用作用例ID的字段名

        Returns:
            适用于pytest.mark.parametrize的元组列表
        """
        if not test_data:
            auto_logger.warning("测试数据为空")
            return []

        # 构建参数化数据
        cases = []
        for data in test_data:
            case_id = data.get(id_field, f"case_{len(cases)}")
            cases.append(pytest.param(data, id=case_id))

        auto_logger.info(f"构建测试用例成功，共 {len(cases)} 个")
        return cases

    @staticmethod
    def merge_data(*data_sources: Dict) -> Dict:
        """
        合并多个数据源

        Args:
            *data_sources: 多个数据字典

        Returns:
            合并后的数据字典
        """
        merged = {}
        for data in data_sources:
            if isinstance(data, dict):
                merged.update(data)
        return merged

    @staticmethod
    def extract_params(data: Dict, keys: List[str]) -> Dict:
        """
        从数据字典中提取指定的参数

        Args:
            data: 原始数据字典
            keys: 需要提取的键列表

        Returns:
            提取后的数据字典
        """
        return {key: data.get(key) for key in keys if key in data}

    @staticmethod
    def replace_variables(text: str, variables: Dict[str, Any]) -> str:
        """
        替换文本中的变量占位符
        支持格式: ${variable_name}

        Args:
            text: 原始文本
            variables: 变量字典

        Returns:
            替换后的文本
        """
        import re

        def replace(match):
            var_name = match.group(1)
            return str(variables.get(var_name, match.group(0)))

        return re.sub(r'\$\{(\w+)\}', replace, str(text))

    @staticmethod
    def process_data_template(template: Dict, variables: Dict[str, Any]) -> Dict:
        """
        处理数据模板，替换所有变量

        Args:
            template: 数据模板字典
            variables: 变量字典

        Returns:
            处理后的数据字典
        """

        def process_value(value):
            if isinstance(value, str):
                return ParametrizeHandler.replace_variables(value, variables)
            elif isinstance(value, dict):
                return {k: process_value(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [process_value(item) for item in value]
            else:
                return value

        return process_value(template)


# 便捷函数
def load_test_data(file_path: str) -> Union[Dict, List]:
    """
    根据文件扩展名自动选择加载方法

    Args:
        file_path: 数据文件路径

    Returns:
        加载的数据
    """
    path = Path(file_path)
    suffix = path.suffix.lower()

    resolved_path = ParametrizeHandler._resolve_file_path(file_path)

    if suffix in ['.yaml', '.yml']:
        return ParametrizeHandler.load_yaml(resolved_path)
    elif suffix == '.json':
        return ParametrizeHandler.load_json(resolved_path)
    else:
        raise ValueError(f"不支持的文件格式: {suffix}")


if __name__ == '__main__':
    # 使用示例
    handler = ParametrizeHandler()

    # 示例1: 加载YAML数据
    data = handler.load_yaml('pytestAutoTest/test_data/login_test_data.yaml')
    # print(len(data['cases']))
    # 示例2: 变量替换
    template = {
        "mobile": "${mobile}",
        "name": "${name}",
        "amount": 10000
    }
    for case_data in data['cases']:
        result = handler.process_data_template(template, case_data)
        print(f"模板处理结果: {result}")
    # # variables = {"mobile": "13800138000", "name": "张三"}
