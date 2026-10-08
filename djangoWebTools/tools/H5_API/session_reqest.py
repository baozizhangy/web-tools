import requests
import json, time, random
from utils.base_request_util import SessionRequest


class H5SessionRequest(SessionRequest):
    def __init__(self, user_no, credit_no, bm_user_no, apply_no, scene=None):
        super().__init__(user_no, credit_no, bm_user_no, scene)
        self.apply_no = apply_no
        if not self.get_base_url():
            raise Exception('session建立失败')


    def _get_url(self, api_path):
        return self.host + api_path


    def _random_number(self):
        return random.randint(100000, 999999)

    def _meta_data(self):
        mata_data = {
            "bizContentNo": "fcdf5f50492092cbc69730323" + str(self._random_number()),
            "channelId": "HUB_LXJ",
            "channelUid": "2000",
            "clientIp": "220.248.97.2",
            "os": "android",
            "timestamp": self._get_date(),
            "userNo": self.bm_user_no,
            "version": "9.4.1"
        }
        return mata_data

    def _base_data(self, data):
        base_data = {
            "appId": "clg-service",
            "data": data,
            "meta": self._meta_data()
        }
        return base_data
    def request_api(self,method, api_path, data=None):
        """
        接口调用方法
        data:请求体，自动包装meta
        """
        url = self._get_url(api_path)
        data = self._base_data(data or {})
        method = method.upper()
        if method == 'POST':
            resp = self.session.post(url, json=data)
        elif  method == 'GET':
            resp = self.session.get(url, json=data)
        else:
            raise Exception('不支持的请求方式')
        try:
            return resp.json()
        except Exception as e:
            print(e)

    def draw_trial(self, term, amt):
        trial_date = {
            "applyNo": self.apply_no,
            "term": term,
            "trialAmt": amt
        }
        url = self._get_url('/lps/api/u/bm/draw/v1/trial')
        trial_data = self._base_data(trial_date)
        resp = self.session.post(url, json=trial_data)
        return resp.json()


if __name__ == '__main__':
    h5_session = H5SessionRequest('UR98532952671213505TEST', 'CT788773509454TEST', 'UR1011159275139043328',
                                  'AP1011159289433382912')
    h5_session.draw_trial(12, 1000)
