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

## 项目结构

```
tg-bot/
├── pages/
│   └── api/
│       └── webhook.ts          # Telegram Webhook API 端点
├── lib/                        # 工具库
│   ├── prisma.ts              # Prisma 客户端
│   ├── logger.ts              # 日志配置
│   ├── config.ts              # 配置管理
│   ├── helpers.ts             # 辅助函数
│   └── menu.ts                # 菜单定义
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
├── prisma/
│   └── schema.prisma          # Prisma 数据库模型
├── data/                      # 数据目录（数据库等）
├── logs/                      # 日志目录
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

## 生产部署

1. 构建生产版本
```bash
npm run build
```

2. 启动生产服务器
```bash
npm start
```

3. 设置环境变量
确保在生产环境中设置所有必要的环境变量

4. 配置 Webhook（推荐）
使用 Webhook 模式可以提高 Bot 的响应速度和稳定性

## 作者

@author seven

@since 2024
