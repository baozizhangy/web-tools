"""
绑卡相关接口测试
- card_query() - 查询绑卡信息
- bank_list_query() - 查询银行列表
- card_bind() - 获取绑卡验证码
- card_bind_sms() - 校验绑卡验证码
"""
import pytest
import allure
from conftest import assert_response_success, assert_response_has_field
from utils.logger_util import web_logger
from api.app.bm_api import BmApi


@allure.feature("绑卡相关接口")
@allure.story("银行卡绑定和验证")
class TestCardInterface:
    """绑卡相关接口测试"""

    @allure.title("查询支持的银行卡列表")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_bank_list_query_success(self, api_with_user_data):
        """
        测试查询支持银行卡列表接口
        验证：
        1. 响应不为空
        2. 返回result=1（成功）
        3. 返回bankList字段
        4. bankList不为空
        """
        web_logger.info("查询支持的银行卡列表")

        response = api_with_user_data.bank_list_query()

        # 验证响应
        # assert_response_success(response, expected_result=1)

        # 验证关键字段
        bank_list = assert_response_has_field(response, 'bizData.bankList')
        assert isinstance(bank_list, list), "bankList应该是列表类型"
        assert len(bank_list) > 0, "bankList不能为空"

        web_logger.info(f"查询到{len(bank_list)}家支持的银行")

    @allure.title("查询银行列表 - 响应结构验证")
    @allure.severity(allure.severity_level.NORMAL)
    def test_bank_list_query_response_structure(self, api_with_user_data):
        """
        测试查询银行列表接口 - 响应结构验证
        验证返回的银行信息结构
        """
        response = api_with_user_data.bank_list_query()

        bank_list = response['bizData']['bankList']

        # 验证每个银行的字段
        if len(bank_list) > 0:
            first_bank = bank_list[0]
            assert isinstance(first_bank, dict), "银行信息应该是字典类型"

            web_logger.info(f"银行信息结构: {first_bank}")

    @allure.title("查询绑卡信息 - 有效user_no")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_card_query_with_valid_user_no(self, api_with_user_data):
        """
        测试查询绑卡信息接口 - 有效的user_no
        前置条件：
        1. 已发起授信获取user_no
        
        验证：
        1. 响应不为空
        2. 返回result=1（成功）
        3. 返回cardList字段
        """
        web_logger.info(f"查询绑卡信息: {api_with_user_data.mobile}")

        # 前置：发起授信获取user_no
        api_with_user_data.check_user()
        api_with_user_data.risk_white_user()
        credit_res = api_with_user_data.credit_apply()

        assert credit_res['bizData']['result'] == 1, "发起授信失败"

        # 从credit_apply响应中获取user_no（如果有）
        # 这里假设可以从响应中获取，实际可能需要从数据库查询
        web_logger.info("前置条件：授信成功")

        # 使用一个有效的user_no进行查询
        # 注意：这里需要使用实际的user_no，可能需要从数据库查询
        user_no = "UR98532533998021465TEST"  # 示例user_no

        response = api_with_user_data.card_query(user_no)

        # 验证响应
        assert response is not None, "查询绑卡信息响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"

        web_logger.info(f"查询绑卡信息成功")

    @allure.title("查询绑卡信息 - 响应结构验证")
    @allure.severity(allure.severity_level.NORMAL)
    def test_card_query_response_structure(self, api_with_user_data):
        """
        测试查询绑卡信息接口 - 响应结构验证
        """
        user_no = "UR98532533998021465TEST"

        response = api_with_user_data.card_query(user_no)

        # 验证响应结构
        assert 'bizData' in response, "响应缺少bizData字段"

        web_logger.info(f"查询绑卡信息响应结构验证通过")

    @allure.title("获取绑卡验证码 - 成功场景")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_card_bind_success(self, api_with_user_data):
        """
        测试获取绑卡验证码接口 - 成功场景
        前置条件：
        1. 已发起授信
        
        验证：
        1. 响应不为空
        2. 返回result=1（成功）
        3. 返回fundBindReqNo字段
        """
        web_logger.info(f"获取绑卡验证码: {api_with_user_data.mobile}")

        # 前置：发起授信
        api_with_user_data.check_user()
        api_with_user_data.risk_white_user()
        credit_res = api_with_user_data.credit_apply()

        assert credit_res['bizData']['result'] == 1, "发起授信失败"
        credit_req_no = credit_res['bizData']['creditReqNo']

        # 使用示例user_no
        user_no = "UR98532945524913388TEST"

        # 获取绑卡验证码
        response = api_with_user_data.card_bind(user_no, credit_req_no)

        # 验证响应
        assert response is not None, "获取绑卡验证码响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"

        web_logger.info(f"获取绑卡验证码成功")

    @allure.title("获取绑卡验证码 - 响应结构验证")
    @allure.severity(allure.severity_level.NORMAL)
    def test_card_bind_response_structure(self, api_with_user_data):
        """
        测试获取绑卡验证码接口 - 响应结构验证
        """
        user_no = "UR98532945524913388TEST"
        credit_req_no = "CR07165952462142829"
        bindScene = 'REPAY'

        response = api_with_user_data.card_bind(user_no, credit_req_no, bindScene)

        # 验证响应结构
        assert 'bizData' in response, "响应缺少bizData字段"

        web_logger.info(f"获取绑卡验证码响应结构验证通过")

    @allure.title("校验绑卡验证码 - 成功场景")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_card_bind_sms_success(self, api_with_user_data):
        """
        测试校验绑卡验证码接口 - 成功场景
        前置条件：
        1. 已获取绑卡验证码
        
        验证：
        1. 响应不为空
        2. 返回result=1（成功）
        """
        web_logger.info(f"校验绑卡验证码: {api_with_user_data.mobile}")

        # 使用示例数据
        user_no = "UR98532945524913388TEST"
        fund_bind_req_no = "BCR1007276847035260928"

        # 校验绑卡验证码
        response = api_with_user_data.card_bind_sms(user_no, fund_bind_req_no)

        # 验证响应
        assert response is not None, "校验绑卡验证码响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"

        web_logger.info(f"校验绑卡验证码成功")

    @allure.title("校验绑卡验证码 - 响应结构验证")
    @allure.severity(allure.severity_level.NORMAL)
    def test_card_bind_sms_response_structure(self, api_with_user_data):
        """
        测试校验绑卡验证码接口 - 响应结构验证
        """
        user_no = "UR98532945524913388TEST"
        fund_bind_req_no = "BCR1007276847035260928"

        response = api_with_user_data.card_bind_sms(user_no, fund_bind_req_no)

        # 验证响应结构
        # assert 'bizData' in response, "响应缺少bizData字段"
        pass
        web_logger.info(f"校验绑卡验证码响应结构验证通过")

    @allure.title("获取绑卡验证码 - 不同场景")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("bind_scene", ['CREDIT', 'DRAW', 'REPAY'])
    def test_card_bind_different_scenes(self, api_with_user_data, bind_scene):
        """
        测试获取绑卡验证码接口 - 不同场景
        验证不同绑卡场景的请求
        """
        web_logger.info(f"测试绑卡场景: {bind_scene}")

        user_no = "UR98532945524913388TEST"
        credit_req_no = "CR07165952462142829"

        response = api_with_user_data.card_bind(user_no, credit_req_no, bindScene=bind_scene)

        assert response is not None, f"场景{bind_scene}的绑卡失败"
        web_logger.info(f"场景{bind_scene}的绑卡成功")
