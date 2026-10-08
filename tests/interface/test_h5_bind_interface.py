"""
H5 绑卡相关接口测试
- query_user_bank_card_list() - 查询用户绑卡列表
- query_card_info() - 查询卡 bin 信息
- bank_submit() - 绑卡提交
- bank_verification() - 绑卡验证码校验
"""
import allure

from api.app.h5_api import H5Api
from utils.logger_util import web_logger


@allure.feature("H5 绑卡相关接口")
@allure.story("绑卡列表、卡bin、绑卡提交与验证码校验")
class TestH5BindInterface:
    """H5 绑卡相关接口测试"""

    @allure.title("查询用户绑卡列表-- 未绑卡用户13609489732")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_query_user_bank_card_list_none(self, env):
        """
        查询用户绑卡列表。
        请求 data 为空。
        - $.data.cardList = [] 表示未绑卡
        - $.data.cardList 非空表示已绑卡成功
        """
        h5_api = H5Api(mobile='13609489732', scene='DRAW', env=env)

        response = h5_api.query_user_bank_card_list()
        assert 'data' in response, "响应缺少 data 字段"
        assert 'cardList' in response['data'], "响应缺少 data.cardList 字段"

        card_list = response['data']['cardList']
        assert card_list is not None, "响应 data.cardList 字段为空"

        if len(card_list) == 0:
            web_logger.info("当前用户未绑卡，data.cardList = []")
        else:
            web_logger.info(f"当前用户已有绑卡信息，cardList={card_list}")

    @allure.title("查询用户绑卡列表-- 已绑卡用户18713341122")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_query_user_bank_card_list(self, env):
        h5_api = H5Api(mobile='18713341122', scene='DRAW', env=env)

        response = h5_api.query_user_bank_card_list()

        assert 'data' in response, "响应缺少 data 字段"
        assert 'cardList' in response['data'], "响应缺少 data.cardList 字段"

        card_list = response['data']['cardList']
        assert card_list is not None, "响应 data.cardList 字段为空"

        if len(card_list) == 0:
            web_logger.info("当前用户未绑卡，data.cardList = []")
        else:
            web_logger.info(f"当前用户已有绑卡信息，cardList={card_list}")

    @allure.title("查询卡bin信息- 测试用户19116851522")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_query_card_info(self, env):
        """
        查询卡 bin 信息。
        固定卡号验证接口联通性。
        """
        h5_api = H5Api(mobile='19116851522', scene='DRAW', env=env)

        response = h5_api.query_card_info(data={
            "cardNo": "620200177371571133"
        })

        assert response is not None, "查询卡bin信息响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"
        web_logger.info(f"查询卡bin信息成功: {response}")

    @allure.title("绑卡提交 - 单接口联通性验证-测试用户15317261864")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_bank_submit_smoke(self, env):
        """
        单接口验证：
        使用随机卡号 + 自动补 applyNo，验证 bindCardSubmit 接口可用。
        """
        h5_api = H5Api(mobile='15317261864', scene='DRAW', env=env)
        submit_data = h5_api.build_bank_submit_data(bind_scene="DRAW")

        response = h5_api.bank_submit(data=submit_data)

        assert response is not None, "绑卡提交响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"
        web_logger.info(f"绑卡提交成功，submit_data={submit_data}, response={response}")

    @allure.title("绑卡验证码校验 - 依赖绑卡提交联调")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_bank_verification_with_submit(self, env):
        """
        联调用例：
        1. 先调用 bindCardSubmit
        2. 从返回结果中获取 bindCardReqNo
        3. 再调用 bindCardVerification
        """
        h5_api = H5Api(mobile='19818810075', scene='DRAW', env=env)
        submit_data = h5_api.build_bank_submit_data(bind_scene="DRAW")
        submit_response = h5_api.bank_submit(data=submit_data)

        assert submit_response is not None, "绑卡提交响应为空"
        assert isinstance(submit_response, dict), "绑卡提交响应应该是字典类型"
        assert 'data' in submit_response, "绑卡提交响应缺少 data 字段"
        assert 'bindCardReqNo' in submit_response['data'], "绑卡提交响应缺少 data.bindCardReqNo 字段"

        bind_card_req_no = submit_response['data']['bindCardReqNo']

        verify_response = h5_api.bank_verification(data={
            "bindCardReqNo": bind_card_req_no,
            "smsCode": "111111"
        })

        assert verify_response is not None, "绑卡验证码校验响应为空"
        assert isinstance(verify_response, dict), "响应应该是字典类型"
        web_logger.info(
            f"绑卡验证码校验完成，submit_data={submit_data}, bindCardReqNo={bind_card_req_no}, response={verify_response}"
        )

    @allure.title("查询用户默认银行卡")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_query_user_default_bank_card(self, env):
        """
        查询用户默认银行卡。
        """
        h5_api = H5Api(mobile='19818810075', scene='DRAW', env=env)
        apply_no = h5_api._get_apply_no()
        response = h5_api.query_user_default_bank_card(data={'applyNo': apply_no})
        assert response is not None, "查询用户默认银行卡响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"
        web_logger.info(f"查询用户默认银行卡成功: {response}")
