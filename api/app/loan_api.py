#!/usr/bin/env python
# -*- coding: UTF-8 -*-


class Loan:
    """
    授信流程类，封装了授信流程的各个步骤接口。
    """

    def __init__(self, credit):
        self.meta = credit.meta
        self.api_root_url = credit.api_root_url
        self.client = credit.client
        self.product_code = credit.product_code
        print(f"self.meta::{self.meta}")

    def _post_data(self, url, data):
        """
        提交数据
        :param data:
        :return:
        """
        json_data = {
            "meta": self.meta,
            "data": data
        }
        return self.client.post(url, json=json_data)

    def available_list(self):
        """
        查询可借列表
        Returns:

        """
        url = "/loan/v1/available/list"
        data = {}
        return self._post_data(url, data)

    def biz_mode(self, fund_code, biz_type='DRAW', loan_no=None, db_no=None):
        """
        借款模式查询
        biz_type:发起场景：DRAW:借款，DB_DRAW_PROCESSING：放款中, REPAY：还款，PRIVILEGE_REPAY：权益还款，SETTLE：提前结清
        loanNo:还款、提前结清必传
        tranProcDbNo:放款中必传
        Returns:{
            'fundCode': 'xiaoyingyidaipro',
            'fundName': '小赢易贷pro',
            'fundLogo': 'https://upload.xurongwl.com/product/logos/xiaoying_r54BlsB.png',
            'applyNo': 'CR0658730121821364225',
            'availableAmt': '2000.00',
            'terms': '6,12',
            'dateEnd': '2023-10-27 15:53',
            'phoneNumber': '123****1774',
            'loanMode': 'API',
            'redirectUrl': None,
            'iosUrl': None,
            'androidUrl': None
            }
        """
        url = "/common/v1/biz/mode"
        data = {
            "fundCode":     fund_code,
            "bizType":      biz_type,
            "loanNo":       loan_no,
            "tranProcDbNo": db_no
        }
        return self._post_data(url, data)

    def pre_query(self, fund_code, apply_no):
        url = "/draw/v1/pre/query"
        data = {
            "fundCode": fund_code,
            "applyNo":  apply_no
        }
        return self._post_data(url, data)

    def draw_submit(self, fund_code, apply_no, acct_no, cust_no, loan_amt, term,
                    purpose, purpose_code, card_id, bind_flow_no, interest_type="MONTHLY", loan_req_no=None):
        """
        查询可借列表
        Returns:

        """
        url = "/draw/v1/submit"
        data = {
            "fundCode":        fund_code,
            "loanAmt":         loan_amt,
            "loanPurpose":     purpose,
            "cardId":          card_id,
            "bindFlowNo":      bind_flow_no,
            "loanTermNum":     term,
            "applyNo":         apply_no,
            "loanPurposeCode": purpose_code,
            "acctNo":          acct_no,
            "custNo":          cust_no,
            "interestType": interest_type,
            "loanReqNo": loan_req_no
        }
        return self._post_data(url, data)

    def draw_result(self, fund_code, db_no):
        """
        借款申请结果查询
        Args:
            fund_code: 
            db_no: 

        Returns:

        """
        url = "/draw/v1/result"
        data = {
            "fundCode": fund_code,
            "tranDbNo":  db_no
        }
        return self._post_data(url, data)

    def draw_list(self):
        """
        借款列表查询
        Returns:

        """
        url = "/draw/v1/apply/list"
        data = {
        }
        return self._post_data(url, data)
