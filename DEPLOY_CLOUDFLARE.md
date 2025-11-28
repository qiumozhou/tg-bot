# Cloudflare 部署指南

## 概述

本指南将帮助你将 Telegram Bot 部署到 Cloudflare Pages。

## ⚠️ 重要注意事项

### 数据库限制

Cloudflare Pages 是静态站点托管服务，**不支持本地文件系统**。这意味着：

1. **SQLite 文件数据库无法使用**
   - 解决方案：使用 Cloudflare D1（SQLite 兼容）或外部数据库服务（如 Supabase、PlanetScale）

2. **日志文件无法写入本地**
   - 解决方案：使用 Cloudflare Workers Logs 或外部日志服务

3. **文件上传需要外部存储**
   - 解决方案：使用 Cloudflare R2 或其他对象存储服务

## 部署步骤

### 第一步：准备数据库

#### 选项 A：使用 Cloudflare D1（推荐）

1. **安装 Wrangler CLI**
   ```bash
   npm install -g wrangler
   ```

2. **登录 Cloudflare**
   ```bash
   wrangler login
   ```

3. **创建 D1 数据库**
   ```bash
   wrangler d1 create tg-bot-db
   ```

4. **获取数据库 ID**
   创建后会显示数据库 ID，保存它

5. **更新 wrangler.toml**
   在 `wrangler.toml` 中取消注释 D1 配置：
   ```toml
   [[d1_databases]]
   binding = "DB"
   database_name = "tg-bot-db"
   database_id = "your-database-id"
   ```

6. **迁移数据库**
   ```bash
   # 首先在本地测试（可选）
   wrangler d1 execute tg-bot-db --file=./prisma/migrations/init.sql
   
   # 然后迁移到远程数据库（生产环境）- 必须使用 --remote 标志
   wrangler d1 execute tg-bot-db --remote --file=./prisma/migrations/init.sql
   ```
   
   **注意**：SQL 迁移文件已经创建在 `prisma/migrations/init.sql`，包含了所有必要的表结构。

#### 选项 B：使用外部数据库

使用 Supabase、PlanetScale 或其他 PostgreSQL/MySQL 服务：

1. 创建数据库实例
2. 更新 `DATABASE_URL` 环境变量
3. 更新 `prisma/schema.prisma` 的 `provider` 为 `postgresql` 或 `mysql`

### 第二步：配置环境变量

在 Cloudflare Pages 项目设置中添加所有必要的环境变量：

**必需变量：**
- `BOT_TOKEN` - Telegram Bot Token
- `DATABASE_URL` - 数据库连接字符串

**支付配置：**
- `ALIPAY_APP_ID`
- `ALIPAY_PRIVATE_KEY`
- `ALIPAY_PUBLIC_KEY`
- `ALIPAY_NOTIFY_URL`
- `WECHAT_APP_ID`
- `WECHAT_MCH_ID`
- `WECHAT_API_KEY`
- `WECHAT_NOTIFY_URL`
- `USTD_API_KEY`
- `USTD_NOTIFY_URL`

**其他配置：**
- `OFFICIAL_CHANNEL_ID`
- `IMAGE_GENERATION_API_URL`
- `IMAGE_GENERATION_API_KEY`
- `VIDEO_GENERATION_API_URL`
- `VIDEO_GENERATION_API_KEY`
- `WEBHOOK_URL` - 部署后的 Webhook URL
- `PROXY_URL` - （可选）代理 URL

### 第三步：部署到 Cloudflare Pages

#### 方法 1：通过 Cloudflare Dashboard（推荐）

1. **登录 Cloudflare Dashboard**
   - 访问 https://dash.cloudflare.com
   - 进入 "Pages" 部分

2. **创建新项目**
   - 点击 "Create a project"
   - 选择 "Connect to Git"
   - 连接你的 GitHub/GitLab 仓库

3. **配置构建设置**
   - **Framework preset**: Next.js
   - **Build command**: `npm run build`
   - **Build output directory**: `.next`
   - **Root directory**: `/` (项目根目录)
   - **Node version**: `20.x` (或更高)

4. **添加环境变量**
   - 在项目设置中添加所有必需的环境变量
   - 区分 Production、Preview、Development 环境

5. **部署**
   - 保存设置后，Cloudflare 会自动构建并部署
   - 首次部署可能需要几分钟

#### 方法 2：使用 Wrangler CLI

```bash
# 安装依赖
npm install

# 构建项目
npm run build

# 部署到 Cloudflare Pages
wrangler pages deploy .next
```

### 第四步：设置 Telegram Webhook

部署完成后，你会获得一个 `*.pages.dev` 域名，例如：
```
https://your-project.pages.dev
```

#### Windows CMD 设置 Webhook

```cmd
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" -H "Content-Type: application/json" -d "{\"url\": \"https://your-project.pages.dev/api/webhook\"}"
```

#### Windows PowerShell 设置 Webhook

```powershell
$botToken = "YOUR_BOT_TOKEN"
$webhookUrl = "https://your-project.pages.dev/api/webhook"
$body = @{
    url = $webhookUrl
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://api.telegram.org/bot$botToken/setWebhook" -Method Post -Body $body -ContentType "application/json"
```

#### Linux/Mac 设置 Webhook

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-project.pages.dev/api/webhook"
  }'
```

#### 验证 Webhook

**Windows CMD:**
```cmd
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"
```

**Windows PowerShell:**
```powershell
$botToken = "YOUR_BOT_TOKEN"
Invoke-RestMethod -Uri "https://api.telegram.org/bot$botToken/getWebhookInfo"
```

**Linux/Mac:**
```bash
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"
```

**预期响应示例：**
```json
{
  "ok": true,
  "result": {
    "url": "https://your-project.pages.dev/api/webhook",
    "has_custom_certificate": false,
    "pending_update_count": 0
  }
}
```

### 第五步：测试

1. 向你的 Bot 发送 `/start` 命令
2. 检查 Cloudflare Pages 的实时日志
3. 验证所有功能是否正常工作

## 代码修改建议

### 1. 数据库连接适配

如果使用 Cloudflare D1，需要修改 `lib/prisma.ts`：

```typescript
import { PrismaClient } from '@prisma/client';

// Cloudflare D1 绑定（在 Cloudflare 环境中）
declare global {
  var DB: D1Database | undefined;
}

const prismaClientSingleton = () => {
  // 在 Cloudflare 环境中使用 D1
  if (typeof globalThis.DB !== 'undefined') {
    return new PrismaClient({
      datasources: {
        db: {
          url: process.env.DATABASE_URL,
        },
      },
    });
  }
  
  // 本地开发使用标准 Prisma
  return new PrismaClient();
};
```

### 2. 日志适配

修改 `lib/logger.ts` 以支持 Cloudflare 环境：

```typescript
// 在 Cloudflare 环境中，使用 console 而不是文件日志
if (typeof process.env.CF_PAGES !== 'undefined') {
  // Cloudflare Pages 环境
  // 使用 console.log，Cloudflare 会自动收集日志
} else {
  // 本地环境，使用文件日志
}
```

## 故障排除

### 构建失败

1. 检查构建日志中的错误信息
2. 确认 Node.js 版本兼容（建议 20.x）
3. 验证所有依赖都已正确安装

### Webhook 不工作

1. **405 Method Not Allowed 错误**
   - 检查 API 路由是否正确处理 POST 请求
   - 确认 `pages/api/webhook.ts` 文件存在且正确导出
   - 验证 Cloudflare Pages 构建日志，确认 API 路由已正确构建

2. **Webhook URL 不可访问**
   - 测试 URL：`curl https://your-project.pages.dev/api/webhook`
   - 确认 Cloudflare Pages 部署成功
   - 检查域名是否正确

3. **其他问题**
   - 确认 `BOT_TOKEN` 环境变量正确
   - 检查 Cloudflare Pages 的实时日志
   - 验证 API 路由是否正确部署到 `.next/server/pages/api/webhook.js`

### 数据库连接失败

1. 确认 `DATABASE_URL` 环境变量正确
2. 检查数据库服务是否可访问
3. 验证数据库权限设置

### 超时错误

Cloudflare Pages 免费版有 10 秒执行时间限制：
- 优化代码，减少处理时间
- 对于长时间任务，考虑使用 Cloudflare Workers
- 使用异步处理和队列

## 性能优化

1. **启用缓存**
   - 在 Cloudflare Pages 设置中启用缓存
   - 使用 Cloudflare CDN 加速

2. **优化构建**
   - 减少依赖包大小
   - 使用代码分割

3. **监控**
   - 使用 Cloudflare Analytics 监控性能
   - 设置告警规则

## 相关资源

- [Cloudflare Pages 文档](https://developers.cloudflare.com/pages/)
- [Cloudflare D1 文档](https://developers.cloudflare.com/d1/)
- [Next.js on Cloudflare](https://developers.cloudflare.com/pages/framework-guides/deploy-a-nextjs-site/)
- [Wrangler CLI 文档](https://developers.cloudflare.com/workers/wrangler/)

## 支持

如果遇到问题，请检查：
1. Cloudflare Pages 构建日志
2. Cloudflare Workers Logs
3. Telegram Bot API 日志

---

**作者**: @author seven  
**时间**: @since 2024

