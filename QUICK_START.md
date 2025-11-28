# 🚀 快速开始 - Cloudflare Workers 部署

## ✅ 改造已完成

你的 Telegram Bot 已经成功改造为支持 Cloudflare Workers 部署！

### 主要改动：

1. ✅ **架构调整**
   - 从 Next.js 迁移到 Cloudflare Workers
   - 创建了 `src/index.ts` 作为 Workers 入口
   - 适配了 Cloudflare Workers 的 Request/Response API

2. ✅ **数据库迁移**
   - 从本地 SQLite 迁移到 Cloudflare D1
   - 创建了数据库迁移脚本 `migrations/schema.sql`
   - 更新了 Prisma 配置以支持 D1

3. ✅ **日志系统**
   - 移除了文件系统依赖（winston）
   - 改用 console 输出，可在 Cloudflare Dashboard 查看

4. ✅ **环境变量管理**
   - 移除了 dotenv 依赖
   - 创建了 `.dev.vars.example` 示例文件
   - 支持 Cloudflare 环境变量绑定

5. ✅ **自动化部署**
   - 配置了 GitHub Actions 自动部署流程
   - 支持推送代码自动部署到 Cloudflare

## 📝 下一步操作

### 第一步：安装依赖

```bash
npm install
```

**注意：** 需要安装新的依赖，包括：
- `@prisma/adapter-d1` - Prisma D1 适配器
- `@cloudflare/workers-types` - Cloudflare Workers 类型定义
- `wrangler` - Cloudflare CLI 工具

### 第二步：配置环境变量

#### 本地开发

```bash
# 复制环境变量示例文件
cp .dev.vars.example .dev.vars

# 编辑 .dev.vars，填入你的配置
# 必需：BOT_TOKEN
```

#### Cloudflare 生产环境

参考 `DEPLOY_WORKERS.md` 中的 "环境变量配置" 部分。

**重要：你的 Token 应该放在这三个地方（根据用途）：**

1. **本地开发** → `.dev.vars` 文件（不提交到 Git）
2. **Cloudflare 生产环境** → Cloudflare Dashboard → Workers → Settings → Variables
3. **GitHub Actions** → GitHub 仓库 → Settings → Secrets and variables → Actions

### 第三步：创建 D1 数据库

```bash
# 登录 Cloudflare
wrangler login

# 创建 D1 数据库
wrangler d1 create tg-bot-db
```

**重要：** 记下返回的 `database_id`，并更新 `wrangler.toml` 文件。

### 第四步：执行数据库迁移

```bash
# 迁移到远程数据库（生产环境）
wrangler d1 execute tg-bot-db --remote --file=./migrations/schema.sql
```

### 第五步：部署到 Cloudflare

#### 方式 A：手动部署

```bash
npm run deploy
```

#### 方式 B：GitHub Actions 自动部署

1. 在 GitHub 仓库中配置 Secrets（参考 `DEPLOY_WORKERS.md`）
2. 推送代码到 main 分支：
```bash
git add .
git commit -m "Deploy to Cloudflare Workers"
git push origin main
```

### 第六步：设置 Telegram Webhook

部署成功后，获取你的 Worker URL（类似 `https://tg-bot.your-subdomain.workers.dev`），然后设置 Webhook：

**PowerShell（Windows）：**
```powershell
$botToken = "YOUR_BOT_TOKEN"
$webhookUrl = "https://your-worker.workers.dev/webhook"
$body = @{ url = $webhookUrl } | ConvertTo-Json

Invoke-RestMethod -Uri "https://api.telegram.org/bot$botToken/setWebhook" `
  -Method Post -Body $body -ContentType "application/json"
```

**Bash（Linux/Mac）：**
```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://your-worker.workers.dev/webhook"}'
```

### 第七步：测试

1. 访问健康检查端点：
```bash
curl https://your-worker.workers.dev/health
```

2. 在 Telegram 中向你的 Bot 发送 `/start` 命令

3. 查看实时日志：
```bash
wrangler tail
```

## 📚 详细文档

- **部署指南：** `DEPLOY_WORKERS.md` - 完整的部署步骤和配置说明
- **数据库迁移：** `migrations/README.md` - D1 数据库操作指南
- **原 Cloudflare Pages 部署：** `DEPLOY_CLOUDFLARE.md` - 备用参考

## 🔍 项目结构

```
├── src/
│   └── index.ts              # Cloudflare Workers 入口
├── lib/
│   ├── prisma.ts             # 数据库连接（支持 D1）
│   ├── logger.ts             # 日志工具（无文件系统）
│   ├── config.ts             # 配置管理
│   ├── constants.ts
│   ├── helpers.ts
│   └── menu.ts
├── handlers/                 # 消息处理器
├── services/                 # 业务逻辑
├── migrations/               # D1 数据库迁移脚本
├── .github/workflows/        # GitHub Actions 配置
├── wrangler.toml             # Cloudflare Workers 配置
├── .dev.vars.example         # 环境变量示例
└── package.json              # 依赖配置（已更新）
```

## ⚠️ 注意事项

1. **依赖包变化：**
   - 移除了：`next`, `react`, `winston`, `dotenv`
   - 新增了：`@prisma/adapter-d1`, `@cloudflare/workers-types`, `wrangler`

2. **环境限制：**
   - Cloudflare Workers 免费版：100,000 请求/天
   - CPU 时间：10ms（免费）/ 50ms（付费）
   - D1 数据库：每天 500 万读取，10 万写入

3. **旧文件保留：**
   - `pages/` 目录保留供参考，可以在确认 Workers 版本正常后删除
   - `next.config.js` 可以删除

## 💡 提示

- 首次部署建议先手动部署测试，确认无误后再启用 GitHub Actions
- `.dev.vars` 文件已添加到 `.gitignore`，不会被提交
- 所有敏感信息应使用 Cloudflare 的 Secret 类型环境变量

## 🆘 遇到问题？

1. 查看 `DEPLOY_WORKERS.md` 中的 "常见问题" 部分
2. 使用 `wrangler tail` 查看实时日志
3. 检查 Cloudflare Dashboard 中的错误信息

---

**作者**: @author seven  
**时间**: @since 2025-11-28

祝你部署顺利！🎉

