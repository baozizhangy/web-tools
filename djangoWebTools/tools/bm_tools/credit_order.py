import datetime
import json
import time
from typing import Callable, Optional

from api.app.bm_api import BmApi
from utils.logger_util import web_logger
from config import db_conn, redis_db_conn
from djangoWebTools.tools.bm_tools.ask_xxl import xxl_job_trigger
from djangoWebTools.tools.bm_tools.easy_mock_update import EasyMock, get_easy_id, get_mock_url, get_mock_name
from pytestAutoTest.data.apply_data import fetch_credit_info

from .bm_common import _log_step


def credit_order(mobile, is_privilege, profit_type=None, term=None, amt=None, env='BM_SIT', channel='lxj'):
    """
    发起借款订单
    :param mobile: 手机号
    :param is_privilege: 是否特权还款标志
    :param term: 借款期限，默认为12期
    :param amt: 借款金额，默认为3500元
    :param env: 环境标识，默认为 BM_SIT
    :param channel: 渠道标识，默认为 lxj
    :param profit_type:权益标识，默认None
    :return: 操作结果信息
    """

    # 设置默认期限和金额
    term = term if term is not None else 12
    amt = amt if amt is not None else 3500
    web_logger.info(f"[借款开始] 手机号: {mobile}, 期数: {term}, 金额: {amt}, 环境: {env}, 渠道: {channel}")
    # 提取用户信息
    credit_res = fetch_credit_info(mobile, env)
    if not credit_res:
        web_logger.warning(f"[授信查询失败] 手机号: {mobile}, 环境: {env}")
        return 'apply_fail'
    bm_user_no, user_no, credit_req_no, apply_no, cust_no = credit_res['bm_user_no'], credit_res['partner_user_no'], \
        credit_res[
            'partner_channel_apply_no'], credit_res['channel_apply_no'], credit_res['cust_no']

    if is_privilege == 'Y':
        if query_profit_status(cust_no, env) is True:
            web_logger.info(f"[已开通特权还款] 用户: {cust_no}")
            return "该用户已开通特权还款"
    api_user = BmApi(term=term, amt=amt, channel_id=channel, mobile=mobile, env=env)
    # 查询用户绑卡信息，返回卡号
    try:
        card_list = api_user.card_query(user_no)['bizData']['cardList']
        card_no = card_list[-1]['cardNo']
    except (IndexError, KeyError):
        web_logger.warning("[绑卡流程] 未查到绑卡信息，准备发起绑卡流程")
        # 查询不到卡信息，触发用户绑卡,获取绑卡验证码
        bind_res = api_user.card_bind(user_no, credit_req_no)
        fund_req_no = bind_res['bizData']['fundBindReqNo']
        if api_user.card_bind_sms(user_no, fund_req_no)['bizData']['result'] == '1':
            web_logger.info("[绑卡成功] 已成功完成绑卡")
        card_no = api_user.card_query(user_no)['bizData']['cardList'][-1]['cardNo']
    # 获取一次借款合同
    if api_user.agreement_list(user_no, credit_req_no)['code'] != '200':
        web_logger.info("[合同失败] 获取借款合同失败")
        return "合同获取失败"
    # 发起试算
    api_user.draw_trial(credit_req_no, apply_no, is_privilege)
    # 试算后，发起借款
    draw_status = api_user.draw_submit(user_no, credit_req_no, card_no, is_privilege, profit_type)
    web_logger.info(f"[借款提交结果] {draw_status}")
    #  判断是否需要二次验证
    result_code = draw_status['bizData']['result']
    biz_no_sql = f"SELECT partner_draw_no FROM hub.hub_channel_bm_draw WHERE user_no = '{bm_user_no}' ORDER BY id DESC LIMIT 1;"
    biz_no = db_conn(env).select_one(biz_no_sql)['data']['partner_draw_no']
    if result_code == 3:
        web_logger.info("[二次验证] 借款需要二次身份验证，biz_no: %s", biz_no)
        # 发起二次验证，真实获取验证码
        api_user.send_sms_code(user_no, biz_no, '01')
        sms_sql = ("select * from cns.p_notice_record where event_code = 'e_draw_identity_verify_code' "
                   f"and p_notice_record.user_no = '{bm_user_no}'order by send_time desc limit 1;")
        sms_code = json.loads(db_conn(env).select_one(sms_sql)['data']['params'])['params']['code']
        web_logger.info(f"[验证码获取成功] code: {sms_code}")
        verify_res = api_user.send_sms(user_no, '01', sms_code, biz_no)
        web_logger.info(f"二次验证码校验通过{verify_res}")
        # 再次确认是否需要验证：
        if api_user.draw_step_query(biz_no, credit_req_no)['bizData']['result'] == 1:
            time.sleep(10)
            iou_sql = f"select fund_code from lps.bm_iou where user_no = '{bm_user_no}' order by loan_date desc limit 1;"
            A = db_conn(env).select_one(iou_sql)
            fund_code = A['data']['fund_code']
            web_logger.info(
                f"查询到用户user_no{bm_user_no},环境{env}的资方{fund_code},本次sql执行结果{A}，执行的sql{iou_sql}")
            if fund_code is not None:
                web_logger.info(f"查询到资方{fund_code}")
                # 创建订单后，根据用户的金额和期数，资方，调整资方mock还款数据
                fund_plan_mock(env, amt, term, fund_code)
                web_logger.info(f"调整mock还款数据成功")
                return "二次创建成功A"
            web_logger.info(f"放款前，修改mock还款计划金额{amt}，期数{term},资方{fund_code}")
            return "二次创建成功B"
    else:
        web_logger.info(f"查询借款流水号sql{biz_no_sql},获取结果{biz_no}")
        api_user.draw_step_query(biz_no, credit_req_no)
        return "订单创建成功"


def _poll_ap_draw_state(loan_req_no, env, timeout_seconds=180, interval_seconds=30, progress_callback=None):
    ap_draw_sql = f"select state from apv.ap_draw where ref_appl_no = '{loan_req_no}';"
    start_time = time.time()
    last_state = None
    if progress_callback:
        progress_callback(f"借据进入风险审批流程")
    while True:
        ap_draw_res = db_conn(env).select_one(ap_draw_sql)
        last_state = ((ap_draw_res or {}).get('data') or {}).get('state')
        web_logger.info(f"轮询ap_draw状态，sql:{ap_draw_sql}, 结果:{ap_draw_res}")
        if last_state in ['PS', 'RJ']:
            return last_state
        if time.time() - start_time >= timeout_seconds:
            return None
        time.sleep(interval_seconds)


def _poll_iou_state(bm_user_no, env, target_states, fail_states=None, timeout_seconds=180, interval_seconds=30,
                    step_name='loan_state', progress_callback=None, state_callback=None):
    iou_sql = (
        f"select loan_state from lps.bm_iou where user_no = '{bm_user_no}' "
        f"order by id desc limit 1;"
    )
    start_time = time.time()
    last_state = None
    fail_states = fail_states or []
    if progress_callback:
        progress_callback(f"查询借据放款中间态")
    while True:
        iou_res = db_conn(env).select_one(iou_sql)
        last_state = ((iou_res or {}).get('data') or {}).get('loan_state')
        web_logger.info(f"轮询{step_name}状态，sql:{iou_sql}, 结果:{iou_res}")
        if progress_callback:
            progress_callback(f"轮询{step_name}状态 loan_state={last_state}")
        if state_callback:
            state_callback(last_state)

        if last_state in target_states or last_state in fail_states:
            return last_state
        if time.time() - start_time >= timeout_seconds:
            return None
        time.sleep(interval_seconds)


def _delete_lcs_cache(env):
    redis_res = redis_db_conn(env).delete_by_pattern("pds*")
    web_logger.info(f"删除pds缓存结果:{redis_res}")
    return redis_res


def _update_fund_match_config(env, loan_query_status=None, fund_code=None):
    if not loan_query_status:
        return None

    loan_query_status = str(loan_query_status).upper()
    if loan_query_status in ['SUCCESS', 'LOAN_SUCCESS', 'NORMAL', '放款成功', 'BLACK_TIME', '资方黑暗期',
                             'FUND_BLACK_TIME', '单资方黑暗期', 'RISK_REJECT', '风险拒绝']:
        return None

    if loan_query_status in ['SPECIFIED_FUND', '指定资金放款']:
        if not fund_code:
            raise AssertionError("指定资金放款场景缺少 fund_code")
        sql = (
            "update pds.fund_biz_config set fund_biz_config.status = '1' "
            "where biz_key = 'exclude_fund_id_card_address' "
            f"and fund_code != '{fund_code}';"
        )
    elif loan_query_status in ['ALL_FUND_MATCH_FAIL', '全部资金匹配失败']:
        sql = (
            "update pds.fund_biz_config set fund_biz_config.status = '1' "
            "where biz_key = 'exclude_fund_id_card_address';"
        )

    else:
        raise AssertionError(f"不支持的放款查询状态:{loan_query_status}")

    update_res = db_conn(env).exec_one(sql)
    web_logger.info(f"放款查询前更新资金匹配配置，状态:{loan_query_status}, sql:{sql}, 结果:{update_res}")
    _delete_lcs_cache(env)
    time.sleep(60)
    return update_res


def _rollback_fund_match_config(env):
    sql = "update pds.fund_biz_config set fund_biz_config.status = '0' where biz_key = 'exclude_fund_id_card_address';"
    rollback_res = db_conn(env).exec_one(sql)
    web_logger.info(f"放款查询后回退资金匹配配置，sql:{sql}, 结果:{rollback_res}")
    _delete_lcs_cache(env)
    return rollback_res


def _update_black_time_config(env, loan_query_status=None, fund_code=None):
    if not loan_query_status:
        return []

    loan_query_status = str(loan_query_status).upper()
    if loan_query_status in ['FUND_BLACK_TIME', '单资方黑暗期']:
        if not fund_code:
            raise AssertionError("单资方黑暗期场景缺少 fund_code")
        query_sql = f"select fund_code, day_draw_end_time from pds.fund_limit where fund_code = '{fund_code}';"
        update_sql = f"UPDATE pds.fund_limit t SET t.day_draw_end_time = '01:00:00' WHERE fund_code = '{fund_code}';"
    elif loan_query_status in ['BLACK_TIME', '资方黑暗期']:
        query_sql = "select fund_code, day_draw_end_time from pds.fund_limit where 1 = 1;"
        update_sql = "UPDATE pds.fund_limit t SET t.day_draw_end_time = '01:00:00' WHERE 1 = 1;"
    else:
        return []

    snapshot = db_conn(env).get_all(query_sql) or []
    update_res = db_conn(env).exec_one(update_sql)
    web_logger.info(f"放款查询前打开黑暗期，状态:{loan_query_status}, sql:{update_sql}, 结果:{update_res}")
    _delete_lcs_cache(env)
    time.sleep(60)
    return snapshot


def _rollback_black_time_config(env, snapshot):
    if not snapshot:
        _delete_lcs_cache(env)
        return None

    rollback_results = []
    for item in snapshot:
        item_fund_code = item.get('fund_code')
        day_draw_end_time = item.get('day_draw_end_time')
        rollback_sql = (
            "UPDATE pds.fund_limit t "
            f"SET t.day_draw_end_time = '{day_draw_end_time}' "
            f"WHERE fund_code = '{item_fund_code}';"
        )
        rollback_results.append(db_conn(env).exec_one(rollback_sql))
    web_logger.info(f"放款查询后回退黑暗期配置，结果:{rollback_results}")
    _delete_lcs_cache(env)
    return rollback_results


def _delete_reject_record(env='BM_SIT'):
    res = sql = "delete FROM fund.fund_reject_record where 1= 1;"
    db_conn(env).exe_multi(sql)
    web_logger.info(f"删除资金拒绝数据，sql:{sql}")
    return res


def query_order(mobile, env='BM_SIT', channel='lxj', loan_query_status=None, fund_code=None, progress_callback=None):
    steps = []

    def log_step(message):
        _log_step(steps, message, progress_callback)

    log_step(
        f"开始查询并推进放款流程，手机号:{mobile}, 环境:{env}, 渠道:{channel}, 场景:{loan_query_status or 'SUCCESS'}")
    job_id_mapping = {
        'BM_SIT': 130,
        'DEV': 122
    }
    aps_job_id_mapping = {
        'BM_SIT': 131,
        'DEV': 123
    }
    cos_job_id_mapping = {
        'BM_SIT': 145,
        'DEV': 136
    }
    fund_jjob_id_mapping = {
        'BM_SIT': 174,
        'DEV': 160
    }
    lps_job_id_mapping = {
        'BM_SIT': 132,
        'DEV': 124
    }
    lps_loan_id_mapping = {
        'BM_SIT': 217,
        'DEV': 196
    }

    latest_iou_sql = (
        "select user_no, loan_req_no, loan_state, fund_code, loan_amt, loan_term, cust_no "
        "from lps.bm_iou where user_no = (select user_no from cis.u_user "
        f"where mobile_no_md5 = md5('{mobile}')) order by loan_date desc limit 1;"
    )
    latest_loan_info = db_conn(env).select_one(latest_iou_sql)
    log_step("查询到需处理的借款订单")
    latest_loan_data = (latest_loan_info or {}).get('data') or {}
    if not latest_loan_data:
        web_logger.info(f"未查询到借款订单，sql:{latest_iou_sql}, 结果:{latest_loan_info}")
        return "未查询到借款订单"

    latest_iou_status = latest_loan_data.get('loan_state')
    if latest_iou_status == 'DS':
        web_logger.info("查询到订单状态为DS，已经放款成功")
        return 'order_ds'
    if latest_iou_status == 'ARJ':
        web_logger.info("查询到订单状态为ARJ，放款失败")
        return 'fail'

    iou_sql = (
        "select user_no, loan_req_no, loan_state, fund_code, loan_amt, loan_term, cust_no "
        "from lps.bm_iou where user_no = (select user_no from cis.u_user "
        f"where mobile_no_md5 = md5('{mobile}')) "
        "and loan_state not in ('ACS','ARJ','DS', 'DJ','CAN') "
        "order by loan_date desc limit 1;"
    )
    loan_info = db_conn(env).select_one(iou_sql)
    log_step("已查询可处理的待放款借据")
    loan_data = (loan_info or {}).get('data') or {}
    if not loan_data:
        web_logger.info(f"未查询到可处理借款订单，sql:{iou_sql}, 结果:{loan_info}")
        return f"未查询到可处理借款订单，当前状态:{latest_iou_status}"

    bm_user_no = loan_data['user_no']
    loan_req_no = loan_data['loan_req_no']
    matched_fund_code = loan_data['fund_code']
    loan_amt = loan_data['loan_amt']
    loan_term = loan_data['loan_term']
    cust_no = loan_data['cust_no']
    effective_fund_code = fund_code or matched_fund_code
    should_rollback_fund_config = bool(loan_query_status) and str(loan_query_status).upper() in [
        'SPECIFIED_FUND', '指定资金放款', 'ALL_FUND_MATCH_FAIL', '全部资金匹配失败'
    ]
    should_rollback_black_time_config = bool(loan_query_status) and str(loan_query_status).upper() in [
        'BLACK_TIME', '资方黑暗期', 'FUND_BLACK_TIME', '单资方黑暗期'
    ]
    black_time_snapshot = []

    try:
        log_step("开始处理资金匹配/黑暗期配置")
        _update_fund_match_config(env, loan_query_status=loan_query_status, fund_code=effective_fund_code)
        black_time_snapshot = _update_black_time_config(
            env,
            loan_query_status=loan_query_status,
            fund_code=effective_fund_code,
        )
        log_step("资金匹配/黑暗期配置处理完成")
        _delete_reject_record(env)
        log_step("已清理资金拒绝记录，开始执行预处理任务")

        pre_job_res = xxl_job_trigger(
            lps_loan_id_mapping.get(env),
            executor_param='{"startMinutes":8800,"endMinutes":0,"size":200,"subProductCode":""}',
            env=env,
        )
        xxl_job_trigger(job_id=cos_job_id_mapping.get(env), env=env)
        log_step(f"预处理任务执行结果:{pre_job_res}，已触发COS任务")
        if pre_job_res != 'pass':
            web_logger.info(f"执行217预处理脚本失败: {pre_job_res}")
            return 'job_217_fail'

        ap_draw_state = _poll_ap_draw_state(
            loan_req_no=loan_req_no,
            env=env,
            progress_callback=log_step,
        )
        if ap_draw_state == 'RJ':
            web_logger.info("ap_draw状态为RJ，直接返回放款失败")
            return 'fail'
        if ap_draw_state != 'PS':
            web_logger.info(f"ap_draw状态轮询超时，loan_req_no:{loan_req_no}, 最终状态:{ap_draw_state}")
            return '风险审批异常'

        aps_job_id = aps_job_id_mapping.get(env)
        bm_job_id = job_id_mapping.get(env)

        if effective_fund_code is not None:
            if effective_fund_code == 'ALLINSUSHANG_F24':
                fund_plan_mock(env, loan_amt, loan_term, cust_no, is_data=datetime.datetime.now(),
                               fund_code=effective_fund_code)
            else:
                fund_plan_mock(env, loan_amt, loan_term, is_data=datetime.datetime.now(), fund_code=effective_fund_code)
        else:
            fund_plan_mock(env, loan_amt, loan_term,
                           is_data=datetime.datetime.now())
        web_logger.info(f"执行放款脚本前，修改mock还款计划金额{loan_amt}，期数{loan_term},资方{effective_fund_code}")
        log_step(f"已修改资方还款计划mock，资方:{effective_fund_code}，金额:{loan_amt}，期数:{loan_term}")

        iou_status = _poll_iou_state(
            bm_user_no=bm_user_no,
            env=env,
            target_states=['APR', 'DR', 'APS', 'DS'],
            fail_states=['ARJ', 'DJ'],
            step_name='放款主流程',
            progress_callback=log_step,
        )
        print(f"查询借据状态，状态输出得结果:{iou_status}")
        if iou_status == 'DS':
            return 'order_ds'
        if iou_status == 'ARJ':
            return 'fail'
        if iou_status == 'DJ':
            return 'fund_fail'

        if iou_status is None:
            return '放款主流程状态轮询超时'

        if iou_status == 'APR':
            web_logger.info("查询到借据状态为APR，开始执行lps放款脚本")
            log_step("借据进入APR，开始执行LPS放款脚本")
            if xxl_job_trigger(bm_job_id, '{"startMinutes":180,"endMinutes":1}', env=env) != 'pass':
                return 'lps_job_fail'

            iou_status = _poll_iou_state(
                bm_user_no=bm_user_no,
                env=env,
                target_states=['DR', 'DS'],
                fail_states=['ARJ', 'DJ'],
                step_name='APR到DR',
                progress_callback=log_step,
            )
            if iou_status == 'DS':
                return 'order_ds'
            if iou_status == 'ARJ':
                return 'fail'
            if iou_status == 'DJ':
                return 'fund_fail'
            if iou_status is None:
                return 'APR到DR轮询超时'

        if iou_status == 'DR':
            web_logger.info("查询到订单状态为DR，开始执行lcs放款脚本")
            log_step("借据进入DR，开始执行LCS放款脚本")
            xxl_job_trigger(lps_job_id_mapping.get(env), executor_param='{"startMinutes":1440,"endMinutes":0}', env=env)
            if xxl_job_trigger(113, env=env) != 'pass':
                return 'job_113_fail'
            if xxl_job_trigger(115, env=env) != 'pass':
                return 'job_115_fail'

            dr_poll_count = 0
            dr_retry_triggered = False

            def trigger_lcs_retry_when_still_dr(state):
                nonlocal dr_poll_count, dr_retry_triggered
                if state != 'DR' or dr_retry_triggered:
                    return
                dr_poll_count += 1
                if dr_poll_count < 2:
                    return
                log_step("连续两次轮询仍为DR，补偿触发一次LCS放款脚本")
                xxl_job_trigger(
                    lps_job_id_mapping.get(env),
                    executor_param='{"startMinutes":1440,"endMinutes":1}',
                    env=env,
                )
                dr_retry_triggered = True

            final_status = _poll_iou_state(
                bm_user_no=bm_user_no,
                env=env,
                target_states=['DS'],
                fail_states=['ARJ', 'DJ'],
                step_name='LCS放款结果',
                progress_callback=log_step,
                state_callback=trigger_lcs_retry_when_still_dr,
            )
            if final_status == 'DS':
                return 'lcs_success'
            if final_status == 'ARJ':
                return 'fail'
            if final_status == 'DJ':
                return 'fund_fail'
            return 'LCS放款结果轮询超时'

        if iou_status == 'APS':
            web_logger.info("查询到订单状态为APS，开始执行APS放款脚本")
            log_step("借据进入APS，开始执行APS放款脚本")
            xxl_job_trigger(fund_jjob_id_mapping.get(env), executor_param='{"endMinutes":0,"minutes":172800}', env=env)
            if xxl_job_trigger(aps_job_id, executor_param='{"startMinutes": 180, "endMinutes": 1}', env=env) != 'pass':
                return 'aps_job_fail'

            final_status = _poll_iou_state(
                bm_user_no=bm_user_no,
                env=env,
                target_states=['DS'],
                fail_states=['ARJ', 'DJ'],
                step_name='APS放款结果',
                progress_callback=log_step,
            )
            if final_status == 'DS':
                return 'lcs_success'
            if final_status == 'ARJ':
                return 'fail'
            if final_status == 'DJ':
                return 'fund_fail'
            return 'APS放款结果轮询超时'

        return f'未知放款状态:{iou_status}'

    finally:
        cleanup_tasks = [("回滚资金匹配配置", lambda: _rollback_fund_match_config(env))]
        if should_rollback_black_time_config and black_time_snapshot:
            cleanup_tasks.append(("回滚黑暗期配置", lambda: _rollback_black_time_config(env, black_time_snapshot)))

        for cleanup_name, cleanup_func in cleanup_tasks:
            try:
                log_step(f"开始{cleanup_name}")
                cleanup_func()
                log_step(f"{cleanup_name}完成")
            except Exception as e:
                web_logger.error(f"{cleanup_name}异常:{e}")
                log_step(f"{cleanup_name}异常:{e}")


def fund_plan_mock(env, amt, term, cust_no=None, is_data=None, fund_code='ZBANK_E8'):
    # 调整资方mock还款数据
    # 一个是创建订单前，一个是触发还款前
    desc_id = get_easy_id(env, fund_code)
    # desc_name = fund_desc_map[fund_code]
    mock_url = get_mock_url(fund_code)
    desc_name = get_mock_name(fund_code)
    web_logger.info(f"更新mock接口的id为{desc_id},环境{env},金额为{amt},期数为{term},本次mock数据更新传时间{is_data}")
    easy_mock = EasyMock(desc_name=desc_name, desc_id=desc_id,
                         mock_url=mock_url, method='post',
                         term=int(term), amt=int(amt), fund_code=fund_code, cust_no=cust_no, is_date=is_data)
    res_1 = easy_mock.easy_mock_update()
    web_logger.info(f"更新mock接口返回数据{res_1}")
    try:
        if res_1['success'] is True:
            web_logger.info(f"更新的id = {desc_id}")
            web_logger.info(f"mock还款数据更新成功")
            return "mock_success"
    except TypeError as e:
        web_logger.info(f"mock还款数据更新失败，错误信息为{e}")
        if res_1 == 'false':
            return "date_false"
        else:
            return "mock_fail"


def query_profit_status(profit_cust_no, env='BM_SIT'):
    """
    cust_no： 用户号

    """
    sql = f"select * from cos.bm_membership_user where cust_no = '{profit_cust_no}'  and status != 'INVALID' and status != 'REFUND';"
    res = db_conn(env).select_one(sql)
    if res['data']:
        return True
    else:
        return None


if __name__ == '__main__':
    A = [
         17814709423,
         17714799966,
         17714083889,
         19814199337,
         15114952964,
         19714462190]
    for index, mobile in enumerate(A):
        if index > 0:
            time.sleep(10)
        print(credit_order(mobile=mobile, is_privilege='Y',profit_type='Y', env='BM_SIT'))
