import json
import time

from utils.logger_util import web_logger
from config import db_conn
from api.app.h5_api import H5Api
from djangoWebTools.tools.bm_tools.ask_xxl import xxl_job_trigger

from .bm_common import _log_step, _to_dict_response, _trigger_repay_sync_job


def _query_loan_req_no(loan_no, env):
    sql = (
        "select loan_req_no from lps.bm_iou "
        f"where loan_no = '{loan_no}' order by id desc limit 1;"
    )
    result = db_conn(env).select_one(sql)
    data = (result or {}).get('data') or {}
    loan_req_no = data.get('loan_req_no')
    if not loan_req_no:
        raise AssertionError(f"未查询到借据对应的 loan_req_no, loan_no:{loan_no}, 查询结果:{result}")
    return str(loan_req_no)


def _extract_total_amount_from_trial(trial_res):
    trial_data = (trial_res or {}).get('data') or {}
    total_amount = trial_data.get('totalAmount')
    if total_amount is None or str(total_amount).strip() == '':
        raise AssertionError(f"还款试算结果缺少 totalAmount:{trial_res}")
    return str(total_amount)


def _query_vip_loan_order_status(loan_no, env):
    sql = f"select order_status from cos.vip_loan_order where loan_no = '{loan_no}' order by id desc limit 1;"
    result = db_conn(env).select_one(sql)
    data = (result or {}).get('data') or {}
    return data.get('order_status'), result


def _update_vip_loan_order_success(loan_no, env):
    sql = f"update cos.vip_loan_order set order_status = 'success' where loan_no = '{loan_no}' and order_status = 'init';"
    return db_conn(env).exec_one(sql)


def _trigger_offline_repay_prepare_jobs(env, progress_callback=None):
    first_job_map = {
        'BM_SIT': '335',
        'DEV': '281',
    }
    second_job_map = {
        'BM_SIT': '332',
        'DEV': '276',
    }
    first_job_id = first_job_map.get(env)
    second_job_id = second_job_map.get(env)
    if not first_job_id or not second_job_id:
        raise AssertionError(f"线下还款暂不支持当前环境:{env}")

    first_res = xxl_job_trigger(first_job_id, env=env)
    if progress_callback:
        progress_callback(f"触发线下还款订单处理job:{first_job_id}，结果:{first_res}")
    if first_res != 'pass':
        return False, f"触发job {first_job_id}失败"

    time.sleep(3)
    second_res = xxl_job_trigger(second_job_id, env=env)
    if progress_callback:
        progress_callback(f"触发线下还款批次处理job:{second_job_id}，结果:{second_res}")
    if second_res != 'pass':
        return False, f"触发job {second_job_id}失败"
    return True, 'pass'


def _query_offline_repay_batch(loan_no, env):
    sql = f"select * from lcs.bm_offline_repay_batch where loan_no = '{loan_no}' order by id desc limit 1;"
    result = db_conn(env).select_one(sql)
    return (result or {}).get('data'), result


def _query_plan_rpy_flag(loan_no, terms, env):
    sql = f"select rpy_flag from lcs.ln_plan where loan_no = '{loan_no}' and term = '{terms}';"
    result = db_conn(env).select_one(sql)
    data = (result or {}).get('data') or {}
    return str(data.get('rpy_flag')) if data.get('rpy_flag') is not None else None, result


def _poll_offline_repay_plan_settled(loan_no, terms, env, timeout_seconds=180, interval_seconds=30,
                                     progress_callback=None):
    start_time = time.time()
    round_no = 0
    last_flag = None
    while True:
        round_no += 1
        trigger_res = _trigger_repay_sync_job(env)
        if progress_callback:
            progress_callback(f"第{round_no}次触发107结果:{trigger_res}")
        if trigger_res != 'pass':
            return False, f"触发107失败，最后rpy_flag:{last_flag}"

        flag, raw_result = _query_plan_rpy_flag(loan_no, terms, env)
        last_flag = flag
        elapsed_time = int(time.time() - start_time)
        if progress_callback:
            progress_callback(f"第{round_no}次查询还款计划结清状态，rpy_flag:{flag}，已耗时:{elapsed_time}秒")
        web_logger.info(f"线下还款轮询ln_plan状态，loan_no:{loan_no}, terms:{terms}, result:{raw_result}")

        if flag == '2':
            return True, flag
        if time.time() - start_time >= timeout_seconds:
            return False, f"time_out:{last_flag}"
        time.sleep(interval_seconds)


def offline_oak_pay_order(mobile, loan_no, terms, env='BM_SIT', pay_channel='alipay_wap', timeout_seconds=180,
                          interval_seconds=30, progress_callback=None):
    """
    线下还款流程：试算 -> oakPayOrder -> 修改订单成功 -> 执行线下还款job -> 107同步 -> 校验当期结清。
    """
    steps = []

    def log_step(message):
        _log_step(steps, message, progress_callback)

    if not mobile:
        raise AssertionError('缺少 mobile')
    if not loan_no:
        raise AssertionError('缺少 loan_no')
    if not terms:
        raise AssertionError('缺少 terms')

    env = (env or 'BM_SIT').upper()
    terms = str(terms)
    log_step(f"开始线下还款流程，loan_no:{loan_no}，terms:{terms}，env:{env}")

    try:
        loan_req_no = _query_loan_req_no(loan_no, env)
        log_step(f"使用上游传入mobile:{mobile}，查询到loanReqNo:{loan_req_no}")

        h5 = H5Api(mobile=mobile, env=env, scene='REPAY')
        h5.login()
        log_step('H5登录成功，开始线下还款试算')

        trial_data = h5.build_repay_trial_data(
            loan_req_no=loan_req_no,
            loan_no=loan_no,
            terms=terms,
            repay_type='SINGLE',
        )
        trial_res = _to_dict_response(h5.repay_trial(data=trial_data))
        if str((trial_res or {}).get('flag')) == 'F':
            log_step(f"还款试算失败:{trial_res}")
            return {"success": False, "code": "offline_repay_trial_fail", "message": "线下还款部分异常：还款试算失败",
                    "steps": steps, "trial": trial_res}
        total_amount = _extract_total_amount_from_trial(trial_res)
        log_step(f"试算成功，totalAmount:{total_amount}")

        order_data = h5.build_oak_pay_order_data(
            loan_no=loan_no,
            terms=terms,
            total_amount=total_amount,
            pay_channel=pay_channel,
        )
        order_res = _to_dict_response(h5.oak_pay_order(data=order_data))
        log_step("oakPayOrder请求完成")
        if str((order_res or {}).get('flag')) == 'F':
            return {"success": False, "code": "oak_pay_order_fail", "message": "线下还款部分异常：oakPayOrder请求失败",
                    "steps": steps, "trial": trial_res, "oakPayOrder": order_res}

        order_status, order_status_raw = _query_vip_loan_order_status(loan_no, env)
        log_step(f"查询vip_loan_order状态:{order_status}")
        if order_status != 'init':
            return {"success": False, "code": "vip_order_status_not_init",
                    "message": "线下还款部分异常：订单状态不是init", "steps": steps,
                    "orderStatusResult": order_status_raw}

        update_order_res = _update_vip_loan_order_success(loan_no, env)
        log_step("vip_loan_order为success")
        update_status, update_status_raw = _query_vip_loan_order_status(loan_no, env)
        if update_status != 'success':
            return {"success": False, "code": "vip_order_update_fail", "message": "线下还款部分异常：订单状态修改失败",
                    "steps": steps, "updateResult": update_order_res, "orderStatusResult": update_status_raw}

        job_success, job_msg = _trigger_offline_repay_prepare_jobs(env, progress_callback=log_step)
        if not job_success:
            return {"success": False, "code": "offline_repay_job_fail", "message": f"线下还款部分异常：{job_msg}",
                    "steps": steps}
        time.sleep(5)
        batch_data, batch_raw = _query_offline_repay_batch(loan_no, env)
        web_logger.info(f"查询线下还款批次记录，loan_no:{loan_no}, result:{batch_raw}")
        log_step(f"查询线下还款批次记录")
        if not batch_data:
            return {"success": False, "code": "offline_repay_batch_not_found",
                    "message": "线下还款部分异常：bm_offline_repay_batch数据未正常写入", "steps": steps,
                    "batchResult": batch_raw}

        settled, settle_msg = _poll_offline_repay_plan_settled(
            loan_no,
            terms,
            env,
            timeout_seconds=timeout_seconds,
            interval_seconds=interval_seconds,
            progress_callback=log_step,
        )
        if not settled:
            return {"success": False, "code": "offline_repay_plan_not_settled",
                    "message": f"线下还款部分异常：当期未结清，结果:{settle_msg}", "steps": steps}

        log_step('线下还款流程完成，当期已结清')
        return {
            "success": True,
            "code": "offline_repay_success",
            "message": "线下还款成功，当期已结清",
            "steps": steps,
            "loanNo": loan_no,
            "terms": terms,
            "totalAmount": total_amount,
            "trial": trial_res,
            "oakPayOrder": order_res,
            "offlineBatch": batch_data,
        }
    except Exception as e:
        log_step(f"线下还款流程异常:{e}")
        return {"success": False, "code": "offline_repay_exception", "message": f"线下还款部分异常：{e}", "steps": steps}
