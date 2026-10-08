#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
fixture中定义函数所接收的参数request：
request.node: 代表当前执行的测试节点（测试函数或模块）。
request.function: 代表当前执行的测试函数。
request.cls: 如果测试函数是在一个类中定义的，那么这个属性代表这个类。
request.module: 代表当前执行的测试模块。
request.config: 提供对配置对象的访问，可以用来获取和修改 Pytest 的配置选项。
request.param: 当使用参数化测试时，可以通过这个属性访问当前参数化的值。
"""
import allure, pytest, yaml, os
from config import db_conn
from utils.logger_util import auto_logger
from utils.personal_util import get_mobile_no
from config import get_urls

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
@allure.step("生成初始化测试手机号")
def get_init_mobile():
    """生成初始化测试手机号"""
    with allure.step("生成初始化测试手机号"):
        mobile = get_mobile_no()
    return mobile


@pytest.fixture
@allure.step("获取测试url")
def get_init_url(env):
    """获取测试url"""
    with allure.step("获取测试url"):
        url = get_urls(env)['FUND_LOAN']
    return url



@allure.step("获取测试数据")
def get_case_data(case_path):
    """获取测试数据"""
    file_path = os.path.join(project_path, case_path)
    with open(file_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
        return data


@pytest.fixture(scope='function')
def check_pre_data():
    """
    前置条件
    """

    pass


def assert_response(resp, expected_code):
    assert resp.status_code == expected_code, f"期望状态码 {expected_code}，实际 {resp.status_code}，响应 {resp.text}"
