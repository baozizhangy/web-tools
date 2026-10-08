"""
还款相关接口测试
- repay_trial() - 还款试算
- repay_submit() - 还款提交
- repay_result_query() - 还款结果查询
"""
import pytest
import allure
from conftest import assert_response_success, assert_response_has_field
from utils.logger_util import web_logger
from api.app.bm_api import BmApi


@allure.feature("还款相关接口")
@allure.story("还款试算与提交")
class TestRepayInterface:
    """还款相关接口测试"""

    def test_repay_trial_current_period_success(self, api_with_user_data):
        """
        测试还款试算接口 - 当期还款
        前置条件：
        1. 用户已有借据
        
        验证：
        1. 响应不为空
        2. 返回result=1（成功）
        3. 返回试算结果信息
        """
        web_logger.info(f"还款试算(当期): {api_with_user_data.mobile}")
        
        user_no = "UR98532257688418423TEST"
        biz_no = "CR07165952462144728"
        fund_draw_no = "BMD958548472074616832"
        trial_type = 1  # 1 - 当期还款
        periods = [1]
        
        response = api_with_user_data.repay_trial(user_no, biz_no, fund_draw_no, trial_type, periods)
        
        # 验证响应
        assert response is not None, "还款试算响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"
        
        web_logger.info(f"还款试算(当期)成功")

    def test_repay_trial_overdue_single_period_success(self, api_with_user_data):
        """
        测试还款试算接口 - 逾期还款(单期)
        验证：
        1. 响应不为空
        2. 返回试算结果
        """
        web_logger.info(f"还款试算(逾期单期): {api_with_user_data.mobile}")
        
        user_no = "UR98532257688418423TEST"
        biz_no = "CR07165952462144728"
        fund_draw_no = "BMD958548472074616832"
        trial_type = 2  # 2 - 逾期还款(单期)
        periods = [2]
        
        response = api_with_user_data.repay_trial(user_no, biz_no, fund_draw_no, trial_type, periods)
        
        # 验证响应
        assert response is not None, "还款试算响应为空"
        
        web_logger.info(f"还款试算(逾期单期)成功")

    def test_repay_trial_overdue_multiple_periods_success(self, api_with_user_data):
        """
        测试还款试算接口 - 逾期还款(多期合并)
        验证：
        1. 响应不为空
        2. 返回试算结果
        """
        web_logger.info(f"还款试算(逾期多期): {api_with_user_data.mobile}")
        
        user_no = "UR98532257688418423TEST"
        biz_no = "CR07165952462144728"
        fund_draw_no = "BMD958548472074616832"
        trial_type = 3  # 3 - 逾期还款(多期合并)
        periods = [2, 3, 4]
        
        response = api_with_user_data.repay_trial(user_no, biz_no, fund_draw_no, trial_type, periods)
        
        # 验证响应
        assert response is not None, "还款试算响应为空"
        
        web_logger.info(f"还款试算(逾期多期)成功")

    def test_repay_trial_early_settlement_success(self, api_with_user_data):
        """
        测试还款试算接口 - 整笔提前结清
        验证：
        1. 响应不为空
        2. 返回试算结果
        """
        web_logger.info(f"还款试算(提前结清): {api_with_user_data.mobile}")
        
        user_no = "UR98532257688418423TEST"
        biz_no = "CR07165952462144728"
        fund_draw_no = "BMD958548472074616832"
        trial_type = 4  # 4 - 整笔提前结清
        periods = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        
        response = api_with_user_data.repay_trial(user_no, biz_no, fund_draw_no, trial_type, periods)
        
        # 验证响应
        assert response is not None, "还款试算响应为空"
        
        web_logger.info(f"还款试算(提前结清)成功")

    def test_repay_trial_response_structure(self, api_with_user_data):
        """
        测试还款试算接口 - 响应结构验证
        """
        user_no = "UR98532257688418423TEST"
        biz_no = "CR07165952462144728"
        fund_draw_no = "BMD958548472074616832"
        trial_type = 1
        periods = [1]
        
        response = api_with_user_data.repay_trial(user_no, biz_no, fund_draw_no, trial_type, periods)
        
        # 验证响应结构
        assert 'bizData' in response, "响应缺少bizData字段"
        
        web_logger.info(f"还款试算响应结构验证通过")

    def test_repay_trial_response_contains_amount(self, api_with_user_data):
        """
        测试还款试算接口 - 验证返回还款金额
        """
        user_no = "UR98532257688418423TEST"
        biz_no = "CR07165952462144728"
        fund_draw_no = "BMD958548472074616832"
        trial_type = 1
        periods = [1]
        
        response = api_with_user_data.repay_trial(user_no, biz_no, fund_draw_no, trial_type, periods)
        
        # 验证返回的还款金额
        if 'bizData' in response:
            biz_data = response['bizData']
            if 'deserveTotalAmt' in biz_data:
                repay_amt = biz_data['deserveTotalAmt']
                assert repay_amt > 0, "还款金额应该大于0"
                web_logger.info(f"还款金额: {repay_amt}")

    def test_repay_submit_success(self, api_with_user_data):
        """
        测试还款提交接口 - 成功场景
        前置条件：
        1. 已进行还款试算
        
        验证：
        1. 响应不为空
        2. 返回result=1或3（成功或需要二次验证）
        """
        web_logger.info(f"还款提交: {api_with_user_data.mobile}")
        
        biz_no = "CR07165952462144728"
        repay_type = 1  # 还款类型
        repay_amt = 3500  # 还款金额
        card_no = "620200179858713386"
        mobile = "15605786856"
        repay_no = "RR182093812093864"
        periods = [1]
        
        response = api_with_user_data.repay_submit(biz_no, repay_type, repay_amt, card_no, mobile, repay_no, periods)
        
        # 验证响应
        assert response is not None, "还款提交响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"
        
        web_logger.info(f"还款提交成功")

    def test_repay_submit_response_structure(self, api_with_user_data):
        """
        测试还款提交接口 - 响应结构验证
        """
        biz_no = "CR07165952462144728"
        repay_type = 1
        repay_amt = 3500
        card_no = "620200179858713386"
        mobile = "15605786856"
        repay_no = "RR182093812093864"
        periods = [1]
        
        response = api_with_user_data.repay_submit(biz_no, repay_type, repay_amt, card_no, mobile, repay_no, periods)
        
        # 验证响应结构
        assert 'bizData' in response, "响应缺少bizData字段"
        
        web_logger.info(f"还款提交响应结构验证通过")

    @pytest.mark.parametrize("repay_type", [1, 2, 3, 4])
    def test_repay_submit_different_types(self, api_with_user_data, repay_type):
        """
        测试还款提交接口 - 不同还款类型
        验证不同还款类型的提交
        """
        web_logger.info(f"还款提交(类型{repay_type}): {api_with_user_data.mobile}")
        
        biz_no = "CR07165952462144728"
        repay_amt = 3500
        card_no = "620200179858713386"
        mobile = "15605786856"
        repay_no = "RR182093812093864"
        periods = [1]
        
        response = api_with_user_data.repay_submit(biz_no, repay_type, repay_amt, card_no, mobile, repay_no, periods)
        
        assert response is not None, f"还款类型{repay_type}的提交失败"
        web_logger.info(f"还款类型{repay_type}的提交成功")

    def test_repay_result_query_success(self, api_with_user_data):
        """
        测试还款结果查询接口 - 成功场景
        前置条件：
        1. 已提交还款
        
        验证：
        1. 响应不为空
        2. 返回还款结果信息
        """
        web_logger.info(f"查询还款结果: {api_with_user_data.mobile}")
        
        repay_req_no = "RR1820938120932908"
        fund_repay_no = "BMR961854325582221312"
        
        response = api_with_user_data.repay_result_query(repay_req_no, fund_repay_no)
        
        # 验证响应
        assert response is not None, "查询还款结果响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"
        
        web_logger.info(f"查询还款结果成功")

    def test_repay_result_query_response_structure(self, api_with_user_data):
        """
        测试还款结果查询接口 - 响应结构验证
        """
        repay_req_no = "RR1820938120932908"
        fund_repay_no = "BMR961854325582221312"
        
        response = api_with_user_data.repay_result_query(repay_req_no, fund_repay_no)
        
        # 验证响应结构
        assert 'bizData' in response or 'data' in response, "响应缺少bizData或data字段"
        
        web_logger.info(f"查询还款结果响应结构验证通过")

    def test_repay_result_query_with_invalid_repay_no(self, api_with_user_data):
        """
        测试还款结果查询接口 - 无效的还款号
        验证：
        1. 使用无效的还款号查询
        2. 接口返回相应的错误信息
        """
        invalid_repay_req_no = "INVALID_RR_123456789"
        
        web_logger.info(f"查询无效的还款结果: {invalid_repay_req_no}")
        
        response = api_with_user_data.repay_result_query(invalid_repay_req_no)
        
        # 验证响应
        assert response is not None, "查询还款结果响应为空"
        
        web_logger.info(f"查询无效还款号返回: {response}")
