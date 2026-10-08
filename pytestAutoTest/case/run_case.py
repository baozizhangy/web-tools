#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import subprocess
import sys

WIN = sys.platform.startswith('win')


def run(test_case_path=None, test_case_name=None):
    # pytestAutoTest/ 目录
    autoTestDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 测试结果目录
    allure_results = os.path.join(autoTestDir, 'reports', 'allure_results')
    # 测试报告目录
    allure_report = os.path.join(autoTestDir, 'reports', 'allure-reports')

    # 确保目录存在
    os.makedirs(allure_results, exist_ok=True)
    os.makedirs(allure_report, exist_ok=True)

    # 切换到测试目录
    original_cwd = os.getcwd()
    os.chdir(autoTestDir)

    try:
        # 根据提供的test_case_path和test_case_name构建pytest命令行参数
        command_args = [sys.executable, "-m", "pytest"]

        if test_case_path and test_case_name:
            command_args.append(f"{test_case_path}::{test_case_name}")
        elif test_case_path:
            command_args.append(test_case_path)

        # 添加其他参数
        command_args.extend([
            "-r", "1",  # 这代表rerun failed tests once ，错误后重试
            "--alluredir", "reports/allure_results",
            "--clean-alluredir",
            "-v"  # 详细输出
        ])

        steps = [
            command_args,
            ["allure", "generate", "reports/allure_results", "-c", "-o", "reports/allure-reports"],
            ["allure", "open", "reports/allure-reports"]
        ]

        for step in steps:
            try:
                print(f"执行命令: {' '.join(step)}")
                if step == command_args:
                    # pytest命令需要特殊处理
                    result = subprocess.run(step)
                    if result.returncode != 0:
                        print(f"命令执行失败，退出码: {result.returncode}")
                        return
                else:
                    subprocess.run(step)
            except FileNotFoundError:
                print(f"未找到命令: {step[0]}，请确保已安装相关工具")
                return
            except Exception as e:
                print(f"执行命令时出错: {e}")
                return
    finally:
        # 恢复原来的工作目录
        os.chdir(original_cwd)


if __name__ == "__main__":
    # 示例调用方法：
    # run(test_case_path="case/app/flow_case/test_0_credit.py::TestCredit", test_case_name="test_credit_success")
    # run(test_case_path="case/app/account_case/test_0_login.py")
    # run(test_case_path="case/app/account_case/test_0_login.py::TestAccount", test_case_name="test_login_success")
    # run(test_case_path="case/app/account_case/test_0_login.py::TestAccount")
    # BM API测试用例
    # run(test_case_path="case/app/bm_api_case/test_user_credit.py::TestUserCredit")
    # run(test_case_path="case/app/bm_api_case/test_user_credit.py::TestUserCredit::test_check_user")
    
    if len(sys.argv) > 1:
        # 如果提供了命令行参数，则使用参数
        if len(sys.argv) == 2:
            run(test_case_path=sys.argv[1])
        elif len(sys.argv) == 3:
            run(test_case_path=sys.argv[1], test_case_name=sys.argv[2])
    else:
        # 默认执行所有测试
        run()