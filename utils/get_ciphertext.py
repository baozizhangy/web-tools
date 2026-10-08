import base64, hashlib, secrets
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.PublicKey import RSA


# AES 加解密类
class OsiApi:

    # 全局配置
    lxj_config = {
        "OSI_PUBLIC_KEY": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAslEddvFlBka3Zv7eHF6lYMDbQlRYiJNpzpg5whxeDzz4bp1+/3oJBz5dpzTEvvtXUSLc2b9I3OhOITtK6rVh4rHNIptohwttxFvCjlXpI3ygW+YfYzC4yBeHTVR2luFLT8DKn5r+gYC0FFFbiymPr7OAhiOhlQ8V747EBElSwbpN2IDwRR4YFlg4JohMjd6upxkXkXWnr+bcCvrMFiHMEq3IQBc805dGpL+yD+Wg6VDJWy10Zs41ZzZGhSNiZS5Bjt2Td3tqoiz0dcw82KVF0b6sABMbooSyhxy9w7/fGjakS592hr+LAZzABDt2TOhjssOmyjE3ZilcOOuBhl4tzQIDAQAB",
        "OSI_MD5_SALT": "eqwrewrqewr",
        "OSI_OUR_PRIVATE_KEY": "MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCyUR128WUGRrdm/t4cXqVgwNtCVFiIk2nOmDnCHF4PPPhunX7/egkHPl2nNMS++1dRItzZv0jc6E4hO0rqtWHisc0im2iHC23EW8KOVekjfKBb5h9jMLjIF4dNVHaW4UtPwMqfmv6BgLQUUVuLKY+vs4CGI6GVDxXvjsQESVLBuk3YgPBFHhgWWDgmiEyN3q6nGReRdaev5twK+swWIcwSrchAFzzTl0akv7IP5aDpUMlbLXRmzjVnNkaFI2JlLkGO3ZN3e2qiLPR1zDzYpUXRvqwAExuihLKHHL3Dv98aNqRLn3aGv4sBnMAEO3ZM6GOyw6bKMTdmKVw464GGXi3NAgMBAAECggEBAKsL9hiPS9nuYaURm9tYyoh51pjUsawow5jiGp1herRhRulMeHL2C8z//PQUQRn1nPd+Wp0gyPLmf3OPHbjwznmXFnA45NaNlviBEKpaLG3W8TfWEYujQ8zkDOyXtb3bVNOm2napRbLR02ud8xMVhfgDVqjVavzB4MfPiaWW9CRRR8lEUHyMEV2u+eqYlJCaPwuF5f1itSoM5nYhmzb/Kl1HIqWIFIfELYUDNGTwIrPwWo/mwQL23mzfrd7QP0fT/VUYJkJu21DwjLHpTtkaNL2JpZH0lvZa8TeLnHWK7H/XTm5amBXXLMoCNf8Fs4M5b+r4fiLZfqo0R8lW0goOKWECgYEA5UxEON5A0j7uDMaOPRBxRv69pozpa4zO/r8KH30yGJ3OyyOo6d1Yq0PSPoDUIpkljqo9Hl36VY2koWZU6NQ5lGLZAK7lApUSFv2S5i8ZcKFeSgBTex+83ljF8MqdjKfBysEo6jK8xwn4q8U4L7/pge92NGV3SNdV79sBj0eR1DUCgYEAxxUFx3R+8b425dPFuk+El/N2GrGYB6a4IfVLltIgARI6SLmxZ8zQo7z07BmaYN/yShp9SszltH+C6rVeQaFDjwmFKAL9pXcTqrtjFn+t9Wa5BbhYemD7R2sx6yfkz5+8eZOMT/fNcPmL9qDBYooXo/DedUZza1gYcYDjPepv9jkCgYEAjugaeMrj4WUBHgs9qQcvYkzvy/Z0n+gRNinAWGHBsB/iOy7NXnvqgErzpKrMC4ghJSoqj1uI4ns1yLWrY7So8jctAcT+y742mQeO31EpbM3Vow9S+CCOqJDxRKIy0O/Y0tHR+yyGBRLM3dk7rF7SXH3u0LcQQeCbGbMH5NF5LKUCgYAPpCIxGoECwzwS8IF/ctHrElC8JinYqAudd2U580ZabzEvF4/NpPTbeHQRvK05YT7q/YvMfa6qcL47bIZ8R4xER64zh5CgGGvuJQzS7rMfLbPptCMXclkrsktYu2ipu1YWgzYp7kEw2BpcBSNMd6cF1V3U/vUAgQpimIrCCZJEWQKBgDiMc9WtMPzZhZob/WB+gNHTF1F+Hc3GTlh+RUnSJpsoY3Uf9BGpZBKzqIiJan0d1qi2VwbXnx5kp7rEKe5c8v9fhzkCHH/kG6F//0+hYD9Fq0vN52hk1ooHvFfdCL2oyGjNzxTD5YvEJA/o3np1BNYdfV+X6gtUUBCz23Tcio1r",
        "OSI_OUR_PRIVATE_KEY_PASSWORD": ""
    }
    wacai_config = {
            "OSI_PUBLIC_KEY": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCFnYFh2RX6ih3l7QdTJri2PDei0wfVSnsBlCT0cYAcL+k/zxmel0g5daRRlxw74AZsQvnWPZABLMU2EQOJbFcTw8cqMmytZsZu0XZyt1jxkmFMAtAoWcB5NuSYATVmhVz0A9bgQtjROXJlZsad+aga1Yi3541cOricLvsaS3SEnQIDAQAB",
            "OSI_MD5_SALT": "eqwrewrqewr",
            "OSI_OUR_PRIVATE_KEY": "MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBALa6y+ycpctvEct9AA2SUjzt+nMj5S/JG1edhnwdx9Qy/DBHyzL2NIPreARB9t4Fu01Owe5bt2xJXkS92BB7EfVpbV7A1zzdWCGhKOIhDvMDsqNZGu15QRxs+cN2FcEIIFd7UsuS7ztZwVjEola2L4OhuERMR5G/FdXfRbHVNgTnAgMBAAECgYBHpH9VmqlKVJbWgIDn0UmbB/cc86LlFGU6+dEDkq2JXiAQUeWyamN2oXihurcun3KrQci5So5kz3M9Ym13MLl+IxLxqAczsnEqBOtStTWISfDBX8igJWTFfUER4s2D2tYuWtSqhv4yUNcD8qdXB5Ml9WjCBo4AI0065G7kw4xvcQJBAPI0YMzJCAXoGnDVvpfB6nKdaIzCQN0xDN8R4kHio2zrdXoRPsAodERcdd5oyjzSmVJe0Ll0i4/6qvL753msyDkCQQDBIzSe6bHUzwp3PPmL/RCzqgY85hH7tWiIq2wzCjsVV80kZ8jdK7CqmNsIJWL/s+CSDgHQBFgd76g9xynJ+/YfAkBa/OpQhEULUwJ72RBcmnCk1hVsq50Ke17GfkVtUuLqDBp53Pih35CuDb4J63vuFX+bvhrTUMENObH2zkNLJmmhAkBBOdeKl5f0K9v3+wK4EUYztwcWSAjovhJIncQT1K+xfI6ObfJ7J0cpxieqr52oh6IfEVXxX5Y2vfpOqtVlHo+3AkEA3vRz2w5/2mDJJceQVvVkxqw0fYhZyWRCm783/sgCpndVKWG9A5sRhqO7FHCGZXbxq5uyb5cFMFYZZalvV1qNFA==",
            "OSI_OUR_PRIVATE_KEY_PASSWORD": ""

        }
    
    # GOC 接口配置 - 用于 http://bm-sit.shangtoutech.com/chg/goc/bm/api
    goc_config = {
        "OSI_PUBLIC_KEY": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqkVLpKUoCdmE1jef0gP84eRuzBz93iLpxUa4gEtjZtZLz+j17hHCxEN9uKaokJPm9e5yAx97Vg4Q8VsSEDIBbxUmRkpb7atVkIn6cgl8XorSssXPnfgnjcQVcQx6Pyn0tgpukxVgN2WNVzX4GmfqaHWb5BHzDP/zbd1nHjzoIrUa9bxQG/Ipz1rTv73TuDk/3eVNWblhNXt+ipPHMWbYQoS8UbIVhzavyaLVpeIo1WT7CwgkNwt/7UEdzOTv5angbVhxJLqntsuk041zo009NyGYn15xq5oZgTWQsUtKgo6DM9lZG/jsVZYtx17vu6mFhLvwZXL4994RGCuCGW9DaQIDAQAB",
        "OSI_MD5_SALT": "eqwrewrqewr",
        "OSI_OUR_PRIVATE_KEY": "privateKey=MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCqRUukpSgJ2YTWN5/SA/zh5G7MHP3eIunFRriAS2Nm1kvP6PXuEcLEQ324pqiQk+b17nIDH3tWDhDxWxIQMgFvFSZGSlvtq1WQifpyCXxeitKyxc+d+CeNxBVxDHo/KfS2Cm6TFWA3ZY1XNfgaZ+podZvkEfMM//Nt3WcePOgitRr1vFAb8inPWtO/vdO4OT/d5U1ZuWE1e36Kk8cxZthChLxRshWHNq/JotWl4ijVZPsLCCQ3C3/tQR3M5O/lqeBtWHEkuqe2y6TTjXOjTT03IZifXnGrmhmBNZCxS0qCjoMz2Vkb+OxVli3HXu+7qYWEu/Blcvj33hEYK4IZb0NpAgMBAAECggEAOwlJv+1vo3Ki5y9kH4o4bQ4qCGVo9FNAoKDzqa/56BcXNCA+3OuVjz0jYxmNyostgknJiCGrPtwjrbt42NqtupknqylvFEnaogHlLxLw50rU4R1K7iezdyjskkTUQgBHE7MsQZ0gvjRcvEc/HdC36r4UbhB3KCO6gHZKoaZWimmVkrs66L9jHAQlymgLXWLxGUeHVgNZr8A8ZWR//PMS8iVpE2yGLNrMJ7oZw10WykJRZELFFChMlKHJA1LWMObjluxmICqxPaHF8nt54T9QvyPV+KLYgBa6d9hwcFeJk1006e7L8AmGkIg7ITNPeG+Kwtp5rSQlIC0e30COyZwJAQKBgQDh/Ct0A+EvjJX56FGskjUsnLrWK3U7JtsTeSoGpyCn7bAliqRpQowLfVwDYBofatR4EqZ/I/XnOSZzPIXaJK0Si9xy3lTh6TTF679lv4VrAH+rC1Ti6aqvhn3tFYMdBMt/em70gEcdqBf/29LZzJ5iXKgXeHalgMbYfTuLE35YCQKBgQDA4sESTovB4XAkp06GjnAoKXdWruI8+4gMR3JSQyaFWrIw5mCyjOqfOOhFRZpRMFQm1FP5pm3+UDy3ath+f3Z+y3WPTB9vBx0tybg3aJVWdhOloKVsQAupwvwiRqTnh59AtMnaLuo7h8DyOjPJGgjtTNBND6ouh/+Vkav5NPqoYQKBgCV/zcoblrNoNb7ZcSwcutwjSdGeNn7RTMsncPTXqNCU3YTtQ6j/1PNXIvygZtVNyeH+3kf8tKJg1mOK6H8xVNLeCH+7KwStyQcKvqDorf/6fjTo1XYt5hfoTl8YEcCv+gC2VVEXNDXUnd7kIFHp5WJXE8GJSM7f1p838Lh8TJvZAoGAbEIYmRzKpgvQtFHO6gih/HihiV5ojk+ioTmseW1E/o3T+0wiM7SRrsHy44ZYQX89i/maFEGL9LO2EEAAuKbzq+Cn38Ca1+cHQn64TSj+wGNPTaOnlOUxZpuQhfBed7CP+nI95J52Suk7qvhtvk5FemKlesry+mDMW3dCLYHFuaECgYEAsJ5qVugdUBqJug3Vs+4BcjaARXyEVebt0m+IDymDwLDdNgPm5qUDPyumj3GIhIFZzq+WaiQ4KJJX4rmAApge6iYio41OC/fy5ukojJ+ekD6TqLW463FkSO+5nsglw7Lz0OaSPbAMlCS6pL1f+5jxSRJGS08I6tHb5iYZLve0yL4=",
        "OSI_OUR_PRIVATE_KEY_PASSWORD": ""
    }

    def __init__(self, channel):
        config_map = {
            "lxj": self.lxj_config,
            "wacai": self.wacai_config,
            "goc": self.goc_config
        }
        self.config = config_map.get(channel, self.lxj_config)

    def get_random_aes_key(self):
        """ 生成一个随机 16 字节的 AES 密钥 """
        return ''.join(
            secrets.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(16))

    def md5_hash(self, content):
        """计算 MD5 哈希值"""
        return hashlib.md5(content.encode()).hexdigest()

    def pad_pkcs7(self, data):
        """PKCS7 填充，使数据长度变为 16 的倍数"""
        pad_len = 16 - (len(data) % 16)
        return data + chr(pad_len) * pad_len

    def aes_cbc_encrypt(self, secret_str, input_str):
        """ AES-128 CBC NoPadding 加密并返回 Base64 编码 """
        if len(secret_str) != 16:
            raise ValueError("AES 密钥长度必须是 16 字节（AES-128）")

        secret_key_bytes = secret_str.encode("utf-8")
        padded_input = self.pad_pkcs7(input_str)  # IV = Key，符合 Java 代码逻辑
        # 确保 input_str 长度是 16 的倍数，否则 NoPadding 会报错
        cipher = AES.new(secret_key_bytes, AES.MODE_CBC, secret_key_bytes)
        encrypted_bytes = cipher.encrypt(padded_input.encode("utf-8"))

        return base64.b64encode(encrypted_bytes).decode("utf-8")

    def aes_cbc_decrypt(self, secret_str, encrypted_base64):
        """AES CBC NoPadding 解密"""
        if len(secret_str) != 16:
            raise ValueError("AES 密钥长度必须是 16 字节（AES-128）")

        secret_key_bytes = secret_str.encode("utf-8")
        iv_bytes = secret_key_bytes  # Java 代码 IV = Key

        encrypted_bytes = base64.b64decode(encrypted_base64)  # Base64 解码
        cipher = AES.new(secret_key_bytes, AES.MODE_CBC, iv_bytes)
        decrypted_bytes = cipher.decrypt(encrypted_bytes)  # 解密

        return decrypted_bytes.rstrip(b"\x00").decode("utf-8")  # 去除填充后转换为字符串

    def rsa_encrypt(self, public_key_str, data):
        """RSA 公钥加密"""
        try:
            # 确保公钥格式正确
            if not public_key_str.startswith("-----BEGIN PUBLIC KEY-----"):
                public_key_str = f"-----BEGIN PUBLIC KEY-----\n{public_key_str}\n-----END PUBLIC KEY-----"

            public_key = RSA.import_key(public_key_str)
            cipher = PKCS1_v1_5.new(public_key)
            encrypted = cipher.encrypt(data.encode())
            return base64.b64encode(encrypted).decode()
        except ValueError as e:
            print(f"RSA 公钥加密失败: {e}")
            raise

    def rsa_decrypt(self, private_key_str, encrypted_data):
        """RSA 私钥解密"""
        try:

            """解析 Base64 编码的 PKCS#8 RSA 私钥"""
            key_bytes = base64.b64decode(private_key_str)
            rsa_private_key = RSA.import_key(key_bytes)  # 获取 RSA 私钥
            cipher = PKCS1_v1_5.new(rsa_private_key)
            decrypted = cipher.decrypt(base64.b64decode(encrypted_data), None)

            if decrypted is None:
                raise ValueError("RSA 解密失败")

            return decrypted.decode()
        except ValueError as e:
            print(f"RSA 私钥解密失败: {e}")
