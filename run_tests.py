#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pytest测试运行脚本
支持不同的测试执行模式和Allure报告生成
"""
import subprocess
import sys
import os
import shutil
from pathlib import Path


# 统一报告目录（与 pytestAutoTest 保持一致）
REPORTS_DIR = Path('reports')
ALLURE_RESULTS = REPORTS_DIR / 'allure_results'
ALLURE_REPORT = REPORTS_DIR / 'allure-reports'


def clean_report_dir():
    """清理旧的 allure_results，保留已有报告目录结构"""
    if ALLURE_RESULTS.exists():
        shutil.rmtree(ALLURE_RESULTS)
    ALLURE_RESULTS.mkdir(parents=True, exist_ok=True)
    ALLURE_REPORT.mkdir(parents=True, exist_ok=True)


def run_tests(test_type='all', verbose=True, generate_report=True):
    """
    运行测试
    :param test_type: 测试类型
        - all: 运行所有测试
        - user: 运行用户相关接口测试
        - credit: 运行授信相关接口测试
        - card: 运行绑卡相关接口测试
        - draw: 运行借款相关接口测试
        - repay: 运行还款相关接口测试
        - privilege: 运行权益相关接口测试
        - smoke: 运行冒烟测试
    :param verbose: 是否详细输出
    :param generate_report: 是否生成Allure报告
    """
    
    # 获取项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 清理旧报告
    clean_report_dir()
    
    # 构建pytest命令
    cmd = ['pytest', 'tests/']
    
    # 根据测试类型添加标记
    if test_type != 'all':
        cmd.extend(['-m', test_type])
    
    # 添加详细输出选项
    if verbose:
        cmd.append('-v')
    
    # 添加日志输出
    cmd.append('--tb=short')
    
    print(f"执行命令: {' '.join(cmd)}")
    print("=" * 60)
    
    # 执行测试
    result = subprocess.run(cmd)
    
    # 生成Allure报告
    if generate_report:
        print("\n" + "=" * 60)
        print("生成Allure报告...")
        print("=" * 60)
        generate_allure_report()
    
    return result.returncode


def generate_allure_report():
    """生成Allure报告"""
    try:
        cmd = [
            'allure', 'generate',
            str(ALLURE_RESULTS),
            '-o', str(ALLURE_REPORT),
            '--clean'
        ]
        
        print(f"执行命令: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Allure报告生成成功！")
            print(f"📊 报告位置: {ALLURE_REPORT / 'index.html'}")
            print("\n💡 查看报告:")
            print(f"   Windows: start {ALLURE_REPORT}\\index.html")
            print(f"   Linux/Mac: open {ALLURE_REPORT}/index.html")
        else:
            print("❌ Allure报告生成失败")
            print(f"错误信息: {result.stderr}")
    except FileNotFoundError:
        print("❌ 未找到allure命令，请先安装allure")
        print("   安装方法: scoop install allure  或  npm install -g allure-commandline")


def run_specific_test(test_file, generate_report=True):
    """
    运行特定的测试文件
    :param test_file: 测试文件名，如 test_user_interface.py
    :param generate_report: 是否生成Allure报告
    """
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 清理旧报告
    clean_report_dir()
    
    cmd = ['pytest', f'tests/{test_file}', '-v', '--tb=short']
    
    print(f"执行命令: {' '.join(cmd)}")
    print("=" * 60)
    
    result = subprocess.run(cmd)
    
    # 生成Allure报告
    if generate_report:
        print("\n" + "=" * 60)
        print("生成Allure报告...")
        print("=" * 60)
        generate_allure_report()
    
    return result.returncode


def run_specific_test_class(test_file, test_class, generate_report=True):
    """
    运行特定的测试类
    :param test_file: 测试文件名
    :param test_class: 测试类名
    :param generate_report: 是否生成Allure报告
    """
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 清理旧报告
    clean_report_dir()
    
    cmd = ['pytest', f'tests/{test_file}::{test_class}', '-v', '--tb=short']
    
    print(f"执行命令: {' '.join(cmd)}")
    print("=" * 60)
    
    result = subprocess.run(cmd)
    
    # 生成Allure报告
    if generate_report:
        print("\n" + "=" * 60)
        print("生成Allure报告...")
        print("=" * 60)
        generate_allure_report()
    
    return result.returncode


def run_specific_test_method(test_file, test_class, test_method, generate_report=True):
    """
    运行特定的测试方法
    :param test_file: 测试文件名
    :param test_class: 测试类名
    :param test_method: 测试方法名
    :param generate_report: 是否生成Allure报告
    """
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 清理旧报告
    clean_report_dir()
    
    cmd = ['pytest', f'tests/{test_file}::{test_class}::{test_method}', '-v', '--tb=short']
    
    print(f"执行命令: {' '.join(cmd)}")
    print("=" * 60)
    
    result = subprocess.run(cmd)
    
    # 生成Allure报告
    if generate_report:
        print("\n" + "=" * 60)
        print("生成Allure报告...")
        print("=" * 60)
        generate_allure_report()
    
    return result.returncode


if __name__ == '__main__':
    if len(sys.argv) > 1:
        test_type = sys.argv[1]
        exit_code = run_tests(test_type)
    else:
        # 默认运行所有测试
        exit_code = run_tests('all')
    
    sys.exit(exit_code)
