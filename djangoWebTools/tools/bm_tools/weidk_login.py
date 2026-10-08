import requests
from aiohttp.web_app import Application

from pytestAutoTest.data import easy_data
from utils.logger_util import web_logger


class WidekApi:
    """
    easy mock 更新接口
    """

    def __init__(self):
        self.session = None
        self.Authorization = None

    def wedik_login(self):
        login_url = 'http://widek-sit.shangtoutech.com/widek-api/manage/login'
        login_data = "name=ziyuan&password=JWT9oGWoyL30DWYzHv6CGZq5uOhDZuPVsz%2B1hV8ddlJK0asL%2F0vGhCMO7REZOqgTBUAQGjD9BezelxA5XSi5JA%3D%3D&code='1'"
        # login_data = {"name": "ziyuan", "password": "JWT9oGWoyL30DWYzHv6CGZq5uOhDZuPVsz%2B1hV8ddlJK0asL%2F0vGhCMO7REZOqgTBUAQGjD9BezelxA5XSi5JA%3D%3D", "code": "1"}
        self.session = requests.Session()
        header = {
            "Authorization": "Basic d2lkZWs6VFZSSmVrNUVWVEk9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
            "Host": "widek-sit.shangtoutech.com",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.Session().post(login_url, data=login_data, headers=header)

        # self.Authorization = response.json()['data']['token']
        return response.json()

    # def easy_mock_update(self):
    #     update_url = 'http://easymock-test.shangtoutech.com/api/mock/update'
    #     mode = easy_data.get_info(term=self.term, amt=self.amt)
    #     web_logger.info(f"修改后的mock数据mode === {mode}")
    #     update_data = {
    #         "description": self.desc_name,
    #         "id": self.desc_id,
    #         "mode": mode,
    #         'method': self.method,
    #         "url": self.mock_url
    #     }
    #     if not self.session:
    #         self.easy_mock_login()
    #     header = {
    #         "Authorization": f"Bearer {self.Authorization}"
    #     }
    #     session_easy = self.session.post(update_url, data=update_data, headers=header)
    #     return session_easy.json()


if __name__ == '__main__':
    A = WidekApi()
    print(A.wedik_login())
