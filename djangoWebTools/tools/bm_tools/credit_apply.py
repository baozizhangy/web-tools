import datetime
import time

from api.app.bm_api import BmApi
from utils.logger_util import web_logger
from config import db_conn


def credit_apply(mobile=None, name=None, id_card=None, env='BM_SIT', channel='lxj', risk_type='36', credit_apply=None):
    """
    API撞库后，发起授信
    :return:
    """
    api_user = BmApi(channel_id=channel, mobile=mobile, risk_type=risk_type, name=name, id_card=id_card, env=env,
                     credit_apply=credit_apply)
    check_res = api_user.check_user()
    if check_res['check_res']['bizData']['result'] == 1:
        web_logger.info(f"撞库成功，授信前添加风控白名单")
        apply_mobile = check_res['mobile']
        if api_user.risk_white_user()['flag']:
            web_logger.info(f"添加风控白名单成功，开始发起授信")
            res = api_user.credit_apply()
            if res['bizData']['result'] == 1:
                apply_sql = f"select * from hub.hub_channel_bm_apply where channel_apply_no = '{res['bizData']['fundCreditNo']}';"
                bm_user_no = db_conn(env=api_user.env).select_one(apply_sql)['data']['user_no']
                web_logger.info(f"发起授信成功，获取用户user_id{bm_user_no}")
                response_data = {"code": 200, "user_no": f"{bm_user_no}", "mobile": f"{apply_mobile}",
                                 "res": f"请求授信接口返回数据：{res}"}
                web_logger.info(f"返回结果::{response_data}")
                return response_data
            else:
                web_logger.info(f"发起授信失败，请检查授信数据,环境::::{api_user.env}结果::::{res}")
                response_data = {"code": 500, "res": f"请求授信接口返回数据{res}"}
                return response_data
    else:
        web_logger.info(f"撞库失败，请检查撞库数据::::{api_user.env}结果::::{check_res}")
        return "撞库失败"


def query_risk_status(user_no, env='BM_SIT', date_secs=100):
    """
    循环查询用户授信状态，成功或者失败结束查询，超时后直接返回超时
    """
    deadline = datetime.datetime.now() + datetime.timedelta(seconds=date_secs)
    time.sleep(10)
    while datetime.datetime.now() < deadline:
        web_logger.info(f"查询授信状态中")
        sql = f"select state from apv.ap_apply where user_no = '{user_no}';"
        res = db_conn(env).select_one(sql)
        if res['data']['state'] == 'PS':
            return 'PS'
        if res['data']['state'] == 'RJ':
            return 'RJ'
        elif res['data'] is None:
            return 'false'
        time.sleep(20)
    return 'timeout'


if __name__ == '__main__':
    for i in range(10):
        time.sleep(5)
        credit_apply(env='BM_SIT', channel='lxj',
                     risk_type='36', credit_apply=None)