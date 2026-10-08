#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import functools

from api.channel.feichangzhun import FeiChangZhun
from api.channel.fuyuanhui import FuYuanHui
from api.channel.guomei import GuoMei
from api.channel.haofenqi import HaoFenQi
from api.channel.haofenqi_s1 import HaoFenQiS1
from api.channel.haojie58 import HaoJie58
from api.channel.huolala import HuoLaLa
from api.channel.jiufu_v2 import JiuFuV2
from api.channel.juzi import JuZi
from api.channel.minsheng import MinSheng
from api.channel.niwodai import NiWoDai
from api.channel.niwodai_s1 import NiWoDaiS1
from api.channel.niwodai_s2 import NiWoDaiS2
from api.channel.shengbei import Shengbei
from api.channel.shiguangfenqi import ShiGuangFenQi
from api.channel.tianmian import TianMian
from api.channel.tianmian_v2 import TianMianV2
from api.channel.tongcheng import TongCheng
from api.channel.weixin import WeiXin
from api.channel.xiaohua import XiaoHua
from api.channel.xiaoxiang_v2 import XiaoXiangV2
from api.channel.xiaoying import XiaoYing
from api.channel.xiecheng_v2 import XieChengV2
from api.channel.xiecheng_v3 import XieChengV3
from api.channel.xinyongfei import XinYongFei
from api.channel.yijiesudai_v2 import YiJieSuDaiV2
from api.channel.yixianghua import YiXiangHua
from api.channel.yunbaobao import YunBaoBao
from api.channel.zhongmi import ZhongMi
from utils.logger_util import web_logger

# 渠道名称与类名的映射表
channel_mapping = {
    "HUB_HUOLALA": HuoLaLa,
    "HUB_ZHONGMI": ZhongMi,
    "HUB_XIAOHUA": XiaoHua,
    "HUB_YIJIESUDAI_V2": YiJieSuDaiV2,
    "HUB_JUZI": JuZi,
    "HUB_MINSHENG": MinSheng,
    "HUB_YIXIANGHUA": YiXiangHua,
    "HUB_TIANMIAN": TianMian,
    "HUB_TIANMIAN_V2": TianMianV2,
    "HUB_SHIGUANGFENQI": ShiGuangFenQi,
    "HUB_HAOFENQI": HaoFenQi,
    "HUB_HAOFENQI_S1": HaoFenQiS1,
    "HUB_58HAOJIE": HaoJie58,
    "HUB_FUYUANHUI": FuYuanHui,
    "HUB_XIAOYING": XiaoYing,
    "HUB_FEICHANGZHUN": FeiChangZhun,
    "HUB_XIAOXIANG_V2": XiaoXiangV2,
    "HUB_XINYONGFEI": XinYongFei,
    "HUB_YUNBAOBAO": YunBaoBao,
    "HUB_JIUFU_V2": JiuFuV2,
    "HUB_NIWODAI": NiWoDai,
    "HUB_NIWODAI_S1": NiWoDaiS1,
    "HUB_NIWODAI_S2": NiWoDaiS2,
    "HUB_SHENGBEI": Shengbei,
    "HUB_TONGCHENG": TongCheng,
    "HUB_GUOMEI": GuoMei,
    "HUB_XIECHENG_V2": XieChengV2,
    "HUB_XIECHENG_V3": XieChengV3,
    "HUB_WEIXIN": WeiXin,
}


def submit_channel_request(channel, method, data):
    # 提交渠道请求
    web_logger.info(f"submit_channel_request::method::{method},\ndata::{data}")
    if channel in channel_mapping:
        channel_class = channel_mapping[channel]
        print(f"submit_channel_request::channel_class::{channel_class.__name__}")
        # 实例化渠道类
        channel_instance = channel_class()
        # 检查渠道类是否具有指定方法
        if hasattr(channel_class, method):
            # 调用渠道方法
            channel_method = getattr(channel_instance, method)
            # 使用functools.partial为方法预先设置参数
            partial_method = functools.partial(channel_method, data)
            res = partial_method()
            web_logger.info(f"提交渠道请求返回::{res}")
            return res
        else:
            web_logger.info(f"渠道类{channel_class.__name__}不包含方法{method}")
            return f"渠道类{channel_class.__name__}不包含方法{method}，暂未实现或异常"
    else:
        web_logger.info("submit_channel_request异常")
        return "未知渠道"


# def get_channel_check_data(channel, mobile, input_id_no, user_name):
#     check_init_param = {
#         "mobile": mobile,
#         "input_id_no": input_id_no,
#         "user_name": user_name
#     }
#     # 按渠道获取准入信息
#     if channel in channel_mapping:
#         channel_class = channel_mapping[channel]
#         res = channel_class().get_check_data(check_init_param)
#         web_logger.info(f"获取准入结果返回::{res}")
#         return res
#     else:
#         web_logger.info("无效的渠道")
#         return None


# def submit_check(env, channel, check_data):
#     # 提交渠道准入申请
#     print(f"submit_check::data::{check_data}")
#
#     if channel in channel_mapping:
#         channel_class = channel_mapping[channel]
#         res = channel_class(env).check(check_data)
#         web_logger.info(f"提交渠道准入申请返回::{res}")
#         return res
#     else:
#         web_logger.info("无效的渠道")
#         return None


# def get_channel_credit_data(channel, mobile, input_id_no, user_name):
#     # 按渠道获取授信信息
#     if channel in channel_mapping:
#         channel_class = channel_mapping[channel]
#         res = channel_class().get_credit_data(mobile, input_id_no, user_name)
#         web_logger.info(f"获取准入结果返回::{res}")
#         return res
#     else:
#         web_logger.info("无效的渠道")
#         return None


# def submit_credit(env, channel, check_data):
#     # 提交渠道准入申请
#     print(f"submit_check::data::{check_data}")
#
#     if channel in channel_mapping:
#         channel_class = channel_mapping[channel]
#         res = channel_class(env).credit(check_data)
#         web_logger.info(f"提交渠道授信申请返回::{res}")
#         return res
#     else:
#         web_logger.info("无效的渠道")
#         return None


# def query_credit(env, channel, data):
#     # 查询渠道授信结果
#     print(f"query_credit::data::{data.get('creditNo'), data.get('openId'), data.get('mobile')}")
#
#     if channel in channel_mapping:
#         channel_class = channel_mapping[channel]
#         res = channel_class(env).credit_result_by_credit_data(data)
#         web_logger.info(f"提交渠道准入申请返回::{res}")
#         return res
#     else:
#         web_logger.info("无效的渠道")
#         return None


# def get_channel_h5_url(env, channel, data):
#     # 查询渠道H5url
#     print(f"query_credit::data::{data}")
#
#     if channel in channel_mapping:
#         channel_class = channel_mapping[channel]
#         res = channel_class(env).get_h5_by_credit_data(data)
#         web_logger.info(f"提交渠道准入申请返回::{res}")
#         return res
#     else:
#         web_logger.info("无效的渠道")
#         return None
