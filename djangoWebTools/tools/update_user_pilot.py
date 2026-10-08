# -*- coding: utf-8 -*-
# @Time    : 2023/6/29 15:34
# @Author  : zhangzhengchuan
from config import db_conn
from utils.cryption_util import md5_encrypt
from utils.logger_util import web_logger


def update_user_pilots(env, phone_number, pilot_code):
    md5_number = md5_encrypt(phone_number)
    web_logger.info(md5_number)

    update_pilot_sql = f"""
        UPDATE lps.wf_task_curr 
        SET lps.`wf_task_curr`.task_Name = '{pilot_code}' 
        WHERE lps.`wf_task_curr`.order_id = (
            SELECT flow_no 
            FROM lps.ap_appl 
            WHERE user_no = (
                SELECT cis.u_user.user_no 
                FROM cis.u_user 
                WHERE cis.u_user.mobile_no_md5 = '{md5_number}'
            ) 
            ORDER BY id DESC 
            LIMIT 1
        )
    """
    pilot_code_to_scene = {
        'pilotIdentityV2':'身份证页',
        'pilotFaceV2':'活体页',
        'pilotContactV2':'联系人页',
        'pilotDetailsV2':'详细资料页'
    }
    # if pilot_code in pilot_code_to_scene:
    #     pilot_scene = pilot_code_to_scene[pilot_code]
    # else:
    #     pilot_scene = None
    pilot_scene = pilot_code_to_scene.get(pilot_code,'未知页面')
    web_logger.info(f"update_pilot_sql 更新节点sql: {update_pilot_sql}")

    try:
        update_pilot_sql_res = db_conn(env).exec_one(update_pilot_sql)
        web_logger.info(f"update_pilot_sql_res 执行结果: {update_pilot_sql_res}")

        if update_pilot_sql_res['code'] == '0':
            return {'code': 0, 'message': f'{pilot_scene}节点更新成功'}
        else:
            return {'code': 1, 'message': f'{pilot_scene}节点更新失败'}
    except Exception as e:
        error_message = f"数据库查询错误: {str(e)}"
        web_logger.error(error_message)
        return {"code":1,"message":error_message}
if __name__ == '__main__':
    resource = update_user_pilots("sit","19601255855","pilotContactV2")









