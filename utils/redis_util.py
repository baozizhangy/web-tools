#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import redis

class RedisUtil:
    def __init__(self, host='localhost', port=6379, password=None, db=0, ):
        self.r = redis.Redis(host=host, port=port, password=password, db=db)

    def set_value(self, key, value, ex=None):
        """
        设置键值对，可以指定过期时间（单位：秒）。
        """
        return self.r.set(key, value, ex=ex)

    def get_value(self, key):
        """
        获取键对应的值。
        """
        return self.r.get(key)

    def delete_key(self, key):
        """
        删除指定键。
        """
        return self.r.delete(key)

    def set_hash_value(self, hash_key, field, value):
        """
        设置哈希表中的键值对。
        """
        return self.r.hset(hash_key, field, value)

    def get_hash_value(self, hash_key, field):
        """
        获取哈希表中指定键的值。
        """
        return self.r.hget(hash_key, field)

    def delete_hash_field(self, hash_key, field):
        """
        删除哈希表中指定的字段。
        """
        return self.r.hdel(hash_key, field)


if __name__ == '__main__':
    r = redis.Redis(host='106.15.234.139', port=36379, password='8NXrzAMf')
    info = r.info()
    print(info)
    version = info.get('redis_version')
    print(f"Redis 版本：{version}")