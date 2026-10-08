#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
断言辅助工具
结合pytest原生assert和扩展功能，提供轻量级的断言辅助
"""

import allure
from typing import Any, Dict, List
from jsonpath_ng import parse
from utils.logger_util import auto_logger
from utils.mysql_util import MySQL
from utils.redis_util import RedisUtil


class AssertHelper:
    """
    断言辅助工具

    设计理念：
    1. 简单断言直接用pytest的assert（推荐）
    2. 本类只提供pytest不支持的扩展功能
    """

    @staticmethod
    @allure.step("断言JSONPath: {json_path} = {expected}")
    def assert_jsonpath(response: Dict, json_path: str, expected: Any):
        """
        JSONPath表达式断言

        Example:
            assert_jsonpath(response, "$.data[0].name", "张三")
        """
        jsonpath_expr = parse(json_path)
        matches = jsonpath_expr.find(response)

        assert matches, f"JSONPath {json_path} 未匹配到数据"
        actual = matches[0].value
        assert actual == expected, f"期望 {expected}, 实际 {actual}"
        auto_logger.info(f"✓ JSONPath {json_path} = {actual}")

    @staticmethod
    @allure.step("断言数据库记录存在")
    def assert_db_exists(sql: str, db_config: Dict = None):
        """
        断言数据库记录存在

        Example:
            assert_db_exists("SELECT * FROM users WHERE mobile='13800138000'")
        """
        db = MySQL(**db_config)
        result = db.get_all(sql)
        assert result is not None, f"数据库记录不存在: {sql}"
        auto_logger.info(f"✓ 数据库记录存在: {result}")
        return result

    @staticmethod
    @allure.step("断言数据库字段值: {field} = {expected}")
    def assert_db_field(sql: str, field: str, expected: Any, db_config: Dict = None):
        """
        断言数据库字段值

        Example:
            assert_db_field("SELECT * FROM users WHERE id=1", "status", "active")
        """
        db = MySQL(**db_config)
        result = db.select_one(sql)
        assert result is not None, f"查询无结果: {sql}"

        actual = result.get(field)
        assert actual == expected, f"字段 {field}: 期望 {expected}, 实际 {actual}"
        auto_logger.info(f"✓ 数据库字段 {field} = {actual}")

    @staticmethod
    @allure.step("断言Redis键存在: {key}")
    def assert_redis_exists(key: str, redis_config: Dict = None):
        """
        断言Redis键存在

        Example:
            assert_redis_exists("code:13800138000")
        """
        redis_client = RedisUtil() if redis_config is None else RedisUtil(**redis_config)
        exists = redis_client.get_value(key)
        assert exists, f"Redis键不存在: {key}"
        auto_logger.info(f"✓ Redis键 {key} 存在")

    @staticmethod
    @allure.step("断言Redis值: {key} = {expected}")
    def assert_redis_value(key: str, expected: Any, redis_config: Dict = None):
        """
        断言Redis值

        Example:
            assert_redis_value("code:13800138000", "123456")
        """
        redis_client = RedisUtil() if redis_config is None else RedisUtil(**redis_config)
        actual = redis_client.get_value(key)
        assert actual == str(expected), f"Redis值: 期望 {expected}, 实际 {actual}"
        auto_logger.info(f"✓ Redis {key} = {actual}")


class SoftAssert:
    """
    软断言工具
    收集所有断言错误，最后统一抛出

    Usage:
        soft = SoftAssert()
        soft.assert_equal(actual, expected, "错误消息1")
        soft.assert_equal(actual2, expected2, "错误消息2")
        soft.assert_all()  # 统一检查，如有错误则抛出
    """

    def __init__(self):
        self.errors = []

    def assert_equal(self, actual: Any, expected: Any, msg: str = ""):
        """软断言：相等"""
        try:
            assert actual == expected, msg or f"期望 {expected}, 实际 {actual}"
            auto_logger.info(f"✓ {msg or '断言通过'}: {actual}")
        except AssertionError as e:
            error_msg = f"✗ {str(e)}"
            self.errors.append(error_msg)
            auto_logger.error(error_msg)

    def assert_in(self, item: Any, container: Any, msg: str = ""):
        """软断言：包含"""
        try:
            assert item in container, msg or f"{item} 不在 {container} 中"
            auto_logger.info(f"✓ {msg or '断言通过'}")
        except AssertionError as e:
            error_msg = f"✗ {str(e)}"
            self.errors.append(error_msg)
            auto_logger.error(error_msg)

    def assert_true(self, condition: bool, msg: str = ""):
        """软断言：为真"""
        try:
            assert condition, msg or "条件为假"
            auto_logger.info(f"✓ {msg or '断言通过'}")
        except AssertionError as e:
            error_msg = f"✗ {str(e)}"
            self.errors.append(error_msg)
            auto_logger.error(error_msg)

    def assert_all(self):
        """检查所有软断言，如有错误则抛出"""
        if self.errors:
            error_summary = "\n".join([f"  {i + 1}. {err}" for i, err in enumerate(self.errors)])
            raise AssertionError(f"软断言失败，共 {len(self.errors)} 个错误:\n{error_summary}")
        else:
            auto_logger.info(f"✓ 所有软断言通过")


# 便捷函数
def get_nested_value(data: Dict, path: str, default: Any = None) -> Any:
    """
    获取嵌套字典的值

    Args:
        data: 数据字典
        path: 字段路径，如 "data.userInfo.mobile"
        default: 默认值

    Returns:
        字段值

    Example:
        mobile = get_nested_value(response, "data.userInfo.mobile")
    """
    keys = path.split('.')
    value = data
    try:
        for key in keys:
            if isinstance(value, dict):
                value = value[key]
            else:
                return default
        return value
    except (KeyError, TypeError):
        return default


if __name__ == '__main__':
    # 使用示例

    # 示例1: 使用辅助断言
    response = {
        "code": "0",
        "msg": "success",
        "data": {
            "list": [{"name": "张三", "age": 18}]
        }
    }

    # JSONPath断言
    AssertHelper.assert_jsonpath(response, "$.data.list[0].name", "张三")

    # 示例2: 软断言
    soft = SoftAssert()
    soft.assert_equal(response["code"], "0", "响应码断言")
    soft.assert_in("success", response["msg"], "消息断言")
    soft.assert_true(len(response["data"]["list"]) > 0, "列表不为空")
    soft.assert_all()

    print("所有断言通过！")
