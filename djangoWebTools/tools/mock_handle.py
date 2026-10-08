#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
操作easymock配置
"""
import json
from functools import wraps

import requests

from config import db_conn, nacos_config

#
# class EasyMockRequest(object):
#     # 调用easymock接口
#     def __init__(self, ):
#         self.mock_url = nacos_config.get("EASYMOCK").get("URL")
#         self.headers = self.get_config_headers()
#
#     def _post(self, path, data=None):
#         """
#         post请求
#         """
#         url = self.mock_url + path
#         data = requests.post(url, json=data, headers=self.headers, verify=False)
#         return data
#
#     @staticmethod
#     def check_token(func):
#         # 登录检查
#         @wraps(func)
#         def wrapper(self, *args, **kwargs):
#             # 检查token是否有效
#             if not self.check_login_status():
#                 # 触发登录流程重新获取token
#                 res = self.login()
#                 if res.status_code != 200:
#                     return False
#                 update_res = self.update_token(token=res.json().get('data', None).get('token', None))
#                 if not update_res:
#                     return False
#
#             return func(self, *args, **kwargs)
#
#         return wrapper
#
#     @staticmethod
#     def get_config_headers(env='SIT'):
#         """
#         获取easymock请求头
#         :return:
#         """
#         sql = "SELECT `value1` FROM `web_tools`.`sys_param` WHERE `code` = 'easymock_token'"
#         res = db_conn(env).select_one(sql)
#         if res.get('data', None).get('value1', None):
#             token = res.get('data', None).get('value1', None)
#         else:
#             token = ''
#         return {"Authorization": f"Bearer {token}"}
#
#     def login(self, name='admin', password='Qcpa7HV2vaz1zoJW'):
#         """
#         登录easymock
#         :return:
#         """
#         url = self.mock_url + '/api/u/login'
#         data = {
#             'name':     name,
#             'password': password,
#         }
#         return requests.post(url, data=data)
#
#     def check_login_status(self):
#         """
#         通过调用分组接口检查登录状态
#         :return:
#         """
#         url = self.mock_url + '/api/group'
#         res = requests.get(url, headers=self.headers)
#         if res.status_code == 200:
#             return True
#         else:
#             return False
#
#     def update_token(self, token=None):
#         # 更新 easymock token 到类属性及数据库
#         self.headers = {"Authorization": f"Bearer {token}"}
#         sql = "UPDATE `web_tools`.`sys_param` SET `value1` = '{}' WHERE `code` = 'easymock_token'".format(token)
#         res = db_conn("SIT").exec_one(sql)
#         if res["code"] == 0:
#             return True
#         else:
#             return False
#
#     def get_project_list(self, group_id='64b50b25cce8c8002247db55',):
#         """
#         获取项目列表
#         :return:
#         """
#         url = self.mock_url + '/api/project'
#         params = {
#             'group': group_id,
#         }
#         requests_res = requests.get(url, params=params, headers=self.headers, verify=False)
#         return requests_res
#
#     @check_token
#     def get_mock_list(self, project_id='64b50b37cce8c8002247db57', keyword='', page_index='',
#                       page_size=''):
#         """
#         获取mock列表
#         :return:
#         """
#         params = {
#             'page_size':  page_size,
#             'page_index': page_index,
#             'keywords':   keyword,
#             'project_id': project_id,
#         }
#
#         url = self.mock_url + '/api/mock'
#         requests_res = requests.get(url, params=params, headers=self.headers, verify=False)
#         return requests_res
#
#     @check_token
#     def get_accurate_mock_data(self, project_id, keyword):
#         """
#         获取mock数据
#         :param project_id:
#         :param keyword:
#         :return:
#         """
#         easymock_data_list = self.get_mock_list(project_id=project_id, keyword=keyword)
#         # print(f"get_mock_list::{easymock_data_list}")
#         mock_list = easymock_data_list.json().get('data', None).get('mocks', None)
#         if mock_list is None:
#             return None
#
#         # 遍历 mocks 列表
#         easymock_data = None
#         # print(f"get_accurate_mock_data::mock_list::{mock_list}")
#         for mock in mock_list:
#             # 检查 URL 是否完全匹配
#             if mock['url'] == keyword:
#                 # print(f"get_accurate_mock_data::mock['url']::{type(mock), mock}")
#                 easymock_data = mock.get('mode', None)
#             else:
#                 pass
#         # print(f"get_accurate_mock_data::{easymock_data}")
#         return easymock_data
#
#     @check_token
#     def post_easymock_update(self, url, mode, method, description, mock_id):
#         """
#         更新mock
#         :param url: 被mock接口完整路径，如"/io.kyoto.support.goa.tpfund.shengbei.ShengBeiCreditFacade/hitLibrary"
#         :param mode: mock模板数据
#         :param method: 请求类型，如：post
#         :param description: 接口描述
#         :param mock_id: easymock分配给该接口的id
#         :return:
#         """
#         data = {
#             'url':         url,
#             'mode':        json.dumps(mode, ensure_ascii=False),
#             'method':      method,
#             'description': description,
#             'id':          mock_id,
#         }
#         return requests.post(self.mock_url + '/api/mock/update', json=data, headers=self.headers, verify=False)
#
#
# easymock = EasyMockRequest()


class Singleton(type):
    """
    单例模式
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MockClient(metaclass=Singleton):
    # mock操作
    # def __init__(self, ):
    #     ...

    def init_params(self, env='SIT'):
        project_list = self.get_project_option_by_env(env)

    @staticmethod
    def get_project_option_by_env(env):
        # 获取 web_tools 数据库中 easymock_project 表数据
        sql = f"SELECT * FROM `web_tools`.`easymock_project` WHERE `env` = '{env}'"
        res = db_conn(env).select_one(sql)
        if res.get('project_id'):
            return res.get('project_id')
        return res

    @staticmethod
    def get_group_option_by_project_id(env, project_id):
        # 获取 web_tools 数据库，对应 group 的数据（项目所对应的 easymock_interface 中的 group ）
        sql = f"""
            SELECT DISTINCT `group` FROM `web_tools`.`easymock_interface` 
            WHERE `project_id` = '{project_id}'"""
        # print(f"get_group_option::{sql}")
        res = db_conn(env).get_all(sql)
        # print(f"get_group_option_by_project_id::{len(res)}{res}")

        return res

    @staticmethod
    def get_method_option_by_group(env, group):
        sql = f"""
            SELECT em.method_id, concat(ei.interface_class, '/', em.method) as method, em.description, em.url 
            FROM `web_tools`.`easymock_interface` ei 
            INNER JOIN `web_tools`.`easymock_method` em ON ei.interface_class = em.interface_class
            WHERE ei.`group` = '{group}' """
        res = db_conn(env).get_all(sql)
        # print(f"get_method_option_by_group::{res}")
        return res

    @staticmethod
    def insert_mock_interface(interface_class, project_id, sys, group, description, env="SIT"):
        # 插入 interface 接口数据
        sql = f"""
            INSERT INTO `web_tools`.`easymock_interface` (`interface_class`, `project_id`, `sys`, `group`, `description`) 
            VALUES (%s, %s, %s, %s, %s)"""
        # print(f"insert_mock_data::{sql}")
        params = (interface_class, project_id, sys, group, description)
        res = db_conn(env).exec_one(sql, params)
        return res

    @staticmethod
    def insert_mock_method(method_id, interface_class, method_type, method, url, description, env="SIT"):
        # 插入 mock 方法数据
        sql = f"""
            INSERT INTO `web_tools`.`easymock_method` (`method_id`, `interface_class`, `type`, `method`, `url`, `description`) 
            VALUES (%s, %s, %s, %s, %s, %s)"""
        # print(f"insert_mock_method::{sql}")
        params = (method_id, interface_class, method_type, method, url, description)
        res = db_conn(env).exec_one(sql, params)
        return res

    @staticmethod
    def insert_mock_data(method_id, description, mock_data, env="SIT"):
        # 插入 mock 模板数据
        sql = f"""
            INSERT INTO `web_tools`.`easymock_data` (`method_id`, `mock_data`, `description`) 
            VALUES (%s, %s, %s)"""
        # print(f"insert_mock_data::{sql}")
        params = (method_id, mock_data, description)
        res = db_conn(env).exec_one(sql, params)
        return res

    @staticmethod
    def get_mock_data_by_method(env, method_id):
        # 查询指定接口id的 mock 模板数据
        sql = f"""
            SELECT data_id, mock_data, description 
            FROM `web_tools`.`easymock_data` 
            WHERE `method_id` = '{method_id}'"""
        res = db_conn(env).get_all(sql)
        # print(f"get_mock_data_by_method::{res}")
        return res

    @staticmethod
    def insert_remark(method_id, title, remark_data, env="SIT"):
        # 查询指定 data_id 的 mock 模板数据
        sql = f"""
            INSERT INTO `web_tools`.`easymock_method_remark` (`title`, `method_id`, `remark_data`) 
            VALUES ( %s, %s, %s);"""

        params = (title, method_id, remark_data)
        res = db_conn(env).exec_one(sql, params)
        return res

    @staticmethod
    def get_remark_by_method(method_id, env="SIT"):
        # 查询指定接口id的 mock 模板数据
        sql = f"""
            SELECT remark_id, title, method_id, remark_data 
            FROM `web_tools`.`easymock_method_remark` 
            WHERE `method_id` = '{method_id}'"""
        res = db_conn(env).get_all(sql)
        # print(f"get_remark_by_method::{res}")
        return res

    @staticmethod
    def get_method_info_by_id(method_id, env="SIT", ):
        # 查询指定接口id的 mock 模板数据
        sql = f"""
            SELECT `type`, `url`, `interface_class`, `method`, `description` 
            FROM `web_tools`.`easymock_method` 
            WHERE `method_id` = '{method_id}' """
        res = db_conn(env).get_all(sql)
        # print(f"get_method_info_by_id::{res}")
        return res

    @staticmethod
    def get_mock_data_by_id(data_id, env="SIT", ):
        # 查询指定接口id的 mock 模板数据
        sql = f"""
            SELECT `method_id`, `mock_data`, `description` 
            FROM `web_tools`.`easymock_data` 
            WHERE `data_id` = '{data_id}' """
        res = db_conn(env).get_all(sql)
        # print(f"get_mock_data_by_id::{res}")
        return res

    @staticmethod
    def get_scene_by_group(group, exec_env="SIT"):
        # 查询指定 group 的对应场景配置
        sql = f"""
            SELECT `scene_id`, `title`, `group`, `data_id_list`, `description` 
            FROM `web_tools`.`easymock_scene` WHERE `group` = '{group}'"""
        res = db_conn(exec_env).get_all(sql)
        # print(f"get_scene_by_group::{res}")
        return res

    @staticmethod
    def insert_scene(group, title, data_id_list, description, exec_env="SIT"):
        # 新增指定 group 的对应场景配置
        sql = f"""
            INSERT INTO `web_tools`.`easymock_scene` (`group`, `title`, `data_id_list`, `description`) 
            VALUES (%s, %s, %s, %s)"""
        params = (group, title, data_id_list, description)
        res = db_conn(exec_env).exec_one(sql, params)
        return res
    #
    # @staticmethod
    # def update_scene(scene_id, title=None, data_id_list=None, description=None, group=None, exec_env="SIT"):
    #     # 修改场景配置
    #     sql = "UPDATE `web_tools`.`easymock_scene` SET "
    #     params = []
    #     fields = []
    #
    #     if title is not None:
    #         fields.append("`title` = %s")
    #         params.append(title)
    #
    #     if data_id_list is not None:
    #         fields.append("`data_id_list` = %s")
    #         params.append(data_id_list)
    #
    #     if description is not None:
    #         fields.append("`description` = %s")
    #         params.append(description)
    #
    #     if group is not None:
    #         fields.append("`group` = %s")
    #         params.append(group)
    #
    #     sql += ", ".join(fields)
    #
    #     # Add the WHERE clause
    #     sql += " WHERE `scene_id` = %s"
    #     params.append(scene_id)
    #     # print(f"update_scene::{sql}, {params}")
    #
    #     res = db_conn(exec_env).exec_one(sql, params)
    #     return res

    # def query_config(self, exec_env, option_type, option_value):
    #     # 查询 mock 各项配置
    #     result = {"code": "0", "data": None, "res_type": None}
    #     if option_type == "init":
    #         # 初始化配置获取
    #         ...
    #
    #     if option_type == "env":
    #         result["data"] = self.get_project_option_by_env(exec_env)
    #
    #     elif option_type == "project":
    #         result["res_type"] = "group"
    #         result["data"] = self.get_group_option_by_project_id(exec_env, option_value)
    #
    #     elif option_type == "group":
    #         result["res_type"] = "method"
    #         result["data"] = self.get_method_option_by_group(exec_env, option_value)
    #
    #     elif option_type == "method":
    #         result["res_type"] = "mock_temp_data"
    #         result["data"] = self.get_mock_data_by_method(exec_env, option_value)
    #         result["remark"] = self.get_remark_by_method(option_value)
    #
    #     elif option_type == "easymock":
    #         result["res_type"] = "easymock_data"
    #         project_id = option_value.get('projectID')
    #         method_url = option_value.get('methodURL')
    #         easymock_data = EasyMockRequest().get_accurate_mock_data(project_id=project_id, keyword=method_url)
    #         # print(f"easymock_data::{easymock_data}")
    #         result["data"] = easymock_data
    #         # print(f"query_config::{result}")
    #     elif option_type == "scene":
    #         result["res_type"] = "scene_list"
    #         group = option_value.get('groupID')
    #         result["data"] = self.get_scene_by_group(group)
    #     return result
    #
    # @classmethod
    # def push_easymock_conf(cls, mock_data_id):
    #     # 更新 mock_data_id 对应的 mock 模板到 easymock
    #     mock_data_info = cls.get_mock_data_by_id(data_id=mock_data_id)[0]
    #     method_id = mock_data_info.get('method_id')
    #     mock_data = json.loads(mock_data_info.get('mock_data'))
    #     # mock_data = mock_data_info.get('mock_data')
    #     # description = mock_data_info.get('description')
    #
    #     method_info = cls.get_method_info_by_id(method_id=method_id)[0]
    #     url = method_info.get('url')
    #     method_type = method_info.get('type')
    #     description = method_info.get('description')
    #     update_res = easymock.post_easymock_update(url=url, mode=mock_data, method=method_type, description=description,
    #                                                mock_id=method_id)
    #     # print(f"update_mock::update_easymock::{update_res.json()}")
    #     return update_res.json()

    def execute_scene(self, data_id_list: str):
        # 执行场景配置
        res_list = []
        # print(f"execute_scene::{type(data_id_list), data_id_list}")
        data_id_list = data_id_list.split(",")
        if len(data_id_list) > 0:
            for data_id in data_id_list:
                res = self.push_easymock_conf(mock_data_id=data_id)
                # print(f"execute_scene::update_mock_conf::{res}")
                if res.get("code") == 200:
                    res_list.append(f"模板 {data_id} 配置成功")
                else:
                    res_list.append(f"模板 {data_id} 配置失败")
        else:
            res_list.append("场景列表为空")

        return {"code": "0", "res_list": res_list}

    # @classmethod
    # def refresh_mock_data_with_easymock(cls):
    #     # 拉取easymock当前配置，更新数据库mock数据
    #     refresh_res = {
    #         "code": "0",
    #         "msg": "更新接口配置如下",
    #         "interface_res": [],
    #         "method_res": [],
    #         "data_res": []
    #     }
    #
    #     project_res = easymock.get_project_list()
    #     project_list = project_res.json().get('data', None)
    #
    #     method_id_sql = """SELECT method_id FROM `web_tools`.`easymock_method` """
    #     method_id_list = db_conn(env="SIT").get_all(method_id_sql)
    #     method_id_list = [item.get('method_id') for item in method_id_list]
    #
    #     for project in project_list:
    #         print(f"refresh::project::{project}")
    #         project_id = project.get('_id')
    #         sys = project.get('name')
    #         mock_list_res = easymock.get_mock_list(project_id=project_id)
    #         mocks = mock_list_res.json().get('data', None).get('mocks', None)
    #         for mock_info in mocks:
    #             if mock_info.get('_id') not in method_id_list:
    #                 point_split = mock_info["url"].split(".")
    #                 if len(point_split) < 3:
    #                     print(f"mock_info<3::{mock_info}")
    #                     continue
    #                 group = point_split[-2]
    #                 interface_class = point_split[-1].split("/")[0]
    #                 method = mock_info["url"].split("/")[-1]
    #                 insert_method_res = cls.insert_mock_method(
    #                     method_id=mock_info.get('_id'),
    #                     interface_class=interface_class,
    #                     method_type=mock_info.get('method'),
    #                     method=method,
    #                     url=mock_info.get('url'),
    #                     description=mock_info.get('description'))
    #                 if insert_method_res.get("code") == "0":
    #                     refresh_res["method_res"].append(mock_info.get('_id'))
    #                 else:
    #                     refresh_res["interface_res"].append(f"执行interface插入语句失败::{insert_method_res}")
    #
    #                 insert_mock_data_res = cls.insert_mock_data(
    #                     method_id=mock_info.get('_id'),
    #                     description="初始模板",
    #                     mock_data=mock_info.get('mode'))
    #                 if insert_mock_data_res.get("code") == "0":
    #                     refresh_res["data_res"].append(mock_info.get('_id'))
    #                 else:
    #                     refresh_res["method_res"].append(f"执行data插入语句失败::{insert_mock_data_res}")
    #
    #                 interface_class_sql = """SELECT `interface_class` FROM `web_tools`.`easymock_interface` """
    #                 interface_class_list = db_conn(env="SIT").get_all(interface_class_sql)
    #                 interface_class_list = [item.get('interface_class') for item in interface_class_list]
    #                 if interface_class not in interface_class_list:
    #                     insert_face_res = cls.insert_mock_interface(interface_class=interface_class, project_id=project_id,
    #                                                sys=sys, group=group, description=mock_info.get('description'))
    #                     if insert_face_res.get("code") == "0":
    #                         refresh_res["interface_res"].append(mock_info.get('_id'))
    #                     else:
    #                         refresh_res["interface_res"].append(f"执行interface插入语句失败::{insert_face_res}")
    #
    #                 else:
    #                     refresh_res["interface_res"].append("接口已存在")
    #
    #     return refresh_res
    #


def mock_base64():
    return "iVBORw0KGgoAAAANSUhEUgAAAjkAAAFBCAYAAACVcr5cAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAFiUAABYlAUlSJPAAAAWZSURBVHhe7dYxEQAgEMCwB/+egQEVvWSpha7zDABAzP4FAEgxOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABJJgcASDI5AECSyQEAkkwOAJBkcgCAJJMDACSZHAAgyeQAAEkmBwBIMjkAQJLJAQCSTA4AkGRyAIAkkwMAJJkcACDJ5AAASSYHAEgyOQBAkskBAJJMDgCQZHIAgCSTAwAkmRwAIMnkAABBMxeXJgZ+f2mLWgAAAABJRU5ErkJggg=="


# if __name__ == '__main__':
    # mock_handle = EasyMockRequest()
    # print("http.client::\n", mock_handle.get_mock_list())
    # print(mock_handle.update_easymock(
    #     url='/io.kyoto.support.goa.tpfund.shengbei.ShengBeiCreditFacade/hitLibrary',
    #     mode={"code": "0001", "existing": True},
    #     method='post', description='省呗准入',
    #     mock_id='661fa3714d1fa30022de9407'))
    # res = get_easymock_header()
    # print(res)

    # mock_client = MockClient().get_method_info_by_id("66792f757e1379001edd0211")

    # ...
    # print(f"refresh_mock_data_with_easymock::{MockClient().refresh_mock_data_with_easymock()}")
