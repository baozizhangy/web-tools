#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
import sys
import datetime
import threading
from time import sleep

import allure
import pytest
from dateutil.relativedelta import relativedelta
from jsonpath_ng import parse
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config import db_conn
from api.app.h5_api import H5Api
from api.app.loan_bill import LoanBill
from djangoWebTools.tools.bm_tools.ask_xxl import xxl_job_trigger


@allure.feature("H5 还款流程")
class TestH5RepayFlow:
    """H5 还款流程测试（试算 -> 提交 -> 短信确认 -> 支付结果）"""

    def _init_h5(self, env, mobile_no: str):
        self.h5 = H5Api(mobile=mobile_no, scene='REPAY', env=env)
        self.h5.login()

    @staticmethod
    def _to_dict(response):
        return response if isinstance(response, dict) else json.loads(response)

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
        sms_code = str(parse("$.params.code").find(json.loads(result["data"]["params"]))[0].value)
        return sms_code

    @staticmethod
    def _get_repay_req_no(submit_res: dict) -> str:
        """repayReqNo 必须有值，否则视为还款发起失败"""
        matches = parse("$.data.repayReqNo").find(submit_res)
        if not matches:
            raise AssertionError(f"还款发起失败：未找到 $.data.repayReqNo, submit响应: {submit_res}")

        repay_req_no = matches[0].value
        if repay_req_no is None or str(repay_req_no).strip() == "":
            raise AssertionError(f"还款发起失败：$.data.repayReqNo 为空, submit响应: {submit_res}")

        return str(repay_req_no)

    def _query_pay_status(self, env, repay_req_no: str) -> str:
        """
        查询支付状态。
        数据库响应按 json 取值 $.data.status
        """
        sql = f"select status from lcs.tr_tran_proc_rp where rp_request_no = '{repay_req_no}';"
        result = db_conn(env).select_one(sql)
        result = self._to_dict(result)

        status_matches = parse("$.data.status").find(result)
        if not status_matches:
            return ""
        return str(status_matches[0].value)

    @staticmethod
    def _status_text(status: str) -> str:
        status_map = {
            "02": "交易处理中",
            "03": "交易成功",
            "04": "交易失败",
            "05": "部分成功",
        }
        return status_map.get(status, f"未知状态({status})")

    def _poll_pay_result(self, env, repay_req_no: str, max_rounds: int = 3) -> str:
        """
        支付结果轮询：
        - 每轮间隔10秒
        - 触发一次 xxl_job_trigger(id=107)
        - 查询状态
        - status=02 继续轮询
        - 其他状态立即返回
        """
        final_status = ""
        for _ in range(max_rounds):
            sleep(10)
            xxl_job_trigger(job_id='107', executor_param=None, env=env)
            final_status = self._query_pay_status(env, repay_req_no)
            if final_status != "02":
                return self._status_text(final_status)

        return self._status_text(final_status)

    def _init_loan_bill(self, loan_no: str, env: str):
        """支付结果输出后，初始化借据一次（异步触发，不等待结果）"""
        init_date = (datetime.datetime.now() - relativedelta(months=2)).strftime("%Y-%m-%d")

        def _run_init():
            LoanBill(loan_no=loan_no, init_date=init_date, env=env).init_plan_1()

        threading.Thread(target=_run_init, daemon=True).start()
        return "S"

    def _run_repay_submit_verify_flow(
        self,
        env,
        mobile_no,
        repay_type: str = "SINGLE",
        use_coupon: bool = False,
    ):
        self._init_h5(env, str(mobile_no))

        # 1) 待还列表
        repay_list_res = self._to_dict(self.h5.repay_list(data={}))
        repay_list = parse("$.data.repayList").find(repay_list_res)
        assert repay_list and len(repay_list[0].value) > 0, f"待还列表为空: {repay_list_res}"
        loan_req_no = str(repay_list[0].value[0]["loanReqNo"])
        loan_no = str(repay_list[0].value[0]["loanNo"])

        # 2) 应还详情
        bill_details_data = self.h5.build_repay_bill_details_data(loan_req_no=loan_req_no, loan_no=loan_no)
        bill_details_res = self._to_dict(self.h5.repay_bill_details(data=bill_details_data))
        repay_details = parse("$.data.repayDetails").find(bill_details_res)
        assert repay_details and len(repay_details[0].value) > 0, f"应还详情为空: {bill_details_res}"

        # 优惠券处理
        coupon_no = ""
        if use_coupon:
            coupon_info = parse("$.data.couponInfo").find(bill_details_res)
            coupon_info_value = coupon_info[0].value if coupon_info else None
            if coupon_info_value and coupon_info_value.get("couponNo"):
                coupon_no = str(coupon_info_value["couponNo"])
            else:
                raise AssertionError(f"未查询到可用优惠券，无法使用优惠券还款: {bill_details_res}")

        terms = repay_details[0].value[0]["term"]

        # 3) 试算
        trial_data = self.h5.build_repay_trial_data(
            loan_req_no=loan_req_no,
            loan_no=loan_no,
            terms=terms,
            repay_type=repay_type,
            couponNo=coupon_no,
        )
        trial_res = self._to_dict(self.h5.repay_trial(data=trial_data))
        assert trial_res.get("code") in [0, "0", 200, "200"], f"trial 接口失败: {trial_res}"
        assert str(trial_res.get("flag")) != "F", f"还款试算失败: {trial_res}"

        repay_apply_amt = parse("$.data.totalAmount").find(trial_res)[0].value
        card_id = parse("$.data.cardInfo.cardId").find(trial_res)[0].value

        # 4) 提交还款
        submit_data = self.h5.build_repay_submit_data(
            loan_req_no=loan_req_no,
            loan_no=loan_no,
            terms=terms,
            repay_apply_amt=repay_apply_amt,
            card_id=card_id,
            repay_type=repay_type,
            couponNo=coupon_no,
        )
        submit_res = self._to_dict(self.h5.repay_submit(data=submit_data))
        assert submit_res.get("code") in [0, "0", 200, "200"], f"submit 接口失败: {submit_res}"
        # repayReqNo 必须存在，否则直接失败
        repay_req_no = self._get_repay_req_no(submit_res)

        # 5) 等待并查库拿验证码
        sleep(3)
        sms_code = self._query_repay_sms_code(env, str(mobile_no))

        # 6) 确认还款
        verify_data = {
            "bizNo": repay_req_no,
            "smsCode": sms_code,
            "scene": "02",
            "preComSerFeeOffline": False,
        }
        if coupon_no:
            verify_data["couponNo"] = coupon_no
        verify_res = self._to_dict(self.h5.post("/clg/lps/api/u/bm/common/v1/verify/sms", data=verify_data))
        assert verify_res.get("code") in [0, "0", 200, "200"], f"verify/sms 接口失败: {verify_res}"

        # 7) 查询还款结果
        repay_result_data = {
            "loanNo": loan_no,
            "loanReqNo": loan_req_no,
            "repayType": repay_type,
            "repayApplyAmt": str(repay_apply_amt),
            "terms": terms,
            "cardId": str(card_id),
            "couponNo": coupon_no,
        }
        repay_result_res = self._to_dict(self.h5.repay_result(data=repay_result_data))

        # 8) 轮询支付结果：02继续查，其他状态直接返回
        pay_result = self._poll_pay_result(env, repay_req_no, max_rounds=3)

        # 输出支付结果后，初始化借据一次（不等待结果）
        print(f"支付结果: {pay_result}")
        with allure.step("初始化借据"):
            self._init_loan_bill(loan_no=loan_no, env=env)

        return {
            "message": "还款申请成功",
            "repayReqNo": repay_req_no,
            "payResult": pay_result,
            "loanNo": loan_no,
            "repay_list": repay_list_res,
            "bill_details": bill_details_res,
            "trial": trial_res,
            "submit": submit_res,
            "verify": verify_res,
            "repay_result": repay_result_res,
        }

    @allure.story("待还列表 -> 应还期数 -> 还款试算 -> 提交 -> 短信确认 -> 支付结果")
    @allure.title("H5 还款流程：repay/list -> billDetails -> trial -> submit -> verify/sms -> pay result")
    @pytest.mark.parametrize("mobile_no", ["14482932217"])
    def test_repay_submit_verify_flow(self, env, mobile_no):
        with allure.step("执行完整还款流程"):
            flow_res = self._run_repay_submit_verify_flow(env, mobile_no)
            allure.attach(
                json.dumps(flow_res, ensure_ascii=False, indent=2),
                name="还款流程响应",
                attachment_type=allure.attachment_type.JSON,
            )


if __name__ == '__main__':
    runner = TestH5RepayFlow()
    print(runner._run_repay_submit_verify_flow("BM_SIT", "14482932217"))
