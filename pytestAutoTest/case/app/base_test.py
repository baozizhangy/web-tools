
"""
测试基类
提供通用的测试方法和断言
"""

import allure
import pytest
from utils.logger_util import auto_logger


class BaseTest:
    """测试基类"""

    def setup_method(self):
        """测试方法级别的前置操作"""
        auto_logger.info("开始执行测试方法")

    def teardown_method(self):
        """测试方法级别的后置操作"""
        auto_logger.info("测试方法执行完成")

    def assert_response_success(self, response, message="接口调用失败"):
        """断言响应成功"""
        with allure.step("检查接口响应是否成功"):
            assert response is not None, f"{message}: 响应为空"
            if hasattr(response, 'json'):
                response_data = response.json()
                assert response_data.get("code") == "0" or response_data.get("status") == 1, \
                    f"{message}: 响应码错误 {response_data}"
            elif isinstance(response, dict):
                assert response.get("code") == "0" or response.get("status") == 1, \
                    f"{message}: 响应码错误 {response}"

    def assert_field_exists(self, obj, field, message="字段不存在"):
        """断言字段存在"""
        with allure.step(f"检查字段 {field} 是否存在"):
            assert field in obj, f"{message}: 字段 {field} 不存在于对象 {obj}"

    def assert_field_value(self, obj, field, expected_value, message="字段值不匹配"):
        """断言字段值"""
        with allure.step(f"检查字段 {field} 的值是否为 {expected_value}"):
            self.assert_field_exists(obj, field)
            actual_value = obj.get(field)
            assert actual_value == expected_value, f"{message}: 期望值 {expected_value}, 实际值 {actual_value}"