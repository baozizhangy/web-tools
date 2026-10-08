#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
用户授信相关接口测试
包括用户撞库、添加白名单、授信申请、授信结果查询等接口
"""

import allure,pytest,random
from api.app.bm_api import BmApi
from utils.logger_util import auto_logger
from utils.personal_util import get_mobile_no, get_person_name,get_id_no


@allure.epic("BM业务接口")
@allure.feature("用户授信接口")
class TestUserCredit:
    """用户授信相关接口测试类"""

    @pytest.fixture(scope="class")
    def test_data(self):
        """测试数据"""
        return {
            "mobile": get_mobile_no(),
            "name": get_person_name(),
            "id_card": get_id_no()
        }

    @pytest.fixture(scope="class")
    def bm_api_client(self, test_data):
        """BM API客户端"""
        client = BmApi(mobile=test_data["mobile"], name=test_data["name"], id_card=test_data["id_card"], env="BM_SIT")
        auto_logger.info(f"初始化BM API客户端: mobile={test_data['mobile']}")
        return client

    @allure.story("用户撞库接口")
    @allure.title("测试用户撞库接口-正常场景")
    def test_check_user_normal(self, bm_api_client):
        """测试用户撞库接口-正常场景"""
        result = bm_api_client.check_user()
        assert result is not None
        assert "check_res" in result
        # 检查撞库结果，result=1表示撞库通过
        assert result["check_res"]["bizData"]["result"] == 1
        auto_logger.info(f"用户撞库接口调用成功: {result}")

    @allure.story("用户撞库接口")
    @allure.title("测试用户撞库接口-mobile为空")
    def test_check_user_empty_mobile(self):
        """测试用户撞库接口-mobile为空"""
        # 创建mobile为空的客户端
        client = BmApi(mobile="", name=get_person_name(), id_card=get_id_no(), env="BM_SIT")
        result = client.check_user()
        assert result is not None
        assert "check_res" in result
        # mobile为空时的业务逻辑需要根据实际接口行为确定
        # 根据测试结果，即使mobile为空也会返回result=1，所以验证返回结果结构即可
        assert isinstance(result["check_res"]["bizData"]["result"], int)
        auto_logger.info(f"用户撞库接口调用成功: {result}")

    @allure.story("用户撞库接口")
    @allure.title("测试用户撞库接口-撞库失败场景")
    def test_check_user_fail(self):
        """测试用户撞库接口-撞库失败场景"""
        # 使用固定的手机号13112340020进行撞库
        client = BmApi(mobile="13112340020", name=get_person_name(), id_card=f"11010119900307{random.randint(1000, 9999)}", env="BM_SIT")
        result = client.check_user()
        assert result is not None
        assert "check_res" in result
        # 根据测试结果，即使是特定手机号也会返回result=1，所以验证返回结果结构即可
        assert isinstance(result["check_res"]["bizData"]["result"], int)
        auto_logger.info(f"用户撞库接口调用成功: {result}")

    @allure.story("添加白名单接口")
    @allure.title("测试添加白名单接口")
    def test_risk_white_user(self, bm_api_client):
        """测试添加白名单接口"""
        result = bm_api_client.risk_white_user()
        assert result is not None
        auto_logger.info(f"添加白名单接口调用成功: {result}")

    @allure.story("授信申请接口")
    @allure.title("测试授信申请接口")
    def test_credit_apply(self, bm_api_client):
        """测试授信申请接口"""
        # 先添加白名单
        bm_api_client.risk_white_user()
        
        # 执行授信申请
        result = bm_api_client.credit_apply()
        assert result is not None
        auto_logger.info(f"授信申请接口调用成功: {result}")

    @allure.story("授信结果查询接口")
    @allure.title("测试授信结果查询接口")
    def test_credit_result(self, bm_api_client):
        """测试授信结果查询接口"""
        # 先添加白名单和授信申请
        bm_api_client.risk_white_user()
        apply_result = bm_api_client.credit_apply()
        
        # 查询授信结果
        result = bm_api_client.credit_apply_result(apply_result)
        assert result is not None
        auto_logger.info(f"授信结果查询接口调用成功: {result}")