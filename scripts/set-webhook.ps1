# PowerShell 脚本：设置 Telegram Bot Webhook
# 使用方法：.\scripts\set-webhook.ps1 -BotToken "YOUR_BOT_TOKEN" -WebhookUrl "https://your-domain.com/api/webhook"

param(
    [Parameter(Mandatory=$true)]
    [string]$BotToken,
    
    [Parameter(Mandatory=$true)]
    [string]$WebhookUrl
)

Write-Host "设置 Telegram Bot Webhook..." -ForegroundColor Cyan
Write-Host "Bot Token: $($BotToken.Substring(0, 10))..." -ForegroundColor Gray
Write-Host "Webhook URL: $WebhookUrl" -ForegroundColor Gray
Write-Host ""

try {
    $body = @{
        url = $WebhookUrl
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "https://api.telegram.org/bot$BotToken/setWebhook" `
        -Method Post `
        -Body $body `
        -ContentType "application/json"

    if ($response.ok) {
        Write-Host "✅ Webhook 设置成功！" -ForegroundColor Green
        Write-Host ""
        
        # 验证 Webhook
        Write-Host "验证 Webhook 信息..." -ForegroundColor Cyan
        $info = Invoke-RestMethod -Uri "https://api.telegram.org/bot$BotToken/getWebhookInfo"
        
        Write-Host "Webhook URL: $($info.result.url)" -ForegroundColor Yellow
        Write-Host "待处理更新数: $($info.result.pending_update_count)" -ForegroundColor Yellow
        Write-Host "自定义证书: $($info.result.has_custom_certificate)" -ForegroundColor Yellow
        
        if ($info.result.url -eq $WebhookUrl) {
            Write-Host ""
            Write-Host "✅ Webhook 验证成功！" -ForegroundColor Green
        } else {
            Write-Host ""
            Write-Host "⚠️ 警告：Webhook URL 不匹配" -ForegroundColor Yellow
        }
    } else {
        Write-Host "❌ Webhook 设置失败：" -ForegroundColor Red
        Write-Host $response | ConvertTo-Json -Depth 10
    }
} catch {
    Write-Host "❌ 错误：$($_.Exception.Message)" -ForegroundColor Red
    Write-Host $_.Exception | Format-List -Force
    exit 1
}

