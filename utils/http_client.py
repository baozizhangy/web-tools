#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
通用HTTP客户端工具类
"""

import http.client
import json
import ssl
from typing import Dict, Any, Optional
from utils.logger_util import auto_logger


class HttpClient:
    """HTTP客户端工具类"""

    def __init__(
        self,
        base_url: str,
        default_headers: Optional[Dict[str, str]] = None,
        verify_ssl: bool = True,
    ):
        """
        初始化HTTP客户端

        Args:
            base_url: 基础URL (例如: "wodek-sit.shangtoutech.com")
            default_headers: 默认请求头
            verify_ssl: 是否校验HTTPS证书
        """
        self.base_url = base_url
        self.default_headers = default_headers or {}
        self.verify_ssl = verify_ssl
        self.logger = auto_logger

    def request(self, method: str, url: str, payload: Any = None, headers: Optional[Dict[str, str]] = None) -> Dict[
        str, Any]:
        """
        发送HTTP请求

        Args:
            method: HTTP方法 (GET, POST, PUT, DELETE等)
            url: 请求URL
            payload: 请求体数据
            headers: 请求头

        Returns:
            dict: 响应数据
        """
        request_headers = self.default_headers.copy()
        if headers:
            request_headers.update(headers)

        if isinstance(payload, dict) or isinstance(payload, list):
            payload_data = json.dumps(payload)
            if 'Content-Type' not in request_headers and 'content-type' not in request_headers:
                request_headers['Content-Type'] = 'application/json'
        elif payload is None:
            payload_data = ''
        else:
            payload_data = str(payload)

        self.logger.info(f"发送请求: {method} {self.base_url}{url}")
        self.logger.debug(f"请求头: {request_headers}")
        self.logger.debug(f"请求体: {payload_data}")

        try:
            if self.base_url.startswith("https://"):
                host = self.base_url[8:]
                context = None if self.verify_ssl else ssl._create_unverified_context()
                conn = http.client.HTTPSConnection(host, context=context)
            elif self.base_url.startswith("http://"):
                host = self.base_url[7:]
                conn = http.client.HTTPConnection(host)
            else:
                context = None if self.verify_ssl else ssl._create_unverified_context()
                conn = http.client.HTTPSConnection(self.base_url, context=context)

            conn.request(method, url, payload_data, request_headers)
            res = conn.getresponse()
            data = res.read()
            conn.close()

            try:
                response_data = json.loads(data.decode("utf-8"))
            except json.JSONDecodeError:
                response_data = data.decode("utf-8")

            self.logger.info(f"请求成功: {res.status}")
            self.logger.debug(f"响应数据: {response_data}")

            return {
                "status_code": res.status,
                "headers": dict(res.headers),
                "data": response_data
            }

        except Exception as e:
            self.logger.error(f"请求失败: {str(e)}")
            raise

    def get(self, url: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """发送GET请求"""
        return self.request("GET", url, headers=headers)

    def post(self, url: str, payload: Any = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """发送POST请求"""
        return self.request("POST", url, payload, headers)

    def put(self, url: str, payload: Any = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """发送PUT请求"""
        return self.request("PUT", url, payload, headers)

    def delete(self, url: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """发送DELETE请求"""
        return self.request("DELETE", url, headers=headers)


# 便捷函数
def create_https_client(
    base_url: str,
    default_headers: Optional[Dict[str, str]] = None,
    verify_ssl: bool = True,
) -> HttpClient:
    """
    创建HTTPS客户端

    Args:
        base_url: 基础URL
        default_headers: 默认请求头
        verify_ssl: 是否校验HTTPS证书

    Returns:
        HttpClient: HTTP客户端实例
    """
    return HttpClient(base_url, default_headers, verify_ssl=verify_ssl)


if __name__ == '__main__':
    client = HttpClient(
        "widek-sit.shangtoutech.com",
        {
            'Authorization': 'Basic d2lkZWs6VFZSSmVrNUVWVEk9',
            'Cookie': 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219d4272aa231e5b-0c40e9bc6f87c3-28623615-287859-19d4272aa2418b0%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTlkNDI3MmFhMjMxZTViLTBjNDBlOWJjNmY4N2MzLTI4NjIzNjE1LTI4Nzg1OS0xOWQ0MjcyYWEyNDE4YjAifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%7D; sidebarStatus=1; Admin-Token=; Refresh-Token='
        },
        verify_ssl=False,
    )

    response = client.post(
        "/widek-api/manage/login?username=coupon&password=RnrDNyb2MfBFyacbr1qq818SvWxx4Na7TNtdPOeZ0%2FXuW%2FbjtR%2BeOf3u0e3ekjDJwZ1cxY01YV%2FXDvODvj8z9g%3D%3D&code=1",
        payload=''
    )
    print(response)
