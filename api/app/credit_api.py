# #!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time

import requests

from utils.rest_client import RestClient
# 修复导入问题，注释掉错误的导入
# from config import credit_api


class Meta:
    def __init__(self, os="ios", appVersion="10.0", version="8.9",
                 branch="com.lightpalm.fenqia", duid="De32143", channel_id="LXJ_APP", product_code="PILOT_APP",
                 channel="app", cid="20106"):
        self.os = os
        self.appVersion = appVersion
        self.version = version
        self.branch = branch
        self.duid = duid
        self.timestamp = str(int(time.time()))
        self.channelId = channel_id
        self.channel = channel
        self.cid = cid
        self.product_code = product_code

    def to_dict(self):
        return {
            "os": self.os,
            "appVersion": self.appVersion,
            "version": self.version,
            "branch": self.branch,
            "duid": self.duid,
            "timestamp": self.timestamp,
            "channel": self.channel,
            "cid": self.cid,
            # "channelId":   self.channelId,
            # "productCode": "PILOT_APP",
            "channelId": self.channel,
            "productCode": self.product_code,
            "pd": self.product_code,
            "pid": self.product_code,
            "clientIp": "101.226.168.228"
        }


class Credit:
    """
    授信流程类，封装了授信流程的各个步骤接口。
    """

    def __init__(self, api_root_url, session=None, channel_id="HUB_TEST", product_code="PILOT_HUB"):
        self.user_no = None
        self.api_root_url = api_root_url
        self.session = session if session is not None else requests.Session()
        self.meta = Meta(channel=channel_id, product_code=product_code).to_dict()
        self.product_code = product_code

    # def update_cookies(self, cookies):
    #     # print(f"update_cookies::{cookies}")
    #     # print(f"ctoken===={cookies.get('ctoken')}")
    #     self.client.headers["C-Token"] = cookies.get("ctoken")

    def _apply_flow(self, data):
        """
        流程节点提交
        流程顺序：
        1、入口点击：entry_click
        2、OCR完成：ocr_ok
        3、人脸识别完成：live_ok
        4、联系人完成：contact_ok
        5、详细资料完成：profile_ok
        6、询问检查：submit_check
        7、绑卡完成：bind_ok
        8、授信申请提交完成：redit_submit_ok
        9、强弹阅读完成：protocols_ok
        :param data:
        :return:
        """
        url = credit_api["flow"]
        print(f"_apply_flow::url::{url}\n::json_data::{data}")
        return self._post_data(url, data)

    def _post_data(self, path, data):
        """
        提交数据
        :param data:
        :return:
        """
        json_data = {
            "meta": self.meta,
            "data": data
        }
        print(f"_post_data::url::{path}\n::json_data::{json_data}")
        return self.session.post(self.api_root_url + path, json=json_data)

    def flow_entry_click(self, entry: str = "entry_click"):
        """
        入口点击：entry_click
        :return: 若存在流程则返回当前流程节点，若不存在则新建流程并返回节点

        """
        flow_data = {
            "nodeType": "entry_click",
            "productCode": self.product_code,
            "entry": entry
        }
        return self._apply_flow(flow_data)

    def flow_entry_click2(self, entry: str = "entry_click"):
        """
        入口点击：entry_click
        :return: 若存在流程则返回当前流程节点，若不存在则新建流程并返回节点

        """
        flow_data = {
            "nodeType": "entry_click",
            "productCode": self.product_code,
            "processVersion": 1,
            "entry": entry
        }
        return self._apply_flow(flow_data)

    def ocr_source(self):
        """
        通过这个接口，判断用户在身份证页使用哪个厂商识别
        :return:
        """
        url = credit_api["ocr"]["ocr_source"]
        data = {}
        return self._post_data(url, data)

    def ocr_ks_ocr(self, ocr_url, mode, ocr_type=1):
        """
        调用旷世ocr
        ocrImageUrl:身份证照片存储地址url
        ocrType:身份证识别类型 0=扫描 1=相册
        ocrMode:身份证正反面标识（0-正面 1-反面）
        :return:
        """
        url = credit_api["ocr"]["ks_ocr"]
        data = {
            "ocrImageUrl": ocr_url,
            "ocrType": ocr_type,
            "ocrMode": mode
        }
        return self._post_data(url, data)

    def ocr_wz_token(self):
        """
        获取微众sdk使用的token，token作拉起sdk使用
        :return:
        """
        url = credit_api["ocr"]["wz_token"]
        data = {}
        return self._post_data(url, data)

    def ocr_wz_ocr(self, ocr_data):
        """
        调用微众ocr，data内容包括
        ocrImageUrl:身份证照片存储地址url
        ocrType:身份证识别类型 0=扫描 1=相册
        ocrMode:身份证正反面标识（0-正面 1-反面）
        uploadType:上传类型 1-正常上传 2-补传
        ocrPartner:识别机构
        flowNo:流程号
        info: 微众sdk识别出的信息，包含以下字段
        - name (string): 姓名，必需
        - gender (string): 性别，必需
        - nationality (string): 民族，必需
        - birth (string): 出生年月日，必需
        - idCard (string): 身份证号，必需
        - address (string): 证件地址，必需
        - authority (string): 签发机关，必需
        - validDate (string): 有效日期，必需
        :return:
        """
        url = credit_api["ocr"]["wz_ocr"]
        # data = {
        #         "ocrImageUrl": ocr_url,
        #         "ocrType": ocr_type,
        #         "ocrMode": mode,
        #         "ocrInfo": info
        #     }
        return self._post_data(url, ocr_data)

    def ocr_h5_ocr(self, ocr_url, mode, ocr_type, partner):
        """
        调用H5身份证识别
        ocrType: 1-扫描 2-照片
        ocrImageUrl:身份证照片存储地址url
        ocrType:身份证识别类型 0=扫描 1=相册
        ocrMode:身份证正反面标识（0-正面 1-反面）
        :return:
        """
        url = credit_api["ocr"]["h5_ocr"]
        data = {
            "ocrImageUrl": ocr_url,
            "ocrType": ocr_type,
            "ocrMode": mode,
            "ocrPartner": partner
        }
        return self._post_data(url, data)

    def ocr_save(self, data):
        """
        身份识别两要素信息存储
        :return:
        """
        url = credit_api["ocr"]["ocr_save"]
        return self._post_data(url, data)

    def ocr_flow_ok(self, entry: str = "entry_click", sub_flow_no: str = None):
        """
        身份证识别完成，节点提交
        :return:
        """
        flow_data = {
            "nodeType": "ocr_ok",
            "productCode": self.product_code,
            "entry": entry,
            "subFlowNo": sub_flow_no
        }
        return self._apply_flow(flow_data)

    def ocr_flow_ok2(self, entry: str = "entry_click", sub_flow_no: str = None):
        """
        身份证识别完成，节点提交
        :return:
        """
        flow_data = {
            "nodeType": "ocr_ok",
            "productCode": self.product_code,
            "processVersion": 1,
            "entry": entry,
            "subFlowNo": sub_flow_no
        }
        return self._apply_flow(flow_data)

    def face_source(self):
        """
        获取人脸识别方式
        :return:
        """
        url = credit_api["face"]["face_source"]
        data = {}
        return self._post_data(url, data)

    def face_ks_token(self):
        """
        获取旷世人脸识别token
        :return:
        """
        url = credit_api["face"]["ks_token"]
        data = {}
        return self._post_data(url, data)

    def face_ks_verify(self, data):
        """
        旷世人脸识别
        :return:
        """
        url = credit_api["face"]["ks_verify"]
        return self._post_data(url, data)

    def face_wz_token(self):
        """
        获取微众人脸识别token
        :return:
        """
        url = credit_api["face"]["wz_token"]
        data = {}
        return self._post_data(url, data)

    def face_wz_verify(self, token):
        """
        微众人脸识别
        :return:
        """
        url = credit_api["face"]["wz_verify"]
        data = {"bizToken": token}
        return self._post_data(url, data)

    def face_flow_ok(self, sub_flow_no, entry: str = "entry_click"):
        """
        人脸识别完成，节点提交
        :return:
        """
        flow_data = {
            "nodeType": "live_ok",
            "productCode": self.product_code,
            "entry": entry,
            "subFlowNo": sub_flow_no
        }
        return self._apply_flow(flow_data)

    def face_flow_ok2(self, sub_flow_no, entry: str = "entry_click"):
        """
        人脸识别完成，节点提交
        :return:
        """
        flow_data = {
            "nodeType": "live_ok",
            "productCode": self.product_code,
            "entry": entry,
            "processVersion": 1,
            "subFlowNo": sub_flow_no
        }
        return self._apply_flow(flow_data)

    def contact_query(self):
        """
        查询已保存联系人信息
        :return:
        """
        url = credit_api["contact"]["query"]
        data = {}
        return self._post_data(url, data)

    def contact_operate(self, data):
        """
        保存联系人信息
        :return:
        """
        url = credit_api["contact"]["operate"]
        return self._post_data(url, data)

    def contact_flow_ok(self, sub_flow_no, entry: str = "entry_click"):
        """
        联系人完成，节点提交
        :return:
        """
        flow_data = {
            "nodeType": "contact_ok",
            "productCode": self.product_code,
            "entry": entry,
            "subFlowNo": sub_flow_no
        }
        return self._apply_flow(flow_data)

    def contact_flow_ok2(self, sub_flow_no, entry: str = "entry_click"):
        """
        联系人完成，节点提交
        :return:
        """
        flow_data = {
            "nodeType": "contact_ok",
            "productCode": self.product_code,
            "processVersion": 1,
            "entry": entry,
            "subFlowNo": sub_flow_no
        }
        return self._apply_flow(flow_data)

    def profile_query(self, flow_no):
        """
        查询已保存详细资料信息
        :return:
        """
        url = credit_api["profile"]["query"]
        data = {"flowNo": flow_no}
        return self._post_data(url, data)

    def profile_operate(self, data):
        """
        保存详细资料信息
        :return:
        """
        url = credit_api["profile"]["operate"]
        return self._post_data(url, data)

    def profile_flow_ok(self, sub_flow_no, entry: str = "entry_click"):
        """
        详细资料完成，节点提交
        :return:
        """
        flow_data = {
            "nodeType": "profile_ok",
            "productCode": self.product_code,
            "entry": entry,
            "subFlowNo": sub_flow_no
        }
        return self._apply_flow(flow_data)

    def profile_flow_ok2(self, sub_flow_no, entry: str = "entry_click"):
        """
        详细资料完成，节点提交
        :return:
        """
        flow_data = {
            "nodeType": "profile_ok",
            "productCode": self.product_code,
            "entry": entry,
            "processVersion": 1,
            "subFlowNo": sub_flow_no
        }
        return self._apply_flow(flow_data)

    # def loading_flow_ok(self, sub_flow_no, entry: str = "tds调用"):
    #     """
    #     loading完成，业务中为分发调用，节点提交，废弃
    #     :return:
    #     """
    #     flow_data = {
    #         "nodeType": "loading_ok",
    #         "productCode": self.product_code,
    #         "entry": entry,
    #         "subFlowNo": sub_flow_no
    #     }
    #     return self._apply_flow(flow_data)

    def flow_submit_check(self, sub_flow_no, entry: str = "entry_click"):
        """
        loading页检查
        :return: 若存在流程则返回当前流程节点，若不存在则新建流程并返回节点

        """
        flow_data = {
            "nodeType": "submit_check",
            "productCode": self.product_code,
            "entry": entry,
            "subFlowNo": sub_flow_no
        }
        return self._apply_flow(flow_data)

    def flow_submit_check2(self, sub_flow_no, entry: str = "entry_click"):
        """
        loading页检查
        :return: 若存在流程则返回当前流程节点，若不存在则新建流程并返回节点
        """
        flow_data = {
            "nodeType": "submit_check",
            "productCode": self.product_code,
            "processVersion": 1,
            "entry": entry,
            "subFlowNo": sub_flow_no
        }
        return self._apply_flow(flow_data)

    def bind_ok(self, sub_flow_no, entry: str = "entry_click"):
        """
        绑卡节点完成，节点提交
        :return:
        """
        flow_data = {
            "nodeType": "bind_ok",
            "productCode": self.product_code,
            "entry": entry,
            "subFlowNo": sub_flow_no
        }
        return self._apply_flow(flow_data)

    def bind_ok2(self, sub_flow_no, entry: str = "entry_click"):
        """
        绑卡节点完成，节点提交
        :return:
        """
        flow_data = {
            "nodeType": "bind_ok",
            "productCode": self.product_code,
            "entry": entry,
            "processVersion": 1,
            "subFlowNo": sub_flow_no
        }
        return self._apply_flow(flow_data)

    def page_query(self, flow_no):
        """
        获取授信申请页面展示信息
        Returns:
        """
        url = credit_api["apply_page"]["query"]
        data = {"flowNo": flow_no}
        return self._post_data(url, data)

    def page_upload(self, data):
        """
        授信申请页面信息上传
         {
        "expectAmount": "42",
        "loanTerm": "nisi pariatur adipisicing",
        "loanPurpose": "magna ut dolore ipsum eu",
        "choiceFundCodeList": ["38"],
        "flowNo": "aute do consectetur"
    }
        Returns:

        """
        url = credit_api["apply_page"]["upload"]
        print(f"========page_upload:{data}")
        return self._post_data(url, data)

    def page_flow_ok(self, sub_flow_no, entry: str = "entry_click"):
        """
        详细资料完成，节点提交
        :return:
        """
        flow_data = {
            "nodeType": "credit_submit_ok",
            "productCode": self.product_code,
            "entry": entry,
            "subFlowNo": sub_flow_no
        }
        return self._apply_flow(flow_data)

    def agreement_query(self, flow_no):
        url = credit_api["agreement"]["query"]
        data = {
            "agreementScene": "00",
            "creditBizReq": {
                "flowNo": flow_no
            }
        }
        return self._post_data(url, data=data)

    def agreement_save(self, flow_no, org_list):
        url = credit_api["agreement"]["save"]
        data = {
            "flowNo": flow_no,
            "loanNo": "",
            "orgCodes": org_list,
            "agreementScene": "00",
            "readResult": "agree",
            "readTime": 3
        }
        return self._post_data(url, data=data)

    def agreement_flow_ok(self, sub_flow_no, entry: str = "entry_click"):
        """
        详细资料完成，节点提交
        :return:
        """
        flow_data = {
            "nodeType": "protocols_ok",
            "productCode": self.product_code,
            "entry": entry,
            "subFlowNo": sub_flow_no
        }
        return self._apply_flow(flow_data)

    def agreement_flow_ok2(self, sub_flow_no, entry: str = "entry_click"):
        """
        详细资料完成，节点提交
        :return:
        """
        flow_data = {
            "nodeType": "protocols_ok",
            "productCode": self.product_code,
            "processVersion": 1,
            "entry": entry,
            "subFlowNo": sub_flow_no
        }
        return self._apply_flow(flow_data)

    def result_query(self, flow_no):
        url = credit_api["apply_result"]["query"]
        data = {"flowNo": flow_no}
        return self._post_data(url, data)

    def result_refresh(self, appl_no):
        url = credit_api["apply_result"]["refresh"]
        json_data = {"applNo": appl_no}
        return self.session.post(self.api_root_url + url, json=json_data)

    def home_info(self):
        url = credit_api["home"]["page_info"]
        return self._post_data(url, data={})

    def append_white(self, mobile, api_root_url='https://bm-sit.swfitpy.com/'):
        """
        通过手机号添加风险白名单
        """
        url = credit_api["white"]
        json_data = {
            "mobileNo": mobile,
            "judgeType": 2,
            "status": 1,
            "type": "string"
        }
        return self.session.post(api_root_url + url, json=json_data)

#