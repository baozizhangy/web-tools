# 接口自动化测试框架

## 项目概述

这是一个基于pytest的接口自动化测试框架，用于测试借贷业务系统的API接口。框架支持单接口测试和业务场景测试。

## 项目结构

```
tests/
├── conftest.py                    # pytest配置和公共fixture
├── test_user_interface.py         # 用户相关接口测试
├── test_credit_interface.py       # 授信相关接口测试
├── test_card_interface.py         # 绑卡相关接口测试
├── test_draw_interface.py         # 借款相关接口测试
├── test_repay_interface.py        # 还款相关接口测试
├── test_privilege_interface.py    # 权益相关接口测试
└── logs/                          # 测试日志目录
```

## 环境要求

- Python 3.7+
- pytest
- requests

## 安装依赖

```bash
pip install pytest requests
```

## 配置说明

### 环境配置

在 `conftest.py` 中配置测试环境：

```python
@pytest.fixture(scope="session")
def env():
    """测试环境配置"""
    return 'BM_SIT'  # 可选值: BM_SIT, DEV, PROD
```

### 渠道配置

```python
@pytest.fixture(scope="session")
def channel():
    """渠道配置"""
    return 'lxj'  # 根据实际渠道修改
```

## 测试用例说明

### 1. 用户相关接口测试 (`test_user_interface.py`)

测试用户撞库和风控白名单功能：

- `test_check_user_success` - 撞库成功场景
- `test_check_user_with_id_card` - 带身份证号的撞库
- `test_risk_white_user_success` - 风控白名单添加成功
- `test_risk_white_user_response_structure` - 风控白名单响应结构验证
- `test_check_user_multiple_users` - 多用户撞库测试

### 2. 授信相关接口测试 (`test_credit_interface.py`)

测试授信申请和查询功能：

- `test_credit_apply_success` - 发起授信成功
- `test_credit_apply_response_structure` - 授信响应结构验证
- `test_credit_apply_result_query` - 查询授信结果
- `test_credit_apply_result_with_invalid_credit_req_no` - 无效creditReqNo查询
- `test_credit_apply_with_different_amounts` - 不同金额授信
- `test_credit_apply_with_different_terms` - 不同期限授信

### 3. 绑卡相关接口测试 (`test_card_interface.py`)

测试银行卡绑定功能：

- `test_bank_list_query_success` - 查询支持的银行列表
- `test_card_query_with_valid_user_no` - 查询绑卡信息
- `test_card_bind_success` - 获取绑卡验证码
- `test_card_bind_sms_success` - 校验绑卡验证码
- `test_card_bind_different_scenes` - 不同绑卡场景

### 4. 借款相关接口测试 (`test_draw_interface.py`)

测试借款申请和查询功能：

- `test_agreement_list_success` - 查询协议列表
- `test_agreement_list_different_scenes` - 不同协议场景
- `test_draw_trial_success` - 借款试算
- `test_draw_trial_with_privilege` - 带权益的借款试算
- `test_draw_submit_success` - 借款提交
- `test_send_sms_code_success` - 发送验证码
- `test_send_sms_success` - 校验验证码
- `test_draw_step_query_success` - 查询借款步骤
- `test_draw_result_query_success` - 查询借款结果
- `test_loan_play_query_success` - 查询借据和还款计划

### 5. 还款相关接口测试 (`test_repay_interface.py`)

测试还款功能：

- `test_repay_trial_current_period_success` - 当期还款试算
- `test_repay_trial_overdue_single_period_success` - 逾期单期还款试算
- `test_repay_trial_overdue_multiple_periods_success` - 逾期多期还款试算
- `test_repay_trial_early_settlement_success` - 提前结清试算
- `test_repay_submit_success` - 还款提交
- `test_repay_submit_different_types` - 不同还款类型
- `test_repay_result_query_success` - 查询还款结果

### 6. 权益相关接口测试 (`test_privilege_interface.py`)

测试权益功能：

- `test_privilege_status_success` - 查询权益状态
- `test_privilege_exposure_success` - 查询权益exposure
- `test_privilege_info_success` - 查询权益信息
- `test_bill_privilege_info_success` - 查询账单权益信息
- `test_profit_status_query_success` - 查询权益结果和当前状态

## 运行测试

### 运行所有测试

```bash
pytest tests/
```

或使用运行脚本：

```bash
python run_tests.py all
```

### 运行特定类型的测试

```bash
# 运行用户相关接口测试
pytest tests/ -m user

# 运行授信相关接口测试
pytest tests/ -m credit

# 运行绑卡相关接口测试
pytest tests/ -m card

# 运行借款相关接口测试
pytest tests/ -m draw

# 运行还款相关接口测试
pytest tests/ -m repay

# 运行权益相关接口测试
pytest tests/ -m privilege
```

### 运行特定的测试文件

```bash
pytest tests/test_user_interface.py -v
```

### 运行特定的测试类

```bash
pytest tests/test_user_interface.py::TestUserInterface -v
```

### 运行特定的测试方法

```bash
pytest tests/test_user_interface.py::TestUserInterface::test_check_user_success -v
```

### 运行冒烟测试

```bash
pytest tests/ -m smoke
```

## 测试报告

测试完成后，日志文件保存在 `tests/logs/pytest.log`

查看测试报告：

```bash
# 查看最后的测试摘要
pytest tests/ -v --tb=short

# 生成HTML报告（需要安装pytest-html）
pip install pytest-html
pytest tests/ --html=report.html
```

## 常用命令

```bash
# 详细输出
pytest tests/ -v

# 显示打印语句
pytest tests/ -s

# 显示最慢的10个测试
pytest tests/ --durations=10

# 失败时立即停止
pytest tests/ -x

# 显示本地变量
pytest tests/ -l

# 并行运行测试（需要安装pytest-xdist）
pip install pytest-xdist
pytest tests/ -n auto
```

## 测试数据

### 用户数据生成

测试框架使用 `personal_util` 模块自动生成随机用户数据：

- `get_mobile_no()` - 生成随机手机号
- `get_person_name()` - 生成随机姓名
- `get_id_no()` - 生成随机身份证号

每次测试运行时，都会生成新的随机用户数据，确保测试的独立性。

### 自定义用户数据

如需使用特定的用户数据，可以在测试中直接指定：

```python
def test_with_specific_user(env, channel):
    api = BmApi(
        channel_id=channel,
        mobile='15605786856',
        name='朱镨',
        id_card='513029199609289243',
        env=env
    )
    response = api.check_user()
    assert response is not None
```

## 断言工具

框架提供了两个常用的断言工具函数：

### `assert_response_success(response, expected_result=1)`

验证API响应成功：

```python
response = api.credit_apply()
assert_response_success(response, expected_result=1)
```

### `assert_response_has_field(response, field_path)`

验证响应包含指定字段：

```python
response = api.credit_apply()
fund_credit_no = assert_response_has_field(response, 'bizData.fundCreditNo')
```

## 日志输出

所有测试都会自动记录日志，包括：

- 测试开始和结束时间
- 测试用户信息
- API请求和响应
- 断言结果

日志输出到控制台和文件 `tests/logs/pytest.log`

## 常见问题

### 1. 导入错误

如果遇到导入错误，确保项目根目录在Python路径中。conftest.py已自动处理此问题。

### 2. 测试失败

检查以下几点：

- 环境配置是否正确（BM_SIT/DEV）
- 网络连接是否正常
- API服务是否可用
- 测试数据是否有效

### 3. 日志目录不存在

如果 `tests/logs/` 目录不存在，pytest会自动创建。

## 扩展测试

### 添加新的测试文件

1. 在 `tests/` 目录下创建新的测试文件，命名为 `test_*.py`
2. 导入 `conftest` 中的fixture和断言工具
3. 编写测试类和测试方法

示例：

```python
import pytest
from conftest import assert_response_success
from utils.logger_util import web_logger

class TestNewInterface:
    def test_new_api(self, api_with_user_data):
        web_logger.info("测试新接口")
        response = api_with_user_data.some_method()
        assert_response_success(response)
```

### 添加新的标记

在 `pytest.ini` 中添加新的标记定义：

```ini
markers =
    new_mark: 新的标记
```

然后在测试中使用：

```python
@pytest.mark.new_mark
def test_something():
    pass
```

## 最佳实践

1. **前置条件清晰** - 在测试中明确说明前置条件
2. **断言明确** - 使用有意义的断言消息
3. **日志详细** - 记录关键步骤和数据
4. **数据隔离** - 使用随机数据避免测试间干扰
5. **错误处理** - 验证错误场景和边界情况

## 联系方式

如有问题或建议，请联系测试团队。
