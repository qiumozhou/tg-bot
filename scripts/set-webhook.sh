#!/bin/bash
# Bash 脚本：设置 Telegram Bot Webhook
# 使用方法：./scripts/set-webhook.sh YOUR_BOT_TOKEN https://your-domain.com/api/webhook

BOT_TOKEN=$1
WEBHOOK_URL=$2

if [ -z "$BOT_TOKEN" ] || [ -z "$WEBHOOK_URL" ]; then
    echo "用法: ./scripts/set-webhook.sh <BOT_TOKEN> <WEBHOOK_URL>"
    echo "示例: ./scripts/set-webhook.sh 123456:ABC-DEF https://example.com/api/webhook"
    exit 1
fi

echo "设置 Telegram Bot Webhook..."
echo "Bot Token: ${BOT_TOKEN:0:10}..."
echo "Webhook URL: $WEBHOOK_URL"
echo ""

# 设置 Webhook
RESPONSE=$(curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/setWebhook" \
  -H "Content-Type: application/json" \
  -d "{\"url\": \"$WEBHOOK_URL\"}")

echo "$RESPONSE" | jq '.'

# 检查是否成功
if echo "$RESPONSE" | jq -e '.ok == true' > /dev/null; then
    echo ""
    echo "✅ Webhook 设置成功！"
    echo ""
    
    # 验证 Webhook
    echo "验证 Webhook 信息..."
    INFO=$(curl -s "https://api.telegram.org/bot$BOT_TOKEN/getWebhookInfo")
    echo "$INFO" | jq '.'
else
    echo ""
    echo "❌ Webhook 设置失败"
    exit 1
fi

