#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import base64
import hashlib


def md5_encrypt(text):
    # md5加密
    # 创建MD5对象
    md5 = hashlib.md5()

    # 更新要加密的数据
    md5.update(str(text).encode('utf-8'))

    # 获取加密结果
    encrypted_text = md5.hexdigest()

    return encrypted_text


class Base64Utils:
    @staticmethod
    def encode(text):
        """
        Base64 编码
        :param text: 待编码的文本
        :return: Base64 编码后的文本
        """
        if isinstance(text, bytes):
            return base64.b64encode(text).decode()
        elif isinstance(text, str):
            return base64.b64encode(text.encode()).decode()
        else:
            raise TypeError("Input must be a string or bytes")

    @staticmethod
    def decode(base64_text):
        """
        Base64 解码
        :param base64_text: Base64 编码后的文本
        :return: 解码后的文本
        """
        return base64.b64decode(base64_text.encode()).decode()

    @staticmethod
    def url_safe_encode(text):
        """
        URL 安全的 Base64 编码
        :param text: 待编码的文本
        :return: URL 安全的 Base64 编码文本
        """
        if isinstance(text, str):
            text = text.encode()
        return base64.urlsafe_b64encode(text).decode().rstrip('=')

    @staticmethod
    def url_safe_decode(base64_text):
        """
        URL 安全的 Base64 解码
        :param base64_text: URL 安全的 Base64 编码文本
        :return: 解码后的文本
        """
        padding = '=' * (4 - (len(base64_text) % 4))
        base64_text += padding
        return base64.urlsafe_b64decode(base64_text.encode()).decode()
