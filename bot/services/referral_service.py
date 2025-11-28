# -*- coding: utf-8 -*-
"""
推广服务

@author seven
@since 2024
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from loguru import logger
from datetime import datetime, timedelta
from bot.models.user import User
from bot.services.user_service import UserService


class ReferralService:
    """
    推广服务类
    
    @author seven
    @since 2024
    """
    
    # 推广奖励配置
    NEW_USER_BONUS = 40  # 新用户奖励
    EXISTING_USER_BONUS = 10  # 老用户奖励
    DAILY_LIMIT = 100  # 每日推广积分上限
    REFERRAL_VALID_DAYS = 7  # 推广链接有效期（天）
    
    @staticmethod
    async def process_referral(
        session: AsyncSession,
        new_user_id: int,
        referral_code: str
    ) -> tuple[bool, int]:
        """
        处理推广逻辑
        
        @param session: 数据库会话
        @param new_user_id: 新用户Telegram ID
        @param referral_code: 推广码
        @return: (是否成功, 奖励积分)
        @author seven
        @since 2024
        """
        try:
            logger.info(f"处理推广 - 新用户ID: {new_user_id}, 推广码: {referral_code}")
            
            # 获取推广人
            referrer = await UserService.get_user_by_referral_code(session, referral_code)
            if not referrer:
                logger.warning(f"推广码不存在 - 推广码: {referral_code}")
                return False, 0
            
            if referrer.telegram_id == new_user_id:
                logger.warning(f"用户不能使用自己的推广码 - 用户ID: {new_user_id}")
                return False, 0
            
            # 检查新用户是否已经存在
            new_user = await UserService.get_user_by_telegram_id(session, new_user_id)
            is_new_user = new_user is None or new_user.created_at is None
            
            # 检查用户是否在7天内使用过其他推广链接
            if not is_new_user:
                # 如果用户已经有推广人，检查是否在有效期内
                if new_user.referred_by and new_user.referred_by != referrer.telegram_id:
                    logger.info(f"用户已有其他推广人 - 用户ID: {new_user_id}")
                    # 检查推广时间是否在7天内
                    if new_user.created_at:
                        days_diff = (datetime.utcnow() - new_user.created_at).days
                        if days_diff <= ReferralService.REFERRAL_VALID_DAYS:
                            logger.info(f"用户在推广有效期内 - 用户ID: {new_user_id}, 天数: {days_diff}")
                            return False, 0
            
            # 确定奖励积分
            if is_new_user:
                bonus_points = ReferralService.NEW_USER_BONUS
                logger.info(f"新用户推广奖励 - 推广人ID: {referrer.telegram_id}, 奖励积分: {bonus_points}")
            else:
                bonus_points = ReferralService.EXISTING_USER_BONUS
                logger.info(f"老用户推广奖励 - 推广人ID: {referrer.telegram_id}, 奖励积分: {bonus_points}")
            
            # 检查每日推广积分上限
            today = datetime.utcnow().date().isoformat()
            if referrer.last_referral_bonus_date != today:
                # 新的一天，重置每日积分
                referrer.daily_referral_points = 0
                referrer.last_referral_bonus_date = today
                logger.info(f"重置推广人每日积分 - 推广人ID: {referrer.telegram_id}, 日期: {today}")
            
            # 检查是否超过每日上限
            if referrer.daily_referral_points + bonus_points > ReferralService.DAILY_LIMIT:
                available_bonus = ReferralService.DAILY_LIMIT - referrer.daily_referral_points
                if available_bonus <= 0:
                    logger.warning(f"推广人今日积分已达上限 - 推广人ID: {referrer.telegram_id}")
                    return False, 0
                bonus_points = available_bonus
            
            # 添加奖励积分
            await UserService.add_points(session, referrer, bonus_points, f"推广奖励 - 用户{new_user_id}")
            referrer.daily_referral_points += bonus_points
            
            # 更新新用户的推广人信息
            if new_user:
                new_user.referred_by = referrer.telegram_id
            
            await session.commit()
            
            logger.info(f"推广奖励发放成功 - 推广人ID: {referrer.telegram_id}, 奖励积分: {bonus_points}")
            return True, bonus_points
            
        except Exception as e:
            logger.error(f"处理推广失败 - 新用户ID: {new_user_id}, 推广码: {referral_code}, 错误: {e}")
            await session.rollback()
            raise
    
    @staticmethod
    async def get_referral_link(bot_username: str, referral_code: str) -> str:
        """
        获取推广链接
        
        @param bot_username: Bot用户名
        @param referral_code: 推广码
        @return: 推广链接
        @author seven
        @since 2024
        """
        try:
            link = f"https://t.me/{bot_username}?start={referral_code}"
            logger.debug(f"生成推广链接 - 推广码: {referral_code}, 链接: {link}")
            return link
        except Exception as e:
            logger.error(f"生成推广链接失败 - 推广码: {referral_code}, 错误: {e}")
            raise

