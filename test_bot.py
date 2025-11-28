# -*- coding: utf-8 -*-
"""
测试Bot连接脚本

@author seven
@since 2024
"""
import os
import asyncio
from dotenv import load_dotenv
from telegram import Bot
from loguru import logger

async def test_connection():
    """测试Bot连接"""
    load_dotenv()
    
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        print("错误: BOT_TOKEN 未设置")
        return
    
    try:
        bot = Bot(token=bot_token)
        bot_info = await bot.get_me()
        
        print("=" * 50)
        print("Bot 连接测试成功！")
        print(f"Bot 用户名: @{bot_info.username}")
        print(f"Bot 名称: {bot_info.first_name}")
        print(f"Bot ID: {bot_info.id}")
        print("=" * 50)
        
        # 测试获取更新
        print("\n测试获取更新...")
        updates = await bot.get_updates(limit=1, timeout=5)
        if updates:
            print(f"收到 {len(updates)} 条更新")
        else:
            print("没有待处理的更新（这是正常的）")
        
        print("\nBot 可以正常连接！")
        
    except Exception as e:
        print(f"连接失败: {e}")
        logger.error(f"连接失败: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())

