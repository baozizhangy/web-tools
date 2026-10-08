#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
工单创建接口测试
"""

import pytest
from pytestAutoTest.core.test_case_model import TestCaseModel, SetupStep, TeardownStep, Assertion
from pytestAutoTest.core.parametrize_handler import ParametrizeHandler


class TestWorkOrderCreate:
    """工单创建接口测试类"""
    
    def setup_method(self):
        """测试方法前置操作"""
        self.handler = ParametrizeHandler()
    
    @pytest.mark.parametrize("case_data", [
        {
            "case_id": "test_workorder_create_001",
            "title": "创建工单-正常流程",
            "request_data": {
                "categoryCode": "APPLY",
                "subCategoryCode": "",
                "urgencyLevel": "URGENT",
                "userNo": "${userNo}",
                "loanNo": "${loanNo}",
                "content": "创建工单",
                "handlerId": 1,
                "deptId": "100",
                "systemCode": "widek"
            },
            "expected_code": "0"
        }
    ])
    def test_workorder_create(self, case_data):
        """工单创建接口测试"""
        # 1. 创建测试用例模型
        test_case = TestCaseModel(
            case_id=case_data["case_id"],
            title=case_data["title"]
        )
        
        # 2. 设置请求数据
        test_case.request_data = case_data["request_data"]
        
        # 3. 添加断言
        test_case.add_assertion(Assertion(
            type="code",
            description="验证响应码",
            expected=case_data["expected_code"]
        ))
        
        test_case.add_assertion(Assertion(
            type="field_exists",
            description="验证orderNo存在",
            field_path="data.orderNo"
        ))
        
        # 4. 打印测试用例信息（实际项目中这里应该是调用API并验证）
        print(f"测试用例: {test_case.title}")
        print(f"请求数据: {test_case.request_data}")
        print(f"断言数量: {len(test_case.assertions)}")
        
        # 5. 实际测试中这里应该调用API并验证断言
        # response = api_client.post("/api/v1/workOrder/create", json=test_case.request_data)
        # for assertion in test_case.assertions:
        #     if assertion.type == "code":
        #         assert response.json()["code"] == assertion.expected
        #     elif assertion.type == "field_exists":
        #         assert assertion.field_path in response.json()
        
        # 6. 这里只是演示，我们简单打印一下断言配置
        for assertion in test_case.assertions:
            print(f"断言: {assertion.description}, 类型: {assertion.type}")


if __name__ == '__main__':
    pytest.main(["-v", __file__])