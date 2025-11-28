# -*- coding: utf-8 -*-
"""
启动命令处理器

@author seven
@since 2024
"""
from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger
from bot.handlers.menu import WELCOME_MESSAGE, DISCLAIMER_MESSAGE, get_main_menu_keyboard
from bot.utils.database import get_session
from bot.services.user_service import UserService
from bot.services.referral_service import ReferralService


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    处理 /start 命令
    
    @param update: Telegram更新对象
    @param context: 上下文对象
    @author seven
    @since 2024
    """
    try:
        user = update.effective_user
        logger.info(f"收到 /start 命令 - 用户ID: {user.id}, 用户名: {user.username}")
        
        # 获取或创建用户
        async with get_session() as session:
            try:
                db_user = await UserService.get_or_create_user(
                    session=session,
                    telegram_id=user.id,
                    username=user.username,
                    first_name=user.first_name,
                    last_name=user.last_name
                )
                
                # 检查是否是推广链接
                if context.args:
                    referral_code = context.args[0]
                    logger.info(f"检测到推广码: {referral_code}, 用户ID: {user.id}")
                    try:
                        success, bonus = await ReferralService.process_referral(
                            session=session,
                            new_user_id=user.id,
                            referral_code=referral_code
                        )
                        if success:
                            logger.info(f"推广奖励发放成功 - 用户ID: {user.id}, 奖励积分: {bonus}")
                    except Exception as e:
                        logger.error(f"处理推广失败 - 用户ID: {user.id}, 推广码: {referral_code}, 错误: {e}")
                
                # 发送免责声明
                await update.message.reply_text(
                    DISCLAIMER_MESSAGE,
                    reply_markup=get_main_menu_keyboard()
                )
                
                logger.info(f"启动消息发送成功 - 用户ID: {user.id}")
                
            except Exception as e:
                logger.error(f"处理 /start 命令失败 - 用户ID: {user.id}, 错误: {e}")
                await update.message.reply_text("发生错误，请稍后重试。")
                raise
                
    except Exception as e:
        logger.error(f"处理 /start 命令时发生异常 - 错误: {e}")
        if update.message:
            await update.message.reply_text("发生错误，请稍后重试。")

