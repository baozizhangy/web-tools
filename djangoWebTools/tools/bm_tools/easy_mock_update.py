import requests
import json
from pytestAutoTest.data import easy_data
from utils.logger_util import web_logger
from config import easy_login_url, easy_update_url, db_conn


class EasyMock:
    """
    easy mock 更新接口
    """

    def __init__(self, desc_name, desc_id, mock_url, method, term, amt, fund_code, cust_no, is_date):
        self.desc_name = desc_name
        self.desc_id = desc_id
        self.mock_url = mock_url
        self.method = method
        self.term = term
        self.amt = amt
        self.fund_code = fund_code
        self.cust_no = cust_no
        self.session = None
        self.Authorization = None
        self.is_date = is_date

    def easy_mock_login(self):
        login_url = easy_login_url()
        web_logger.info(f'easy mock登录中...登录url...{login_url}')
        login_data = {
            "name": "admin",
            "password": "Qcpa7HV2vaz1zoJW"
        }
        self.session = requests.Session()
        response = requests.Session().post(login_url, data=login_data)
        self.Authorization = response.json()['data']['token']
        return response.json()

    def easy_mock_update(self):
        update_url = easy_update_url()
        web_logger.info(f"easy mock更新中...更新url...{update_url},is_data......{self.is_date}")
        if self.fund_code.startswith('ZBANK'):
            mode = easy_data.get_info(term=self.term, amt=self.amt, is_date=self.is_date)
            if mode == "请输入正确的日期格式":
                return 'false'
        if self.fund_code.startswith('ALLINSUSHANG'):
            mode = easy_data.get_tl_info(term=self.term, amt=self.amt, user_no=self.cust_no, is_date=self.is_date)
            if mode == '请输入正确的日期格式':
                return 'false'
        if self.fund_code.startswith('ALLINBLUEOCEAN'):
            mode = easy_data.get_lh_info(term=self.term, amt=self.amt, is_date=self.is_date)
            if mode == '请输入正确的日期格式':
                return 'false'
        if self.fund_code.startswith('ZHONGQIANLIAN'):
            mode = easy_data.get_zql_info(term=self.term, amt=self.amt, is_date=self.is_date)
            if mode == '请输入正确的日期格式':
                return 'false'
        web_logger.info(f"mock数据更新数据{self.term},{self.amt}")
        web_logger.info(
            f"修改的desc_id === {self.desc_id}，修改的mock_url === {self.mock_url} 修改后的mock数据mode === {mode}，")
        update_data = {
            "description": self.desc_name,
            "id": self.desc_id,
            "mode": mode,
            'method': self.method,
            "url": self.mock_url
        }
        if not self.session:
            self.easy_mock_login()
        header = {
            "Authorization": f"Bearer {self.Authorization}"
        }
        session_easy = self.session.post(update_url, data=update_data, headers=header)
        web_logger.info(f"mock本次更新数据{update_data}")
        return session_easy.json()


def get_easy_id(env='BM_SIT', fund_code='ZBANK_E8'):
    # 获取不同环境的mock_id，用来修改还款计划
    web_logger.info(f"获取mock_id中...mock_id...{env},获取的{fund_code}资方的mock_id")

    mock_id = {
        'ZBANK': {'BM_SIT': '66d196d07e1379001edd027a', 'DEV': '66b4307d7e1379001edd021f'},
        'ALLINSUSHANG': {'BM_SIT': '67ea388e4b115700225c7fe6', 'DEV': '67d4e5037d8f5e002203a06f'},
        'ALLINBLUEOCEAN': {'BM_SIT': '68383c5ab8eb4f0022280936', 'DEV': '681ad02969edc40022e2d5c9'},
        'ZHONGQIANLIAN': {'BM_SIT': '6892fa6e30d52600224302e5', 'DEV': '6883432f63e93d0022e1fa80'}
    }
    for prefix in mock_id:
        if fund_code.startswith(prefix):
            web_logger.info(f"获取mock_id中...{env}, 获取的 {fund_code} 资方的 mock_id")
            return mock_id[prefix].get(env)

    return None


def get_mock_url(fund_code='ZBANK_F8'):
    # 获取mock_url
    web_logger.info(f"获取{fund_code}资方的mock_url")
    mock_url = {
        'ZBANK': '/io.kyoto.support.goa.tpfund.zbank.ZBankRepayFacade/repayPlanQuery',
        'ALLINSUSHANG': '/io.kyoto.support.goa.tpfund.sushang.SuShangRepayFacade/repayPlanQuery',
        'ALLINBLUEOCEAN': '/io.kyoto.support.goa.tpfund.allinblueocean.LanHaiRepayFacade/repayPlanQuery',
        'ZHONGQIANLIAN': '/io.kyoto.support.goa.tpfund.zhongqianlian.ZhongQianLianRepayFacade/repayPlan'
    }
    for prefix, url in mock_url.items():
        if fund_code.startswith(prefix):
            return url


def get_mock_name(fund_code='ZBANK_F8'):
    mock_name = {
        'ZBANK': '众邦-还款计划查询',
        'ALLINSUSHANG': '通联苏商-还款计划查询',
        'ALLINBLUEOCEAN': '通联蓝海-还款计划查询',
        'ZHONGQIANLIAN': '中黔联-还款计划查询'
    }
    for prefix, name in mock_name.items():
        if fund_code.startswith(prefix):
            return name


def get_repay_result_mock_id(env='BM_SIT', fund_code='ZBANK_E8'):
    """获取还款结果查询mock_id"""
    web_logger.info(f"获取还款结果查询mock_id, env:{env}, fund_code:{fund_code}")
    mock_id = {
        'ZHONGQIANLIAN': {'BM_SIT': '689ad72030d52600224302e8', 'DEV': '688343b363e93d0022e1fa83'},
        'ALLINSUSHANG': {'BM_SIT': '67ea37534b115700225c7fd9', 'DEV': '681c4b8d69edc40022e2d5ca'},
        'ZBANK': {'BM_SIT': '66d197197e1379001edd027d', 'DEV': '66b2ddd77e1379001edd021c'}
    }
    for prefix in mock_id:
        if fund_code.startswith(prefix):
            return mock_id[prefix].get(env)
    return None


def get_repay_result_mock_url(fund_code='ZBANK_E8'):
    """获取还款结果查询mock_url"""
    web_logger.info(f"获取{fund_code}资方的还款结果查询mock_url")
    mock_url = {
        'ZHONGQIANLIAN': '/io.kyoto.support.goa.tpfund.zhongqianlian.ZhongQianLianRepayFacade/repayQuery',
        'ALLINSUSHANG': '/io.kyoto.support.goa.tpfund.sushang.SuShangRepayFacade/repayResultQuery',
        'ZBANK': '/io.kyoto.support.goa.tpfund.zbank.ZBankRepayFacade/repayStatusQuery'
    }
    for prefix, url in mock_url.items():
        if fund_code.startswith(prefix):
            return url
    return None


def get_repay_result_mock_name(fund_code='ZBANK_E8'):
    """获取还款结果查询mock描述名称"""
    mock_name = {
        'ZHONGQIANLIAN': '中黔联-还款结果查询',
        'ALLINSUSHANG': '通联苏商-还款结果查询',
        'ZBANK': '众邦-还款结果查询'
    }
    for prefix, name in mock_name.items():
        if fund_code.startswith(prefix):
            return name
    return None


def build_repay_result_mock_data(fund_code, repay_status):
    """
    构建还款结果查询mock数据
    repay_status: 'SUCCESS', 'FAIL', 'PROCESSING'
    """
    if fund_code.startswith('ZHONGQIANLIAN'):
        status_map = {'SUCCESS': '1', 'FAIL': '0', 'PROCESSING': '2'}
        mode = {
            "code": "10000",
            "msg": "成功",
            "bizData": {
                "loanRequestNo": "@string(16)",
                "status": status_map.get(repay_status, '0'),
                "loanAmount": "4000",
                "loanTime": "2025-11-20 10:00:00",
                "message": "还款成功" if repay_status == 'SUCCESS' else "还款失败",
                "orderNo": "C882508050014960003"
            }
        }
    elif fund_code.startswith('ALLINSUSHANG'):
        status_map = {'SUCCESS': 'A', 'FAIL': 'F', 'PROCESSING': 'U'}
        mode = {
            "code": "0000",
            "msg": "成功",
            "bizData": {
                "repay_no": "REPAY20231001001",
                "user_id": "CT0984590184257454080",
                "repay_amt": 120,
                "repay_status": status_map.get(repay_status, 'F'),
                "repay_bill_time": "2026-02-11 16:00:45",
                "repay_msg": "账户"
            }
        }
    elif fund_code.startswith('ZBANK'):
        status_map = {'SUCCESS': '1', 'FAIL': '2', 'PROCESSING': '0'}
        mode = {
            "code": "000000",
            "msg": "success",
            "result": {
                "repay_status": status_map.get(repay_status, '2'),
                "fail_msg": "还款成功" if repay_status == 'SUCCESS' else "还款失败",
                "partner_repay_no": "@string(20)",
                "actual_repay_amount": 0.0,
                "repay_principal": 0.0,
                "repay_interest": 0.0,
                "repay_penalty_amount": 0.0,
                "repay_intefine": 0.0,
                "repay_fee": 0.0,
                "grt_fee": "",
                "trans_seq_no": "@string(22)"
            }
        }
    else:
        return None
    return json.dumps(mode, ensure_ascii=False)


def update_repay_result_mock(env, fund_code, repay_status='FAIL'):
    """
    更新还款结果查询mock数据
    env: 'BM_SIT', 'DEV'
    fund_code: 'ZHONGQIANLIAN_F36', 'ALLINSUSHANG_F24', 'ZBANK_E8'
    repay_status: 'SUCCESS', 'FAIL', 'PROCESSING'
    """
    web_logger.info(f"开始更新还款结果查询mock, env:{env}, fund_code:{fund_code}, repay_status:{repay_status}")
    desc_id = get_repay_result_mock_id(env, fund_code)
    if not desc_id:
        web_logger.error(f"未找到{fund_code}在{env}环境的还款结果查询mock_id")
        return {"success": False, "msg": f"未找到{fund_code}在{env}环境的还款结果查询mock_id"}

    mock_url = get_repay_result_mock_url(fund_code)
    desc_name = get_repay_result_mock_name(fund_code)
    if not mock_url or not desc_name:
        web_logger.error(f"未找到{fund_code}的还款结果查询mock配置")
        return {"success": False, "msg": f"未找到{fund_code}的还款结果查询mock配置"}

    mode = build_repay_result_mock_data(fund_code, repay_status)
    if not mode:
        web_logger.error(f"不支持的资方:{fund_code}")
        return {"success": False, "msg": f"不支持的资方:{fund_code}"}

    update_url = easy_update_url()
    update_data = {
        "description": desc_name,
        "id": desc_id,
        "mode": mode,
        "method": "post",
        "url": mock_url
    }

    easy_mock = EasyMock(
        desc_name=desc_name,
        desc_id=desc_id,
        mock_url=mock_url,
        method='post',
        term=12,
        amt=0,
        fund_code=fund_code,
        cust_no=None,
        is_date=None
    )
    login_res = easy_mock.easy_mock_login()
    if not login_res.get('success'):
        web_logger.error(f"easymock登录失败:{login_res}")
        return {"success": False, "msg": "easymock登录失败"}

    header = {"Authorization": f"Bearer {easy_mock.Authorization}"}
    session_easy = easy_mock.session.post(update_url, data=update_data, headers=header)
    web_logger.info(f"还款结果查询mock更新结果:{session_easy.json()}")
    return session_easy.json()


def mock_data_update(user_no, env):
    iou_sql = f"select fund_code from lps.bm_iou where user_no = '{user_no}' order by loan_date desc limit 1;"
    print(iou_sql)
    fund_code = db_conn(env).select_one(iou_sql)['data']['fund_code']
    return fund_code


if __name__ == '__main__':
    # easy_mock = EasyMock(desc_name='中黔联-还款结果查询', desc_id=get_easy_id('DEV', 'ZHONGQIANLIAN_F36'),
    #                      mock_url=get_mock_url('ZHONGQIANLIAN_F36'), method='post',
    #                      term=12, amt=4000, fund_code='ZHONGQIANLIAN_F36', cust_no=None, is_date='2025-05-29')
    print(update_repay_result_mock('DEV', 'ZHONGQIANLIAN_F36', 'SUCCESS'))
    # print(get_mock_url('ALLINSUSHANG_F8'))
