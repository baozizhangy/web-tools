#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
测试数据管理模块
用于统一管理接口自动化测试中的测试数据
"""

import random
from utils.personal_util import get_mobile_no, get_id_no, get_person_name


class TestDataManager:
    """测试数据管理器"""

    @staticmethod
    def get_test_user():
        """获取测试用户数据"""
        return {
            "mobile": get_mobile_no(),
            "id_no": get_id_no(),
            "name": get_person_name()
        }

    @staticmethod
    def get_test_credentials():
        """获取测试凭证数据"""
        return {
            "valid_code": "123456",  # 有效验证码示例
            "invalid_code": "666666"  # 无效验证码示例
        }

    @staticmethod
    def get_test_profile_data():
        """获取测试用户资料数据"""
        education_options = ["01", "02", "03", "04", "05"]  # 对应:研究生,大学本科,大学专科,高中或中专,初中及以下
        marriage_options = ["01", "02", "03", "04"]  # 对应:未婚,离异,丧偶,已婚
        income_options = ["01", "02", "03", "04", "05"]  # 对应:3000以下,3000-6000,6000-10000,10000-30000,30000以上
        
        return {
            "education": random.choice(education_options),
            "marriage": random.choice(marriage_options),
            "income": random.choice(income_options),
            "address": "上海市-上海市辖区-徐汇区",
            "address_detail": "徐汇徐汇徐汇徐汇徐汇地址详细信息"
        }