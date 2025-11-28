# 项目结构说明

## 目录结构

```
tg-bot/
├── main.py                      # 主程序入口
├── requirements.txt             # Python依赖包
├── config.example.py            # 配置文件示例
├── README.md                    # 项目说明文档
├── SETUP.md                     # 设置指南
├── .gitignore                   # Git忽略文件
│
├── bot/                         # Bot核心代码包
│   ├── __init__.py
│   │
│   ├── models/                  # 数据库模型
│   │   ├── __init__.py
│   │   ├── base.py             # 基础模型
│   │   ├── user.py             # 用户模型
│   │   ├── order.py            # 订单模型
│   │   ├── payment.py          # 支付模型
│   │   └── transaction.py      # 交易记录模型
│   │
│   ├── services/                # 业务逻辑服务
│   │   ├── __init__.py
│   │   ├── user_service.py     # 用户服务
│   │   ├── order_service.py    # 订单服务
│   │   ├── payment_service.py  # 支付服务
│   │   ├── payment_api.py      # 支付API接口
│   │   ├── channel_service.py  # 频道检查服务
│   │   ├── referral_service.py # 推广服务
│   │   └── image_service.py    # 图像生成服务
│   │
│   ├── handlers/                # 消息处理器
│   │   ├── __init__.py
│   │   ├── start.py            # /start 命令处理器
│   │   ├── callback.py         # 回调查询处理器
│   │   ├── message.py          # 消息处理器
│   │   └── menu.py             # 菜单定义
│   │
│   └── utils/                   # 工具函数
│       ├── __init__.py
│       ├── logger.py           # 日志配置
│       ├── database.py         # 数据库工具
│       └── helpers.py          # 辅助函数
│
├── data/                        # 数据目录（数据库文件）
└── logs/                        # 日志目录
```

## 核心模块说明

### 1. 数据库模型 (bot/models/)

- **User**: 用户信息、积分、等级、推广码等
- **Order**: 订单信息（图片/视频生成订单）
- **Payment**: 支付订单信息
- **Transaction**: 积分变动交易记录

### 2. 服务层 (bot/services/)

- **UserService**: 用户创建、查询、积分管理
- **OrderService**: 订单创建和管理
- **PaymentService**: 支付订单创建和管理
- **PaymentAPI**: 支付接口调用（支付宝/微信/USDT）
- **ChannelService**: 官方频道关注检查
- **ReferralService**: 推广链接和奖励处理
- **ImageGenerationService**: 图像/视频生成API调用

### 3. 处理器 (bot/handlers/)

- **start.py**: 处理 /start 命令，显示免责声明和主菜单
- **callback.py**: 处理所有按钮回调查询
- **message.py**: 处理用户发送的图片和文本消息
- **menu.py**: 定义所有菜单和按钮布局

### 4. 工具类 (bot/utils/)

- **logger.py**: 日志系统配置
- **database.py**: 数据库连接和会话管理
- **helpers.py**: 通用辅助函数（订单号生成、推广码生成等）

## 主要功能流程

### 用户注册流程

1. 用户发送 `/start` 命令
2. 系统创建或更新用户信息
3. 检查是否有推广码参数
4. 如有推广码，处理推广奖励
5. 显示免责声明和主菜单

### 积分充值流程

1. 用户点击"获积分" -> "充值获积分"
2. 选择积分套餐
3. 选择支付方式（支付宝/微信/USDT）
4. 创建支付订单
5. 生成支付链接
6. 用户支付后（需要实现回调接口），自动充值积分

### 图片生成流程

1. 用户选择功能（如"图片脱衣"）
2. 检查是否关注官方频道
3. 检查用户积分是否足够
4. 用户上传图片
5. 扣除积分，创建订单
6. 调用图像生成API（待实现）
7. 返回生成结果

### 推广奖励流程

1. 用户A通过推广链接使用Bot
2. 系统检测推广码
3. 查询推广人信息
4. 判断是新用户还是老用户
5. 计算奖励积分（新用户40积分，老用户10积分）
6. 检查每日推广积分上限（100积分）
7. 发放奖励并记录交易

## 待完善功能

1. **支付接口集成**
   - 接入支付宝SDK
   - 接入微信支付SDK
   - 接入USDT支付接口
   - 实现支付回调处理

2. **图像生成API集成**
   - 实现图像生成API调用
   - 实现视频生成API调用
   - 处理生成结果并返回给用户

3. **其他功能菜单**
   - 胸部爱抚
   - 自慰
   - 颜射
   - 口交
   - 手交
   - 性交

## 配置要求

### 必需配置

- `BOT_TOKEN`: Telegram Bot Token
- `DATABASE_URL`: 数据库连接URL
- `OFFICIAL_CHANNEL_ID`: 官方频道ID

### 可选配置

- 支付相关配置（如果启用支付功能）
- 图像生成API配置（如果启用生成功能）
- 日志配置

## 数据库设计

所有模型都继承自 `BaseModel`，包含以下通用字段：
- `id`: 主键
- `created_at`: 创建时间
- `updated_at`: 更新时间

具体字段请参考各模型文件。

