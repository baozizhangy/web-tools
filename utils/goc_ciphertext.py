#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
GOC 接口加解密模块
用于 http://bm-sit.shangtoutech.com/chg/goc/bm/api 接口
加密方式：AES ECB + RSA SHA256WithRSA 签名
"""
import base64
import json
import time
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256


class GocSecurity:
    """
    GOC 接口加解密类
    - AES ECB 模式加密业务数据
    - RSA SHA256WithRSA 签名
    """

    # GOC 配置
    goc_config = {
        "APP_ID": "lxj",
        "AES_KEY": "dgfeg12678swospm",
        "PUBLIC_KEY": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqkVLpKUoCdmE1jef0gP84eRuzBz93iLpxUa4gEtjZtZLz+j17hHCxEN9uKaokJPm9e5yAx97Vg4Q8VsSEDIBbxUmRkpb7atVkIn6cgl8XorSssXPnfgnjcQVcQx6Pyn0tgpukxVgN2WNVzX4GmfqaHWb5BHzDP/zbd1nHjzoIrUa9bxQG/Ipz1rTv73TuDk/3eVNWblhNXt+ipPHMWbYQoS8UbIVhzavyaLVpeIo1WT7CwgkNwt/7UEdzOTv5angbVhxJLqntsuk041zo009NyGYn15xq5oZgTWQsUtKgo6DM9lZG/jsVZYtx17vu6mFhLvwZXL4994RGCuCGW9DaQIDAQAB",
        "PRIVATE_KEY": "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCqRUukpSgJ2YTWN5/SA/zh5G7MHP3eIunFRriAS2Nm1kvP6PXuEcLEQ324pqiQk+b17nIDH3tWDhDxWxIQMgFvFSZGSlvtq1WQifpyCXxeitKyxc+d+CeNxBVxDHo/KfS2Cm6TFWA3ZY1XNfgaZ+podZvkEfMM//Nt3WcePOgitRr1vFAb8inPWtO/vdO4OT/d5U1ZuWE1e36Kk8cxZthChLxRshWHNq/JotWl4ijVZPsLCCQ3C3/tQR3M5O/lqeBtWHEkuqe2y6TTjXOjTT03IZifXnGrmhmBNZCxS0qCjoMz2Vkb+OxVli3HXu+7qYWEu/Blcvj33hEYK4IZb0NpAgMBAAECggEAOwlJv+1vo3Ki5y9kH4o4bQ4qCGVo9FNAoKDzqa/56BcXNCA+3OuVjz0jYxmNyostgknJiCGrPtwjrbt42NqtupknqylvFEnaogHlLxLw50rU4R1K7iezdyjskkTUQgBHE7MsQZ0gvjRcvEc/HdC36r4UbhB3KCO6gHZKoaZWimmVkrs66L9jHAQlymgLXWLxGUeHVgNZr8A8ZWR//PMS8iVpE2yGLNrMJ7oZw10WykJRZELFFChMlKHJA1LWMObjluxmICqxPaHF8nt54T9QvyPV+KLYgBa6d9hwcFeJk1006e7L8AmGkIg7ITNPeG+Kwtp5rSQlIC0e30COyZwJAQKBgQDh/Ct0A+EvjJX56FGskjUsnLrWK3U7JtsTeSoGpyCn7bAliqRpQowLfVwDYBofatR4EqZ/I/XnOSZzPIXaJK0Si9xy3lTh6TTF679lv4VrAH+rC1Ti6aqvhn3tFYMdBMt/em70gEcdqBf/29LZzJ5iXKgXeHalgMbYfTuLE35YCQKBgQDA4sESTovB4XAkp06GjnAoKXdWruI8+4gMR3JSQyaFWrIw5mCyjOqfOOhFRZpRMFQm1FP5pm3+UDy3ath+f3Z+y3WPTB9vBx0tybg3aJVWdhOloKVsQAupwvwiRqTnh59AtMnaLuo7h8DyOjPJGgjtTNBND6ouh/+Vkav5NPqoYQKBgCV/zcoblrNoNb7ZcSwcutwjSdGeNn7RTMsncPTXqNCU3YTtQ6j/1PNXIvygZtVNyeH+3kf8tKJg1mOK6H8xVNLeCH+7KwStyQcKvqDorf/6fjTo1XYt5hfoTl8YEcCv+gC2VVEXNDXUnd7kIFHp5WJXE8GJSM7f1p838Lh8TJvZAoGAbEIYmRzKpgvQtFHO6gih/HihiV5ojk+ioTmseW1E/o3T+0wiM7SRrsHy44ZYQX89i/maFEGL9LO2EEAAuKbzq+Cn38Ca1+cHQn64TSj+wGNPTaOnlOUxZpuQhfBed7CP+nI95J52Suk7qvhtvk5FemKlesry+mDMW3dCLYHFuaECgYEAsJ5qVugdUBqJug3Vs+4BcjaARXyEVebt0m+IDymDwLDdNgPm5qUDPyumj3GIhIFZzq+WaiQ4KJJX4rmAApge6iYio41OC/fy5ukojJ+ekD6TqLW463FkSO+5nsglw7Lz0OaSPbAMlCS6pL1f+5jxSRJGS08I6tHb5iYZLve0yL4=",
        "PRIVATE_KEY_PASSWORD": ""
    }

    def __init__(self, config=None):
        """
        初始化
        :param config: 自定义配置，可选
        """
        if config:
            self.config = config
        else:
            self.config = self.goc_config

    @staticmethod
    def decode_key(aes_key):
        """
        解码 AES 密钥
        对应 Java: AESUtil.decodeKey(bizConfig.getBmGocAesKey())
        支持两种格式：
        1. 原始密钥字符串（16/24/32字节）
        2. Base64 编码的密钥
        """
        # 如果是 16/24/32 字节的字符串，直接作为密钥使用
        if len(aes_key) in (16, 24, 32):
            return aes_key.encode('utf-8')
        # 否则尝试 Base64 解码
        return base64.b64decode(aes_key)

    @staticmethod
    def pad_pkcs7(data_bytes):
        """PKCS7 填充（字节级别）"""
        pad_len = 16 - (len(data_bytes) % 16)
        return data_bytes + bytes([pad_len] * pad_len)

    @staticmethod
    def unpad_pkcs7(data_bytes):
        """去除 PKCS7 填充"""
        pad_len = data_bytes[-1]
        return data_bytes[:-pad_len]

    def aes_ecb_encrypt(self, data, aes_key):
        """
        AES ECB 模式加密
        对应 Java: AESUtil.encryptWithECB(data, AESUtil.decodeKey(aesKey), true)
        :param data: 待加密的字符串
        :param aes_key: AES 密钥（原始字符串或 Base64 编码）
        :return: Base64 编码的加密结果
        """
        try:
            # 解码 AES 密钥
            aes_key_bytes = self.decode_key(aes_key)

            # 先将数据编码为字节，再进行 PKCS7 填充
            data_bytes = data.encode('utf-8')
            padded_data = self.pad_pkcs7(data_bytes)

            # AES ECB 加密
            cipher = AES.new(aes_key_bytes, AES.MODE_ECB)
            encrypted_bytes = cipher.encrypt(padded_data)

            # Base64 编码
            return base64.b64encode(encrypted_bytes).decode('utf-8')
        except Exception as e:
            print(f"AES ECB 加密失败: {e}")
            raise

    def aes_ecb_decrypt(self, encrypted_base64, aes_key):
        """
        AES ECB 模式解密
        :param encrypted_base64: Base64 编码的加密数据
        :param aes_key: AES 密钥（原始字符串或 Base64 编码）
        :return: 解密后的字符串
        """
        try:
            # 解码 AES 密钥
            aes_key_bytes = self.decode_key(aes_key)

            # Base64 解码
            encrypted_bytes = base64.b64decode(encrypted_base64)

            # AES ECB 解密
            cipher = AES.new(aes_key_bytes, AES.MODE_ECB)
            decrypted_bytes = cipher.decrypt(encrypted_bytes)

            # 去除 PKCS7 填充
            decrypted_data = self.unpad_pkcs7(decrypted_bytes)

            return decrypted_data.decode('utf-8')
        except Exception as e:
            print(f"AES ECB 解密失败: {e}")
            raise

    @staticmethod
    def create_sign_str(data_map):
        """
        创建签名内容字符串
        对应 Java: RSAUtil.createSignStr(signMap)
        :param data_map: 待签名的字典
        :return: 签名内容字符串（按 key 排序后拼接）
        """
        sorted_keys = sorted(data_map.keys())
        return '&'.join([f"{k}={data_map[k]}" for k in sorted_keys if data_map[k] is not None])

    def sign_by_sha256_with_rsa(self, data_map, private_key_str, password=None):
        """
        RSA SHA256WithRSA 签名
        对应 Java: RSAUtil.signBySHA256WithRSA(map, privateKey, password)
        :param data_map: 待签名的字典（按 key 排序后拼接）
        :param private_key_str: Base64 编码的私钥
        :param password: 私钥密码（可选）
        :return: Base64 编码的签名
        """
        try:
            # 创建签名内容字符串
            sign_content = self.create_sign_str(data_map)

            # 解析私钥
            # 处理可能存在的 "privateKey=" 前缀
            if private_key_str.startswith("privateKey="):
                private_key_str = private_key_str.replace("privateKey=", "")

            key_bytes = base64.b64decode(private_key_str)
            if password:
                rsa_key = RSA.import_key(key_bytes, passphrase=password)
            else:
                rsa_key = RSA.import_key(key_bytes)

            # SHA256 哈希
            h = SHA256.new(sign_content.encode('utf-8'))

            # RSA 签名
            signature = pkcs1_15.new(rsa_key).sign(h)

            return base64.b64encode(signature).decode('utf-8')
        except Exception as e:
            print(f"RSA SHA256WithRSA 签名失败: {e}")
            raise

    def verify_by_sha256_with_rsa(self, public_key_str, sign_content, signature_base64):
        """
        RSA SHA256WithRSA 验签
        对应 Java: RSAUtil.verifyBySHA256WithRSA(publicKey, signContent, sign)
        :param public_key_str: Base64 编码的公钥
        :param sign_content: 签名内容字符串
        :param signature_base64: Base64 编码的签名
        :return: 验签是否成功
        """
        try:
            # 确保公钥格式正确
            if not public_key_str.startswith("-----BEGIN PUBLIC KEY-----"):
                public_key_str = f"-----BEGIN PUBLIC KEY-----\n{public_key_str}\n-----END PUBLIC KEY-----"

            public_key = RSA.import_key(public_key_str)

            # SHA256 哈希
            h = SHA256.new(sign_content.encode('utf-8'))

            # 解码签名
            signature = base64.b64decode(signature_base64)

            # 验签
            pkcs1_15.new(public_key).verify(h, signature)
            return True
        except (ValueError, TypeError) as e:
            print(f"RSA SHA256WithRSA 验签失败: {e}")
            return False

    def encrypt_data(self, data):
        """
        加密数据并生成请求对象
        对应 Java: bmSecurityService.encryptData(JSON.toJSONString(request))
        :param data: 待加密的数据（字符串或字典）
        :return: 加密后的请求字典 {appId, bizData, timestamp, sign}
        """
        # 如果是字典，转为 JSON 字符串
        if isinstance(data, dict):
            data = json.dumps(data, ensure_ascii=False, separators=(',', ':'))

        # 1. AES ECB 加密业务数据
        biz_data = self.aes_ecb_encrypt(data, self.config.get("AES_KEY"))

        # 2. 生成时间戳（秒级）
        timestamp = int(time.time())

        # 3. 构建请求对象
        bm_request = {
            "appId": self.config.get("APP_ID"),
            "bizData": biz_data,
            "timestamp": timestamp
        }

        # 4. RSA SHA256WithRSA 签名
        sign = self.sign_by_sha256_with_rsa(
            bm_request,
            self.config.get("PRIVATE_KEY"),
            self.config.get("PRIVATE_KEY_PASSWORD")
        )
        bm_request["sign"] = sign

        return bm_request

    def decrypt_response(self, response):
        """
        解密响应数据
        对应 Java 的响应解密流程：验签 + AES 解密
        :param response: 响应字典 {appId, bizData, timestamp, sign}
        :return: 解密后的业务数据（字典）
        :raises ValueError: 验签失败或解密失败
        """
        # 1. 构建签名 Map
        sign_map = {
            "appId": response.get("appId"),
            "timestamp": response.get("timestamp"),
            "bizData": response.get("bizData")
        }

        # 2. 创建签名内容字符串
        sign_content = self.create_sign_str(sign_map)

        # 3. 验签
        verify_result = self.verify_by_sha256_with_rsa(
            self.config.get("PUBLIC_KEY"),
            sign_content,
            response.get("sign")
        )

        if not verify_result:
            raise ValueError("验签失败")

        # 4. AES ECB 解密
        decrypted_biz_data = self.aes_ecb_decrypt(
            response.get("bizData"),
            self.config.get("AES_KEY")
        )

        # 5. 尝试解析为 JSON
        try:
            return json.loads(decrypted_biz_data)
        except json.JSONDecodeError:
            return decrypted_biz_data


if __name__ == '__main__':
    # 测试示例
    goc = GocSecurity()

    # 测试数据
    test_data = {
        "oprSys": "DL",
        "intfType": "HYQTZJInsightScore53102",
        "idNo": "513029199609289243",
        "custName": "张三"
    }

    print("原始数据:", json.dumps(test_data, ensure_ascii=False))

    # 注意：需要先配置正确的 AES_KEY 和 APP_ID 才能正常运行
    # encrypted_request = goc.encrypt_data(test_data)
    # print("加密后请求:", json.dumps(encrypted_request, ensure_ascii=False, indent=2))
