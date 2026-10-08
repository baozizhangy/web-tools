def print_request_payload(file_path: str) -> None:
    with open(file_path, "rb") as f:
        file_bytes = f.read()

    payload = {
        "fileBytes": list(file_bytes),
    }

    print(f"byte_length={len(file_bytes)}")
    print(payload)


if __name__ == "__main__":
    file_path = r"/tests/interface/优惠券用户信息导入模板.xlsx"
    print_request_payload(file_path)
