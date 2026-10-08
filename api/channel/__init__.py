#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time
import requests

from config import get_urls
from utils.logger_util import web_logger


def hub_request(env, channel_id, method, biz_data, ):
    # hub通用接口 env=SIT/DEV
    json_data = {
        "timestamp":      time.time(),
        "channelId":      channel_id,
        "method":         method,
        "bizData":        biz_data
    }
    url = get_urls(env).get("HUB_PATH")
    print(f"hub_request::request::url::{url},data::{json_data}")
    responds = requests.post(url, json=json_data)
    web_logger.info(f"hub_request::request::{json_data},\nresponds::{responds.json()}")
    return responds


# if __name__ == '__main__':
#     res = hub_request("DEV", "HuoLaLaApiRequest", "HUB_HUOLALA", "check", {
#   "userName": "廉廑",
#   "md5Phone": "7ed939943ca608f9487d3ce3ee954125",
#   "md5IdNo": "b06c4dcf5eb346d51db07148c681155f",
#   "md5PhoneAndIdNo": "89811bad53075b30217d7aab7d8513d8",
#   "partnerId": "eeebcd8e-9ed9-422a-aeac-61c66f4a2bf9",
#   "openId": "fb51fde4-af70-4613-91b9-bee794c1169a"
# })
#     print(f"hub_request::res::{res.json()}")
