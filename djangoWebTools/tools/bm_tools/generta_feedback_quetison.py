# -*- coding: utf-8 -*-
# @Time    : 2023/6/29 15:34
# @Author  : zhangzhengchuan
import time
from faker import Faker

# from api.app.credit_api import Credit
# from api.app.help_center import HelpCenter
# from api.app.user_api import UserApi
# from config import help_submit_api,db_conn
from config import  db_conn
from utils.cryption_util import md5_encrypt
from utils.jwt_util import validate_token
from utils.logger_util import web_logger
from utils.nacos_util import Nacos
from utils.personal_util import get_mobile_no,get_random_question_type,get_fund_product_type


# def login_user(env):
#     number = get_mobile_no()  # 获取手机号码
#     # user = UserApi(env=env,mobile=number,app='LXJ_APP')  # 初始化UserApi
#     send_code_res = user.send_code(number)  # 发送验证码
#     get_code_res = user.get_code(number)  # 获取验证码响应
#     code = get_code_res.json().get('data').get('code')  # 提取验证码
#     login_code_res = user.login_code(user.mobile,code)  # 登录验证码
#     api_root_path = user.api_root_url  # 获取API根路径
#     # refresh_res = user.credit.home_info().json()
#     # web_logger.info(f"----2,{user.credit.home_info().header.get('ctoken')}")
#     session = user.session
#     return session,api_root_path,number  # 返回会话、API路径和手机号码

#
# def generate_feedback_questions(env,num_users,num_questions_per_user,questiontype,productname):
#     fake = Faker(["en_US","zh_CN"])  # 初始化Faker以生成假数据
#     number_list = []
#
#     for _ in range(num_users):
#         login_user_info_session,api_root_path,number = login_user(env)  # 调用登录函数
#         number_md5 = md5_encrypt(number)  # 对号码进行MD5加密
#         number_user_no_sql = f"SELECT user_no FROM cis.u_user WHERE cis.u_user.mobile_no_md5 = '{number_md5}'"  # SQL查询
#         user_no = db_conn(env).get_all(number_user_no_sql)[0].get('user_no')  # 从数据库获取用户编号
#
#         help_submit = HelpCenter(api_root_path,login_user_info_session,user_no=user_no)  # 初始化HelpCenter
#
#         for _ in range(num_questions_per_user):
#             content = fake.paragraph(nb_sentences=5)  # 生成假内容
#             imageurl = ['string']  # 假图像URL用stringd代替
#             question_type = questiontype if questiontype is not None else get_random_question_type()  # 获取问题类型
#             product_name = productname if productname is not None else get_fund_product_type(env.lower())  # 获取产品名称
#             help_center_question_submit_res = help_submit.help_center_question_submit(  # 提交问题
#                 content=content,
#                 questiontype=question_type,
#                 productname=product_name,
#                 imageurl=imageurl
#             )
#             if help_center_question_submit_res.status_code == 200:
#                 # 添加到号码列表
#                 number_list.append((number,user_no,content))
#             web_logger.info(help_center_question_submit_res)
#             web_logger.info(f"Successfully submitted question for user {number}: {help_center_question_submit_res}")
#             web_logger.info(f"help_center_question_submit_res:{help_center_question_submit_res}")
#             time.sleep(5)  # 等待5秒，防止频繁提交
#
#     web_logger.info(number_list)  # 记录提交情况
#     return number_list # 返回号码列表
def get_fund_question_types(env):
    try:
        config_data = Nacos(env.lower()).get_css_config()
        print(config_data)
        fund_type_list = [{"value":value} for value in config_data]
        # 获取配置
        return {"code": 0, "data": fund_type_list}
    except Exception as e:
        # 记录错误并返回相应的错误信息
        web_logger.error(f"Failed to get fund question types: {str(e)}")
        return {"code": 1, "error": "获取配置失败"}


if __name__ == '__main__':
    # aa = generate_feedback_questions(env="SIT",num_users=2, num_questions_per_user=2,questiontype=None,productname=None)
    # print(aa)
    pass
    # bb =get_fund_question_types("sit")
    # print(bb)
    # cc = login_user("SIT")
    # print(cc)

