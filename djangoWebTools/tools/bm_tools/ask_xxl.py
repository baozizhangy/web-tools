import requests
from utils.logger_util import web_logger
from config import get_xxl_login_urls, get_xxl_trigger_urls


def xxl_job_login(env):
    web_logger.info(f'xxl-job登录中...环境{env}')
    # if env == 'BM_SIT':
    #     login_url = 'http://bm-sit.shangtoutech.com/xxl-job-admin/login'
    # elif env == 'DEV':
    #     login_url = 'http://bm-dev.shangtoutech.com/xxl-job-admin/login'
    # else:
    #     return 'env参数错误'
    if env == 'DEV' or env == 'BM_SIT':
        login_url = get_xxl_login_urls(env)
    else:
        return 'env参数错误'
    login_data = {
        "userName": "admin",
        "password": "npT5kcoVYbw9NU",
        "ifRemember": "on"
    }
    session_xxl = requests.Session()
    # 登录获取cookie
    web_logger.info(f'发送登录请求到 {login_url}，请求数据: {login_data}')
    response = session_xxl.post(login_url, data=login_data)
    web_logger.info(f'登录响应状态码: {response.status_code}')
    web_logger.info(f'登录响应内容: {response.text}')
    cookies = session_xxl.cookies.get_dict()
    web_logger.info(f'获取到的 cookies: {cookies}')
    if 'XXL_JOB_LOGIN_IDENTITY' not in cookies:
        web_logger.error('未找到 XXL_JOB_LOGIN_IDENTITY cookie')
        return '未找到 XXL_JOB_LOGIN_IDENTITY cookie'
    cookie_1 = 'XXL_JOB_LOGIN_IDENTITY=' + cookies['XXL_JOB_LOGIN_IDENTITY']
    # 更新headers,用于触发任务接口调用
    new_headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': cookie_1
    }
    web_logger.info(f'cookie_1:{cookie_1}')
    return new_headers


def xxl_job_trigger(job_id, executor_param=None, env='BM_SIT'):
    # if env == 'BM_SIT':
    #     url = 'http://bm-sit.shangtoutech.com/xxl-job-admin/jobinfo/trigger'
    # elif env == 'DEV':
    #     url = 'http://bm-dev.shangtoutech.com//xxl-job-admin/jobinfo/trigger'
    # else:
    #     return 'env参数错误'
    if env == 'DEV' or env == 'BM_SIT':
        url = get_xxl_trigger_urls(env)
    else:
        return 'env参数错误'
    # 登录成功后更新headers
    headers = xxl_job_login(env)
    data = {
        'id': job_id,
        'executorParam': executor_param,
        'addressList': '',
    }
    # 触发xxl-job脚本
    resource = requests.post(url, headers=headers, data=data).json()
    if resource.get('code') == 200:
        return 'pass'
    else:
        return 'fail'


if __name__ == '__main__':
    print(xxl_job_trigger('123', 'AC0909785396127223808,2024-10-02,2025-01-23', 'BM_SIT'))
