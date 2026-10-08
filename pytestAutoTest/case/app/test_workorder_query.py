#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
工单查询接口测试
通过前置方法登录成功，获取相应的refresh_token字段，
赋值给下面查询接口，添加到header中，校验查询功能
"""

import pytest
import json
from utils.http_client import HttpClient
from pytestAutoTest.core.parametrize_handler import ParametrizeHandler


# 在模块级别定义测试数据，以便pytest可以正确收集
handler = ParametrizeHandler()
test_data = handler.load_yaml('pytestAutoTest/test_data/login_test_data.yaml')
query_cases = test_data.get('query_cases', [])


class TestWorkOrderQuery:
    """工单查询接口测试类"""

    def setup_method(self):
        """测试方法前置操作"""
        # 创建HTTP客户端用于登录 (使用dev环境)
        self.login_client = HttpClient("https://wodek-sit.shangtoutech.com", {
            'authorization': 'Basic d29kZWs6VFZSSmVrNUVWVEk9',
            'Content-Type': 'application/json'
        })

        # 创建HTTP客户端用于查询 (使用dev环境)
        self.query_client = HttpClient("https://wodek-sit.shangtoutech.com")

    def perform_login(self, username, password):
        """
        执行登录操作

        Args:
            username: 用户名
            password: 密码

        Returns:
            dict: 登录响应数据
        """
        # 构造登录URL
        login_url = f"/wodek-api/login?username={username}&password={password}"

        # 执行登录
        response = self.login_client.post(login_url)
        return response['data']

    def query_work_orders(self, token, query_params):
        """
        查询工单列表

        Args:
            token: 登录获取的token
            query_params: 查询参数

        Returns:
            dict: 查询响应数据
        """
        # 设置查询接口的请求头
        headers = {
            'authorizationtoken': f'Bearer {token}',
            'origin': 'https://wodek-sit.shangtoutech.com',
            'sys-code': 'wodek',
            'Content-Type': 'application/json;charset=UTF-8',
            'Host': 'wodek-sit.shangtoutech.com'
        }

        # 设置默认查询参数
        payload_data = {
            "current": 1,
            "pageSize": 20,
            "menuType": "WORK_ORDER_MANAGEMENT"
        }

        # 合并传入的查询参数
        payload_data.update(query_params)

        # 发送查询请求 (使用正确的路径)
        response = self.query_client.post(
            "/css/api/v1/workOrder/queryList",
            payload=payload_data,
            headers=headers
        )
        return response

    @pytest.mark.parametrize("query_case", query_cases)
    def test_workorder_query(self, query_case):
        """工单查询接口测试"""
        # 打印测试数据
        print(f"查询数据: {query_case}")

        # 执行登录 (写死使用正常账号密码)
        # 注意：由于环境变更，需要使用dev环境的有效用户凭证
        login_response = self.perform_login(
            "stt",
            "wuPIVIa9vJ0zzA4Z5gINgjT93jtac9ntttWePAAz50nmLu28G1IdCypmSXn04GIOgZzbA66IgTSHGz8iwoa3Wg%3D%3D"
        )
        print(f"登录响应: {login_response}")

        # 验证登录成功
        assert login_response.get("code") == 200, f"登录失败: {login_response.get('msg')}"
        token = login_response.get("token")
        assert token is not None, "未获取到token"

        # 执行工单查询
        query_response = self.query_work_orders(token, query_case)
        print(f"查询响应: {query_response}")

        # 验证查询结果
        assert query_response['status_code'] == 200, f"查询请求失败，状态码: {query_response['status_code']}"

        # 解析响应数据
        response_data = query_response['data']
        assert isinstance(response_data, dict), "查询响应格式错误"

        # 1. 基础断言：code 必须为 0 才视为成功（兼容字符串 "0"）
        code_value = response_data.get("code")
        assert str(code_value) == "0", f"查询失败: {response_data.get('msg')}"

        data_block = response_data.get("data") or {}
        rows = data_block.get("rows") or []

        # 2. 当请求包含 urgencyLevel 时，校验返回首条数据的 urgencyLevel 一致
        if query_case.get("urgencyLevel"):
            assert rows, "返回数据为空，无法校验紧急程度"
            first_row_level = rows[0].get("urgencyLevel")
            assert first_row_level == query_case["urgencyLevel"], (
                f"紧急程度不一致，期望 {query_case['urgencyLevel']} 实际 {first_row_level}"
            )

        # 3. 请求参数为空（无额外筛选条件）时，校验 total 与返回记录数量一致
        business_filters = {
            k: v for k, v in query_case.items() if k not in {"current", "pageSize", "menuType"}
        }
        if not business_filters:
            total = data_block.get("total")
            assert total == len(rows), (
                f"总数不匹配，total={total} rows={len(rows)}"
            )

        print("工单查询测试通过")


if __name__ == '__main__':
    pytest.main(["-v", __file__])