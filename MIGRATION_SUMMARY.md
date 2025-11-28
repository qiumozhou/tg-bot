# ✨ Cloudflare Workers 改造总结

## 📊 改造概览

将 Telegram Bot 从 **Next.js + SQLite** 架构成功迁移到 **Cloudflare Workers + D1** 架构。

**改造时间：** 2025-11-28  
**改造作者：** @author seven

---

## 🎯 核心改动

### 1️⃣ 新建文件

| 文件路径 | 说明 |
|---------|------|
| `src/index.ts` | Cloudflare Workers 主入口文件 |
| `migrations/schema.sql` | D1 数据库迁移脚本（包含所有表结构） |
| `migrations/README.md` | D1 数据库操作指南 |
| `.dev.vars.example` | 环境变量配置示例（本地开发用） |
| `.github/workflows/deploy.yml` | GitHub Actions 自动化部署流程 |
| `DEPLOY_WORKERS.md` | 完整的部署指南文档 |
| `QUICK_START.md` | 快速开始指南 |
| 本文件 | 改造总结文档 |

### 2️⃣ 修改文件

| 文件路径 | 主要变更 |
|---------|---------|
| `wrangler.toml` | 从 Pages 配置改为 Workers 配置，添加 D1 绑定 |
| `package.json` | 更新依赖和脚本，移除 Next.js 相关，添加 Workers 工具 |
| `tsconfig.json` | 适配 Cloudflare Workers 环境，添加类型定义 |
| `lib/prisma.ts` | 支持 D1 数据库适配器，保持向后兼容 |
| `lib/logger.ts` | 移除文件系统依赖，改用 console 输出 |
| `lib/config.ts` | 移除 dotenv，直接使用环境变量 |

### 3️⃣ 可以删除的文件（已确认 Workers 版本正常后）

- `pages/` 目录 - Next.js API Routes
- `next.config.js` - Next.js 配置
- `next-env.d.ts` - Next.js 类型定义

---

## 🔄 依赖包变更

### ❌ 移除的依赖

```json
{
  "next": "^14.1.0",           // Next.js 框架
  "react": "^18.2.0",          // React（不需要）
  "react-dom": "^18.2.0",      // React DOM
  "winston": "^3.11.0",        // 文件日志库
  "dotenv": "^16.4.1",         // 环境变量加载
  "eslint-config-next": "^14.1.0"  // Next.js ESLint 配置
}
```

### ✅ 新增的依赖

```json
{
  "@prisma/adapter-d1": "^5.9.0",      // Prisma D1 适配器
  "@cloudflare/workers-types": "^4.20231218.0",  // Workers 类型定义
  "wrangler": "^3.22.0"                 // Cloudflare CLI 工具
}
```

### 🔧 保留的依赖

```json
{
  "@prisma/client": "^5.9.0",
  "axios": "^1.6.5",
  "node-telegram-bot-api": "^0.64.0",
  "prisma": "^5.9.0",
  "typescript": "^5.3.3"
}
```

---

## 🗂️ 架构对比

### Before（Next.js + SQLite）

```
Next.js Application
├── API Routes (pages/api/)
│   ├── webhook.ts        → 处理 Telegram Webhook
│   └── polling.ts        → 轮询模式（不推荐）
├── SQLite Database       → 本地文件数据库
├── Winston Logger        → 写入日志文件
└── dotenv                → 从 .env 加载配置
```

**限制：**
- 需要服务器持续运行
- SQLite 文件存储有限
- 日志文件管理复杂
- 扩展性差

### After（Cloudflare Workers + D1）

```
Cloudflare Workers
├── Workers Entry (src/index.ts)
│   └── Webhook Handler   → 直接处理 HTTP 请求
├── D1 Database           → Cloudflare 管理的 SQLite
├── Console Logger        → 输出到 Cloudflare Logs
└── Environment Variables → Cloudflare 绑定
```

**优势：**
- 无服务器，按需计费
- 全球 CDN 加速
- 自动扩展
- 免费层额度充足
- 零运维成本

---

## 🔐 环境变量配置指南

### 配置位置

| 环境 | 配置方式 | 文件/位置 |
|------|---------|----------|
| **本地开发** | `.dev.vars` 文件 | 根目录（不提交到 Git） |
| **Cloudflare 生产** | Dashboard 配置 | Workers → Settings → Variables |
| **GitHub Actions** | Repository Secrets | Settings → Secrets and variables |

### 必需变量

```bash
BOT_TOKEN=你的Telegram_Bot_Token  # 必需！
```

### 可选变量

```bash
# 支付配置
ALIPAY_APP_ID=...
ALIPAY_PRIVATE_KEY=...
ALIPAY_PUBLIC_KEY=...
WECHAT_APP_ID=...
WECHAT_MCH_ID=...
WECHAT_API_KEY=...
USTD_API_KEY=...

# 功能配置
OFFICIAL_CHANNEL_ID=@your_channel
IMAGE_GENERATION_API_URL=...
IMAGE_GENERATION_API_KEY=...
VIDEO_GENERATION_API_URL=...
VIDEO_GENERATION_API_KEY=...

# 系统配置
WEBHOOK_URL=https://your-worker.workers.dev
LOG_LEVEL=INFO
NODE_ENV=production
```

---

## 📋 部署检查清单

### 部署前

- [ ] 安装所有依赖：`npm install`
- [ ] 登录 Cloudflare：`wrangler login`
- [ ] 创建 D1 数据库：`wrangler d1 create tg-bot-db`
- [ ] 更新 `wrangler.toml` 中的 `database_id`
- [ ] 执行数据库迁移：`wrangler d1 execute tg-bot-db --remote --file=./migrations/schema.sql`
- [ ] 配置本地 `.dev.vars` 文件（用于测试）
- [ ] 在 Cloudflare Dashboard 配置环境变量

### 部署

- [ ] 手动部署测试：`npm run deploy`
- [ ] 验证 Worker URL 可访问：`curl https://your-worker.workers.dev/health`
- [ ] 设置 Telegram Webhook
- [ ] 验证 Webhook 状态：`curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo`

### 部署后

- [ ] 在 Telegram 中测试 `/start` 命令
- [ ] 测试菜单功能
- [ ] 测试支付功能（如有）
- [ ] 测试图片/视频处理功能（如有）
- [ ] 检查 Cloudflare Dashboard 日志
- [ ] 配置 GitHub Actions（如需自动部署）

---

## 🚀 部署命令速查

### 本地开发

```bash
# 启动本地开发服务器
npm run dev

# 查看实时日志
wrangler tail
```

### 数据库操作

```bash
# 创建数据库
wrangler d1 create tg-bot-db

# 执行迁移（远程）
wrangler d1 execute tg-bot-db --remote --file=./migrations/schema.sql

# 查询数据库
wrangler d1 execute tg-bot-db --remote --command="SELECT * FROM users LIMIT 5"

# 数据库信息
wrangler d1 info tg-bot-db
```

### 部署

```bash
# 构建项目
npm run build

# 部署到 Cloudflare
npm run deploy

# 或使用 wrangler 直接部署
wrangler deploy
```

### Telegram Webhook

```bash
# 设置 Webhook（PowerShell）
$botToken = "YOUR_TOKEN"
$webhookUrl = "https://your-worker.workers.dev/webhook"
Invoke-RestMethod -Uri "https://api.telegram.org/bot$botToken/setWebhook" -Method Post -Body (@{url=$webhookUrl} | ConvertTo-Json) -ContentType "application/json"

# 获取 Webhook 信息
curl "https://api.telegram.org/bot<YOUR_TOKEN>/getWebhookInfo"

# 删除 Webhook
curl -X POST "https://api.telegram.org/bot<YOUR_TOKEN>/deleteWebhook"
```

---

## 💰 Cloudflare 免费层配额

| 资源 | 免费层限制 | 付费后限制 |
|------|-----------|-----------|
| **Workers 请求** | 100,000 次/天 | 10M 次/月起 |
| **CPU 时间** | 10ms/请求 | 50ms/请求 |
| **D1 读取** | 5,000,000 次/天 | 无限 |
| **D1 写入** | 100,000 次/天 | 无限 |
| **D1 存储** | 5 GB | 无限 |

**对于中小型 Bot，免费层完全够用！**

---

## 📈 性能对比

| 指标 | Next.js 部署 | Cloudflare Workers |
|------|-------------|-------------------|
| **冷启动** | ~2-5秒 | ~5-10ms |
| **响应时间** | 50-200ms | 10-50ms |
| **全球访问** | 单区域 | 300+ 数据中心 |
| **扩展性** | 手动扩展 | 自动无限扩展 |
| **运维成本** | 需要管理服务器 | 零运维 |
| **费用** | 固定月费 | 按使用量付费 |

---

## 🔧 故障排查

### 常见问题

**Q: 部署后 Bot 无响应？**
- 检查 Webhook 是否设置成功
- 查看 Cloudflare Dashboard 日志
- 确认 BOT_TOKEN 环境变量已配置

**Q: 数据库连接失败？**
- 确认 D1 数据库已创建
- 检查 `wrangler.toml` 中的 `database_id`
- 确认数据库迁移已执行

**Q: TypeScript 类型错误？**
- 运行 `npm install` 安装所有依赖
- 确认 `@cloudflare/workers-types` 已安装

**Q: GitHub Actions 部署失败？**
- 检查 GitHub Secrets 是否配置正确
- 确认 `CLOUDFLARE_API_TOKEN` 权限足够

---

## 📚 相关文档

- **[QUICK_START.md](QUICK_START.md)** - 快速开始指南
- **[DEPLOY_WORKERS.md](DEPLOY_WORKERS.md)** - 详细部署文档
- **[migrations/README.md](migrations/README.md)** - 数据库操作指南
- **[Cloudflare Workers 文档](https://developers.cloudflare.com/workers/)**
- **[Cloudflare D1 文档](https://developers.cloudflare.com/d1/)**

---

## ✅ 完成状态

- ✅ 项目架构迁移完成
- ✅ 数据库适配完成
- ✅ 日志系统适配完成
- ✅ 环境变量管理配置完成
- ✅ GitHub Actions 配置完成
- ✅ 文档编写完成
- ⏳ 等待部署测试

---

**下一步：按照 QUICK_START.md 开始部署！**

祝你部署顺利！🎉

---

**作者**: @author seven  
**日期**: 2025-11-28

