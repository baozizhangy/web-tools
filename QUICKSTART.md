# 快速开始指南

## 1. 环境准备

### 安装pytest

```bash
pip install pytest
```

### 验证安装

```bash
pytest --version
```

## 2. 项目结构

```
webtools/
├── tests/
│   ├── conftest.py                    # pytest配置和公共fixture
│   ├── test_user_interface.py         # 用户相关接口测试
│   ├── test_credit_interface.py       # 授信相关接口测试
│   ├── test_card_interface.py         # 绑卡相关接口测试
│   ├── test_draw_interface.py         # 借款相关接口测试
│   ├── test_repay_interface.py        # 还款相关接口测试
│   ├── test_privilege_interface.py    # 权益相关接口测试
│   ├── README.md                      # 详细文档
│   └── logs/                          # 测试日志
├── pytest.ini                         # pytest配置
├── run_tests.py                       # 测试运行脚本
└── ...其他项目文件
```

## 3. 快速运行测试

### 方式一：使用pytest命令

```bash
# 进入项目根目录
cd d:\tools\webtools

# 运行所有测试
pytest tests/ -v

# 运行特定测试文件
pytest tests/test_user_interface.py -v

# 运行特定测试类
pytest tests/test_user_interface.py::TestUserInterface -v

# 运行特定测试方法
pytest tests/test_user_interface.py::TestUserInterface::test_check_user_success -v
```

### 方式二：使用运行脚本

```bash
# 运行所有测试
python run_tests.py all

# 运行特定类型的测试
python run_tests.py user      # 用户相关
python run_tests.py credit    # 授信相关
python run_tests.py card      # 绑卡相关
python run_tests.py draw      # 借款相关
python run_tests.py repay     # 还款相关
python run_tests.py privilege # 权益相关
```

## 4. 测试分类

### 用户相关接口 (test_user_interface.py)

```bash
pytest tests/test_user_interface.py -v
```

**包含的测试：**
- 撞库接口
- 风控白名单接口

### 授信相关接口 (test_credit_interface.py)

```bash
pytest tests/test_credit_interface.py -v
```

**包含的测试：**
- 发起授信
- 查询授信结果
- 不同金额授信
- 不同期限授信

### 绑卡相关接口 (test_card_interface.py)

```bash
pytest tests/test_card_interface.py -v
```

**包含的测试：**
- 查询银行列表
- 查询绑卡信息
- 获取绑卡验证码
- 校验绑卡验证码
- 不同绑卡场景

### 借款相关接口 (test_draw_interface.py)

```bash
pytest tests/test_draw_interface.py -v
```

**包含的测试：**
- 查询协议列表
- 借款试算
- 借款提交
- 发送验证码
- 校验验证码
- 查询借款步骤
- 查询借款结果
- 查询借据和还款计划

### 还款相关接口 (test_repay_interface.py)

```bash
pytest tests/test_repay_interface.py -v
```

**包含的测试：**
- 当期还款试算
- 逾期还款试算
- 提前结清试算
- 还款提交
- 查询还款结果

### 权益相关接口 (test_privilege_interface.py)

```bash
pytest tests/test_privilege_interface.py -v
```

**包含的测试：**
- 查询权益状态
- 查询权益exposure
- 查询权益信息
- 查询账单权益信息
- 查询权益结果和当前状态

## 5. 常用命令

```bash
# 详细输出（显示每个测试的详细信息）
pytest tests/ -v

# 显示打印语句
pytest tests/ -s

# 显示最慢的10个测试
pytest tests/ --durations=10

# 失败时立即停止
pytest tests/ -x

# 显示本地变量
pytest tests/ -l

# 只运行失败的测试
pytest tests/ --lf

# 运行上次失败的测试，然后运行其他测试
pytest tests/ --ff
```

## 6. 查看测试结果

### 控制台输出

测试完成后，会在控制台显示：

```
tests/test_user_interface.py::TestUserInterface::test_check_user_success PASSED
tests/test_user_interface.py::TestUserInterface::test_risk_white_user_success PASSED
...

======================== 10 passed in 5.23s ========================
```

### 日志文件

详细的测试日志保存在 `tests/logs/pytest.log`

查看日志：

```bash
# Windows
type tests\logs\pytest.log

# Linux/Mac
cat tests/logs/pytest.log

# 查看最后100行
tail -100 tests/logs/pytest.log
```

## 7. 测试数据说明

### 随机生成用户数据

每次测试运行时，框架会自动生成随机的用户数据：

- 手机号：随机生成
- 姓名：随机生成
- 身份证号：随机生成

这确保了测试的独立性和可重复性。

### 查看生成的用户数据

在测试日志中可以看到生成的用户数据：

```
开始执行测试: test_check_user_success
调用/userAccess接口::mobile::15605786856,name::朱镨,id_card::513029199609289243
```

## 8. 常见问题

### Q: 测试失败，提示"导入错误"

**A:** 确保在项目根目录运行pytest：

```bash
cd d:\tools\webtools
pytest tests/
```

### Q: 测试失败，提示"连接错误"

**A:** 检查以下几点：

1. 网络连接是否正常
2. API服务是否可用
3. 环境配置是否正确（BM_SIT/DEV）

### Q: 如何修改测试环境？

**A:** 编辑 `tests/conftest.py`：

```python
@pytest.fixture(scope="session")
def env():
    """测试环境配置"""
    return 'BM_SIT'  # 改为 'DEV' 或其他环境
```

### Q: 如何修改测试渠道？

**A:** 编辑 `tests/conftest.py`：

```python
@pytest.fixture(scope="session")
def channel():
    """渠道配置"""
    return 'lxj'  # 改为其他渠道
```

### Q: 如何只运行某个测试类？

**A:** 使用 `::` 指定：

```bash
pytest tests/test_user_interface.py::TestUserInterface -v
```

### Q: 如何只运行某个测试方法？

**A:** 使用 `::` 指定：

```bash
pytest tests/test_user_interface.py::TestUserInterface::test_check_user_success -v
```

## 9. 下一步

1. **运行第一个测试**

   ```bash
   pytest tests/test_user_interface.py::TestUserInterface::test_check_user_success -v
   ```

2. **查看测试日志**

   ```bash
   cat tests/logs/pytest.log
   ```

3. **运行所有用户相关测试**

   ```bash
   pytest tests/test_user_interface.py -v
   ```

4. **运行所有接口测试**

   ```bash
   pytest tests/ -v
   ```

5. **查看详细文档**

   打开 `tests/README.md` 了解更多信息

## 10. 支持的Python版本

- Python 3.7+
- Python 3.8+
- Python 3.9+
- Python 3.10+
- Python 3.11+

## 11. 获取帮助

- 查看详细文档：`tests/README.md`
- 查看测试日志：`tests/logs/pytest.log`
- 查看pytest官方文档：https://docs.pytest.org/
