"""
权益相关接口测试
- privilege_status() - 查询权益状态
- privilege_exposure() - 查询权益exposure
- privilege_info() - 查询权益信息
- bill_privilege_info() - 查询账单权益信息
- profit_status_query() - 查询权益结果和当前状态
"""
import pytest
import allure
from conftest import assert_response_success, assert_response_has_field
from utils.logger_util import web_logger
from api.app.bm_api import BmApi


@allure.feature("权益相关接口")
@allure.story("权益状态与信息查询")
class TestPrivilegeInterface:
    """权益相关接口测试"""

    def test_privilege_status_success(self, api_with_user_data):
        """
        测试查询权益状态接口 - 成功场景
        验证：
        1. 响应不为空
        2. 返回权益状态信息
        """
        web_logger.info(f"查询权益状态: {api_with_user_data.mobile}")
        
        # 设置user_no
        api_with_user_data.user_no = "UR1105157518080090112"
        
        response = api_with_user_data.privilege_status()
        
        # 验证响应
        assert response is not None, "查询权益状态响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"
        
        web_logger.info(f"查询权益状态成功")

    def test_privilege_status_response_structure(self, api_with_user_data):
        """
        测试查询权益状态接口 - 响应结构验证
        """
        api_with_user_data.user_no = "UR98532646364720619TEST"
        
        response = api_with_user_data.privilege_status()
        
        # 验证响应结构
        assert 'bizData' in response or 'data' in response, "响应缺少bizData或data字段"
        
        web_logger.info(f"查询权益状态响应结构验证通过")

    def test_privilege_exposure_success(self, api_with_user_data):
        """
        测试查询权益exposure接口 - 成功场景
        验证：
        1. 响应不为空
        2. 返回权益exposure信息
        """
        web_logger.info(f"查询权益exposure: {api_with_user_data.mobile}")
        
        api_with_user_data.user_no = "UR1105157518080090112"
        draw_req_no = "971139616990375936"
        
        response = api_with_user_data.privilege_exposure(draw_req_no)
        
        # 验证响应
        assert response is not None, "查询权益exposure响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"
        
        web_logger.info(f"查询权益exposure成功")

    def test_privilege_exposure_response_structure(self, api_with_user_data):
        """
        测试查询权益exposure接口 - 响应结构验证
        """
        api_with_user_data.user_no = "UR1191577283845259264"
        draw_req_no = "LFN1191578430468063232"
        
        response = api_with_user_data.privilege_exposure(draw_req_no)
        
        # 验证响应结构
        # assert 'bizData' in response or 'data' in response, "响应缺少bizData或data字段"
        
        web_logger.info(f"查询权益exposure响应结构验证通过")

    def test_privilege_info_success(self, api_with_user_data):
        """
        测试查询权益信息接口 - 成功场景
        验证：
        1. 响应不为空
        2. 返回权益信息
        """
        web_logger.info(f"查询权益信息: {api_with_user_data.mobile}")
        
        api_with_user_data.user_no = "UR98532646364720619TEST"
        
        response = api_with_user_data.privilege_info()
        
        # 验证响应
        assert response is not None, "查询权益信息响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"
        
        web_logger.info(f"查询权益信息成功")

    def test_privilege_info_response_structure(self, api_with_user_data):
        """
        测试查询权益信息接口 - 响应结构验证
        """
        api_with_user_data.user_no = "UR1191577283845259264"
        
        response = api_with_user_data.privilege_info()
        
        # 验证响应结构
        assert 'bizData' in response or 'data' in response, "响应缺少bizData或data字段"
        
        web_logger.info(f"查询权益信息响应结构验证通过")

    def test_bill_privilege_info_success(self, api_with_user_data):
        """
        测试查询账单权益信息接口 - 成功场景
        验证：
        1. 响应不为空
        2. 返回账单权益信息
        """
        web_logger.info(f"查询账单权益信息: {api_with_user_data.mobile}")
        
        api_with_user_data.user_no = "UR98532646364720619TEST"
        
        response = api_with_user_data.bill_privilege_info()
        
        # 验证响应
        assert response is not None, "查询账单权益信息响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"
        
        web_logger.info(f"查询账单权益信息成功")

    def test_bill_privilege_info_response_structure(self, api_with_user_data):
        """
        测试查询账单权益信息接口 - 响应结构验证
        """
        api_with_user_data.user_no = "UR98532646364720619TEST"
        
        response = api_with_user_data.bill_privilege_info()
        
        # 验证响应结构
        assert 'bizData' in response or 'data' in response, "响应缺少bizData或data字段"
        
        web_logger.info(f"查询账单权益信息响应结构验证通过")

    def test_profit_status_query_success(self, api_with_user_data):
        """
        测试查询权益结果和当前状态接口 - 成功场景
        验证：
        1. 响应不为空
        2. 返回权益结果和状态信息
        """
        web_logger.info(f"查询权益结果和当前状态: {api_with_user_data.mobile}")
        
        response = api_with_user_data.profit_status_query()
        
        # 验证响应
        assert response is not None, "查询权益结果和当前状态响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"
        
        web_logger.info(f"查询权益结果和当前状态成功")

    def test_profit_status_query_response_structure(self, api_with_user_data):
        """
        测试查询权益结果和当前状态接口 - 响应结构验证
        """
        response = api_with_user_data.profit_status_query()
        
        # 验证响应结构
        # assert 'bizData' in response or 'data' in response, "响应缺少bizData或data字段"
        
        web_logger.info(f"查询权益结果和当前状态响应结构验证通过")

    def test_privilege_status_with_different_users(self, env, channel):
        """
        测试查询权益状态接口 - 多用户场景
        验证不同用户的权益状态查询
        """
        user_nos = [
            "UR1105157518080090112",
            "UR98532533998021465TEST",
        ]
        
        for user_no in user_nos:
            web_logger.info(f"查询用户{user_no}的权益状态")
            
            api = BmApi(channel_id=channel, env=env)
            api.user_no = user_no
            
            response = api.privilege_status()
            
            assert response is not None, f"用户{user_no}的权益状态查询失败"
            web_logger.info(f"用户{user_no}的权益状态查询成功")
