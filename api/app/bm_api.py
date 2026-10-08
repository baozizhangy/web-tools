import random, json, requests
from utils.base_request_util import BaseRequestUtil
from pytestAutoTest.data import apply_data
from utils.personal_util import get_person_name, get_id_no, get_mobile_no, generate_valid_bank_card
from utils.logger_util import web_logger
from utils.cryption_util import md5_encrypt
from datetime import datetime


class BmApi:
    def __init__(self, term=12, amt=3500, channel_id='lxj', risk_type='36', mobile=None, name=None, id_card=None,
                 env=None,
                 user_no=None, credit_apply=None):
        self.term = term
        self.amt = amt
        self.channel_id = channel_id
        if credit_apply == 'credit_reject':
            self.mobile = get_mobile_no(144)
        elif risk_type == '24':
            self.mobile = mobile or get_mobile_no(166)
        else:
            self.mobile = mobile or get_mobile_no()
        self.name = name or get_person_name()
        self.id_card = id_card or get_id_no()
        self.env = env or 'BM_SIT'
        self.user_no = user_no
        self.flow_num = random.randint(0, 9999)
        self.req_data = apply_data.ResultBase(self.mobile, self.name, self.id_card)
        self.req_api = BaseRequestUtil(channel=self.channel_id)

    def check_user(self):
        # 撞库
        web_logger.info(
            f"调用/userAccess接口::mobile::{self.mobile},name::{self.name},id_card::{self.id_card},env::{self.env},channel::{self.channel_id}")
        mobile_md5 = md5_encrypt(self.mobile)
        if self.id_card is not None:
            id_no_md5 = md5_encrypt(self.id_card)
            json_data = {
                "mobileNoMd5": mobile_md5,
                "idNoMd5": id_no_md5
            }
        else:
            json_data = {
                "mobileNoMd5": mobile_md5,
            }

        res = self.req_api.response_handle(
            self.req_api.request_handle(json_data, f"{self.channel_id}/userAccess", env=self.env))
        # print(f'撞库结果{res}')
        json_data = {"mobile": self.mobile,
                     "check_res": res}
        return json_data
        # return json_data

    def risk_white_user(self):
        json_data = {
            "mobileNo": self.mobile,
            "judgeType": 2,
            "bizConf": None,
            "status": 1,
            "type": "string"
        }
        if self.env == 'BM_SIT':
            res = requests.post("http://bm-sit.shangtoutech.com/chg/cis/test/bmPhoneWhite/addOrUpdateBmPhoneWhite",
                                json=json_data)
            return res.json()
        else:
            res = requests.post("http://bm-dev.shangtoutech.com/chg/cis/test/bmPhoneWhite/addOrUpdateBmPhoneWhite",
                                json=json_data)
            return res.json()

    def credit_apply(self):
        # 发起授信
        check_res = self.risk_white_user()
        web_logger.info(f"调用{self.env}/风控添加白名单接口::check_res::{check_res}")
        json_data = {
            "creditReqNo": 'CT' + str(random.randint(100000000000, 999999999999)) + 'TEST',
            "userNo": 'UR98532' + str(random.randint(100000000000, 999999999999)) + 'TEST',
            "fundUserNo": str(random.randint(100000000000, 999999999999)),
            "authFaceInfo": self.req_data.face_info(),
            "authIdInfo": self.req_data.id_info(),
            "contactInfo": self.req_data.contact_info(),
            "deviceInfo": self.req_data.device_info(),
            "geoInfo": self.req_data.geo_info(),
            "jobInfo": self.req_data.job_info(),
            "userBaseInfo": self.req_data.user_base_info(),
            "userProfileInfo": self.req_data.user_profile_info()
        }

        # return json.dumps(json_data)
        res = self.req_api.response_handle(
            self.req_api.request_handle(json_data, f"{self.channel_id}/creditApply", env=self.env))
        web_logger.info(f"调用{self.env}/creditApply接口::json_data::{json_data}，授信接口响应数据{res}")
        return res

    def credit_apply_result(self, credit_req_no):
        # 获取授信结果
        json_data = {
            "creditReqNo": credit_req_no
        }
        web_logger.info(f"调用{self.env}/授信结果查询接口::json_data::{json_data}")
        res = self.req_api.response_handle(
            self.req_api.request_handle(json_data, f"{self.channel_id}/creditResultQuery", env=self.env))
        return res

    def card_query(self, user_no):
        # 查询用户绑卡信息,user_no = 渠道授信申请用户suer_no
        json_data = {
            "userNo": user_no,
            "fundUserNo": "fundloan"
        }
        web_logger.info(f"调用{self.env}/查询银行卡接口::json_data::{json_data}")
        res = self.req_api.response_handle(
            self.req_api.request_handle(json_data, f"{self.channel_id}/userCardQuery", env=self.env))
        return res

    def bank_list_query(self):
        # 查询支持的银行卡列表
        json_data = {
            "bindScene": "CREDIT"
        }
        web_logger.info(f"调用{self.env}/查询支持银行卡列表::json_data::{json_data}")
        res = self.req_api.response_handle(
            self.req_api.request_handle(json_data, f"{self.channel_id}/bankListQuery", env=self.env))
        return res

    def card_bind(self, user_no, credit_req_no, bindScene='DRAW'):
        # 获取绑卡验证码/CREDIT - 授信绑卡；DRAW - 借款绑卡；REPAY - 还款换绑卡
        # if bindScene == 'REPAY' and loan_no is None:
        #     return '还款换绑卡，loan_no为必填项'
        # if bindScene == "REPAY":
        #     bank_key = 'drawReqNo'
        # credit_req_no = apply_data.get_partner_draw_no(self.env, loan_no)
        bank_key = 'creditReqNo' if bindScene == 'DRAW' else 'drawReqNo'
        json_data = {
            "bankCode": "0003",
            "bankMobile": self.mobile,
            "bankName": "工商银行",
            "bindReqNo": "BBC0947929000348372" + str(self.flow_num),
            "bindScene": bindScene,
            "cardId": "",
            "cardNo": generate_valid_bank_card('62020017'),
            # "cardNo": '620200175038573138',
            bank_key: credit_req_no,
            # "creditReqNo": credit_req_no,  # 授信申请单号
            # "drawReqNo":credit_req_no,
            "fundCode": "fundloan",
            "userNo": user_no  # 渠道授信申请用户suer_no
        }

        res = self.req_api.response_handle(
            self.req_api.request_handle(json_data, f"{self.channel_id}/cardBind", env=self.env))
        web_logger.info(f"调用{self.env}/获取绑卡验证码::json_data::{json_data},绑卡响应::res::{res}")
        return res

    def card_bind_sms(self, user_no, fund_bind_req_no):
        # 校验绑卡验证码
        json_data = {
            "bindReqNo": "BBC0947929000348372" + str(self.flow_num),  # 请求绑卡流水号
            "userNo": user_no,  # 渠道授信申请用户suer_no
            "fundBindReqNo": fund_bind_req_no,  # 获取验证码接口返回
            "smsCode": "1234",
            "fundCode": "fundloan"
        }
        res = self.req_api.response_handle(
            self.req_api.request_handle(json_data, f"{self.channel_id}/cardBindSms", env=self.env))
        web_logger.info(f"调用{self.env}/绑卡验证码校验流程,本次绑卡响应::res::{res}::json_data::{json_data}")
        return res

    def account_info(self, user_no, credit_req_no):
        # 查询用户授信额度
        json_data = {
            "creditReqNo": credit_req_no,
            "userNo": user_no
        }
        res = self.req_api.response_handle(
            self.req_api.request_handle(json_data, f'{self.channel_id}/accountInfoQuery', env=self.env))
        return res

    def agreement_list(self, user_no, credit_req_no, scene='DRAW'):
        # 查询用户协议列表REGISTER-注册、CREDIT-授信、DRAW-借款、BIND-绑卡、LOAN-借据详情、REPAY-还款、PRIVILEGE-权益
        # 默认获取借款协议，如果更换了协议类型，需要更换json参数
        # 参数较多，处理时考虑使用apply_data生成数据，生成时考虑测试场景
        json_data = {
            "creditReqNo": credit_req_no,
            "fundCode": "fundloan",
            "scene": scene,
            "userNo": user_no
        }
        res = self.req_api.response_handle(
            self.req_api.request_handle(json_data, f'{self.channel_id}/agreementList', env=self.env))
        return res

    def draw_trial(self, credit_req_no, fund_credit_no, profit='N'):
        # 试算,
        # 通过hub_channel_bm_apply 获取
        json_data = {
            "creditReqNo": credit_req_no,
            "loanAmt": self.amt,
            "loanTerm": self.term,
            "fundCode": "fundloan",
            "fundCreditNo": fund_credit_no,
            "isPrivilegeTrial": profit  # 是否获取权益,默认不试算
        }
        res = self.req_api.response_handle(
            self.req_api.request_handle(json_data, f'{self.channel_id}/drawTrial', env=self.env))
        web_logger.info(f"调用{self.env}/试算接口::试算返回{res},json_data::{json_data}")
        return res

    def draw_submit(self, user_no, credit_req_no, card_no, profit='N', profit_type=None):
        # 借款提交，参数比较多，处理时考虑使用apply_data生成数据，生成时考虑测试场景
        json_data = {"authFaceInfo": {},
                     "cardInfo": {  # 通过银行卡查询接口获取信息
                         "bankCode": "0003",
                         "bankMobile": self.mobile,
                         "bankName": "工商银行",
                         "cardNo": card_no
                     },
                     "deviceInfo": self.req_data.device_info(),
                     "drawApplyInfo": {
                         "drawApplyTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                         "interestMethod": 2,
                         "loanAmt": self.amt,
                         "loanPurpose": "01",
                         "loanTerm": self.term,
                         "repayMethod": 2
                     },
                     "geoInfo": self.req_data.job_info(),
                     "drawReqNo": "CR0716595246214" + str(self.flow_num),
                     "creditReqNo": credit_req_no,
                     "userNo": user_no,
                     "fundUserNo": "",
                     "isPrivilegeProcess": profit,
                     "privilegeConfigUid": profit_type,
                     "fundCode": "fundloan",
                     }

        res = self.req_api.response_handle(
            self.req_api.request_handle(json_data, f'{self.channel_id}/drawSubmit', env=self.env))
        return res

    def send_sms_code(self, user_no, biz_no, scene):
        # 发送二次校验验证码 scene = 01 - 借款提交验证短信；02 - 还款提交验证短信；
        # 01时biz_no = hub_channel_bm_draw.partner_draw_no,在数据库内获取
        json_data = {
            "userNo": user_no,
            "scene": scene,
            "bizNo": biz_no,
            "fundCode": "fundloan"
        }
        res = self.req_api.response_handle(
            self.req_api.request_handle(json_data, f'{self.channel_id}/sendSmsCode', env=self.env))
        return res

    def send_sms(self, user_no, scene, sms_code, biz_no):
        # 二次验证码校验 scene = 01 - 借款提交验证短信；02 - 还款提交验证短信；
        # 01时biz_no = hub_channel_bm_draw.partner_draw_no,在数据库内获取
        json_data = {
            "userNo": user_no,
            "scene": scene,
            "bizNo": biz_no,
            "smsCode": sms_code
        }
        res = self.req_api.response_handle(
            self.req_api.request_handle(json_data, f'{self.channel_id}/sendSms', env=self.env))
        return res

    def draw_step_query(self, biz_no, credit_req_no):
        # 验证后，待确认是否还需要再次验证
        json_data = {
            "drawReqNo": biz_no,
            "creditReqNo": credit_req_no,
            "fundCode": "fundloan"
        }
        res = self.req_api.response_handle(
            self.req_api.request_handle(json_data, f'{self.channel_id}/drawStepQuery', env=self.env))
        return res

    def draw_result_query(self, biz_no, credit_req_no):
        # 放款结果查询
        json_data = {
            "drawReqNo": biz_no,
            "creditReqNo": credit_req_no
        }

        res = self.req_api.response_handle(
            self.req_api.request_handle(json_data, f'{self.channel_id}/drawResultQuery', env=self.env))
        return res

    def loan_play_query(self, biz_no, fund_draw_no):
        # 查询借据及还款计划

        json_data = {
            "drawReqNo": biz_no,
            "fundDrawNo": fund_draw_no,
            "fundCode": "fundloan"
        }
        res = self.req_api.response_handle(
            self.req_api.request_handle(json_data, f'{self.channel_id}/loanPlanQuery', env=self.env))
        return res

    def profit_status_query(self):
        # 查询权益结果和当前状态
        json_data = {
            "drawReqNo": "CR0716595246214803456",
            "fundDrawNo": "FCR0716595246214803456"
        }

        res = self.req_api.response_handle(
            self.req_api.request_handle(json_data, f'{self.channel_id}/privilegePlanQuery', env=self.env))

        return res

    def repay_trial(self, user_no, biz_no, fund_draw_no, trial_type, periods):
        # 还款试算,
        # trialType 1 - 当期还款（必须按顺序，不能跳期）2 - 逾期还款（单期） 3 - 逾期还款（多期合并） 4 - 整笔提前结清
        # biz_no,fund_draw_no, -- 取值表：hub.hub_channel_bm_draw
        json_data = {
            "userNo": user_no,
            "drawReqNo": biz_no,
            "fundDrawNo": fund_draw_no,
            "trialType": trial_type,
            "trialPeriods": periods
        }

        res = self.req_api.response_handle(
            self.req_api.request_handle(json_data, f'{self.channel_id}/repayTrial', env=self.env))

        return res

    def repay_submit(self, biz_no, repay_type, repay_amt, card_no, mobile, repay_no, periods):
        # 还款提交  repayType 映射关系与试算一致
        # 还款提交hub_bm_repay_apply.partner_repay_no
        json_data = {
            "repayReqNo": repay_no,
            "drawReqNo": biz_no,
            "fundDrawNo": "FD712983712" + str(self.flow_num),
            "repayType": repay_type,
            "repayApplyTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "repayApplyAmt": repay_amt,
            "cardNo": card_no,
            "bankMobile": mobile,
            "periods": periods
        }
        res = self.req_api.response_handle(
            self.req_api.request_handle(json_data, f'{self.channel_id}/repaySubmit', env=self.env))

        return res

    def repay_result_query(self, repay_req_no, fund_repay_no=None):
        # 还款结果查询
        json_data = {
            "repayReqNo": "RR182093812093864",
            "fundRepayNo": "FRP81902380192381"
        }
        res = self.req_api.response_handle(
            self.req_api.request_handle(json_data, f'{self.channel_id}/repayResultQuery', env=self.env))

        return res

    # 权益相关
    def privilege_status(self):
        # 查询权益结果和当前状态
        json_data = {
            "userNo": self.user_no
        }
        res = self.req_api.response_handle(
            self.req_api.request_handle(json_data, f'{self.channel_id}/privilegeStatus', env=self.env))
        return res

    def privilege_exposure(self, draw_req_no):
        # 查询权益 exposure
        json_data = {
            "userNo": self.user_no,
            "drawReqNo": draw_req_no,
            "fundCode": "fundloan"
        }
        res = self.req_api.response_handle(
            self.req_api.request_handle(json_data, f'{self.channel_id}/privilegeExposure', env=self.env))
        return res

    def privilege_info(self):
        json_data = {
            "userNo": self.user_no,
            "scene": "loan_submit"
        }
        resource = self.req_api.response_handle(
            self.req_api.request_handle(json_data, f'{self.channel_id}/privilegeInfo', env=self.env))
        return resource

    def bill_privilege_info(self):
        json_data = {
            "userNo": self.user_no
        }
        res = self.req_api.response_handle(
            self.req_api.request_handle(json_data, f'{self.channel_id}/billPrivilegeInfo', env=self.env))
        return res

    def fund_loan_notice(self):
        json_data = {
            "requestNo": "test_1234" + str(self.flow_num),
            "creditReqNo": "CT901270288865TEST",
            "userNo": "UR98532135676827873TEST",
            "fundUserNo": "UR1072139389251018752",
            "fundLoanInfo": {
                "loanAmt": 3000.00,
                "loanTerm": 3,
                "bankCardNo": "620302175739897001",
                "loanSuccTime": "2024-12-15 13:39:41"
            }
        }
        res = self.req_api.response_handle(
            self.req_api.request_handle(json_data, f'{self.channel_id}/fundLoanNotice', env=self.env))

        return res


if __name__ == '__main__':
    bm_api = BmApi(mobile='15605786856', name='朱镨', channel_id='lxj', id_card='513029199609289243', env='BM_SIT',
                   user_no='UR98532646364720619TEST')
    print(bm_api.privilege_exposure('LFN1191578430468063232'))
    # print(bm_api.privilege_info())
    # print(bm_api.privilege_status())
    # print(bm_api.check_user())
    # print(bm_api.risk_white_user())
    # print(bm_api.credit_apply())
    # print(bm_api.credit_apply_result('CT262193370382TEST'))
    # print(bm_api.card_query('UR98532533998021465TEST'))
    print(bm_api.card_bind('UR98532945524913388TEST', 'CR07165952462142829', 'REPAY'))
    # print(bm_api.card_bind_sms('UR98532945524913388TEST', 'BCR1007276847035260928'))
    # print(bm_api.account_info('UR98532272416657945TEST', 'CT314997747149TEST'))
    # print(bm_api.agreement_list('UR98532790162168433TEST', 'CT285508642807TEST', 'BIND'))
    # print(bm_api.draw_trial('CT314997747149TEST', 'BM957945124799660032', 'N'))
    # print(bm_api.draw_submit('UR98532272416657945TEST', 'CT314997747149TEST', '620200179858713386','N'))
    # print(bm_api.send_sms_code('UR98532272416657945TEST', 'CR07165952462147917', '01'))
    # print(bm_api.send_sms('UR98532272416657945TEST', '01', '8991', 'CR07165952462147917'))
    # print(bm_api.draw_step_query('CR07165952462147917', 'CT314997747149TEST')) #  一直DR待放款时，需要手动执行一下LCS的补偿任务
    # print(bm_api.draw_result_query('CR07165952462147917', 'CT314997747149TEST'))
    # print(bm_api.loan_play_query('CR07165952462147917', 'CT314997747149TEST'))
    # print(bm_api.repay_trial('UR98532257688418423TEST', 'CR07165952462144728', 'BMD958548472074616832', 4, [2,3,4,5,6,7,8,9,10,11,12]))
    # print(bm_api.repay_submit('CR07165952462144728','4'))
    # print(bm_api.send_sms_code('UR98532257688418423TEST', 'RR1820938120932908', '02'))
    # print(bm_api.send_sms('UR98532257688418423TEST', '02', '6904', 'RR1820938120932908'))
    # print(bm_api.repay_result_query('RR1820938120932908','BMR961854325582221312'))
    # print(bm_api.fund_loan_notice())
