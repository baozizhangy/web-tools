#!/usr/bin/env python
# -*- coding: UTF-8 -*-


"""
java服务端方法枚举值
public enum MethodEnum {
    CHECK("check", "准入"),
    REGISTER("register", "注册"),
    BANK_LIST("bank_list", "支持的银行卡列表"),
    BANK_INFO("bank_info", "查询用户已绑卡信息"),
    BIND_LIST("bind_list", "查询绑卡列表"),
    NEED_BIND("need_bind", "用户绑卡查询接口"),
    NEED_BIND_CARD("need_bind_card", "获取用户准入后流程参数"),
    BIND_URL("bind_url", "获取前置绑卡URL"),
    BIND_QUERY("bind_query", "签约绑卡查询"),
    BIND_CARD("bind_card", "绑卡"),
    BIND_VERIFY("bind_verify", "绑卡验证"),
    GET_PROFILE("get_profile", "信息采集"),
    //yixianghua
    PROFILES("profiles", "信息补充"),
    SEND_DATA("send_data", "渠道推送进件数据"),
    EXTRA_SEND_DATA("extra_send_data", "补充数据"),
    //全民
    PUSH_PHASE_ONE("push_phase_one", "推送阶段一"),
    //全民
    PUSH_PHASE_TWO("push_phase_two", "推送阶段二"),
    SUBMIT("submit", "进件"),
    STATUS("status", "订单状态查询"),
    SUBMIT_CHECK("submit_check", "进件资格检查"),
    SUBMIT_RESULT("submit_result", "进件结果"),
    CONCLUSION("conclusion", "授信结果查询"),
    CONCLUSION_DETAIL("conclusion_detail", "授信额度查询"),
    CONTRACT("contract", "授信协议查询"),
    ORDER_CONTRACT("order_contract", "获取借款协议"),
    SCENE_URL("scene_url", "获取下载链接"),
    //yixianghua 还款地址查询scene_url_repay
    FIND_REPAY_URL("find_repay_url", "还款地址查询"),
    //yixianghua
    IS_NEED_ADD_VERIFY("is_need_add_verify", "是否需要增验"),
    LOGIN_URL("login_url", ""),
    H5_WITHDRAW_URL("h5_withdraw_url", "获取h5借款url"),
    LOAN_INFO("loan_info", "贷款信息查询"),
    ORDER_STATUS("order_status", "订单状态"),
    LOAN_RECORD("loan_record", "查询借据列表"),
    CONFIRM_URL("confirm_url", "下单"),
    CONFIRM_ORDER("confirm_order", "下单"),
    CONFIRM_SIGN("confirm_sign", "签约"),
    CONFIRM_CODE("confirm_code", "借款确认"),
    CONFIRM_VCODE("confirm_vcode", "借款确认"),
    FUNDED_RESULT("repayment-result", "放款结果查询"),
    TRIAL("trial", "试算"),
    REPAY("repay", "还款"),
    REPAY_INFO("repay_info", "还款计划查询"),
    REPAY_RESULT("repay_result", "还款结果查询"),
    REPAY_VCODE("repay_vcode", "还款确认"),
    // ---推送接口
    ORDER_STATUS_PUSH("order_status", "订单状态推送"),
    CONCLUSION_PUSH("conclusion", "授信推送"),
    REPAY_INFO_PUSH("repay_info", "还款计划推送"),

"""
import time
import requests
from config import get_urls
from utils.logger_util import web_logger


def channel_handle_request(env, data, ):
    # hub统一调用接口 env=SIT/DEV
    print(f"channel_handle_request::data::{env, get_urls(env), data}")
    url = get_urls(env).get("HUB_PATH")
    responds = requests.post(url, json=data)
    web_logger.info(f"hub_request::request::{data},\nresponds::{responds.json()}")
    return responds.json()


class BaseRequest:
    """
    渠道通用请求
    接口：check,credit,credit_result
    """

    def __init__(self, channel_id=None, channel_name=None, channel_method_enum=None,
                 channel_uid=None, py_code=None):
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.channel_method_enum = channel_method_enum
        self.channel_uid = channel_uid
        self.py_code = py_code

    @classmethod
    def non_empty(cls, required_fields):
        # 验证必填字段

        def decorator(func):

            def wrapper(self, data):
                errors = {}
                for field in required_fields:
                    field_value = data.get(field)
                    if not field_value:
                        errors[field] = f"获取该接口参数时{field}不能为空"
                if errors:
                    return {"success": False, "errors": errors}
                return func(self, data)

            return wrapper

        return decorator

    def data_model(self, method, data):
        """
        封装请求数据通用格式
        :param method:
        :param data:
        :return:
        """
        return {
            "timestamp": int(time.time()*1000),
            "channelId": self.channel_id,
            "method":    method,
            "bizData":   data
        }

    def get_channel_methods(self, data):
        # 从枚举类中获取渠道方法
        method_list = [
            {"inner_method": member.value[0], "method_name": member.value[1], "method": member.value[2]}
            for member in self.channel_method_enum
        ]
        return method_list
        # return BaseRequest.get_channel_method(self.channel_method_enum)

    # @staticmethod
    # def get_channel_method(channel_methods_enum):
    #     method_list = [
    #         {"inner_method": member.value[0], "method_name": member.value[1], "method": member.value[2]}
    #         for member in channel_methods_enum
    #     ]
    #     return method_list

    # @staticmethod
    # def get_channel_method(method_list):
    #     # 获取渠道方法
    #     return [{"method": method.method, "method_name": method.method_name, "method_type": method.method_type}
    #             for method in method_list]

    # def _request(self, method, biz_data):
    #     # 通用请求方法
    #     res = hub_request(
    #         self.env, channel_id=self.channel_id, method=method, biz_data=biz_data)
    #     web_logger.info(f"BaseRequest:check res:{res}")
    #     return res

    # @staticmethod
    # def general_send(env, json_data):
    #     # 渠道通用请求接口调用
    #     # 用于统一提交
    #     url = get_urls(env).get("HUB_PATH")
    #     print(f"general_send::url::{url},data::{json_data}")
    #     responds = requests.post(url, json=json_data)
    #     return responds

    # def check(self, data):
    #     web_logger.info(f"BaseRequest:check data:{data}")
    #     # 调用准入
    #     return self._request(method="check", biz_data=data).json()
    #
    # def register(self, data):
    #     # 调用注册
    #     return self._request(method="register", biz_data=data).json()
    #
    # def bank_list(self, data):
    #     # 支持的银行卡列表
    #     return self._request(method="bank_list", biz_data=data).json()
    #
    # def bank_info(self, data):
    #     # 查询用户已绑卡信息
    #     return self._request(method="bank_info", biz_data=data).json()
    #
    # def bind_list(self, data):
    #     # 查询绑卡列表
    #     return self._request(method="bind_list", biz_data=data).json()
    #
    # def need_bind(self, data):
    #     # 用户绑卡查询接口
    #     return self._request(method="need_bind", biz_data=data).json()
    #
    # def need_bind_card(self, data):
    #     # 获取用户准入后流程参数
    #     return self._request(method="need_bind_card", biz_data=data).json()
    #
    # def bind_url(self, data):
    #     # 获取前置绑卡URL
    #     return self._request(method="bind_url", biz_data=data).json()
    #
    # def bind_query(self, data):
    #     # 签约绑卡查询
    #     return self._request(method="bind_query", biz_data=data).json()
    #
    # def bind_card(self, data):
    #     # 绑卡
    #     return self._request(method="bind_card", biz_data=data).json()
    #
    # def bind_verify(self, data):
    #     # 绑卡验证
    #     return self._request(method="bind_list", biz_data=data).json()
    #
    # def get_profile(self, data):
    #     # 信息采集
    #     return self._request(method="bind_list", biz_data=data).json()
    #
    # def profiles(self, data):
    #     # 信息补充
    #     return self._request(method="profiles", biz_data=data).json()
    #
    # def send_data(self, data):
    #     # 渠道推送进件数据
    #     return self._request(method="send_data", biz_data=data).json()
    #
    # def extra_send_data(self, data):
    #     # 补充数据
    #     return self._request(method="extra_send_data", biz_data=data).json()
    #
    # def push_phase_one(self, data):
    #     # 推送阶段一
    #     return self._request(method="push_phase_one", biz_data=data).json()
    #
    # def push_phase_two(self, data):
    #     # 推送阶段二
    #     return self._request(method="push_phase_two", biz_data=data).json()
    #
    # def submit(self, data):
    #     # 进件
    #     return self._request(method="submit", biz_data=data).json()
    #
    # def status(self, data):
    #     # 订单状态查询
    #     return self._request(method="status", biz_data=data).json()
    #
    # def submit_check(self, data):
    #     # 进件资格检查
    #     return self._request(method="submit_check", biz_data=data).json()
    #
    # def submit_result(self, data):
    #     # 进件结果
    #     return self._request(method="submit_result", biz_data=data).json()
    #
    # def conclusion(self, data):
    #     # 授信结果查询
    #     return self._request(method="conclusion", biz_data=data).json()
    #
    # def conclusion_detail(self, data):
    #     # 授信额度查询
    #     return self._request(method="conclusion_detail", biz_data=data).json()
    #
    # def contract(self, data):
    #     # 授信协议查询
    #     return self._request(method="contract", biz_data=data).json()
    #
    # def order_contract(self, data):
    #     # 获取借款协议
    #     return self._request(method="order_contract", biz_data=data).json()
    #
    # def scene_url(self, data):
    #     # 获取下载链接
    #     return self._request(method="scene_url", biz_data=data).json()
    #
    # def find_repay_url(self, data):
    #     # 获取还款链接
    #     return self._request(method="find_repay_url", biz_data=data).json()
    #
    # def is_need_add_verify(self, data):
    #     # 是否需要增验
    #     return self._request(method="is_need_add_verify", biz_data=data).json()
    #
    # def login_url(self, data):
    #     # login_url
    #     return self._request(method="login_url", biz_data=data).json()
    #
    # def h5_withdraw_url(self, data):
    #     # 获取h5借款url
    #     return self._request(method="h5_withdraw_url", biz_data=data).json()
    #
    # def loan_info(self, data):
    #     # 贷款信息查询
    #     return self._request(method="loan_info", biz_data=data).json()
    #
    # def order_status(self, data):
    #     # 订单状态
    #     return self._request(method="order_status", biz_data=data).json()
    #
    # def loan_record(self, data):
    #     # 查询借据列表
    #     return self._request(method="loan_record", biz_data=data).json()
    #
    # def confirm_url(self, data):
    #     # 下单
    #     return self._request(method="confirm_url", biz_data=data).json()
    #
    # def confirm_order(self, data):
    #     # 下单
    #     return self._request(method="confirm_order", biz_data=data).json()
    #
    # def confirm_sign(self, data):
    #     # 签约
    #     return self._request(method="confirm_sign", biz_data=data).json()
    #
    # def confirm_code(self, data):
    #     # 借款确认
    #     return self._request(method="confirm_code", biz_data=data).json()
    #
    # def confirm_vcode(self, data):
    #     # 借款确认
    #     return self._request(method="confirm_vcode", biz_data=data).json()
    #
    # def repayment_result(self, data):
    #     # 放款结果查询 repayment-result
    #     return self._request(method="repayment-result", biz_data=data).json()
    #
    # def trial(self, data):
    #     # 试算
    #     return self._request(method="trial", biz_data=data).json()
    #
    # def repay(self, data):
    #     # 还款
    #     return self._request(method="repay", biz_data=data).json()
    #
    # def repay_info(self, data):
    #     # 还款计划查询
    #     return self._request(method="repay_info", biz_data=data).json()
    #
    # def repay_result(self, data):
    #     # 还款结果查询
    #     return self._request(method="repay_result", biz_data=data).json()
    #
    # def repay_vcode(self, data):
    #     # 还款确认
    #     return self._request(method="repay_vcode", biz_data=data).json()


# class PushBaseRequest:
#     # 推送基类
#     def __init__(self, channel_id=None):
#         self.env = env
#         self.channel_id = channel_id
#
#     def _push_request(self, method, biz_data):
#         # 通用请求方法
#         res = hub_request(
#             self.env, channel_id=self.channel_id, method=method, biz_data=biz_data)
#         return res
#
#     def repay_vcode(self, data):
#         # 订单状态推送
#         return self._push_request(method="order_status", biz_data=data).json()
#
#     def conclusion(self, data):
#         # 授信推送
#         return self._push_request(method="conclusion", biz_data=data).json()
#
#     def repay_info(self, data):
#         # 还款计划推送
#         return self._push_request(method="repay_info", biz_data=data).json()
