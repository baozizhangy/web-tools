#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from config import db_conn
from utils.logger_util import web_logger


@csrf_exempt
def get_navigation_config(env='BM_SIT'):
    sql = "SELECT title, type, url, remark FROM `web_tools`.`bookmark_data` "
    res = db_conn('BM_SIT').get_all(sql)
    return JsonResponse(res, safe=False, charset='utf-8')

@csrf_exempt
def create_navigation_config(request):
    # 入参为 {type: "outer", title: "test", url: "http", remark: "test111"} 插入到`web_tools`.`bookmark_data`
    data = json.loads(request.body)
    type = data.get('type')
    title = data.get('title')
    url = data.get('url')
    remark = data.get('remark')
    if not type or not title or not url:
        return JsonResponse({"error": "type, title, url不能为空"}, status=400)
    sql = "INSERT INTO `web_tools`.`bookmark_data` (type, title, url, remark) VALUES ('%s', '%s', '%s', '%s')" % (
        type, title, url, remark)
    res = db_conn('BM_SIT').exec_one(sql)
    print(res)
    return JsonResponse({"success": "ok"}, status=200)
#

# if __name__ == '__main__':
#     print(get_navigation_config())
