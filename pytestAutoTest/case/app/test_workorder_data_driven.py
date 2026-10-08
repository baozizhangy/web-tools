#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
工单创建接口测试 - 数据驱动版本
"""

import pytest
from pytestAutoTest.core.test_case_model import TestCaseModel, SetupStep, TeardownStep, Assertion
from pytestAutoTest.core.parametrize_handler import ParametrizeHandler



# 在模块级别定义测试数据，以便pytest可以正确收集
handler = ParametrizeHandler()
test_data = handler.load_yaml('pytestAutoTest/test_data/login_test_data.yaml')
test_cases = test_data.get('cases', [])


class TestWorkOrderCreateDataDriven:
    """工单创建接口数据驱动测试类"""
    
    def create_test_case(self, case_data):
        """创建测试用例模型"""
        test_case = TestCaseModel(
            case_id=f"test_workorder_create_{case_data.get('loanNo', '')}",
            title=f"登录-用户{case_data.get('username', '')}"
        )
        
        # 设置请求数据，使用变量占位符
        test_case.request_data = {
            "username":"${username}",
            "password":"${password}"
        }
        
        # 添加断言
        test_case.add_assertion(Assertion(
            type="code",
            description="验证响应码",
            expected="0"
        ))
        
        test_case.add_assertion(Assertion(
            type="field_exists",
            description="登录成功",
            field_path="data.orderNo"
        ))
        
        return test_case
    
    @pytest.mark.parametrize("case_data", test_cases)
    def test_workorder_create(self, case_data):
        """工单创建接口测试"""
        # 创建测试用例
        test_case = self.create_test_case(case_data)
        
        # 使用变量替换处理请求数据
        handler = ParametrizeHandler()
        processed_request_data = handler.process_data_template(
            test_case.request_data, 
            case_data
        )
        
        # 打印测试信息
        print(f"测试用例ID: {test_case.case_id}")
        print(f"测试用例标题: {test_case.title}")
        print(f"原始请求数据: {test_case.request_data}")
        print(f"处理后请求数据: {processed_request_data}")
        
        # 打印断言信息
        for i, assertion in enumerate(test_case.assertions):
            print(f"断言{i+1}: {assertion.description}")
        
        # 实际测试中这里应该：
        # 1. 调用API接口（使用processed_request_data）
        # 2. 验证断言
        # 3. 执行前置和后置步骤（如果有的话）
        
        # 示例验证（模拟）
        assert len(processed_request_data) > 0
        assert len(test_case.assertions) == 2
        print("测试用例执行完成")


if __name__ == '__main__':
    pytest.main(["-v", __file__])