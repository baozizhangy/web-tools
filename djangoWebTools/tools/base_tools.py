#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from config import db_conn
from utils.cryption_util import md5_encrypt


# 字符串转md5值


# 根据手机号查询user_no
def select_user_no_by_mobile(env, mobile):
    sql = 'SELECT user_no FROM cis.u_user WHERE mobile_no_md5 = "{}" LIMIT 1'.format(md5_encrypt(mobile))
    get_user_res = db_conn(env).select_one(sql)
    return get_user_res
