import concurrent.futures
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import requests


@dataclass
class EndpointConfig:
    path: str
    method: str = "POST"
    params: Dict[str, Any] = field(default_factory=dict)
    description: str = ""


DEFAULT_BASE_URL = "https://collection.shangtoutech.com/hutta-api/"
# DEFAULT_BASE_URL = 'https://wodek-sit.shangtoutech.com/hutta-api/'
DEFAULT_ENDPOINTS = [
    # EndpointConfig(
    #     path="/api/collection/phoneList/sendSMS",
    #     method="POST",
    #     params={"templetId": 19, "phoneListId": 12010},
    #     description="发送短信（POST）"
    # )
    # ,
    EndpointConfig(
        path="/system/userMsg/query",
        method="GET",
        params={"id": "12010"},
        description="查询短信（GET）"
    )
    # ,

    # EndpointConfig(
    #     path="/test/test3",
    #     method="POST",
    #     params={"id": "12010"},
    #     description="测试接口（post）"
    # )
    # ,
    # EndpointConfig(
    #     path="/test/test4",
    #     method="POST",
    #     params={"id": "12010"},
    #     description="测试接口（post）"
    # ),
]


class DualEndpointTester:
    def __init__(
            self,
            tokens: List[str],  # 改为接收token列表
            base_url: Optional[str] = None,
            endpoints: Optional[List[EndpointConfig]] = None,
            request_interval: float = 0.0,
            timeout: int = 30,
            rate_limit_code: int = 40002,
            rate_limit_message: str = "操作频繁，稍后重试"
    ):
        self.base_url = base_url or DEFAULT_BASE_URL
        self.tokens = tokens if isinstance(tokens, list) else [tokens]  # 兼容单个token字符串
        self.endpoints = endpoints or DEFAULT_ENDPOINTS
        self.request_interval = max(0.0, request_interval)
        self.timeout = timeout
        self.rate_limit_code = rate_limit_code
        self.rate_limit_message = rate_limit_message

    def get_headers(self, token: str) -> Dict[str, str]:
        """根据token生成请求头"""
        return {
            "authorizationtoken": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def send_request(
            self,
            endpoint: EndpointConfig,
            request_id: int,
            endpoint_idx: int,
            token: str,
            token_idx: int
    ) -> Tuple[int, int, int, Dict[str, Any]]:
        """发送单个HTTP请求

        Args:
            endpoint: 接口配置
            request_id: 请求ID
            endpoint_idx: 接口索引
            token: 使用的token
            token_idx: token索引
        """
        try:
            payload = endpoint.params.copy()
            payload["_request_id"] = request_id
            payload["_endpoint_idx"] = endpoint_idx
            payload["_timestamp"] = int(time.time() * 1000)
            payload["_token_preview"] = f"...{token[-6:]}" if len(token) > 6 else token

            url = f"{self.base_url}{endpoint.path}"
            method = endpoint.method.upper()
            headers = self.get_headers(token)

            if method == "GET":
                response = requests.get(
                    url,
                    params=payload,
                    headers=headers,
                    timeout=self.timeout
                )
            else:
                response = requests.request(
                    method,
                    url,
                    json=payload,
                    headers=headers,
                    timeout=self.timeout
                )
            try:
                response_data = response.json()
                status_code = int(response_data.get('code', response.status_code))
            except ValueError:
                response_data = {"raw_response": response.text}
                status_code = response.status_code

            response_summary = {
                "body": response_data,
                "http_status": response.status_code,
                "elapsed_ms": int(response.elapsed.total_seconds() * 1000),
                "request_ts": payload["_timestamp"],
                "user_token_suffix": token[-4:] if len(token) > 4 else token,
                "token_idx": token_idx
            }

            return request_id, endpoint_idx, status_code, response_summary

        except Exception as e:
            return request_id, endpoint_idx, 0, {"error": str(e)}

    def worker(self, request_id: int) -> List[Tuple[int, int, int, dict]]:
        """工作线程函数，发送两个接口的请求"""
        results = []
        # 轮询使用token，模拟不同用户
        token_idx = request_id % len(self.tokens)
        current_token = self.tokens[token_idx]

        for idx, endpoint_config in enumerate(self.endpoints):
            # 发送请求到两个不同的接口
            result = self.send_request(
                endpoint=endpoint_config,
                request_id=request_id,
                endpoint_idx=idx,
                token=current_token,
                token_idx=token_idx
            )
            results.append(result)

            if self.request_interval:
                time.sleep(self.request_interval)
        return results

    def run_test(self, num_requests: int = 10, workers: int = 5):
        """运行并发测试

        Args:
            num_requests: 总请求数(每个worker会发送2个请求)
            workers: 并发工作线程数
        """
        print(f"开始测试: 共 {num_requests} 个worker，每个worker发送 {len(self.endpoints)} 个请求")
        print(f"总请求数: {num_requests * len(self.endpoints)}")
        print(f"并发数: {workers}")
        if self.request_interval:
            print(f"请求间隔: {self.request_interval}s (用于模拟滑动窗口)")
        print("")

        results = {
            "total": 0,
            "by_endpoint": {
                idx: {
                    "success": 0,
                    "rate_limited": 0,
                    "errors": 0,
                    "endpoint": endpoint.path,
                    "method": endpoint.method,
                    "description": endpoint.description or f"接口 {idx + 1}",
                    "latencies": []
                }
                for idx, endpoint in enumerate(self.endpoints)
            }
        }

        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            # 提交任务
            future_to_id = {
                executor.submit(self.worker, i): i
                for i in range(num_requests)
            }

            # 处理结果
            for future in concurrent.futures.as_completed(future_to_id):
                request_id = future_to_id[future]
                try:
                    # 获取worker的返回结果(包含两个接口的响应)
                    endpoint_results = future.result()

                    # 处理每个接口的响应
                    for req_id, endpoint_idx, status_code, response_data in endpoint_results:
                        results["total"] += 1
                        endpoint_key = endpoint_idx

                        if status_code == 200:
                            results["by_endpoint"][endpoint_key]["success"] += 1
                            status = "✅ 成功"
                        elif status_code == self.rate_limit_code:
                            results["by_endpoint"][endpoint_key]["rate_limited"] += 1
                            status = "⚠️  被限流"
                        else:
                            results["by_endpoint"][endpoint_key]["errors"] += 1
                            status = f"❌ 错误 {status_code}"

                        if "elapsed_ms" in response_data:
                            results["by_endpoint"][endpoint_key]["latencies"].append(response_data["elapsed_ms"])

                        request_ts = response_data.get("request_ts")
                        if request_ts:
                            dt_object = time.localtime(request_ts / 1000)
                            ms = request_ts % 1000
                            readable_ts = f"{time.strftime('%Y-%m-%d %H:%M:%S', dt_object)}.{ms:03d}"
                        else:
                            readable_ts = "N/A"

                        token_idx = response_data.get("token_idx", 0)
                        token_suffix = response_data.get("user_token_suffix", "N/A")

                        print(
                            f"请求 {req_id} - 接口{endpoint_idx + 1} {status}: "
                            f"time={readable_ts} [User {token_idx + 1} | ...{token_suffix}] "
                            f"status={response_data.get('http_status')} body={response_data.get('body')}"
                        )

                except Exception as e:
                    print(f"请求 {request_id} 异常: {str(e)}")

        # 打印摘要
        self._print_summary(results)

    def _print_summary(self, results: dict):
        """打印测试结果摘要"""
        print("\n" + "=" * 50)
        print("测试完成!")
        print("=" * 50)
        print(f"总请求数: {results['total']}")

        for idx, stats in results["by_endpoint"].items():
            success = stats["success"]
            rate_limited = stats["rate_limited"]
            errors = stats["errors"]
            total = success + rate_limited + errors

            print(f"\n接口 {idx + 1}: {stats['endpoint']}")
            print(f"  成功: {success} ({(success / total) * 100:.1f}%)" if total > 0 else "  成功: 0")
            print(f"  被限流: {rate_limited} ({(rate_limited / total) * 100:.1f}%)" if total > 0 else "  被限流: 0")
            print(f"  错误: {errors} ({(errors / total) * 100:.1f}%)" if total > 0 else "  错误: 0")


# 使用示例
if __name__ == "__main__":
    # 替换为您的token列表，支持多个用户
    TOKENS = [
        "eyJhbGciOiJSUzI1NiJ9.eyJ1c2VyTmFtZSI6InRlc3QwMDEiLCJleHAiOjE3Nzg4NDkyMDMsImxvZ2luX3VzZXJfa2V5IjoiZGYzMDM4NGMtYmViNy00NzY1LTllNzItYTg2NjQxMjFkYTYxIn0.WX3SKI0nXfxpgX3SbAdtWdiwm8T-bQL1zF5WVwzJu6fkQUoh_lU2wWQJHvBxXlfScv6M61b0Zgpo7zT-wSvqnat-FBeGDEJk-xLDQDJ8Q6lsxuomnDP2b7tDrLNqplfLadwbmVZqZz3gZxRY_kp_qwlZ4iYsp7UgkYK44F0VZNVPJKyaFxh7Ju7KuNIGFanxG4Wcppl4XlcXbK80xUmMQ-w9KciB68NXfc-gisMunY7v3QQU9h4geswg2ah8GJAegJteIcK6xZ3ujYu4tTP-GuuJjwxXOd0dEiOGcTWGl8GUuWRWgc-W9Xy7aYDs6L8drEUlUFmKgEvHr0yiHn0UpA"
    ]

    # 创建测试器实例
    tester = DualEndpointTester(TOKENS)

    # 运行测试
    # 参数说明:
    # - num_requests: 总请求数。如果有两个用户，建议设为偶数以平均分配
    # - workers: 并发worker数量
    tester.run_test(num_requests=20, workers=2)
