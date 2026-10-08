#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import redis
from redis.exceptions import RedisError

from utils.logger_util import web_logger


class RedisDB:
    def __init__(self, host, port, password=None, db=0, decode_responses=True):
        self.host = host
        self.port = port
        self.password = password
        self.db = db
        self.decode_responses = decode_responses
        self.client = redis.Redis(
            host=self.host,
            port=self.port,
            password=self.password,
            db=self.db,
            decode_responses=self.decode_responses
        )

    def get_conn(self):
        return self.client

    def get(self, key):
        try:
            value = self.client.get(key)
            if value is None:
                return {'code': '0', 'message': '查询结果为空', 'data': None}
            return {'code': '0', 'message': '查询成功', 'data': value}
        except RedisError as e:
            web_logger.error(f"Redis get 异常: {e}")
            return {'code': '9999', 'message': 'Redis 查询异常', 'data': str(e)}

    def get_keys(self, pattern='*', count=100):
        try:
            keys = list(self.client.scan_iter(match=pattern, count=count))
            return {'code': '0', 'message': '查询成功', 'data': keys}
        except RedisError as e:
            web_logger.error(f"Redis get_keys 异常: {e}")
            return {'code': '9999', 'message': 'Redis 查询异常', 'data': str(e)}

    def exists(self, key):
        try:
            exists = self.client.exists(key)
            return {'code': '0', 'message': '查询成功', 'data': bool(exists)}
        except RedisError as e:
            web_logger.error(f"Redis exists 异常: {e}")
            return {'code': '9999', 'message': 'Redis 查询异常', 'data': str(e)}

    def delete(self, *keys):
        try:
            if not keys:
                return {'code': '0', 'message': '未传入需要删除的key', 'data': 0}
            deleted_count = self.client.delete(*keys)
            return {'code': '0', 'message': '删除成功', 'data': deleted_count}
        except RedisError as e:
            web_logger.error(f"Redis delete 异常: {e}")
            return {'code': '9999', 'message': 'Redis 删除异常', 'data': str(e)}

    def delete_by_pattern(self, pattern, count=100):
        try:
            keys = list(self.client.scan_iter(match=pattern, count=count))
            if not keys:
                return {'code': '0', 'message': '未查询到需要删除的key', 'data': 0}
            deleted_count = self.client.delete(*keys)
            return {'code': '0', 'message': '删除成功', 'data': deleted_count}
        except RedisError as e:
            web_logger.error(f"Redis delete_by_pattern 异常: {e}")
            return {'code': '9999', 'message': 'Redis 删除异常', 'data': str(e)}

    def hget(self, name, key):
        try:
            value = self.client.hget(name, key)
            if value is None:
                return {'code': '0', 'message': '查询结果为空', 'data': None}
            return {'code': '0', 'message': '查询成功', 'data': value}
        except RedisError as e:
            web_logger.error(f"Redis hget 异常: {e}")
            return {'code': '9999', 'message': 'Redis 查询异常', 'data': str(e)}

    def hdel(self, name, *keys):
        try:
            if not keys:
                return {'code': '0', 'message': '未传入需要删除的hash field', 'data': 0}
            deleted_count = self.client.hdel(name, *keys)
            return {'code': '0', 'message': '删除成功', 'data': deleted_count}
        except RedisError as e:
            web_logger.error(f"Redis hdel 异常: {e}")
            return {'code': '9999', 'message': 'Redis 删除异常', 'data': str(e)}
