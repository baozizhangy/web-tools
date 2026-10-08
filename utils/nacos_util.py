#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import yaml
from nacos import NacosClient

import re


def remove_comments(json_str):
    # 使用正则表达式删除类似 // 的注释
    json_str = re.sub(r'//.*', '', json_str)
    return json_str


class Nacos:
    def __init__(self, run_env):
        # 根据传入的环境示例话一个nacos对象
        self.env = run_env
        self.name = "nacos"
        self.password = "hxnmg0U9IoPHfdNC"

    def client(self, namespace):
        # nacos客户端
        print(f"连接namespace::{namespace}")
        if self.env == "local":
            nacos_server = 'test.shangtoutech.com:80'  # Nacos服务器地址
            print(f'访问的nacos地址{nacos_server}')
        else:
            nacos_server = 'nacos-headless.kube-public'  # Nacos服务器地址
        return NacosClient(nacos_server, namespace=namespace,
                           username=self.name, password=self.password)

    # def get_testapi_config(self,group='goa-service',data_id='mock.properties'):
    #     try:
    #         # 从 Nacos 客户端获取配置
    #         config_api = self.client(self.env).get_config(data_id=data_id, group=group)
    #
    #         # 正则匹配模式
    #         pattern = re.compile(r'(Xyfv2[a-zA-Z]*Mock)=([^\s]*)')
    #         matches = pattern.findall(config_api)
    #
    #         modified_parts = []
    #         unmodified_parts = []
    #
    #         start = 0
    #         for key,value in matches:
    #             # 找到匹配的开始和结束位置
    #             match_start = config_api.find(f"{key}={value}",start)
    #             # web_logger.info(f"match_start:{key}:{value}")
    #             match_end = match_start + len(f"{key}={value}")
    #             # web_logger.info(f"match_end:{key}:{value}")
    #
    #             # 保存未修改的部分
    #             if start < match_start:
    #                 unmodified_parts.append(config_api[start:match_start])
    #
    #             # 修改匹配的部分
    #             if value == 'N':
    #                 modified_part = f"{key}=Y"
    #             else:
    #                 modified_part = f"{key}=Y"
    #
    #             modified_parts.append(modified_part)
    #             start = match_end
    #
    #         # 保存最后一部分（如果有的话）
    #         if start < len(config_api):
    #             unmodified_parts.append(config_api[start:])
    #
    #         # 将修改后的部分和未修改的部分合并
    #         modified_string = '\n'.join(modified_parts)
    #         unmodified_string = ''.join(unmodified_parts)
    #         # web_logger.info(f"modified_string:{modified_string}")
    #
    #         # 合并修改的部分和未修改的部分
    #         final_result = unmodified_string + '\n' + modified_string
    #         # web_logger.info(f"final_result:{final_result}")
    #         return final_result
    #
    #     except Exception as e:
    #         # 异常处理
    #         print(f"Error: {e}")
    #         return None
    #
    # def update_config(self,group='goa-service',data_id='mock.properties'):
    #     try:
    #         updated_content = self.get_testapi_config(group=group,data_id=data_id)
    #         if updated_content is None:
    #             return {"No content to update."}
    #
    #         client = self.client(self.env)
    #         success = client.publish_config(data_id=data_id,group=group,content=updated_content)
    #
    #         if success:
    #             return {"Configuration updated_goa successfully."}
    #         else:
    #             return {"Failed to update configuration."}
    #
    #     except Exception as e:
    #         print(f"Error updating goa_configuration: {e}")

    # def get_tds_config(self,group='tds-service',data_id='flowPolicyRuleMock.json'):
    #     get_tds_config = self.client(self.env).get_config(data_id=data_id, group=group)
    #     get_tds_config_data_json = json.dumps(get_tds_config,indent=4,ensure_ascii=False)
    #     return get_tds_config_data_json

    def get_css_config(self, group='css', data_id='application.properties'):
        get_css_config = self.client(self.env).get_config(data_id=data_id, group=group)
        # 使用正则表达式提取 product_list 中的数据
        match = re.search(r'feedback\.page\.product_list=\[(.*?)\]', get_css_config)
        if match:
            product_list_str = match.group(1)  # 获取括号中的内容
            # 将字符串转换为列表
            product_list = [item.strip().strip('"') for item in product_list_str.split(",")]
        return product_list


#
#
# def update_tds_config(client, group='tds-service',data_id='flowPolicyRuleMock.json',user_no=None,fund_code=None):
#     try:
#         # 获取当前配置
#         tds_config = client.get_config(data_id=data_id, group=group)
#         # web_logger.info(f"Received tds_config before update: {tds_config}:")
#         tds_config = remove_comments(tds_config)
#         # web_logger.info(f"Received tds_config after: {tds_config}")
#
#         # 检查 tds_config 的类型
#         if isinstance(tds_config,str):
#             web_logger.info(f"Attempting to parse JSON from: {tds_config}")
#             try:
#                 tds_config = json.loads(tds_config)
#             except json.JSONDecodeError:
#                 raise ValueError("Configuration data is a string but cannot be parsed as JSON.")
#
#         if not isinstance(tds_config,dict):
#             raise ValueError("Current configuration is not in dictionary format.")
#
#         # 处理 fund_code 为列表
#         fund_code_list = fund_code if isinstance(fund_code,list) else ([fund_code] if fund_code is not None else [])
#
#         web_logger.info(f"fund_code_list---1:{fund_code_list}")
#
#         new_tds_data = {
#             user_no:{
#                 "mockSwitch":"Y",
#                 "fundCodeList":fund_code_list
#             }
#         }
#
#         if user_no in tds_config:
#             return {"user_no存在,不做更新操作"}
#
#         # 更新配置
#         tds_config.update(new_tds_data)
#
#         # 将更新后的配置转换为 JSON 字符串
#         config_json = json.dumps(tds_config,indent=4,ensure_ascii=False)
#
#         # 发布配置
#         success = client.publish_config(data_id=data_id, group=group, content=config_json)
#         if success:
#             return {"Configuration updated_tds successfully."}
#         else:
#             return {"Failed to update_tds configuration."}
#     except Exception as e:
#         web_logger.error(f"Error updating tds_configuration: {e}")
#         return {"Error occurred"}

if __name__ == '__main__':
    nacos_conn = Nacos('local')
    run_client = nacos_conn.client('local')
    nacos_config = yaml.safe_load(run_client.get_config(group='auto-test', data_id='application.properties'))
    print(nacos_config)
