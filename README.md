# NSFW Telegram Bot

一款功能强大的Telegram机器人，支持图像和视频生成功能。

## 功能特性

- 图像生成（脱衣、换脸等）
- 视频生成（多种场景）
- 积分系统
- 支付系统（支付宝、微信、USTD）
- 用户等级系统
- 分享获积分功能
- 官方频道检查

## 安装步骤

1. 克隆项目
```bash
git clone <repository-url>
cd tg-bot
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的配置信息
```

4. 运行机器人
```bash
python main.py
```

## 项目结构

```
tg-bot/
├── main.py                 # 主入口文件
├── bot/                    # Bot核心代码
│   ├── __init__.py
│   ├── handlers/          # 消息处理器
│   ├── models/            # 数据库模型
│   ├── services/          # 业务逻辑服务
│   └── utils/             # 工具函数
├── data/                  # 数据目录（数据库等）
├── logs/                  # 日志目录
├── requirements.txt       # 依赖包
├── .env.example          # 环境变量示例
└── README.md             # 说明文档
```

## 配置说明

详见 `.env.example` 文件中的注释。

## 注意事项

- 生成1张图像消耗：5积分
- 生成1段视频消耗：20积分
- 使用前需要关注官方频道

## 作者

@author seven

@since 2024

