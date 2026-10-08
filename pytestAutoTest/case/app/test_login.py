#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
登录接口测试
"""

import pytest
from utils.http_client import HttpClient
from pytestAutoTest.core.parametrize_handler import ParametrizeHandler


# 在模块级别定义测试数据，以便pytest可以正确收集
handler = ParametrizeHandler()
test_data = handler.load_yaml('pytestAutoTest/test_data/login_test_data.yaml')
test_cases = test_data.get('cases', [])


class TestLogin:
    """登录接口测试类"""
    
    def setup_method(self):
        """测试方法前置操作"""
        # 创建HTTP客户端
        self.client = HttpClient("wodek-sit.shangtoutech.com", {
            'authorization': 'Basic d29kZWs6VFZSSmVrNUVWVEk9',
            'Content-Type': 'application/json'
        })
    
    @pytest.mark.parametrize("case_data", test_cases)
    def test_login(self, case_data):
        """登录接口测试"""
        # 打印测试数据
        print(f"测试数据: {case_data}")
        
        # 从测试数据中获取用户名和密码
        username = case_data.get('username')
        password = case_data.get('password')
        
        # 检查必要参数
        if not username or not password:
            pytest.fail("测试数据缺少必要的用户名或密码参数")
        
        # 构造登录URL（直接使用YAML中的密码，不进行额外编码）
        login_url = f"/wodek-api/login?username={username}&password={password}"
        
        # 执行登录
        print(f"执行登录: 用户名={username}")
        response = self.client.post(login_url)
        login_response = response['data']
        print(f"登录响应: {login_response}")
        
        # 验证登录结果
        # 检查HTTP状态码
        assert response['status_code'] == 200, f"HTTP状态码错误: {response['status_code']}"
        
        # 根据不同的测试数据，预期结果可能不同
        if 'password' in case_data and case_data['password'] == 12332123:
            # 对于错误密码的测试用例，预期登录失败
            assert login_response.get("code") == 500, f"预期登录失败，但实际返回码: {login_response.get('code')}"
            assert "密码解密失败" in login_response.get("msg", ""), f"预期密码解密失败消息，实际: {login_response.get('msg')}"
            print(f"登录失败（预期）: {login_response.get('msg')}")
        else:
            # 对于正确密码的测试用例，预期登录成功
            assert login_response.get("code") == 200, f"登录失败: {login_response.get('msg')}"
            assert "token" in login_response, "响应中未包含token"
            assert login_response.get("token") is not None, "token为空"
            print("登录测试通过")


if __name__ == '__main__':
    pytest.main(["-v", __file__])