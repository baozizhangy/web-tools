import json
import re
from time import sleep
from typing import Any, Optional

import requests
from jsonpath_ng import parse

from config import api_get_url, db_conn
from utils.logger_util import web_logger


INIT_URL = (
    "http://bm-sit.shangtoutech.com"
    "/clg/bcs/api/p/hub/v1/page/load/22572"
    "?td_channelid=2001&loadingPage=bind"
    "&channelSource=WX_MP&channelId=HUB_LXJ&h5Type=4"
)


class H5Login:
    """H5 登录及通用请求封装类。"""

    def __init__(self, env: str, mobile_no: str):
        self.env = env
        self.mobile_no = mobile_no
        self.api_path = api_get_url(env)
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self.bc_token: str = ""
        self.token: str = ""
        self.h5_version: str = ""
        self.logged_in = False

    def request(self, method: str, path: str, **kwargs) -> Any:
        url = f"{self.api_path}/{path.lstrip('/')}"
        web_logger.info(
            f"[H5Request] {method.upper()} {url} | Payload: {kwargs.get('json') or kwargs.get('params')}"
        )

        response = self.session.request(method, url, **kwargs)
        web_logger.info(f"[H5Response] Status: {response.status_code} | Body: {response.text}")

        assert response.status_code == 200, f"接口请求失败: {response.status_code}, 响应: {response.text}"

        try:
            return response.json()
        except Exception:
            return response.text

    def post(self, path: str, data: Optional[Any] = None, meta: Optional[dict] = None, **kwargs) -> Any:
        if not self.logged_in:
            self.login()

        payload = {
            "data": data if data is not None else {},
            "meta": meta or {
                "version": self.h5_version,
                "channelId": "2001"
            }
        }
        return self.request("POST", path, json=payload, **kwargs)

    def get(self, path: str, params: Optional[Any] = None, **kwargs) -> Any:
        if not self.logged_in:
            self.login()
        return self.request("GET", path, params=params, **kwargs)

    def _init_bc_token(self):
        web_logger.info(f"[H5Login] Step1 GET {INIT_URL}")
        resp = self.session.get(INIT_URL)
        assert resp.status_code == 200, f"init_url 请求失败: {resp.status_code}"

        self.bc_token = resp.headers.get("BC-Token", "")
        if self.bc_token:
            self.session.headers.update({"BC-Token": self.bc_token})

        match = re.search(r'lexiaorong/([0-9.]+)/', resp.text)
        self.h5_version = match.group(1) if match else "1.0.137"
        web_logger.info(f"[H5Login] BC-Token: {self.bc_token} | Version: {self.h5_version}")

    def _send_sms_code(self):
        data = {
            "mobileNo": self.mobile_no,
            "codeType": "MESSAGE",
            "smsCodeScene": "",
            "channelSource": "WX_MP"
        }
        res = self.post_without_login("clg/lps/api/p/bm/login/v1/sendCode", data=data)
        assert res.get("data", {}).get("message") == "发送成功", f"发送验证码失败: {res}"

    def _query_sms_code(self) -> str:
        sql = (
            "SELECT params FROM cns.p_notice_record "
            "WHERE user_no = ("
            f"    SELECT user_no FROM cis.u_user WHERE mobile_no_md5 = md5('{self.mobile_no}')"
            ") "
            "AND event_code = 'e_login_verify_code' "
            "ORDER BY id DESC LIMIT 1"
        )
        sleep(3)
        web_logger.info(f"[H5Login] Step3 DB query: {sql}")
        result = db_conn(self.env).select_one(sql)
        assert result.get("code") == "0" and result.get("data"), f"数据库查询验证码失败: {result}"

        sms_code = str(parse("$.params.code").find(json.loads(result["data"]["params"]))[0].value)
        web_logger.info(f"[H5Login] 短信验证码: {sms_code}")
        return sms_code

    def _verify_login(self, sms_code: str):
        data = {
            "mobileNo": self.mobile_no,
            "smsCode": sms_code,
            "loginType": "SMS_CODE",
            "channelSource": "WX_MP",
            "channelId": "HUB_LXJ"
        }

        url = f"{self.api_path}/clg/lps/api/p/bm/login/v1/login"
        payload = {"data": data, "meta": {"version": self.h5_version, "channelId": "2001"}}
        resp = self.session.post(url, json=payload)
        assert resp.status_code == 200, f"登录请求失败: {resp.status_code}"

        body = resp.json()
        self.token = (
            (body.get("data") or {}).get("token")
            or body.get("token")
            or resp.headers.get("BC-Token")
            or ""
        )
        assert self.token, f"登录成功但未获取到 Token: {body}"

        self.session.headers.update({"BC-Token": self.token})
        self.logged_in = True
        web_logger.info(f"[H5Login] 登录成功，Token: {self.token}")

    def post_without_login(self, path: str, data: Optional[Any] = None, meta: Optional[dict] = None, **kwargs) -> Any:
        payload = {
            "data": data if data is not None else {},
            "meta": meta or {
                "version": self.h5_version,
                "channelId": "2001"
            }
        }
        return self.request("POST", path, json=payload, **kwargs)

    def login(self) -> requests.Session:
        if self.logged_in:
            return self.session

        self._init_bc_token()
        self._send_sms_code()
        sms_code = self._query_sms_code()
        self._verify_login(sms_code)
        return self.session
