#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
BM API完整授信流程测试用例
包括从用户撞库到授信结果查询的完整流程测试
"""

import allure
import pytest
import random

from api.app.bm_api import BmApi
from utils.logger_util import auto_logger
from utils.personal_util import get_mobile_no, get_id_no, get_person_name


@allure.epic("BM业务接口")
@allure.feature("完整授信流程")
class TestCompleteCreditFlow:
    """完整授信流程测试"""

    @pytest.fixture(scope="class")
    def test_data(self):
        """生成测试数据"""
        return {
            "mobile": get_mobile_no(),
            "name": get_person_name(),
            "id_card": get_id_no()
        }

    @pytest.fixture(scope="class")
    def bm_api_client(self, test_data):
        """创建BM API客户端实例"""
        api_client = BmApi(
            mobile=test_data["mobile"],
            name=test_data["name"],
            id_card=test_data["id_card"],
            env="BM_SIT"
        )
        auto_logger.info(f"创建BM API客户端: mobile={test_data['mobile']}, name={test_data['name']}, id_card={test_data['id_card']}")
        return api_client

    @pytest.fixture(scope="class")
    def credit_application(self, bm_api_client):
        """执行授信申请并返回申请号"""
        # 添加白名单
        bm_api_client.risk_white_user()
        
        # 生成授信申请号
        credit_req_no = 'CT' + str(random.randint(100000000000, 999999999999)) + 'TEST'
        
        # 执行授信申请（使用自定义的授信申请号）
        apply_result = self._perform_credit_apply(bm_api_client, credit_req_no)
        
        auto_logger.info(f"提取到授信申请号: {credit_req_no}")
        return credit_req_no

    def _perform_credit_apply(self, bm_api_client, credit_req_no):
        """执行授信申请，使用指定的授信申请号"""
        # 准备授信申请数据
        json_data = {
            "creditReqNo": credit_req_no,
            "userNo": 'UR98532' + str(random.randint(100000000000, 999999999999)) + 'TEST',
            "fundUserNo": str(random.randint(100000000000, 999999999999)),
            "authFaceInfo": bm_api_client.req_data.face_info(),
            "authIdInfo": bm_api_client.req_data.id_info(),
            "contactInfo": bm_api_client.req_data.contact_info(),
            "deviceInfo": bm_api_client.req_data.device_info(),
            "geoInfo": bm_api_client.req_data.geo_info(),
            "jobInfo": bm_api_client.req_data.job_info(),
            "userBaseInfo": bm_api_client.req_data.user_base_info(),
            "userProfileInfo": bm_api_client.req_data.user_profile_info()
        }
        
        # 发起授信申请
        res = bm_api_client.req_api.response_handle(
            bm_api_client.req_api.request_handle(json_data, f"{bm_api_client.channel_id}/creditApply", env=bm_api_client.env))
        auto_logger.info(f"调用{bm_api_client.env}/creditApply接口::json_data::{json_data}，授信接口响应数据{res}")
        return res

    @allure.story("完整授信流程")
    @allure.title("从撞库到授信结果查询完整流程测试")
    @allure.description("验证从用户撞库、添加白名单、授信申请到授信结果查询的完整流程")
    def test_complete_credit_flow(self, bm_api_client, credit_application):
        """测试完整授信流程"""
        
        # 步骤1: 用户撞库
        with allure.step("1. 用户撞库"):
            check_result = bm_api_client.check_user()
            assert "check_res" in check_result
            assert check_result["check_res"] is not None
            auto_logger.info(f"撞库完成: mobile={check_result['mobile']}")
        
        # 步骤2: 添加白名单（已在前置中执行）
        with allure.step("2. 添加白名单"):
            auto_logger.info("白名单已在前置中添加")
        
        # 步骤3: 授信申请（已在前置中执行）
        with allure.step("3. 授信申请"):
            auto_logger.info(f"授信申请已在前置中完成，申请号: {credit_application}")
        
        # 步骤4: 授信结果查询
        with allure.step("4. 授信结果查询"):
            query_result = bm_api_client.credit_apply_result(credit_req_no=credit_application)
            assert query_result is not None
            auto_logger.info(f"授信结果查询完成: credit_req_no={credit_application}")
        
        # 完整的授信流程测试完成
        auto_logger.info("完整的授信流程测试完成")
        
        # 在报告中展示流程结果
        allure.attach(str(check_result), "撞库结果", allure.attachment_type.JSON)
        allure.attach("白名单添加完成", "白名单结果", allure.attachment_type.TEXT)
        allure.attach(f"授信申请完成，申请号: {credit_application}", "授信申请结果", allure.attachment_type.TEXT)
        allure.attach(str(query_result), "授信查询结果", allure.attachment_type.JSON)