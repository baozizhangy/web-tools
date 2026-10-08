import datetime
import json
import shutil
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Dict
from urllib.parse import quote

import requests
import urllib3
from openpyxl import load_workbook

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import get_widek_url, db_conn

SAVE_URL = "/manage/coupon/distribute/save"
SUBMIT_TASK_URL = "/manage/coupon/distribute/submitTask?taskNo={task_no}"
BASIC_AUTH = "Basic d2lkZWs6VFZSSmVrNUVWVEk9"
LOGIN_COOKIE = "sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219d4272aa231e5b-0c40e9bc6f87c3-28623615-287859-19d4272aa2418b0%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTlkNDI3MmFhMjMxZTViLTBjNDBlOWJjNmY4N2MzLTI4NjIzNjE1LTI4Nzg1OS0xOWQ0MjcyYWEyNDE4YjAifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%7D; sidebarStatus=1; Admin-Token=; Refresh-Token="
EXCEL_FILE_PATH = Path(__file__).resolve().parent / "优惠券用户信息导入模板.xlsx"
DISCOUNT_COUPON_CODE = "CP1203201968512307200"
FIXED_AMOUNT_COUPON_CODE = "CP1203201672830652416"
DISCOUNT_TASK_NAME = "折扣券"
FIXED_AMOUNT_TASK_NAME = "固定金额券"

DEV_DISCOUNT_COUPON_CODE = "CP1211764633282097152"
DEV_FIXED_AMOUNT_COUPON_CODE = "CP1211764872994959360"


def _get_coupon_code(env):
    if env == 'DEV':
        return DEV_DISCOUNT_COUPON_CODE, DEV_FIXED_AMOUNT_COUPON_CODE
    if env == 'BM_SIT':
        return DISCOUNT_COUPON_CODE, FIXED_AMOUNT_COUPON_CODE
    raise ValueError(f"不支持的 coupon 环境: {env}")


def _get_login_url(env):
    if env == "DEV":
        return "/manage/login?username=ziyuan&password=jy0sRSPzO1V%2FeTiYAcoJ56tfF%2FDhLlH3C1LQknjDcibGzStfmNpzIH13K3FOcNmzQEIlznasWdG5DLZOilXBGw%3D%3D&code=1"
    if env == "BM_SIT":
        return "/manage/login?username=coupon&password=RnrDNyb2MfBFyacbr1qq818SvWxx4Na7TNtdPOeZ0%2FXuW%2FbjtR%2BeOf3u0e3ekjDJwZ1cxY01YV%2FXDvODvj8z9g%3D%3D&code=1"
    raise ValueError(f"不支持的 widek 环境: {env}")


def create_temp_excel_copy(template_path: Path = EXCEL_FILE_PATH) -> Path:
    temp_dir = Path(tempfile.mkdtemp(prefix="coupon_send_"))
    temp_file_path = temp_dir / template_path.name
    shutil.copy2(template_path, temp_file_path)
    print(f"created_temp_excel={temp_file_path}")
    return temp_file_path


def cleanup_temp_file(file_path: Path) -> None:
    try:
        if file_path.exists():
            file_path.unlink()
        parent_dir = file_path.parent
        if parent_dir.exists() and not any(parent_dir.iterdir()):
            parent_dir.rmdir()
        print(f"cleaned_temp_excel={file_path}")
    except Exception as exc:
        print(f"cleanup_temp_excel_failed={file_path}, error={exc}")


def query_coupon_arrival(user_no: str, coupon_code: str, env: str = "BM_SIT", timeout_secs: int = 90) -> bool:
    """轮询查询优惠券是否实际到账(status='01')，超时返回 False。"""
    deadline = datetime.datetime.now() + datetime.timedelta(seconds=timeout_secs)
    time.sleep(3)
    while datetime.datetime.now() < deadline:
        sql = (
            f"select * from cos.offering_record "
            f"where user_no = '{user_no}' and coupon_code = '{coupon_code}' "
            f"and status = '01' order by id desc limit 1;"
        )
        print(f"query_coupon_arrival: {sql}")
        res = db_conn(env).select_one(sql)
        if res["data"] is not None:
            print(f"coupon_arrived: user_no={user_no}, coupon_code={coupon_code}")
            return True
        print(f"coupon_not_arrived_yet, retry after 15s...")
        time.sleep(15)
    print(f"coupon_arrival_timeout: user_no={user_no}, coupon_code={coupon_code}")
    return False


def update_excel_user_info(user_no: str, mobile: str, file_path: Path) -> Path:
    workbook = load_workbook(file_path)
    try:
        worksheet = workbook.active
        worksheet["A2"] = user_no
        worksheet["B2"] = mobile
        workbook.save(file_path)
        print(f"updated_excel={file_path}")
        print(f"A2={worksheet['A2'].value}, B2={worksheet['B2'].value}")
        return file_path
    finally:
        workbook.close()


def build_file_bytes(file_path: Path) -> list[int]:
    with open(file_path, "rb") as file:
        return list(file.read())


def extract_token(response: requests.Response) -> str:
    response_json = response.json()
    token = response_json.get("token")
    if not token:
        raise ValueError("登录成功，但未在 $.token 中取到 token")
    return token


def extract_task_no(response: requests.Response) -> str:
    response_json = response.json()
    task_no = response_json.get("msg")
    if not task_no:
        raise ValueError("save接口成功，但未在 $.msg 中取到 taskNo")
    return str(task_no)


def login(session: requests.Session, env, base_url: str) -> str:
    headers = {
        "Authorization": BASIC_AUTH,
        "Cookie": LOGIN_COOKIE,
    }
    response = session.post(f"{base_url}{_get_login_url(env)}", data="", headers=headers, verify=False)
    print("login_status=", response.status_code)
    print("login_headers=", dict(response.headers))
    print("login_cookies=", session.cookies.get_dict())
    try:
        print("login_response=")
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    except ValueError:
        print("login_response_text=")
        print(response.text)
    response.raise_for_status()

    token = extract_token(response)
    session.headers.update({
        "AuthorizationToken": f"Bearer {token}",
        "Content-Type": "application/json",
    })
    print("authorization_token=", session.headers.get("AuthorizationToken"))
    return token


def get_coupon_config(env: str, discount: bool) -> Dict[str, str]:
    discount_code, fixed_code = _get_coupon_code(env)
    if discount:
        return {
            "couponCode": discount_code,
            "taskName": DISCOUNT_TASK_NAME,
        }
    return {
        "couponCode": fixed_code,
        "taskName": FIXED_AMOUNT_TASK_NAME,
    }


def build_save_payload(file_path: Path, env: str, discount: bool) -> Dict[str, Any]:
    coupon_config = get_coupon_config(env, discount)
    return {
        "taskName": coupon_config["taskName"],
        "couponCode": coupon_config["couponCode"],
        "totalLimit": -1,
        "perUserLimit": -1,
        "scheduleType": "IMMEDIATE",
        "scheduleTime": None,
        "validType": "RELATIVE",
        "validStart": None,
        "validEnd": None,
        "validDays": 7,
        "sendRemind": 1,
        "expireRemind": 0,
        "remindDay": None,
        "fileBytes": build_file_bytes(file_path),
        "operateType": "0",
    }


def submit_task(session: requests.Session, task_no: str, base_url: str) -> requests.Response:
    submit_url = SUBMIT_TASK_URL.format(task_no=quote(task_no, safe=""))
    print(f"submit_task_no={task_no}")
    response = session.post(f"{base_url}{submit_url}", data="", verify=False)
    print("submit_status=", response.status_code)
    try:
        print("submit_response=")
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    except ValueError:
        print("submit_response_text=")
        print(response.text)
    response.raise_for_status()
    return response


def confirm_task(session: requests.Session, save_response: requests.Response, base_url: str) -> requests.Response:
    task_no = extract_task_no(save_response)
    print(f"confirmed_task_no={task_no}")
    return submit_task(session, task_no, base_url)


def coupon_send(discount: bool, file_path: Path, env: str, base_url: str) -> Dict[str, requests.Response]:
    session = requests.Session()
    session.headers.update({
        "Authorization": BASIC_AUTH,
        "Content-Type": "application/json",
    })

    login(session, env, base_url)

    payload = build_save_payload(file_path, env, discount)
    print(f"file_path={file_path}")
    print(f"discount={discount}")
    print(f"taskName={payload['taskName']}, couponCode={payload['couponCode']}")
    print(f"byte_length={len(payload['fileBytes'])}")
    print(f"first_bytes={payload['fileBytes'][:10]}")
    print("save_request_headers=", dict(session.headers))
    print("save_request_cookies=", session.cookies.get_dict())

    save_response = session.post(f"{base_url}{SAVE_URL}", json=payload, verify=False)
    print("save_status=", save_response.status_code)
    try:
        print("save_response=")
        print(json.dumps(save_response.json(), ensure_ascii=False, indent=2))
    except ValueError:
        print("save_response_text=")
        print(save_response.text)
    save_response.raise_for_status()

    submit_response = confirm_task(session, save_response, base_url)
    return {
        "save_response": save_response,
        "submit_response": submit_response,
    }


def update_excel_and_send(user_no: str, mobile: str, discount: bool, env: str = 'BM_SIT',
                          template_path: Path = EXCEL_FILE_PATH) -> Dict[str, requests.Response]:
    temp_file_path = create_temp_excel_copy(template_path)
    base_url = get_widek_url(env)
    try:
        updated_file_path = update_excel_user_info(user_no, mobile, temp_file_path)
        return coupon_send(discount, updated_file_path, env, base_url)
    finally:
        cleanup_temp_file(temp_file_path)


if __name__ == "__main__":
    update_excel_and_send("UR1183459582182334464", "15020136158", True, env='DEV')
