#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from api.channel.niwodai import NiWoDai, NiWoDaiMethodsEnum


class NiWoDaiS1(NiWoDai):
    # 你我贷S1
    def __init__(self, ):
        super().__init__(channel_id="HUB_NIWODAI_S1", channel_name="你我贷S1",
                 channel_method_enum=NiWoDaiMethodsEnum, channel_uid="20590", py_code="niwodai_s1")
