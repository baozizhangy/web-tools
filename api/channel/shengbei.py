from enum import Enum
from api.channel._base_requests import BaseRequest
from utils.cryption_util import md5_encrypt
from utils.personal_util import get_mobile_no, get_person_name

# shengBeiMethodMap.put("user-check", MethodEnum.CHECK.getCode());
# shengBeiMethodMap.put("audit-apply", MethodEnum.SUBMIT.getCode());
# shengBeiMethodMap.put("audit-info", MethodEnum.CONCLUSION.getCode());
# shengBeiMethodMap.put("contract-list", MethodEnum.CONTRACT.getCode());


class ShengbeiMethodsEnum(Enum):
    # ("渠道方法名", "方法中文名", "对应的数据模板方法")
    CHECK = ("ser-check", "准入", "get_check_data")
    CREDIT = ("audit-apply", "授信", "get_credit_data")
    CREDIT_RESULT = ("audit-info", "授信结果", "get_credit_result_data")
    CONTRACT = ("contract-list", "协议列表", "get_contract_data")


class Shengbei(BaseRequest):

    def __init__(self, ):
        super().__init__(channel_id="HUB_SHENGBEI", channel_name="省呗", channel_method_enum=ShengbeiMethodsEnum,
                         channel_uid="21883", py_code="shengbei")

    def get_check_data(self, data):
        # 准入接口入参
        mobile = data.get("channelMobile")
        id_no = data.get("channelIdNo")
        check_no = data.get("channelCheckNo")
        name = data.get("channelCustName")
        channel_user_no = data.get("channelUserNo")
        channel_credit_no = data.get("channelCreditNo")
        req_data = {
            "phoneNo":        md5_encrypt(mobile),
            "idNo":           md5_encrypt(id_no),
            "custName":       name,
            "serial":         check_no,
            "idType":         "01",
            "custNo":         channel_user_no,
            "phoneNoAndIdNo": md5_encrypt(mobile + id_no)

        }
        return self.data_model(ShengbeiMethodsEnum.CHECK.value[0], req_data)

    def get_credit_data(self, data):
        mobile = data.get("channelMobile")
        id_no = data.get("channelIdNo")
        name = data.get("channelCustName")
        bank_card = data.get("channelBankCardNo")
        channel_user_no = data.get("channelUserNo")
        channel_check_no = data.get("channelCheckNo")
        channel_credit_no = data.get("channelCreditNo")
        channel_draw_no = data.get("channelDrawNo")
        channel_repay_no = data.get("channelRepayNo")
        hub_user_id = data.get("hubUserId")
        hub_order_no = data.get("hubOrderNo")
        hub_sub_order_no = data.get("hubSubOrderNo")
        req_data = {
            "creditApplyNo":          channel_credit_no,
            "custNo":                 channel_user_no,
            "custName":               name,
            "idType":                 "01",
            "idNo":                   id_no,
            "idValidDate":            "20220101",
            "idExpireDate":           "20320101",
            "idAddress":              "河北省石家庄市新华区马甲路120号",
            "issueAgency":            "GovernmentOffice",
            "issueDate":              "20220101",
            "gender":                 "01",
            "birthDate":              "19901005",
            "phoneNo":                mobile,
            "nation":                 "汉族",
            "maritalStatus":          "10",
            "educationType":          "30",
            "occupationType":         "1",
            "monthlyIncome":          "6",
            "addressProvince":        "上海市",
            "addressCity":            "上海市",
            "addressArea":            "徐汇区",
            "addressDetail":          "龙华路222号",
            "relationInfo":           {
                "relationType1":    "4",
                "relationPhoneNo1": get_mobile_no(),
                "relationName1":    get_person_name(),
                "relationType2":    "3",
                "relationPhoneNo2": get_mobile_no(),
                "relationName2":    get_person_name()
            },
            "terminalInfo":           {
                "phoneMarker":   "Samsung",
                "phoneModel":    "GalaxyS20",
                "mac":           "AA:BB:CC:DD:EE:FF",
                "ip":            "192.168.0.1",
                "systemVersion": "Android11",
                "imei":          "123456789012345",
                "imsi":          "987654321098765",
                "brand":         "Samsung",
                "androidId":     "1234567890",
                "isEmulator":    "N",
                "rootAccess":    "N",
                "terminalType":  "ANDROID"
            },
            "idCertificationUpUrl":   "https://platplat.oss-cn-shanghai.aliyuncs.com/user/4155112/idCard/1626405124/idCard.jpeg",
            "idCertificationDownUrl": "https://platplat.oss-cn-shanghai.aliyuncs.com/user/4155112/idCard/1626405124/idCard.jpeg",
            "livePhotoUrl":           "https://platplat.oss-cn-shanghai.aliyuncs.com/user/4155112/idCard/1626405124/idCard.jpeg",
            "companyName":            "上海市旭荣科技有限公司",
            "companyProvince":        "上海市",
            "companyCity":            "上海市",
            "companyArea":            "徐汇区",
            "companyAddress":         "云锦路111号",
            "companyPhoneNo":         "02186660000"
        }
        return self.data_model(ShengbeiMethodsEnum.CREDIT.value[0], req_data)

    def get_credit_result_data(self, data):
        # 授信结果查询接口入参
        channel_user_no = data.get("channelUserNo")
        channel_credit_no = data.get("channelCreditNo")
        req_data = {
            "creditApplyNo":    channel_credit_no,
            "custNo":           channel_user_no
        }
        return self.data_model(ShengbeiMethodsEnum.CREDIT_RESULT.value[0], req_data)

    def get_contract_data(self, data):
        # 合同接口入参
        channel_user_no = data.get("channelUserNo")
        channel_credit_no = data.get("channelCreditNo")
        channel_draw_no = data.get("channelDrawNo")

        req_data = {
            "scene":    "04",
            "custNo":           channel_user_no,
            "loanApplyNo": channel_draw_no
        }
        return self.data_model(ShengbeiMethodsEnum.CONTRACT.value[0], req_data)
