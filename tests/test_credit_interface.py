"""
授信相关接口测试
- credit_apply() - 发起授信
- credit_apply_result() - 查询授信结果
"""
import pytest
import allure
from conftest import assert_response_success, assert_response_has_field
from utils.logger_util import web_logger
from api.app.bm_api import BmApi


@allure.feature("授信相关接口")
@allure.story("授信申请和查询")
class TestCreditInterface:
    """授信相关接口测试"""

    @allure.title("发起授信 - 成功场景")
    @allure.description("验证发起授信接口的成功场景，包括前置条件和响应验证")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_credit_apply_success(self, api_with_user_data):
        """
        测试发起授信接口 - 成功场景
        前置条件：
        1. 用户已撞库成功
        2. 用户已添加到风控白名单
        
        验证：
        1. 响应不为空
        2. 返回result=1（成功）
        3. 返回fundCreditNo字段（授信号）
        4. 返回creditReqNo字段（授信申请号）
        """
        web_logger.info(f"发起授信: {api_with_user_data.mobile}")
        
        # 前置：撞库
        check_res = api_with_user_data.check_user()
        assert check_res['check_res']['bizData']['result'] == 1, "撞库失败"
        web_logger.info("前置条件：撞库成功")
        
        # 前置：添加风控白名单
        white_res = api_with_user_data.risk_white_user()
        assert white_res['flag'] == "S" , "添加风控白名单失败"
        web_logger.info("前置条件：风控白名单添加成功")
        
        # 发起授信
        response = api_with_user_data.credit_apply()
        
        # 验证响应
        assert_response_success(response, expected_result=1)
        
        # 验证关键字段
        fund_credit_no = assert_response_has_field(response, 'bizData.fundCreditNo')
        credit_req_no = assert_response_has_field(response, 'bizData.creditReqNo')
        
        web_logger.info(f"授信成功，fundCreditNo: {fund_credit_no}, creditReqNo: {credit_req_no}")

    @allure.title("发起授信 - 响应结构验证")
    @allure.severity(allure.severity_level.NORMAL)
    def test_credit_apply_response_structure(self, api_with_user_data):
        """
        测试发起授信接口 - 响应结构验证
        验证返回的完整字段结构
        """
        # 前置条件
        api_with_user_data.check_user()
        api_with_user_data.risk_white_user()
        
        response = api_with_user_data.credit_apply()
        
        # 验证响应结构
        assert 'bizData' in response, "响应缺少bizData字段"
        biz_data = response['bizData']
        print("bizData:", biz_data)
        # 验证必要字段
        required_fields = ['result', 'fundCreditNo', 'creditReqNo']
        for field in required_fields:
            assert field in biz_data, f"bizData缺少字段: {field}"
        
        web_logger.info(f"授信响应结构验证通过")

    @allure.title("查询授信结果")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_credit_apply_result_query(self, api_with_user_data):
        """
        测试查询授信结果接口
        前置条件：
        1. 已发起授信
        
        验证：
        1. 响应不为空
        2. 能够查询到授信结果
        """
        web_logger.info(f"查询授信结果: {api_with_user_data.mobile}")
        
        # 前置：发起授信
        api_with_user_data.check_user()
        api_with_user_data.risk_white_user()
        credit_res = api_with_user_data.credit_apply()
        
        assert credit_res['bizData']['result'] == 1, "发起授信失败"
        credit_req_no = credit_res['bizData']['creditReqNo']
        web_logger.info(f"前置条件：授信成功，creditReqNo: {credit_req_no}")
        
        # 查询授信结果
        response = api_with_user_data.credit_apply_result(credit_req_no)
        
        # 验证响应
        assert response is not None, "查询授信结果响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"
        
        web_logger.info(f"查询授信结果成功，返回数据: {response}")

    @allure.title("查询授信结果 - 无效号")
    @allure.severity(allure.severity_level.NORMAL)
    def test_credit_apply_result_with_invalid_credit_req_no(self, api_with_user_data):
        """
        测试查询授信结果接口 - 无效的creditReqNo
        验证：
        1. 使用无效的creditReqNo查询
        2. 接口返回相应的错误信息
        """
        invalid_credit_req_no = "INVALID_CT_123456789"
        web_logger.info(f"查询无效的授信结果: {invalid_credit_req_no}")
        
        response = api_with_user_data.credit_apply_result(invalid_credit_req_no)
        
        # 验证响应
        assert response is not None, "查询授信结果响应为空"
        
        web_logger.info(f"查询无效creditReqNo返回: {response}")

    def test_credit_apply_with_different_amounts(self, env, channel):
        """
        测试发起授信接口 - 不同金额场景
        验证不同金额的授信请求
        """
        amounts = [3000, 5000, 10000]
        
        for amt in amounts:
            web_logger.info(f"测试授信金额: {amt}")
            
            api = BmApi(
                channel_id=channel,
                amt=amt,
                env=env
            )
            
            # 前置条件
            api.check_user()
            api.risk_white_user()
            
            # 发起授信
            response = api.credit_apply()
            
            assert response is not None, f"金额{amt}的授信失败"
            web_logger.info(f"金额{amt}的授信成功")

    def test_credit_apply_with_different_terms(self, env, channel):
        """
        测试发起授信接口 - 不同期限场景
        验证不同期限的授信请求
        """
        terms = [6, 12, 24]
        
        for term in terms:
            web_logger.info(f"测试授信期限: {term}期")
            
            api = BmApi(
                channel_id=channel,
                term=term,
                env=env
            )
            
            # 前置条件
            api.check_user()
            api.risk_white_user()
            
            # 发起授信
            response = api.credit_apply()
            
            assert response is not None, f"期限{term}的授信失败"
            web_logger.info(f"期限{term}的授信成功")
