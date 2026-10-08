#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# myproject/api.py
import json, sys
from decimal import Decimal
from queue import Queue, Empty
import threading

from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from api.app.loan_bill import LoanBill, RepayLoan, LoanCompensationFlow
from djangoWebTools.tools.bm_tools.ask_xxl import xxl_job_trigger
from djangoWebTools.tools.bm_tools.credit_apply import credit_apply, query_risk_status
from djangoWebTools.tools.bm_tools.credit_order import credit_order, query_order, fund_plan_mock
from djangoWebTools.tools.bm_tools.repay_order import repay_order, trail_order, query_repay_order
from djangoWebTools.tools.bm_tools.repay_result import query_repay_result
from djangoWebTools.tools.bm_tools.offline_oak_pay import offline_oak_pay_order
from djangoWebTools.tools.query_user_info import query_user_info_by_mobile, generate_random_user_info, random_user_info
from api.app.h5_api import H5Api
from api.app.h5_scene import H5SceneService
from tests.interface.coupon_send import update_excel_and_send, _get_coupon_code, query_coupon_arrival


@csrf_exempt
def query_user(request):
    # 查询用户号user_no

    if request.method == 'POST':
        # 获取请求参数
        data = json.loads(request.body)
        print(f"query_user::data=={data}")
        env = data.get('env')
        mobile = data.get('mobile').replace(" ", "")
        user_no = data.get('user_no')
        if not mobile and not user_no:
            return JsonResponse({'error': '手机号和user_no不能同时为空'})
        res = query_user_info_by_mobile(env, mobile, user_no)
        return JsonResponse(res, charset='utf-8')
    return JsonResponse({'error': '无效的请求'})


@csrf_exempt
def init_plan(request):
    data = json.loads(request.body)
    loan_no = data.get('loan_no')
    overdue_type = (data.get('overdue_type') or 'N').upper()
    day = data.get('day')
    bill_day = bool(data.get('bill_day'))
    env = data.get('env')

    if not loan_no:
        return JsonResponse({"success": 3, "res": "缺少 loan_no"}, charset='utf-8')
    if overdue_type not in ['Y', 'N']:
        return JsonResponse({"success": 4, "res": "overdue_type 仅支持 Y 或 N"}, charset='utf-8')
    if overdue_type == 'Y' and (day is None or str(day).strip() == ''):
        return JsonResponse({"success": 3, "res": "逾期场景缺少 day"}, charset='utf-8')
    if overdue_type == 'N' and not bill_day and (day is None or str(day).strip() == ''):
        return JsonResponse({"success": 3, "res": "非逾期场景缺少 day"}, charset='utf-8')

    try:
        res = LoanBill(loan_no=loan_no, overdue_type=overdue_type, day=day, bill_day=bill_day, env=env).init_plan_1()
    except AssertionError as e:
        return JsonResponse({"success": 5, "res": str(e)}, charset='utf-8')

    if res[0] == 'S':
        return JsonResponse({"success": 0, "res": "订单初始化成功,计息计费中"}, charset='utf-8')
    elif res[0] == 'F':
        return JsonResponse({"success": 1, "res": '试算接口超时，使用下方工具，手动触发计息'}, charset='utf-8')
    else:
        return JsonResponse({"success": 2, "res": "订单初始化异常，检查数据没有问题，使用下方工具，手动触发计息"},
                            charset='utf-8')


@csrf_exempt
def repay_loan(request):
    data = json.loads(request.body)
    loan_no = data.get('loan_no')
    repay_all_loan = data.get('repay_all_loan')
    env = data.get('env')
    repay_plan = RepayLoan(loan_no, env)
    if repay_all_loan is False or repay_all_loan is None:
        if repay_plan.repay_plan() == "成功":
            return JsonResponse({"success": 0, "res": "当前单笔借据全款还款成功"}, charset='utf-8')
        else:
            return JsonResponse({"success": 1, "res": "当前单笔借据还款失败"}, charset='utf-8')
    else:
        if repay_plan.repay_all() == "成功":
            return JsonResponse({"success": 10, "res": "用户下所有借据全额还款成功"}, charset='utf-8')
        else:
            return JsonResponse({"success": 20, "res": "用户下所有借据还款失败"}, charset='utf-8')


@csrf_exempt
def trigger_xxl_job(request):
    from_data = json.loads(request.body)
    job_id = from_data.get('job_id')
    executor_param = from_data.get('executor_param')
    env = from_data.get('env')
    if xxl_job_trigger(job_id, executor_param, env) == 'pass':
        return JsonResponse({"success": 0, "res": "触发成功"}, charset='utf-8')
    else:
        return JsonResponse({"success": -1, "res": "触发失败"}, charset='utf-8')


@csrf_exempt
def loan_compensation(request):
    data = json.loads(request.body)
    loan_no = data.get('loan_no')
    fund_code = data.get('fund_code')
    number = data.get('number')
    env = data.get('env')

    if not loan_no:
        return JsonResponse({"success": 3, "res": "缺少 loan_no"}, charset='utf-8')
    if not fund_code:
        return JsonResponse({"success": 4, "res": "缺少 fund_code"}, charset='utf-8')

    try:
        flow = LoanCompensationFlow(loan_no=loan_no, fund_code=fund_code, number=number, env=env)
        config = flow.load_compensation_config()
        effective_number = flow.calculate_effective_number()
        max_day = flow.calculate_max_day()
        init_result = flow.init_overdue_for_compensation()
        if not init_result or init_result[0] != 'S':
            return JsonResponse({
                "success": 1,
                "res": "订单初始化失败或计息计费未完成",
                "data": {
                    "config": config,
                    "effective_number": effective_number,
                    "max_day": max_day,
                }
            }, charset='utf-8')

        flow.wait_until_overdue_days_ready()
        round_results = flow.execute_compensation_rounds()
        summary = flow.summary()
        summary['round_results'] = round_results
        return JsonResponse({"success": 0, "res": "代偿流程完成", "data": summary}, charset='utf-8')
    except TimeoutError as e:
        return JsonResponse({"success": 2, "res": str(e)}, charset='utf-8')
    except AssertionError as e:
        return JsonResponse({"success": 5, "res": str(e)}, charset='utf-8')
    except Exception as e:
        return JsonResponse({"success": 9, "res": f"代偿流程异常: {e}"}, charset='utf-8')


@csrf_exempt
def bm_credit_apply(request):
    data = json.loads(request.body)
    mobile = data.get('mobile')
    name = data.get('name')
    id_card = data.get('id_card')
    env = data.get('env').upper()
    channel = data.get('channel')
    risk_type = data.get('risk_type')
    credit_apply_type = data.get('credit_apply')
    count = data.get('count', 1)

    # 校验count参数
    try:
        count = int(count)
    except (ValueError, TypeError):
        count = 1
    count = max(1, min(count, 10))

    # 批量模式（count > 1）：全随机生成，SSE流式输出
    if count > 1:
        message_queue = Queue()

        def sse_payload(event_type, payload):
            return f"data: {json.dumps({'type': event_type, **payload}, ensure_ascii=False)}\n\n"

        def worker():
            try:
                from concurrent.futures import ThreadPoolExecutor, as_completed

                # ===== Phase 1: 并发发起 N 个授信申请 =====
                message_queue.put(('progress', {'message': f'开始批量发起 {count} 个授信申请，渠道：{channel}，风险类型：{risk_type}'}))

                def do_apply(idx):
                    """单个授信申请"""
                    res = credit_apply(None, None, None, env, channel=channel, risk_type=risk_type,
                                       credit_apply=credit_apply_type)
                    return idx, res

                apply_results = []
                with ThreadPoolExecutor(max_workers=min(count, 5)) as executor:
                    futures = {executor.submit(do_apply, i): i for i in range(count)}
                    for future in as_completed(futures):
                        idx, res = future.result()
                        apply_results.append((idx, res))
                        if isinstance(res, dict) and res.get('code') == 200:
                            message_queue.put(('progress',
                                               {'message': f'[{len(apply_results)}/{count}] 用户 {res.get("mobile", "N/A")} 授信申请已提交...'}))
                        else:
                            err_msg = res.get('res', str(res)) if isinstance(res, dict) else str(res)
                            message_queue.put(('progress',
                                               {'message': f'[{len(apply_results)}/{count}] 授信申请发起失败: {err_msg}'}))

                # 按 idx 排序
                apply_results.sort(key=lambda x: x[0])

                # ===== Phase 2: 并发轮询 N 个授信状态 =====
                message_queue.put(('progress', {'message': f'全部 {count} 个授信申请已提交，开始并发查询授信状态...'}))

                passed = 0
                rejected = 0
                timeout = 0
                empty = 0
                apply_fail = 0
                crash_fail = 0
                details = []

                def do_poll(idx, apply_result):
                    """单个状态轮询"""
                    if isinstance(apply_result, dict) and apply_result.get('code') == 200:
                        bm_user_no = apply_result['user_no']
                        bm_mobile = apply_result['mobile']
                        status = query_risk_status(bm_user_no, env)
                        return idx, {
                            'user_no': bm_user_no,
                            'mobile': bm_mobile,
                            'status': status,
                            'res': apply_result.get('res', ''),
                        }
                    else:
                        err_res = apply_result.get('res', str(apply_result)) if isinstance(apply_result, dict) else str(apply_result)
                        return idx, {
                            'user_no': None,
                            'mobile': None,
                            'status': 'apply_fail' if (
                                        isinstance(apply_result, dict) and apply_result.get('code') == 500) else 'crash_fail',
                            'res': err_res,
                        }

                with ThreadPoolExecutor(max_workers=min(count, 5)) as executor:
                    futures = {executor.submit(do_poll, idx, res): idx for idx, res in apply_results}
                    for future in as_completed(futures):
                        idx, detail = future.result()
                        details.append((idx, detail))
                        if detail['status'] == 'PS':
                            passed += 1
                        elif detail['status'] == 'RJ':
                            rejected += 1
                        elif detail['status'] == 'timeout':
                            timeout += 1
                        elif detail['status'] == 'false':
                            empty += 1
                        elif detail['status'] == 'apply_fail':
                            apply_fail += 1
                        else:
                            crash_fail += 1
                        message_queue.put(('progress',
                                           {'message': f'状态轮询中: 通过{passed} | 拒绝{rejected} | 超时{timeout} | 其他{empty + apply_fail + crash_fail}'}))

                # 按 idx 排序详情
                details.sort(key=lambda x: x[0])
                ordered_details = [d for _, d in details]

                summary = (
                    f'批量授信完成：共发起 {count} 个用户，'
                    f'授信通过 {passed} 个，授信拒绝 {rejected} 个，'
                    f'查询超时 {timeout} 个，结果为空 {empty} 个，'
                    f'发起失败 {apply_fail} 个，撞库失败 {crash_fail} 个'
                )
                message_queue.put(('done', {
                    'result': {
                        'success': '批量授信完成',
                        'res': summary,
                        'data': {
                            'total': count,
                            'passed': passed,
                            'rejected': rejected,
                            'timeout': timeout,
                            'empty': empty,
                            'apply_fail': apply_fail,
                            'crash_fail': crash_fail,
                            'details': ordered_details,
                        }
                    }
                }))
            except Exception as e:
                message_queue.put(('error', {'message': f'批量授信流程异常: {e}'}))
            finally:
                message_queue.put(('close', {}))

        def event_stream():
            threading.Thread(target=worker, daemon=True).start()
            while True:
                try:
                    event_type, payload = message_queue.get(timeout=15)
                except Empty:
                    yield sse_payload('progress', {'message': '流程执行中，请继续等待...'})
                    continue
                if event_type == 'close':
                    break
                yield sse_payload(event_type, payload)

        response = StreamingHttpResponse(event_stream(), content_type='text/event-stream; charset=utf-8')
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        return response

    # 单用户模式（count == 1）
    apply_status = credit_apply(mobile, name, id_card, env, channel=channel, risk_type=risk_type,
                                credit_apply=credit_apply_type)

    # 撞库失败返回字符串，优先判断
    if apply_status == '撞库失败':
        return JsonResponse({"success": 2, "res": "准入检查失败，检查撞库数据"}, charset='utf-8')

    if apply_status['code'] == 200:
        bm_user_no = apply_status['user_no']
        bm_mobile = apply_status['mobile']
        risk_status = query_risk_status(bm_user_no, env)
        if risk_status == 'PS':
            return JsonResponse({"success": "授信通过",  "res": f"用户user_no：{bm_user_no}，手机号：{bm_mobile},{apply_status['res']}"},
                                charset='utf-8')
        elif risk_status == 'RJ':
            return JsonResponse({"success": "授信拒绝", "res": f"用户user_no：{bm_user_no}，手机号：{bm_mobile},{apply_status['res']}"},
                                charset='utf-8')
        elif risk_status == 'timeout':
            return JsonResponse({"success": "查询超时",  "res": f"用户user_no：{bm_user_no}，手机号：{bm_mobile},{apply_status['res']}"},
                                charset='utf-8')
        elif risk_status == 'false':
            return JsonResponse({"success": '结果为空',
                                  "res": f"用户user_no：{bm_user_no}，手机号：{bm_mobile},{apply_status['res']}"},
                                charset='utf-8')
    elif apply_status['code'] == 500:
        return JsonResponse({"success": 1, "res": f"授信申请发起异常，检查数据,{apply_status['res']}"},
                            charset='utf-8')


@csrf_exempt
def bm_credit_order(request):
    data = json.loads(request.body)
    mobile = data.get('mobile')
    term = data.get('Term')
    amt = data.get('amt')
    env = data.get('env').upper()
    channel = data.get('channel')
    is_privilege = data.get('isPrivilege')
    profit_type = data.get('profitType')
    order_status = credit_order(mobile, is_privilege, profit_type, term, amt, env, channel=channel)
    if order_status == 'apply_fail':
        return JsonResponse({"success": 3, "res": "订单提交失败，授信数据查询异常"}, charset='utf-8')
    elif order_status == '二次创建成功A':
        return JsonResponse({"success": 1, "res": "二次验证绑卡验证创建订单成功"}, charset='utf-8')
    elif order_status == '二次创建成功B':
        return JsonResponse(
            {"success": 4, "res": "二次绑卡创单成功，但是mock修改失败，需要手动查询放款结果再次修改资方还款计划mock"},
            charset='utf-8')
    elif order_status == '订单创建成功':
        return JsonResponse({"success": 2, "res": "订单创建成功"}, charset='utf-8')
    elif order_status == '该用户已开通特权还款':
        return JsonResponse({"success": 5, "res": "已有未废单的权益，不支持再次购买"}, charset='utf-8')
    elif order_status == '合同获取失败':
        return JsonResponse({"success": 6, "res": "合同获取失败"}, charset='utf-8')
    else:
        return JsonResponse({"success": 0, "res": "订单提交失败，检查配置"}, charset='utf-8')


def _build_query_order_response_data(order_status):
    response_mapping = {
        'fail': {"success": 'fail', "res": "最后一笔订单不是放款中订单"},
        'fund_fail': {"success": 'fund_fail', "res": "借据进入DJ，资方放款失败或待重新匹配"},
        'lcs_fail': {"success": 'lcs_fail', "res": "lps脚本执行完成，lcs脚本待执行，可再次请求重试"},
        'lcs_success': {"success": 'lcs_success', "res": "lcs脚本执行完成，lps脚本执行完成，五分钟未放款成功，可重复执行"},
        'order_ds': {"success": 200, "res": "最新一笔订单放款成功"},
        'job_217_fail': {"success": 'job_217_fail', "res": "预处理放款任务执行失败"},
        'lps_job_fail': {"success": 'lps_job_fail', "res": "LPS放款脚本执行失败"},
        'job_113_fail': {"success": 'job_113_fail', "res": "LCS任务113执行失败"},
        'job_115_fail': {"success": 'job_115_fail', "res": "LCS任务115执行失败"},
        'aps_job_fail': {"success": 'aps_job_fail', "res": "APS放款脚本执行失败"},
        '风险审批异常': {"success": 'risk_timeout', "res": "风险审批状态未在预期时间内变为PS"},
        '放款主流程状态轮询超时': {"success": 'loan_poll_timeout', "res": "放款主流程状态轮询超时"},
        'APR到DR轮询超时': {"success": 'apr_to_dr_timeout', "res": "APR到DR状态轮询超时"},
        'LCS放款结果轮询超时': {"success": 'lcs_timeout', "res": "LCS放款结果轮询超时"},
        'APS放款结果轮询超时': {"success": 'aps_timeout', "res": "APS放款结果轮询超时"},
    }
    return response_mapping.get(order_status, {"success": -1, "res": f"订单查询失败，检查配置，执行结果:{order_status}"})


@csrf_exempt
def bm_query_order(request):
    data = json.loads(request.body)
    print(f"本次请求的参数{data}")
    mobile = data.get('mobile')
    env = data.get('env').upper()
    channel = data.get('channel')
    loan_query_status = data.get('loanQueryStatus') or data.get('loan_query_status')
    fund_code = data.get('fundCode') or data.get('fund_code')
    message_queue = Queue()

    def sse_payload(event_type, payload):
        return f"data: {json.dumps({'type': event_type, **payload}, ensure_ascii=False)}\n\n"

    def worker():
        try:
            order_status = query_order(
                mobile,
                env,
                channel=channel,
                loan_query_status=loan_query_status,
                fund_code=fund_code,
                progress_callback=lambda message: message_queue.put(('progress', {'message': message})),
            )
            message_queue.put(('done', {'result': _build_query_order_response_data(order_status)}))
        except Exception as e:
            message_queue.put(('error', {'message': f'查询订单放款流程异常:{e}'}))
        finally:
            message_queue.put(('close', {}))

    def event_stream():
        threading.Thread(target=worker, daemon=True).start()
        while True:
            try:
                event_type, payload = message_queue.get(timeout=15)
            except Empty:
                yield sse_payload('progress', {'message': '流程执行中，请继续等待...'})
                continue

            if event_type == 'close':
                break
            yield sse_payload(event_type, payload)

    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream; charset=utf-8')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response


def _build_query_repay_result_response_data(query_status):
    if query_status == 'repay_processing_not_found':
        return {"success": 'repay_processing_not_found', "res": '未查询到还款记录'}
    if query_status == 'repay_not_processing':
        return {"success": 'repay_not_processing', "res": '当前借据无还款中流程'}
    if query_status == 'repay_success':
        return {"success": 'repay_success', "res": '还款结果已达到成功状态03'}
    if query_status == 'repay_success_offline_no_term':
        return {"success": 'repay_success_offline_no_term', "res": '线下还款需要指定期数'}
    if str(query_status).startswith('repay_success_offline_fail:'):
        return {"success": 'repay_success_offline_fail', "res": f"线下还款失败:{query_status.split(':', 1)[1]}"}
    if query_status == 'repay_fail':
        return {"success": 'repay_fail', "res": '还款结果已达到失败状态04'}
    if query_status == 'repay_partial_success':
        return {"success": 'repay_partial_success', "res": '还款结果已达到部分成功状态05'}
    if query_status == 'repay_fail_offer_not_found':
        return {"success": 'repay_fail_offer_not_found', "res": '未查询到可处理的FUND处理中报盘记录'}
    if query_status == 'repay_fail_inner_update_fail':
        return {"success": 'repay_fail_inner_update_fail', "res": 'INNER渠道修正SQL执行失败'}
    if query_status == 'repay_partial_success_not_supported_single_offer':
        return {"success": 'repay_partial_success_not_supported_single_offer', "res": '单笔完成扣款，不支持部分还款'}
    if query_status == 'repay_partial_success_not_supported_compensate':
        return {"success": 'repay_partial_success_not_supported_compensate', "res": '代偿后不支持部分还款'}
    if query_status == 'repay_partial_success_no_processing_records':
        return {"success": 'repay_partial_success_no_processing_records', "res": '未查询到还款中的tran_proc_rp_no'}
    if query_status == 'repay_partial_success_fund_timeout':
        return {"success": 'repay_partial_success_fund_timeout', "res": '等待FUND变为03超时'}
    if query_status == 'repay_partial_success_no_inner_offers':
        return {"success": 'repay_partial_success_no_inner_offers', "res": '未查询到INNER渠道offer_req_no'}
    if query_status == 'repay_partial_success_offer_status_mismatch':
        return {"success": 'repay_partial_success_offer_status_mismatch', "res": '107执行后未满足FUND=03且INNER=02的部分成功条件'}
    if query_status == 'partial_success_sql_update_fail':
        return {"success": 'partial_success_sql_update_fail', "res": '部分成功修正SQL执行失败'}
    if str(query_status).startswith('repay_success_timeout:'):
        return {"success": 'repay_success_timeout', "res": f"还款成功场景轮询超时，最终状态:{query_status.split(':', 1)[1]}"}
    if str(query_status).startswith('repay_fail_timeout:'):
        return {"success": 'repay_fail_timeout', "res": f"还款失败场景轮询超时，最终状态:{query_status.split(':', 1)[1]}"}
    if str(query_status).startswith('repay_partial_success_timeout:'):
        return {"success": 'repay_partial_success_timeout', "res": f"部分成功场景轮询超时，最终状态:{query_status.split(':', 1)[1]}"}
    return {"success": -1, "res": f"还款结果查询失败，执行结果:{query_status}"}


@csrf_exempt
def bm_query_repay_result(request):
    data = json.loads(request.body)
    loan_no = data.get('loan_no')
    mobile = data.get('mobile')
    env = data.get('env').upper()
    channel = data.get('channel')
    repay_query_status = data.get('repayQueryStatus') or data.get('repay_query_status')
    term = data.get('term')
    message_queue = Queue()

    def sse_payload(event_type, payload):
        return f"data: {json.dumps({'type': event_type, **payload}, ensure_ascii=False)}\n\n"

    def worker():
        try:
            result_status = query_repay_result(
                mobile,
                loan_no,
                repay_query_status,
                env=env,
                channel=channel,
                term=term,
                progress_callback=lambda message: message_queue.put(('progress', {'message': message})),
            )
            message_queue.put(('done', {'result': _build_query_repay_result_response_data(result_status)}))
        except Exception as e:
            message_queue.put(('error', {'message': f'查询还款结果流程异常:{e}'}) )
        finally:
            message_queue.put(('close', {}))

    def event_stream():
        threading.Thread(target=worker, daemon=True).start()
        while True:
            try:
                event_type, payload = message_queue.get(timeout=15)
            except Empty:
                yield sse_payload('progress', {'message': '流程执行中，请继续等待...'})
                continue

            if event_type == 'close':
                break
            yield sse_payload(event_type, payload)

    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream; charset=utf-8')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response


@csrf_exempt
def bm_repay_order(request):
    data = json.loads(request.body)
    loan_no = data.get('loan_no')
    trial_type = data.get('repay_type')
    env = data.get('env').upper()
    channel = data.get('channel')
    repay_status = repay_order(loan_no, trial_type, env, channel)
    if repay_status['code'] == 200:
        return JsonResponse({"success": 0, "res": f"还款发起成功，发起结果{repay_status}"}, charset='utf-8')
    elif repay_status['code'] == 201:
        return JsonResponse({"success": 1, "res": f"还款试算发生异常，检查数据{repay_status}"},
                            charset='utf-8')
    elif repay_status['code'] == 202:
        return JsonResponse({"success": 2, "res": f"还款发起异常，检查数据{repay_status}"},
                            charset='utf-8')
    else:
        return JsonResponse({"success": 3, "res": repay_status}, charset='utf-8')


@csrf_exempt
def bm_query_repay_order(request):
    # 使用还款申请接口，返回的流水号查询还款状态
    data = json.loads(request.body)
    repay_req_no = data.get('repay_req_no')
    env = data.get('env').upper()
    channel = data.get('channel')
    repay_status = query_repay_order(repay_req_no, env, channel)
    return JsonResponse({"success": 0, "res": repay_status}, charset='utf-8')


@csrf_exempt
def bm_repay_trail_order(request):
    data = json.loads(request.body)
    loan_no = data.get('loan_no')
    trial_type = data.get('repay_type')
    env = data.get('env').upper()
    channel = data.get('channel')
    trial_status = trail_order(loan_no, trial_type, env, channel)
    return JsonResponse({"success": 0, "res": f"试算发起成功，发起结果{trial_status}"}, charset='utf-8')


@csrf_exempt
def bm_update_mock(request):
    data = json.loads(request.body)
    env = data.get('env').upper()
    amt = data.get('amt')
    term = data.get('period')
    fund_code = data.get('fund_code')
    cust_no = data.get('cust_no')
    is_date = data.get('is_date')
    update_status = fund_plan_mock(env, amt, term, cust_no, is_date, fund_code)
    if update_status == 'mock_success':
        return JsonResponse({"success": 0, "res": "mock还款数据更新成功"}, charset='utf-8')
    elif update_status == 'date_false':
        return JsonResponse({"success": 2, "res": "is_date字段传参错误"}, charset='utf-8')
    else:
        return JsonResponse({"success": 1, "res": "mock还款数据更新失败，检查配置"}, charset='utf-8')

        # @csrf_exempt
        # def bm_easy_mock_data(request):
        #     # 还款前需要拉取资方还款计划与我方还款计划比对，确保还款计划期数一致
        #     data = json.loads(request.body)
        #     amt = data.get('amt')
        #     term = data.get('term')
        #     env = data.get('env').upper()
        #     status = fund_plan_mock(env, amt, term)
        #     if status == 'mock_success':
        #         return JsonResponse({"success": 0, "res": "mock还款数据更新成功"}, charset='utf-8')
        #     else:
        #         return JsonResponse({"success": -1, "res": "mock还款数据更新失败，检查配置"}, charset='utf-8')


@csrf_exempt
def bm_get_h5_url(request):
    data = json.loads(request.body)
    env = data.get('env').upper()
    mobile = data.get('mobile')
    scene = data.get('scene')
    h5_url = H5Api(mobile, scene, env).request_url()
    if h5_url is None:
        return JsonResponse({"success": -1, "res": "获取h5链接失败，检查配置"}, charset='utf-8')
    return JsonResponse({"success": 0, "res": h5_url}, charset='utf-8')


@csrf_exempt
def h5_bind_card_scene(request):
    if request.method != 'POST':
        return JsonResponse({'error': '无效的请求'})

    data = json.loads(request.body or '{}')
    env = data.get('env')
    mobile = data.get('mobile')
    bind_scene = (data.get('bindScene') or 'DRAW').upper()
    card_no = data.get('cardNo')
    payChannel = data.get('payChannel')

    if not env or not mobile:
        return JsonResponse({'error': '缺少 env 或 mobile'}, status=200)

    if bind_scene not in ['DRAW', 'REPAY']:
        return JsonResponse({'error': 'bindScene 仅支持 DRAW 或 REPAY'}, status=200)

    service = H5SceneService(mobile=mobile, env=env)
    result = service.run_bind_card_scene(
        bind_scene=bind_scene,
        card_no=card_no,
        pay_channel=payChannel
    )
    return JsonResponse({"success": 0, "data": result}, charset='utf-8')


@csrf_exempt
def h5_draw_submit_scene(request):
    if request.method != 'POST':
        return JsonResponse({'error': '无效的请求'})

    data = json.loads(request.body or '{}')
    env = data.get('env')
    mobile = data.get('mobile')
    loan_amt = data.get('amt')
    loan_term = data.get('term')
    is_privilege_process = (data.get('isPrivilegeProcess') or 'N').upper()
    is_continuous_monthly = (data.get('isContinuousMonthly') or 'Y').upper()
    loan_purpose_desc = data.get('loanPurposeDesc') or '购物'
    loan_purpose_code = data.get('loanPurposeCode') or '01'

    if not env or not mobile:
        return JsonResponse({'error': '缺少 env 或 mobile'}, status=200)
    if loan_amt is None or loan_term is None:
        return JsonResponse({'error': '缺少 amt 或 term'}, status=200)
    if is_privilege_process not in ['N', 'Y']:
        return JsonResponse({'error': 'isPrivilegeProcess 仅支持 N 或 Y'}, status=200)
    if is_continuous_monthly not in ['N', 'Y']:
        return JsonResponse({'error': 'isContinuousMonthly 仅支持 N 或 Y'}, status=200)

    def wrapped_stream():
        message_queue = Queue()

        def emit(event_type, payload):
            return f"data: {json.dumps({'type': event_type, **payload}, ensure_ascii=False)}\n\n"

        def worker():
            try:
                service = H5SceneService(mobile=mobile, env=env)
                result = service.run_draw_submit_scene(
                    loan_amt=loan_amt,
                    loan_term=loan_term,
                    is_privilege_process=is_privilege_process,
                    is_continuous_monthly=is_continuous_monthly,
                    loan_purpose_desc=loan_purpose_desc,
                    loan_purpose_code=loan_purpose_code,
                    progress_callback=lambda message: message_queue.put(('progress', {'message': message})),
                )
                message_queue.put(('done', {'result': result}))
            except Exception as e:
                message_queue.put(('error', {'message': str(e)}))
            finally:
                message_queue.put(('close', {}))

        threading.Thread(target=worker, daemon=True).start()
        yield emit('progress', {'message': '已收到请求，开始执行 H5 借款流程'})

        while True:
            try:
                event_type, payload = message_queue.get(timeout=1)
            except Empty:
                continue
            if event_type == 'close':
                break
            yield emit(event_type, payload)

    response = StreamingHttpResponse(wrapped_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response


@csrf_exempt
def h5_repay_scene(request):
    if request.method != 'POST':
        return JsonResponse({'error': '无效的请求'})

    data = json.loads(request.body or '{}')
    env = data.get('env')
    mobile = data.get('mobile')
    loan_no = data.get('loanNo')
    repay_type = (data.get('repayType') or 'SINGLE').upper()
    use_coupon = data.get('useCoupon') in [True, 'true', 'True', 1]

    if not env or not mobile:
        return JsonResponse({'error': '缺少 env 或 mobile'}, status=200)
    if not loan_no:
        return JsonResponse({'error': '缺少 loanNo'}, status=200)
    if repay_type not in ['SINGLE', 'ALL']:
        return JsonResponse({'error': 'repayType 仅支持 SINGLE 或 ALL'}, status=200)

    def wrapped_stream():
        message_queue = Queue()

        def emit(event_type, payload):
            return f"data: {json.dumps({'type': event_type, **payload}, ensure_ascii=False)}\n\n"

        def worker():
            try:
                service = H5SceneService(mobile=mobile, env=env)
                result = service.run_repay_scene(
                    loan_no=loan_no,
                    repay_type=repay_type,
                    use_coupon=use_coupon,
                    progress_callback=lambda message: message_queue.put(('progress', {'message': message})),
                )
                message_queue.put(('done', {'result': result}))
            except Exception as e:
                message_queue.put(('error', {'message': str(e)}))
            finally:
                message_queue.put(('close', {}))

        threading.Thread(target=worker, daemon=True).start()
        yield emit('progress', {'message': '已收到请求，开始执行 H5 还款流程'})

        while True:
            try:
                event_type, payload = message_queue.get(timeout=1)
            except Empty:
                continue
            if event_type == 'close':
                break
            yield emit(event_type, payload)

    response = StreamingHttpResponse(wrapped_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response


@csrf_exempt
def h5_coupon_receive(request):
    if request.method != 'POST':
        return JsonResponse({'error': '无效的请求'}, status=200)

    data = json.loads(request.body or '{}')
    mobile = (data.get('mobile') or '').strip()
    user_no = (data.get('user_no') or '').strip()
    coupon_type = (data.get('couponType') or '').strip().lower()
    env = (data.get('env') or 'BM_SIT').strip()

    if not mobile:
        return JsonResponse({'error': '缺少 mobile'}, status=200)
    if not user_no:
        return JsonResponse({'error': '缺少 user_no'}, status=200)
    if coupon_type not in ['discount', 'fixed']:
        return JsonResponse({'error': 'couponType 仅支持 discount 或 fixed'}, status=200)

    try:
        discount_code, fixed_code = _get_coupon_code(env)
        coupon_code = discount_code if coupon_type == 'discount' else fixed_code

        result = update_excel_and_send(
            user_no=user_no,
            mobile=mobile,
            discount=(coupon_type == 'discount'),
            env=env,
        )
        save_response = result['save_response'].json()
        submit_response = result['submit_response'].json()

        if not query_coupon_arrival(user_no=user_no, coupon_code=coupon_code, env=env):
            return JsonResponse({
                'success': -1,
                'error': '优惠券发放接口已提交，但轮询超时未到账，请手工确认。',
                'coupon_code': coupon_code,
            }, charset='utf-8')

        return JsonResponse({
            'success': 0,
            'res': '领取优惠券已到账',
            'data': {
                'save': save_response,
                'submit': submit_response,
            }
        }, charset='utf-8')
    except Exception as e:
        return JsonResponse({'error': f'领取优惠券失败: {e}'}, status=200)


if __name__ == '__main__':
    print(sys.path)


@csrf_exempt
def bm_offline_oak_pay(request):
    """
    橡树线下还款接口
    
    功能说明:
    - 通过 oakPayOrder 接口发起线下还款
    - 自动执行线下还款批次处理 job
    - 轮询验证当期是否结清
    
    请求参数:
    - mobile: 手机号 (必填)
    - loan_no: 借据号 (必填)
    - terms: 期数 (必填, 1-12)
    - env: 环境 (必填, BM_SIT/DEV)
    
    返回:
    - SSE 流式输出，实时返回执行日志
    - 最终返回成功或失败状态
    """
    # 解析请求参数
    data = json.loads(request.body)
    mobile = data.get('mobile')
    loan_no = data.get('loan_no')
    terms = data.get('terms')
    env = data.get('env', 'BM_SIT').upper()
    
    # 创建消息队列用于线程间通信
    message_queue = Queue()

    def sse_payload(event_type, payload):
        """构造 SSE 格式的数据"""
        def json_serializer(obj):
            """处理特殊类型的 JSON 序列化"""
            from decimal import Decimal
            import datetime
            if isinstance(obj, Decimal):
                return str(obj)
            if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
                return obj.isoformat()
            raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')
        
        return f"data: {json.dumps({'type': event_type, **payload}, ensure_ascii=False, default=json_serializer)}\n\n"

    def worker():
        """后台工作线程，执行线下还款流程"""
        try:
            # 调用线下还款方法
            result = offline_oak_pay_order(
                mobile=mobile,
                loan_no=loan_no,
                terms=terms,
                env=env,
                progress_callback=lambda message: message_queue.put(('progress', {'message': message})),
            )
            
            # 将结果放入队列
            message_queue.put(('done', {'result': result}))
        except Exception as e:
            # 捕获异常并放入队列
            message_queue.put(('error', {'message': f'线下还款流程异常:{e}'}) )
        finally:
            # 标记流结束
            message_queue.put(('close', {}))

    def event_stream():
        """SSE 事件流生成器"""
        # 启动后台工作线程
        threading.Thread(target=worker, daemon=True).start()
        
        while True:
            try:
                # 从队列获取消息，超时 15 秒
                event_type, payload = message_queue.get(timeout=15)
            except Empty:
                # 超时则发送心跳消息
                yield sse_payload('progress', {'message': '流程执行中，请继续等待...'})
                continue

            # 如果是关闭事件，结束流
            if event_type == 'close':
                break
            
            # 发送事件数据
            yield sse_payload(event_type, payload)

    # 返回 SSE 流式响应
    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream; charset=utf-8')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response
