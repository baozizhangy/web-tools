"""
MCP Tools —— 每个 tool 是对现有业务函数的薄包装。
规则：
  1. 只包装，不实现新业务逻辑
  2. 返回值统一包含 success, next_action
  3. 参数使用 Python 类型注解（MCP 自动生成 schema）
"""
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from typing import Optional
from api.app.h5_scene import H5SceneService
from api.app.h5_api import H5Api
from api.app.loan_bill import LoanBill, LoanCompensationFlow
from djangoWebTools.tools.bm_tools.credit_order import query_order, fund_plan_mock
from djangoWebTools.tools.bm_tools.repay_result import query_repay_result
from djangoWebTools.tools.bm_tools.offline_oak_pay import offline_oak_pay_order
from djangoWebTools.tools.bm_tools.ask_xxl import xxl_job_trigger
from djangoWebTools.tools.bm_tools.credit_apply import credit_apply as bm_credit_apply, query_risk_status
from tests.interface.coupon_send import update_excel_and_send, _get_coupon_code, query_coupon_arrival
from config import db_conn


def _query_iou(env: str, loan_req_no: str = "", loan_no: str = "", fields: list = None):
    """通过 loan_req_no(唯一) 或 loan_no 精确查询 lps.bm_iou，返回指定字段的 dict。
    不用 mobile+limit1，避免多借据时查错数据。
    """
    if not fields:
        fields = ['loan_no', 'fund_code', 'loan_req_no', 'loan_amt', 'loan_term', 'loan_state']

    if loan_req_no:
        where = f"loan_req_no = '{loan_req_no}'"
    elif loan_no:
        where = f"loan_no = '{loan_no}'"
    else:
        return {}

    columns = ', '.join(fields)
    sql = f"select {columns} from lps.bm_iou where {where};"
    result = db_conn(env).select_one(sql)
    return (result or {}).get('data') or {}


# ============================================================
# H5 流程类工具
# ============================================================

def h5_get_url(mobile: str, scene: str = "DRAW", env: str = "BM_SIT") -> dict:
    """
    获取 H5 页面链接。用于校验或手动操作。

    前置条件：用户已存在。
    scene: DRAW（借款页）/ REPAY（还款页），默认 DRAW。用户说"借款"→DRAW，"还款"→REPAY。
    返回：H5 URL。
    """
    try:
        url = H5Api(mobile, scene, env).request_url()
        if url is None or url == "fail":
            return {"success": False, "error": "获取 H5 链接失败，检查 mobile 是否已注册", "mobile": mobile}
        return {
            "success": True,
            "url": url,
            "mobile": mobile,
            "scene": scene,
            "next_action": "链接已获取，可直接在浏览器打开进行手动操作。"
        }
    except Exception as e:
        return {"success": False, "error": str(e), "mobile": mobile}


def h5_bind_card(
    mobile: str,
    bind_scene: str = "DRAW",
    env: str = "BM_SIT",
    pay_channel: str = "baofu"
) -> dict:
    """
    H5 绑卡流程。自动登录、查询卡 BIN、提交签约、验证并轮询渠道绑定状态。

    前置条件：用户已存在。
    bind_scene: DRAW（借款绑卡）/ REPAY（还款绑卡），默认 DRAW。用户说"借款"→DRAW，"还款"→REPAY。
    pay_channel: baofu / allinpay / huifu / all，默认 baofu。
    返回：绑卡结果和各渠道状态。
    调用后：绑卡成功后可调用 h5_draw_submit 发起借款。
    """
    try:
        service = H5SceneService(mobile=mobile, env=env)
        result = service.run_bind_card_scene(
            bind_scene=bind_scene,
            pay_channel=pay_channel,
        )
        return {
            "success": result.get("success") == 0,
            "mobile": mobile,
            "bind_scene": bind_scene,
            "card_no": result.get("cardNo"),
            "message": result.get("message"),
            "data": result,
            "next_action": f"绑卡{'成功' if result.get('success') == 0 else '失败'}。"
                           f"成功后调用 h5_draw_submit(mobile='{mobile}', env='{env}') 发起借款。"
        }
    except Exception as e:
        return {"success": False, "error": str(e), "mobile": mobile}


def h5_draw_submit(
    mobile: str,
    amt: int = 3000,
    term: int = 12,
    is_privilege_process: str = "Y",
    is_continuous_monthly: str = "Y",
    env: str = "BM_SIT"
) -> dict:
    """
    发起 H5 借款申请。自动完成：清理旧订单 → 登录 → 预查询 → 绑卡检测（未绑则自动绑）
    → 权益匹配 → 试算 → 提交 → 短信验证。不含放款。

    前置条件：用户已存在且已授信。
    amt: 借款金额 1000-10000，默认 3000。
    term: 期限 3/6/9/12，默认 12。
    is_privilege_process: 是否购买权益 Y/N，默认 Y。
    is_continuous_monthly: 权益是否连续包月 Y/N，默认 Y。Y=OM(连续包月)，N=CM(单次购买)。
    返回：loanReqNo（借款申请号）。

    调用后必须：调用 query_loan_status(mobile, env) 触发放款并等待放款成功。
    """
    try:
        service = H5SceneService(mobile=mobile, env=env)
        result = service.run_draw_submit_scene(
            loan_amt=amt,
            loan_term=term,
            is_privilege_process=is_privilege_process,
            is_continuous_monthly=is_continuous_monthly,
        )
        loan_req_no = result.get("loanReqNo")
        return {
            "success": True,
            "mobile": mobile,
            "loanReqNo": loan_req_no,
            "applyNo": result.get("applyNo"),
            "amt": amt,
            "term": term,
            "is_privilege_process": is_privilege_process,
            "is_continuous_monthly": is_continuous_monthly,
            "steps": result.get("steps"),
            "next_action": f"借款已提交，loanReqNo={loan_req_no}。"
                           f"下一步必须调用 query_loan_status(mobile='{mobile}', env='{env}') "
                           f"触发放款并等待放款成功。"
        }
    except Exception as e:
        return {"success": False, "error": str(e), "mobile": mobile}


def h5_repay(
    mobile: str,
    loan_no: str,
    repay_type: str = "SINGLE",
    use_coupon: bool = False,
    env: str = "BM_SIT"
) -> dict:
    """
    发起 H5 还款申请（仅提交，不放款任务）。自动完成：登录 → 查询 loanReqNo → 账单详情 → 试算 → 提交 → 验证码。

    前置条件：借据已放款成功，账单已初始化（init_bill）。
    repay_type: SINGLE（当期还款）/ ALL（提前结清），默认 SINGLE。用户说"还当期/部分还"→SINGLE，"提前结清/全部还"→ALL。
    use_coupon: 是否使用优惠券，默认 False。优惠券仅在此阶段使用，不影响后续 query_repay_status。

    重要：本 tool 只完成还款申请的提交和短信校验，不会触发放款任务。
    调用后必须继续调用 query_repay_status 以触发 XXL-Job 并轮询还款终态。
    """
    try:
        service = H5SceneService(mobile=mobile, env=env)
        result = service.run_repay_scene(
            loan_no=loan_no,
            repay_type=repay_type,
            use_coupon=use_coupon,
        )
        return {
            "success": result.get("success") == 0,
            "mobile": mobile,
            "loan_no": loan_no,
            "repay_type": repay_type,
            "message": result.get("message"),
            "steps": result.get("steps"),
            "data": result,
            "next_action": f"还款申请已提交，下一步必须调用 query_repay_status(mobile='{mobile}', loan_no='{loan_no}', repay_type='{repay_type}', env='{env}') 触发放款任务并轮询还款终态。"
        }
    except Exception as e:
        return {"success": False, "error": str(e), "mobile": mobile, "loan_no": loan_no}


def offline_oak_pay(
    mobile: str,
    loan_no: str,
    terms: int,
    env: str = "BM_SIT",
    pay_channel: str = "alipay_wap"
) -> dict:
    """
    橡树线下还款。自动完成：试算 → oakPayOrder → 修改订单 → 执行线下还款 job → 107 同步 → 校验当期结清。

    前置条件：借据已放款成功，账单已初始化。
    terms: 还款期数 1-12。
    pay_channel: 支付渠道，默认 alipay_wap。
    返回：线下还款结果。
    """
    try:
        result = offline_oak_pay_order(
            mobile=mobile,
            loan_no=loan_no,
            terms=terms,
            env=env,
            pay_channel=pay_channel,
        )
        return {
            "success": result.get("success") == 0,
            "mobile": mobile,
            "loan_no": loan_no,
            "terms": terms,
            "data": result,
            "next_action": "线下还款流程已完成。"
        }
    except Exception as e:
        return {"success": False, "error": str(e), "mobile": mobile, "loan_no": loan_no}


def coupon_receive(
    mobile: str,
    user_no: str,
    coupon_type: str = "discount",
    env: str = "BM_SIT"
) -> dict:
    """
    为用户领取优惠券。创建优惠券 Excel 任务并提交。

    前置条件：用户已存在且有 user_no。
    coupon_type: discount（折扣券）/ fixed（固定金额券），默认 discount。用户说"折扣券"→discount，"固定券"→fixed。
    返回：优惠券领取结果。
    """
    try:
        discount_code, fixed_code = _get_coupon_code(env)
        coupon_code = discount_code if coupon_type == "discount" else fixed_code

        result = update_excel_and_send(
            user_no=user_no,
            mobile=mobile,
            discount=(coupon_type == "discount"),
            env=env,
        )

        if not query_coupon_arrival(user_no=user_no, coupon_code=coupon_code, env=env):
            return {
                "success": False,
                "mobile": mobile,
                "user_no": user_no,
                "coupon_code": coupon_code,
                "coupon_type": coupon_type,
                "error": "优惠券发放接口已提交，但轮询超时未到账，请手工确认。",
            }

        return {
            "success": True,
            "mobile": mobile,
            "user_no": user_no,
            "coupon_type": coupon_type,
            "save_response": result["save_response"].json(),
            "submit_response": result["submit_response"].json(),
            "next_action": f"优惠券已到账。可在还款时传入 use_coupon=true 使用。"
        }
    except Exception as e:
        return {"success": False, "error": str(e), "mobile": mobile}


# ============================================================
# 数据处理类工具
# ============================================================

def credit_apply(
    mobile: Optional[str] = None,
    name: Optional[str] = None,
    id_card: Optional[str] = None,
    env: str = "BM_SIT",
    channel: str = "lxj",
    risk_type: str = "36",
) -> dict:
    """
    创建借贷测试用户：自动随机生成身份信息 → 撞库 → 风控白名单 → 发起授信 → 等待授信通过。

    前置条件：无（mobile/name/id_card 不传则自动随机生成）。
    risk_type: 36=正常授信, 24=高风险用户。
               自然语言：正常→36, 高风险→24。
    返回：user_no, mobile, name, id_card, risk_status。
    调用后：mobile 可直接用于后续的 h5_bind_card、h5_draw_submit 等操作。
    """
    try:
        result = bm_credit_apply(
            mobile=mobile,
            name=name,
            id_card=id_card,
            env=env,
            channel=channel,
            risk_type=risk_type,
        )
        if isinstance(result, dict) and result.get("code") == 200:
            user_no = result["user_no"]
            mobile_no = result["mobile"]
            # 等待授信审批通过
            risk_status = query_risk_status(user_no=user_no, env=env)
            if risk_status == "PS":
                return {
                    "success": True,
                    "user_no": user_no,
                    "mobile": mobile_no,
                    "risk_status": risk_status,
                    "env": env,
                    "next_action": f"用户已创建并授信通过，mobile={mobile_no}, user_no={user_no}。"
                                   f"下一步调用 h5_bind_card(mobile='{mobile_no}', env='{env}') 进行绑卡。"
                }
            elif risk_status == "RJ":
                return {
                    "success": False,
                    "user_no": user_no,
                    "mobile": mobile_no,
                    "risk_status": risk_status,
                    "error": "授信被拒绝(RJ)，请更换身份信息重试。"
                }
            elif risk_status == "timeout":
                return {
                    "success": False,
                    "user_no": user_no,
                    "mobile": mobile_no,
                    "risk_status": risk_status,
                    "error": "授信审批超时，请稍后重试或联系管理员。"
                }
            else:
                return {
                    "success": False,
                    "user_no": user_no,
                    "mobile": mobile_no,
                    "risk_status": risk_status,
                    "error": f"授信状态异常：{risk_status}。"
                }
        elif isinstance(result, str) and "撞库失败" in result:
            return {"success": False, "error": result, "env": env}
        else:
            code = result.get("code") if isinstance(result, dict) else None
            return {"success": False, "error": f"授信失败(code={code})", "data": result, "env": env}
    except Exception as e:
        return {"success": False, "error": str(e), "env": env}


def query_loan_status(
    mobile: str,
    env: str = "BM_SIT",
    channel: str = "lxj",
    fund_code: str = "",
    loan_req_no: str = ""
) -> dict:
    """
    触发放款任务（LPX/LCS/APS）并轮询直到放款到达终态。

    前置条件：已通过 h5_draw_submit 提交借款申请（有 loanReqNo）。
    loan_req_no: h5_draw_submit 返回的 loanReqNo（LP开头），传入后直接精确定位借据，避免多借据场景查错数据。
    fund_code: 资方代码，一般不需传，query_order 内部自动查。
    返回：放款状态，放款成功时附带 loan_no、fund_code。
    状态含义：order_ds=放款成功, fund_fail=资方失败, lcs_fail/lcs_success=可重试。

    调用后：
      - 放款成功 → 调用 init_bill(loan_no) 初始化账单
      - 放款失败 → 检查返回的 res 字段定位原因
    """
    try:
        result = query_order(
            mobile=mobile,
            env=env,
            channel=channel,
            loan_query_status=None,
            fund_code=fund_code,
            progress_callback=None,
        )
        is_success = result == "order_ds"
        resp = {
            "success": is_success,
            "mobile": mobile,
            "result": result,
        }
        if is_success:
            # 优先用传入的 loan_req_no 精确查询；否则从 iou 表取最新一条
            if loan_req_no:
                iou_data = _query_iou(env=env, loan_req_no=loan_req_no, fields=['loan_no', 'fund_code'])
            else:
                req_sql = (
                    "select loan_req_no from lps.bm_iou where user_no = (select user_no from cis.u_user "
                    f"where mobile_no_md5 = md5('{mobile}')) order by loan_date desc limit 1;"
                )
                req_info = db_conn(env).select_one(req_sql)
                req_data = (req_info or {}).get('data') or {}
                lr_no = req_data.get('loan_req_no', '')
                iou_data = _query_iou(env=env, loan_req_no=lr_no, fields=['loan_no', 'fund_code'])
            resp["loan_no"] = iou_data.get('loan_no', '')
            resp["fund_code"] = iou_data.get('fund_code', '')
            _ln = resp["loan_no"]
            resp["next_action"] = f"放款成功。下一步调用 init_bill(loan_no='{_ln}', env='{env}') 初始化账单。"
        else:
            resp["next_action"] = f"放款未成功（状态={result}）。检查错误原因后重试。"
        return resp
    except Exception as e:
        return {"success": False, "error": str(e), "mobile": mobile}


def query_repay_status(
    mobile: str,
    loan_no: str,
    repay_type: str = "SINGLE",
    repay_query_status: str = "SUCCESS",
    term: int = 0,
    env: str = "BM_SIT",
    channel: str = "lxj"
) -> dict:
    """
    触发还款任务（XXL-Job 107）并轮询直到还款到达终态。这是还款流程的核心步骤，决定最终还款结果。

    前置条件：已通过 h5_repay 提交还款申请。
    repay_type: SINGLE（当期还款）/ ALL（提前结清），默认 SINGLE。ALL 时会按提前结清（ES）查询。
                用户说"还当期/只还一期"→SINGLE，"全部结清"→ALL。
    repay_query_status: 期望的还款终态，默认 SUCCESS。
        SUCCESS          → 轮询等到 03（还款成功）
        FAIL             → mock 资方失败，轮询等到 04（还款失败）
        PARTIAL_SUCCESS  → INNER 渠道改失败，轮询等到 05（部分成功）
        用户说"还款成功"→SUCCESS，"还款失败"→FAIL，"部分还款/还一点"→PARTIAL_SUCCESS。
    term: 指定期数，0 表示最新一期。仅 repay_type=SINGLE 时生效。
    返回：还款终态。
    状态含义：repay_success=03 成功, repay_fail=04 失败, repay_partial_success=05 部分成功。
    """
    try:
        # 映射 repay_type → term 参数:
        # SINGLE → None(最新一期) 或具体期数; ALL → 'all'(ES提前结清)
        if repay_type.upper() == "ALL":
            query_term = "all"
        elif term > 0:
            query_term = term
        else:
            query_term = None

        result_status = query_repay_result(
            mobile=mobile,
            loan_no=loan_no,
            repay_query_status=repay_query_status,
            env=env,
            channel=channel,
            term=query_term,
            progress_callback=None,
        )
        return {
            "success": result_status in ("repay_success", "repay_partial_success"),
            "mobile": mobile,
            "loan_no": loan_no,
            "repay_type": repay_type,
            "result_status": result_status,
            "next_action": f"还款结果已确认：{result_status}。"
        }
    except Exception as e:
        return {"success": False, "error": str(e), "mobile": mobile, "loan_no": loan_no}


def init_bill(
    loan_no: str,
    overdue_type: str = "N",
    day: int = 0,
    bill_day: bool = True,
    env: str = "BM_SIT"
) -> dict:
    """
    初始化借据的还款计划（计息计费）。支持正常账单和逾期账单。

    前置条件：借据已放款成功（有 loan_no）。
    overdue_type: N=正常, Y=逾期，默认 N。用户说"正常"→N，"逾期"→Y。
    day: 逾期天数，overdue_type=Y 时必填。
    bill_day: 是否到账单日，默认 True。

    调用后：
      - 正常账单 → 可调用 h5_repay 发起还款
      - 逾期账单 → 可调用 compensation 执行代偿流程
    """
    try:
        bill = LoanBill(
            loan_no=loan_no,
            overdue_type=overdue_type,
            day=day,
            bill_day=bill_day,
            env=env,
        )
        res = bill.init_plan_1()

        if res[0] == "S":
            status = "初始化成功"
        elif res[0] == "F":
            status = "试算接口超时，需手动触发计息"
        else:
            status = "初始化异常"

        if overdue_type == "Y":
            next_action = f"逾期账单已初始化(逾期{day}天)。可调用 compensation(loan_no='{loan_no}', env='{env}') 执行代偿。"
        else:
            next_action = f"账单已初始化。可调用 h5_repay(mobile=<手机号>, loan_no='{loan_no}', env='{env}') 发起还款。"

        return {
            "success": res[0] == "S",
            "loan_no": loan_no,
            "status": status,
            "overdue_type": overdue_type,
            "next_action": next_action,
        }
    except AssertionError as e:
        return {"success": False, "loan_no": loan_no, "error": str(e)}
    except Exception as e:
        return {"success": False, "loan_no": loan_no, "error": str(e)}


def update_fund_mock(
    env: str = "BM_SIT",
    amt: int = 3500,
    term: int = 12,
    cust_no: str = "",
    fund_code: str = "ZBANK_E8",
    is_date: str = ""
) -> dict:
    """
    更新资方还款计划 mock 数据。用于借款前或还款前调整资方 mock 以匹配预期。

    前置条件：无严格前置，通常借款前或还款前调用。
    amt: 金额，默认 3500。
    term: 期数，默认 12。
    fund_code: 资方代码，默认 ZBANK_E8。
    is_date: 传 "true" 时同步更新 mock 日期。
    返回：mock 更新结果。
    """
    try:
        result = fund_plan_mock(
            env=env,
            amt=amt,
            term=term,
            cust_no=cust_no or None,
            is_data=is_date or None,
            fund_code=fund_code,
        )
        return {
            "success": result == "mock_success",
            "result": result,
            "fund_code": fund_code,
            "next_action": f"Mock 数据{'已更新' if result == 'mock_success' else '更新失败'}。"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def compensation(
    loan_no: str,
    fund_code: str = "",
    number: int = 0,
    env: str = "BM_SIT"
) -> dict:
    """
    执行代偿全流程。自动完成：加载代偿配置 → 初始化逾期账单 → 等待逾期天数就绪 → 执行多轮代偿。

    前置条件：借据已放款成功，账单已逾期（overdue_type=Y）。
    fund_code: 资方代码，默认自动从 lps.bm_iou 按 loan_no 查询。
    number: 代偿轮数，0 表示自动计算。
    返回：代偿流程摘要和各轮结果。
    """
    try:
        if not fund_code:
            iou_data = _query_iou(env=env, loan_no=loan_no, fields=['fund_code'])
            fund_code = iou_data.get('fund_code', '') or None
        flow = LoanCompensationFlow(
            loan_no=loan_no,
            fund_code=fund_code or None,
            number=number or None,
            env=env,
        )
        config = flow.load_compensation_config()
        effective_number = flow.calculate_effective_number()
        max_day = flow.calculate_max_day()
        init_result = flow.init_overdue_for_compensation()

        if not init_result or init_result[0] != "S":
            return {
                "success": False,
                "loan_no": loan_no,
                "error": "逾期账单初始化失败或计息未完成",
                "config": config,
                "effective_number": effective_number,
                "max_day": max_day,
            }

        flow.wait_until_overdue_days_ready()
        round_results = flow.execute_compensation_rounds()
        summary = flow.summary()
        summary["round_results"] = round_results

        return {
            "success": True,
            "loan_no": loan_no,
            "data": summary,
            "next_action": "代偿流程已完成。"
        }
    except Exception as e:
        return {"success": False, "loan_no": loan_no, "error": str(e)}


def trigger_job(
    job_id: int,
    executor_param: str = "",
    env: str = "BM_SIT"
) -> dict:
    """
    手动触发 XXL-Job 分布式任务。作为兜底工具，用于重试失败的任务或执行特殊操作。

    前置条件：无。
    job_id: XXL-Job 任务 ID（130=LPX放款, 131=APS放款, 107=还款同步, 等）。
    executor_param: 任务参数，格式视具体 job 而定。
    返回：触发结果。
    """
    try:
        param = executor_param if executor_param else None
        result = xxl_job_trigger(job_id=job_id, executor_param=param, env=env)
        return {
            "success": result == "pass",
            "job_id": job_id,
            "result": result,
            "next_action": f"Job {job_id} {'触发成功' if result == 'pass' else '触发失败'}。"
        }
    except Exception as e:
        return {"success": False, "error": str(e), "job_id": job_id}
