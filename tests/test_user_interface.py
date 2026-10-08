"""
用户相关接口测试
- check_user() - 撞库
- risk_white_user() - 风控白名单
"""
import pytest
import allure
from conftest import assert_response_success, assert_response_has_field
from utils.logger_util import web_logger


@allure.feature("用户相关接口")
@allure.story("用户撞库和风控白名单")
class TestUserInterface:
    """用户相关接口测试"""

    @allure.title("撞库接口 - 成功场景")
    @allure.description("验证撞库接口的成功场景，包括响应结构和数据验证")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_check_user_success(self, api_with_user_data):
        """
        测试撞库接口 - 成功场景
        验证：
        1. 响应不为空
        2. 返回result=1（成功）
        3. 返回mobile字段
        4. 返回check_res字段
        """
        web_logger.info(f"测试用户: {api_with_user_data.mobile}")
        
        response = api_with_user_data.check_user()
        
        # 验证响应结构
        assert response is not None, "撞库接口响应为空"
        assert 'mobile' in response, "响应缺少mobile字段"
        assert 'check_res' in response, "响应缺少check_res字段"
        
        # 验证撞库结果
        check_res = response['check_res']
        assert_response_success(check_res, expected_result=1)
        
        # 验证返回的mobile与请求一致
        assert response['mobile'] == api_with_user_data.mobile, \
            f"返回的mobile不匹配: {response['mobile']} != {api_with_user_data.mobile}"
        
        web_logger.info(f"撞库成功，返回数据: {response}")

    @allure.title("撞库接口 - 带身份证号")
    @allure.description("验证撞库接口同时传入手机号和身份证号的场景")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_check_user_with_id_card(self, api_with_user_data):
        """
        测试撞库接口 - 带身份证号
        验证：
        1. 同时传入手机号和身份证号
        2. 接口正常返回
        """
        web_logger.info(f"测试用户(带身份证): {api_with_user_data.mobile}, {api_with_user_data.id_card}")
        
        response = api_with_user_data.check_user()
        
        assert response is not None, "撞库接口响应为空"
        assert 'check_res' in response, "响应缺少check_res字段"
        
        check_res = response['check_res']
        assert_response_success(check_res, expected_result=1)
        
        web_logger.info(f"撞库成功(带身份证)")

    @allure.title("风控白名单接口 - 成功场景")
    @allure.description("验证风控白名单接口的成功场景")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_risk_white_user_success(self, api_with_user_data):
        """
        测试风控白名单接口 - 成功场景
        验证：
        1. 响应不为空
        2. 返回flag=True
        3. 返回code字段
        """
        web_logger.info(f"添加风控白名单: {api_with_user_data.mobile}")
        
        response = api_with_user_data.risk_white_user()
        
        # 验证响应结构
        assert response is not None, "风控白名单接口响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"
        
        # 验证返回结果
        assert 'flag' in response, "响应缺少flag字段"
        assert response['flag'] == 'S', f"期望flag=S，实际flag={response['flag']}"
        
        web_logger.info(f"风控白名单添加成功，返回数据: {response}")

    @allure.title("风控白名单接口 - 响应结构验证")
    @allure.description("验证风控白名单接口返回的完整字段")
    @allure.severity(allure.severity_level.NORMAL)
    def test_risk_white_user_response_structure(self, api_with_user_data):
        """
        测试风控白名单接口 - 响应结构验证
        验证返回的完整字段
        """
        response = api_with_user_data.risk_white_user()
        
        # 验证必要字段
        required_fields = ['flag', 'code']
        for field in required_fields:
            assert field in response, f"响应缺少必要字段: {field}"
        
        web_logger.info(f"风控白名单响应结构验证通过")

    @allure.title("撞库接口 - 多用户场景")
    @allure.description("验证不同用户的撞库功能")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("mobile,name,id_card", [
        ('15605786856', '朱镨', '513029199609289243'),
        ('18711595893', '测试用户', '110101199001011234'),
    ])
    def test_check_user_multiple_users(self, env, channel, mobile, name, id_card):
        """
        测试撞库接口 - 多用户场景
        验证不同用户的撞库功能
        """
        from api.app.bm_api import BmApi
        
        api = BmApi(channel_id=channel, mobile=mobile, name=name, id_card=id_card, env=env)
        response = api.check_user()
        
        assert response is not None, f"用户{mobile}撞库失败"
        assert response['mobile'] == mobile, f"返回的mobile不匹配"
        
        web_logger.info(f"用户{mobile}撞库成功")
