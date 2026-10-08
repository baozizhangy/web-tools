# #!/usr/bin/env python
# # -*- coding: UTF-8 -*-
# import time
# import hashlib
# # from api.app.bind_api import Bind
# # from api.app.credit_api import Credit
# # from api.app.user_api import UserApi
# from config import db_conn, get_nacos_client
# from pytestAutoTest.data.temp_info import  generate_contact_info, generate_profile_info, insert_face
# from utils.jwt_util import validate_token
# from utils.logger_util import web_logger
# from utils.nacos_util import
# from utils.personal_util import get_mobile_no, get_id_no, get_person_name
# # from config import db_conn, get_nacos_client, redis_conn
# # from pytestAutoTest.data.temp_info import generate_ocr_info, generate_contact_info, generate_profile_info, insert_face
# # from utils.nacos_util import update_tds_config
#
# node_list = {
#     "user_logged": {
#         "node_name": "用户登录成功，未实名"
#     },
#     "auth": {
#         "node_name": "用户实名成功，进入联系人节点"
#     },
#     "contact": {
#         "node_name": "联系人完成，进入详细资料节点"
#     },
#     "profile": {
#         "node_name": "详细资料完成，进入机构选择页"
#     },
#     "credit_commit": {
#         "node_name": "授信提交成功"
#     },
#     "loan_commit": {
#         "node_name": "借款提交成功"
#     },
# }
#
#
# def md5_encrypt(text):
#     md5 = hashlib.md5()
#     md5.update(text.encode('utf-8'))
#     return md5.hexdigest()
#
#
# def create_user_two(env, channel=None, product_code=None, assign_node=None,
#                     mobile_no=None, id_no=None, name=None,fund_code=None):
#     """
#     登录、授信分发、借款流程
#     """
#     create_user_res = {"node_list": [], "exception": []}
#
#     print(f"input_info:{env},{mobile_no}, {id_no}, {name}")
#     web_logger.info(f"====登录用户:{env},{mobile_no}, {id_no}, {name},{channel}====")
#     if not mobile_no:
#         mobile_no = get_mobile_no()
#     user = UserApi(env, mobile_no)
#     create_user_res["APP_H5链接"] = user.home_page_url
#     print(f"user手机号码：{mobile_no}")
#     create_user_res["mobile"] = mobile_no
#     # 发送验证码
#     send_code_res = user.send_code(user.mobile).json()
#
#     if send_code_res.get("status") != 1:
#         create_user_res["node_list"].append(f"发送登录验证码失败，返回：{send_code_res}")
#         web_logger.info(f"====发送验证码失败:{send_code_res}====")
#         return create_user_res
#
#     web_logger.info(f"====发送验证码成功:{send_code_res}====")
#     # 获取验证码
#     get_code_res = user.get_code(user.mobile)
#     if get_code_res.status_code != 200:
#         create_user_res["node_list"].append(f"获取登录验证码调用失败::{get_code_res}")
#         return create_user_res
#
#     get_code_res = get_code_res.json()
#     if get_code_res.get("code") != 0:
#         create_user_res["node_list"].append("获取验证码失败")
#         web_logger.info(f"====获取验证码失败:{get_code_res}====")
#         return create_user_res
#
#     code = get_code_res.get("data").get("code")
#     # 登录
#     logged_user_res = user.login_code(user.mobile, code)
#     print(f"登录返回:{logged_user_res}")
#
#     if not logged_user_res.json().get("phone_number"):
#         create_user_res["node_list"].append("登录失败")
#         web_logger.info(f"====登录失败:{logged_user_res}====")
#         return create_user_res
#     web_logger.info(f"===={mobile_no}登录成功====")
#
#
#     # 用户登录成功
#     user_no = validate_token(logged_user_res.headers.get('C-Token')).get('data').get('user_no')
#     device_no = validate_token(logged_user_res.headers.get('C-Token')).get('data').get('duid')
#
#     # 更新tds配置
#     if fund_code:
#         update_tds_user_config = update_tds_config(get_nacos_client(env), user_no=user_no,fund_code=fund_code)
#
#         print(f"update_tds_user_config::{update_tds_user_config}")
#
#     if user_no is not None:
#         user.user_no = user_no
#         create_user_res["user_no"] = user_no
#
#         # 获取C-Token
#         create_user_res["C-Token"] = logged_user_res.headers.get('C-Token')
#         web_logger.info("获取的token：{}".format(create_user_res["C-Token"]))
#
#     redis_conn.set(f"web_tools:ctoken:{env}:{mobile_no}:", create_user_res["C-Token"])
#     create_user_res["node_list"].append("用户登录成功")
#
#     if device_no is not None:
#         create_user_res["device_no"] = device_no
#         collect_device_res = user.collect_device(device_no=device_no)
#         print(f"collect_device_res::{collect_device_res.json()}")
#         if collect_device_res.status_code != 200:
#             create_user_res["node_list"].append("上传设备信息失败")
#         create_user_res["node_list"].append("上传设备信息成功")
#
#         collect_contacts_res = user.collect_contacts()
#         print(f"collect_contacts_res::{collect_contacts_res.json()}")
#         if collect_contacts_res.status_code != 200:
#             create_user_res["node_list"].append("上传联系人信息失败")
#         create_user_res["node_list"].append("上传联系人信息成功")
#
#
#
#     # 创建授信流程
#     user.credit = Credit(
#         user.api_root_url, user.session,
#         channel_id=channel, product_code=product_code)
#
#     # 刷新首页
#     refresh_res = user.credit.home_info().json()
#     if refresh_res.get("code") != "0":
#         create_user_res["node_list"].append("刷新首页失败")
#         web_logger.info(f"====刷新首页失败:{refresh_res}====")
#         return create_user_res
#     create_user_res["node_list"].append("刷新首页成功")
#
#     if assign_node == "user_logged":
#         return create_user_res
#
#     create_flow_res = user.credit.flow_entry_click2().json()
#     print(f"创建用户结果:{create_flow_res}")
#
#     if create_flow_res.get("data", {}).get("nextNode") != "pilotIdentityV2":
#         create_user_res["node_list"].append("授信创建流程失败，非pilotIdentityV2节点")
#         web_logger.info(f"====授信创建流程失败:{create_flow_res}====")
#         return create_user_res
#
#     flow_data = create_flow_res.get("data", {})
#     web_logger.info("授信返回信息：{}".format(flow_data))
#     if flow_data is not None:
#         user.credit.flow_no = flow_data.get("flowNo")
#         create_user_res["flow_no"] = flow_data.get("flowNo")
#         user.credit.sub_flow_no = create_flow_res.get("data").get("subFlowNo")
#         create_user_res["sub_flow_no"] = flow_data.get("subFlowNo")
#         web_logger.info("授信流水：{}".format(user.credit.sub_flow_no))
#         web_logger.info("授信流水1：{}".format(create_user_res["sub_flow_no"]))
#
#     # 上传身份证
#
#     if id_no is None or len(id_no) < 18:
#         id_no = get_id_no()
#     if name is None or len(name) < 2:
#         name = get_person_name()
#     print(f"上传身份证：{id_no}, {name}")
#     wz_front_data = generate_ocr_info(ocr_mode=0, id_no=id_no, name=name, flow_no=user.credit.flow_no)
#     ocr_front_res = user.credit.ocr_wz_ocr(wz_front_data).json()
#     web_logger.info(f"====身份证正面识别结果上传===={ocr_front_res}")
#     wz_back_data = generate_ocr_info(ocr_mode=1, flow_no=user.credit.flow_no)
#     ocr_back_res = user.credit.ocr_wz_ocr(wz_back_data).json()
#     web_logger.info(f"====身份证反面识别结果上传===={ocr_back_res}")
#     if ocr_front_res.get("code") != "0" or ocr_back_res.get("code") != "0":
#         create_user_res["node_list"].append("身份证上传失败")
#         return create_user_res
#     create_user_res["node_list"].append("身份证上传成功")
#
#     # 身份证节点提交
#     web_logger.info(r"====身份证正反面上传成功====进行节点提交")
#     ocr_save_data = {"name": ocr_front_res.get("data").get("name"),
#                      "idNo": ocr_front_res.get("data").get("idCardNo"), }
#     ocr_save_res = user.credit.ocr_save(ocr_save_data).json()
#     web_logger.info(f"====ocr节点保存结果===={ocr_save_res}")
#     if ocr_save_res.get("code") != "0":
#         create_user_res["node_list"].append("身份证节点保存失败")
#         return create_user_res
#     create_user_res["node_list"].append("身份证节点保存成功")
#     web_logger.info(f"====身份证节点保存成功====")
#
#     # ocr流程节点提交
#     next_node_res = user.credit.ocr_flow_ok2(sub_flow_no=user.credit.sub_flow_no).json()
#     print(f"===身份证流程节点返回===={next_node_res}")
#     if next_node_res.get("code") != "0":
#         create_user_res["node_list"].append("身份证节点提交失败")
#         return create_user_res
#     create_user_res["node_list"].append("身份证节点提交成功")
#     create_user_res["用户姓名"] = name
#     create_user_res["用户身份证"] = id_no
#     if assign_node == "identity":
#         return create_user_res
#
#     # 节点检查
#     web_logger.info(f"====身份证流程节点返回===={next_node_res}")
#     next_node = next_node_res.get("data", {}).get("nextNode")
#     if next_node != "pilotFaceV2":
#         create_user_res["node_list"].append("进入人脸识别节点失败，非pilotFace节点")
#         web_logger.info(f"====进入人脸识别节点失败:{create_flow_res}====")
#         return create_user_res
#
#     # 向cis::u_face_detect、u_face_detect_his表插入人脸数据
#     face_submit_res = insert_face(db_conn(env=env), user_no=user_no, channel_id=channel)
#
#     web_logger.info(f"====insert_face::face_submit_res::{face_submit_res}")
#     if face_submit_res.get("code") != "0":
#         create_user_res["node_list"].append("人脸数据插入cis.u_face_detect失败")
#         return create_user_res
#
#     create_user_res["node_list"].append("人脸数据插入cis.u_face_detect成功")
#
#     next_node_res = user.credit.face_flow_ok2(sub_flow_no=user.credit.sub_flow_no).json()
#     web_logger.info("返回：{}".format(next_node_res))
#     if next_node_res.get("code") != "0":
#         create_user_res["node_list"].append("人脸流程节点提交失败")
#         return create_user_res
#     create_user_res["node_list"].append("人脸流程节点提交成功")
#     print(f"===人脸流程节点返回===={next_node_res}")
#
#     # 节点检查
#     next_node = next_node_res.get("data", {}).get("nextNode")
#     if next_node != "pilotContactV2":
#         create_user_res["node_list"].append("进入联系人节点失败，非pilotContact节点")
#         web_logger.info(f"====进入联系人节点失败:{next_node_res}====")
#         return create_user_res
#     create_user_res["node_list"].append("进入联系人节点成功")
#
#     if assign_node == "face":
#         return create_user_res
#
#     next_node_res = user.credit.face_flow_ok2(sub_flow_no=user.credit.sub_flow_no).json()
#     next_node = next_node_res.get("data", {}).get("nextNode")
#     if next_node != "pilotContactV2":
#         create_user_res["node_list"].append("进入联系人节点失败，非pilotContactV2节点")
#         web_logger.info(f"====进入人脸识别节点失败:{next_node_res}====")
#         return create_user_res
#     create_user_res["node_list"].append("进入联系人节点成功")
#
#     # 生成联系人信息并保存
#     contact_info = generate_contact_info()
#     contact_res = user.credit.contact_operate(contact_info).json()
#     if contact_res.get("code") != "0":
#         create_user_res["node_list"].append("联系人信息保存失败")
#         web_logger.info(f"====联系人信息保存失败:{contact_res}====")
#         return create_user_res
#     create_user_res["node_list"].append("联系人信息保存成功")
#
#     if assign_node == "contact":
#         return create_user_res
#
#     # 联系人节点提交
#     next_node_res = user.credit.contact_flow_ok2(sub_flow_no=user.credit.sub_flow_no).json()
#     next_node = next_node_res.get("data", {}).get("nextNode")
#     print(f"===联系人流程节点返回===={next_node_res}")
#     if next_node != "pilotDetailsV2":
#         create_user_res["node_list"].append("联系人节点提交失败")
#         web_logger.info(f"====联系人节点提交失败:{next_node_res}====")
#         return create_user_res
#     web_logger.info(f"===联系人流程节点返回===={next_node_res}")
#     create_user_res["node_list"].append("联系人节点提交成功")
#
#     # 详细资料节点提交
#     profile_info = generate_profile_info()
#     print(f"generate_profile_info======={profile_info}")
#     profile_res = user.credit.profile_operate(profile_info).json()
#     print(f"profile_res======={profile_res}")
#     if profile_res.get("code") != "0":
#         create_user_res["node_list"].append("详细资料保存失败")
#         web_logger.info(f"====详细资料保存失败:{profile_res}====")
#         return create_user_res
#     create_user_res["node_list"].append("详细资料保存成功")
#
#     if assign_node == "profile":
#         return create_user_res
#
#     # 详细资料节点提交
#     next_node_res = user.credit.profile_flow_ok2(sub_flow_no=user.credit.sub_flow_no).json()
#     print(f"===详细资料流程节点返回===={next_node_res}")
#     if next_node_res.get("flag") != "S":
#         create_user_res["node_list"].append(f"详细资料页节点提交失败，msg:{next_node_res.get('msg')}")
#         return create_user_res
#
#     next_node = next_node_res.get("data", {}).get("nextNode")
#     if next_node == "pilotMandatoryProtocolsV2":
#         create_user_res["node_list"].append("进入强弹协议页")
#         # 协议查询
#         agreement_res = user.credit.agreement_query(flow_no=user.credit.flow_no).json()
#         web_logger.info(f"====协议查询结果为：{agreement_res}====")
#         if agreement_res.get("code") != "0":
#             create_user_res["node_list"].append("协议查询失败")
#             web_logger.info(f"====协议查询失败:{agreement_res}====")
#             return create_user_res
#
#         # 保存协议
#         org_list = [org_info['orgCode'] for org_info in agreement_res.get('data', {}).get('orgInfoList', []) if
#                     'orgCode' in org_info]
#         agreement_save_res = user.credit.agreement_save(user.credit.flow_no, org_list).json()
#         if agreement_save_res.get("code") != "0":
#             create_user_res["node_list"].append("保存协议失败")
#             web_logger.info(f"====保存协议失败:{agreement_save_res}====")
#             return create_user_res
#         create_user_res["node_list"].append("保存协议成功")
#         web_logger.info(f"====保存协议成功:{agreement_save_res}====")
#
#         if assign_node == "agreement":
#             return create_user_res
#         # 协议节点后检查
#         next_node_res = user.credit.agreement_flow_ok2(sub_flow_no=user.credit.sub_flow_no).json()
#         if next_node_res.get("code") != "0":
#             create_user_res["node_list"].append("协议节点提交失败")
#             web_logger.info(f"====协议节点提交失败:{next_node_res}====")
#             return create_user_res
#         web_logger.info(f"====协议节点提交成功:{next_node_res}====")
#         create_user_res["node_list"].append("协议节点提交成功")
#
#     elif next_node != "pilotLoadingV2" and next_node != "pilotMandatoryProtocolsV2":
#         create_user_res["node_list"].append("进入pilotLoadingV2页失败，非pilotLoadingV2节点")
#         web_logger.info(f"====进入pilotLoadingV2页失败:{next_node_res}====")
#         return create_user_res
#     create_user_res["node_list"].append("进入pilotLoadingV2节点成功")
#
#     # 进件前检查
#     check_times = 0  # 检查次数
#     max_times = 8  # 最高检查次数
#     wait_time = 3
#     while check_times < max_times:
#         next_node_res = user.credit.flow_submit_check2(sub_flow_no=user.credit.sub_flow_no).json()
#         web_logger.info(
#             f"====第{check_times}次查询submit_check结果为：{next_node_res}====")
#         # 节点为非pilotLoading，结束循环
#         if next_node_res.get("data").get("nextNode") != "pilotLoadingV2":
#             break
#
#         time.sleep(wait_time)
#         check_times += 1
#
#     next_node = next_node_res.get("data", {}).get("nextNode")
#     print(f"===提交检查结果为：{next_node}====")
#     # user.credit.flow_submit_check2(sub_flow_no=user.credit.sub_flow_no).json()
#     # 绑卡节点处理
#     if next_node == "pilotBindCardV2":
#         create_user_res["node_list"].append("进入绑定银行节点")
#         user.bind = Bind(user.api_root_url, user.credit.meta, user.session)
#         # 获取可用银行卡
#         usable_list = user.bind.get_usable_card2(node_type="apply", flow_no=user.credit.flow_no).json()
#         web_logger.info(f"====获取可用银行卡信息结果====\n{usable_list}")
#
#         next_node_res = user.credit.bind_ok2(user.credit.sub_flow_no).json()
#         if next_node_res.get("code") != "0":
#             create_user_res["node_list"].append("绑定银行卡失败")
#             web_logger.info(f"====绑定银行卡失败:{next_node_res}====")
#             return create_user_res
#         next_node = next_node_res.get("data", {}).get("nextNode")
#
#     if assign_node == "bind":
#         return create_user_res
#     if next_node == "creditResult":
#         create_user_res["node_list"].append("进入审批结果页")
#         next_node_res = user.credit.result_query(user.credit.flow_no).json()
#         web_logger.info("审批结果页返回响应：{}".format(next_node_res))
#         if next_node_res.get("code") != "0":
#             create_user_res["node_list"].append("获取审批结果失败")
#             web_logger.info(f"====获取审批结果失败:{next_node_res}====")
#             return create_user_res
#         create_user_res["node_list"].append("获取审批结果成功")
#         create_user_res["审批结果"] = next_node_res
#         fundList = next_node_res['data']['fundList']
#         web_logger.info("可申请的机构：{}".format(fundList))
#         if fundList is not None:
#             fund_status = {item['fundCode']: item['appStatus'] for item in fundList}
#             web_logger.info("申请机构的状态：".format(fund_status))
#             create_user_res["node_list"].append(fund_status)
#             return create_user_res
#         else:
#             create_user_res["node_list"].append("没有可申请机构")
#             return create_user_res
#
#     if assign_node == "submitted":
#         return create_user_res
#
#
# def call_create_user_multiple_times(num_times,**kwargs):
#     results = []
#     num_times = int(num_times)
#
#     web_logger.info(f"call_create_user_multiple_times::kwargs::{kwargs}")
#     for _ in range(num_times):
#         get_res = create_user_two(**kwargs)
#         results.append(get_res)
#     phones = [item['mobile'] for item in results]
#     results_res = {'phones': phones, 'results': results}
#     return results_res
#
#
# def get_fund_code_list(env):
#     try:
#         # 查询数据库以获取数据
#         fund_code_list_sql = "SELECT id, fund_code, product_name FROM lcs.fund_product"
#         fund_code_list_res = db_conn(env).get_all(fund_code_list_sql)
#
#         # 记录获取的数据
#         web_logger.info(f"Fetched fund code list: {fund_code_list_res}")
#
#         # 格式化数据
#         formatted_data = [
#             {
#                 "id": item['id'],
#                 "name": item['product_name'],
#                 "fund_code": item['fund_code'],
#                 "fund_name_code": item['product_name'] + item['fund_code']
#             }
#             for item in fund_code_list_res
#         ]
#
#         return {
#             "code": 0,
#             "data": formatted_data,
#             "msg": "Successfully retrieved fund code list"
#         }
#
#     except Exception as e:
#         # 记录错误信息并返回错误响应
#         error_message = f"An error occurred while getting fund code list: {e}"
#         web_logger.error(error_message)
#         return {
#             "code": 1,
#             "data": [],
#             "msg": error_message
#         }
#
#
#
#
# if __name__ == '__main__':
#     # res = create_user_two(env="SIT", assign_node="identity", mobile_no=get_mobile_no())
#     res = create_user_two(env="DEV", channel="LXJ_APP", product_code='PILOT_APP', assign_node="credit",
#                           mobile_no='13112342226', id_no=None, name=None,fund_code="fundloan")
#     print(f"complete_flow::{res}")
