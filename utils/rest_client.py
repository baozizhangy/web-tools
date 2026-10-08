import requests
import json as complex_json
from typing import Dict, Any
from utils.logger_util import web_logger


def log_request(url: str, method: str, headers: Dict[str, str], params: Dict[str, Any],
                data: Any, json: Any, files: Dict[str, Any], cookies: Dict[str, str],
                response):
    """
    log_request 方法用于记录 HTTP 请求的详细   信息，包括请求 URL、HTTP 方法、请求头部、查询参数、请求体数据、请求体 JSON、
    文件上传和 cookies 等信息
    """
    # logger.info(f"\n\n\n\nRequest : \n{url}")
    web_logger.info(f"Request Method URL: \n{method} {url}")
    # logger.info(f"Request Headers: \n{complex_json.dumps(headers, indent=4, ensure_ascii=False)}")
    # logger.info(f"Request Params: \n{complex_json.dumps(params, indent=4, ensure_ascii=False)}")
    # logger.info(f"Request Data: \n{complex_json.dumps(data, indent=4, ensure_ascii=False)}")
    web_logger.info(f"Request JSON: \n{complex_json.dumps(json, indent=4, ensure_ascii=False)}")
    # logger.info(f"Request Files: \n{files}")
    # logger.info(f"Request Cookies: \n{complex_json.dumps(cookies, indent=4, ensure_ascii=False)}")
    web_logger.info(f"Response Data: \n{response.text}\n\n")


class RestClient:
    """
    RestClient 类用于发送 RESTful API 请求，主要功能是通过 requests 库发送 HTTP 请求，并记录请求的详细信息。
    """
    def __init__(self, api_root_url: str, session: requests.Session = None, headers: Dict[str, str] = None) -> None:
        self.api_root_url = api_root_url
        # self.session = session if session is not None else requests.Session()
        self.session = session if session is not None else requests.Session()
        self.headers = headers or {
            "Content-Type": "application/json",
            "Accept":       "application/json"
        }

    def request(
            self, url: str, method: str, data: Any = None, json: Any = None,
            headers: Dict[str, str] = None, params: Dict[str, Any] = None,
            files: Dict[str, Any] = None, cookies: Dict[str, str] = None
    ):
        """
        request 方法用于发送 HTTP 请求，支持 GET、POST、PUT、DELETE 和 PATCH 方法。
        """
        url = self.api_root_url + url
        headers = headers or {}
        headers.update(self.headers)
        params = params or {}
        files = files or {}
        cookies = cookies or {}
        if method.upper() == "GET":
            response = self.session.get(url, headers=headers, params=params)
        elif method.upper() == "POST":
            response = self.session.post(url, json=json, headers=headers, data=data, files=files, cookies=cookies)
            response.close()
        elif method.upper() == "PUT":
            if json:
                data = complex_json.dumps(json)
            response = self.session.put(url, headers=headers, data=data, files=files, cookies=cookies)
        elif method.upper() == "DELETE":
            response = self.session.delete(url, headers=headers, params=params)
        elif method.upper() == "PATCH":
            if json:
                data = complex_json.dumps(json)
            response = self.session.patch(url, headers=headers, data=data, files=files, cookies=cookies)
        else:
            raise ValueError(f"Invalid HTTP method: {method}")
        # log_request(url, method, headers, params, data, json, files, cookies, response)
        return response

    def get(self, url: str, **kwargs: Any):
        return self.request(url, "GET", **kwargs)

    def post(self, url: str, **kwargs: Any):
        return self.request(url, "POST", **kwargs)

    def put(self, url: str, data: Any = None, json: Any = None, **kwargs: Any) :
        return self.request(url, "PUT", data, json, **kwargs)

    def delete(self, url: str, **kwargs: Any):
        return self.request(url, "DELETE", **kwargs)

    def patch(self, url: str, data: Any = None, json: Any = None, **kwargs: Any):
        return self.request(url, "PATCH", data, json, **kwargs)


# if __name__ == "__main__":
#     login = RestClient('https://apppreview.xurongwl.com')
#
#     config_info = read_file("../app/config/config.yaml")
#     user_info = config_info.get("login_case").get("test_user_1")
#     user_mobile = user_info.get("mobile")
#     user_pwd = user_info.get("pwd")
#     json_data = {
#         'number': user_mobile,
#         'password': user_pwd,
#     }
#     c_token = get_ctoken()
#     login.headers.update({'C-Token': c_token})
#     login.post('/users/loginpwd', json=json_data)
#     print(login.session.cookies.get_dict())
