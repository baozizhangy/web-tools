#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from enum import Enum


class ChannelMethodsEnum(Enum):
    # 渠道方法枚举，对应基类或渠道类中实现的方法
    # 通用提交方法
    GENERAL_SUBMIT = ("general_submit", "通用提交", "push_data")
    # 测试代码实现的方法枚举
    GET_CHECK_DATA = ("get_check_data", "获取准入参数", "get_param")
    GET_REGISTER_DATA = ("get_register_data", "获取注册参数", "get_param")
    GET_PROFILE_DATA = ("get_profile_data", "获取详细资料参数", "get_param")
    GET_CREDIT_DATA = ("get_credit_data", "获取授信参数", "get_param")
    GET_DRAW_URL = ("get_draw_url", "获取借款URL", "get_param")
    GET_REPAY_URL = ("get_repay_url", "获取还款URL", "get_param")
    # 业务系统渠道方法枚举
    CHECK = ("check", "准入", "push_data")
    REGISTER = ("register", "注册", "push_data")
    BANK_LIST = ("bank_list", "支持的银行卡列表", "push_data")
    BANK_INFO = ("bank_info", "查询用户已绑卡信息", "push_data")
    BIND_LIST = ("bind_list", "查询绑卡列表", "push_data")
    NEED_BIND = ("need_bind", "用户绑卡查询接口", "push_data")
    NEED_BIND_CARD = ("need_bind_card", "获取用户准入后流程参数", "push_data")
    BIND_URL = ("bind_url", "获取前置绑卡URL", "push_data")
    BIND_QUERY = ("bind_query", "签约绑卡查询", "push_data")
    BIND_CARD = ("bind_card", "绑卡", "push_data")
    BIND_VERIFY = ("bind_verify", "绑卡验证", "push_data")
    GET_PROFILE = ("get_profile", "信息采集", "push_data")
    # yixianghua
    PROFILES = ("profiles", "信息补充提交", "push_data")
    SEND_DATA = ("send_data", "渠道推送进件数据", "push_data")
    EXTRA_SEND_DATA = ("extra_send_data", "补充数据", "push_data")
    # 全民
    PUSH_PHASE_ONE = ("push_phase_one", "推送阶段一", "push_data")
    # 全民
    PUSH_PHASE_TWO = ("push_phase_two", "推送阶段二", "push_data")
    SUBMIT = ("submit", "进件", "push_data")
    STATUS = ("status", "订单状态查询", "push_data")
    SUBMIT_CHECK = ("submit_check", "进件资格检查", "push_data")
    SUBMIT_RESULT = ("submit_result", "进件结果", "push_data")
    CONCLUSION = ("conclusion", "授信结果查询", "push_data")
    CONCLUSION_DETAIL = ("conclusion_detail", "授信额度查询", "push_data")
    CONTRACT = ("contract", "授信协议查询", "push_data")
    ORDER_CONTRACT = ("order_contract", "获取借款协议", "push_data")
    SCENE_URL = ("scene_url", "获取下载链接", "push_data")
    # yixianghua 还款地址查询scene_url_repay
    FIND_REPAY_URL = ("find_repay_url", "还款地址查询", "push_data")
    # yixianghua
    IS_NEED_ADD_VERIFY = ("is_need_add_verify", "是否需要增验", "push_data")
    LOGIN_URL = ("login_url", "登录URL", "push_data")
    H5_WITHDRAW_URL = ("h5_withdraw_url", "获取h5借款url", "push_data")
    LOAN_INFO = ("loan_info", "贷款信息查询", "push_data")
    ORDER_STATUS = ("order_status", "订单状态", "push_data")
    LOAN_RECORD = ("loan_record", "查询借据列表", "push_data")
    CONFIRM_URL = ("confirm_url", "下单", "push_data")
    CONFIRM_ORDER = ("confirm_order", "下单", "push_data")
    CONFIRM_SIGN = ("confirm_sign", "签约", "push_data")
    CONFIRM_CODE = ("confirm_code", "借款确认", "push_data")
    CONFIRM_VCODE = ("confirm_vcode", "借款验证", "push_data")
    FUNDED_RESULT = ("repayment_result", "放款结果查询", "push_data")
    TRIAL = ("trial", "试算", "push_data")
    REPAY = ("repay", "还款", "push_data")
    REPAY_INFO = ("repay_info", "还款计划查询", "push_data")
    REPAY_RESULT = ("repay_result", "还款结果查询", "push_data")
    REPAY_VCODE = ("repay_vcode", "还款确认", "push_data")
    # 推送接口
    ORDER_STATUS_PUSH = ("order_status", "订单状态推送", "push_data")
    CONCLUSION_PUSH = ("conclusion", "授信推送", "push_data")
    REPAY_INFO_PUSH = ("repay_info", "还款计划推送", "push_data")

    def __init__(self, method, method_name, method_type):
        self.method = method
        self.method_name = method_name
        self.method_type = method_type

    def __str__(self):
        return str({"method": self.value[0], "method_name": self.value[1], "method_type": self.value[2]})
