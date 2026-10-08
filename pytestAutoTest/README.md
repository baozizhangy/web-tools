# pytest接口自动化测试框架

## 项目介绍
本项目是基于pytest的接口自动化测试框架，用于测试BM相关接口功能。

## 目录结构
```
pytestAutoTest/
├── case/                 # 测试用例目录
│   ├── app/              # APP相关接口测试
│   │   └── bm_api_case/  # BM接口测试用例
├── data/                 # 测试数据
├── reports/              # 测试报告
│   ├── allure_results/   # allure测试结果
│   └── allure_report/    # allure测试报告
├── business/             # 业务逻辑封装
└── utils/                # 工具类
```

## 环境准备
1. 安装Python 3.7+
2. 安装依赖包：`pip install -r requirements.txt`
3. 安装allure：[allure官网](https://docs.qameta.io/allure/)

## 运行测试

### 方式一：直接运行测试用例
```bash
# 运行所有测试用例
python -m pytest case/app/bm_api_case/ -v

# 运行指定测试用例
python -m pytest case/app/bm_api_case/test_complete_credit_flow.py -v
```

### 方式二：运行测试并推送报告到企业微信
```bash
python run_tests_with_report.py
```

## 查看测试报告
```bash
# 生成allure报告
allure generate reports/allure_results/ -o reports/allure_report/ --clean

# 打开allure报告
allure open reports/allure_report/
```

## 报告推送
测试执行完成后，会自动将测试结果推送到企业微信群机器人。
Webhook地址：https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=2cbcecaf-53aa-4367-aba5-1aac2005222d

推送内容包括：
- 测试用例总数
- 通过/失败/错误用例数
- 通过率
- 执行时长
- 报告访问链接（需要部署allure报告服务）

## 配置说明
- `pytest.ini`：pytest配置文件
- 测试结果默认保存在`reports/allure_results/`目录
- 测试报告默认生成在`reports/allure_report/`目录