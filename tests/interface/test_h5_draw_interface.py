"""
H5 借款相关接口测试
- draw_pre_query() - 借款基础信息查询
- draw_trial() - 借款试算
- draw_submit() - 借款提交
- draw_result() - 借款结果查询
- draw_supply_query() - 借款补件查询
- draw_supply_submit() - 借款补件提交
"""
import allure
import pytest

from config import db_conn
from api.app.h5_api import H5Api
from utils.logger_util import web_logger

DRAW_TEST_MOBILE = '18510341393'
DRAW_HISTORY_MOBILE = '19116851522'


@pytest.fixture
def draw_api(env):
    """借款接口专属前置：清洗数据后初始化 H5Api 并登录。"""
    sql = (
        "update lps.bm_iou set loan_state = 'DJ' "
        "where user_no = (select user_no from cis.u_user "
        f"where mobile_no_md5 = md5('{DRAW_TEST_MOBILE}')) and loan_state != 'DS';"
    )
    db_conn(env).exec_one(sql)

    h5_api = H5Api(mobile=DRAW_TEST_MOBILE, scene='DRAW', env=env)
    h5_api.login()
    return h5_api


@pytest.fixture
def prepared_draw_context(draw_api):
    """借款实时场景上下文：统一复用 applyNo 与 loanFlowNo。"""
    context = draw_api.prepare_draw_context()
    return {
        "h5_api": draw_api,
        "applyNo": context["applyNo"],
        "loanFlowNo": context["loanFlowNo"],
        "preQueryResponse": context["preQueryResponse"],
    }


@allure.feature("H5 借款相关接口")
@allure.story("借款基础信息、试算、提交、结果与补件")
class TestH5DrawInterface:
    """H5 借款相关接口测试"""

    @allure.title("借款基础信息查询")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_draw_pre_query(self, draw_api):
        request_data = draw_api.build_draw_pre_query_data()

        response = draw_api.draw_pre_query(data=request_data)
        memberCardInfoList = response.get("privilegeInfo").get('memberCardInfoList')
        assert response is not None, "借款基础信息查询响应为空"
        assert len(memberCardInfoList), "当前用户未购买权益"
        web_logger.info(f"借款基础信息查询成功: {response}")

    @allure.title("借款试算")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_draw_trial(self, prepared_draw_context):
        h5_api = prepared_draw_context["h5_api"]
        request_data = h5_api.build_draw_trial_data(
            trial_amt="3000",
            term=12,
            apply_no=prepared_draw_context["applyNo"],
            loan_flow_no=prepared_draw_context["loanFlowNo"],
        )

        response = h5_api.draw_trial(data=request_data)

        assert response is not None, "借款试算响应为空"
        resp_amt = response.get("prinAmt")
        resp_trem = response.get("totalTerms")
        assert resp_amt == "3000.00", "借款试算金额有误"
        assert resp_trem == "12", "借款试算期限有误"
        web_logger.info(f"借款试算成功: {response}")

    @allure.title("借款提交")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_draw_submit(self, prepared_draw_context):
        h5_api = prepared_draw_context["h5_api"]
        request_data = h5_api.build_draw_submit_data(
            apply_no=prepared_draw_context["applyNo"],
            card_id="BMCI1195546293322485761",
            loan_amt="3000",
            loan_term="12",
            loan_flow_no=prepared_draw_context["loanFlowNo"],
            loan_purpose_desc="购物",
            loan_purpose_code="01",
            is_privilege_process="N",
            privilege_config_uid="",
        )

        response = h5_api.draw_submit(data=request_data)

        assert response is not None, "借款提交响应为空"
        resp_amt = response.get("loanAmt")
        resp_term = response.get("term")
        assert resp_amt == "3000.00", "借款提交金额有误"
        assert resp_term == "12", "借款提交期限有误"
        web_logger.info(f"借款提交成功: {response}")

    @allure.title("借款结果查询")
    @allure.severity(allure.severity_level.NORMAL)
    def test_draw_result(self, env):
        h5_api = H5Api(mobile=DRAW_HISTORY_MOBILE, scene='DRAW', env=env)
        request_data = h5_api.build_draw_result_data(
            apply_no="AP1181106828290781184",
            loan_req_no="LP1181615697962184704",
        )

        response = h5_api.draw_result(data=request_data)

        assert response is not None, "借款结果查询响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"
        web_logger.info(f"借款结果查询成功: {response}")

    @allure.title("借款补件查询")
    @allure.severity(allure.severity_level.NORMAL)
    def test_draw_supply_query(self, env):
        h5_api = H5Api(mobile=DRAW_HISTORY_MOBILE, scene='DRAW', env=env)
        request_data = h5_api.build_draw_supply_query_data(
            loan_req_no="LP1181615697962184704",
        )

        response = h5_api.draw_supply_query(data=request_data)

        assert response is not None, "借款补件查询响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"
        web_logger.info(f"借款补件查询成功: {response}")

    @allure.title("借款补件提交")
    @allure.severity(allure.severity_level.NORMAL)
    def test_draw_supply_submit(self, env):
        h5_api = H5Api(mobile=DRAW_HISTORY_MOBILE, scene='DRAW', env=env)
        request_data = h5_api.build_draw_supply_submit_data(
            loan_req_no="LP1181615697962184704",
            address="上海市-上海市辖区-徐汇区",
            address_detail="测试工具执行单接口测试补充数据",
        )

        response = h5_api.draw_supply_submit(data=request_data)

        assert response is not None, "借款补件提交响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"
        web_logger.info(f"借款补件提交成功: {response}")
