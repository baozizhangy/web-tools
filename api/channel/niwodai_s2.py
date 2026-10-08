#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from api.channel.niwodai import NiWoDai, NiWoDaiMethodsEnum


class NiWoDaiS2(NiWoDai):
    # 你我贷S1
    def __init__(self, ):
        super().__init__(channel_id="HUB_NIWODAI_S2", channel_name="你我贷S2",
                         channel_method_enum=NiWoDaiMethodsEnum, channel_uid="21096", py_code="niwodai_s2")
