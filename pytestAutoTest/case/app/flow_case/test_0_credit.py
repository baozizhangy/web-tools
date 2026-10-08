# #!/usr/bin/env python
# # -*- coding: UTF-8 -*-
# import allure
#
# from api.app.credit_api import Credit
# from utils.logger_util import auto_logger
#
#
# # from pytestAutoTest.business.account import send_code_success, get_code_success, login_success
# # from utils.personal_util import get_mobile_no
#
#
# @allure.epic("APP模式")
# @allure.feature("APP流程模块")
# @allure.story("授信提交成功场景")
# class TestCredit:
#     @allure.title("九步流程提交正确，授信提交成功")
#     @allure.description("该用例是针对整个授信流程的测试")
#     def test_credit_success(self, get_logged_user, create_credit_flow, flow_ocr_commit):
#         try:
#             with allure.step("1.获取已登录用户"):
#                 logged_user = get_logged_user
#                 assert logged_user.mobile, "用户登录失败"
#                 auto_logger.info(f"授信流程获取已登录用户成功，手机号为:{logged_user.mobile}")
#
#             with allure.step("2.APP创建授信流程，进入身份证识别节点"):
#                 # logged_user.credit = Credit(logged_user.api_root_url, logged_user.session, channel_id="LXJ_APP", product_code="PILOT_APP")
#                 # create_flow_res = logged_user.credit.flow_entry_click().json()
#                 user, create_flow_res = create_credit_flow
#                 assert create_flow_res.get("data").get("nextNode") == "pilotIdentity", "未进入身份证识别节点"
#                 auto_logger.info(f"APP创建授信流程成功，nextNode为:{create_flow_res.get('data').get('nextNode')}")
#
#             with allure.step("3.APP提交OCR"):
#                 ocr_res = flow_ocr_commit
#                 print(f"ocr_res:{ocr_res}")
#                 ...
#             with allure.step("4.APP提交人脸"):
#                 ...
#             with allure.step("5.APP提交联系人"):
#                 ...
#             with allure.step("6.APP提交详细资料"):
#                 ...
#             with allure.step("7.APP选择进件机构"):
#                 ...
#             with allure.step("8.APP进行前置绑卡"):
#                 ...
#             with allure.step("9.APP同意机构协议"):
#                 ...
#             with allure.step("10.APP授信提交"):
#                 ...
#         except Exception as e:
#             allure.attach(body=str(e), title="异常详情", attachment_type=allure.attachment_type.TEXT)
#
#
# @allure.step("用例前置处理")
# @allure.description("在用例执行前，进行业务系统配置、mock配置")
# def setup():
#     ...
#
#
# @allure.step("用例后置处理")
# @allure.description("用例执行后，进行业务系统数据还原、按需还原mock配置")
# def teardown():
#     ...
