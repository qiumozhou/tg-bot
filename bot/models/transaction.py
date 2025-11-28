# -*- coding: utf-8 -*-
"""
交易记录模型

@author seven
@since 2024
"""
from sqlalchemy import Column, String, Integer, BigInteger, Enum
import enum
from loguru import logger
from .base import BaseModel


class TransactionType(enum.Enum):
    """交易类型"""
    CHARGE = "charge"  # 充值
    CONSUME = "consume"  # 消费
    REFERRAL = "referral"  # 推广奖励


class Transaction(BaseModel):
    """
    交易记录模型
    
    @author seven
    @since 2024
    """
    __tablename__ = 'transactions'
    
    user_id = Column(BigInteger, nullable=False, index=True, comment='用户Telegram ID')
    transaction_type = Column(Enum(TransactionType), nullable=False, comment='交易类型')
    points = Column(Integer, nullable=False, comment='积分变动（正数为增加，负数为减少）')
    related_user_id = Column(BigInteger, nullable=True, comment='关联用户ID（推广奖励时使用）')
    description = Column(String(512), nullable=True, comment='交易描述')
    
    def __repr__(self):
        return f"<Transaction(user_id={self.user_id}, type={self.transaction_type}, points={self.points})>"

