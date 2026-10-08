#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
import sys
from pathlib import Path

import allure

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from api.app.h5_login import H5Login


@allure.feature("H5 登录")
class TestH5Login:
    @allure.story("完整登录流程")
    def test_h5_full_login(self, env):
        mobile_no = "15329302800"
        h5 = H5Login(env=env, mobile_no=mobile_no)
        h5.login()

        with allure.step("验证接口复用"):
            res = h5.post("clg/lps/api/u/bm/repay/v1/repay/list", data={})
            assert res.get("code") in [0, "0", 200, "200"]


if __name__ == "__main__":
    h5 = H5Login(env="BM_SIT", mobile_no="14511936328")
    h5.login()
    result = h5.post("/clg/lps/api/u/bm/repay/v1/repay/list", data={})
    result_dict = result if isinstance(result, dict) else json.loads(result)
    print(f"接口结果: {result_dict}")
