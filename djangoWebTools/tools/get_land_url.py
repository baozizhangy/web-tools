from config import db_conn
import json
import requests

from utils.logger_util import web_logger


def get_land_urls(env, channel_id):
    ch_source_sql = f"SELECT channel_uid FROM lps.ch_source WHERE lps.ch_source.channel_id='{channel_id}' LIMIT 1"
    ch_source_res = db_conn(env).get_all(ch_source_sql)

    if not ch_source_res:
        return {
            "code":1,
            "msg":"未找到channel_uid"
        }

    channel_uid = ch_source_res[0]['channel_uid']
    base_url = "https://test2.xurongwl.com" if env == 'dev' else "https://test3.xurongwl.com"
    url = f"{base_url}/clg/bcs/test/hub/h5/url?channelUid={channel_uid}"
    web_logger.info(f"获取着陆页的urls: {url}")

    try:
        response = requests.get(url=url,verify=True)  # Set verify=True for security
        response.raise_for_status()  # Raise HTTPError for bad responses
        result = response.json()

        if result.get('code') != '0':
            return {
                "code":1,
                "msg":"接口返回失败，传入channel_id不正确"
            }

        return {
            "code":0,
            "msg":f"获取{channel_id}的url成功",
            "data":result.get('data')
        }

    except requests.exceptions.RequestException as e:
        web_logger.error(f"接口调用失败，错误信息: {str(e)}")
        return {
            "code":"999",
            "msg":"接口调用失败，错误信息",
            "error":str(e)
        }

