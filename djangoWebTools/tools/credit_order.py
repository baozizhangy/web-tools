import requests, random, json
# from api.app.user_api import UserApi
from jsonpath_ng import parse
from config import get_urls, db_conn
from utils.personal_util import generate_valid_bank_card
from utils.logger_util import web_logger


class CreditOrder:
    def __init__(self, mobile, amt=1000, term=12, env='BM_SIT'):
        self.env = env
        self.mobile = mobile
        self.amt = amt
        self.term = term
        self.order_url = get_urls('SIT').get('CLG_PATH')
        self.session = requests.session()
        self.bank_sms_result = None
        self.flow_num = random.randint(0, 9999)
        self.get_token()

    def get_user_info(self):
        user_info = []
        user_sql = (f"select l.cust_no,l.user_no,l.acct_no,l.appl_no from lps.ap_fund_appl l join cis.u_user c on "
                    f"l.mobile_no = c.mobile_no where c.mobile_no_md5=md5({self.mobile}) and l.apply_state = 'APS'and fund_code = 'fundloan';")
        user_info_1 = db_conn("SIT").select_one(user_sql.format(self.mobile))
        web_logger.info(f"查询倒流用户信息手机号:{self.mobile},查询结果：{user_info_1}")
        try:
            user_info.append(parse("$.data.cust_no").find(user_info_1)[0].value)
            user_info.append(parse("$.data.user_no").find(user_info_1)[0].value)
            user_info.append(parse("$.data.acct_no").find(user_info_1)[0].value)
            user_info.append(parse("$.data.appl_no").find(user_info_1)[0].value)
        except IndexError:
            # 查询不到用户信息，抛出fail，用于后续的判断
            return "fail"
        return user_info

    def get_bm_user_info(self):
        bm_info = []
        info_sql = f"SELECT user_no,cust_no from cis.u_user u WHERE u.mobile_no_md5 = MD5('{self.mobile}');"
        bm_info_1 = db_conn(self.env).select_one(info_sql)
        web_logger.info(f"查询助贷用户信息手机号:{self.mobile},查询结果：{bm_info_1}")
        try:
            bm_info.append(parse("$.data.user_no").find(bm_info_1)[0].value)
            bm_info.append(parse("$.data.cust_no").find(bm_info_1)[0].value)
        except IndexError:
            web_logger.info(f"查询助贷用户信息手机号:{self.mobile},查询结果：{bm_info_1}")
            # 查询不到助贷用户信息，抛出fail，用于后续的判断
            return "fail"
        return bm_info

    # def get_token(self):
    #     # 登录成功后，session用于请求其他接口
    #     user = UserApi('SIT', self.mobile, 'Loan_app')
    #     if user.send_code(self.mobile):
    #         try:
    #             web_logger.info('开始获取登录验证码')
    #             sms_code = parse("$.data.code").find(user.get_code(self.mobile).json())[0].value
    #         except IndexError:
    #             return "获取验证码失败"
    #         print(f'验证码获取成功{sms_code}')
    #         if sms_code is not None:
    #             if user.login_code(self.mobile, sms_code):
    #                 # 把user方法登录成功状态保存到初始化的session中
    #                 print(f'重新登录用户成功')
    #                 self.session = user.session
    #         else:
    #             return "登录失败"

    def _post(self, path, json=None, data=None):
        response = self.session.post(self.order_url + path, json=json, data=data).json()
        web_logger.info(f"本次请求的接口==={path},请求参数======={json},接口相应结果======{response}")
        return response

    def get_mode_info(self, loan_no=None):

        json_data = {
            "data": {
                "bizType": "DRAW",
                "fundCode": "fundloan",
                "loanNo": loan_no
            },
            "meta": {
                "version": "10.1"
            }
        }
        res = self._post("/common/v1/biz/mode", json_data)
        return res

    def query_bank_card(self, apply_no=None):
        # 获取用户已经绑定的银行卡
        json_data = {
            "data": {
                "applyReqNo": apply_no,
                "fundCode": "fundloan",
                "nodeType": "credit"
            },
            "meta": {
                "version": "10.1"
            }
        }
        res = self._post("/pilot/bind/queryUsableBankCard", json_data)
        return res

    def verify_bank_card(self):
        user_info = self.get_user_info()
        try:
            card_info = self.query_bank_card(apply_no=user_info[3])['data']['cardList'][0]
        except IndexError:
            return "fail"
        # 确认选择已绑定银行卡
        json_data = {
            "data": {
                "nodeType": "credit",
                "flowNo": "",
                "fundCode": "fundloan",
                "bindFlowNo": "BBC0947929000348372" + str(self.flow_num),
                "isFourFactorBind": False,
                "bankCode": card_info['bankCode'],
                "bankName": card_info['bankName'],
                "mobileNo": card_info['mobileNo'],
                "cardNo": card_info['cardNo'],
                "cardSource": "fundCard",
                "cardId": card_info['bankCardId'],
                "applyReqNo": user_info[3],
                "bindBizNo": "BCN0947429920719380" + str(self.flow_num)
            },
            "meta": {
                "version": "10.1"
            }
        }
        res = self._post("/pilot/bind/fundBindCard", json_data)
        return res['flag']

    def verify_order(self):
        # 二次确认了默认卡以后，重新进行确认试算
        user_info = self.get_user_info()
        json_data = {
            "data": {
                "fundCode": "fundloan",
                "applyNo": user_info[3],
                "trialAmt": self.amt
            },
            "meta": {
                "version": "10.1"
            }
        }
        res = self._post("/draw/v1/pre/query", json_data)
        return res['flag']

    def get_bank_sms(self):
        if self.bank_sms_result is None:
            # bank_no = get_bank_card()
            bank_num = random.randint(0, 9)

            user_info = self.get_user_info()
            if user_info == "fail":
                return "用户激活数据查询失败"
            json_data = {
                "data": {
                    "nodeType": "credit",
                    "flowNo": "",
                    "fundCode": "fundloan",
                    "bindFlowNo": "BBC0947929000348372" + str(self.flow_num),
                    "isFourFactorBind": False,
                    "mobileNo": self.mobile,
                    "cardNo": generate_valid_bank_card('62020017'),
                    "bankName": "工商银行",
                    "bankCode": "0003",
                    "applyReqNo": user_info[3],
                    "bindBizNo": "BCN0947429920719380" + str(self.flow_num)
                },
                "meta": {
                    "version": "10.1"
                }
            }
            res = self._post("/pilot/bind/fundBindCard", json_data)
            print(f"获取验证码结果====={res},======请求参数======{json_data}")
            send_status = parse('$.data.bindStatus.code').find(res)[0].value
            if send_status == '02':
                self.bank_sms_result = res
            else:
                # 获取验证码失败，返回fail
                return "fail"
        return self.bank_sms_result

    def verify_code(self):
        bank_sms_result = self.get_bank_sms()
        user_info = self.get_user_info()
        if bank_sms_result != 'fail':
            bind_flow_no = parse('$.data.bindFlowNo').find(bank_sms_result)[0].value
            bind_biz_no = parse('$.data.bindBizNo').find(bank_sms_result)[0].value
            json_data = {
                "data": {
                    "verifyCode": "1234",
                    "bindFlowNo": bind_flow_no,
                    "bindBizNo": bind_biz_no,
                    "applyReqNo": user_info[3],
                    "fundCode": "fundloan"
                },
                "meta": {
                    "version": "10.1"
                }
            }
            res = self._post("/pilot/bind/verifyCode", json_data)
            print(f"确认绑卡的结果=========={res}")
            # 返回绑卡结果
            return res['flag']
        else:
            return "绑卡验证码发送失败"

    def order_trial(self):
        user_info = self.get_user_info()
        json_data = {
            "data": {
                "fundCode": "fundloan",
                "trialAmt": self.amt,
                "term": self.term,
                "interestType": "MONTHLY",
                "acctNo": user_info[2],
                "applyNo": user_info[3],
                "custNo": user_info[1],
                "hasServiceFee": "Y"
            },
            "meta": {
                "version": "10.0.1"
            }
        }
        res = self._post("/draw/v1/trial", json_data)
        return res

    def query_contract(self, apply):
        # 查询合同，借款时必须先查询合同
        json_data = {
            "data": {
                "agreementScene": "01",
                "loanBizReq": {
                    "applyNo": apply
                }
            },
            "meta": {
                "version": "10.0.1"
            }
        }
        self._post("/fund-agreement/queryAgreement", json_data)
        return 'pass'

    def get_order_sms(self):
        json_data = {
            "data": {
                "bizScreen": "DRAW",
                "bizType": "SMS",
                "fundCode": "fundloan"
            },
            "meta": {
                "version": "10.1"
            }
        }
        res = self._post("/common/v1/bizcof", json_data)
        # 借款二次校验,获取验证码
        return res['flag']

    def verify_order_code(self):
        bm_user = self.get_bm_user_info()
        sms_code_sql = f"select params from cns.p_notice_record where user_no = '{bm_user[0]}' and event_code = 'e_draw_identity_verify_code' order by send_time desc limit 1;"
        a = db_conn(self.env).select_one(sms_code_sql)
        web_logger.info(f"查询短信验证码的sql结果======{a}，执行的环境：{self.env}，执行的sql{sms_code_sql}")
        # sql查询的结果包含字符串，先将字符串转为json，在json取值，获取验证码
        sms_code = parse('$.params.code').find(json.loads(a['data']['params']))[0].value
        user_info = self.get_user_info()
        # 借款二次校验，校验验证码
        json_data = {
            "data": {
                "fundCode": "fundloan",
                "loanReqNo": "",
                "smsCode": sms_code,
                "applyNo": user_info[3],
                "repayTerm": self.term,
                "bizType": "draw",
                "serialNumber": ""
            },
            "meta": {
                "version": "10.1"
            }
        }
        res = self._post("/common/v1/verifyCode", json_data)
        return res

    #
    # def order_submit(self):
    #     if self.verify_code() == 'S':
    #         # 如果绑卡成功，主动请求一次试算
    #         self.order_trial()
    #         user_info = self.get_user_info()
    #         # 试算成功后获取一遍最新合同
    #         self.query_contract(user_info[3])
    #         bm_user_info = self.get_bm_user_info()
    #         bank_sms_result = self.get_bank_sms()
    #         bind_flow_no = parse('$.data.bindFlowNo').find(bank_sms_result)[0].value
    #         # 查询用户银行卡card_id
    #         bank_info = f"SELECT * from cis.bm_default_bankcard t where t.cust_no = '{bm_user_info[1]}';"
    #         card = db_conn(self.env).select_one(bank_info)
    #         print(f"env==={self.env},sql===={bank_info},res ==={card}")
    #         card_id = card['data']['card_id']
    #         # bind_biz_no = parse('$.data.bindBizNo').find(bank_sms_result)[0].value
    #         json_data = {
    #             "data": {
    #                 "applyNo": user_info[3],
    #                 "bindFlowNo": bind_flow_no,
    #                 "cardId": card_id,
    #                 "fundCode": "fundloan",
    #                 "interestType": "MONTHLY",
    #                 "loanAmt": self.amt,
    #                 "loanPurpose": "购物",
    #                 "loanPurposeCode": "01",
    #                 "loanTermNum": self.term,
    #                 "acctNo": user_info[2],
    #                 "custNo": user_info[0],
    #                 "loanReqNo": "",
    #                 "drawScreenType": "CONTRACT_CONFIRM",
    #                 "selectPrivilege": False,
    #                 "privilegeConfigUid": "20004"
    #             },
    #             "meta": {
    #                 "version": "10.0.1"
    #             }
    #         }
    #         res = self._post("/draw/v1/submit", json_data)
    #         # print(f"确认下单结果====={res}")
    #         return res['flag']
    def order_submit(self):
        user_info = self.get_user_info()
        bm_user_info = self.get_bm_user_info()
        if self.get_mode_info()['flag'] == 'S':
            # 先请求一遍试算
            self.order_trial()
            # 再获取绑卡列表,如果用户有已绑卡数据，那么直接确认使用默认卡。
            bank_info = self.verify_bank_card()
            if bank_info == 'fail':
                return "用户没有绑定卡，需要先走绑卡流程"
            elif bank_info == 'S':
                if self.verify_order() == 'S':
                    # 试算成功后获取一遍最新合同
                    self.query_contract(user_info[3])
                    # 重新获取合同后，直接确认借款
                    bank_sms_result = self.get_bank_sms()
                    bind_flow_no = parse('$.data.bindFlowNo').find(bank_sms_result)[0].value
                    # 查询用户银行卡card_id
                    bank_info = f"SELECT * from cis.bm_default_bankcard t where t.cust_no = '{bm_user_info[1]}';"
                    card = db_conn(self.env).select_one(bank_info)
                    print(f"env==={self.env},sql===={bank_info},res ==={card}")
                    card_id = card['data']['card_id']
                    json_data = {
                        "data": {
                            "applyNo": user_info[3],
                            "bindFlowNo": bind_flow_no,
                            "cardId": card_id,
                            "fundCode": "fundloan",
                            "interestType": "MONTHLY",
                            "loanAmt": self.amt,
                            "loanPurpose": "购物",
                            "loanPurposeCode": "01",
                            "loanTermNum": self.term,
                            "acctNo": user_info[2],
                            "custNo": user_info[0],
                            "loanReqNo": "",
                            "drawScreenType": "CONTRACT_CONFIRM",
                            "selectPrivilege": False,
                            "privilegeConfigUid": "20004"
                        },
                        "meta": {
                            "version": "10.0.1"
                        }
                    }
                    res = self._post("/draw/v1/submit", json_data)
                    # print(f"确认下单结果====={res}")
                    return res['flag']
        else:
            return "用户没有绑定卡，需要先走绑卡流程"

    def credit_loan(self):
        if self.order_submit() == 'S':
            if self.get_order_sms() == 'S':
                if self.verify_order_code()['flag'] == 'S':
                    return "确认借款成功"
                else:
                    return "确认借款失败"
            return "发送确认借款验证码失败"
        else:
            return "确认借款失败"


if __name__ == '__main__':
    A = CreditOrder('13112340008', amt=2200)
    # print(A.get_mode_info())
    # print(A.get_user_info())
    # print(A.get_bank_sms())
    # print(A.order_submit())
    # print(A.verify_code())
    print(A.credit_loan())
