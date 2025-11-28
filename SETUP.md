# Bot 设置指南

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件（参考 `config.example.py`），至少需要配置：

```env
BOT_TOKEN=your_telegram_bot_token
DATABASE_URL=sqlite+aiosqlite:///./data/bot.db
OFFICIAL_CHANNEL_ID=@your_official_channel
```

### 3. 运行Bot

```bash
python main.py
```

## 功能说明

### 已实现功能

- ✅ 用户注册和管理
- ✅ 积分系统
- ✅ 菜单系统
- ✅ 支付订单创建（支付宝/微信/USDT接口占位符）
- ✅ 推广链接和奖励系统
- ✅ 官方频道检查
- ✅ 图片上传接收

### 待完善功能

- ⏳ 支付接口集成（需要接入实际的支付SDK）
- ⏳ 图像/视频生成API集成（需要接入实际的生成服务）
- ⏳ 支付回调处理
- ⏳ 更多功能菜单项的实现

## 配置说明

### Bot Token

从 [@BotFather](https://t.me/BotFather) 获取你的Bot Token。

### 支付配置

支付功能目前使用占位符，需要：

1. 配置支付宝SDK（如果需要支付宝支付）
2. 配置微信支付SDK（如果需要微信支付）
3. 配置USDT支付接口（如果需要USDT支付）
4. 实现支付回调接口

### 图像生成配置

图像生成功能需要：

1. 配置图像生成API URL和密钥
2. 实现 `bot/services/image_service.py` 中的API调用逻辑

## 数据库

使用SQLite数据库（默认），数据文件存储在 `data/bot.db`。

首次运行会自动创建数据库表结构。

## 日志

日志文件存储在 `logs/bot.log`，会自动轮转和压缩。

## 注意事项

1. 确保有足够的磁盘空间存储日志和数据库
2. 生产环境建议使用PostgreSQL等专业数据库
3. 配置支付回调URL时需要确保服务器可以接收外部请求
4. 图像生成功能需要根据实际API文档进行集成

## 开发建议

1. 先完善支付接口集成
2. 然后实现图像生成API调用
3. 测试所有功能流程
4. 部署到生产环境前进行充分测试

