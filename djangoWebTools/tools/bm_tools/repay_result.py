import json
import time

from utils.logger_util import web_logger
from config import db_conn

from .bm_common import _log_step, _trigger_repay_sync_job
from .offline_oak_pay import offline_oak_pay_order


def _query_repay_proc_record(loan_no, env, term=None):
    """
    查询还款主状态
    term: 期数，None表示查最新一条，'all'表示提前结清，具体数字表示指定期数
    """
    if term == "all":
        # 提前结清场景
        sql = (
            "select status, tran_proc_rp_no, rpy_terms from lcs.tr_tran_proc_rp "
            f"where loan_no = '{loan_no}' and rpy_type = 'ES';"
        )
        return db_conn(env).get_all(sql) or []
    elif term:
        # 指定期数
        sql = (
            "select status, tran_proc_rp_no, rpy_terms from lcs.tr_tran_proc_rp "
            f"where loan_no = '{loan_no}' and rpy_terms = '{term}';"
        )
        return db_conn(env).get_all(sql) or []
    else:
        # 查最新一条
        sql = (
            "select status, tran_proc_rp_no, rpy_terms from lcs.tr_tran_proc_rp "
            f"where loan_no = '{loan_no}' order by id desc limit 1;"
        )
        result = db_conn(env).select_one(sql)
        return [result.get('data')] if result and result.get('data') else []


def _query_repay_offer_data(loan_no, env):
    sql = (
        "select status, tran_channel, fund_code, offer_req_no from lcs.tr_offer_data where biz_no = "
        "(select tran_proc_rp_no from lcs.tr_tran_proc_rp "
        f"where loan_no = '{loan_no}');"
    )
    return db_conn(env).get_all(sql) or []


def _is_compensation_loan(loan_no, env):
    sql = f"select compensate_type from lcs.ln_loan where loan_no = '{loan_no}';"
    loan_info = db_conn(env).select_one(sql)
    loan_data = (loan_info or {}).get('data') or {}
    return loan_data.get('compensate_type') == 'OCP'


def _mock_fund_repay_fail(env, fund_code, loan_no=None):
    from djangoWebTools.tools.bm_tools.easy_mock_update import update_repay_result_mock
    web_logger.info(f"准备修改资方还款失败mock, env:{env}, fund_code:{fund_code}, loan_no:{loan_no}")
    try:
        result = update_repay_result_mock(env, fund_code, repay_status='FAIL')
        if result.get('success'):
            return {"success": True, "msg": f"{fund_code} 失败mock已更新"}
        return {"success": False, "msg": f"{fund_code} mock更新失败:{result.get('msg')}"}
    except Exception as e:
        web_logger.error(f"修改资方还款失败mock异常:{e}")
        return {"success": False, "msg": f"mock更新异常:{e}"}


def _query_processing_offer_req_nos(loan_no, env):
    sql = (
        "select offer_req_no from lcs.tr_offer_data where biz_no = "
        "(select tran_proc_rp_no from lcs.tr_tran_proc_rp "
        f"where loan_no = '{loan_no}') and status = '02';"
    )
    offer_data = db_conn(env).get_all(sql) or []
    return [item.get('offer_req_no') for item in offer_data if item.get('offer_req_no')]


def _query_inner_offer_req_nos(loan_no, env):
    sql = (
        "select offer_req_no from lcs.tr_offer_data where biz_no = "
        "(select tran_proc_rp_no from lcs.tr_tran_proc_rp "
        f"where loan_no = '{loan_no}') and tran_channel = 'INNER';"
    )
    offer_data = db_conn(env).get_all(sql) or []
    return [item.get('offer_req_no') for item in offer_data if item.get('offer_req_no')]


def _update_partial_success_sql(env, offer_req_nos):
    if not offer_req_nos:
        return {"success": False, "msg": "未查询到INNER渠道offer_req_no"}

    req_no_sql = ','.join([f"'{request_no}'" for request_no in offer_req_nos])
    request_sql = (
        "update pas.fd_request set status = '04', remark = '账户余额不足,不支持路由卡' "
        f"where request_no in ({req_no_sql});"
    )
    withhold_sql = (
        "UPDATE pas.fd_withhold_bf t SET t.result_code = '0001', "
        "t.result_msg = '账户余额不足，不支持路由卡' "
        f"WHERE t.request_no in ({req_no_sql});"
    )
    withhold_tl_sql = (
        "UPDATE pas.fd_withhold_tl t SET t.trans_result_code = '0001', "
        "t.trans_result_msg = '账户余额不足，不支持路由', status = '04' "
        f"WHERE t.request_no in ({req_no_sql});"
    )
    request_res = db_conn(env).exec_one(request_sql)
    withhold_res = db_conn(env).exec_one(withhold_sql)
    withhold_tl_res = db_conn(env).exec_one(withhold_tl_sql)
    web_logger.info(
        f"部分成功修正SQL执行结果 request:{request_res}, withhold:{withhold_res}, withhold_tl:{withhold_tl_res}"
    )
    return {
        "success": True,
        "request_res": request_res,
        "withhold_res": withhold_res,
        "withhold_tl_res": withhold_tl_res,
    }


def _poll_repay_final_status(loan_no, env, target_status, term=None, timeout_seconds=90, interval_seconds=30,
                             progress_callback=None):
    """
    轮询还款主状态
    term: 期数，None表示查最新一条，'all'表示提前结清，具体数字表示指定期数
    timeout_seconds: 超时时间，默认180秒（3分钟）
    """
    start_time = time.time()
    last_status = None
    round_no = 0

    while True:
        round_no += 1
        repay_proc_records = _query_repay_proc_record(loan_no, env, term=term)

        if not repay_proc_records:
            if progress_callback:
                progress_callback(f"第{round_no}次查询还款主状态，未查询到记录")
            last_status = None
        elif len(repay_proc_records) == 1:
            last_status = repay_proc_records[0].get('status')
            if progress_callback:
                progress_callback(
                    f"第{round_no}次查询还款主状态，当前状态:{last_status}，已耗时:{int(time.time() - start_time)}秒")
        else:
            # 多条记录，只要有一条达到目标状态就算成功
            statuses = [record.get('status') for record in repay_proc_records]
            any_match = any(status == target_status for status in statuses)
            if progress_callback:
                progress_callback(
                    f"第{round_no}次查询还款主状态，共{len(repay_proc_records)}条记录，状态:{statuses}，已耗时:{int(time.time() - start_time)}秒")
            if any_match:
                last_status = target_status
            else:
                last_status = ','.join(statuses)

        elapsed_time = time.time() - start_time

        if last_status == target_status:
            return last_status

        if elapsed_time >= timeout_seconds:
            if progress_callback:
                progress_callback(f"轮询超时，已达到{timeout_seconds}秒限制")
            return last_status

        trigger_res = _trigger_repay_sync_job(env)
        if progress_callback:
            progress_callback(f"第{round_no}次触发107结果:{trigger_res}")
        time.sleep(interval_seconds)

    return last_status


def query_repay_result(mobile, loan_no, repay_query_status, env='BM_SIT', channel='lxj', term=None,
                       progress_callback=None):
    steps = []

    def log_step(message):
        _log_step(steps, message, progress_callback)

    repay_query_status = (repay_query_status or '').upper()
    if not mobile:
        raise AssertionError('缺少 mobile')
    if not loan_no:
        raise AssertionError('缺少 loan_no')
    if repay_query_status not in ['SUCCESS', 'FAIL', 'PARTIAL_SUCCESS']:
        raise AssertionError(f'不支持的还款结果查询状态:{repay_query_status}')

    term_desc = f"期数:{term}" if term else "最新一条"
    log_step(f"开始查询还款结果，借据号:{loan_no}，环境:{env}，目标状态:{repay_query_status}，{term_desc}")
    repay_proc_records = _query_repay_proc_record(loan_no, env, term=term)
    if not repay_proc_records:
        log_step('未查询到还款记录，终止流程')
        return 'repay_processing_not_found'

    # 检查是否有还款中的记录
    processing_records = [r for r in repay_proc_records if r.get('status') == '02']
    if not processing_records:
        statuses = [r.get('status') for r in repay_proc_records]
        log_step(f'当前借据无还款中流程，当前状态:{statuses}，终止流程')
        return 'repay_not_processing'

    log_step(f"查询到{len(processing_records)}条还款中记录")

    if repay_query_status == 'SUCCESS':
        log_step('进入还款成功场景，开始轮询主状态是否变更为03')
        final_status = _poll_repay_final_status(
            loan_no,
            env,
            target_status='03',
            term=term,
            progress_callback=log_step,
        )

        if final_status == '03':
            return 'repay_success'

        # 如果轮询后状态为05，检查是否需要触发线下还款
        if final_status == '05':
            log_step('轮询后主状态为05，检查是否需要触发线下还款')
            # 重新查询当前状态，确认没有02
            repay_proc_records_check = _query_repay_proc_record(loan_no, env, term=term)
            has_status_02 = any(r.get('status') == '02' for r in repay_proc_records_check)

            if not has_status_02:
                log_step('确认当前无02状态，触发线下还款流程')
                if not term:
                    log_step('线下还款需要指定期数，当前未指定期数，终止流程')
                    return 'repay_success_offline_no_term'

                offline_result = offline_oak_pay_order(
                    mobile=mobile,
                    loan_no=loan_no,
                    terms=term,
                    env=env,
                    progress_callback=log_step,
                )

                if offline_result.get('success'):
                    log_step('线下还款成功，当期已结清')
                    return 'repay_success'
                else:
                    log_step(f"线下还款失败:{offline_result.get('message')}")
                    return f"repay_success_offline_fail:{offline_result.get('code')}"
            else:
                log_step('检测到仍有02状态，不触发线下还款')

        return f'repay_success_timeout:{final_status}'

    if repay_query_status == 'FAIL':
        # 只查询状态为02的还款记录对应的offer_data
        processing_tran_proc_rp_nos = [r.get('tran_proc_rp_no') for r in processing_records if r.get('tran_proc_rp_no')]
        if not processing_tran_proc_rp_nos:
            log_step('未查询到还款中的tran_proc_rp_no，终止流程')
            return 'repay_fail_offer_not_found'

        tran_proc_rp_no_sql = ','.join([f"'{no}'" for no in processing_tran_proc_rp_nos])
        offer_sql = (
            f"select status, tran_channel, fund_code, offer_req_no from lcs.tr_offer_data "
            f"where biz_no in ({tran_proc_rp_no_sql}) and status = '02';"
        )
        offer_data = db_conn(env).get_all(offer_sql) or []
        log_step(f"查询到{len(offer_data)}条处理中的offer_data记录")

        fund_offers = [
            item for item in offer_data
            if item.get('tran_channel') == 'FUND'
        ]

        if not fund_offers:
            # 没有FUND渠道，查询INNER渠道并修改为失败（代偿场景）
            log_step('未查询到FUND处理中报盘记录，尝试修改INNER渠道为失败')
            inner_offers = [
                item for item in offer_data
                if item.get('tran_channel') == 'INNER'
            ]
            if not inner_offers:
                log_step('未查询到INNER处理中报盘记录，终止流程')
                return 'repay_fail_offer_not_found'

            inner_offer_req_nos = [item.get('offer_req_no') for item in inner_offers if item.get('offer_req_no')]
            log_step(f"准备将INNER渠道改失败，offer_req_no:{inner_offer_req_nos}")
            update_res = _update_partial_success_sql(env, inner_offer_req_nos)
            log_step(f"INNER渠道修正SQL执行结果:{update_res}")
            if not update_res.get('success'):
                return 'repay_fail_inner_update_fail'

            trigger_res = _trigger_repay_sync_job(env)
            log_step(f"修改INNER后触发107结果:{trigger_res}")

            final_status = _poll_repay_final_status(
                loan_no,
                env,
                target_status='04',
                term=term,
                progress_callback=log_step,
            )
            if final_status == '04':
                return 'repay_fail'
            return f'repay_fail_timeout:{final_status}'

        modified_fund_codes = []
        try:
            for item in fund_offers:
                fund_code = item.get('fund_code')
                mock_res = _mock_fund_repay_fail(env, fund_code, loan_no=loan_no)
                log_step(f"资方{fund_code}失败mock处理结果:{mock_res}")
                if mock_res.get('success'):
                    modified_fund_codes.append(fund_code)

            final_status = _poll_repay_final_status(
                loan_no,
                env,
                target_status='04',
                term=term,
                progress_callback=log_step,
            )
            if final_status == '04':
                return 'repay_fail'
            return f'repay_fail_timeout:{final_status}'
        finally:
            if modified_fund_codes:
                from djangoWebTools.tools.bm_tools.easy_mock_update import update_repay_result_mock
                log_step(f"开始回退mock状态到SUCCESS，资方:{modified_fund_codes}")
                for fund_code in modified_fund_codes:
                    try:
                        rollback_res = update_repay_result_mock(env, fund_code, repay_status='SUCCESS')
                        log_step(f"资方{fund_code}mock回退结果:{rollback_res.get('success', False)}")
                    except Exception as e:
                        log_step(f"资方{fund_code}mock回退异常:{e}")

    # 部分成功场景：先检查代偿标识
    compensate_flag_sql = (
        f"select compensate_rpy_flag from lcs.tr_tran_proc_rp "
        f"where loan_no = '{loan_no}' and status = '02';"
    )
    compensate_flag_result = db_conn(env).get_all(compensate_flag_sql) or []
    if compensate_flag_result:
        compensate_flags = [r.get('compensate_rpy_flag') for r in compensate_flag_result]
        log_step(f"查询到代偿标识:{compensate_flags}")
        if 'Y' in compensate_flags:
            log_step('代偿后不支持部分还款，终止流程')
            return 'repay_partial_success_not_supported_compensate'

    # 查询offer_data的渠道信息
    processing_tran_proc_rp_nos = [r.get('tran_proc_rp_no') for r in processing_records if r.get('tran_proc_rp_no')]
    if not processing_tran_proc_rp_nos:
        log_step('未查询到还款中的tran_proc_rp_no，终止流程')
        return 'repay_partial_success_no_processing_records'

    tran_proc_rp_no_sql = ','.join([f"'{no}'" for no in processing_tran_proc_rp_nos])
    offer_channel_sql = (
        f"select tran_channel, status, offer_req_no, fund_code from lcs.tr_offer_data "
        f"where biz_no in ({tran_proc_rp_no_sql});"
    )
    offer_data = db_conn(env).get_all(offer_channel_sql) or []
    channels = [item.get('tran_channel') for item in offer_data]
    log_step(f"查询到offer_data渠道:{set(channels)}")

    # 判断是否包含FUND渠道
    has_fund = 'FUND' in channels
    if has_fund:
        log_step('包含FUND渠道，等待FUND状态变为03')
        # 只触发一次107，等待FUND变为03
        trigger_res = _trigger_repay_sync_job(env)
        log_step(f"触发107结果:{trigger_res}")

        # 轮询检查FUND是否变为03（最多等待3分钟）
        start_time = time.time()
        fund_success = False
        while time.time() - start_time < 180:
            offer_data_check = db_conn(env).get_all(offer_channel_sql) or []
            fund_offers = [item for item in offer_data_check if item.get('tran_channel') == 'FUND']
            fund_statuses = [item.get('status') for item in fund_offers]
            log_step(f"FUND渠道状态:{fund_statuses}")

            if any(status == '03' for status in fund_statuses):
                log_step('FUND渠道已有记录变为03')
                fund_success = True
                break

            time.sleep(30)

        if not fund_success:
            log_step('等待FUND变为03超时')
            return 'repay_partial_success_fund_timeout'

    # 查询INNER渠道的offer_req_no并修改为失败
    inner_offers = [item for item in offer_data if item.get('tran_channel') == 'INNER']
    inner_offer_req_nos = [item.get('offer_req_no') for item in inner_offers if item.get('offer_req_no')]

    if not inner_offer_req_nos:
        log_step('未查询到INNER渠道offer_req_no')
        return 'repay_partial_success_no_inner_offers'

    log_step(f"准备将INNER渠道改失败，offer_req_no:{inner_offer_req_nos}")
    update_res = _update_partial_success_sql(env, inner_offer_req_nos)
    log_step(f"部分成功修正SQL执行结果:{update_res}")
    if not update_res.get('success'):
        return 'partial_success_sql_update_fail'

    # 修改成功后再次触发107
    second_trigger_res = _trigger_repay_sync_job(env)
    log_step(f"部分成功修正后再次触发107，结果:{second_trigger_res}")

    # 轮询验证状态变更为05
    final_status = _poll_repay_final_status(
        loan_no,
        env,
        target_status='05',
        term=term,
        progress_callback=log_step,
    )
    if final_status == '05':
        return 'repay_partial_success'
    return f'repay_partial_success_timeout:{final_status}'
