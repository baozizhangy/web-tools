#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
测试配置与运行期钩子：
- 提供通用夹具
- 汇总执行结果并在会话结束生成 Allure 报告、可选推送企业微信
"""

import pytest,os
import allure
import time
from utils.logger_util import auto_logger
from utils.personal_util import get_mobile_no, get_id_no, get_person_name
from utils.allure_report_util import allure_report_util
from utils.mysql_util import MySQL
import os

# 导入配置模块
try:
    from config import db_conn, RUN_ENV
except ImportError:
    # 如果无法导入配置，使用默认配置
    db_conn = None
    RUN_ENV = None

# 模块级统计容器，避免从 report 上取 config
_TEST_STATS = {
    "start_time": None,
    "passed": 0,
    "failed": 0,
    "error": 0,
    "skipped": 0,
}

def pytest_addoption(parser):
    group = parser.getgroup("runtime options")
    group.addoption("--env", action="store", default="BM_SIT", help="运行环境，如 BM_SIT/BM_UAT")
    group.addoption(
        "--report", action="store", default="generate", choices=["generate", "none"],
        help="会话结束是否生成 Allure 报告"
    )
    group.addoption(
        "--notify", action="store", default="none", choices=["wechat", "none"],
        help="会话结束是否推送企业微信"
    )


def pytest_sessionstart(session):
    auto_logger.info("开始设置测试会话环境")
    _TEST_STATS["start_time"] = time.time()
    _TEST_STATS["passed"] = 0
    _TEST_STATS["failed"] = 0
    _TEST_STATS["error"] = 0
    _TEST_STATS["skipped"] = 0


def pytest_runtest_logreport(report):
    # 仅统计 call 阶段（不含 setup/teardown）
    if report.when != "call":
        return
    if report.passed:
        _TEST_STATS["passed"] += 1
    elif report.failed:
        # 统一计入 failed（pytest 不区分 assertion 与 error 到不同桶）
        _TEST_STATS["failed"] += 1
    elif report.skipped:
        _TEST_STATS["skipped"] += 1


@pytest.fixture
def test_data():
    """生成测试数据"""
    return {
        "mobile": get_mobile_no(),
        "name": get_person_name(),
        "id_card": get_id_no()
    }


@pytest.fixture
def logger():
    """提供日志记录器"""
    return auto_logger


@pytest.fixture
def api_client():
    """通用API客户端fixture"""
    # 这里可以返回一个基础的API客户端
    # 具体的API客户端可以在测试类中创建
    return None


@pytest.fixture(scope="session")
def db_connection():
    """
    创建数据库连接的fixture
    根据配置文件或环境变量获取数据库连接
    """
    # 获取运行环境，默认为BM_SIT
    env = os.environ.get('TEST_ENV') or RUN_ENV or "BM_SIT"
    
    # 尝试从配置文件获取数据库连接
    if db_conn:
        try:
            db = db_conn(env)
            auto_logger.info(f"成功从配置文件获取{env}环境数据库连接")
            yield db
            return
        except Exception as e:
            auto_logger.warning(f"从配置文件获取数据库连接失败: {e}")
    
    # 如果无法从配置文件获取，则使用默认配置
    auto_logger.info("使用默认配置创建数据库连接")
    db = MySQL(
        host="localhost",
        port=3306,
        user="root",
        password="password",
        db="test_db"
    )
    yield db
    # 连接会在MySQL类中自动管理


@pytest.fixture
def db_insert(db_connection):
    """
    数据库插入操作fixture
    用法: db_insert("INSERT INTO table (col1, col2) VALUES (%s, %s)", (val1, val2))
    """
    def _insert(sql, params=None):
        """
        插入数据
        
        Args:
            sql: SQL插入语句
            params: 参数元组或列表
            
        Returns:
            dict: 执行结果
        """
        return db_connection.exec_one(sql, params)
    
    return _insert


@pytest.fixture
def db_update(db_connection):
    """
    数据库更新操作fixture
    用法: db_update("UPDATE table SET col1=%s WHERE id=%s", (new_val, id))
    """
    def _update(sql, params=None):
        """
        更新数据
        
        Args:
            sql: SQL更新语句
            params: 参数元组或列表
            
        Returns:
            dict: 执行结果
        """
        return db_connection.exec_one(sql, params)
    
    return _update


@pytest.fixture
def db_delete(db_connection):
    """
    数据库删除操作fixture
    用法: db_delete("DELETE FROM table WHERE id=%s", (id,))
    """
    def _delete(sql, params=None):
        """
        删除数据
        
        Args:
            sql: SQL删除语句
            params: 参数元组或列表
            
        Returns:
            dict: 执行结果
        """
        return db_connection.exec_one(sql, params)
    
    return _delete


@pytest.fixture
def db_select(db_connection):
    """
    数据库查询操作fixture
    用法: db_select("SELECT * FROM table WHERE id=%s", (id,))
    """
    def _select(sql, params=None):
        """
        查询数据
        
        Args:
            sql: SQL查询语句
            params: 参数元组或列表
            
        Returns:
            list/dict: 查询结果
        """
        return db_connection.get_all(sql, params)
    
    return _select


@pytest.fixture
def db_transaction(db_connection):
    """
    数据库事务操作fixture
    支持多个SQL操作在一个事务中执行
    用法: db_transaction([sql1, sql2, ...])
    """
    def _execute_transaction(sql_list):
        """
        执行事务操作
        
        Args:
            sql_list: SQL语句列表
            
        Returns:
            dict: 执行结果
        """
        return db_connection.exe_multi(sql_list)
    
    return _execute_transaction


def pytest_sessionfinish(session, exitstatus):
    if _TEST_STATS["start_time"] is None:
        return
    duration = time.time() - _TEST_STATS["start_time"]

    # 按选项生成 Allure 报告
    report_opt = session.config.getoption("--report")
    if report_opt == "generate":
        try:
            allure_report_util.generate_allure_report(
                results_dir="./reports/allure_results",
                report_dir="./reports/allure-reports"
            )
        except Exception as e:
            auto_logger.error(f"生成 Allure 报告异常: {e}")

    # 生成报告后，如果开启通知，则带上本地报告地址（file:// 链接）
    notify_opt = session.config.getoption("--notify")
    if notify_opt == "wechat":
        try:
            report_index = os.path.abspath(os.path.join(".", "reports", "allure-reports", "index.html"))
            # 转为 file:// URL，Windows 需要使用正斜杠
            report_index_normalized = report_index.replace('\\', '/')
            report_url = f"file:///{report_index_normalized}"
            allure_report_util.send_test_result_to_wechat(
                report_title="BM接口自动化测试报告",
                passed_count=_TEST_STATS["passed"],
                failed_count=_TEST_STATS["failed"],
                error_count=_TEST_STATS["error"],
                duration=duration,
                report_url=report_url,
            )
        except Exception as e:
            auto_logger.error(f"推送企业微信异常: {e}")