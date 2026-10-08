import random
from utils.personal_util import get_person_name, get_id_no, get_mobile_no
from config import db_conn

count_no = 0

while count_no < 4:
    random_num = random.randint(0, 9999999999)
    sql_list = []
    name = get_person_name()
    id_no = get_id_no()
    mobile = get_mobile_no()
    cust_no = "TESTCT000001" + str(random_num)
    acct_no = "TESTAC000001" + str(random_num)
    user_no = "TESTR000001" + str(random_num)
    for i in range(1, 5):
        case_num = random.randint(0, 99999999999)
        case_no = "TESTCM00001" + str(case_num)
        loan_req_no = "TESTLP00001" + str(case_num)
        loan_no = "TESTLN00001" + str(case_num)
        sql_1 = (
            "INSERT INTO lcs.cm_collection_case(id,case_no,app,fund_source,product_code,sub_product_code,org_code,fund_code,"
            "loan_req_no,loan_no,cust_no,acct_no,user_no,cust_name,id_no,mobile_no,channel_id,loan_source,office_id,"
            "first_contact_relationship,first_contact_name,first_contact_tel_no,second_contact_relationship,"
            "second_contact_name,second_contact_tel_no,credit_limit,loan_amt,term,date_loan,date_loan_start,"
            "date_loan_end,earliest_due_date,repay_day,overdue_days,overdue_periods,overdue_amount,prin_amt,"
            "int_amt,oint_amt,deduct_amt,fee1_amt,fee2_amt,fee3_amt,fee4_amt,fee5_amt,fee6_amt,remain_total_amt,"
            "remain_prin_amt,remain_int_amt,remain_fee1_amt,remain_fee2_amt,remain_fee3_amt,remain_fee4_amt,"
            "remain_fee5_amt,remain_fee6_amt,remain_equity_amt,time_in,date_out,remarks,collection_status,status,"
            "overdue_status,del_flag,date_created,created_by,date_updated,updated_by)VALUES"
            f"(id,'{case_no}','乐小融','ZBANK','P_LOAN','P_LOAN_F36','ZBANK','ZBANK_E8','{loan_req_no}',"
            f"'{loan_no}','{cust_no}','{acct_no}','{user_no}','{name}',"
            f"'{id_no}','{mobile}','HUB_LXJ','HUB_LXJ','10001','母亲','0uArZpy-妻1','44Ssn4672031','朋友',"
            "'0XmJVNV-子1','blv7J5119031',28000.00,1300.00,12,'2034-01-20 00:00:00','2034-01-20','2034-01-20','2034-02-20'"
            ",11,1,'1',31.60,0.00,0.00,0.00,0.00,0.00,0.00,23.92,7.68,0.00,0.00,1567.20,1100.04,87.96,0.00,0.00,287.04,92.16,0.00,0.00,0.00,"
            "'2025-04-24',null,null,'M1','1','1','0','2025-04-23 18:56:53','sys','2025-04-24 09:50:33','sys');")

        sql_list.append(sql_1)
        # print(sql_1)
    db_conn("BM_SIT").exe_multi(sql_list)
    count_no += 1
