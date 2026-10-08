#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
import datetime
import threading
from time import sleep

import allure
import pytest
from dateutil.relativedelta import relativedelta
from jsonpath_ng import parse

from config import db_conn
from h5_login import H5Login
from api.app.loan_bill import LoanBill


@pytest.mark.repay
@allure.feature("H5 还款单接口")
class TestH5RepaySingleApi:
    """H5 还款单接口测试"""

    @staticmethod
    def _to_dict(response):
        return response if isinstance(response, dict) else json.loads(response)

    def _init_loan_bill_once(self, env, loan_no: str):
        """每次测试后触发一次借据初始化（异步，不等待结果）"""
        init_date = (datetime.datetime.now() - relativedelta(months=2)).strftime("%Y-%m-%d")

        def _run_init():
            LoanBill(loan_no=loan_no, init_date=init_date, env=env).init_plan_1()

        threading.Thread(target=_run_init, daemon=True).start()

    def _query_repay_sms_code(self, env, mobile_no: str) -> str:
        sql = (
            "select params from cns.p_notice_record "
            "where user_no = (select user_no from cis.u_user "
            f"where mobile_no_md5 = md5('{mobile_no}')) "
            "and event_code = 'e_repay_identity_verify_code' "
            "order by id desc limit 1"
        )
        result = db_conn(env).select_one(sql)
        assert result.get("code") == "0" and result.get("data"), f"还款验证码查询失败: {result}"
        return str(parse("$.params.code").find(json.loads(result["data"]["params"]))[0].value)

    def _get_loan_info(self, h5):
        repay_list_res = self._to_dict(h5.post("/clg/lps/api/u/bm/repay/v1/repay/list", data={}))
        loan_req_no = str(parse("$.data.repayList[0].loanReqNo").find(repay_list_res)[0].value)
        loan_no = str(parse("$.data.repayList[0].loanNo").find(repay_list_res)[0].value)
        self._current_loan_no = loan_no
        return repay_list_res, loan_req_no, loan_no

    @pytest.fixture(autouse=True)
    def _after_each_test_init_bill(self, env):
        self._current_loan_no = None
        self._need_init_bill = False
        yield
        if self._need_init_bill and self._current_loan_no:
            with allure.step("初始化借据"):
                self._init_loan_bill_once(env, self._current_loan_no)

    @pytest.fixture
    def h5_client(self, env):
        mobile_no = "14511936328"
        h5 = H5Login(env=env, mobile_no=mobile_no)
        h5.login()
        return h5, mobile_no

    @allure.story("repay/list")
    def test_repay_list_success(self, h5_client):
        h5, _ = h5_client
        with allure.step("调用 repay/list"):
            res, _, _ = self._get_loan_info(h5)
            allure.attach(json.dumps(res, ensure_ascii=False, indent=2), "repay_list", allure.attachment_type.JSON)
            assert res.get("code") in [0, "0", 200, "200"], f"repay/list 失败: {res}"
            assert parse("$.data.repayList[0].loanReqNo").find(res), f"未返回 loanReqNo: {res}"
            assert parse("$.data.repayList[0].loanNo").find(res), f"未返回 loanNo: {res}"

    @allure.story("billDetails")
    def test_bill_details_success(self, h5_client):
        h5, _ = h5_client
        _, loan_req_no, loan_no = self._get_loan_info(h5)

        with allure.step("调用 billDetails"):
            res = self._to_dict(
                h5.post(
                    "/clg/lps/api/u/bm/repay/v1/billDetails",
                    data={"loanReqNo": loan_req_no, "loanNo": loan_no},
                )
            )
            allure.attach(json.dumps(res, ensure_ascii=False, indent=2), "bill_details", allure.attachment_type.JSON)
            assert res.get("code") in [0, "0", 200, "200"], f"billDetails 失败: {res}"
            assert parse("$.data.repayDetails[0].term").find(res), f"未返回 term: {res}"

    @allure.story("trial")
    def test_trial_success(self, h5_client):
        h5, _ = h5_client
        _, loan_req_no, loan_no = self._get_loan_info(h5)
        bill_res = self._to_dict(
            h5.post(
                "/clg/lps/api/u/bm/repay/v1/billDetails",
                data={"loanReqNo": loan_req_no, "loanNo": loan_no},
            )
        )
        terms = str(parse("$.data.repayDetails[0].term").find(bill_res)[0].value)

        with allure.step("调用 trial"):
            res = self._to_dict(
                h5.post(
                    "/clg/lps/api/u/bm/repay/v1/trial",
                    data={
                        "loanNo": loan_no,
                        "loanReqNo": loan_req_no,
                        "repayType": "SINGLE",
                        "terms": terms,
                    },
                )
            )
            allure.attach(json.dumps(res, ensure_ascii=False, indent=2), "trial", allure.attachment_type.JSON)
            assert res.get("code") in [0, "0", 200, "200"], f"trial 失败: {res}"
            assert parse("$.data.totalAmount").find(res), f"未返回 totalAmount: {res}"
            assert parse("$.data.cardInfo.cardId").find(res), f"未返回 cardId: {res}"

    @allure.story("submit")
    def test_submit_success(self, h5_client):
        h5, _ = h5_client
        _, loan_req_no, loan_no = self._get_loan_info(h5)
        bill_res = self._to_dict(
            h5.post(
                "/clg/lps/api/u/bm/repay/v1/billDetails",
                data={"loanReqNo": loan_req_no, "loanNo": loan_no},
            )
        )
        terms = parse("$.data.repayDetails[0].term").find(bill_res)[0].value
        trial_res = self._to_dict(
            h5.post(
                "/clg/lps/api/u/bm/repay/v1/trial",
                data={
                    "loanNo": loan_no,
                    "loanReqNo": loan_req_no,
                    "repayType": "SINGLE",
                    "terms": str(terms),
                },
            )
        )
        repay_apply_amt = parse("$.data.totalAmount").find(trial_res)[0].value
        card_id = parse("$.data.cardInfo.cardId").find(trial_res)[0].value

        with allure.step("调用 submit"):
            res = self._to_dict(
                h5.post(
                    "/clg/lps/api/u/bm/repay/v1/submit",
                    data={
                        "loanReqNo": loan_req_no,
                        "loanNo": loan_no,
                        "repayType": "SINGLE",
                        "terms": terms,
                        "channelSource": "",
                        "repayApplyAmt": str(repay_apply_amt),
                        "cardId": str(card_id),
                        "preComSerFeeOffline": False,
                    },
                )
            )
            allure.attach(json.dumps(res, ensure_ascii=False, indent=2), "submit", allure.attachment_type.JSON)
            assert res.get("code") in [0, "0", 200, "200"], f"submit 失败: {res}"
            assert parse("$.data.repayReqNo").find(res), f"未返回 repayReqNo: {res}"

    @allure.story("verify/sms")
    def test_verify_sms_success(self, env, h5_client):
        h5, mobile_no = h5_client
        _, loan_req_no, loan_no = self._get_loan_info(h5)
        bill_res = self._to_dict(
            h5.post(
                "/clg/lps/api/u/bm/repay/v1/billDetails",
                data={"loanReqNo": loan_req_no, "loanNo": loan_no},
            )
        )
        terms = parse("$.data.repayDetails[0].term").find(bill_res)[0].value
        trial_res = self._to_dict(
            h5.post(
                "/clg/lps/api/u/bm/repay/v1/trial",
                data={
                    "loanNo": loan_no,
                    "loanReqNo": loan_req_no,
                    "repayType": "SINGLE",
                    "terms": str(terms),
                },
            )
        )
        repay_apply_amt = parse("$.data.totalAmount").find(trial_res)[0].value
        card_id = parse("$.data.cardInfo.cardId").find(trial_res)[0].value

        submit_res = self._to_dict(
            h5.post(
                "/clg/lps/api/u/bm/repay/v1/submit",
                data={
                    "loanReqNo": loan_req_no,
                    "loanNo": loan_no,
                    "repayType": "SINGLE",
                    "terms": terms,
                    "channelSource": "",
                    "repayApplyAmt": str(repay_apply_amt),
                    "cardId": str(card_id),
                    "preComSerFeeOffline": False,
                },
            )
        )
        repay_req_no = str(parse("$.data.repayReqNo").find(submit_res)[0].value)

        sleep(3)
        sms_code = self._query_repay_sms_code(env, mobile_no)

        with allure.step("调用 verify/sms"):
            res = self._to_dict(
                h5.post(
                    "/clg/lps/api/u/bm/common/v1/verify/sms",
                    data={
                        "bizNo": repay_req_no,
                        "smsCode": sms_code,
                        "scene": "02",
                        "preComSerFeeOffline": False,
                    },
                )
            )
            allure.attach(json.dumps(res, ensure_ascii=False, indent=2), "verify_sms", allure.attachment_type.JSON)
            assert res.get("code") in [0, "0", 200, "200"], f"verify/sms 失败: {res}"
            self._need_init_bill = True
