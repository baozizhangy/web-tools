import json

from api.app.bm_api import BmApi
from utils.logger_util import web_logger
from config import db_conn
from djangoWebTools.tools.bm_tools.ask_xxl import xxl_job_trigger


def repay_order(loan_no, trial_type, env='BM_SIT', channel='lxj'):
    info_sql = (f"select user_no,partner_draw_no,channel_apply_no from hub.hub_channel_bm_draw "
                f"where draw_no = (select loan_req_no from lcs.ln_loan where loan_no = '{loan_no}');")
    web_logger.info(f"查询环境{env}")
    info = db_conn(env).select_one(info_sql)['data']
    web_logger.info(f"查询用户信息sql   {info_sql},查询结果{info}")
    bm_user_no, biz_no, credit_req_no = info['user_no'], info['partner_draw_no'], info['channel_apply_no']
    user_info_sql = f"select partner_user_no from hub.hub_channel_bm_apply where user_no = '{bm_user_no}';"
    user_no = db_conn(env).select_one(user_info_sql)['data']['partner_user_no']
    bm_api = BmApi(channel_id=channel, mobile=None, env=env)
    repay_no = "RR182093812093" + str(bm_api.flow_num)
    periods = []
    if trial_type == 4:
        sql = f"select term from lcs.ln_plan where loan_no = '{loan_no}' and rpy_flag != 2;"
        periods = [i['term'] for i in db_conn(env).get_all(sql)]
    if trial_type == 1 or trial_type == 2:
        sql = f"select term from lcs.ln_plan where loan_no = '{loan_no}' and rpy_flag != 2 order by term limit 1;"
        periods.append(db_conn(env).select_one(sql)['data']['term'])
    # 试算
    trial_res = bm_api.repay_trial(user_no, biz_no, credit_req_no, trial_type, periods)
    web_logger.info(f"试算结果为:{trial_res}，本次还款方式:{trial_type},触发还款的期数:{periods}")
    if trial_res['bizData']['result'] != 1:
        return {"code": 201, "res": f"试算异常，发起还款失败"}
    repay_amt = trial_res['bizData']['deserveTotalAmt']
    T = bm_api.card_query(user_no)['bizData']['cardList'][-1]
    card_no, mobile = T['cardNo'], T['bankMobile']
    # 发起还款请求
    repay_res = bm_api.repay_submit(biz_no, trial_type, repay_amt, card_no, mobile, repay_no, periods)
    web_logger.info(f"还款请求结果为{repay_res}")
    if repay_res['bizData']['result'] == 2:
        return {"code": 202, "res": f"发起还款失败{repay_res}"}
    if repay_res['bizData']['result'] == 1:
        responses = {"code": 200, "res": f"还款发起成功，还款流水号{repay_no}"}
        return responses
    if repay_res['bizData']['result'] == 3:
        # 判断是否需要二次验证，需要时发送短信验证码
        bm_api.send_sms_code(user_no, repay_no, '02')
        sms_sql = ("select * from cns.p_notice_record where event_code = 'e_repay_identity_verify_code' "
                   f"and p_notice_record.user_no = '{bm_user_no}'order by send_time desc limit 1;")
        sms_code = json.loads(db_conn(env).select_one(sms_sql)['data']['params'])['params']['code']
        # 校验还款验证码
        bm_api.send_sms(user_no, '02', sms_code, repay_no)
        responses = {"code": 200, "res": f"还款发起成功，还款流水号{repay_no}"}
        web_logger.info(f"还款发起成功，短信校验结果{responses}")
        return responses


def trail_order(loan_no, trial_type, env='BM_SIT', channel='lxj'):
    info_sql = (f"select user_no,partner_draw_no,channel_apply_no from hub.hub_channel_bm_draw "
                f"where draw_no = (select loan_req_no from lcs.ln_loan where loan_no = '{loan_no}');")
    info = db_conn(env).select_one(info_sql)['data']
    bm_user_no, biz_no, credit_req_no = info['user_no'], info['partner_draw_no'], info['channel_apply_no']
    user_info_sql = f"select partner_user_no from hub.hub_channel_bm_apply where user_no = '{bm_user_no}';"
    user_no = db_conn(env).select_one(user_info_sql)['data']['partner_user_no']
    bm_api = BmApi(mobile=None, channel_id=channel, env=env)
    periods = []
    if trial_type == 4:
        sql = f"select term from lcs.ln_plan where loan_no = '{loan_no}' and rpy_flag != 2;"
        periods = [i['term'] for i in db_conn(env).get_all(sql)]
    if trial_type == 1 or trial_type == 2:
        sql = f"select term from lcs.ln_plan where loan_no = '{loan_no}' and rpy_flag != 2 order by term limit 1;"
        periods.append(db_conn(env).select_one(sql)['data']['term'])
    # 试算
    trial_res = bm_api.repay_trial(user_no, biz_no, credit_req_no, trial_type, periods)
    web_logger.info(f"试算结果为:{trial_res}，本次还款方式:{trial_type},触发还款的期数:{periods}")
    responses = {"code": 200, "res": f"试算发起成功，试算结果{trial_res}"}
    web_logger.info(f"还款发起成功，短信校验结果{responses}")
    return responses


def query_repay_order(repay_req_no, env='BM_SIT', channel='lxj'):
    bm_api = BmApi(mobile=None, channel_id=channel, env=env)
    repay_info = bm_api.repay_result_query(repay_req_no)
    if xxl_job_trigger('107', env=env) == 'pass':
        web_logger.info(f"执行放款中状态同步成功")
    return repay_info
