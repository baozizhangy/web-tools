"""
WebTools 造数 MCP Server

启动方式:
    python -m mcp_server.server                     # stdio 本地模式
    uvicorn djangoWebTools.asgi:application         # HTTP 服务模式（嵌入 Django）

调用方 AI 可通过自然语言指令自动编排下方注册的 tool 来生成测试数据。
完整链路：创建用户&授信 → H5绑卡 → H5借款 → 完成放款 → 初始化账单 → 还款 → 确认还款结果

MCP 协议：基于 stdio 的 JSON-RPC 2.0，不暴露任何源代码或数据库信息。
"""
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from mcp.server.fastmcp import FastMCP


def _register_tools(mcp: FastMCP):
    """将 tools.py 中的所有 tool 注册到 MCP 实例。延迟导入以隔离 Django 依赖。"""
    from mcp_server.tools import (
        credit_apply,
        h5_bind_card,
        h5_draw_submit,
        h5_repay,
        h5_get_url,
        offline_oak_pay,
        coupon_receive,
        init_bill,
        query_loan_status,
        query_repay_status,
        update_fund_mock,
        compensation,
        trigger_job,
    )

    mcp.tool(name="credit_apply", description="创建借贷测试用户并授信：自动随机生成身份信息→撞库→风控白名单→授信→等待授信通过。不传参数则全自动生成")(credit_apply)
    mcp.tool(name="h5_bind_card", description="H5 绑卡流程：登录→卡BIN查询→签约提交→验证→轮询渠道绑定状态")(h5_bind_card)
    mcp.tool(name="h5_draw_submit", description="H5 借款申请：清理→登录→预查询→自动绑卡→权益匹配→试算→提交→验证码。不含放款，调用后必须调用 query_loan_status")(h5_draw_submit)
    mcp.tool(name="h5_repay", description="H5 还款：登录→查loanReqNo→账单详情→试算→提交→验证码→查询还款结果")(h5_repay)
    mcp.tool(name="h5_get_url", description="获取 H5 页面链接（借款页或还款页），用于手动操作或校验")(h5_get_url)
    mcp.tool(name="offline_oak_pay", description="橡树线下还款全流程：试算→oakPayOrder→执行job→校验结清")(offline_oak_pay)
    mcp.tool(name="coupon_receive", description="为用户领取折扣券或固定金额优惠券")(coupon_receive)
    mcp.tool(name="init_bill", description="初始化借据还款计划，支持正常(N)和逾期(Y)两种模式")(init_bill)
    mcp.tool(name="query_loan_status", description="触发放款任务(LPX/LCS/APS)并轮询到终态。h5_draw_submit 之后必须调用此 tool 才能完成放款")(query_loan_status)
    mcp.tool(name="query_repay_status", description="触发还款任务并轮询到终态(03成功/04失败/05部分成功)")(query_repay_status)
    mcp.tool(name="update_fund_mock", description="更新资方还款计划 mock 数据，用于借款前或还款前调整")(update_fund_mock)
    mcp.tool(name="compensation", description="执行代偿全流程：逾期账单初始化→等待逾期天数→多轮代偿")(compensation)
    mcp.tool(name="trigger_job", description="手动触发 XXL-Job 任务，兜底工具用于重试或特殊操作")(trigger_job)


# ============================================================
# 生命周期指引 Prompt
# ============================================================
LIFECYCLE_GUIDE = """
## 借贷数据生成状态机

### 业务背景
这是一个消费金融助贷平台的测试数据生成器。数据生成遵循固定链条，每个阶段有明确的 tool 入口。
你拿到用户的自然语言指令后，判断执行到哪个阶段为止，然后按序调用 tool。

---

### 阶段 → Tool 对照表

```
阶段 1: 创建用户&授信      →  credit_apply(mobile, name, id_card, env, channel, risk_type)
        产出: user_no, mobile, name, id_card
        条件: 用户未提供 mobile 时执行
        说明: 随机生成身份信息 → 撞库 → 风控白名单 → 授信 → 等待授信通过(PS)

阶段 2: H5 绑卡           →  h5_bind_card(mobile, env)
        前置: mobile 已存在
        产出: 卡绑定完成

阶段 3: H5 借款           →  h5_draw_submit(mobile, amt, term, is_privilege_process, env)
        前置: 已完成绑卡（如未绑会自动绑）
        产出: loanReqNo（借款申请号）
        注意: 此步不包含放款！

阶段 4: 完成放款           →  query_loan_status(mobile, env)
        前置: 已提交借款（有 loanReqNo）
        产出: loan_no（借据号），放款成功
        关键状态: order_ds=成功, fund_fail=资方拒绝, lcs_fail/lcs_success=可重试

阶段 5: 初始化账单         →  init_bill(loan_no, overdue_type, day, env)
        前置: 已放款成功（有 loan_no）
        overdue_type: N=正常, Y=逾期
        产出: 账单就绪

阶段 6: H5 还款            →  h5_repay(mobile, loan_no, repay_type, use_coupon, env)
        前置: 账单已初始化
        repay_type: SINGLE=当期, ALL=提前结清
        产出: 还款结果

阶段 7: 确认还款终态       →  query_repay_status(mobile, loan_no, repay_query_status, env)
        前置: 已发起还款
        状态: 03=成功, 04=失败, 05=部分成功

阶段 *: 代偿               →  compensation(loan_no, fund_code, number, env)
        前置: 借据已逾期（阶段5传 overdue_type=Y）
        产出: 代偿完成
```

### 辅助 Tool

| Tool | 用途 |
|------|------|
| h5_get_url(mobile, scene) | 获取 H5 页面链接，用于手动操作或校验 |
| offline_oak_pay(mobile, loan_no, terms) | 橡树线下还款，替代 H5 还款的另一条路径 |
| coupon_receive(mobile, user_no) | 领取优惠券，h5_repay 时可使用 |
| update_fund_mock(env, amt, term, fund_code) | 更新资方 mock 还款计划，借款或还款前调整 |
| trigger_job(job_id, executor_param, env) | 手动触发 XXL-Job 任务，用于重试失败步骤 |

---

### 用户意图 → 执行终点映射

| 用户说 | 执行到 | 说明 |
|--------|--------|------|
| "造一个用户" / "创建用户" / "授信" | 阶段 1 | |
| "绑卡" | 阶段 2 | 需提供 mobile |
| "借款成功" / "放款成功" | 阶段 4 | 从阶段 1 开始直到放款成功 |
| "可以还款的数据" | 阶段 5 | 从阶段 1 到账单初始化完成 |
| "还款成功" | 阶段 7 | 从阶段 1 到还款成功 |
| "逾期数据" / "造一笔逾期" | 阶段 5 | 阶段 4 后 init_bill 传 overdue_type='Y' |
| "部分还款成功" | 阶段 7 | 关注最终状态是否为 05 部分成功 |
| "代偿数据" | 阶段 * | 先造逾期，再调用 compensation |
| "H5 还款" / "优惠券还款" | 阶段 6 | 用 h5_repay（区别于阶段 6/7 的原子操作）|

---

### 执行规则

1. **跳过规则**
   - 用户提供了 mobile → 跳过阶段 1（用户已存在）
   - 用户提供了 loan_no → 跳过阶段 1-4，从阶段 5 开始

2. **失败处理**
   - 每个 tool 返回 success=True/False
   - 失败时不要继续后续阶段，报告当前状态和失败原因
   - 放款失败(fund_fail) → 告知用户资方拒绝，建议换手机号重试
   - 放款超时(lcs_success) → 建议再次调用 query_loan_status 重试

3. **参数默认值**
   - env: 默认 'BM_SIT'，用户指定则用指定的
   - amt: 默认 3000，范围 1000-10000
   - term: 默认 12，可选 3/6/9/12
   - 所有参数都有合理默认值，用户不指定时直接用默认值

4. **执行前检查**
   - 每个 tool 的 description 中标明了前置条件
   - 检查上一阶段的返回值是否满足下一阶段的前置条件
   - 不确定时用 query_loan_status 或 h5_get_url 探测当前状态
"""


# ============================================================
# 工厂函数：创建配置好的 MCP 实例
# ============================================================
def create_mcp() -> FastMCP:
    """
    创建并返回一个配置完整的 FastMCP 实例。
    已注册 lifecycle_guide prompt 和全部 13 个 tool。
    支持两种传输模式：
      - stdio:   mcp.run(transport="stdio")
      - HTTP:    mcp.sse_app() 作为 ASGI 子应用挂载
    """
    mcp = FastMCP(
        name="webtools-data-generator",
        instructions="""
你是一个消费金融测试数据生成器。
根据用户的自然语言指令，自动编排下方注册的 tool 来生成测试数据。

基本规则：
- 用户说"借款成功" → 从 credit_apply 开始，一路执行到 query_loan_status 返回放款成功
- 用户说"可以还款/还款成功" → 继续往下执行到 init_bill 或 h5_repay
- 用户给了 mobile → 跳过生成用户，从该 mobile 已有的阶段继续
- 用户给了 loan_no → 跳过生成用户和借款，直接 init_bill 或 h5_repay
- 每步失败时停止并报告原因，不要盲目继续

完整指引见 lifecycle_guide prompt。
""",
    )

    @mcp.prompt(
        name="lifecycle_guide",
        description="借贷数据生成完整生命周期指引。调用方 AI 应在处理造数请求前阅读此 Prompt，以理解各阶段依赖关系和执行规则。"
    )
    async def lifecycle_guide() -> str:
        return LIFECYCLE_GUIDE

    _register_tools(mcp)
    return mcp


# ============================================================
# stdio 启动入口（本地开发 / Claude Code 直连）
# ============================================================
if __name__ == "__main__":
    mcp = create_mcp()
    mcp.run(transport="stdio")
