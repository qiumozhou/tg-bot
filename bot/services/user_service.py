# -*- coding: utf-8 -*-
"""
用户服务

@author seven
@since 2024
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from loguru import logger
from bot.models.user import User
from bot.utils.helpers import generate_referral_code, get_user_level
from datetime import datetime


class UserService:
    """
    用户服务类
    
    @author seven
    @since 2024
    """
    
    @staticmethod
    async def get_or_create_user(
        session: AsyncSession,
        telegram_id: int,
        username: str = None,
        first_name: str = None,
        last_name: str = None
    ) -> User:
        """
        获取或创建用户
        
        @param session: 数据库会话
        @param telegram_id: Telegram用户ID
        @param username: 用户名
        @param first_name: 名
        @param last_name: 姓
        @return: 用户对象
        @author seven
        @since 2024
        """
        try:
            logger.info(f"获取或创建用户 - Telegram ID: {telegram_id}, Username: {username}")
            
            # 查询用户
            result = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            user = result.scalar_one_or_none()
            
            if user:
                # 更新用户信息
                logger.info(f"用户已存在，更新信息 - Telegram ID: {telegram_id}")
                user.username = username
                user.first_name = first_name
                user.last_name = last_name
            else:
                # 创建新用户
                logger.info(f"创建新用户 - Telegram ID: {telegram_id}")
                referral_code = generate_referral_code()
                user = User(
                    telegram_id=telegram_id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    points=0,
                    level="P1",
                    referral_code=referral_code,
                    is_active=True
                )
                session.add(user)
                await session.commit()
                logger.info(f"新用户创建成功 - Telegram ID: {telegram_id}, 推广码: {referral_code}")
            
            await session.refresh(user)
            return user
            
        except Exception as e:
            logger.error(f"获取或创建用户失败 - Telegram ID: {telegram_id}, 错误: {e}")
            await session.rollback()
            raise
    
    @staticmethod
    async def get_user_by_telegram_id(session: AsyncSession, telegram_id: int) -> User:
        """
        根据Telegram ID获取用户
        
        @param session: 数据库会话
        @param telegram_id: Telegram用户ID
        @return: 用户对象，不存在返回None
        @author seven
        @since 2024
        """
        try:
            logger.debug(f"查询用户 - Telegram ID: {telegram_id}")
            result = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            user = result.scalar_one_or_none()
            return user
        except Exception as e:
            logger.error(f"查询用户失败 - Telegram ID: {telegram_id}, 错误: {e}")
            raise
    
    @staticmethod
    async def get_user_by_referral_code(session: AsyncSession, referral_code: str) -> User:
        """
        根据推广码获取用户
        
        @param session: 数据库会话
        @param referral_code: 推广码
        @return: 用户对象，不存在返回None
        @author seven
        @since 2024
        """
        try:
            logger.debug(f"根据推广码查询用户 - 推广码: {referral_code}")
            result = await session.execute(
                select(User).where(User.referral_code == referral_code)
            )
            user = result.scalar_one_or_none()
            return user
        except Exception as e:
            logger.error(f"根据推广码查询用户失败 - 推广码: {referral_code}, 错误: {e}")
            raise
    
    @staticmethod
    async def add_points(session: AsyncSession, user: User, amount: int, reason: str = None):
        """
        给用户增加积分
        
        @param session: 数据库会话
        @param user: 用户对象
        @param amount: 积分数量
        @param reason: 原因
        @author seven
        @since 2024
        """
        try:
            logger.info(f"给用户增加积分 - 用户ID: {user.telegram_id}, 积分: {amount}, 原因: {reason}")
            user.add_points(amount)
            # 更新等级
            user.level = get_user_level(user.points)
            await session.commit()
            logger.info(f"用户积分增加成功 - 用户ID: {user.telegram_id}, 当前积分: {user.points}, 等级: {user.level}")
        except Exception as e:
            logger.error(f"增加积分失败 - 用户ID: {user.telegram_id}, 积分: {amount}, 错误: {e}")
            await session.rollback()
            raise
    
    @staticmethod
    async def deduct_points(session: AsyncSession, user: User, amount: int) -> bool:
        """
        扣除用户积分
        
        @param session: 数据库会话
        @param user: 用户对象
        @param amount: 积分数量
        @return: 是否成功
        @author seven
        @since 2024
        """
        try:
            logger.info(f"扣除用户积分 - 用户ID: {user.telegram_id}, 积分: {amount}")
            success = user.deduct_points(amount)
            if success:
                # 更新等级
                user.level = get_user_level(user.points)
                await session.commit()
                logger.info(f"用户积分扣除成功 - 用户ID: {user.telegram_id}, 当前积分: {user.points}, 等级: {user.level}")
            else:
                logger.warning(f"用户积分不足 - 用户ID: {user.telegram_id}, 当前积分: {user.points}, 需要积分: {amount}")
            return success
        except Exception as e:
            logger.error(f"扣除积分失败 - 用户ID: {user.telegram_id}, 积分: {amount}, 错误: {e}")
            await session.rollback()
            raise

