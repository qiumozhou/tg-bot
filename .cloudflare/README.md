# Cloudflare 部署指南

## 部署方式

### 方式一：Cloudflare Pages（推荐）

Cloudflare Pages 支持 Next.js 应用，但需要注意以下限制：

1. **数据库问题**：SQLite 文件数据库在 Cloudflare Pages 中无法使用
   - 解决方案：使用 Cloudflare D1（SQLite 兼容）或外部数据库服务

2. **文件系统限制**：无法写入本地文件系统
   - 日志文件需要使用外部服务或 Cloudflare Workers Logs

### 方式二：Cloudflare Workers

使用 `@cloudflare/next-on-pages` 适配器将 Next.js 转换为 Workers 兼容格式。

## 部署步骤

### 使用 Cloudflare Pages

1. **登录 Cloudflare Dashboard**
   - 访问 https://dash.cloudflare.com
   - 进入 "Pages" 部分

2. **创建新项目**
   - 点击 "Create a project"
   - 连接你的 Git 仓库（GitHub/GitLab）

3. **配置构建设置**
   - **Framework preset**: Next.js
   - **Build command**: `npm run build`
   - **Build output directory**: `.next`
   - **Root directory**: `/` (项目根目录)

4. **设置环境变量**
   在 Cloudflare Pages 项目设置中添加以下环境变量：
   ```
   BOT_TOKEN=your-telegram-bot-token
   DATABASE_URL=your-database-url
   ALIPAY_APP_ID=your-alipay-app-id
   ALIPAY_PRIVATE_KEY=your-alipay-private-key
   ALIPAY_PUBLIC_KEY=your-alipay-public-key
   ALIPAY_NOTIFY_URL=your-alipay-notify-url
   WECHAT_APP_ID=your-wechat-app-id
   WECHAT_MCH_ID=your-wechat-mch-id
   WECHAT_API_KEY=your-wechat-api-key
   WECHAT_NOTIFY_URL=your-wechat-notify-url
   USTD_API_KEY=your-usdt-api-key
   USTD_NOTIFY_URL=your-usdt-notify-url
   OFFICIAL_CHANNEL_ID=your-official-channel-id
   IMAGE_GENERATION_API_URL=your-image-api-url
   IMAGE_GENERATION_API_KEY=your-image-api-key
   VIDEO_GENERATION_API_URL=your-video-api-url
   VIDEO_GENERATION_API_KEY=your-video-api-key
   WEBHOOK_URL=https://your-project.pages.dev/api/webhook
   PROXY_URL=your-proxy-url (可选)
   ```

5. **部署**
   - 保存设置后，Cloudflare 会自动构建并部署
   - 部署完成后，你会获得一个 `*.pages.dev` 域名

6. **设置 Telegram Webhook**
   ```bash
   curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
     -d "url=https://your-project.pages.dev/api/webhook"
   ```

## 数据库迁移到 Cloudflare D1

由于 Cloudflare Pages 不支持本地文件系统，建议使用 Cloudflare D1：

1. **创建 D1 数据库**
   ```bash
   wrangler d1 create tg-bot-db
   ```

2. **更新 Prisma Schema**
   修改 `prisma/schema.prisma` 中的 `datasource`：
   ```prisma
   datasource db {
     provider = "sqlite"
     url      = env("DATABASE_URL")
   }
   ```

3. **迁移数据库**
   ```bash
   npx prisma migrate deploy
   ```

## 注意事项

- Cloudflare Pages 有 10 秒的执行时间限制（免费版）
- 对于长时间运行的任务，考虑使用 Cloudflare Workers
- 日志需要使用 Cloudflare Workers Logs 或外部日志服务
- 文件上传需要使用 Cloudflare R2 或其他存储服务

## 故障排除

如果遇到问题：
1. 检查 Cloudflare Pages 构建日志
2. 确认所有环境变量已正确设置
3. 验证 Webhook URL 是否可访问
4. 检查数据库连接配置

