#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import allure, pytest, json
from pytestAutoTest.business.fixture_account import get_case_data, get_init_url
from utils.base_request_util import BaseRequestUtil


@allure.epic("API模式")
@allure.feature("授信模块")
@allure.suite("撞库节点")
class TestCheckUser:
    @allure.story("登录成功场景")
    @allure.title("使用正确的验证码登录成功")
    @pytest.mark.parametrize('case',
                             [pytest.param(i) for i in get_case_data("data\ApiData\check_data.yaml")['checkout']])
    def test_checkout_user(self, case):
        req_api = BaseRequestUtil()
        path = case["path"]
        mobile = case["mobile"]
        id_card = case["id_card"]
        result = case["result"]
        with allure.step(f"{mobile}开始执行"):
            req_data = {"mobileNoMd5": mobile, "idNoMd5": id_card}
            print(f"{req_data}请求参数")
            req = req_api.request_handle(req_data, path, "BM_SIT")
            res = req_api.response_handle(req)
            print(f"{res}请求结果")
            assert res.get("bizData").get("result") == result
