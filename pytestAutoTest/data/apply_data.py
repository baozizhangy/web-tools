import random, json
from utils.personal_util import get_person_name, get_id_no, get_gender
from pytestAutoTest.data.temp_info import generate_contact_info
from utils.base_request_util import common_request
from config import db_conn


class IdCardInfo:
    def __init__(self):
        self.ocr_info = {
            'front_url': 'http://bmtestprivate.oss-cn-shanghai.aliyuncs.com/bmtestprivate/ocr/hub/UR0954878282463973376/1739930734663/gdzmxd/HUB_IDCARD_FRONT.jpeg',
            'back_url': 'http://bmtestprivate.oss-cn-shanghai.aliyuncs.com/bmtestprivate/ocr/hub/UR0954878282463973376/1739930734573/k5vva3/HUB_IDCARD_BACK.jpeg',
            'face_url': 'http://bmtestprivate.oss-cn-shanghai.aliyuncs.com/bmtestprivate/live/hub/UR0954985329893314560/1739946685785/eoxggk/HUB_LIVE.jpeg'}

    def _get_data(self, url):
        json_data = {'url': url}
        res = common_request.api_request('get', json_data, '/chg/ccs/api/p/file/access')
        return json.loads(res)['data']

    def front_data(self):
        return self._get_data(self.ocr_info['front_url'])

    def back_data(self):
        return self._get_data(self.ocr_info['back_url'])

    def face_url(self):
        return self._get_data(self.ocr_info['face_url'])


class ResultBase:
    def __init__(self, mobile, name, id_card_no):
        self.mobile = mobile
        self.name = name
        self.id_card_no = id_card_no
        self.ocr_data = IdCardInfo()

    def user_base_info(self):
        # 账户信息
        user_info = {'userName': self.name, 'mobileNo': self.mobile}
        return user_info

    def user_profile_info(self):
        # 用户基础信息,枚举状态对照接口文档
        education = ['01', '02', '03', '04', '05']
        loan_term = [3, 6, 9, 12]
        loanPurpose = ['01', '02', '03', '04', '05', '06', '07', '08']
        monthIncome = ['01', '02', '03', '04', '05']
        residentialType = ['01', '02', '03', '04', '05']
        profile_info = {
            "address": "上海市-上海市辖区-徐汇区",
            "addressDetail": "徐汇徐汇徐汇徐汇徐汇地址详细信息",
            "education": random.choice(education),
            "expectedLoanAmt": 19000,
            "expectedLoanTerm": random.choice(loan_term),
            "loanPurpose": random.choice(loanPurpose),
            "marriage": "03",
            "monthIncome": random.choice(monthIncome),
            "residentialCity": "上海市辖区",
            "residentialCityCode": "310100",
            "residentialDistrict": "徐汇区",
            "residentialDistrictCode": "310104",
            "residentialProvince": "上海市",
            "residentialProvinceCode": "310000",
            "residentialType": random.choice(residentialType)
        }

        return profile_info

    def id_info(self):
        # id_card_no = get_id_no()
        idCardSex = get_gender(self.id_card_no)
        if idCardSex == "女":
            sex = 1
        else:
            sex = 0
        id_info_data = {
            "idCardAddress": "新疆郑州市中原区周集乡幸福村5号",
            "idCardAuthority": "九江县公安局",
            "idCardBackImgUrl": self.ocr_data.back_data(),
            "idCardBirthday": "1990-09-25",
            "idCardEndDate": "20341001",
            "idCardEthnicity": "汉",
            "idCardFrontImgUrl": self.ocr_data.front_data(),
            "idCardNo": self.id_card_no,
            "idCardSex": sex,
            "idCardStartDate": "20241001",
            "name": self.name
        }
        return id_info_data

    def face_info(self):
        face_data = {
            "faceCollectTime": "2025-02-19 10:43:04",
            "faceDetectBasicData": "{\"attackResult\":{\"result\":false,\"score\":0.26,\"threshold\":0.5},\"bizNo\":\"\",\"images\":{\"imageBest\":\"http://private-sit.oss-cn-shanghai.aliyuncs.com/private-sit/live/ks/UR0678422985435332608/1698736513281/zuS2t4/1.jpeg\"},\"requestId\":\"1531397565,39b19451-393c-4fc4-8fae-6dc74b2b00d7\",\"resultCode\":1000,\"resultMessage\":\"SUCCESS\",\"riskInfo\":{\"deviceInfoLevel\":\"2\",\"deviceInfoTags\":{\"isHook\":1,\"isInjection\":1,\"isRoot\":0,\"isVirtualEnvironment\":1}},\"timeUsed\":1448,\"verification\":{\"idcard\":{\"confidence\":86.63057,\"thresholds\":{\"1e-3\":62.168713,\"1e-4\":69.31534,\"1e-5\":74.39926,\"1e-6\":78.038055}}}}",
            "faceImg1Url": self.ocr_data.face_url(),
            "faceScore": 86.63057,
            "faceSource": 1
        }
        return face_data

    def contact_info(self):
        contactInfo = generate_contact_info()['contactInfos']
        return contactInfo

    def job_info(self):
        job = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15']
        job_type = ['01', '02', '03', '04', '05', '06', '07']
        job_group = ['01', '02', '03', '04', '05']
        job_data = {
            "companyAddress": "上海市-上海市辖区-徐汇区",
            "companyAddressDetail": "徐汇徐汇徐汇徐汇徐汇地址详细信息",
            "companyName": "个体工商户",
            "companyType": random.choice(job_type),
            "jobCategory": random.choice(job_group),
            "jobIndustry": random.choice(job)
        }
        return job_data

    def device_info(self):
        device_data = {
            "deviceId": "5FADD09B-8D7D-4A24-A825-C22EF2B89EAF",
            "ip": "222.71.89.50",
            "isRoot": 0,
            "isSimulator": 0,
            "os": "ios",
            "os_version": "18.3.1"
        }
        return device_data

    def geo_info(self):
        geo_info_data = {
            "address": "上海市-上海市辖区-徐汇区",
            "addressDetail": "徐汇徐汇徐汇徐汇徐汇地址详细信息",
            "latitude": "31.222222",
            "longitude": "121.222222"
        }
        return geo_info_data


class DrawOrder:
    def __init__(self, mobile):
        self.mobile = mobile

    def card_info(self, card_no, bank_code, bank_name):
        card_info_sql = "SELECT * from cis.bm_default_bankcard t where t.cust_no = 'CT0956024127729180672'; "

        card_info_data = {
            "bankCode": bank_code,
            "bankMobile": self.mobile,
            "bankName": bank_name,
            "cardNo": card_no
        }
        return card_info_data
    # if __name__ == '__main__':


def get_partner_draw_no(env, loan_no):
    # 获取渠道借款流水号，用于还款绑卡使用
    draw_no_sql = ("select partner_draw_no from hub.hub_channel_bm_draw where draw_no = "
                   f"(select loan_req_no from lcs.ln_loan where loan_no = '{loan_no}');")
    draw_no = db_conn(env).select_one(draw_no_sql)['data']['partner_draw_no']
    return draw_no


def fetch_credit_info(mobile, env):
    # 授信用户基本信息
    credit_info_query = ("select channel_apply_no, user_no as bm_user_no, partner_user_no, partner_channel_apply_no,cust_no "
                         "from hub.hub_channel_bm_apply where user_no = (select user_no from cis.u_user where "
                         f"mobile_no_md5 = md5('{mobile}'));")
    credit_res = db_conn(env).select_one(credit_info_query)['data']
    return credit_res if credit_res else None


if __name__ == '__main__':
    print(get_partner_draw_no('LN0984624832295522304'))
