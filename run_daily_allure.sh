#!/usr/bin/env bash
set -euo pipefail

# ===== 1) 切换到项目目录（脚本所在目录） =====
cd "$(cd "$(dirname "$0")" && pwd)"

# ===== 2) 配置环境变量（按需替换） =====
export TEST_ENV=local
export WECHAT_WEBHOOK_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=2cbcecaf-53aa-4367-aba5-1aac2005222d"
export ALLURE_REPORT_URL="http://web-tools.shangtoutech.com/allure/index.html"
export RUN_MARK=""

# 如系统找不到allure命令，可配置绝对路径（取消下一行注释并修改）
# export ALLURE_BIN="/usr/local/bin/allure"

# ===== 3) 执行一次：pytest -> 生成报告 -> 推送企业微信 =====
python ./utils/allure_report_util.py

echo "[OK] daily pytest/allure/wechat finished."
