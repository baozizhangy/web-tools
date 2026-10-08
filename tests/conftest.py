import pytest,sys,allure,json

import shutil
from pathlib import Path


def pytest_configure(config):
    """测试开始前自动清理上次的 allure 原始结果，避免新旧数据混淆"""
    allure_dir = Path(__file__).parent / "reports" / "allure_results"
    if allure_dir.exists():
        shutil.rmtree(allure_dir)
    allure_dir.mkdir(parents=True, exist_ok=True)


# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from api.app.bm_api import BmApi
from utils.logger_util import web_logger
from utils.personal_util import get_person_name, get_id_no, get_mobile_no


@pytest.fixture(scope="session")
def env():
    """测试环境配置"""
    return 'BM_SIT'


@pytest.fixture(scope="session")
def channel():
    """渠道配置"""
    return 'lxj'


@pytest.fixture
def bm_api(env, channel):
    """BmApi实例 - 随机生成用户数据"""
    return BmApi(channel_id=channel, env=env)


@pytest.fixture
def test_user_data():
    """随机生成测试用户数据"""
    return {
        'mobile': get_mobile_no(),
        'name': get_person_name(),
        'id_card': get_id_no(),
        'term': 12,
        'amt': 3500
    }


@pytest.fixture
def api_with_user_data(env, channel, test_user_data):
    """带随机用户数据的BmApi实例"""
    return BmApi(
        channel_id=channel,
        mobile=test_user_data['mobile'],
        name=test_user_data['name'],
        id_card=test_user_data['id_card'],
        term=test_user_data['term'],
        amt=test_user_data['amt'],
        env=env
    )


def assert_response_success(response, expected_result=1):
    """
    验证API响应成功
    :param response: API响应数据
    :param expected_result: 期望的result值，默认为1
    """
    assert response is not None, "响应数据不能为空"
    assert isinstance(response, dict), "响应应该是字典类型"
    assert 'bizData' in response or 'data' in response, "响应缺少bizData或data字段"
    
    if 'bizData' in response:
        assert 'result' in response['bizData'], "bizData缺少result字段"
        assert response['bizData']['result'] == expected_result, \
            f"期望result={expected_result}，实际result={response['bizData']['result']}"


def assert_response_has_field(response, field_path):
    """
    验证响应包含指定字段
    :param response: API响应数据
    :param field_path: 字段路径，如 'bizData.fundCreditNo' 或 'data.user_no'
    """
    keys = field_path.split('.')
    current = response
    
    for key in keys:
        assert isinstance(current, dict), f"无法访问字段 {key}，当前值不是字典"
        assert key in current, f"响应缺少字段 {key}"
        current = current[key]
    
    assert current is not None, f"字段 {field_path} 的值为空"
    return current


@pytest.fixture(autouse=True)
def log_test_info(request):
    """自动记录测试信息"""
    web_logger.info(f"\n{'='*60}")
    web_logger.info(f"开始执行测试: {request.node.name}")
    web_logger.info(f"{'='*60}")
    
    # 添加Allure报告信息
    allure.dynamic.title(request.node.name)
    allure.dynamic.description(f"测试方法: {request.node.name}")
    
    yield
    
    web_logger.info(f"完成测试: {request.node.name}")
    web_logger.info(f"{'='*60}\n")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Allure报告钩子
    """
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call":
        if rep.failed:
            allure.attach(
                str(rep.longrepr),
                name="失败信息",
                attachment_type=allure.attachment_type.TEXT
            )
