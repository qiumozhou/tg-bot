# -*- coding: utf-8 -*-
"""
配置文件示例
复制此文件为 config.py 并填入实际配置

@author seven
@since 2024
"""

# Telegram Bot配置
BOT_TOKEN = "your_bot_token_here"

# 数据库配置
DATABASE_URL = "sqlite+aiosqlite:///./data/bot.db"

# 支付配置
# 支付宝支付配置
ALIPAY_APP_ID = "your_alipay_app_id"
ALIPAY_PRIVATE_KEY = "your_alipay_private_key"
ALIPAY_PUBLIC_KEY = "your_alipay_public_key"
ALIPAY_NOTIFY_URL = "https://your-domain.com/api/payment/alipay/notify"

# 微信支付配置
WECHAT_APP_ID = "your_wechat_app_id"
WECHAT_MCH_ID = "your_wechat_mch_id"
WECHAT_API_KEY = "your_wechat_api_key"
WECHAT_NOTIFY_URL = "https://your-domain.com/api/payment/wechat/notify"

# USTD配置
USTD_API_KEY = "your_ustd_api_key"
USTD_NOTIFY_URL = "https://your-domain.com/api/payment/ustd/notify"

# 官方频道配置
OFFICIAL_CHANNEL_ID = "@your_official_channel"

# 图像生成API配置
IMAGE_GENERATION_API_URL = "https://your-api-url.com/generate"
IMAGE_GENERATION_API_KEY = "your_api_key"

# 视频生成API配置
VIDEO_GENERATION_API_URL = "https://your-api-url.com/generate_video"
VIDEO_GENERATION_API_KEY = "your_api_key"

# 日志配置
LOG_LEVEL = "INFO"
LOG_FILE = "logs/bot.log"

