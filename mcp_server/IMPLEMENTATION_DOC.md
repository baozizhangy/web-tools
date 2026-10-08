# MCP Server 技术实现文档

## 一、我们要做什么

在现有项目 `D:\tools\webtools` 内新建 `mcp_server/` 目录，基于 Python `mcp` 包（v1.27.1）的 `FastMCP` 框架，将前端已有的 12 个造数入口包装为 MCP tool。调用方 AI 通过自然语言触发，MCP server 自动编排调用链并返回结果。

核心原则：**只写薄包装，不写业务逻辑；只写指引，不写死流程。**

---

## 二、整体架构

```
┌─────────────────────────────────────────────────────┐
│  调用方 (Claude Desktop / Claude Code / 其他AI)      │
│  "帮我造一笔借款成功的数据"                            │
└─────────────────┬───────────────────────────────────┘
                  │ MCP 协议 (stdio, JSON-RPC)
                  │ 交换内容：tool 元数据 + 调用参数 + 返回值
                  │ 不交换：源代码、数据库、配置
                  ▼
┌─────────────────────────────────────────────────────┐
│  mcp_server/server.py     ← MCP 入口                 │
│  ┌─────────────────────────────────────────────────┐│
│  │ FastMCP("webtools-data-generator")              ││
│  │                                                 ││
│  │ Prompt 模板  →  状态机 + 场景说明                 ││
│  │ Tool 注册    →  12 个 @mcp.tool() 装饰的函数      ││
│  └─────────────────────────────────────────────────┘│
│                  │ import                            │
├──────────────────┼──────────────────────────────────┤
│  mcp_server/tools.py  ← 12 个 tool 的薄包装实现        │
│  (每个 tool 15-20 行，直接调用现有业务函数)             │
└──────────────────┼──────────────────────────────────┘
                   │ import
                   ▼
┌─────────────────────────────────────────────────────┐
│  现有业务层（不改动）                                  │
│  api/app/h5_scene.py         → H5SceneService       │
│  api/app/h5_api.py           → H5Api                │
│  api/app/loan_bill.py        → LoanBill 等          │
│  djangoWebTools/tools/bm_tools/ → 各业务函数          │
│  config/                     → Nacos/MySQL/Redis    │
└─────────────────────────────────────────────────────┘
```

**关键点：** MCP server 和 Django 是平级进程，各自启动，共享底层模块。`mcp_server/` 不依赖 Django 的 request/response 层。

---

## 三、实现步骤总览

共 6 步，预计工作量约 **半天**：

| 步骤 | 内容 | 目的 |
|------|------|------|
| 1 | 环境准备 + 目录创建 | 安装 mcp SDK，建立文件骨架 |
| 2 | 实现 Prompt 模板 | AI 的"说明书"，决定编排正确率 |
| 3 | 实现 12 个 tool | 薄包装现有业务函数为 MCP tool |
| 4 | 实现 server.py 入口 | 组装 FastMCP，注册 tools + prompt |
| 5 | 配置 Claude Code 调用 | 编辑 `.mcp.json`，让 Claude Code 能发现 |
| 6 | 验证测试 | 用自然语言自测，修正 description |

---

## 四、分步详解

### 步骤 1：环境准备 + 目录创建

**目的：** 确保 MCP SDK 可用，创建最小文件骨架。

```bash
# 安装 mcp SDK
pip install mcp

# 创建目录
mkdir -p mcp_server

# 创建三个文件
# mcp_server/__init__.py      ← 空文件
# mcp_server/server.py        ← 步骤 4 实现
# mcp_server/tools.py         ← 步骤 3 实现
```

`__init__.py` 内容为空，仅标识为 Python 包。

---

### 步骤 2：实现 Prompt 模板

**目的：** 这是整个 MCP 最核心的部分。MCP 的 `Prompt` 机制会在调用方 AI 初始化连接时注入这段文本作为系统级指引。AI 根据这段文本理解：
- 整个业务有多少个阶段
- 每个阶段用什么 tool
- 什么场景执行到什么阶段为止

**文件位置：** `mcp_server/server.py` 内，通过 `@mcp.prompt()` 注册。

**内容框架：**

```python
@mcp.prompt(
    name="lifecycle_guide",
    description="借贷数据生成生命周期指引，调用方 AI 在发起任何造数操作前应阅读此指引。"
)
async def lifecycle_guide() -> str:
    return """
## 借贷数据生成状态机

### 业务背景
这是一个消费金融借贷平台，数据生成遵循以下链条：

    生成用户 → H5绑卡 → H5借款提交 → 完成放款 → 初始化账单 → 发起还款 → 查询还款结果
                                      ↓
                                 代偿（逾期后）

### 阶段与 Tool 对照表
| 阶段 | Tool | 前置条件 | 产出 |
|------|------|----------|------|
| 1. 生成用户 | generate_test_user | 无 | mobile, name, id_card, bank_card |
| 2. H5绑卡 | h5_bind_card | 已存在 mobile | 绑卡完成 |
| 3. H5借款 | h5_draw_submit | 已绑卡 | loanReqNo |
| 4. 完成放款 | query_loan_status | 已提交借款 | loan_no, 放款成功 |
| 5. 初始化账单 | init_bill | 已有 loan_no | 账单就绪 |
| 6. 发起还款 | h5_repay | 账单已初始化 | 还款结果 |
| 7. 查询还款 | query_repay_status | 已发起还款 | 还款终态 |
| *. 代偿 | compensation | loan_no 已逾期 | 代偿完成 |

### 用户意图 → 执行终点
| 用户说 | 执行到阶段 | 说明 |
|--------|-----------|------|
| "造一个用户" | 阶段1 | 只生成身份信息 |
| "绑卡" | 阶段2 | |
| "借款成功" | 阶段4 | 从阶段1执行到阶段4 |
| "可以还款的数据" | 阶段5 | 从阶段1执行到阶段5 |
| "还款成功" | 阶段7 | 从阶段1执行到阶段7 |
| "逾期数据" | 阶段5 | 阶段4后，阶段5传 overdue_type='Y' |
| "部分还款成功" | 阶段7 | 执行到阶段7，关注返回的 repay_state='05' |
| "代偿数据" | 阶段* | 先造逾期数据，再调用 compensation |

### 执行规则
1. 用户给了 mobile → 跳过阶段1
2. 用户给了 loan_no → 跳过阶段1-4，从阶段5开始
3. 每个阶段执行前检查前置条件是否满足
4. 阶段失败时不要继续，报告当前状态和失败原因
5. 环境默认 'BM_SIT'，用户指定则用指定的
6. 金额默认 3000（范围 1000-10000），期限默认 12（可选 3/6/9/12）

### 关键状态码含义
- 还款 result.status: 03=成功, 04=失败, 05=部分成功
- 放款成功: loan_state='DS'
    """
```

**为什么先写 Prompt 而不是先写 tool：** Prompt 定义了 AI 的行为边界和推理逻辑。先写它，就能以 AI 的视角验证"这个 tool 清单是否完整，阶段依赖是否清晰"。如果 Prompt 写出来发现某个场景缺失，说明 tool 设计有漏洞。

---

### 步骤 3：实现 12 个 tool

**目的：** 每个 tool 做三件事：
1. 接收调用方 AI 传来的参数
2. 调用现有业务函数
3. 返回结构化结果 + 下一步提示

所有 tool 放在 `mcp_server/tools.py`，每个 tool 是一个 async 函数，内部调用现有的同步业务函数。

#### Tool 分类

**第一类：完整场景 tool（自闭环，内部包含多步）**

| Tool | 包装的现有函数 | 内部包含的步骤 |
|------|---------------|---------------|
| h5_bind_card | H5SceneService.run_bind_card_scene() | 登录→卡bin查询→提交→验证→轮询 |
| h5_draw_submit | H5SceneService.run_draw_submit_scene() | 清理→登录→预查询→自动绑卡→试算→提交→验证 |
| h5_repay | H5SceneService.run_repay_scene() | 登录→查loanReqNo→账单详情→试算→提交→验证→查结果 |
| offline_oak_pay | offline_oak_pay_order() | 线下还款→批次job→轮询结清 |
| coupon_receive | update_excel_and_send() | 创建优惠券任务 |

**第二类：单步操作 tool**

| Tool | 包装的现有函数 | 说明 |
|------|---------------|------|
| generate_test_user | random_user_info() | 生成随机身份 |
| query_loan_status | query_order() | 触发放款任务+轮询 |
| query_repay_status | query_repay_result() | 触发还款任务+轮询 |
| init_bill | LoanBill.init_plan_1() | 初始化还款计划 |
| update_fund_mock | fund_plan_mock() | 更新资方mock |
| compensation | LoanCompensationFlow | 代偿全流程 |

**第三类：辅助 tool**

| Tool | 包装的现有函数 | 说明 |
|------|---------------|------|
| h5_get_url | H5Api.request_url() | 获取H5链接 |
| trigger_job | xxl_job_trigger() | 触发XXL-Job |

#### Tool 编写规范（每个 tool 必须遵守）

```python
async def example_tool(param1: str, param2: int = 3000, env: str = "BM_SIT") -> dict:
    """
    description 包含三要素：
    1. 这个 tool 做什么（一句话）
    2. 前置条件是什么
    3. 调用后返回什么，下一步该调什么
    
    参数使用 Python 类型注解 + 默认值，MCP 自动生成 schema
    """
    try:
        # 1. 调用现有业务函数（这是唯一的逻辑）
        result = SomeExistingService(param1, env).do_something(param2)
        
        # 2. 返回结构化结果 + 下一步提示
        return {
            "success": True,
            "data": result,
            "next_action": f"已完成 XXX。下一步应调用 next_tool_name(param='{param1}')。"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "suggestion": "建议检查参数或前置条件是否满足。"
        }
```

#### 关键 tool 实现示例（3 个代表）

**Tool 1: generate_test_user — 最简单的一类**

```python
from djangoWebTools.tools.query_user_info import random_user_info

async def generate_test_user(env: str = "BM_SIT") -> dict:
    """
    随机生成一个测试用户的身份信息，包括姓名、手机号、身份证号、银行卡号。
    
    前置条件：无。
    返回：mobile, name, id_card, bank_card。
    调用后：mobile 可直接用于后续的 h5_bind_card、h5_draw_submit 等操作。
    """
    try:
        user = random_user_info(env=env)
        return {
            "success": True,
            "mobile": user.get("mobile"),
            "name": user.get("name"),
            "id_card": user.get("id_card"),
            "bank_card": user.get("bank_card"),
            "env": env,
            "next_action": f"用户已生成，mobile={user.get('mobile')}。下一步可执行 h5_bind_card(mobile='{user.get('mobile')}') 进行绑卡。"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
```

**Tool 2: h5_draw_submit — 有复杂入参的一类**

```python
from api.app.h5_scene import H5SceneService

async def h5_draw_submit(
    mobile: str,
    amt: int = 3000,
    term: int = 12,
    is_privilege_process: str = "N",
    env: str = "BM_SIT"
) -> dict:
    """
    发起 H5 借款申请，自动完成数据清理、登录、绑卡检测/自动绑卡、试算和提交。不包含放款。
    
    前置条件：用户已存在且已绑卡（如未绑卡会自动绑卡）。
    参数：
      mobile: 手机号（必填）
      amt: 借款金额，1000-10000，默认 3000
      term: 借款期限，可选 3/6/9/12，默认 12
      is_privilege_process: 是否购买权益，'Y' 或 'N'，默认 'N'
      env: 环境，默认 'BM_SIT'
    返回：loanReqNo（借款申请号）。
    调用后：必须调用 query_loan_status(mobile, env) 触发放款并轮询到放款成功。
    """
    try:
        service = H5SceneService(mobile=mobile, env=env)
        result = service.run_draw_submit_scene(
            loan_amt=amt,
            loan_term=term,
            is_privilege_process=is_privilege_process,
        )
        return {
            "success": True,
            "mobile": mobile,
            "loanReqNo": result.get("loanReqNo"),
            "applyNo": result.get("applyNo"),
            "steps": result.get("steps"),
            "next_action": f"借款已提交，loanReqNo={result.get('loanReqNo')}。下一步调用 query_loan_status(mobile='{mobile}', env='{env}') 触发放款并等待成功。"
        }
    except Exception as e:
        return {"success": False, "error": str(e), "mobile": mobile}
```

**Tool 3: init_bill — 有枚举约束的一类**

```python
from typing import Literal
from api.app.loan_bill import LoanBill

async def init_bill(
    loan_no: str,
    overdue_type: Literal["N", "Y"] = "N",
    day: int = 0,
    env: str = "BM_SIT"
) -> dict:
    """
    初始化借据的还款计划（计息计费）。支持正常账单和逾期账单。
    
    前置条件：借据已放款成功（有 loan_no）。
    参数：
      loan_no: 借据号（必填）
      overdue_type: 'N'=正常账单, 'Y'=逾期账单，默认 'N'
      day: 逾期天数（overdue_type='Y' 时必填）
      env: 环境，默认 'BM_SIT'
    返回：初始化结果。
    调用后：
      - 正常账单：可调用 h5_repay 发起还款
      - 逾期账单：可调用 compensation 执行代偿
    """
    try:
        bill = LoanBill(loan_no=loan_no, overdue_type=overdue_type, day=day, bill_day=True, env=env)
        res = bill.init_plan_1()
        if res[0] == 'S':
            status = "账单初始化成功"
        elif res[0] == 'F':
            status = "试算接口超时，需手动触发计息"
        else:
            status = "初始化异常"
        
        next_action = ""
        if overdue_type == 'Y':
            next_action = f"逾期账单已初始化。可调用 compensation(loan_no='{loan_no}', env='{env}') 执行代偿。"
        else:
            next_action = f"账单已初始化。可调用 h5_repay(mobile=<手机号>, loan_no='{loan_no}', env='{env}') 发起还款。"
        
        return {
            "success": True,
            "loan_no": loan_no,
            "status": status,
            "overdue_type": overdue_type,
            "next_action": next_action
        }
    except Exception as e:
        return {"success": False, "loan_no": loan_no, "error": str(e)}
```

**其余 9 个 tool 按相同模式编写，不再展开。** 每个都是 15-20 行的薄包装。

---

### 步骤 4：实现 server.py 入口

**目的：** 组装 FastMCP 实例，注册 Prompt 和所有 tool，启动 stdio 服务。

```python
# mcp_server/server.py
"""
WebTools 造数 MCP Server
启动方式: python -m mcp_server.server
"""

import sys
import os

# 确保项目根目录在 sys.path 中，以便 import 现有模块
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from mcp.server.fastmcp import FastMCP

# 1. 创建 MCP Server 实例
mcp = FastMCP(
    name="webtools-data-generator",
    instructions="""
    这是一个消费金融测试数据生成器。
    你可以根据用户的自然语言指令，自动编排并调用相应的 tool 来生成测试数据。
    完整的数据链路为：生成用户 → 绑卡 → 借款 → 放款 → 初始化账单 → 还款。
    详见 lifecycle_guide prompt。
    """
)


# 2. 注册 Prompt 模板（步骤 2 的内容）
@mcp.prompt(
    name="lifecycle_guide",
    description="借贷数据生成生命周期指引"
)
async def lifecycle_guide() -> str:
    return """
## 借贷数据生成状态机
...（步骤 2 的完整内容）
"""


# 3. 注册所有 tools（从 tools.py 导入）
from mcp_server.tools import (
    generate_test_user,
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

mcp.tool()(generate_test_user)
mcp.tool()(h5_bind_card)
mcp.tool()(h5_draw_submit)
mcp.tool()(h5_repay)
mcp.tool()(h5_get_url)
mcp.tool()(offline_oak_pay)
mcp.tool()(coupon_receive)
mcp.tool()(init_bill)
mcp.tool()(query_loan_status)
mcp.tool()(query_repay_status)
mcp.tool()(update_fund_mock)
mcp.tool()(compensation)
mcp.tool()(trigger_job)


# 4. 启动入口
if __name__ == "__main__":
    mcp.run(transport="stdio")
```

**为什么使用 `mcp.tool()(func)` 而不是 `@mcp.tool()` 装饰器：** 因为 tool 函数定义在 `tools.py` 中，用这种注册方式可以保持文件分离——`server.py` 只管组装，`tools.py` 只管实现。

---

### 步骤 5：配置 Claude Code 调用

**目的：** 让 Claude Code 能发现并调用你的 MCP server。

在项目根目录创建或编辑 `.mcp.json`：

```json
{
  "mcpServers": {
    "webtools-data-generator": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "D:\\tools\\webtools"
    }
  }
}
```

配置后重启 Claude Code，它会在启动时自动连接该 MCP server。

**连接过程：**
1. Claude Code 启动 → 读取 `.mcp.json`
2. 启动 `python -m mcp_server.server` 进程
3. MCP 初始化握手 → 传输 tool 列表 + prompt
4. 用户在对话框输入 → AI 根据 tool 列表和 prompt 决策调用

---

### 步骤 6：验证测试

**目的：** 验证 AI 能否正确理解自然语言并编排 tool 调用链。

用以下测试用例验证：

| 测试输入 | 期望 AI 调用的 tool 链 |
|----------|----------------------|
| "生成一个测试用户" | generate_test_user |
| "帮我造一笔借款成功的数据" | generate_test_user → h5_bind_card → h5_draw_submit → query_loan_status |
| "造一笔逾期的数据" | [同上] → init_bill(overdue_type='Y', day=5) |
| "用 loan_no=XXX 初始化账单" | init_bill(loan_no='XXX') |
| "给 mobile=139xxx 的用户绑卡" | h5_bind_card(mobile='139xxx') |
| "生成一笔 5000 元 6 期的借款" | generate_test_user → h5_bind_card → h5_draw_submit(amt=5000, term=6) → query_loan_status |
| "代偿数据" | [完整借款链条] → init_bill(overdue_type='Y') → compensation |

**如果某条指令 AI 没理解对** → 回改对应 tool 的 description 或 Prompt 模板，直到正确。

---

## 五、最终文件清单

```
新增文件：
  mcp_server/
  ├── __init__.py               # 空文件
  ├── server.py                 # ~100 行：FastMCP 组装 + Prompt + 注册
  └── tools.py                  # ~250 行：12 个 tool 函数

修改文件：
  .mcp.json                     # 新增 MCP server 配置（项目根目录）
  requirements.txt              # 添加 mcp>=1.27.0

不修改任何现有业务代码。
```

---

## 六、设计决策记录

| 决策 | 理由 |
|------|------|
| 使用 FastMCP（非底层 Server） | FastMCP 用装饰器注册 tool，代码更简洁 |
| stdio 传输（非 HTTP/SSE） | Claude Code 默认用 stdio，本地进程通信无网络开销 |
| tool 放在独立文件 tools.py | server.py 只组装，不写逻辑，便于维护 |
| tool 函数用 async | 虽然现有业务函数是同步的，但 MCP 协议本身是异步的，用 async 便于后续扩展 |
| 返回值统一包含 next_action | 即使 Prompt 模板已经告诉了 AI 下一步，返回值再次提示能提高编排正确率 |
| 不存在组合 tool | AI 根据 Prompt + description 自行推理编排，避免写死逻辑 |

---

## 七、后续扩展

| 优先级 | 扩展内容 | 方式 |
|--------|---------|------|
| 高 | 新造数场景 | 在 tools.py 中新增一个 tool，在 Prompt 中追加场景说明 |
| 中 | 环境切换支持更多 | 修改 env 参数的 Literal 类型 |
| 低 | SSE 流式进度 | MCP 支持 ProgressNotification，长耗时操作可改造 |
