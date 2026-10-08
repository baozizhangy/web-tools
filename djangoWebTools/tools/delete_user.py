# -*- coding: UTF-8 -*-

import hashlib
from config import db_conn
from utils.logger_util import web_logger


# 手机号加密
def md5_encrypt(text):
    md5 = hashlib.md5()
    md5.update(text.encode('utf-8'))
    return md5.hexdigest()


user_sql = [
    "delete FROM `cis`.`u_hub_user`  where user_no in ('{}')",
    "delete FROM `cis`.`c_cust`  where cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{}') )",
    "delete FROM `cis`.`u_user`  where user_no in ('{}')"
]

# 实名sql
ocr_sql = [
    "delete FROM `cis`.`u_idcard_ocr`  where user_no in ('{}')",
    "delete FROM `cis`.`u_idcard_ocr_his`  where user_no in ('{}')",
    "delete FROM `cis`.`u_face_detect`  where user_no in ('{}')",
    "delete FROM `cis`.`u_face_detect_his`  where user_no in ('{}')",
    "delete FROM `cis`.`u_cust_cert`  where user_no in ('{}')"
]

# 联系人
contact_sql = [
    "delete FROM `cis`.`c_contact`  where cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{}') )",
    "delete FROM `cis`.`c_contact_his`  where cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{}') )",
    "delete FROM `cis`.`u_hub_contact`  where user_no in ('{}')"
]
# 详细资料
detail_sql = [
    "delete FROM `cis`.`c_person_info`  where cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{}') )",
    "delete FROM `cis`.`u_hub_person_info`  where user_no in ('{}')",
    "delete FROM `cis`.`c_job_info`  where cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{}') )",
    "delete FROM `cis`.`c_job_info_his`  where cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{}') )",
    "delete FROM `cis`.`c_address`  where cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{}') )",
    "delete FROM `cis`.`u_hub_address`  where user_no in ('{}')",
    "delete FROM `cis`.`u_hub_job_info`  where user_no in ('{}')",
    "delete FROM `cis`.`c_address_his`  where cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{}') )"
]

# 删除借据信息
loan_sql = [
    "DELETE FROM `lcs`.`pilot_third_request` WHERE cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{}') )",
    "DELETE FROM hub.hub_channel_lending_record WHERE cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{"
    "}') )",
    "DELETE FROM `lps`.`i_iou` WHERE cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{}') )",
    "DELETE FROM `lps`.`i_iou_flow` WHERE cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{}') )",
    "DELETE FROM `lcs`.`pilot_loan` WHERE cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{}') )",
    "DELETE FROM `lcs`.`pilot_loan_his` WHERE cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{}') )",
    "DELETE FROM `lcs`.`pilot_plan` WHERE cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{}') )",
    "DELETE FROM `lcs`.`pilot_plan_his` WHERE cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{}') )",
    "DELETE FROM `lcs`.`pilot_privilege_order` WHERE cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{"
    "}') )",
    "DELETE FROM `lcs`.`pilot_privilege_plan` WHERE cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{"
    "}') )",
    "DELETE FROM `lcs`.`pilot_privilege_plan_his` WHERE cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ("
    "'{}') )",
    "DELETE FROM `lcs`.`pilot_putout_calc` WHERE cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{}') )",
    "DELETE FROM `lcs`.`pilot_putout_calc_detail` WHERE cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{}') )",
    "DELETE FROM `lcs`.`pilot_putout_calc_detail_his` WHERE cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{}') )",
    "DELETE FROM `lcs`.`pilot_putout_calc_his` WHERE cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{}') )",
    "DELETE FROM `lcs`.`pilot_repay_trial` WHERE cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{}') )",
    "DELETE FROM `lcs`.`pilot_repay_trial_his` WHERE cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{"
    "}') )",
    "DELETE FROM `lcs`.`pilot_tran_proc_db` WHERE cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{}') )",
    "DELETE FROM `lcs`.`pilot_tran_proc_rp` WHERE cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{}') )",
    "DELETE FROM hub.hub_tran_proc_db_summary  WHERE cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{}') )",
    "DELETE FROM hub.hub_tran_proc_rp WHERE cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{}') )",
    "DELETE FROM hub.hub_loan_summary WHERE cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{}') )"
]

# 删除绑卡信息
bind_sql = [
    "DELETE FROM `cis`.u_bankcard WHERE user_no in ('{}')",
    "DELETE FROM `cis`.u_bankcard_cert WHERE user_no in ('{}')",
    "DELETE FROM `cis`.u_fund_bankcard WHERE user_no in ('{}')",
    "DELETE FROM `cis`.u_fund_bind_card_req WHERE user_no in ('{}')",
    "DELETE FROM `cis`.u_fund_bind_relation WHERE user_no in ('{}')",
    "DELETE FROM cis.u_bank_card_ocr_his WHERE user_no in ('{}')"
]

# 删除权限信息
auth_sql = [
    "DELETE FROM `cis`.u_device WHERE user_no in ('{}')",
    "DELETE FROM `cis`.u_device_his WHERE user_no in ('{}')",
    "DELETE FROM `cis`.u_geo WHERE user_no in ('{}')",
    "DELETE FROM `cis`.u_geo_his WHERE user_no in ('{}')",
]

# 删除还款信息
repay_sql = [
    "DELETE FROM lcs.pilot_plan WHERE cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{}') )",
    "DELETE FROM lcs.pilot_plan_his WHERE cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{}') )",
    "DELETE FROM lcs.pilot_tran_proc_rp WHERE cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{}') )"
]

# 删除授信信息
credit_sql = [
    "DELETE FROM `lps`.ap_appl WHERE user_no in ('{}')",
    "DELETE FROM `lps`.ap_fund_appl WHERE user_no in ('{}')",
    "DELETE FROM `lps`.ap_fund_appl_log WHERE user_no in ('{}')",
    "DELETE FROM `lps`.ap_fund_appl_his WHERE user_no in ('{}')",
    "DELETE FROM lps.ap_fund_bind_skip WHERE user_no in ('{}')",
    "DELETE FROM `lps`.`wf_order` WHERE `creator` in ('{}')",
    "DELETE FROM `lps`.`wf_task_curr` WHERE `order_Id` IN (SELECT flow_no FROM `lps`.ap_appl WHERE user_no in ('{}'))",
    "DELETE FROM ams.ac_pilot_account WHERE cust_no in (SELECT cust_no FROM cis.u_user WHERE user_no in ('{}') )",
    "DELETE FROM lps.ap_fund_abandon WHERE user_no in ('{}')",
    "DELETE FROM hub.hub_channel_ap_apply_summary WHERE user_no in ('{}')",
    "DELETE FROM hub.hub_fund_ap_apply_summary WHERE user_no in ('{}')",
    "DELETE FROM hub.hub_push_task WHERE user_no in ('{}')",
    "DELETE FROM hub.hub_channel_request WHERE user_no in ('{}')",
    "DELETE FROM lps.ap_fund_distribution_record WHERE user_no in ('{}')",
    "DELETE FROM hub.hub_channel_appl_ctrl WHERE user_no in ('{}')",
    "DELETE FROM tds.flow_user_rule_exec WHERE user_no in ('{}')",
    "DELETE FROM hub.hub_account_summary WHERE user_no in ('{}')",
    "DELETE FROM `lcs`.`pilot_third_request` WHERE user_no in ('{}')",
    "DELETE FROM hub.hub_channel_lending_record WHERE user_no in ('{}')"
]

toast_list = []


class DeleteUser:

    def __init__(self, env, mobile):
        self.env = env
        self.mobile = mobile
        self.mobile_md5 = md5_encrypt(mobile)

    """
    第一步 根据手机号查询user_no
    第二步 根据user_no查询身份证密文
    第三步 根据身份证密文查询出所有的user_no列表
    """

    def get_user_no_list(self):
        user_list = []
        user_data = db_conn(self.env).get_all(
            f"SELECT * FROM cis.u_user WHERE cis.u_user.mobile_no_md5 = '{self.mobile_md5}'")
        if user_data:
            if user_data[0]['cust_no']:
                user_no = user_data[0]['user_no']
                cust_no = user_data[0]['cust_no']
                web_logger.info("要删除的user_no:{},cust_no:{}".format(user_no, cust_no))
                # 根据user_no查出加密的身份证号
                id_card = db_conn(self.env).get_all(
                    "SELECT JSON_EXTRACT(front_ocr_info , '$.idCard') as idcard FROM `cis`.`u_idcard_ocr` "
                    "WHERE user_no='{}' LIMIT 1".format(user_no))
                web_logger.info("根据user_no查出加密的身份证号:{}".format(id_card))
                if id_card:
                    id_card = id_card[0]['idcard']
                    web_logger.info("手机号对应的身份证密文：{}".format(id_card))
                    user_nos = db_conn(self.env).get_all(
                        "SELECT user_no FROM `cis`.`u_idcard_ocr` WHERE  JSON_EXTRACT(front_ocr_info , '$.idCard') in ({})".format(
                            id_card))
                    web_logger.info("根据身份证密文查出的user_nos：{}".format(user_nos))
                    if user_nos:
                        for user_no in user_nos:
                            user_list.append(user_no['user_no'])
                            web_logger.info('删除的元素不止一个，要删除的user_list:{}'.format(user_list))
                        return user_list
                    else:
                        user_list.append(user_no)
                        web_logger.info('删除的元素只有一个，要删除的user_list:{}'.format(user_list))
                        return user_list
                else:
                    user_list.append(user_no)
                    web_logger.info('要删除的user_list:{}'.format(user_list))
                    return user_list
            else:
                user_no = user_data[0]['user_no']
                web_logger.info("要删除的user_no:{}".format(user_no))
                user_list.append(user_no)
                web_logger.info('要删除的user_list:{}'.format(user_list))
                return user_list
        else:
            return None

    # 删除用户信息
    def del_user(self, user_no):
        for item in user_sql:
            for i in user_no:
                print(111, item, i)
                web_logger.info("删除用户信息：{}".format(item.format(i)))
                db_conn(self.env).exec_one(item.format(i))
        return toast_list.append("用户信息删除成功")

    # 删除实名信息
    def del_ocr(self, user_no):
        for item in ocr_sql:
            for i in user_no:
                web_logger.info("删除实名信息：{}".format(item.format(i)))
                db_conn(self.env).exec_one(item.format(i))
        return toast_list.append("实名删除成功")

    # 删除联系人信息
    def del_contact(self, user_no):
        for item in contact_sql:
            for i in user_no:
                web_logger.info("删除联系人信息：{}".format(item.format(i)))
                db_conn(self.env).exec_one(item.format(i))
        return toast_list.append("联系人删除成功")

    # 删除详细资料页信息
    def del_detail(self, user_no):
        for item in detail_sql:
            for i in user_no:
                web_logger.info("删除详细资料信息：{}".format(item.format(i)))
                db_conn(self.env).exec_one(item.format(i))
        return toast_list.append("详细资料删除成功")

    # 删除授信信息
    def del_credit(self, user_no):
        for item in credit_sql:
            for i in user_no:
                web_logger.info("删除授信信息：{}".format(item.format(i)))
                db_conn(self.env).exec_one(item.format(i))
        return toast_list.append("授权信息删除成功")

    # 删除借据信息
    def del_loan(self, user_no):
        for item in loan_sql:
            for i in user_no:
                web_logger.info("删除借据信息：{}".format(item.format(i)))
                db_conn(self.env).exec_one(item.format(i))
        return toast_list.append("借据删除成功")

    # 删除绑卡人信息
    def del_bind(self, user_no):
        for item in bind_sql:
            for i in user_no:
                web_logger.info("删除绑卡信息：{}".format(item.format(i)))
                db_conn(self.env).exec_one(item.format(i))
        return toast_list.append("借据删除成功")

    # 删除还款信息
    def del_repay(self, user_no):
        for item in repay_sql:
            for i in user_no:
                web_logger.info("删除绑卡信息：{}".format(item.format(i)))
                db_conn(self.env).exec_one(item.format(i))
        return toast_list.append("还款信息删除成功")

    # 删除权限人信息
    def del_auth(self, user_no):
        for item in auth_sql:
            for i in user_no:
                web_logger.info("删除权限人信息：{}".format(item.format(i)))
                db_conn(self.env).exec_one(item.format(i))
        return toast_list.append("权限信息删除成功")

    def node_del(self, node_items):
        """
        按节点删除：
            1、选择某个节点，输入手机号即可以删除所有信息
            2、不选择节点，删除全部信息
        """
        user_no = self.get_user_no_list()  # 获取要删除的用户ID
        if user_no:
            for item in node_items:
                if item != 'del_user':
                    web_logger.info("执行的方法：{}".format(item))
                    getattr(self, item)(user_no)
                    return "删除手机号：{},删除节点：{}".format(self.mobile, toast_list)
                else:
                    web_logger.info("删除用户是删除所有的节点数据，固所有节点都需要跑一遍删除")
                    node_items = ['del_auth', 'del_repay', 'del_bind', 'del_loan', 'del_credit'
                        , 'del_detail', 'del_contact', 'del_ocr', 'del_user']
                    for item in node_items:
                        web_logger.info("执行的方法：{}".format(item))
                        getattr(self, item)(user_no)
                    return "删除手机号：{},删除节点：{}".format(self.mobile, toast_list)

        else:
            return "手机号：{}未查询到用户ID，不可删除，请确认好再次删除".format(self.mobile)


if __name__ == '__main__':
    aa = DeleteUser('SIT', '13083666916')
    print(aa.del_credit(['UR0909779953531265024']))

