"""
H5 协议查询接口测试
- quertAppAgreement() - 查询协议内容
- readAgreement() - 合同阅读

分层示例：
1. api/app/h5_api.py 只负责接口封装与必要参数补全
2. tests 层负责固定冒烟 + 参数覆盖
"""
import allure
import pytest

from api.app.h5_api import H5Api
from utils.logger_util import web_logger


@allure.feature("H5 协议查询接口")
@allure.story("协议查询")
class TestH5AgreementInterface:
    """H5 协议查询接口测试"""

    @pytest.fixture(scope="class", autouse=True)
    def setup_h5_api(self, request, env):
        """类级初始化：登录一次，整组用例复用同一个登录态。"""
        h5_api = H5Api(mobile="15009926666", scene="DRAW", env=env)
        h5_api.login()
        request.cls.h5_api = h5_api
        request.cls.env = env
        web_logger.info("H5 协议测试初始化完成，复用同一登录态执行查询与阅读接口")

    @allure.title("协议查询 - CREDIT 冒烟验证")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_query_app_agreement_credit_smoke(self):
        """
        单接口冒烟测试：
        只固定一组最稳定参数，验证接口通路可用。
        """
        response = self.h5_api.quertAppAgreement(data={
            "agreementScene": "CREDIT",
            "fileFormat": "html"
        })

        assert response is not None, "CREDIT 协议查询响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"
        web_logger.info(f"CREDIT 协议查询成功: {response}")

    @allure.title("协议查询 - 借款环节查询合同")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("agreement_scene", ["CREDIT", "DRAW", "BIND"])
    def test_query_app_agreement_different_scenes(self, agreement_scene):
        """
        参数覆盖测试：
        同一个接口，不同业务场景单独覆盖。
        - CREDIT: 固定参数查询
        - DRAW/BIND: 自动补 bindCardBizReq.applyNo
        """
        response = self.h5_api.quertAppAgreement(data={
            "agreementScene": agreement_scene,
            "fileFormat": "html"
        })

        assert response is not None, f"{agreement_scene} 协议查询响应为空"
        assert isinstance(response, dict), f"{agreement_scene} 响应应该是字典类型"
        web_logger.info(f"{agreement_scene} 协议查询成功: {response}")

    @allure.title("协议查询 - 场景自动补 applyNo")
    @allure.severity(allure.severity_level.NORMAL)
    def test_query_app_agreement_draw_auto_apply_no(self):
        """
        验证接口层能力：
        DRAW 场景不手动传 bindCardBizReq，
        由 h5_api 内部自动补 applyNo。
        """
        response = self.h5_api.quertAppAgreement(agreement_scene="DRAW")

        assert response is not None, "DRAW 协议查询响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"
        web_logger.info(f"DRAW 自动补 applyNo 查询成功: {response}")

    @allure.title("合同阅读 - 阅读成功")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_read_agreement_smoke(self):
        """
        合同阅读单接口测试：
        直接使用固定 previewFlowNo 验证接口通路。
        """
        response = self.h5_api.readAgreement(data={
            "previewFlowNo": "PW1194364760704450560",
            "readResult": "agree",
            "readTime": 10
        })

        assert response is not None, "合同阅读响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"
        web_logger.info(f"合同阅读联通性验证成功: {response}")

    @allure.title("合同阅读 - 阅读失败请求")
    @allure.severity(allure.severity_level.NORMAL)
    def test_read_agreement_fail(self):
        """
        合同阅读失败传参测试。
        """
        response = self.h5_api.readAgreement(data={
            "previewFlowNo": "PW1194364760704450560",
            "readResult": "reject",
            "readTime": 10
        })

        assert response is not None, "合同阅读响应为空"
        assert response.get("flag") == "S", "接口请求失败"
        web_logger.info(f"阅读失败状态请求成功，请求结果为{response.get('flag')}")


