# -*- coding: utf-8 -*-
"""
消息处理器

@author seven
@since 2024
"""
from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger
import os
from bot.utils.database import get_session
from bot.services.user_service import UserService
from bot.services.channel_service import ChannelService
from bot.services.order_service import OrderService
from bot.models.order import OrderType, OrderStatus


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    处理图片消息
    
    @param update: Telegram更新对象
    @param context: 上下文对象
    @author seven
    @since 2024
    """
    try:
        user = update.effective_user
        photo = update.message.photo[-1]  # 获取最大尺寸的图片
        
        logger.info(f"收到图片消息 - 用户ID: {user.id}, 文件ID: {photo.file_id}")
        
        async with get_session() as session:
            try:
                # 获取用户信息
                db_user = await UserService.get_user_by_telegram_id(session, user.id)
                if not db_user:
                    await update.message.reply_text("请先使用 /start 命令开始使用机器人。")
                    return
                
                # 检查是否关注官方频道
                bot = context.bot
                is_subscribed = await ChannelService.check_user_subscribed(bot, user.id)
                if not is_subscribed:
                    channel_id = os.getenv('OFFICIAL_CHANNEL_ID', '@your_official_channel')
                    await update.message.reply_text(
                        f"❌ 请先关注官方频道才能使用此功能！\n\n"
                        f"官方频道：{channel_id}\n"
                        f"关注后请重新上传图片。"
                    )
                    return
                
                # 检查用户积分（默认图片处理，5积分）
                points_required = 5
                if not db_user.check_points(points_required):
                    await update.message.reply_text(
                        f"❌ 你的积分不足。当前积分：{db_user.points}，需要积分：{points_required}，请先获取足够积分"
                    )
                    return
                
                # 扣除积分并创建订单
                success = await UserService.deduct_points(session, db_user, points_required)
                if not success:
                    await update.message.reply_text(
                        f"❌ 积分扣除失败。当前积分：{db_user.points}，需要积分：{points_required}"
                    )
                    return
                
                # 创建订单
                order = await OrderService.create_order(
                    session=session,
                    user_id=user.id,
                    order_type=OrderType.IMAGE,
                    points_cost=points_required
                )
                
                # 下载图片文件
                bot = context.bot
                file = await bot.get_file(photo.file_id)
                
                await update.message.reply_text(f"✅ 图片接收成功，订单号：{order.order_no}\n正在处理中，请稍候...")
                
                # TODO: 调用图像生成API处理图片
                # 这里应该调用实际的图像生成服务
                # result = await image_generation_service.process_image(file.file_path, order.order_no)
                
                # 暂时模拟处理
                await update.message.reply_text(
                    f"⚠️ 图像生成功能待实现\n"
                    f"订单号：{order.order_no}\n"
                    f"已扣除积分：{points_required}\n"
                    f"剩余积分：{db_user.points - points_required}"
                )
                
                logger.info(f"图片处理完成 - 订单号: {order.order_no}, 用户ID: {user.id}")
                
            except Exception as e:
                logger.error(f"处理图片失败 - 用户ID: {user.id}, 错误: {e}")
                await update.message.reply_text("处理图片时发生错误，请稍后重试。")
                raise
        
    except Exception as e:
        logger.error(f"处理图片消息失败 - 用户ID: {user.id if user else None}, 错误: {e}")
        if update.message:
            await update.message.reply_text("处理图片时发生错误，请稍后重试。")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    处理文本消息
    
    @param update: Telegram更新对象
    @param context: 上下文对象
    @author seven
    @since 2024
    """
    try:
        user = update.effective_user
        text = update.message.text
        
        logger.info(f"收到文本消息 - 用户ID: {user.id}, 内容: {text}")
        
        # 这里可以根据文本内容进行不同的处理
        # 暂时回复提示信息
        await update.message.reply_text("请使用菜单按钮进行操作。")
        
    except Exception as e:
        logger.error(f"处理文本消息失败 - 用户ID: {user.id if user else None}, 错误: {e}")
        if update.message:
            await update.message.reply_text("处理消息时发生错误，请稍后重试。")

