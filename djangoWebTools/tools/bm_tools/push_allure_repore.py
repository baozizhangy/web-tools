import requests

def push_wework_markdown(webhook, allure_report_url):
    markdown_content = f"""
## ✅ API渠道自动化回归完成
🔗 [点击查看接口自动化报告]({allure_report_url})

如有失败用例，请及时跟进修复。
"""
    payload = {
        "msgtype": "markdown",
        "markdown": {
            "content": markdown_content
        }
    }
    resp = requests.post(webhook, json=payload)
    print("企业微信推送结果:", resp.text)

if __name__ == "__main__":
    # 替换为你的机器人 Webhook 和 Allure 可访问 URL
    WEBHOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=2cbcecaf-53aa-4367-aba5-1aac2005222d"
    ALLURE_REPORT_URL = "http://0.10.10.0:8000/index.html"
    push_wework_markdown(WEBHOOK, ALLURE_REPORT_URL)
