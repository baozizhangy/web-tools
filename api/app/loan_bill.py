import requests, hashlib, datetime, time
from datetime import timedelta

from dateutil.relativedelta import relativedelta
from jsonpath_ng import parse
from djangoWebTools.tools.bm_tools.ask_xxl import xxl_job_trigger

from config import loan_api
from config import db_conn

# 初始化账单
init_plan = ["delete from lcs.ln_plan_increase t WHERE t.loan_no = '{loan_no}';",
             "delete from lcs.tr_tran_proc_rp  WHERE loan_no = '{loan_no}';",
             "delete from fund.fd_tran_proc_rp  WHERE fd_loan_no = '{fd_loan_no}';",
             "delete from lcs.tr_adjust_detail where loan_no = '{loan_no}';",
             "delete from lcs.tr_tran_proc_adjust where loan_no = '{loan_no}';",
             "delete from lcs.tr_tran_proc_adjust_prin where loan_no = '{loan_no}';",
             "delete from lcs.tr_prin_adjust_detail where loan_no = '{loan_no}';",
             "delete from lcs.ln_fee4_carry_settle_record where loan_no = '{loan_no}';",
             "delete from lcs.tr_tran_detail where loan_no = '{loan_no}' and tran_code = 'fee1Amt';",
             "delete from fund.fd_compensation_record where loan_no = '{loan_no}';",

             "UPDATE lcs.ln_plan SET date_due = DATE_ADD('{init_date}', INTERVAL(term + 1) MONTH),"
             "date_grace = DATE_ADD(DATE_ADD('{init_date}', INTERVAL (term + 1) MONTH), INTERVAL ('{free_days}') DAY),"
             "date_start = CASE WHEN term != 0 THEN DATE_ADD('{init_date}', INTERVAL term MONTH) ELSE date_start END WHERE loan_no = '{loan_no}';",

             # "UPDATE lcs.ln_plan t SET t.rpy_flag = '0', t.act_prin_amt = 0.00, t.act_int_amt = 0.00, t.act_fee3_amt = 0.00,"
             # " t.act_fee4_amt = 0.00, t.date_settle = null, t.overdue_days = 0 WHERE t.loan_no = '{loan_no}' and term != 0;",
             "update lcs.ln_plan set rpy_flag = '0', oint_amt =0,act_prin_amt = 0,deduct_amt=0,fee1_amt=0,act_deduct_amt=0,act_fee1_amt=0,"
             "act_int_amt = 0,act_oint_amt = 0,act_fee3_amt= 0,act_fee4_amt = 0,fee5_amt= 0,fee6_amt = 0,act_fee5_amt= 0 ,act_fee6_amt = 0,date_settle = null,"
             "overdue_days = 0,compensated_type = 0,int_amt = prin_amt * 0.08 where loan_no = '{loan_no}'  and term != 0;",

             "update lcs.ln_plan as l join lcs.ln_plan as p on l.loan_no = p.loan_no and p.term = 1 "
             "set l.int_amt  = l.prin_amt * 0.08,l.fee3_amt = p.fee3_amt, l.fee4_amt=p.fee4_amt "
             "where l.loan_no = '{loan_no}' and l.term != 0;",
             # 线下还款记录
             "delete from lcs.bm_offline_repay_batch where loan_no = '{loan_no}';",
             "delete from lcs.bm_offline_repay_record where loan_no = '{loan_no}';",
             "delete from lcs.bm_fee_trans_record where loan_no = '{loan_no}';",
             "delete  from lcs.`tr_online_repay_proc` where loan_no = '{loan_no}';",
             "delete from cos.vip_loan_order where loan_no = '{loan_no}';",

             "UPDATE lcs.ln_plan_snapshot SET date_due = DATE_ADD('{init_date}', INTERVAL(term + 1) MONTH),"
             "date_grace = DATE_ADD(DATE_ADD('{init_date}', INTERVAL (term + 1) MONTH), INTERVAL ('{free_days}') DAY),"
             "date_start = CASE WHEN term != 0 THEN DATE_ADD('{init_date}', INTERVAL term MONTH) ELSE date_start END WHERE loan_no = '{loan_no}';",

             "UPDATE fund.fd_plan SET date_due = DATE_ADD('{init_date}', INTERVAL(term + 1) MONTH), "
             "date_start = CASE WHEN term != 0 THEN DATE_ADD('{init_date}', INTERVAL term MONTH) ELSE date_start END WHERE fd_loan_no = '{fd_loan_no}';",

             "UPDATE fund.fd_plan_snapshot SET date_due = DATE_ADD('{init_date}', INTERVAL(term + 1) MONTH),"
             " date_start = CASE WHEN term != 0 THEN DATE_ADD('{init_date}', INTERVAL term MONTH) ELSE date_start END WHERE fd_loan_no = '{fd_loan_no}';",

             "update fund.fd_plan set rpy_flag = '0',fee3_amt=0,fee4_amt = 0,act_prin_amt = 0,"
             "act_int_amt = 0,act_oint_amt = 0,act_fee3_amt= 0,act_fee4_amt = 0,date_settle = null,"
             "overdue_days = 0,compensated_type = 0,int_amt = prin_amt * 0.08 where fd_loan_no = '{fd_loan_no}'  and term != 0;",

             "UPDATE lcs.ln_loan t SET t.date_loan = STR_TO_DATE( CONCAT(DATE_FORMAT(DATE_ADD('{init_date}', INTERVAL 1 MONTH), '%Y-%m-%d'), ' 00:00:00'), '%Y-%m-%d %H:%i:%s'),"
             " t.status = 'RP',t.compensate_type = 'NCP', t.overdue_days = '0', t.overdue_status = 'M0',date_compensate = null,"
             " t.date_cash = STR_TO_DATE( CONCAT(DATE_FORMAT(DATE_ADD('{init_date}', INTERVAL 1 MONTH), '%Y-%m-%d'), ' 00:00:00'), '%Y-%m-%d %H:%i:%s'),"
             " t.date_inst = DATE_ADD('{init_date}', INTERVAL 1 MONTH), t.date_end = DATE_ADD('{init_date}', INTERVAL 1 MONTH), "
             "t.date_stat = DATE_ADD('{init_date}', INTERVAL 1 MONTH),t.date_settle= null,loan_bal = loan_amt WHERE t.loan_no = '{loan_no}'",

             "UPDATE fund.fd_loan t SET t.date_loan = STR_TO_DATE( CONCAT(DATE_FORMAT(DATE_ADD('{init_date}', INTERVAL 1 MONTH), '%Y-%m-%d'), ' 00:00:00'), '%Y-%m-%d %H:%i:%s'),"
             " t.status = 'RP', t.overdue_days = '0',t.compensate_type = 'NCP', t.overdue_status = 'M0',date_compensate = null,"
             " t.date_cash = STR_TO_DATE( CONCAT(DATE_FORMAT(DATE_ADD('{init_date}', INTERVAL 1 MONTH), '%Y-%m-%d'), ' 00:00:00'), '%Y-%m-%d %H:%i:%s'),"
             " t.date_inst = DATE_ADD('{init_date}', INTERVAL 1 MONTH), t.date_end = DATE_ADD('{init_date}', INTERVAL 1 MONTH), "
             "t.date_stat = DATE_ADD('{init_date}', INTERVAL 1 MONTH) WHERE t.fd_loan_no = '{fd_loan_no}';"]

# 结清单借据
repay_loan = ["update fund.fd_loan set date_settle = '{today}',status = 'FP' where fd_loan_no = '{fd_loan_no}';",
              "update fund.fd_plan_snapshot set rpy_flag = '2' , act_prin_amt = prin_amt,act_int_amt = int_amt,act_oint_amt=oint_amt,date_settle= '{today}' where fd_loan_no = '{fd_loan_no}';",
              "update fund.fd_plan set rpy_flag = '2' , act_prin_amt = prin_amt,act_int_amt = int_amt,act_oint_amt=oint_amt,date_settle= '{today}' where fd_loan_no = '{fd_loan_no}';",
              "update lcs.ln_loan set date_settle = '{today}',status = 'FP' where loan_no = '{loan_no}';",
              "update lcs.ln_plan_snapshot set rpy_flag = '2' , act_prin_amt = prin_amt,act_int_amt = int_amt,act_oint_amt=oint_amt,date_settle= '{today}' where loan_no = '{loan_no}';",
              "update lcs.ln_plan set rpy_flag = '2' , act_prin_amt = prin_amt,act_int_amt = int_amt,act_oint_amt=oint_amt,date_settle= '{today}' where loan_no = '{loan_no}';"]
# 结清用户借据
repay_all_loan = ["update fund.fd_loan set date_settle = '{today}',status = 'FP' where acct_no = '{acct_no}';",
                  "update fund.fd_plan_snapshot set rpy_flag = '2' , act_prin_amt = prin_amt,act_int_amt = int_amt,act_oint_amt=oint_amt,date_settle= '{today}' where acct_no = '{acct_no}';",
                  "update fund.fd_plan set rpy_flag = '2' , act_prin_amt = prin_amt,act_int_amt = int_amt,act_oint_amt=oint_amt,date_settle= '{today}' where acct_no = '{acct_no}';",
                  "update lcs.ln_loan set date_settle = '{today}',status = 'FP' where acct_no = '{acct_no}';",
                  "update lcs.ln_plan_snapshot set rpy_flag = '2' , act_prin_amt = prin_amt,act_int_amt = int_amt,act_oint_amt=oint_amt,date_settle= '{today}' where acct_no = '{acct_no}';",
                  "update lcs.ln_plan set rpy_flag = '2' , act_prin_amt = prin_amt,act_int_amt = int_amt,act_oint_amt=oint_amt,date_settle= '{today}' where acct_no = '{acct_no}';"]


# xurong_loan_nos = "select loan_no from lcs.pilot_loan where cust_no = (select cust_no from cis.u_user where mobile_no_md5 = '{}');"


def get_loan_info(env, loan_no):
    """
    通过客账单号获取部分信息
    """
    sql_1 = """SELECT fd_loan_no,free_days,acct_no,loan_amt,term,date_loan from lcs.ln_loan where loan_no = '{}';""".format(
        loan_no)
    res = db_conn(env).select_one(sql_1)
    print(res, 'sql查询结果', sql_1)
    return res['data']


def get_channel_draw_no(env, loan_no):
    """
    根据主单号获取渠道流水号
    """
    iou_sql = "select channel_draw_no from lps.bm_iou where loan_no = '{loan_no}';"
    iou_data = db_conn(env).select_one(iou_sql.format(loan_no=loan_no))
    # return jsonpath(iou_data, "$..channel_draw_no")[0]
    return parse("$.data.channel_draw_no").find(iou_data)[0].value


def _get_overdue_config(env, fund_code):
    config_sql = ("select max(case when compensation_type = 'OVERDUE' then compensation_value end) as overdue_value,"
                  " max(case when compensation_type = 'ACCUMULATED' then compensation_value end) as accumulated_value, "
                  "max(case when compensation_type = 'CONSECUTIVE' then compensation_value end) as consecutive_value "
                  f"from pds.fund_compensation_config where fund_code = '{fund_code}'and status = '1'and compensation_type in "
                  "('OVERDUE', 'ACCUMULATED', 'CONSECUTIVE');")
    config_data = db_conn(env).select_one(config_sql)
    return config_data['data']


def _query_loan_overdue_days(env, loan_no):
    sql = f"select overdue_days from lcs.ln_loan where loan_no = '{loan_no}';"
    return db_conn(env).select_one(sql)['data']['overdue_days']


def md5_encrypt(text):
    md5 = hashlib.md5()
    md5.update(text.encode('utf-8'))
    return md5.hexdigest()


class LoanBill:
    """
    账单初始化
    """

    def __init__(self, loan_no, overdue_type='N', day=0, bill_day=False, init_date=None, env='BM_SIT'):
        self.env = env
        self.loan_no = loan_no
        self.overdue_type = str(overdue_type or 'N').upper()
        self.bill_day = bool(bill_day)
        self.day = self._validate_day(day)
        self.init_date = self._resolve_init_date(init_date)
        self.value = get_loan_info(env, loan_no)
        self.free_days = self.value['free_days']
        self.fd_loan_no = self.value['fd_loan_no']
        self.acct_no = self.value['acct_no']
        self.amt = self.value['loan_amt']
        self.term = self.value['term']
        self.draw_no = get_channel_draw_no(self.env, self.loan_no)

    def _validate_day(self, day):
        if day is None or str(day).strip() == '':
            return 0
        try:
            day = int(day)
        except (TypeError, ValueError):
            raise AssertionError("day 必须为整数")
        if day < 0:
            raise AssertionError("day 不能小于 0")
        return day

    def _resolve_init_date(self, init_date):
        if init_date is not None and str(init_date).strip() != '':
            try:
                return datetime.datetime.strptime(str(init_date).strip(), '%Y-%m-%d').strftime('%Y-%m-%d')
            except ValueError:
                raise AssertionError('init_date 格式必须为 YYYY-MM-DD')
        return self._build_init_date()

    def _build_init_date(self):
        if self.overdue_type not in ['Y', 'N']:
            raise AssertionError("overdue_type 仅支持 Y 或 N")

        two_month_base_date = datetime.datetime.now() - relativedelta(months=2)
        if self.overdue_type == 'Y':
            target_date = two_month_base_date - timedelta(days=self.day)
            return target_date.strftime('%Y-%m-%d')

        if self.bill_day:
            return two_month_base_date.strftime('%Y-%m-%d')

        month_last_day = (two_month_base_date + relativedelta(day=31)).date()
        target_date = (datetime.datetime.now() - timedelta(days=self.day)) - relativedelta(months=1)
        if target_date.date() > month_last_day:
            max_day = (month_last_day - two_month_base_date.date()).days
            raise AssertionError(f"输入的计息天数超过当月可计算的最大天数，当前最大可输入 {max_day} 天")
        return target_date.strftime('%Y-%m-%d')

    def init_plan_1(self):
        """
            执行初始化sql
        """
        if self.fd_loan_no:
            for sql in init_plan:
                update_sql = sql.format(loan_no=self.loan_no, init_date=self.init_date, fd_loan_no=self.fd_loan_no,
                                        free_days=self.free_days)
                print(f"修改订单信息过程:{update_sql}")
                db_conn(self.env).exec_one(update_sql)
            # 订单初始化完成后，触发计息计费
            # return self.init_token()
            date_3 = datetime.datetime.now().date()
            param_data = f"{self.acct_no},{self.init_date},{date_3}"
            poll_num = 0
            job_id_mapping = {
                'BM_SIT': 123,
                'DEV': 117
            }
            bm_job_id = job_id_mapping.get(self.env)
            # 执行计息计费脚本
            if xxl_job_trigger(bm_job_id, param_data, self.env) == 'pass':
                # 循环查询计息计费结果
                while poll_num <= 3:
                    date_sql = f"select cal_date from lcs.ln_plan_increase where loan_no = '{self.loan_no}' order by cal_date desc limit 1;"
                    new_data = db_conn(self.env).select_one(date_sql)
                    # if new_data == date_3:
                    #     print(f"第{poll_num + 1}次查询试算结果成功")
                    #     return "S"
                    if new_data['data'] is not None:
                        print(f"第{poll_num + 1}次查询计息计费结果成功{new_data},{date_3},{date_sql}")
                        # if fund_plan_mock(self.env, self.amt, self.term) == 'mock_success':
                        #     web_logger.info(f"mock还款数据更新成功")
                        return "S"
                    else:
                        print(f"第{poll_num + 1}次查询计息计费结果失败，正在重试{new_data},{date_3},{date_sql}")
                        poll_num += 1
                        time.sleep(10)
                raise Exception("F")
            else:
                return "F"
        else:
            return "无FD_LOAN_NO"

    def order_status(self):
        """
        查询重置后是否是逾期状态状态，用来确认调用试算接口的参数
        """
        # 获取用户初始时间，并+2月获取第一期应还款日
        date_1 = datetime.datetime.strptime(self.init_date, '%Y-%m-%d')
        date_2 = (date_1 + relativedelta(months=2)).date()
        # 获取当前时间
        date_3 = datetime.datetime.now().date()
        if date_3 > date_2:
            return "O"
        else:
            return "C"


class LoanCompensationFlow:
    """借据代偿流程，按步骤提供方法给接口层调用。"""

    def __init__(self, loan_no, fund_code, number=None, env='BM_SIT'):
        self.loan_no = loan_no
        self.fund_code = fund_code
        self.number = self._to_int(number)
        self.env = env
        self.config = None
        self.effective_number = None
        self.max_day = None

    @staticmethod
    def _to_int(value):
        if value in [None, '']:
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            raise AssertionError(f"无效整数参数: {value}")

    def load_compensation_config(self):
        config = _get_overdue_config(self.env, self.fund_code) or {}
        self.config = {
            'overdue_value': self._to_int(config.get('overdue_value')),
            'accumulated_value': self._to_int(config.get('accumulated_value')),
            'consecutive_value': self._to_int(config.get('consecutive_value')),
        }
        if self.config['overdue_value'] is None:
            raise AssertionError('资方未配置 OVERDUE 代偿天数')
        return self.config

    def calculate_effective_number(self):
        if self.config is None:
            self.load_compensation_config()

        candidates = [
            self.config.get('accumulated_value'),
            self.config.get('consecutive_value'),
            self.number,
        ]
        valid_candidates = [int(item) for item in candidates if item is not None]
        if not valid_candidates:
            raise AssertionError('累计逾期期数、连续逾期期次、代偿几期均为空，无法计算执行期数')

        self.effective_number = min(valid_candidates)
        return self.effective_number

    def calculate_max_day(self):
        if self.config is None:
            self.load_compensation_config()
        if self.effective_number is None:
            self.calculate_effective_number()

        overdue_value = self.config['overdue_value']
        self.max_day = overdue_value + 30 * (self.effective_number - 1)
        return self.max_day

    def init_overdue_for_compensation(self):
        if self.max_day is None:
            self.calculate_max_day()
        return LoanBill(loan_no=self.loan_no, overdue_type='Y', day=self.max_day, env=self.env).init_plan_1()

    def wait_until_overdue_days_ready(self, timeout_seconds=180, interval_seconds=5):
        if self.max_day is None:
            self.calculate_max_day()

        deadline = time.time() + timeout_seconds
        while time.time() < deadline:
            overdue_days = _query_loan_overdue_days(self.env, self.loan_no)
            if overdue_days is not None and int(overdue_days) >= int(self.max_day):
                return True
            time.sleep(interval_seconds)
        raise TimeoutError(f'初始化逾期天数超时，期望 overdue_days={self.max_day}')

    def build_compensation_executor_param(self):
        return f"{self.fund_code}|{datetime.datetime.now().strftime('%Y%m%d')}"

    def trigger_compensation_job(self):
        # 根据环境选择不同的 job_id: bm_sit=171, dev=153
        job_id = 171 if self.env == 'BM_SIT' else 153
        executor_param = self.build_compensation_executor_param()
        result = xxl_job_trigger(job_id, executor_param, self.env)
        if result != 'pass':
            raise AssertionError(f'触发代偿任务失败: job_id={job_id}, executor_param={executor_param}')
        return executor_param

    def trigger_compensation_result_job(self):
        # 根据环境选择不同的 job_id: bm_sit=182, dev=167
        job_id = 182 if self.env == 'BM_SIT' else 167
        result = xxl_job_trigger(job_id, self.fund_code, self.env)
        if result != 'pass':
            raise AssertionError(f'触发代偿结果任务失败: job_id={job_id}, executor_param={self.fund_code}')
        return self.fund_code

    def execute_single_round(self, sleep_seconds=30):
        executor_param = self.trigger_compensation_job()
        time.sleep(sleep_seconds)
        self.trigger_compensation_result_job()
        return {
            'job_id': 171,
            'executor_param': executor_param,
            'result_job_id': 182,
            'result_executor_param': self.fund_code,
        }

    def execute_compensation_rounds(self, sleep_seconds=30):
        if self.effective_number is None:
            self.calculate_effective_number()

        results = []
        for index in range(1, self.effective_number + 1):
            round_result = self.execute_single_round(sleep_seconds=sleep_seconds)
            round_result['round'] = index
            results.append(round_result)
        return results

    def summary(self):
        return {
            'loan_no': self.loan_no,
            'fund_code': self.fund_code,
            'config': self.config,
            'effective_number': self.effective_number,
            'max_day': self.max_day,
            'message': '代偿流程完成',
        }


class LoanBillApi:

    def __init__(self, api_root_url, session=None):
        self.loan_no = None
        self.api_root_url = api_root_url
        self.session = session if session is not None else requests.Session()

    def post_trial(self, loan_No, repayMethod, term=1):
        """
        提交试算
        :param data:
        :return:
        """

        path = loan_api['trial']
        json_data = {
            "meta": {
                "version": "10.0.5"
            },
            "data": {
                "fundCode": "fundloan",
                "loanNo": loan_No,
                "repayMethod": repayMethod,
                "terms": term
            }
        }
        print(f"_post_data::url::{path}\n::json_data::{json_data}")
        return self.session.post(self.api_root_url + path, json=json_data, verify=False)


class RepayLoan:
    """
    还款
    """

    def __init__(self, loan_no, env='BM_SIT'):
        self.loan_no = loan_no
        self.env = env
        self.acct_no = get_loan_info(self.env, self.loan_no)[2]
        self.fd_loan_no = get_loan_info(self.env, self.loan_no)[0]
        self.repay_time = datetime.datetime.now().strftime("%Y-%m-%d")

    def repay_plan(self):
        if self.loan_no:
            for i in repay_loan:
                update_sql = i.format(loan_no=self.loan_no, today=self.repay_time, fd_loan_no=self.fd_loan_no)
                print(f"修改借据信息过程:{update_sql}")
                try:
                    db_conn(self.env).exec_one(update_sql)
                except Exception as e:
                    return f"修改借据信息过程异常{e}"
            return "成功"

    def repay_all(self):
        if self.loan_no:
            for i in repay_all_loan:
                update_sql = i.format(acct_no=self.acct_no, today=self.repay_time)
                print(f"修改借据信息过程:{update_sql}")
                try:
                    db_conn(self.env).exec_one(update_sql)
                except Exception as e:
                    return "修改借据信息过程异常"
                db_conn(self.env).exec_one(update_sql)
            return "成功"


if __name__ == '__main__':
    A = LoanBill('LN1215827929569783808', init_date='2025-07-15', env='BM_SIT')
    print(A.init_plan_1())
    # print(A.init_token())
    # print(A.init_plan_1())
    # print(A.get_channel_draw_no())
    # value = get_loan_info('BM_SIT', 'LN0957955130932604928')
    # print(value['date_loan'])
    # # # 初始化账单测试
    # R = RepayLoan('LN0910370382551269376')
    # print(R.repay_plan())
    # print(_get_overdue_config('BM_SIT', 'ZBANK_E8'))
