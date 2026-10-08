import datetime, json, random
from dateutil.relativedelta import relativedelta


def get_random():
    return random.randint(1, 99999999)


def get_date(is_date=None):
    if is_date and isinstance(is_date, str):
        try:
            date = (datetime.datetime.strptime(is_date, "%Y-%m-%d") - relativedelta(months=1)).date()
            return date
        except ValueError:
            return "请输入正确的日期格式"
    return None


def get_info(term=12, amt=3500, is_date=None):
    """
    生成还款计划mock数据
    """
    if is_date and isinstance(is_date, str):
        try:
            date = datetime.datetime.strptime(is_date, "%Y-%m-%d")

        except ValueError:
            return "请输入正确的日期格式"
    else:
        date = datetime.datetime.now()
    print("验证时间字段的问题{}")
    list_1 = []
    for i in range(term):
        A = {
            'term_no1': i + 1,
            # 'repay_date': (datetime.datetime.now() + datetime.timedelta(days=i * 30)).strftime("%Y%m%d"),
            'repay_date': (date + relativedelta(months=i)).strftime("%Y%m%d"),
            'principal1': round(float(amt / term), 2),
            'interest1': round(float(amt / term * 0.08), 2),
            'is_overdue': '0',
            'penalty_amount1': 0,
            'actualRepayDate': None,
            'paid_principal1': 0,
            'paid_interest1': 0,
            'paid_penalty_amount1': 0,
            'intefine1': 0,
            'paid_intefine1': 0,
            'grtFee': 0,
            'actualGrtFee': 0
        }
        list_1.append(A)
    mode = {
        "code": "000000",
        "msg": "success",
        "result": {
            "repay_plan": list_1, }}
    return json.dumps(mode)


def get_tl_info(term=12, amt=3500, user_no=None, is_date=None):
    date_obj = get_date(is_date)
    if isinstance(date_obj, str):
        return date_obj
    if date_obj is not None:
        date = date_obj
    # if is_date and isinstance(is_date, str):
    #     try:
    #         date = (datetime.datetime.strptime(is_date, "%Y-%m-%d") - relativedelta(months=1)).date()
    #     except ValueError:
    #         return "请输入正确的日期格式"
    else:
        date = datetime.datetime.now()
    list_1 = []
    # period_no = random.randint(1, 99999999)
    loan_no = 'FUND_NO25041100009517' + str(get_random())
    if user_no is None:
        user_no = 'CT0984590184257' + str(get_random())
    for i in range(term):
        A = {
            "loan_no": loan_no,
            "term_no": i + 1,
            "period_id": loan_no + "_" + str(i + 1),
            "status": "0",
            "start_day": (date + relativedelta(months=i)).strftime("%Y%m%d"),
            "end_day": (date + relativedelta(months=i + 1)).strftime("%Y%m%d"),
            # 宽限期写死三天，可都配置
            "settle_day": (date + relativedelta(months=i + 1, days=3)).strftime("%Y%m%d"),
            "principal_balance": 0,
            "deserved_principal": round(float(amt) / term, 2),
            "paid_principal": 0,
            "interest_balance": round(float(amt / term * 0.08), 2),
            "deserved_interest": round(float(amt / term * 0.08), 2),
            "paid_interest": 0,
            "penalty_balance": 0,
            "deserved_penalty": 0,
            "paid_penalty": 0

        }
        list_1.append(A)
    mode = {
        "code": "0000",
        "msg": "success",
        "bizData": {
            "user_id": user_no,
            "loan_no": loan_no,
            "product_no": "TLZY0001",
            "loan_amt": amt,
            "loan_periods": term,
            "loan_date": str(date),
            "repay_type": "1",
            "period_bill": list_1

        }}
    return json.dumps(mode)


def get_lh_info(term=12, amt=3500, is_date=None):
    date_obj = get_date(is_date)
    if isinstance(date_obj, str):
        return date_obj
    if date_obj is not None:
        date = date_obj
    # if is_date and isinstance(is_date, str):
    #     try:
    #         date = (datetime.datetime.strptime(is_date, "%Y-%m-%d") - relativedelta(months=1)).date()
    #     except ValueError:
    #         return "请输入正确的日期格式"
    else:
        date = datetime.datetime.now()
    list_1 = []
    amount_amt = round(float(amt) / term, 2)
    interest = round(float(amt / term * 0.08), 2)
    for i in range(term):
        A = {
            "currentNum": i + 1,
            "repayNum": term,
            "startDate": (date + relativedelta(months=i)).strftime("%Y%m%d"),
            "repayDate": (date + relativedelta(months=i + 1)).strftime("%Y%m%d"),
            "graceDate": (date + relativedelta(months=i + 1, days=3)).strftime("%Y%m%d"),
            "repayAmount": (amount_amt + interest),
            "repayPrincipal": amount_amt,
            "repayInterest": interest,
            "repayFee": 0,
            "repayOverdueFee": 0,
            "repayCompoundInterest": 0,
            "discountInterest": 0,
            "discountFee": 0,
            "leftRepayAmount": (amount_amt + interest),
            "leftRepayPrincipal": amount_amt,
            "leftRepayInterest": interest,
            "leftRepayFee": 0,
            "leftRepayOverdueFee": 0,
            "leftRepayCompoundInterest": 0,
            "leftDiscountInterest": 0,
            "leftDiscountFee": 0,
            "overdueDays": 0,
            "repayStatus": "1"
        }
        list_1.append(A)

    mode = {
        "code": "0000",
        "msg": "success",
        "bizData": {
            "reasonCode": "A00",
            "reasonMsg": "success",
            "dataList": list_1
        }
    }
    return json.dumps(mode)


def get_zql_info(term=12, amt=3500, is_date=None):
    date_obj = get_date(is_date)
    if isinstance(date_obj, str):
        return date_obj
    if date_obj is not None:
        date = date_obj
    else:
        date = datetime.datetime.now()
    list_1 = []
    amount_amt = round(float(amt) / term, 2)
    interest = round(float(amt / term * 0.16), 2)
    service_fee = round(float(amt / term * 0.05), 2)
    consultfee = round(float(amt / term * 0.05), 2)
    order_no_test = 'TEST882508060015' + str(get_random())
    for i in range(term):
        A = {
            "orderNo": order_no_test,
            "installCnt": i + 1,
            "totalAmount": sum([amount_amt, interest, service_fee, consultfee]),
            "principal": amount_amt,
            "interest": interest,
            "serviceFee": service_fee,
            "consultFee": consultfee,
            "otherFee": "0",
            "overdueFee": "0.00",
            "repaymentTotalAmount": "0.00",
            "repaymentPrincipal": "0.00",
            "repaymentInterest": "0.00",
            "repaymentServiceFee": "0.00",
            "repaymentConsultFee": "0.00",
            "repaymentOtherFee": "0",
            "repaymentOverdueFee": "0.00",
            "reductionAmt": "0",
            "status": "0",
            "lateRepayDate": (date + relativedelta(months=i)).strftime("%Y-%m-%d"),
            "comFlag": "2"
        }
        list_1.append(A)
    mode = {
        "code": "10000",
        "msg": "成功",
        "bizData": {
            "transDate": (date - relativedelta(months=1)).strftime("%Y-%m-%d"),
            "totalInstallCnt": term,
            "repayPlanList": list_1
        }
    }
    return json.dumps(mode)


def get_zql_info(term=12, amt=3500, is_date=None):
    date_obj = get_date(is_date)
    if isinstance(date_obj, str):
        return date_obj
    if date_obj is not None:
        date = date_obj
    else:
        date = datetime.datetime.now()
    list_1 = []
    amount_amt = round(float(amt) / term, 2)
    interest = round(float(amt / term * 0.16), 2)
    service_fee = round(float(amt / term * 0.05), 2)
    consultfee = round(float(amt / term * 0.05), 2)
    order_no_test = 'TEST882508060015' + str(get_random())
    for i in range(term):
        A = {
            "orderNo": order_no_test,
            "installCnt": i + 1,
            "totalAmount": sum([amount_amt, interest, service_fee, consultfee]),
            "principal": amount_amt,
            "interest": interest,
            "serviceFee": service_fee,
            "consultFee": consultfee,
            "otherFee": "0",
            "overdueFee": "0.00",
            "repaymentTotalAmount": "0.00",
            "repaymentPrincipal": "0.00",
            "repaymentInterest": "0.00",
            "repaymentServiceFee": "0.00",
            "repaymentConsultFee": "0.00",
            "repaymentOtherFee": "0",
            "repaymentOverdueFee": "0.00",
            "reductionAmt": "0",
            "status": "0",
            "lateRepayDate": (date + relativedelta(months=i + 1)).strftime("%Y-%m-%d"),
            "comFlag": "2"
        }
        list_1.append(A)
    mode = {
        "code": "10000",
        "msg": "成功",
        "bizData": {
            "transDate": (date).strftime("%Y-%m-%d"),
            "totalInstallCnt": term,
            "repayPlanList": list_1
        }
    }
    return json.dumps(mode)


if __name__ == '__main__':
    # print(get_tl_info(term=12, amt=1100, user_no='CT0984590865815076864', is_date='2023-03-01'))
    # print(get_info(term=12, amt=1100, is_date="123"))
    # print(mock_data_update('UR0957937150588891136','DEV'))
    # print(get_lh_info(12, 1100, is_date='2025-05-29'))
    print(get_zql_info(12, 1100, is_date='2025-05-29'))
