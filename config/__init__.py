#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os

import yaml

from utils.file_util import read_file
from utils.ftp_util import FTPClient
from utils.logger_util import web_logger
from utils.mysql_util import MySQL
from utils.nacos_util import Nacos
from utils.redis_db import RedisDB

# 从系统环境变量获取该测试运行环境配置， 键名为：TEST_ENV
RUN_ENV = os.environ.get('TEST_ENV')
nacos_conn = Nacos(RUN_ENV)
print(f"运行环境 RUN_ENV::{RUN_ENV}")
run_client = nacos_conn.client(RUN_ENV.lower())
nacos_config = yaml.safe_load(run_client.get_config(group='auto-test', data_id='application.properties'))
# 自动化用例执行环境
case_env = "SIT"

# nacos中获取mysql配置
# sit_mysql_conf = nacos_config.get("MYSQL").get("SIT")
dev_mysql_conf = nacos_config.get("MYSQL").get("DEV")
bm_sit_mysql_conf = nacos_config.get("MYSQL").get("BM_SIT")
# hw_mysql_conf = nacos_config.get("MYSQL").get("HW")
bm_sit_redis_conf = nacos_config.get("REDIS").get("BM_SIT")
dev_redis_conf = nacos_config.get("REDIS").get("DEV")

# nacos中的urls常量
urls = nacos_config.get("URLS")
xxl_login = nacos_config.get("XXL").get('LOGIN')
xxl_trigger = nacos_config.get("XXL").get('TRIGGER')
easy_mock = nacos_config.get("EASY")
h5_get_url = nacos_config.get("H5API")
base_url = nacos_config.get("BASE_API")
# dev域名或路径
dev_urls = urls.get("DEV")
dev_login_xxl = xxl_login.get("DEV_URL")
dev_trigger_xxl = xxl_trigger.get("DEV_URL")
dev_h5_get_url = h5_get_url.get("DEV_URL")
dev_get_url = base_url.get("DEV_URL")
# BM_sit域名或路径
bm_urls = urls.get("BM_SIT")
bm_sit_login_xxl = xxl_login.get("BM_SIT_URL")
bm_sit_trigger_xxl = xxl_trigger.get("BM_SIT_URL")
bm_sit_h5_get_url = h5_get_url.get("BM_SIT_URL")
sit_get_url = base_url.get("BM_SIT_URL")

# widek地址
widek_config = nacos_config.get("WIDEK_URL_MAP")
dev_widek_url = widek_config.get("DEV")
bm_sit_widek_url = widek_config.get("BM_SIT")
web_logger.info(f"widek配置 DEV:{dev_widek_url}, BM_SIT:{bm_sit_widek_url}")

local_nacos_client = nacos_conn.client("local")
sit_nacos_client = nacos_conn.client("bm-sit")
dev_nacos_client = nacos_conn.client("bm-dev")


# 公共服务域名


def get_nacos_client(env):
    if env == "SIT":
        return sit_nacos_client
    if env == "DEV":
        return dev_nacos_client


def get_urls(env):
    if env == "DEV":
        return dev_urls
    # if env == "SIT":
    #     return sit_urls
    # if env == "HW":
    #     return hws_urls
    if env == "BM_SIT":
        return bm_urls


def get_xxl_login_urls(env):
    if env == "DEV":
        return dev_login_xxl
    if env == "BM_SIT":
        return bm_sit_login_xxl


def get_xxl_trigger_urls(env):
    if env == "DEV":
        return dev_trigger_xxl
    if env == "BM_SIT":
        return bm_sit_trigger_xxl


def easy_login_url():
    return easy_mock.get('LOGIN')


def easy_update_url():
    return easy_mock.get('UPDATE')


def h5_get_env_url(env):
    if env == "DEV":
        return dev_h5_get_url
    if env == "BM_SIT":
        return bm_sit_h5_get_url


def api_get_url(env):
    if env == "DEV":
        return dev_get_url
    if env == "BM_SIT":
        return sit_get_url


# sit连接池，默认为连接到lps数据库，执行其他数据库SQL时需指定库名
# sit_conn = MySQL(
#     sit_mysql_conf.get("HOST"), sit_mysql_conf.get("PORT"),
#     sit_mysql_conf.get("USER"), sit_mysql_conf.get("PASSWORD"))
# dev连接池，默认为连接到lps数据库，执行其他数据库SQL时需指定库名
dev_conn = MySQL(
    dev_mysql_conf.get("HOST"), dev_mysql_conf.get("PORT"),
    dev_mysql_conf.get("USER"), dev_mysql_conf.get("PASSWORD"))
# bm_sit连接池，默认为连接到lps数据库，执行其他数据库SQL时需指定库名
bm_sit_conn = MySQL(
    bm_sit_mysql_conf.get("HOST"), bm_sit_mysql_conf.get("PORT"),
    bm_sit_mysql_conf.get("USER"), bm_sit_mysql_conf.get("PASSWORD"))


# dev连接池，默认为连接到lps数据库，执行其他数据库SQL时需指定库名
# hw_conn = MySQL(
#     hw_mysql_conf.get("HOST"), hw_mysql_conf.get("PORT"),
#     hw_mysql_conf.get("USER"), hw_mysql_conf.get("PASSWORD"))

#
# widek = nacos_config.get("WIDEK")
# widek_token = widek.get("TOKEN")
# widek_host = widek.get("HOST")
# widek_port = widek.get("PORT")
#
# web_logger.info(f"从系统环境变量中获取到host：{widek_host}")
#
# web_logger.info(f"从系统环境变量中获取到port：{widek_port}")

def get_widek_url(env):
    if env == "DEV":
        return dev_widek_url
    if env == "BM_SIT":
        return bm_sit_widek_url
    raise ValueError(f"不支持的 widek 环境: {env}")
# SFTP 连接访问配置
# FTP = nacos_config.get("FTP")
# # print(f"FTP:{type(FTP), FTP}")
# xr_sftp_client = FTPClient(FTP.get("host"), FTP.get("port"), FTP.get("username"), FTP.get("password"))
# xr_sftp_client.connect()


# redis 连接访问配置


def redis_db_conn(env, db=0):
    web_logger.info(f"本次请求的环境: {env}")
    if env == "DEV":
        redis_conf = dev_redis_conf
    elif env == "BM_SIT":
        redis_conf = bm_sit_redis_conf
    else:
        raise ValueError(f"不支持的 redis 环境: {env}")

    return RedisDB(
        redis_conf.get("host"),
        redis_conf.get("port"),
        redis_conf.get("password"),
        db=db
    )


bm_sit_redis_db = redis_db_conn("BM_SIT")



def db_conn(env):
    # if env == "SIT":
    #     # print(f"env::{env}, sit_conn::{sit_conn.__dict__}")
    #     return sit_conn
    if env == "DEV":
        return dev_conn
    if env == "BM_SIT":
        return bm_sit_conn
    # if env == "HW":
    #     return hw_conn
    # else:
    #     return sit_conn


# 接口配置
# 获取当前文件的绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 获取clg_api_config.yaml文件中的配置，配置为APP流程的接口信息
clg_api_conf_data = read_file(f"{BASE_DIR}/clg_api_config.yaml")
# # 授信接口配置
credit_api = clg_api_conf_data.get("credit")
# # print(f"api_conf_data::{api_conf_data}")
# # 绑卡接口配置
# bind_api = clg_api_conf_data.get("bind")
# # 帮助中心接口配置
# help_submit_api = clg_api_conf_data.get("help")
# 助贷订单接口配置
loan_api = clg_api_conf_data.get("bm_api")

if __name__ == '__main__':
    # aa = help_submit_api['helpsubmit']
    # print(aa)
    # print(loan_api['check_user'])
    # print(get_urls('DEV')['FUND_LOAN'])
    # print(get_xxl_trigger_urls('BM_SIT'))
    # print(easy_login_url())
    res = bm_sit_redis_db.delete_by_pattern("lcs*")
    print(res)
    # print(bm_sit_redis_conf)

