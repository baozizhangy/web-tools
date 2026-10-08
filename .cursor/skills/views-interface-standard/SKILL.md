---
name: views-interface-standard
description: 在 webtools 项目中新增 Django 接口时的标准规范。适用于在 views.py 新增 BM 工具接口或 H5 场景接口，包括同步 JsonResponse 接口和异步 SSE 流式接口两种模式。
---

# views.py 接口开发标准

适用于 `djangoWebTools/views.py` 中新增接口时的标准做法。

---

## 一、接口分类

| 类型 | 适用场景 | 响应方式 |
|------|----------|----------|
| 同步接口 | 操作简单、耗时短 | `JsonResponse` |
| SSE 流式接口 | 有轮询/等待/进度推送需求 | `StreamingHttpResponse` |

---

## 二、通用约定（所有接口必须遵守）

### 装饰器与请求解析
```python
@csrf_exempt
def my_view(request):
    data = json.loads(request.body)
    env = data.get('env', 'BM_SIT').upper()
```

- 必须加 `@csrf_exempt`
- 统一用 `json.loads(request.body)` 解析请求体
- `env` 参数统一 `.upper()` 处理，有默认值时用 `data.get('env', 'BM_SIT').upper()`

### 响应格式
```python
# 成功
return JsonResponse({"success": 0, "res": "操作成功描述"}, charset='utf-8')

# 业务失败（具体类型）
return JsonResponse({"success": 1, "res": "失败原因描述"}, charset='utf-8')

# 参数缺失
return JsonResponse({"success": 3, "res": "缺少 loan_no"}, charset='utf-8')

# 通用/未知失败
return JsonResponse({"success": -1, "res": "操作失败，检查配置"}, charset='utf-8')

# 请求方式错误
return JsonResponse({'error': '无效的请求'})
```

**success 编码约定：**
- `0` = 成功
- `1, 2, 3...` = 具体业务失败类型（从 1 开始递增）
- `-1` = 通用/兜底失败
- 字符串 code（如 `'lcs_fail'`、`'repay_success'`）= 复杂状态映射场景

### POST 方法检查

**所有接口必须检查 `request.method == 'POST'`**。当前 BM 工具接口大多遗漏此检查，新增接口不得再省略。

```python
# ✅ 正确：顶部检查
@csrf_exempt
def my_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': '无效的请求'}, status=200)
    data = json.loads(request.body)
    ...

# ❌ 错误：缺少 POST 检查，GET 请求也会触发业务逻辑
@csrf_exempt
def my_view(request):
    data = json.loads(request.body)  # GET 请求无 body，直接报错
    ...
```

### 参数解析规范

**env 参数必须同时做 `.upper()` 和默认值**：

```python
# ✅ 正确
env = data.get('env', 'BM_SIT').upper()

# ❌ 缺少 .upper()
env = data.get('env', 'BM_SIT')

# ❌ 缺少默认值
env = data.get('env').upper()
```

**前端参数命名兼容**：前端 JS 传参惯用 camelCase（`loanQueryStatus`、`repayQueryStatus`、`bindScene`），后端内部用 snake_case。视图中对关键参数应做双名兼容：

```python
# ✅ 正确：同时支持前端 camelCase 和内部 snake_case
loan_query_status = data.get('loanQueryStatus') or data.get('loan_query_status')
fund_code = data.get('fundCode') or data.get('fund_code')
```

### 参数校验
```python
if not loan_no:
    return JsonResponse({"success": 3, "res": "缺少 loan_no"}, charset='utf-8')
if param not in ['Y', 'N']:
    return JsonResponse({"success": 4, "res": "xxx 仅支持 Y 或 N"}, charset='utf-8')
```

### 异常处理分层规范

视图层遵循三层异常处理策略：

```python
try:
    result = some_business_function(...)
    return JsonResponse({"success": 0, "res": "操作成功"}, charset='utf-8')
except AssertionError as e:
    # 第 1 层：业务断言失败（参数组合不合法、状态不满足前置条件）
    return JsonResponse({"success": 5, "res": str(e)}, charset='utf-8')
except TimeoutError as e:
    # 第 2 层：轮询/等待超时（可重试）
    return JsonResponse({"success": 2, "res": str(e)}, charset='utf-8')
except Exception as e:
    # 第 3 层：未知异常，记录日志并返回通用失败
    return JsonResponse({"success": -1, "res": f"操作异常: {e}"}, charset='utf-8')
```

**原则：**
- 简单同步接口（单次调用、无轮询）不强制 try/except，由 Django 统一处理 500
- 多步骤流程（如 `loan_compensation`、`h5_coupon_receive`）必须捕获异常，避免中间状态不一致
- `AssertionError` 是项目内部用于"业务前置条件不满足"的信号，视图中应单独捕获
- 未知异常兜底返回 `success: -1`，附上异常信息便于排查

### 双通道同步规则（MCP + HTTP）

本项目同时支持两套调用通道，**新增或修改业务功能时，两个通道必须同步更新**，缺一不可。

| 通道 | 入口文件 | 调用方 | 注册方式 |
|------|----------|--------|----------|
| MCP 协议 | `mcp_server/tools.py` | AI Agent（Claude Code 等） | `mcp_server/server.py` 中 `_register_tools()` |
| HTTP 端点 | `djangoWebTools/views.py` | 前端页面（`web_page/static/component/*.js`） | `djangoWebTools/urls.py` 中 `path()` |

**同步清单：**

1. 业务逻辑统一放在 `djangoWebTools/tools/` 或 `tests/interface/` 层，两个通道共用
2. `mcp_server/tools.py` 包装为 MCP tool 函数
3. `djangoWebTools/views.py` 包装为 Django view 函数
4. `mcp_server/server.py` 的 `_register_tools()` 注册新 tool
5. `djangoWebTools/urls.py` 注册新路由
6. 两个通道的**参数校验、默认值、返回值结构**保持一致

**常见漏改场景（重点防范）：**

- 只改了 `mcp_server/tools.py`，忘了改 `djangoWebTools/views.py` → 前端页面不生效
- 只改了 `djangoWebTools/views.py`，忘了改 `mcp_server/tools.py` → AI Agent 不生效
- 两个都改了，但轮询/状态确认逻辑只加了一个通道 → 行为不一致

**验证方法：** 新增功能后，用 `grep` 确认新函数名在两个文件中都出现。

---

## 三、同步接口模板

```python
@csrf_exempt
def bm_xxx_action(request):
    data = json.loads(request.body)
    loan_no = data.get('loan_no')
    env = data.get('env').upper()
    channel = data.get('channel')

    if not loan_no:
        return JsonResponse({"success": 3, "res": "缺少 loan_no"}, charset='utf-8')

    result = some_tool_function(loan_no, env, channel)

    if result == 'success':
        return JsonResponse({"success": 0, "res": "操作成功"}, charset='utf-8')
    elif result == 'specific_fail':
        return JsonResponse({"success": 1, "res": "具体失败原因"}, charset='utf-8')
    else:
        return JsonResponse({"success": -1, "res": "操作失败，检查配置"}, charset='utf-8')
```

---

## 四、SSE 流式接口模板

适用于有进度推送需求的长流程接口（放款、还款结果查询、H5 场景等）。

```python
@csrf_exempt
def bm_xxx_stream(request):
    data = json.loads(request.body)
    loan_no = data.get('loan_no')
    mobile = data.get('mobile')
    env = data.get('env').upper()
    channel = data.get('channel')

    message_queue = Queue()

    def sse_payload(event_type, payload):
        return f"data: {json.dumps({'type': event_type, **payload}, ensure_ascii=False)}\n\n"

    def worker():
        try:
            result = some_long_running_function(
                loan_no,
                env,
                channel=channel,
                progress_callback=lambda message: message_queue.put(('progress', {'message': message})),
            )
            message_queue.put(('done', {'result': _build_xxx_response_data(result)}))
        except Exception as e:
            message_queue.put(('error', {'message': f'流程异常:{e}'}))
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
```

**SSE 事件类型约定：**
| event_type | 含义 |
|------------|------|
| `progress` | 进度消息，`{'message': '...'}` |
| `done` | 流程完成，`{'result': {...}}` |
| `error` | 流程异常，`{'message': '...'}` |
| `close` | 流结束标志，不对外发送 |

---

## 五、复杂状态映射模板

当业务函数返回多种状态码时，提取为独立的 `_build_xxx_response_data()` 函数，不要把映射逻辑写在 view 函数体内。

```python
def _build_xxx_response_data(status):
    response_mapping = {
        'success_case': {"success": 0, "res": "操作成功"},
        'specific_fail_a': {"success": 'specific_fail_a', "res": "具体失败原因A"},
        'specific_fail_b': {"success": 'specific_fail_b', "res": "具体失败原因B"},
        'timeout_case': {"success": 'timeout', "res": "轮询超时"},
    }
    return response_mapping.get(status, {"success": -1, "res": f"操作失败，执行结果:{status}"})
```

---

## 六、异步结果 DB 轮询规范

适用于所有"接口请求成功后业务有延迟，需等待 DB 状态变更才算完成"的场景。本规范是基础规则，新增涉及异步状态等待的功能时必须遵守。

### 适用场景

- 授信审批结果等待（`query_risk_status`）
- 放款状态轮询（`query_order` 内部）
- 还款结果轮询（`query_repay_result` 内部）
- 优惠券到账确认（`query_coupon_arrival`）
- 绑卡渠道状态轮询

### 核心原则

1. **轮询逻辑放在业务层**（`djangoWebTools/tools/` 或 `tests/interface/`），不在 view 函数内直接写轮询
2. **view 层只做**：参数解析 → 调业务函数 → 拿结果 → 组响应
3. **同步 JsonResponse 接口也需要轮询**：不要因为接口是同步的就跳过轮询直接返回成功

### 标准模板

```python
import datetime
import time
from config import db_conn

def query_xxx_status(params, env='BM_SIT', timeout_secs=60):
    """
    轮询查询 XXX 状态直到到达终态或超时。

    Args:
        params: 查询参数
        env: 环境
        timeout_secs: 超时秒数，默认 60

    Returns:
        成功返回终态标识/True，超时返回 'timeout'/False
    """
    deadline = datetime.datetime.now() + datetime.timedelta(seconds=timeout_secs)
    time.sleep(3)  # 初始等待，给异步业务处理留缓冲

    while datetime.datetime.now() < deadline:
        sql = f"select ... from database.table where ...;"
        res = db_conn(env).select_one(sql)

        if res["data"] is not None:
            # 成功条件满足 → 返回成功
            return True  # 或返回具体状态值

        # 可选：失败条件判断
        # if <失败条件>:
        #     return False

        time.sleep(5)  # 轮询间隔

    return False  # 或 return 'timeout'
```

### 关键参数约定

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `timeout_secs` | 60 | 总超时，到达后返回超时结果 |
| 初始 sleep | 3s | 接口调用后等待，避免立即查询 |
| 轮询间隔 | 5-15s | 视业务延迟而定。授信/放款 20s，优惠券 5-15s |

### DB 查询规范

- 必须使用 `database.table` 完整路径（如 `cos.offering_record`、`apv.ap_apply`）
- 用 `db_conn(env).select_one(sql)` 执行
- 结果通过 `res["data"]` 取值，无数据时 `res["data"] is None`
- SQL 中变量用 f-string 拼接，变量来自函数参数（非外部输入，无需防注入）

### view 层调用模式

```python
@csrf_exempt
def h5_xxx(request):
    data = json.loads(request.body)
    # ... 参数解析与校验 ...

    # 1. 先提交业务请求
    result = submit_xxx(...)

    # 2. 再轮询确认 DB 状态
    if not query_xxx_status(params, env=env):
        return JsonResponse({
            'success': -1,
            'error': 'XXX 接口已提交，但轮询超时未生效，请手工确认。',
            'detail': {...},
        }, charset='utf-8')

    # 3. DB 确认到账后返回成功
    return JsonResponse({
        'success': 0,
        'res': 'XXX 已完成',
        'data': {...},
    }, charset='utf-8')
```

### 已有轮询函数一览

| 函数 | 文件 | 查询目标 | timeout | 间隔 |
|------|------|----------|---------|------|
| `query_risk_status` | `djangoWebTools/tools/bm_tools/credit_apply.py` | `apv.ap_apply.state` | 100s | 20s |
| `query_coupon_arrival` | `tests/interface/coupon_send.py` | `cos.offering_record.status` | 90s | 15s |
| `query_order`(内部轮询) | `djangoWebTools/tools/bm_tools/credit_order.py` | 放款状态 | — | — |
| `query_repay_result`(内部轮询) | `djangoWebTools/tools/bm_tools/repay_result.py` | 还款结果 | — | — |

### 反模式（禁止）

```python
# ❌ 错误：提交接口后直接返回成功，不等待 DB 确认
def h5_coupon_receive(request):
    result = update_excel_and_send(...)
    return JsonResponse({'success': 0, 'res': '领取成功'})  # 实际可能未到账

# ✅ 正确：提交后轮询 DB，确认到账再返回
def h5_coupon_receive(request):
    result = update_excel_and_send(...)
    if not query_coupon_arrival(user_no, coupon_code, env):
        return JsonResponse({'success': -1, 'error': '超时未到账'})
    return JsonResponse({'success': 0, 'res': '领取优惠券已到账'})
```

---
## 七、H5 场景接口补充规范

H5 接口服务于前端 `web_page/static/component/*.js`，与 BM 后端工具接口存在以下差异，必须遵守。

### H5 vs BM 关键差异

| 项目 | BM 工具接口 | H5 场景接口 |
|------|------------|------------|
| 错误响应格式 | `{"success": N, "res": "..."}` | `{"error": "..."}` + `status=200` |
| env 处理 | `data.get('env').upper()` | `data.get('env')` 不 upper（H5SceneService 内部处理） |
| JSON 解析 | `json.loads(request.body)` | `json.loads(request.body or '{}')` |
| 业务入口 | 直接调 `djangoWebTools/tools/` | 通过 `H5SceneService` / `H5Api` |
| 参数字符串 | 一般不 strip | 部分 `.strip()` 处理（mobile、user_no） |

### 参数解析模板

```python
@csrf_exempt
def h5_xxx_scene(request):
    if request.method != 'POST':
        return JsonResponse({'error': '无效的请求'}, status=200)

    data = json.loads(request.body or '{}')
    mobile = (data.get('mobile') or '').strip()
    env = data.get('env')  # H5 不加 .upper()，H5SceneService 内部处理

    if not env or not mobile:
        return JsonResponse({'error': '缺少 env 或 mobile'}, status=200)
    if param not in ['A', 'B']:
        return JsonResponse({'error': 'param 仅支持 A 或 B'}, status=200)

    service = H5SceneService(mobile=mobile, env=env)
    result = service.run_xxx_scene(...)
    return JsonResponse({"success": 0, "data": result}, charset='utf-8')
```

### H5 SSE 内联模式

H5 场景的 SSE 接口使用 `wrapped_stream()` 内联模式，与 BM 的 `event_stream()` 模式等效但更紧凑：

```python
@csrf_exempt
def h5_xxx_scene(request):
    # ... 参数解析与校验 ...

    def wrapped_stream():
        message_queue = Queue()

        def emit(event_type, payload):
            return f"data: {json.dumps({'type': event_type, **payload}, ensure_ascii=False)}\n\n"

        def worker():
            try:
                service = H5SceneService(mobile=mobile, env=env)
                result = service.run_xxx_scene(
                    ...,
                    progress_callback=lambda msg: message_queue.put(('progress', {'message': msg})),
                )
                message_queue.put(('done', {'result': result}))
            except Exception as e:
                message_queue.put(('error', {'message': str(e)}))
            finally:
                message_queue.put(('close', {}))

        threading.Thread(target=worker, daemon=True).start()
        yield emit('progress', {'message': '已收到请求，开始执行流程'})

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
```

### 布尔值参数解析

前端开关组件传入 `true`/`false` 字符串或布尔值，需做兼容判断：

```python
# ✅ 正确：同时处理布尔值和字符串
use_coupon = data.get('useCoupon') in [True, 'true', 'True', 1]
```

### 错误响应格式（H5 专用）

H5 前端 `bm_h5_repay_scene.js` 等直接读取 `result.error` 展示错误信息，因此校验失败返回 `{'error': '...'}` 而非 `{'success': N}`：

```python
# ❌ BM 风格 — H5 前端无法正确展示
return JsonResponse({"success": 3, "res": "缺少 mobile"})

# ✅ H5 风格 — 前端直接取 result.error
return JsonResponse({'error': '缺少 mobile'}, status=200)
```

注意：`status=200` 显式指定，防止 Django 默认返回 400/500 状态码导致前端 fetch 进入 catch 分支。

### 已有 H5 接口一览

| view 函数 | 业务入口 | 响应类型 |
|-----------|----------|----------|
| `h5_bind_card_scene` | `H5SceneService.run_bind_card_scene()` | JsonResponse |
| `h5_draw_submit_scene` | `H5SceneService.run_draw_submit_scene()` | SSE |
| `h5_repay_scene` | `H5SceneService.run_repay_scene()` | SSE |
| `h5_coupon_receive` | `update_excel_and_send()` + `query_coupon_arrival()` | JsonResponse |
| `bm_get_h5_url` | `H5Api.request_url()` | JsonResponse |

---
## 八、URL 注册规范

### 命名规则
| 接口类型 | URL 前缀 | 示例 |
|----------|----------|------|
| BM 工具接口 | `api/xxx` | `api/credit_apply`, `api/query_order` |
| H5 场景接口 | `api/h5/scene/xxx` | `api/h5/scene/bind_card` |
| 导航配置 | `api/nav/xxx` | `api/nav/get`, `api/nav/add` |

### 注册步骤（每次新增接口必须同时完成）

**第一步：在 `views.py` 实现 view 函数**

**第二步：在 `urls.py` 导入**
```python
from djangoWebTools.views import (
    ...,
    my_new_view,  # 新增
)
```

**第三步：在 `urlpatterns` 注册路由**
```python
path('api/my_new_endpoint', my_new_view, name='my_new_view'),
```

---

## 九、import 引用规范

```python
# Django 核心
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt

# 标准库（SSE 接口需要）
from queue import Queue, Empty
import threading

# 业务逻辑层（api/app/）
from api.app.h5_api import H5Api
from api.app.h5_scene import H5SceneService
from api.app.loan_bill import LoanBill, RepayLoan, LoanCompensationFlow

# 工具函数层（djangoWebTools/tools/）
from djangoWebTools.tools.bm_tools.credit_apply import credit_apply, query_risk_status
from djangoWebTools.tools.bm_tools.credit_order import credit_order, query_order
from djangoWebTools.tools.query_user_info import query_user_info_by_mobile
```

**原则：**
- 业务逻辑放在 `api/app/` 或 `djangoWebTools/tools/` 中，view 函数只做参数解析、调用、响应组装
- view 函数不直接写 HTTP 请求、SQL、业务计算逻辑

---

## 十、当前已注册接口一览

| view 函数 | URL | 响应类型 | 业务说明 |
|-----------|-----|----------|----------|
| `query_user` | `api/query_user` | JsonResponse | 查询用户信息 |
| `init_plan` | `api/init_plan` | JsonResponse | 初始化账单/计息 |
| `repay_loan` | `api/repay_loan` | JsonResponse | 借据还款 |
| `loan_compensation` | `api/loan_compensation` | JsonResponse | 借据代偿流程 |
| `trigger_xxl_job` | `api/trigger_xxl_job` | JsonResponse | 触发 XXL-Job |
| `bm_credit_apply` | `api/credit_apply` | JsonResponse | 助贷授信申请 |
| `bm_credit_order` | `api/credit_order` | JsonResponse | 助贷创单 |
| `bm_query_order` | `api/query_order` | SSE | 查询订单/触发放款脚本 |
| `bm_repay_order` | `api/bm_repay_order` | JsonResponse | 发起还款 |
| `bm_query_repay_order` | `api/query_repay_order` | JsonResponse | 查询还款状态 |
| `bm_query_repay_result` | `api/query_repay_result` | SSE | 查询还款结果 |
| `bm_repay_trail_order` | `api/bm_repay_trail_order` | JsonResponse | 还款试算 |
| `bm_update_mock` | `api/bm_update_mock` | JsonResponse | 更新 mock 还款数据 |
| `bm_get_h5_url` | `api/bm_get_h5_url` | JsonResponse | 获取 H5 链接 |
| `h5_bind_card_scene` | `api/h5/scene/bind_card` | JsonResponse | H5 绑卡场景 |
| `h5_draw_submit_scene` | `api/h5/scene/draw_submit` | SSE | H5 借款提交场景 |
| `h5_repay_scene` | `api/h5/scene/repay` | SSE | H5 还款场景 |
| `h5_coupon_receive` | `api/h5/scene/coupon_receive` | JsonResponse | H5 领取优惠券 |
| `bm_offline_oak_pay` | `api/offline_oak_pay` | SSE | 橡树线下还款 |

---

## 十一、新增接口检查清单

- [ ] view 函数加了 `@csrf_exempt`
- [ ] **检查了 `request.method == 'POST'`**（BM 接口也需检查，不可省略）
- [ ] 用 `json.loads(request.body)` 解析参数
- [ ] `env` 参数做了 `.upper()` **且有默认值** `data.get('env', 'BM_SIT').upper()`
- [ ] 前端 camelCase 参数做了双名兼容：`data.get('loanQueryStatus') or data.get('loan_query_status')`
- [ ] 必填参数做了非空校验，返回格式符合规范
- [ ] 响应统一带 `charset='utf-8'`
- [ ] 复杂状态映射提取为 `_build_xxx_response_data()` 函数
- [ ] 多步骤流程用三层 try/except（AssertionError / TimeoutError / Exception）
- [ ] SSE 接口包含 `progress / done / error / close` 四种事件
- [ ] SSE 接口设置了 `Cache-Control: no-cache` 和 `X-Accel-Buffering: no`
- [ ] 在 `urls.py` 完成 import 和 `path()` 注册
- [ ] URL 命名符合 BM/H5 前缀规范
- [ ] 涉及异步状态等待的接口，实现了 DB 轮询确认（参考第六章）
- [ ] 轮询逻辑放在业务层，不在 view 函数内直接写 while/sleep
- [ ] **双通道同步**：`mcp_server/tools.py` 和 `djangoWebTools/views.py` 都已更新
- [ ] **双通道同步**：`mcp_server/server.py` 的 `_register_tools()` 和 `djangoWebTools/urls.py` 都已注册
- [ ] 用 grep 确认新函数名在 `mcp_server/tools.py` 和 `djangoWebTools/views.py` 中均出现
- [ ] **H5 接口专用**：错误响应用 `JsonResponse({'error': '...'}, status=200)` 格式
- [ ] **H5 接口专用**：SSE 用 `wrapped_stream()` 内联模式（参见第七章）
