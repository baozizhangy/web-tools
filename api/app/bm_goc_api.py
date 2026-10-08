import random, json, requests
from utils.goc_ciphertext import GocSecurity
from utils.logger_util import web_logger
from utils.personal_util import get_person_name, get_id_no, get_mobile_no


class BmGocApi:
    """
    新建的类，用于调用 http://bm-sit.shangtoutech.com/chg/goc/bm/api 接口
    使用 GocSecurity 的 AES ECB 加密 + RSA SHA256WithRSA 签名
    域名直接指定，不从配置中取
    """

    def __init__(self, env=None, config=None):
        self.env = env or 'BM_SIT'
        # 直接指定域名，不从配置中取
        self.base_url = 'http://bm-sit.shangtoutech.com/chg/goc'
        self.goc_security = GocSecurity(config=config)

    def call_api(self, request_data, api_path):
        """
        通用接口调用方法
        :param request_data: 请求数据字典
        :param api_path: API路径，例如: /bm/api/queryCreditForOut
        :return: 解密后的响应数据
        """
        web_logger.info(f"调用{self.env}/GOC接口::request_data::{request_data}, api_path::{api_path}")

        # 1. 使用 GocSecurity 加密数据并生成签名
        encrypted_request = self.goc_security.encrypt_data(request_data)

        # 2. 发送请求
        url = self.base_url + api_path
        web_logger.info(f"请求URL::{url}, 加密后请求数据::{json.dumps(encrypted_request, ensure_ascii=False)}")

        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=encrypted_request, headers=headers)

        web_logger.info(f"调用{self.env}/GOC接口响应::response::{response.text}")

        # 3. 解密响应（验签 + AES 解密）
        response_json = response.json()
        try:
            decrypted_data = self.goc_security.decrypt_response(response_json)
            web_logger.info(
                f"解密后的响应数据::{json.dumps(decrypted_data, ensure_ascii=False) if isinstance(decrypted_data, dict) else decrypted_data}")
            return decrypted_data
        except ValueError as e:
            web_logger.error(f"响应解密失败::{e}, 原始响应::{response_json}")
            return response_json

    def query_credit_for_out(self, id_no=None, id_type=None, cust_name=None, effective_time=None,
                             need_result='Y', mobile_no=None, appl_no=None, asyncSign=None, id_card_front_url=None,
                             id_card_back_url=None, face_info_url=None):
        """
        查询资信接口
        :param id_no: 身份证号 (可选，根据资信要求)
        :param id_type: 证件类型 (可选，根据资信要求)
        :param cust_name: 客户姓名 (可选，根据资信要求)
        :param effective_time: 有效期(天) (可选)
        :param need_result: 是否同步返回查询结果，Y-是，N-否 (默认Y)
        :param mobile_no: 手机号 (额外参数)
        :param appl_no: 业务号 (额外参数)
        :param id_card_front_url: 身份证正面url (额外参数)
        :param id_card_back_url: 身份证反面url (额外参数)
        :param face_info_url: 活体影像url (额外参数)
        :return: 解密后的响应数据
        """
        json_data = {
            "oprSys": "DL",  # 固定值
            "intfType": "HYQTZJInsightScore53102"  # 昊悦-钱塘-火山引擎-多维洞察预测评分53102
        }

        # 可选参数
        if id_no:
            json_data["idNo"] = id_no
        if id_type:
            json_data["idType"] = id_type
        if cust_name:
            json_data["custName"] = cust_name
        if effective_time:
            json_data["effectiveTime"] = effective_time
        if need_result:
            json_data["needResult"] = need_result

        # 额外参数 params
        params = {}
        if mobile_no:
            params["mobileNo"] = mobile_no
        if appl_no:
            params["applNo"] = appl_no
        if id_card_front_url:
            params["idCardFrontUrl"] = id_card_front_url
        if id_card_back_url:
            params["idCardBackUrl"] = id_card_back_url
        if face_info_url:
            params["faceInfoUrl"] = face_info_url
        if asyncSign:
            params["asyncSign"] = asyncSign
        if params:
            json_data["params"] = params

        return self.call_api(json_data, "/bm/api/queryCreditForOut")

    def query_credit_result(self, cr_no, intf_type="HYQTZJInsightScore53102"):
        """
        查询资信结果接口
        :param cr_no: 申请返回的请求号 (必传)
        :param intf_type: 对应资信枚举IntfType的code (必传，默认HYQTZJInsightScore53102)
        :return: 解密后的响应数据
        """
        json_data = {
            "oprSys": "DL",  # 固定值
            "intfType": intf_type,
            "crNo": cr_no
        }

        return self.call_api(json_data, "/bm/api/queryCreditResult")


if __name__ == '__main__':
    # 使用示例 - 直接使用 goc_ciphertext.py 中的默认配置
    goc_api = BmGocApi(env='BM_SIT')

    # 调用查询资信接口
    result = goc_api.query_credit_for_out(
        id_no=get_id_no(),
        id_type="01",
        cust_name=get_person_name(),
        effective_time="30",
        need_result="Y",
        mobile_no=get_mobile_no(),
        id_card_front_url="https://gips1.baidu.com/it/u=1410005327,4082018016&fm=3028&app=3028&f=JPEG&fmt=auto?w=960&h=1280",
        id_card_back_url="https://gips2.baidu.com/it/u=2068760849,3022258785&fm=3028&app=3028&f=JPEG&fmt=auto?w=960&h=1280",
        face_info_url="https://gips0.baidu.com/it/u=567323913,331130417&fm=3028&app=3028&f=JPEG&fmt=auto&q=100&size=f1000_1000",
        asyncSign="N",
        appl_no="APPL" + str(random.randint(100000000000, 999999999999))
    )
    # result = goc_api.query_credit_for_out(
    #     id_no='130200200101175421',
    #     id_type="01",
    #     cust_name='包忠诚',
    #     effective_time="2",
    #     need_result="Y",
    #     mobile_no='19334136086',
    #     appl_no="APPL" + str(random.randint(100000000000, 999999999999))
    # )
    print("查询结果:", json.dumps(result, ensure_ascii=False, indent=2))

    # print(goc_api.query_credit_result('CR20260115000000000021'))
