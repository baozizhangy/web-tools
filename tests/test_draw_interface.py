"""
借款相关接口测试
- agreement_list() - 查询协议列表
- draw_trial() - 借款试算
- draw_submit() - 借款提交
- send_sms_code() - 发送验证码
- send_sms() - 校验验证码
- draw_step_query() - 查询借款步骤
- draw_result_query() - 查询借款结果
- loan_play_query() - 查询借据和还款计划
"""
import pytest
from conftest import assert_response_success, assert_response_has_field
from utils.logger_util import web_logger
from api.app.bm_api import BmApi


class TestDrawInterface:
    """借款相关接口测试"""

    def test_agreement_list_success(self, api_with_user_data):
        """
        测试查询协议列表接口 - 成功场景
        前置条件：
        1. 已发起授信
        
        验证：
        1. 响应不为空
        2. 返回result=1（成功）
        3. 返回agreementList字段
        """
        web_logger.info(f"查询协议列表: {api_with_user_data.mobile}")
        
        # 前置：发起授信
        api_with_user_data.check_user()
        api_with_user_data.risk_white_user()
        credit_res = api_with_user_data.credit_apply()
        
        assert credit_res['bizData']['result'] == 1, "发起授信失败"
        credit_req_no = credit_res['bizData']['creditReqNo']
        
        # 使用示例user_no
        user_no = "UR98532790162168433TEST"
        
        # 查询协议列表
        response = api_with_user_data.agreement_list(user_no, credit_req_no, scene='DRAW')
        
        # 验证响应
        assert response is not None, "查询协议列表响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"
        
        web_logger.info(f"查询协议列表成功")

    def test_agreement_list_response_structure(self, api_with_user_data):
        """
        测试查询协议列表接口 - 响应结构验证
        """
        user_no = "UR98532790162168433TEST"
        credit_req_no = "CT285508642807TEST"
        
        response = api_with_user_data.agreement_list(user_no, credit_req_no)
        
        # 验证响应结构
        assert 'code' in response or 'bizData' in response, "响应缺少code或bizData字段"
        
        web_logger.info(f"查询协议列表响应结构验证通过")

    @pytest.mark.parametrize("scene", ['REGISTER', 'CREDIT', 'DRAW', 'BIND', 'LOAN', 'REPAY', 'PRIVILEGE'])
    def test_agreement_list_different_scenes(self, api_with_user_data, scene):
        """
        测试查询协议列表接口 - 不同场景
        验证不同协议场景的查询
        """
        web_logger.info(f"查询协议列表场景: {scene}")
        
        user_no = "UR98532790162168433TEST"
        credit_req_no = "CT285508642807TEST"
        
        response = api_with_user_data.agreement_list(user_no, credit_req_no, scene=scene)
        
        assert response is not None, f"场景{scene}的协议查询失败"
        web_logger.info(f"场景{scene}的协议查询成功")

    def test_draw_trial_success(self, api_with_user_data):
        """
        测试借款试算接口 - 成功场景
        前置条件：
        1. 已发起授信
        
        验证：
        1. 响应不为空
        2. 返回result=1（成功）
        3. 返回试算结果信息
        """
        web_logger.info(f"借款试算: {api_with_user_data.mobile}")
        
        # 前置：发起授信
        api_with_user_data.check_user()
        api_with_user_data.risk_white_user()
        credit_res = api_with_user_data.credit_apply()
        
        assert credit_res['bizData']['result'] == 1, "发起授信失败"
        credit_req_no = credit_res['bizData']['creditReqNo']
        fund_credit_no = credit_res['bizData']['fundCreditNo']
        
        # 借款试算
        response = api_with_user_data.draw_trial(credit_req_no, fund_credit_no, profit='N')
        
        # 验证响应
        assert response is not None, "借款试算响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"
        
        web_logger.info(f"借款试算成功")

    def test_draw_trial_response_structure(self, api_with_user_data):
        """
        测试借款试算接口 - 响应结构验证
        """
        credit_req_no = "CT314997747149TEST"
        fund_credit_no = "BM957945124799660032"
        
        response = api_with_user_data.draw_trial(credit_req_no, fund_credit_no)
        
        # 验证响应结构
        assert 'bizData' in response, "响应缺少bizData字段"
        
        web_logger.info(f"借款试算响应结构验证通过")

    def test_draw_trial_with_privilege(self, api_with_user_data):
        """
        测试借款试算接口 - 带权益试算
        验证是否获取权益信息
        """
        credit_req_no = "CT314997747149TEST"
        fund_credit_no = "BM957945124799660032"
        
        # 不获取权益
        response_no_privilege = api_with_user_data.draw_trial(credit_req_no, fund_credit_no, profit='N')
        assert response_no_privilege is not None, "不获取权益的试算失败"
        
        # 获取权益
        response_with_privilege = api_with_user_data.draw_trial(credit_req_no, fund_credit_no, profit='Y')
        assert response_with_privilege is not None, "获取权益的试算失败"
        
        web_logger.info(f"借款试算(权益)成功")

    def test_draw_submit_success(self, api_with_user_data):
        """
        测试借款提交接口 - 成功场景
        前置条件：
        1. 已发起授信
        2. 已获取绑卡信息
        
        验证：
        1. 响应不为空
        2. 返回result=1或3（成功或需要二次验证）
        """
        web_logger.info(f"借款提交: {api_with_user_data.mobile}")
        
        # 前置：发起授信
        api_with_user_data.check_user()
        api_with_user_data.risk_white_user()
        credit_res = api_with_user_data.credit_apply()
        
        assert credit_res['bizData']['result'] == 1, "发起授信失败"
        
        # 使用示例数据
        user_no = "UR98532272416657945TEST"
        credit_req_no = "CT314997747149TEST"
        card_no = "620200179858713386"
        
        # 借款提交
        response = api_with_user_data.draw_submit(user_no, credit_req_no, card_no, profit='N')
        
        # 验证响应
        assert response is not None, "借款提交响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"
        
        web_logger.info(f"借款提交成功")

    def test_draw_submit_response_structure(self, api_with_user_data):
        """
        测试借款提交接口 - 响应结构验证
        """
        user_no = "UR98532272416657945TEST"
        credit_req_no = "CT314997747149TEST"
        card_no = "620200179858713386"
        
        response = api_with_user_data.draw_submit(user_no, credit_req_no, card_no)
        
        # 验证响应结构
        assert 'bizData' in response, "响应缺少bizData字段"
        
        web_logger.info(f"借款提交响应结构验证通过")

    def test_send_sms_code_success(self, api_with_user_data):
        """
        测试发送验证码接口 - 成功场景
        验证：
        1. 响应不为空
        2. 返回result=1（成功）
        """
        web_logger.info(f"发送验证码: {api_with_user_data.mobile}")
        
        user_no = "UR98532272416657945TEST"
        biz_no = "CR07165952462147917"
        scene = "01"  # 01 - 借款提交验证短信；02 - 还款提交验证短信
        
        response = api_with_user_data.send_sms_code(user_no, biz_no, scene)
        
        # 验证响应
        assert response is not None, "发送验证码响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"
        
        web_logger.info(f"发送验证码成功")

    def test_send_sms_success(self, api_with_user_data):
        """
        测试校验验证码接口 - 成功场景
        验证：
        1. 响应不为空
        2. 返回result=1（成功）
        """
        web_logger.info(f"校验验证码: {api_with_user_data.mobile}")
        
        user_no = "UR98532272416657945TEST"
        scene = "01"
        sms_code = "8991"
        biz_no = "CR07165952462147917"
        
        response = api_with_user_data.send_sms(user_no, scene, sms_code, biz_no)
        
        # 验证响应
        assert response is not None, "校验验证码响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"
        
        web_logger.info(f"校验验证码成功")

    def test_draw_step_query_success(self, api_with_user_data):
        """
        测试查询借款步骤接口 - 成功场景
        验证：
        1. 响应不为空
        2. 返回result=1（成功）
        """
        web_logger.info(f"查询借款步骤: {api_with_user_data.mobile}")
        
        biz_no = "CR07165952462147917"
        credit_req_no = "CT314997747149TEST"
        
        response = api_with_user_data.draw_step_query(biz_no, credit_req_no)
        
        # 验证响应
        assert response is not None, "查询借款步骤响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"
        
        web_logger.info(f"查询借款步骤成功")

    def test_draw_result_query_success(self, api_with_user_data):
        """
        测试查询借款结果接口 - 成功场景
        验证：
        1. 响应不为空
        2. 返回drawResultList字段
        """
        web_logger.info(f"查询借款结果: {api_with_user_data.mobile}")
        
        biz_no = "CR07165952462147917"
        credit_req_no = "CT314997747149TEST"
        
        response = api_with_user_data.draw_result_query(biz_no, credit_req_no)
        
        # 验证响应
        assert response is not None, "查询借款结果响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"
        
        web_logger.info(f"查询借款结果成功")

    def test_loan_play_query_success(self, api_with_user_data):
        """
        测试查询借据和还款计划接口 - 成功场景
        验证：
        1. 响应不为空
        2. 返回result=1（成功）
        3. 返回借据和还款计划信息
        """
        web_logger.info(f"查询借据和还款计划: {api_with_user_data.mobile}")
        
        biz_no = "CR07165952462147917"
        fund_draw_no = "CT314997747149TEST"
        
        response = api_with_user_data.loan_play_query(biz_no, fund_draw_no)
        
        # 验证响应
        assert response is not None, "查询借据和还款计划响应为空"
        assert isinstance(response, dict), "响应应该是字典类型"
        
        web_logger.info(f"查询借据和还款计划成功")
