# -*- coding: utf-8 -*-
"""
Telegram Bot 主程序入口

@author seven
@since 2024
"""
import os
import sys
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from loguru import logger
from bot.utils.logger import setup_logger
from bot.utils.database import init_db
from bot.handlers.start import start_command
from bot.handlers.callback import callback_query_handler
from bot.handlers.message import handle_photo, handle_text

# Windows 事件循环策略修复
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def post_init(application: Application) -> None:
    """
    应用初始化后的回调函数
    
    @param application: Bot应用实例
    @author seven
    @since 2024
    """
    try:
        logger.info("初始化数据库...")
        await init_db()
        logger.info("数据库初始化完成")
        
        # 获取Bot信息，确认连接成功
        bot = application.bot
        bot_info = await bot.get_me()
        logger.info("=" * 80)
        logger.info(f"Bot 连接成功！")
        logger.info(f"Bot 用户名: @{bot_info.username}")
        logger.info(f"Bot 名称: {bot_info.first_name}")
        logger.info(f"Bot ID: {bot_info.id}")
        logger.info("=" * 80)
        logger.info("Bot 正在轮询中，等待消息...")
        logger.info("按 Ctrl+C 停止Bot")
        logger.info("=" * 80)
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        raise


def main():
    """
    主函数
    
    @author seven
    @since 2024
    """
    try:
        # 加载环境变量
        load_dotenv()
        
        # 设置日志
        log_level = os.getenv('LOG_LEVEL', 'INFO')
        log_file = os.getenv('LOG_FILE', 'logs/bot.log')
        setup_logger(log_level, log_file)
        
        logger.info("=" * 80)
        logger.info("Telegram Bot 启动中...")
        logger.info("=" * 80)
        
        # 获取Bot Token
        bot_token = os.getenv('BOT_TOKEN')
        if not bot_token:
            raise ValueError("BOT_TOKEN 环境变量未设置，请在 .env 文件中配置")
        
        logger.info("创建Bot应用...")
        
        # 创建应用
        application = (
            Application.builder()
            .token(bot_token)
            .post_init(post_init)
            .build()
        )
        
        # 注册处理器
        logger.info("注册命令处理器...")
        application.add_handler(CommandHandler("start", start_command))
        
        logger.info("注册回调查询处理器...")
        application.add_handler(CallbackQueryHandler(callback_query_handler))
        
        logger.info("注册消息处理器...")
        application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
        
        logger.info("正在启动轮询...")
        logger.info("=" * 80)
        
        # 运行Bot（让 run_polling 自己管理事件循环）
        # run_polling 会阻塞直到收到停止信号（Ctrl+C）
        try:
            application.run_polling(
                allowed_updates=Update.ALL_TYPES,
                close_loop=True,
                drop_pending_updates=True  # 启动时丢弃待处理的更新
            )
        except Exception as e:
            logger.error(f"轮询过程中发生错误: {e}")
            raise
        
    except KeyboardInterrupt:
        logger.info("收到停止信号，Bot 正在关闭...")
    except Exception as e:
        logger.error(f"Bot 启动失败: {e}")
        raise
    finally:
        logger.info("Bot 已关闭")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("程序已退出")
