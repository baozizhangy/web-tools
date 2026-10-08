"""
H5 还款相关接口测试
- repay_list() - 待还列表查询
- repay_bill_details() - 还款详情查询
- repay_trial() - 还款试算
- repay_submit() - 还款提交
"""
import allure
import pytest
from jsonpath_ng import parse

from api.app.h5_api import H5Api
from utils.logger_util import web_logger


REPAY_TEST_MOBILE = "14511936328"


@pytest.fixture
def repay_api(env):
    """还款接口专属前置：初始化 H5Api 并登录。"""
    h5_api = H5Api(mobile=REPAY_TEST_MOBILE, scene='REPAY', env=env)
    h5_api.login()
    return h5_api


@pytest.fixture
def repay_context(repay_api):
    """还款实时场景上下文：统一复用 loanReqNo、loanNo、term、repayApplyAmt、cardId。"""
    repay_list_res = repay_api.repay_list(data={})
    assert repay_list_res is not None, "待还列表响应为空"
    assert isinstance(repay_list_res, dict), "待还列表响应应该是字典类型"

    loan_req_no = str(parse("$.data.repayList[0].loanReqNo").find(repay_list_res)[0].value)
    loan_no = str(parse("$.data.repayList[0].loanNo").find(repay_list_res)[0].value)

    bill_details_data = repay_api.build_repay_bill_details_data(loan_req_no=loan_req_no, loan_no=loan_no)
    bill_details_res = repay_api.repay_bill_details(data=bill_details_data)
    assert bill_details_res is not None, "还款详情响应为空"
    assert isinstance(bill_details_res, dict), "还款详情响应应该是字典类型"

    terms = parse("$.data.repayDetails[0].term").find(bill_details_res)[0].value

    trial_data = repay_api.build_repay_trial_data(
        loan_req_no=loan_req_no,
        loan_no=loan_no,
        terms=terms,
    )
    trial_res = repay_api.repay_trial(data=trial_data)
    assert trial_res is not None, "还款试算响应为空"
    assert isinstance(trial_res, dict), "还款试算响应应该是字典类型"

    repay_apply_amt = parse("$.data.totalAmount").find(trial_res)[0].value
    card_id = parse("$.data.cardInfo.cardId").find(trial_res)[0].value

    return {
        "h5_api": repay_api,
        "repay_list": repay_list_res,
        "loanReqNo": loan_req_no,
        "loanNo": loan_no,
        "bill_details": bill_details_res,
        "terms": terms,
        "trial": trial_res,
        "repayApplyAmt": repay_apply_amt,
        "cardId": card_id,
    }


@allure.feature("H5 还款相关接口")
@allure.story("待还列表、详情、试算与提交")
class TestH5RepayInterface:
    """H5 还款相关接口测试"""

    @allure.title("待还列表查询")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_repay_list(self, repay_api):
        response = repay_api.repay_list(data={})

        assert response is not None, "待还列表响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"
        web_logger.info(f"待还列表查询成功: {response}")

    @allure.title("还款详情查询")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_repay_bill_details(self, repay_context):
        response = repay_context["bill_details"]

        assert response is not None, "还款详情响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"
        web_logger.info(f"还款详情查询成功: {response}")

    @allure.title("还款试算")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_repay_trial(self, repay_context):
        response = repay_context["trial"]

        assert response is not None, "还款试算响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"
        web_logger.info(f"还款试算成功: {response}")

    @allure.title("还款提交")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_repay_submit(self, repay_context):
        h5_api = repay_context["h5_api"]
        submit_data = h5_api.build_repay_submit_data(
            loan_req_no=repay_context["loanReqNo"],
            loan_no=repay_context["loanNo"],
            terms=repay_context["terms"],
            repay_apply_amt=repay_context["repayApplyAmt"],
            card_id=repay_context["cardId"],
        )

        response = h5_api.repay_submit(data=submit_data)

        assert response is not None, "还款提交响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"
        web_logger.info(f"还款提交成功: {response}")
