#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import requests, json, time
from utils.get_ciphertext import OsiApi
from utils.logger_util import web_logger
from config import get_urls


class BaseRequestUtil:
    # 实现http请求,解密响应数据
    def __init__(self,channel='lxj'):
        self.sign_data = OsiApi(channel=channel)


    def request_handle(self, request_data, api_path, env,method=None, url=None):
        """请求处理"""
        aes_key = self.sign_data.get_random_aes_key()
        web_logger.info(
            f'本次接口请求明文: {request_data},接口地址==={api_path},请求方法===={method}方法= None时，默认为post')
        encrypt_content = self.sign_data.aes_cbc_encrypt(aes_key, json.dumps(request_data))

        public_key = self.sign_data.config.get("OSI_PUBLIC_KEY")
        encrypt_key = self.sign_data.rsa_encrypt(public_key, aes_key)
        timestamp = int(time.time() * 1000)
        sign_content = encrypt_content + encrypt_key + str(timestamp) + self.sign_data.config.get("OSI_MD5_SALT")
        sign = self.sign_data.md5_hash(sign_content)

        req_body = {
            "timestamp": timestamp,
            "content": encrypt_content,
            "key": encrypt_key,
            "sign": sign
        }
        if url is None:
            url = get_urls(env)['FUND_LOAN']
        web_logger.info(f'请求的url==={url + api_path}')
        headers = {"Content-Type": "application/json"}
        if method is None or method == 'post':
            response = requests.post(url + api_path, json=req_body, headers=headers)
            web_logger.info(f'加密后请求参数==={req_body}')
            print(f"请求结果{response.text}")
            return response.text
        else:
            response = requests.get(url, params=req_body, headers=headers)
            return response.text

    def response_handle(self, resp_str):
        """响应处理"""
        resp_map = json.loads(resp_str)

        if "code" in resp_map:
            return {"code": resp_map["code"], "msg": resp_map["msg"]}

        sign_content = resp_map["content"] + resp_map["key"] + str(resp_map["timestamp"]) + self.sign_data.config.get(
            "OSI_MD5_SALT")
        calculated_sign = self.sign_data.md5_hash(sign_content)

        if resp_map["sign"] != calculated_sign:
            raise ValueError("响应结果验签失败")

        aes_key = self.sign_data.rsa_decrypt(self.sign_data.config.get("OSI_OUR_PRIVATE_KEY"), resp_map["key"])
        biz_data = self.sign_data.aes_cbc_decrypt(aes_key, resp_map["content"])
        return json.loads(biz_data)

    def get_request_data(self, request_data):
        """请求处理"""
        aes_key = self.sign_data.get_random_aes_key()
        web_logger.info(
            f'本次接口请求明文: {request_data}')

        encrypt_content = self.sign_data.aes_cbc_encrypt(aes_key, json.dumps(request_data))
        public_key = self.sign_data.config.get("OSI_PUBLIC_KEY")
        encrypt_key = self.sign_data.rsa_encrypt(public_key, aes_key)
        timestamp = int(time.time() * 1000)
        sign_content = encrypt_content + encrypt_key + str(timestamp) + self.sign_data.config.get("OSI_MD5_SALT")
        sign = self.sign_data.md5_hash(sign_content)

        req_body = {
            "timestamp": timestamp,
            "content": encrypt_content,
            "key": encrypt_key,
            "sign": sign
        }
        return req_body


class CommonRequest:
    def __init__(self, base_url='http://bm-sit.shangtoutech.com'):
        self.base_url = base_url

    def api_request(self, method, request_data, api_path):
        url = f"{self.base_url}{api_path}"
        if method.upper() == 'POST':
            res = requests.post(url, json=request_data)
            return res.text
        else:
            res = requests.get(url, params=request_data)
            return res.text


class SessionRequest:

    def __init__(self, user_no, credit_no, bm_user_no, scene=None):
        # self.base_url = base_url
        self.user_no = str(user_no)
        self.credit_no = str(credit_no)
        self.bm_user_no = bm_user_no
        self.session = requests.session()
        self.host = 'http://bm-sit.shangtoutech.com'
        self.scene = scene if scene else 'DRAW'

    def _get_date(self):
        return int(time.time() * 1000)

    def _get_header(self):
        return {
            'Content-Type': 'application/json',
            'Host': 'bm-sit.shangtoutech.com'
        }

    def _get_biz_data(self):
        biz_data = {
            "scene": self.scene,
            "userNo": self.user_no,
            "creditReqNo": self.credit_no
        }
        str_biz_data = json.dumps(biz_data)
        base_data = json.dumps({
            "bizData": str_biz_data,
            "channelId": "HUB_LXJ",
            "method": "bm_scene_url",
            "timestamp": self._get_date()
        })
        return base_data

    def get_base_url(self):
        url = f'{self.host}/clg/hub/api/channel/handleRequest'
        req = self.session.post(url, data=self._get_biz_data(), headers=self._get_header())
        try:
            return req.json()['data']['bizData']['url']
        except (TypeError, KeyError):
            return "用户数据异常"

    def get_session(self):
        url = self.get_base_url()
        if url == "用户数据异常":
            return False
        self.session.get(url)
        return True



common_request = CommonRequest()
if __name__ == '__main__':
    # data_json = {
    #     "mobileNoMd5": "38ccf3e5b64cc3136e79d00336da3e29"}
    # request_re = req_api.request_handle(data_json, "/userAccess")
    # print(req_api.response_handle(request_re))
    # data_json = {
    #     'url': 'http://bmtestprivate.oss-cn-shanghai.aliyuncs.com/bmtestprivate/ocr/hub/UR0954878282463973376/1739930734663/gdzmxd/HUB_IDCARD_FRONT.jpeg'}
    # # print(common_request.api_request('get', data_json, '/chg/ccs/api/p/file/access'))
    # # print(req_api.get_request_data(data_json))
    # A = {
    #     "timestamp": 1742300003106,
    #     "content": "cDj0spV6ZeqH4u1ujUCTEbIrNpy+BND/d1zV94qvOS6S/S0myQAVhHgGkufxm9aI4mbLBArSU1vNwA7zWdL6LHl1ryR8PYowTz04564zyqMdtmADjv/7pF7IO3sUOT4amfqDGb9l7n3hZCB78h78dp1AopeXd/yzZenjqyT4lejvkK+MM6sIJoclLLnDM1lmsvqhG1THKZ8hvx6TCnoKVQ==",
    #     "key": "rJ/XkyKAHwqHFGRrHRDNChrdvjUT0TPtxk124f2QTEbsWdJosorEDHtk0MzzqD2SLG8BmGqVdD7KhGjxyVVNWzwbxTRgd964iJNx2fp36Pm2lG0zapftqReRvd13SryMeTGp/WCftkpjyIthDRFSnlQy5Xr9+agj0pM85TAV0i1Gq7Br/3M6yIkmYPPa1kE0ZN3eZVlOve2LCru9oDMY4hH58m75X1Hk6m9dx3lT4dWMNNa2yTsBQNKxlEv6KFE45HJuGR6ksOpzsIk2DdTSNoCHIdwuv9ziZFPC/vyr0zoT2s3O6SadogvoxKbBDqhHx17vw8LB8/NC9rW4yj9hYw==",
    #     "sign": "8c54cd0564d4bf87612bc1ab89645786"
    # }
    # print(req_api.response_handle(json.dumps(A)))
    A = SessionRequest('UR98532952671213505TEST', 'CT788773509454TEST', '123')
    print(A.get_session())
