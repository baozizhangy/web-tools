#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import jwt

salt = 'iv%x1fo9l7_u9bf_u!9#g#m*)*=ej@bek5)(@u3kh*72+unjv='


def validate_token(token):
    """
    校验token有效性
    :param token:加密token
    :return: 状态
    """

    # 定义返回相应字典
    result = {'status': False, 'data': None, 'error': None}
    try:
        verified_payload = jwt.decode(token, salt, algorithm='HS256', options={"verify_signature": False})
        result['status'] = True
        result['data'] = verified_payload
    except jwt.ExpiredSignatureError:
        result['error'] = 'token已失效'
    except jwt.DecodeError as err:
        result['error'] = 'token认证失败'
    except jwt.InvalidTokenError:
        result['error'] = '非法的token'
    return result


if __name__ == '__main__':
    res = validate_token("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHBfb3MiOiJvdGhlciIsImFwcF92ZXJzaW9uIjoiNy45LjEiLCJhcHBpZCI6OCwiYnJhbmNoIjoiY29tLmxpZ2h0cGFsbS5mZW5xaWEiLCJjaGFubmVsIjoiamVua2luc19jaGFubmVsIiwiZGlkIjo4LCJkdWlkIjoiWExsdm9ZcjNkVHNEQUNzNWZSM3ZMSE1FIiwiZ3JvdXAiOiJkZWZhdWx0IiwiaW5pdCI6MTY5MzI4NzU5MSwibGFzdCI6NjI4LCJvcyI6Im90aGVyIiwicGQiOiJmZW5xaSIsInBpZCI6ImZlbnFpIiwicXVlcnlfb3MiOiJvdGhlciIsInF1ZXJ5X3ZlcnNpb24iOiI2LjcuNSIsInN0cyI6MTY5MzI4NzU5MSwidGFncyI6W10sInZlcnNpb24iOiI3LjkuMSIsInZpc2l0cyI6MiwieHJfc2lkIjoiU1dwWk1GcFhVVFJPUjBVelRXMVJkMDR5U1hsYWFrcHJUa2RaTkU1SFNUVlpVMGs2TVhGaGNsTkNPa3hYY1d4ck1UbDFPWGhCYXpreGIwNXRSa1J6U1RoVFVFVnJWUSIsInVzZXJfaWQiOjg5LCJudW1iZXIiOiIxMjM0NTI5NTAyMjciLCJjaWQiOiJqZW5raW5zX2NoYW5uZWwiLCJwZF9jcmVhdGVkIjp0cnVlLCJicmFuY2hfY3JlYXRlZCI6dHJ1ZSwidHMiOjE2OTMyODc1OTEsInBkX2N0cyI6MTY5MzI4NzU5MSwiY3RzIjoxNjkzMjg3NTkxLCJicmFuY2hfbHRzIjowLCJsYXN0MiI6NDEsInVzZXJfbm8iOiJVUjA2NDE4NjE0NTIxNDQzMzY4OTYiLCJwcmV2aWV3X3NpZCI6IjY0ZWQ4NGE3MmQwN2IyZjJkNGY4NGI5YSJ9.E1EFyJnO_yUxmxirUCKe5qA-fPgpsxFELdFiYgDEW4c")
    print(f"res::{type(res)},{res}")