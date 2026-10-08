import json
import datetime
import threading
from time import sleep
from typing import Any, Optional, Callable

from dateutil.relativedelta import relativedelta
from jsonpath_ng import parse

from config import db_conn
from api.app.h5_api import H5Api
from api.app.loan_bill import LoanBill
from djangoWebTools.tools.bm_tools.ask_xxl import xxl_job_trigger
from utils.personal_util import generate_valid_bank_card
from utils.logger_util import web_logger


class H5SceneService:
    """H5 场景编排服务，供测试平台或 views 层直接调用。"""

    def __init__(self, mobile: str, env: str):
        self.mobile = str(mobile)
        self.env = env
        self.h5 = H5Api(mobile=self.mobile, env=self.env)

    def login(self, scene: Optional[str] = None):
        if scene:
            self.h5.scene = scene
        return self.h5.login()

    @staticmethod
    def _to_dict(response):
        return response if isinstance(response, dict) else json.loads(response)

    @staticmethod
    def _log_step(steps: list, message: str, progress_callback: Optional[Callable[[str], None]] = None):
        web_logger.info(f"[H5_SCENE_STEP] {message}")
        steps.append(message)
        if progress_callback:
            progress_callback(message)

    @staticmethod
    def _get_repay_req_no(submit_res: dict) -> str:
        matches = parse("$.data.repayReqNo").find(submit_res)
        if not matches:
            raise AssertionError(f"还款发起失败：未找到 $.data.repayReqNo, submit响应: {submit_res}")

        repay_req_no = matches[0].value
        if repay_req_no is None or str(repay_req_no).strip() == "":
            raise AssertionError(f"还款发起失败：$.data.repayReqNo 为空, submit响应: {submit_res}")
        return str(repay_req_no)

    def _query_repay_sms_code(self) -> Optional[str]:
        sql = (
            "select params from cns.p_notice_record "
            "where user_no = (select user_no from cis.u_user "
            f"where mobile_no_md5 = md5('{self.mobile}')) "
            "and event_code = 'e_repay_identity_verify_code' "
            "order by id desc limit 1"
        )
        result = db_conn(self.env).select_one(sql)
        if not (result.get("code") == "0" and result.get("data")):
            web_logger.info(f"还款验证码未查询到，result: {result}")
            return None
        return str(parse("$.params.code").find(json.loads(result["data"]["params"]))[0].value)

    def _query_draw_sms_code(self) -> Optional[str]:
        sql = (
            "select params from cns.p_notice_record "
            "where user_no = (select user_no from cis.u_user "
            f"where mobile_no_md5 = md5('{self.mobile}')) "
            "and event_code = 'e_draw_identity_verify_code' "
            "order by id desc limit 1"
        )
        result = db_conn(self.env).select_one(sql)
        if not (result.get("code") == "0" and result.get("data")):
            web_logger.info(f"借款验证码未查询到，result: {result}")
            return None
        return str(parse("$.params.code").find(json.loads(result["data"]["params"]))[0].value)

    def _query_iou_state_by_loan_req_no(self, loan_req_no: str) -> Optional[str]:
        sql = f"select loan_state from lps.bm_iou where loan_req_no = '{loan_req_no}' order by id desc limit 1;"
        result = db_conn(self.env).select_one(sql)
        result = self._to_dict(result)
        data = result.get("data") or {}
        return data.get("loan_state")

    def _query_pay_status(self, repay_req_no: str) -> str:
        sql = f"select status from lcs.tr_tran_proc_rp where rp_request_no = '{repay_req_no}';"
        result = db_conn(self.env).select_one(sql)
        result = self._to_dict(result)

        status_matches = parse("$.data.status").find(result)
        if not status_matches:
            return ""
        return str(status_matches[0].value)

    def _query_rp_processing(self, repay_req_no: str) -> bool:
        """检查还款流水是否已在 rp 表中处于处理中状态(02)"""
        sql = f"select status from lcs.tr_tran_proc_rp where rp_request_no = '{repay_req_no}' and status = '02';"
        result = db_conn(self.env).select_one(sql)
        result = self._to_dict(result)
        return bool(result.get("data"))

    @staticmethod
    def _status_text(status: str) -> str:
        status_map = {
            "02": "交易处理中",
            "03": "交易成功",
            "04": "交易失败",
            "05": "部分成功",
        }
        return status_map.get(status, f"未知状态({status})")

    def _poll_pay_result(self, repay_req_no: str, max_rounds: int = 3) -> str:
        final_status = ""
        for _ in range(max_rounds):
            sleep(10)
            xxl_job_trigger(job_id='107', executor_param=None, env=self.env)
            final_status = self._query_pay_status(repay_req_no)
            if final_status != "02":
                return self._status_text(final_status)
        return self._status_text(final_status)

    def _init_loan_bill(self, loan_no: str, overdue_type: str = "N", day: int = 0, bill_day: bool = True):
        def _run_init():
            LoanBill(loan_no=loan_no, overdue_type=overdue_type, day=day, bill_day=bill_day, env=self.env).init_plan_1()

        threading.Thread(target=_run_init, daemon=True).start()
        return "S"

    def clean_draw_data(self):
        sql = (
            "update lps.bm_iou set loan_state = 'DJ' "
            "where user_no = (select user_no from cis.u_user "
            f"where mobile_no_md5 = md5('{self.mobile}')) and loan_state != 'DS';"
        )
        return db_conn(self.env).select_one(sql)

    def _query_latest_ds_loan_req_no(self) -> Optional[str]:
        sql = (
            "select loan_req_no from lps.bm_iou "
            "where user_no = (select user_no from cis.u_user "
            f"where mobile_no_md5 = md5('{self.mobile}')) "
            "and loan_state = 'DS' order by id desc limit 1;"
        )
        result = self._to_dict(db_conn(self.env).select_one(sql))
        if result.get("code") != "0" or not result.get("data"):
            return None
        loan_req_no = result["data"].get("loan_req_no")
        if not loan_req_no:
            return None
        return str(loan_req_no)

    def _query_loan_req_no_by_loan_no(self, loan_no: str) -> Optional[str]:
        sql = (
            "select loan_req_no from lps.bm_iou "
            "where user_no = (select user_no from cis.u_user "
            f"where mobile_no_md5 = md5('{self.mobile}')) "
            f"and loan_no = '{loan_no}' order by id desc limit 1;"
        )
        result = self._to_dict(db_conn(self.env).select_one(sql))
        if result.get("code") != "0" or not result.get("data"):
            return None
        loan_req_no = result["data"].get("loan_req_no")
        if not loan_req_no:
            return None
        return str(loan_req_no)

    def _get_bank_no(self, pay_channel='baofu'):
        if pay_channel in ('baofu', None, 'NONE'):
            prefix = '62020017'
            while True:
                bank_no = generate_valid_bank_card(prefix)
                if int(str(bank_no)[-1]) % 2 == 0:
                    return bank_no

        elif pay_channel == 'allinpay':
            prefix = '62020017'
            while True:
                bank_no = generate_valid_bank_card(prefix)
                if int(str(bank_no)[-1]) in (1, 9):
                    return bank_no

        elif pay_channel == 'huifu':
            prefix = '622828177'
            while True:
                bank_no = generate_valid_bank_card(prefix)
                if int(str(bank_no)[-1]) % 2 == 0:
                    return bank_no

        elif pay_channel == 'all':
            prefix = '622828177'
            while True:
                bank_no = generate_valid_bank_card(prefix)
                if int(str(bank_no)[-1]) in (1, 9):
                    return bank_no

        return generate_valid_bank_card('62020017')

    def run_repay_submit_scene(self, max_rounds: int = 3):
        """还款提交完整场景：list -> billDetails -> trial -> submit -> verify/sms -> pay result"""
        self.login(scene='REPAY')

        repay_list_res = self._to_dict(self.h5.repay_list(data={}))
        loan_req_no = str(parse("$.data.repayList[0].loanReqNo").find(repay_list_res)[0].value)
        loan_no = str(parse("$.data.repayList[0].loanNo").find(repay_list_res)[0].value)

        bill_details_data = self.h5.build_repay_bill_details_data(loan_req_no=loan_req_no, loan_no=loan_no)
        bill_details_res = self._to_dict(self.h5.repay_bill_details(data=bill_details_data))
        terms = parse("$.data.repayDetails[0].term").find(bill_details_res)[0].value

        trial_data = self.h5.build_repay_trial_data(
            loan_req_no=loan_req_no,
            loan_no=loan_no,
            terms=terms,
        )
        trial_res = self._to_dict(self.h5.repay_trial(data=trial_data))
        repay_apply_amt = parse("$.data.totalAmount").find(trial_res)[0].value
        card_id = parse("$.data.cardInfo.cardId").find(trial_res)[0].value

        submit_data = self.h5.build_repay_submit_data(
            loan_req_no=loan_req_no,
            loan_no=loan_no,
            terms=terms,
            repay_apply_amt=repay_apply_amt,
            card_id=card_id,
        )
        submit_res = self._to_dict(self.h5.repay_submit(data=submit_data))
        repay_req_no = self._get_repay_req_no(submit_res)

        sleep(3)
        sms_code = self._query_repay_sms_code()
        verify_res = self._to_dict(
            self.h5.post(
                "/clg/lps/api/u/bm/common/v1/verify/sms",
                data={
                    "bizNo": repay_req_no,
                    "smsCode": sms_code,
                    "scene": "02",
                    "preComSerFeeOffline": False,
                },
            )
        )

        pay_result = self._poll_pay_result(repay_req_no, max_rounds=max_rounds)
        # self._init_loan_bill(loan_no)

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
        }

    def run_repay_scene(
            self,
            loan_no: str,
            repay_type: str = "SINGLE",
            use_coupon: bool = False,
            progress_callback: Optional[Callable[[str], None]] = None,
    ):
        """还款场景：根据手机号+借据号查询 loanReqNo -> 详情 -> 试算 -> 提交 -> verify/sms -> repay_result。"""
        steps = []
        repay_type = str(repay_type).upper()
        assert repay_type in ["SINGLE", "ALL"], "repay_type 仅支持 SINGLE 或 ALL"

        self._log_step(steps, "开始登录 H5 REPAY 场景", progress_callback)
        self.login(scene='REPAY')

        self._log_step(steps, f"开始根据借据号查询 loanReqNo，loanNo={loan_no}", progress_callback)
        loan_req_no = self._query_loan_req_no_by_loan_no(loan_no)
        if not loan_req_no:
            return {
                "success": -1,
                "message": "未查询到 loanReqNo",
                "steps": steps,
                "loanNo": loan_no,
            }

        self._log_step(steps, f"查询应还详情，loanReqNo={loan_req_no}", progress_callback)
        bill_details_data = self.h5.build_repay_bill_details_data(loan_req_no=loan_req_no, loan_no=loan_no)
        bill_details_res = self._to_dict(self.h5.repay_bill_details(data=bill_details_data))
        repay_details = parse("$.data.repayDetails").find(bill_details_res)
        repay_details_value = repay_details[0].value if repay_details else []

        if not repay_details_value:
            self._log_step(steps, "应还详情为空，当前借据已结清", progress_callback)
            return {
                "success": 1,
                "message": "当前借据已结清",
                "steps": steps,
                "loanNo": loan_no,
                "loanReqNo": loan_req_no,
                "bill_details": bill_details_res,
            }

        if repay_type == "SINGLE":
            terms = parse("$.data.repayDetails[0].term").find(bill_details_res)[0].value
            self._log_step(steps, f"本次按单期还款处理，term={terms}", progress_callback)
        else:
            terms = parse("$.data.repayDetails[0].term").find(bill_details_res)[0].value
            repay_type = "ALL"
            self._log_step(steps, f"本次按提前结清处理，terms=ALL", progress_callback)

        # 优惠券处理
        coupon_no = ""
        if use_coupon:
            coupon_info = parse("$.data.couponInfo").find(bill_details_res)
            coupon_info_value = coupon_info[0].value if coupon_info else None
            if not coupon_info_value or not coupon_info_value.get("couponNo"):
                self._log_step(steps, "未查询到可用优惠券或非代偿借据，终止流程", progress_callback)
                return {
                    "success": -3,
                    "message": "没有优惠券或未代偿借据，无法使用优惠券还款",
                    "steps": steps,
                    "loanNo": loan_no,
                    "loanReqNo": loan_req_no,
                    "bill_details": bill_details_res,
                }
            coupon_no = str(coupon_info_value["couponNo"])
            self._log_step(steps, f"使用优惠券还款，couponNo={coupon_no}", progress_callback)

        self._log_step(steps, "开始还款试算", progress_callback)
        trial_data = self.h5.build_repay_trial_data(
            loan_req_no=loan_req_no,
            loan_no=loan_no,
            terms=terms,
            repay_type=repay_type,
            couponNo=coupon_no,
        )
        trial_res = self._to_dict(self.h5.repay_trial(data=trial_data))
        if str(trial_res.get("flag")) == "F":
            self._log_step(steps, "还款试算失败，流程结束", progress_callback)
            return {
                "success": -2,
                "message": "还款试算失败",
                "steps": steps,
                "loanNo": loan_no,
                "loanReqNo": loan_req_no,
                "bill_details": bill_details_res,
                "trial": trial_res,
            }

        repay_apply_amt = parse("$.data.totalAmount").find(trial_res)[0].value
        card_id = parse("$.data.cardInfo.cardId").find(trial_res)[0].value

        self._log_step(steps, "开始发起还款提交", progress_callback)
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
        repay_req_no = self._get_repay_req_no(submit_res)
        self._log_step(steps, f"还款提交完成，repayReqNo={repay_req_no}", progress_callback)

        sleep(3)
        self._log_step(steps, "开始查询还款验证码", progress_callback)
        sms_code = self._query_repay_sms_code()

        verify_res = None
        if sms_code is None:
            # 1) 先判断 RP 表是否已有处理中的流水
            if self._query_rp_processing(repay_req_no):
                self._log_step(steps, "跳过短信验证，还款已在处理中，还款发起成功", progress_callback)
            else:
                # 2) RP 表无数据，查绑卡表是否有 status=03
                bind_sql = (
                    "select bind_status from lps.bm_bind_card_req_detail "
                    "where bind_req_no in (select internal_req_no from lps.bm_bind_card_req "
                    f"where biz_no = '{loan_req_no}')"
                )
                bind_result = db_conn(self.env).select_one(bind_sql)
                bind_result = self._to_dict(bind_result)
                bind_data = bind_result.get('data') or {}
                has_bind_03 = bool(bind_data)
                if has_bind_03:
                    self._log_step(steps, "绑卡状态包含03，走绑卡流程提交验证", progress_callback)
                    verify_data = {
                        "bizNo": repay_req_no,
                        "smsCode": "111111",
                        "scene": "02",
                        "preComSerFeeOffline": False,
                    }
                    if coupon_no:
                        verify_data["couponNo"] = coupon_no
                    verify_res = self._to_dict(
                        self.h5.post("/clg/lps/api/u/bm/common/v1/verify/sms", data=verify_data)
                    )
                    self._log_step(steps, "补充短信校验完成", progress_callback)
                else:
                    return {
                        "success": -4,
                        "message": "还款发起失败：验证码为空且无绑卡数据",
                        "steps": steps,
                        "loanNo": loan_no,
                        "loanReqNo": loan_req_no,
                        "repayReqNo": repay_req_no,
                        "submit": submit_res,
                    }
        else:
            self._log_step(steps, "还款验证码查询成功，开始短信校验", progress_callback)
            verify_data = {
                "bizNo": repay_req_no,
                "smsCode": sms_code,
                "scene": "02",
                "preComSerFeeOffline": False,
            }
            if coupon_no:
                verify_data["couponNo"] = coupon_no
            verify_res = self._to_dict(
                self.h5.post("/clg/lps/api/u/bm/common/v1/verify/sms", data=verify_data)
            )
            self._log_step(steps, "还款短信校验完成", progress_callback)

        self._log_step(steps, "开始查询还款结果", progress_callback)
        repay_result_data = {
            "loanNo": loan_no,
            "loanReqNo": loan_req_no,
            "repayType": repay_type,
            "repayApplyAmt": str(repay_apply_amt),
            "terms": terms,
            "cardId": str(card_id),
            "couponNo": "",
        }
        repay_result_res = self._to_dict(self.h5.repay_result(data=repay_result_data))

        return {
            "success": 0,
            "message": "还款流程执行完成",
            "steps": steps,
            "loanNo": loan_no,
            "loanReqNo": loan_req_no,
            "repayReqNo": repay_req_no,
            "repayType": repay_type,
            "terms": terms,
            "bill_details": bill_details_res,
            "trial": trial_res,
            "submit": submit_res,
            "verify": verify_res,
            "repay_result": repay_result_res,
        }

    def run_draw_submit_scene(
            self,
            loan_amt: Any = "3000",
            loan_term: Any = "12",
            is_privilege_process: str = "N",
            is_continuous_monthly: str = "Y",
            loan_purpose_desc: str = "购物",
            loan_purpose_code: str = "01",
            progress_callback: Optional[Callable[[str], None]] = None,
    ):
        """借款提交流程场景：清洗 -> pre/query -> trial -> submit。"""
        steps = []

        loan_amt = int(loan_amt)
        loan_term = int(loan_term)
        is_privilege_process = str(is_privilege_process).upper()
        is_continuous_monthly = str(is_continuous_monthly).upper()

        assert 1000 <= loan_amt <= 10000, "amt 仅支持 1000 ~ 10000"
        assert loan_term in [3, 6, 9, 12], "term 仅支持 3, 6, 9, 12"
        assert is_privilege_process in ["N", "Y"], "is_privilege_process 仅支持 N 或 Y"
        assert is_continuous_monthly in ["N", "Y"], "is_continuous_monthly 仅支持 N 或 Y"

        self._log_step(steps, "开始清理借款数据", progress_callback)
        self.clean_draw_data()
        self._log_step(steps, "开始登录 H5 DRAW 场景", progress_callback)
        self.login(scene='DRAW')

        self._log_step(steps, "开始查询借款预处理信息", progress_callback)
        context = self.h5.prepare_draw_context()
        pre_query_res = context["preQueryResponse"]
        pre_query_data = pre_query_res.get("data") or {}

        bank_card_info = ((pre_query_data.get("accPrdInfo") or {}).get("bankCardInfo"))
        if not bank_card_info:
            self._log_step(steps, "未检测到绑卡信息，开始自动绑卡", progress_callback)
            bind_res = self.run_bind_card_scene(bind_scene="DRAW")
            if bind_res.get("success") != 0:
                return {
                    "success": -4,
                    "message": "借款前自动绑卡失败",
                    "steps": steps,
                    "bind_card": bind_res,
                }
            self._log_step(steps, "自动绑卡成功，重新查询借款信息", progress_callback)
            context = self.h5.prepare_draw_context(apply_no=context["applyNo"])
            pre_query_res = context["preQueryResponse"]
            pre_query_data = pre_query_res.get("data") or {}
            bank_card_info = ((pre_query_data.get("accPrdInfo") or {}).get("bankCardInfo"))
        else:
            self._log_step(steps, "已检测到绑卡信息", progress_callback)

        assert bank_card_info, f"借款信息查询未返回 bankCardInfo: {pre_query_res}"
        card_id = bank_card_info.get("cardId")
        assert card_id, f"借款信息查询未返回 bankCardInfo.cardId: {pre_query_res}"

        privilege_config_uid = ""
        if is_privilege_process == "Y":
            self._log_step(steps, "开始处理权益信息", progress_callback)
            member_card_info_list = ((pre_query_data.get("privilegeInfo") or {}).get("memberCardInfoList")) or []
            if member_card_info_list:
                card_subscription_info_list = member_card_info_list[0].get("cardSubscriptionInfoList") or []
                target_subscription_type = "OM" if is_continuous_monthly == "Y" else "CM"
                matched_card = next(
                    (item for item in card_subscription_info_list if
                     item.get("subscriptionType") == target_subscription_type),
                    None,
                )
                if matched_card:
                    privilege_config_uid = matched_card.get("configUid") or ""
                    assert privilege_config_uid, f"权益配置缺少 configUid: {matched_card}"
                    self._log_step(steps, f"权益匹配成功，subscriptionType={target_subscription_type}",
                                   progress_callback)
                else:
                    is_privilege_process = "N"
                    self._log_step(steps, "未找到匹配权益，自动降级为无权益借款", progress_callback)
            else:
                is_privilege_process = "N"
                self._log_step(steps, "权益列表为空，自动降级为无权益借款", progress_callback)
        else:
            self._log_step(steps, "本次按无权益借款处理", progress_callback)

        self._log_step(steps, "开始借款试算", progress_callback)
        trial_data = self.h5.build_draw_trial_data(
            trial_amt=loan_amt,
            term=loan_term,
            apply_no=context["applyNo"],
            loan_flow_no=context["loanFlowNo"],
        )
        trial_res = self._to_dict(self.h5.draw_trial(data=trial_data))

        self._log_step(steps, "开始提交借款申请", progress_callback)
        submit_data = self.h5.build_draw_submit_data(
            apply_no=context["applyNo"],
            card_id=card_id,
            loan_amt=loan_amt,
            loan_term=loan_term,
            loan_flow_no=context["loanFlowNo"],
            loan_purpose_desc=loan_purpose_desc,
            loan_purpose_code=loan_purpose_code,
            is_privilege_process=is_privilege_process,
            privilege_config_uid=privilege_config_uid,
        )
        submit_res = self._to_dict(self.h5.draw_submit(data=submit_data))
        loan_req_no = str(parse("$.data.loanReqNo").find(submit_res)[0].value)
        self._log_step(steps, f"借款提交完成，loanReqNo={loan_req_no}", progress_callback)

        sleep(3)
        self._log_step(steps, "开始查询借款验证码", progress_callback)
        sms_code = self._query_draw_sms_code()

        verify_res = None
        if sms_code is None:
            iou_state = self._query_iou_state_by_loan_req_no(loan_req_no)
            web_logger.info(f"验证码为空，查询借据状态 loanReqNo={loan_req_no}, loan_state={iou_state}")
            if iou_state == 'ACS':
                bind_sql = (
                    "select bind_status from lps.bm_bind_card_req_detail "
                    "where bind_req_no in (select internal_req_no from lps.bm_bind_card_req "
                    f"where biz_no = '{loan_req_no}')"
                )
                bind_result = db_conn(self.env).select_one(bind_sql)
                bind_result = self._to_dict(bind_result)
                bind_data = bind_result.get('data') or {}
                has_bind_03 = bool(bind_data)
                if has_bind_03:
                    self._log_step(steps, "ACS状态且绑卡状态包含03，走绑卡流程提交验证", progress_callback)
                    verify_res = self._to_dict(
                        self.h5.post(
                            "/clg/lps/api/u/bm/common/v1/verify/sms",
                            data={"bizNo": loan_req_no, "smsCode": "111111", "scene": "01"},
                        )
                    )
                    self._log_step(steps, "补充短信校验完成，发起借款成功", progress_callback)
                else:
                    self._log_step(steps, "ACS状态但绑卡状态无03，跳过平台验证码，发起借款成功", progress_callback)
            else:
                self._log_step(steps, "绑卡验证码验证有效期内，跳过平台验证码，发起借款成功", progress_callback)
        else:
            self._log_step(steps, "借款验证码查询成功，开始短信校验", progress_callback)
            verify_res = self._to_dict(
                self.h5.post(
                    "/clg/lps/api/u/bm/common/v1/verify/sms",
                    data={"bizNo": loan_req_no, "smsCode": sms_code, "scene": "01"},
                )
            )
            self._log_step(steps, "借款短信校验完成", progress_callback)

        return {
            "message": "借款申请已提交",
            "applyNo": context["applyNo"],
            "loanFlowNo": context["loanFlowNo"],
            "cardId": card_id,
            "isPrivilegeProcess": is_privilege_process,
            "privilegeConfigUid": privilege_config_uid,
            "steps": steps,
            "pre_query": pre_query_res,
            "trial": trial_res,
            "submit": submit_res,
            "verify": verify_res,
            "loanReqNo": loan_req_no,
        }

    def _query_bind_status_by_channel(self, bind_card_req_no: str, pay_channel: str):
        sql = (
            "select b.bind_status from lps.bm_bind_card_req_detail as a "
            "join lps.bm_bind_card_req_detail as b on a.bind_req_no = b.bind_req_no "
            f"where a.cert_no = '{bind_card_req_no}' and b.pay_channel = '{pay_channel}';"
        )
        return self._to_dict(db_conn(self.env).select_one(sql))

    def _query_bind_status_all_channels(self, bind_card_req_no: str):
        sql = (
            "select b.pay_channel, b.bind_status from lps.bm_bind_card_req_detail as a "
            "join lps.bm_bind_card_req_detail as b on a.bind_req_no = b.bind_req_no "
            f"where a.cert_no = '{bind_card_req_no}' order by b.sort;"
        )
        query_res = self._to_dict(db_conn(self.env).select_one(sql))
        data = query_res.get("data") or []
        if isinstance(data, dict):
            data = [data]
        return data

    def _query_pending_bind_cert_no(self, bind_card_req_no: str):
        sql = (
           f"select b.cert_no from lps.bm_bind_card_req_detail as a "
           f"join lps.bm_bind_card_req_detail as b "
           f"on a.bind_req_no = b.bind_req_no where a.cert_no = '{bind_card_req_no}'"
           f" and b.bind_status = '3';"
        )
        result = self._to_dict(db_conn(self.env).select_one(sql))
        data = result.get("data") or {}
        return data.get("cert_no")

    def run_bind_card_scene(
            self,
            bind_scene: str = "DRAW",
            card_no: Optional[str] = None,
            sms_code: str = "111111",
            pay_channel: str = "baofu",
    ):
        """??????? submit ????????????? cert_no???? verification ?????????"""
        self.login(scene=bind_scene)
        pay_channel = str(pay_channel) if pay_channel is not None else 'baofu'
        if pay_channel == 'all':
            actual_card_no = self._get_bank_no('all')
        elif pay_channel in ('allinpay', 'huifu'):
            actual_card_no = self._get_bank_no(pay_channel)
        elif card_no:
            actual_card_no = str(card_no)
        else:
            actual_card_no = self._get_bank_no(pay_channel)

        loan_req_no = None
        if bind_scene == "REPAY":
            loan_req_no = self._query_latest_ds_loan_req_no()
            if not loan_req_no:
                return {
                    "success": -3,
                    "message": "当前用户没有放款借据，无法触发还款绑卡",
                    "cardNo": actual_card_no,
                }

        card_bin_res = self._to_dict(self.h5.query_card_info(data={"cardNo": actual_card_no}))
        if card_bin_res.get("flag") != "S":
            return {
                "success": -1,
                "message": "绑卡申请签约发起异常",
                "cardNo": actual_card_no,
                "card_bin": card_bin_res,
            }

        card_bin_data = card_bin_res.get("data") or {}
        bank_code = card_bin_data.get("bankCode") or card_bin_data.get("bank_code")
        bank_name = card_bin_data.get("bankName") or card_bin_data.get("bank_name")

        submit_data = self.h5.build_bank_submit_data(
            bind_scene=bind_scene,
            card_no=actual_card_no,
            bank_code=bank_code,
            bank_name=bank_name,
            loan_req_no=loan_req_no,
        )
        submit_res = self._to_dict(self.h5.bank_submit(data=submit_data))
        print(f"??????{submit_res}")
        submit_data_res = submit_res.get("data") or {}
        if submit_data_res.get("result") not in ['3', 3]:
            return {
                "success": -2,
                "message": "签约绑卡成功",
                "cardNo": f"本次签约绑卡号为：{actual_card_no}",
                "card_bin": card_bin_res,
                "submit": submit_res,
                "bindResults": [],
            }

        bind_card_req_no = submit_data_res.get('bindCardReqNo')
        assert bind_card_req_no, f"???????? data.bindCardReqNo ??: {submit_res}"
        latest_bind_card_req_no = bind_card_req_no
        bind_results = []

        verify_res = self._to_dict(self.h5.bank_verification(data={
            "bindCardReqNo": bind_card_req_no,
            "smsCode": sms_code,
        }))
        bind_results.append({
            "round": 1,
            "bindCardReqNo": bind_card_req_no,
            "submit": submit_res,
            "verify": verify_res,
        })

        if pay_channel in ('all', 'allinpay', 'huifu'):
            round_index = 1
            while True:
                sleep(1)
                next_bind_card_req_no = self._query_pending_bind_cert_no(latest_bind_card_req_no)
                if not next_bind_card_req_no:
                    break
                round_index += 1
                latest_bind_card_req_no = next_bind_card_req_no
                next_verify_res = self._to_dict(self.h5.bank_verification(data={
                    "bindCardReqNo": next_bind_card_req_no,
                    "smsCode": sms_code,
                }))
                bind_results.append({
                    "round": round_index,
                    "bindCardReqNo": next_bind_card_req_no,
                    "submit": None,
                    "verify": next_verify_res,
                })

        sleep(2)
        card_list_res = self._to_dict(self.h5.query_user_bank_card_list())
        assert 'data' in card_list_res and 'cardList' in card_list_res['data'], f"?????????????{card_list_res}"

        if pay_channel == 'all':
            channel_statuses = self._query_bind_status_all_channels(bind_card_req_no)
            is_success = bool(channel_statuses) and all(str(item.get('bind_status')) == '1' for item in channel_statuses)
            return {
                "success": 0 if is_success else -4,
                "message": "签约绑卡成功" if is_success else "签约绑卡有失败请求",
                "payChannel": pay_channel,
                "cardNo": actual_card_no,
                "bindCardReqNo": bind_card_req_no,
                "bindResults": bind_results,
                "channelStatuses": channel_statuses,
                "cardList": card_list_res,
            }

        if pay_channel in ('allinpay', 'huifu'):
            bind_status_res = self._query_bind_status_by_channel(bind_card_req_no, pay_channel)
            bind_status = (bind_status_res.get('data') or {}).get('bind_status')
            is_success = str(bind_status) == '1'
            return {
                "success": 0 if is_success else -4,
                "message": "签约绑卡成功" if is_success else "签约绑卡有失败请求",
                "payChannel": pay_channel,
                "cardNo": actual_card_no,
                "bindCardReqNo": bind_card_req_no,
                "bindStatus": bind_status,
                "bindResults": bind_results,
                "cardList": card_list_res,
            }

        return {
            "success": 0,
            "message": "签约绑卡结果",
            "payChannel": pay_channel,
            "cardNo": f"本次签约绑卡号为：{actual_card_no}",
            "bindCardReqNo": bind_card_req_no,
            "bindResults": bind_results,
            "cardList": card_list_res,
        }
