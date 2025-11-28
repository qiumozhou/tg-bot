# -*- coding: utf-8 -*-
"""
回调查询处理器

@author seven
@since 2024
"""
from telegram import Update
from telegram.ext import ContextTypes
from loguru import logger
from bot.handlers.menu import (
    get_main_menu_keyboard,
    get_strip_menu_keyboard,
    get_points_menu_keyboard,
    get_recharge_menu_keyboard,
    get_payment_method_keyboard
)
from bot.utils.database import get_session
from bot.services.user_service import UserService
from bot.services.payment_service import PaymentService, PaymentMethod
from bot.services.payment_api import PaymentAPI
from bot.services.channel_service import ChannelService
from bot.services.referral_service import ReferralService


async def callback_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    处理回调查询
    
    @param update: Telegram更新对象
    @param context: 上下文对象
    @author seven
    @since 2024
    """
    try:
        query = update.callback_query
        await query.answer()
        
        data = query.data
        user = update.effective_user
        
        logger.info(f"收到回调查询 - 用户ID: {user.id}, 数据: {data}")
        
        # 主菜单
        if data == "menu_main":
            await query.edit_message_text(
                "请选择功能：",
                reply_markup=get_main_menu_keyboard()
            )
        
        # 脱衣菜单
        elif data == "menu_strip":
            await query.edit_message_text(
                "脱衣功能：\n\n图片脱衣：5积分/图片\n视频脱衣：20积分/视频",
                reply_markup=get_strip_menu_keyboard()
            )
        
        # 积分菜单
        elif data == "menu_points":
            await query.edit_message_text(
                "获积分：",
                reply_markup=get_points_menu_keyboard()
            )
        
        # 充值菜单
        elif data == "points_recharge":
            text = """充值获积分

操作说明：
请选择充值积分数量和支付方式后，点击确定充值。之后会返回支付链接。点击链接后跳转到相应方式中进行支付。

备注：生成1张图像消耗：5积分    生成1段视频消耗：20积分

积分套餐：
• 20积分20元
• 55积分50元
• 120积分100元
• 250积分200元"""
            await query.edit_message_text(text, reply_markup=get_recharge_menu_keyboard())
        
        # 选择充值套餐
        elif data.startswith("recharge_"):
            package_key = data.replace("recharge_", "")
            await query.edit_message_text(
                f"选择支付方式（套餐：{package_key}积分）",
                reply_markup=get_payment_method_keyboard(package_key)
            )
        
        # 个人中心
        elif data == "menu_profile":
            async with get_session() as session:
                try:
                    db_user = await UserService.get_user_by_telegram_id(session, user.id)
                    if db_user:
                        username = f"@{db_user.username}" if db_user.username else "未设置"
                        text = f"""个人中心

【名称】：{username}
⭐️【积分】：{db_user.points}
💎【等级】：{db_user.level}"""
                        await query.edit_message_text(text, reply_markup=get_main_menu_keyboard())
                    else:
                        await query.edit_message_text("用户不存在，请重新开始。", reply_markup=get_main_menu_keyboard())
                except Exception as e:
                    logger.error(f"获取用户信息失败: {e}")
                    await query.edit_message_text("获取用户信息失败，请稍后重试。", reply_markup=get_main_menu_keyboard())
        
        # 处理支付
        elif data.startswith("pay_"):
            parts = data.split("_")
            if len(parts) == 3:
                package_key = parts[1]
                payment_method_str = parts[2]
                
                try:
                    payment_method = PaymentMethod[payment_method_str.upper()]
                    
                    async with get_session() as session:
                        try:
                            payment = await PaymentService.create_payment(
                                session=session,
                                user_id=user.id,
                                package_key=package_key,
                                payment_method=payment_method
                            )
                            
                            # 生成支付链接
                            bot = context.bot
                            if payment_method == PaymentMethod.ALIPAY:
                                payment_url = await PaymentAPI.create_alipay_payment(payment)
                                await PaymentService.update_payment_url(session, payment, payment_url)
                                
                                text = f"""支付宝支付

请打开链接并使用支付宝支付~
支付{payment.amount}元，充值{payment.points}积分
订单号：{payment.order_no}(复制补单)
支付链接：{payment_url}
点击跳转到浏览器打开，或复制链接到浏览器打开
请于5分钟内完成支付，超过5分钟后支付失效~

👇🏻点击一键跳转支付👇🏻"""
                                
                                from telegram import InlineKeyboardButton, InlineKeyboardMarkup
                                keyboard = [[InlineKeyboardButton("跳转支付", url=payment_url)],
                                           [InlineKeyboardButton("⬅️ 返回主菜单", callback_data="menu_main")]]
                                reply_markup = InlineKeyboardMarkup(keyboard)
                                
                            elif payment_method == PaymentMethod.WECHAT:
                                trade_no, payment_url = await PaymentAPI.create_wechat_payment(payment)
                                await PaymentService.update_payment_url(session, payment, payment_url)
                                
                                text = f"""微信充值

您的支付订单号为：
[ {trade_no} ]
请保留好订单号，如有问题，请向客服提供此订单号
微信支付链接: 
{payment_url}
请在15分钟内点上面链接完成支付订单。过期请重新选择。
支付成功后，积分将自动到账。若5分钟仍未到账，请提供订单号，联系客服。"""
                                
                                from telegram import InlineKeyboardButton, InlineKeyboardMarkup
                                keyboard = [[InlineKeyboardButton("跳转支付", url=payment_url)],
                                           [InlineKeyboardButton("⬅️ 返回主菜单", callback_data="menu_main")]]
                                reply_markup = InlineKeyboardMarkup(keyboard)
                                
                            else:  # USDT
                                payment_url = await PaymentAPI.create_usdt_payment(payment)
                                await PaymentService.update_payment_url(session, payment, payment_url)
                                
                                text = f"""USDT支付

订单号：{payment.order_no}
金额：{payment.amount}元
积分：{payment.points}积分
支付链接：{payment_url}"""
                                
                                from telegram import InlineKeyboardButton, InlineKeyboardMarkup
                                keyboard = [[InlineKeyboardButton("跳转支付", url=payment_url)],
                                           [InlineKeyboardButton("⬅️ 返回主菜单", callback_data="menu_main")]]
                                reply_markup = InlineKeyboardMarkup(keyboard)
                            
                            await query.edit_message_text(text, reply_markup=reply_markup)
                            
                        except Exception as e:
                            logger.error(f"创建支付订单失败: {e}")
                            await query.edit_message_text("创建支付订单失败，请稍后重试。", reply_markup=get_main_menu_keyboard())
                            
                except Exception as e:
                    logger.error(f"创建支付订单失败 - 用户ID: {user.id}, 错误: {e}")
                    await query.edit_message_text("创建支付订单失败，请稍后重试。", reply_markup=get_main_menu_keyboard())
        
        # 分享获积分
        elif data == "points_share":
            async with get_session() as session:
                try:
                    db_user = await UserService.get_user_by_telegram_id(session, user.id)
                    if db_user:
                        bot_username = context.bot.username
                        referral_link = await ReferralService.get_referral_link(bot_username, db_user.referral_code)
                        
                        text = f"""分享获积分

下面这条消息带有你的专属分享链接，请分享到其他群或用户。其他用户进来后，你将获取积分。

积分规则：
新用户通过你的专属链接使用机器人，你将获取40积分。推广用户无积分上限。
非新用户通过你的专属链接使用机器人，如果该用户7天内没有通过别人的推广链接使用机器人，则你将获取10积分。积分每日上限：100

你的专属推广链接：
{referral_link}

推广码：{db_user.referral_code}"""
                        
                        await query.edit_message_text(text, reply_markup=get_main_menu_keyboard())
                    else:
                        await query.edit_message_text("用户不存在，请重新开始。", reply_markup=get_main_menu_keyboard())
                except Exception as e:
                    logger.error(f"获取分享链接失败: {e}")
                    await query.edit_message_text("获取分享链接失败，请稍后重试。", reply_markup=get_main_menu_keyboard())
        
        # 图片脱衣
        elif data == "strip_image":
            text = """图片脱衣：5积分/图片

注意事项：
使用我们的服务即表示您同意，用户协议且不得用于非法用途。
建议上传：站立，单人，无遮挡，主体人物清晰的照片无奇怪动作姿势

效果预览 (【NSFW】官方功能更新频道 )
如果没有关注官方频道 机器人不会出图！

【菜单】上传图片"""
            from telegram import InlineKeyboardButton, InlineKeyboardMarkup
            keyboard = [[InlineKeyboardButton("上传图片", callback_data="upload_image_strip")],
                       [InlineKeyboardButton("⬅️ 返回", callback_data="menu_strip")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text, reply_markup=reply_markup)
        
        # 视频脱衣
        elif data == "strip_video":
            text = """视频脱衣：20积分/视频

注意事项：
使用我们的服务即表示您同意 用户协议且不得用于非法用途。
建议上传站立，单人，无遮挡，主体人物清晰的照片 无奇怪动作姿势

效果预览 (【NSFW】官方功能更新频道 )
如果没有关注官方频道 机器人不会出图！

【菜单】上传图片"""
            from telegram import InlineKeyboardButton, InlineKeyboardMarkup
            keyboard = [[InlineKeyboardButton("上传图片", callback_data="upload_video_strip")],
                       [InlineKeyboardButton("⬅️ 返回", callback_data="menu_strip")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text, reply_markup=reply_markup)
        
        # 其他菜单项（待实现）
        else:
            await query.edit_message_text("功能开发中，敬请期待。", reply_markup=get_main_menu_keyboard())
            
    except Exception as e:
        logger.error(f"处理回调查询失败 - 错误: {e}")
        if update.callback_query:
            await update.callback_query.answer("发生错误，请稍后重试。")

