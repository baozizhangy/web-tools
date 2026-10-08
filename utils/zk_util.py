#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from dubbo.client import DubboClient, ZkRegister


class ZkUtil(object):
    # python3-dubbo 模块实现的 zk 调用 dubbo 服务
    def __init__(self, _zk_ip='106.15.234.139:32181'):
        # 需注释源码中 revision 字段，否则会报错
        self.zk = ZkRegister(_zk_ip)

    def client(self, interface):
        return DubboClient(interface, zk_register=self.zk, version=None)

    def call(self, interface, method, *args, ):
        client = self.client(interface)
        # print(f"Calling {method} {args}")
        return client.call(method, (*args,))


if __name__ == '__main__':
    zk_ip = '106.15.234.139:32181'
    biz_no = "202404090000000004"
    zk = ZkUtil(zk_ip)
    res = zk.call('io.kyoto.risk.apv.dist.DistApplyFacade', 'queryApplyInfo', biz_no)
    print(res)
