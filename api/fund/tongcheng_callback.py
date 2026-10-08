# #!/usr/bin/env python
# # -*- coding: UTF-8 -*-
# import time
#
# from api.fund._base_requests import FundBaseRequest
#
#
# class Tongcheng(FundBaseRequest):
#     # 同程机构回调接口
#
#     def __init__(self):
#         super().__init__(fund_code="tongcheng", fund_name="同程")
#
#     @FundBaseRequest.marked_method
#     def credit_callback_data(self, user_no="我方user_no", apply_no="我方applyNo", channel_apply_no="我方channel_apply_no",
#                              status="03", amount=160000, suc_date=time.time()):
#         """授信回调"""
#         path = f"tongcheng/credit/apply"
#         json_data = {
#             "memberId":       user_no,
#             "applyNo":        apply_no,
#             "channelApplyNo": channel_apply_no,
#             "creditStatus":   status,
#             "creditLimit":    amount,
#             "sucDate":        suc_date
#         }
#         response = self.fund_res_model(method_name="授信结果回调", method_url=path, method_data=json_data)
#         return response
#
#     @FundBaseRequest.marked_method
#     def tongcheng_draw(self, user_no="我方user_no", apply_no="我方applyNo", channel_apply_no="我方channel_apply_no",):
#         """借款回调"""
#         path = f"/tongcheng/loan"
#         json_data = {
#             "channelApplyNo": channel_apply_no,
#             "memberId": user_no,
#             "loanNo": "TQYJKN202401020001",
#             "loanAmt": 800000,
#             "serviceFee": 0,
#             "boundDiscountAmt": 0,
#             "loanTerm": 6,
#             "loanTermUnit": 3,
#             "periodType": 2,
#             "loanPurpose":"教育",
#             "bankName": "招商银行",
#             "applyTime": "2023-09-17 10:25:58",
#             "successTime": "2023-09-19 10:29:19"
#         }
#         response = self.fund_res_model(method_name="借款结果回调", method_url=path, method_data=json_data)
#         return response
#
#     @FundBaseRequest.marked_method
#     def tongcheng_repay(self, user_no="我方user_no", apply_no="我方applyNo", channel_apply_no="我方channel_apply_no",):
#         """还款回调"""
#         path = f"/tongcheng/repay"
#         json_data = {
#              "channelApplyNo": channel_apply_no,
#              "memberId": user_no,
#              "loanNo": "TQYJKN20231222435532",
#              "repayNo": "TQYHKN2023122234332",
#              "instalNums": "2,3",
#              "repaymentType": 1,
#              "repayAmt": 210882,
#              "repayPrincipal": 201925,
#              "repayInterest": 5590,
#              "repayLatefee": 0,
#              "repayAdvanceFee": 0,
#              "payChannel": 1,
#              "cardNo": "622222023762829478",
#              "bankName": "招商银行",
#              "applyTime": "2023-09-08 17:06:34",
#              "successTime": "2023-09-08 17:08:34",
#              "settleStatus": 1
#         }
#         response = self.fund_res_model(method_name="还款结果回调", method_url=path, method_data=json_data)
#         return response
#
#
# if __name__ == '__main__':
#     tongcheng = Tongcheng()
#     mark = tongcheng.get_marked_methods()
#     print(mark)
#     credit_data = tongcheng.credit_callback_data()
#     print(credit_data)
#     print(f"fdsafdsaf \n dshaf/n")
#
#     # @staticmethod
#     # def draw_callback(user_no, channel_apply_no, applyNo, status="03", amount=160000, suc_date=time.time()):
#     #     # 借款回调
#     #     url = f"{cbg_gateway}{tongcheng_api.get('draw_callback')}"
#     #     json_data = {
#     #         "channelApplyNo":   "CR0658629802327392256",
#     #         "memberId":         "UR0655876971492339712",
#     #         "loanNo":           "TQYJKN20230907180703365",
#     #         "loanAmt":          800000,
#     #         "serviceFee":       0,
#     #         "boundDiscountAmt": 0,
#     #         "loanTerm":         6,
#     #         "loanTermUnit":     3,
#     #         "periodType":       2,
#     #         "loanPurpose":      "教育",
#     #         "bankName":         "招商银行",
#     #         "applyTime":        "2023-09-17 10:25:58",
#     #         "successTime":      "2023-09-19 10:29:19"
#     #     }
#     #     response = requests.request("POST", url, json=json_data)
#     #     return response
#     #
#     # @staticmethod
#     # def repay_callback(user_no, channel_apply_no, applyNo, status="03", amount=160000, suc_date=time.time()):
#     #     # 还款回调
#     #     url = f"{cbg_gateway}{tongcheng_api.get('repay_callback')}"
#     #     json_data = {
#     #         "channelApplyNo":  "CRTONGCHENG0647082406671257604",
#     #         "memberId":        "UR0647082363117588480",
#     #         "loanNo":          "TQYJKN20230907180703654",
#     #         "repayNo":         "TQYHKN20230908170837384",
#     #         "instalNums":      "2,3",
#     #         "repaymentType":   1,
#     #         "repayAmt":        210882,
#     #         "repayPrincipal":  201925,
#     #         "repayInterest":   5590,
#     #         "repayLatefee":    0,
#     #         "repayAdvanceFee": 0,
#     #         "payChannel":      1,
#     #         "cardNo":          "622222023762829478",
#     #         "bankName":        "招商银行",
#     #         "applyTime":       "2023-09-08 17:06:34",
#     #         "successTime":     "2023-09-08 17:08:34",
#     #         "settleStatus":    1
#     #     }
#     #     response = requests.request("POST", url, json=json_data)
#     #     return response
#
#
# # if __name__ == '__main__':
# #     res = TongchengCallback.credit_callback("ur43214", "CR3214", "4321432").json()
# #     print(res)
