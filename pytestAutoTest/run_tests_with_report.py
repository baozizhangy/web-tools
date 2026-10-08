


# !/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
执行 pytest 测试。报告生成与推送在 conftest 钩子中处理。
"""

import subprocess
import sys
import time
import os
import re
import webbrowser

# 添加项目根目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.logger_util import auto_logger


def run_pytest_tests(test_path="case/app/bm_api_case/", verbose=True):
    """
    运行pytest测试
    :param test_path: 测试路径
    :param verbose: 是否详细输出
    :return: 测试结果
    """
    try:
        # 构造pytest命令
        cmd = ["python", "-m", "pytest", test_path]
        if verbose:
            cmd.append("-v")

        auto_logger.info(f"执行测试命令: {' '.join(cmd)}")

        # 记录开始时间
        start_time = time.time()

        # 执行测试
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())

        # 记录结束时间
        end_time = time.time()
        duration = end_time - start_time

        # 输出结果
        auto_logger.info(f"测试执行完成，耗时: {duration:.2f}秒")
        auto_logger.info(f"返回码: {result.returncode}")

        if result.stdout:
            auto_logger.info(f"标准输出:\n{result.stdout}")

        if result.stderr:
            auto_logger.error(f"错误输出:\n{result.stderr}")

        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "duration": duration
        }
    except Exception as e:
        auto_logger.error(f"执行测试异常: {e}")
        return None


def main():
    """主函数"""
    auto_logger.info("开始执行BM接口自动化测试")

    # 切换到pytestAutoTest目录
    current_dir = os.getcwd()
    pytest_dir = os.path.join(current_dir, "pytestAutoTest")
    if os.path.exists(pytest_dir):
        os.chdir(pytest_dir)
        auto_logger.info(f"切换工作目录到: {pytest_dir}")

    # 执行测试（报告生成与推送由 conftest 钩子接管）
    test_result = run_pytest_tests()
    if not test_result:
        auto_logger.error("测试执行失败")
        sys.exit(1)

    sys.exit(test_result["returncode"])

    # 保留：如有需要，可在本地手动执行：
    # allure generate reports/allure_results -o reports/allure-report --clean


if __name__ == "__main__":
    main()