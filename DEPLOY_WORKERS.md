# Cloudflare Workers 部署指南

本文档详细说明如何将 Telegram Bot 部署到 Cloudflare Workers。

## 📋 准备工作

### 1. 安装依赖

```bash
npm install
```

### 2. 安装 Wrangler CLI（如果尚未安装）

```bash
npm install -g wrangler
```

### 3. 登录 Cloudflare

```bash
wrangler login
```

这将打开浏览器，让你登录 Cloudflare 账户。

## 🗄️ 数据库设置

### 创建 D1 数据库

```bash
npm run db:d1-create
```

或直接使用：

```bash
wrangler d1 create tg-bot-db
```

**重要：** 记下返回的 `database_id`，并更新 `wrangler.toml` 文件中的配置。

### 执行数据库迁移

**本地测试（可选）：**

```bash
npm run db:d1-migrate-local
```

**生产环境（必需）：**

```bash
npm run db:d1-migrate-remote
```

### 验证数据库

```bash
wrangler d1 execute tg-bot-db --remote --command="SELECT name FROM sqlite_master WHERE type='table'"
```

应该看到 4 个表：`users`, `orders`, `payments`, `transactions`

## 🔐 环境变量配置

### 方式一：Cloudflare Dashboard（推荐用于生产环境）

1. 访问 https://dash.cloudflare.com
2. 进入 **Workers & Pages**
3. 选择你的 Worker（部署后会自动创建）
4. 进入 **Settings → Variables**
5. 添加以下环境变量（敏感信息选择 "Secret" 类型）：

**必需变量：**
```
BOT_TOKEN=你的Telegram Bot Token（Secret）
```

**支付配置（如需使用）：**
```
ALIPAY_APP_ID=支付宝配置
ALIPAY_PRIVATE_KEY=支付宝私钥（Secret）
ALIPAY_PUBLIC_KEY=支付宝公钥
ALIPAY_NOTIFY_URL=https://your-worker.workers.dev/api/notify/alipay

WECHAT_APP_ID=微信配置
WECHAT_MCH_ID=微信商户号
WECHAT_API_KEY=微信支付密钥（Secret）
WECHAT_NOTIFY_URL=https://your-worker.workers.dev/api/notify/wechat

USTD_API_KEY=USDT API密钥（Secret）
USTD_NOTIFY_URL=https://your-worker.workers.dev/api/notify/usdt
```

**其他配置：**
```
OFFICIAL_CHANNEL_ID=@your_channel_name
IMAGE_GENERATION_API_URL=https://your-image-api.com
IMAGE_GENERATION_API_KEY=your_key（Secret）
VIDEO_GENERATION_API_URL=https://your-video-api.com
VIDEO_GENERATION_API_KEY=your_key（Secret）
WEBHOOK_URL=https://your-worker.workers.dev
LOG_LEVEL=INFO
```

### 方式二：本地开发（.dev.vars）

1. 复制示例文件：
```bash
cp .dev.vars.example .dev.vars
```

2. 编辑 `.dev.vars` 填入你的配置

3. 本地测试：
```bash
npm run dev
```

### 方式三：GitHub Secrets（用于 CI/CD）

在 GitHub 仓库设置中配置：

1. 进入仓库 **Settings → Secrets and variables → Actions**
2. 添加以下 Repository secrets：

**Cloudflare 部署凭证（必需）：**
```
CLOUDFLARE_API_TOKEN=你的Cloudflare API Token
CLOUDFLARE_ACCOUNT_ID=你的Cloudflare Account ID
```

**获取 API Token：**
- 访问 https://dash.cloudflare.com/profile/api-tokens
- 创建新 Token，选择 "Edit Cloudflare Workers" 模板
- 复制生成的 Token

**获取 Account ID：**
- 访问 https://dash.cloudflare.com
- 点击任意 Worker
- 在右侧可以看到 Account ID

**所有应用环境变量：**
添加上述所有环境变量作为 GitHub Secrets。

## 🚀 部署

### 方式一：手动部署

```bash
npm run deploy
```

或

```bash
wrangler deploy
```

### 方式二：GitHub Actions 自动部署

1. 确保已配置 GitHub Secrets
2. 推送代码到 `main` 分支：

```bash
git add .
git commit -m "Deploy to Cloudflare Workers"
git push origin main
```

3. GitHub Actions 会自动：
   - 构建项目
   - 部署到 Cloudflare Workers
   - 设置 Telegram Webhook
   - 验证部署状态

## 🔗 设置 Telegram Webhook

部署成功后，需要设置 Telegram Webhook。

### 自动设置（推荐）

如果使用 GitHub Actions，Webhook 会自动设置。

### 手动设置

**Windows PowerShell：**

```powershell
$botToken = "YOUR_BOT_TOKEN"
$webhookUrl = "https://your-worker.workers.dev/webhook"
$body = @{ url = $webhookUrl } | ConvertTo-Json

Invoke-RestMethod -Uri "https://api.telegram.org/bot$botToken/setWebhook" `
  -Method Post -Body $body -ContentType "application/json"
```

**Linux/Mac：**

```bash
BOT_TOKEN="YOUR_BOT_TOKEN"
WEBHOOK_URL="https://your-worker.workers.dev/webhook"

curl -X POST "https://api.telegram.org/bot${BOT_TOKEN}/setWebhook" \
  -H "Content-Type: application/json" \
  -d "{\"url\": \"${WEBHOOK_URL}\"}"
```

### 验证 Webhook

```bash
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"
```

## ✅ 测试部署

### 1. 健康检查

```bash
curl https://your-worker.workers.dev/health
```

应返回：
```json
{
  "status": "ok",
  "timestamp": "2024-11-28T...",
  "service": "tg-bot-worker"
}
```

### 2. 测试 Bot

在 Telegram 中向你的 Bot 发送：
- `/start` - 测试启动命令
- 测试菜单功能
- 测试图片上传等

### 3. 查看日志

**实时日志：**

```bash
npm run cf:tail
```

或

```bash
wrangler tail
```

**Cloudflare Dashboard：**
- 访问 https://dash.cloudflare.com
- 进入你的 Worker
- 查看 **Logs** 标签

## 🔧 常见问题

### 1. 部署失败

**检查：**
- Wrangler 是否已登录：`wrangler whoami`
- `wrangler.toml` 配置是否正确
- 网络连接是否正常

### 2. Webhook 设置失败

**检查：**
- BOT_TOKEN 是否正确
- Worker URL 是否可访问
- Webhook URL 必须是 HTTPS

### 3. 数据库连接失败

**检查：**
- D1 数据库是否已创建
- `wrangler.toml` 中的 `database_id` 是否正确
- 数据库迁移是否已执行

### 4. 环境变量未生效

**Cloudflare Dashboard 设置优先级最高**
- 在 Dashboard 中设置的变量会覆盖其他方式
- 修改后需要重新部署

### 5. Bot 无响应

**检查：**
- Webhook 是否设置成功：`getWebhookInfo`
- Worker 是否运行正常：访问 `/health`
- 查看 Worker 日志查找错误

## 📊 监控和维护

### 查看使用情况

在 Cloudflare Dashboard 中可以看到：
- 请求数量
- 错误率
- CPU 使用时间
- 数据库读写次数

### 更新部署

修改代码后重新部署：

```bash
npm run deploy
```

或推送到 GitHub（如果配置了 Actions）

### 回滚部署

在 Cloudflare Dashboard 中可以回滚到之前的版本：
1. 进入 Worker
2. 查看 **Deployments** 历史
3. 选择要回滚的版本

## 🎉 完成！

恭喜！你的 Telegram Bot 现在已经运行在 Cloudflare Workers 上了！

**接下来：**
- 测试所有功能
- 监控性能和错误
- 根据需要调整配置

---

**作者**: @author seven  
**时间**: @since 2025-11-28

