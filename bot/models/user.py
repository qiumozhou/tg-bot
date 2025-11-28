# -*- coding: utf-8 -*-
"""
用户模型

@author seven
@since 2024
"""
from sqlalchemy import Column, String, Integer, Boolean, BigInteger
from loguru import logger
from .base import BaseModel


class User(BaseModel):
    """
    用户模型
    
    @author seven
    @since 2024
    """
    __tablename__ = 'users'
    
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True, comment='Telegram用户ID')
    username = Column(String(255), nullable=True, comment='用户名')
    first_name = Column(String(255), nullable=True, comment='名')
    last_name = Column(String(255), nullable=True, comment='姓')
    points = Column(Integer, default=0, nullable=False, comment='积分')
    level = Column(String(10), default='P1', nullable=False, comment='等级')
    referral_code = Column(String(32), unique=True, nullable=False, index=True, comment='推广码')
    referred_by = Column(BigInteger, nullable=True, comment='推广人Telegram ID')
    is_active = Column(Boolean, default=True, nullable=False, comment='是否激活')
    last_referral_bonus_date = Column(String(10), nullable=True, comment='最后获得推广奖励的日期')
    daily_referral_points = Column(Integer, default=0, nullable=False, comment='当日推广积分')
    
    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, username={self.username}, points={self.points})>"
    
    def add_points(self, amount: int) -> bool:
        """
        增加积分
        
        @param amount: 积分数量
        @return: 是否成功
        @author seven
        @since 2024
        """
        try:
            logger.info(f"用户 {self.telegram_id} 增加积分: {amount}, 当前积分: {self.points}")
            self.points += amount
            logger.info(f"用户 {self.telegram_id} 积分更新后: {self.points}")
            return True
        except Exception as e:
            logger.error(f"增加积分失败 - 用户ID: {self.telegram_id}, 积分: {amount}, 错误: {e}")
            raise
    
    def deduct_points(self, amount: int) -> bool:
        """
        扣除积分
        
        @param amount: 积分数量
        @return: 是否成功
        @author seven
        @since 2024
        """
        try:
            logger.info(f"用户 {self.telegram_id} 扣除积分: {amount}, 当前积分: {self.points}")
            if self.points < amount:
                logger.warning(f"用户 {self.telegram_id} 积分不足: 当前{self.points}, 需要{amount}")
                return False
            self.points -= amount
            logger.info(f"用户 {self.telegram_id} 积分扣除后: {self.points}")
            return True
        except Exception as e:
            logger.error(f"扣除积分失败 - 用户ID: {self.telegram_id}, 积分: {amount}, 错误: {e}")
            raise
    
    def check_points(self, required: int) -> bool:
        """
        检查积分是否足够
        
        @param required: 需要的积分数量
        @return: 是否足够
        @author seven
        @since 2024
        """
        return self.points >= required

