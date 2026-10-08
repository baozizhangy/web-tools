import json
from typing import Any, Optional

from config import db_conn, h5_get_env_url
from utils.base_request_util import CommonRequest
from utils.logger_util import web_logger
from utils.personal_util import generate_valid_bank_card

from api.app.h5_login import H5Login


class H5Api:
    """H5 接口封装类，内部组合 H5Login，后续接口可继续补充到这里。"""

    def __init__(self, mobile: str, scene: Optional[str] = None, env: Optional[str] = None):
        """
        兼容原有调用方式：H5Api(mobile, scene, env)
        同时也支持关键字方式：H5Api(mobile=..., env=..., scene=...)
        """
        self.env = env
        self.mobile = mobile
        self.scene = scene
        self.client = H5Login(env=self.env, mobile_no=mobile)

    def login(self):
        return self.client.login()

    def post(self, path: str, data: Optional[Any] = None, **kwargs):
        return self.client.post(path, data=data, **kwargs)

    def get(self, path: str, params: Optional[Any] = None, **kwargs):
        return self.client.get(path, params=params, **kwargs)

    def _get_user_no(self):
        """
        通过手机号获取信息，用于接口请求，查询为空时返回None
        """
        sql = (
            "select partner_user_no, partner_channel_apply_no, apply_no from hub.hub_channel_bm_apply where user_no ="
            f" (select user_no from cis.u_user where mobile_no_md5 = md5('{self.mobile}'));"
        )
        result = db_conn(self.env).select_one(sql)['data']
        return result

    def _get_apply_no(self):
        """通过手机号获取 apply_no，供 tests 层串流程时复用。"""
        user_info = self._get_user_no()
        assert user_info is not None, f"未查询到用户信息, mobile={self.mobile}"
        apply_no = user_info.get("apply_no")
        assert apply_no, f"未查询到 apply_no, mobile={self.mobile}"
        return apply_no

    def build_bank_submit_data(
            self,
            bind_scene: str = "DRAW",
            card_no: Optional[str] = None,
            bank_code: str = "0003",
            bank_name: str = "工商银行",
            mobile_no: Optional[str] = None,
            apply_no: Optional[str] = None,
            loan_req_no: Optional[str] = None,
    ) -> dict:
        """
        生成绑卡提交请求参数。
        供 tests 层联调时复用，避免把前置依赖写进 bank_verification。
        """
        payload = {
            "cardNo": card_no or generate_valid_bank_card('62020017'),
            "bankCode": bank_code,
            "bankName": bank_name,
            "mobileNo": mobile_no or self.mobile,
            "applyNo": apply_no or self._get_apply_no(),
            "bindScene": bind_scene,
        }
        if loan_req_no:
            payload["loanReqNo"] = loan_req_no
        return payload

    def build_draw_pre_query_data(self, apply_no: Optional[str] = None) -> dict:
        """生成借款基础信息查询请求参数。"""
        return {
            "applyNo": apply_no or self._get_apply_no(),
        }

    def extract_loan_flow_no(self, pre_query_response: dict) -> str:
        """从借款基础信息查询响应中提取 loanFlowNo。"""
        assert pre_query_response is not None, "pre/query 响应不能为空"
        assert isinstance(pre_query_response, dict), "pre/query 响应应该是字典类型"
        assert 'data' in pre_query_response, "pre/query 响应缺少 data 字段"
        assert 'loanFlowNo' in pre_query_response['data'], "pre/query 响应缺少 data.loanFlowNo 字段"

        loan_flow_no = pre_query_response['data']['loanFlowNo']
        assert loan_flow_no is not None and str(loan_flow_no).strip() != "", "loanFlowNo 不能为空"
        return str(loan_flow_no)

    def prepare_draw_context(self, apply_no: Optional[str] = None) -> dict:
        """
        准备借款场景上下文。
        一个借款场景只调用一次 pre/query，统一获取并复用 loanFlowNo。
        """
        request_data = self.build_draw_pre_query_data(apply_no=apply_no)
        pre_query_response = self.draw_pre_query(data=request_data)
        loan_flow_no = self.extract_loan_flow_no(pre_query_response)
        return {
            "applyNo": request_data['applyNo'],
            "loanFlowNo": loan_flow_no,
            "preQueryResponse": pre_query_response,
        }

    def build_draw_trial_data(
            self,
            trial_amt: Any = "3000",
            term: int = 12,
            apply_no: Optional[str] = None,
            loan_flow_no: Optional[str] = None,
    ) -> dict:
        """生成借款试算请求参数。"""
        return {
            "trialAmt": str(trial_amt),
            "term": term,
            "applyNo": apply_no or self._get_apply_no(),
            "loanFlowNo": loan_flow_no or "",
        }

    def build_draw_submit_data(
            self,
            card_id: str,
            loan_amt: Any = "3000",
            loan_term: Any = "12",
            apply_no: Optional[str] = None,
            loan_flow_no: Optional[str] = None,
            loan_purpose_desc: str = "购物",
            loan_purpose_code: str = "01",
            is_privilege_process: str = "N",
            privilege_config_uid: str = "",
    ) -> dict:
        """生成借款提交请求参数。"""
        return {
            "applyNo": apply_no or self._get_apply_no(),
            "cardId": card_id,
            "loanAmt": str(loan_amt),
            "loanPurposeDesc": loan_purpose_desc,
            "loanPurposeCode": loan_purpose_code,
            "loanTerm": str(loan_term),
            "loanFlowNo": loan_flow_no or "",
            "isPrivilegeProcess": is_privilege_process,
            "privilegeConfigUid": privilege_config_uid,
        }

    def build_draw_result_data(self, apply_no: str, loan_req_no: str) -> dict:
        """生成借款结果查询请求参数。"""
        return {
            "applyNo": apply_no,
            "loanReqNo": loan_req_no,
        }

    def build_draw_supply_query_data(self, loan_req_no: str) -> dict:
        """生成借款补件查询请求参数。"""
        return {
            "loanReqNo": loan_req_no,
        }

    def build_draw_supply_submit_data(
            self,
            loan_req_no: str,
            address: str = "上海市-上海市辖区-徐汇区",
            address_detail: str = "测试工具执行单接口测试补充数据",
    ) -> dict:
        """生成借款补件提交请求参数。"""
        return {
            "loanReqNo": loan_req_no,
            "supplyInfo": {
                "profileInfo": {
                    "address": address,
                    "addressDetail": address_detail,
                }
            }
        }

    def build_repay_bill_details_data(self, loan_req_no: str, loan_no: str) -> dict:
        """生成还款详情接口请求参数。"""
        return {
            "loanReqNo": loan_req_no,
            "loanNo": loan_no,
        }

    def build_repay_trial_data(
            self,
            loan_req_no: str,
            loan_no: str,
            terms: Any,
            repay_type: str = "SINGLE",
            couponNo: str = "",
    ) -> dict:
        """生成还款试算接口请求参数。"""
        data = {
            "loanNo": loan_no,
            "loanReqNo": loan_req_no,
            "repayType": repay_type,
            "terms": str(terms),
        }
        if couponNo:
            data["couponNo"] = couponNo
        return data

    def build_repay_submit_data(
            self,
            loan_req_no: str,
            loan_no: str,
            terms: Any,
            repay_apply_amt: Any,
            card_id: Any,
            repay_type: str = "SINGLE",
            channel_source: str = "",
            pre_com_ser_fee_offline: bool = False,
            couponNo: str = "",
    ) -> dict:
        """生成还款提交请求参数。"""
        data = {
            "loanReqNo": loan_req_no,
            "loanNo": loan_no,
            "repayType": repay_type,
            "terms": terms,
            "channelSource": channel_source,
            "repayApplyAmt": str(repay_apply_amt),
            "cardId": str(card_id),
            "preComSerFeeOffline": pre_com_ser_fee_offline,
        }
        if couponNo:
            data["couponNo"] = couponNo
        return data

    def build_oak_pay_order_data(
            self,
            loan_no: str,
            terms: Any,
            total_amount: Any,
            pay_channel: str = "alipay_wap",
    ) -> dict:
        """生成 Oak 支付下单接口请求参数。"""
        return {
            "payChannel": pay_channel,
            "loanNo": loan_no,
            "terms": str(terms),
            "totalAmount": str(total_amount),
        }

    def _get_url(self):
        """根据环境获取 H5 场景 URL 请求地址。"""
        return h5_get_env_url(self.env)

    def request_url(self, scene: Optional[str] = None):
        """保留原有能力：根据手机号和 scene 获取 H5 场景 URL。"""
        current_scene = scene or self.scene
        assert current_scene, "scene 不能为空"

        common_request = CommonRequest(self._get_url())
        user_info = self._get_user_no()
        if user_info is None:
            return 'fail'

        json_data = {
            "bizData": {
                "scene": current_scene,
                "userNo": user_info['partner_user_no'],
                "creditReqNo": user_info['partner_channel_apply_no']
            },
            "channelId": "HUB_LXJ",
            "method": "bm_scene_url",
            "timestamp": 1698219054566
        }

        json_data['bizData'] = json.dumps(json_data['bizData'])
        web_logger.info(f"请求参数{json_data},请求url{self._get_url()}")
        url = json.loads(common_request.api_request('POST', json_data, 'handleRequest'))
        web_logger.info(f"本次请求的url为{url}")
        return url['data']['bizData']

    def _build_agreement_request_data(
            self,
            agreement_scene: str,
            file_format: str = "html",
            data: Optional[dict] = None,
    ) -> dict:
        request_data = dict(data or {})
        request_data.setdefault("agreementScene", agreement_scene)
        request_data.setdefault("fileFormat", file_format)

        if agreement_scene in ["DRAW", "BIND"]:
            user_info = self._get_user_no()
            assert user_info is not None, f"未查询到用户信息, mobile={self.mobile}"
            apply_no = user_info.get("apply_no")
            assert apply_no, f"未查询到 apply_no, mobile={self.mobile}"
            request_data.setdefault("bindCardBizReq", {"applyNo": apply_no})

        return request_data

    def repay_list(self, path: str = "/clg/lps/api/u/bm/repay/v1/repay/list", data: Optional[dict] = None):
        return self.post(path, data=data or {})

    def repay_bill_details(self, path: str = "/clg/lps/api/u/bm/repay/v1/billDetails", data: Optional[dict] = None):
        return self.post(path, data=data or {})

    def repay_trial(self, path: str = "/clg/lps/api/u/bm/repay/v1/trial", data: Optional[dict] = None):
        return self.post(path, data=data or {})

    def repay_submit(self, path: str = "/clg/lps/api/u/bm/repay/v1/submit", data: Optional[dict] = None):
        return self.post(path, data=data or {})

    def oak_pay_order(self, path: str = "/clg/lps/api/u/bm/repay/v1/oakPayOrder", data: Optional[dict] = None):
        return self.post(path, data=data or {})

    def repay_result(self, path: str = "/clg/lps/api/u/bm/repay/v1/result", data: Optional[dict] = None):
        return self.post(path, data=data or {})

    def draw_pre_query(self, path: str = "/clg/lps/api/u/bm/draw/v1/pre/query", data: Optional[dict] = None):
        return self.post(path, data=data or {})

    def draw_trial(self, path: str = "/clg/lps/api/u/bm/draw/v1/trial", data: Optional[dict] = None):
        return self.post(path, data=data or {})

    def draw_submit(self, path: str = "/clg/lps/api/u/bm/draw/v1/submit", data: Optional[dict] = None):
        return self.post(path, data=data or {})

    def draw_result(self, path: str = "/clg/lps/api/u/bm/draw/v1/result", data: Optional[dict] = None):
        return self.post(path, data=data or {})

    def draw_supply_query(self, path: str = "/clg/lps/api/u/bm/draw/v1/supply/query", data: Optional[dict] = None):
        return self.post(path, data=data or {})

    def draw_supply_submit(self, path: str = "/clg/lps/api/u/bm/draw/v1/supply/submit", data: Optional[dict] = None):
        return self.post(path, data=data or {})

    def quertAppAgreement(
            self,
            path: str = "/clg/lps/api/p/bm-agreement/quertAppAgreement",
            data: Optional[dict] = None,
            agreement_scene: Optional[str] = None,
            file_format: str = "html",
    ):
        current_scene = agreement_scene or (data or {}).get("agreementScene") or self.scene
        assert current_scene, "agreementScene 不能为空"

        request_data = self._build_agreement_request_data(
            agreement_scene=current_scene,
            file_format=file_format,
            data=data,
        )
        return self.post(path, data=request_data)

    def readAgreement(self, path: str = "/clg/lps/api/p/bm-agreement/readAgreement", data: Optional[dict] = None):
        return self.post(path, data=data or {})

    def downloadAgreement(self, path: str = "/clg/lps/api/p/bm-agreement/download/url", data: Optional[dict] = None):
        return self.post(path, data=data or {})

    def bank_submit(self, path: str = "/clg/lps/api/u/bm/bind/v1/bindCardSubmit", data: Optional[dict] = None):
        return self.post(path, data=data or {})

    def bank_verification(self, path: str = "/clg/lps/api/u/bm/bind/v1/bindCardVerification", data: Optional[dict] = None):
        return self.post(path, data=data or {})

    def query_user_bank_card_list(self, path: str = "/clg/lps/api/u/bm/bind/v1/queryCardList", data: Optional[dict] = None):
        return self.post(path, data=data or {})

    def query_bank_list(self, path: str = "/clg/lps/api/u/bm/bind/v1/queryBankList", data: Optional[dict] = None):
        return self.post(path, data=data or {})

    def query_card_info(self, path: str = "/clg/lps/api/u/bm/bind/v1/queryCardBinInfoByCardNo", data: Optional[dict] = None):
        return self.post(path, data=data or {})

    def query_user_default_bank_card(self, path: str = "/clg/lps/api/u/bm/bind/v1/queryDefaultCard", data: Optional[dict] = None):
        return self.post(path, data=data or {})


if __name__ == '__main__':
    A = H5Api(mobile='19125772577', scene='DRAW', env='DEV')
    print(A.request_url())
