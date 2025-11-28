# NSFW Telegram Bot

一款功能强大的Telegram机器人，支持图像和视频生成功能。

## 功能特性

- 图像生成（脱衣、换脸等）
- 视频生成（多种场景）
- 积分系统
- 支付系统（支付宝、微信、USDT）
- 用户等级系统
- 分享获积分功能
- 官方频道检查

## 技术栈

- **框架**: Next.js 14
- **语言**: TypeScript
- **数据库**: SQLite (Prisma ORM)
- **Bot SDK**: node-telegram-bot-api
- **日志**: Winston

## 安装步骤

1. 克隆项目
```bash
git clone <repository-url>
cd tg-bot
```

2. 安装依赖
```bash
npm install
# 或
yarn install
```

3. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的配置信息
```

4. 初始化数据库
```bash
npm run db:push
# 或
npx prisma db push
```

5. 运行开发服务器
```bash
npm run dev
```

6. 设置 Webhook（可选）
如果使用 Webhook 模式，需要将 Telegram Bot 的 Webhook 设置为：
```
https://your-domain.com/api/webhook
```

## 本地开发（推荐）

使用 Polling 模式进行本地开发，无需设置 Webhook：

```bash
npm run bot:dev
```

## 项目结构

```
tg-bot/
├── pages/
│   └── api/
│       ├── webhook.ts          # Telegram Webhook API 端点
│       └── polling.ts          # Polling 模式实现
├── lib/                        # 工具库
│   ├── prisma.ts              # Prisma 客户端
│   ├── logger.ts              # 日志配置
│   ├── config.ts              # 配置管理
│   ├── helpers.ts             # 辅助函数
│   ├── menu.ts                # 菜单定义
│   └── constants.ts            # 常量定义
├── services/                   # 业务逻辑服务
│   ├── userService.ts         # 用户服务
│   ├── orderService.ts        # 订单服务
│   ├── paymentService.ts      # 支付服务
│   ├── paymentApi.ts          # 支付 API 接口
│   ├── referralService.ts     # 推广服务
│   └── channelService.ts      # 频道服务
├── handlers/                   # 消息处理器
│   ├── startHandler.ts        # /start 命令处理器
│   ├── callbackHandler.ts     # 回调查询处理器
│   └── messageHandler.ts      # 消息处理器
├── scripts/                    # 脚本文件
│   └── start-polling.ts       # Polling 模式启动脚本
├── prisma/
│   └── schema.prisma          # Prisma 数据库模型
├── data/                      # 数据目录（数据库等）
├── logs/                      # 日志目录
├── .next/                     # Next.js 构建输出目录（构建后生成）
├── package.json               # 依赖包
├── tsconfig.json              # TypeScript 配置
├── next.config.js             # Next.js 配置
└── README.md                  # 说明文档
```

## 配置说明

环境变量配置请参考 `.env.example` 文件。主要配置项包括：

- `BOT_TOKEN`: Telegram Bot Token
- `DATABASE_URL`: 数据库连接字符串
- 支付相关配置（支付宝、微信、USDT）
- 官方频道 ID
- 图像/视频生成 API 配置
- `PROXY_URL`: 代理配置（如果需要）

## 数据库管理

### 生成 Prisma Client
```bash
npm run db:generate
```

### 推送数据库变更
```bash
npm run db:push
```

### 创建迁移
```bash
npm run db:migrate
```

### 打开 Prisma Studio
```bash
npm run db:studio
```

## 开发说明

- 所有方法都添加了详细的注释说明
- 每个执行步骤都记录对应的日志信息
- 处理异常时向外抛出，避免随意捕获并吞没异常
- 调用外部请求发生错误时，错误日志包含请求URL、请求参数以及异常响应内容

## 注意事项

- 生成1张图像消耗：5积分
- 生成1段视频消耗：20积分
- 使用前需要关注官方频道

## 构建和部署

### 构建生产版本

```bash
npm run build
```

构建后的文件位于：
- **`.next/`** - Next.js 构建输出目录
  - `.next/server/` - 服务端代码
  - `.next/static/` - 静态资源
  - `.next/BUILD_ID` - 构建ID

### 启动生产服务器

```bash
npm start
```

### 部署到 Cloudflare Pages

详细部署指南请参考 [DEPLOY_CLOUDFLARE.md](./DEPLOY_CLOUDFLARE.md)

**快速部署步骤：**

1. **准备数据库**
   - 使用 Cloudflare D1 或外部数据库服务（Supabase、PlanetScale 等）
   - SQLite 文件数据库在 Cloudflare Pages 中无法使用

2. **通过 Cloudflare Dashboard 部署**
   - 登录 https://dash.cloudflare.com
   - 进入 Pages → Create a project
   - 连接 Git 仓库
   - 配置构建设置：
     - Framework: Next.js
     - Build command: `npm run build`
     - Build output directory: `.next`
   - 添加所有环境变量

3. **设置 Webhook**
   
   **Windows PowerShell:**
   ```powershell
   .\scripts\set-webhook.ps1 -BotToken "YOUR_BOT_TOKEN" -WebhookUrl "https://your-project.pages.dev/api/webhook"
   ```
   
   **Linux/Mac:**
   ```bash
   chmod +x scripts/set-webhook.sh
   ./scripts/set-webhook.sh YOUR_BOT_TOKEN https://your-project.pages.dev/api/webhook
   ```
   
   **或使用 curl (Windows CMD):**
   ```cmd
   curl -X POST "https://api.telegram.org/bot<BOT_TOKEN>/setWebhook" -H "Content-Type: application/json" -d "{\"url\": \"https://your-project.pages.dev/api/webhook\"}"
   ```

4. **使用 CLI 部署（可选）**
   ```bash
   npm install -g wrangler
   wrangler login
   npm run deploy:cf
   ```

**⚠️ 重要提示：**
- Cloudflare Pages 不支持本地文件系统
- 需要将 SQLite 迁移到 Cloudflare D1 或外部数据库
- 日志需要使用 Cloudflare Workers Logs 或外部服务

## 构建输出说明

运行 `npm run build` 后，构建文件会生成在以下位置：

- **`.next/`** - Next.js 构建输出目录（主要构建文件）
  - 包含编译后的 JavaScript 代码
  - 优化的静态资源
  - 服务端渲染文件

- **`node_modules/.prisma/`** - Prisma Client 生成的文件

构建后的项目可以直接使用 `npm start` 启动生产服务器。

## 作者

@author seven

@since 2024
