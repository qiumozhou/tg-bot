# -*- coding: utf-8 -*-
"""
支付模型

@author seven
@since 2024
"""
from sqlalchemy import Column, String, Integer, BigInteger, Enum, Numeric
import enum
from loguru import logger
from .base import BaseModel


class PaymentMethod(enum.Enum):
    """支付方式"""
    ALIPAY = "alipay"  # 支付宝
    WECHAT = "wechat"  # 微信
    USDT = "usdt"  # USDT


class PaymentStatus(enum.Enum):
    """支付状态"""
    PENDING = "pending"  # 待支付
    PAID = "paid"  # 已支付
    FAILED = "failed"  # 支付失败
    EXPIRED = "expired"  # 已过期


class Payment(BaseModel):
    """
    支付模型
    
    @author seven
    @since 2024
    """
    __tablename__ = 'payments'
    
    user_id = Column(BigInteger, nullable=False, index=True, comment='用户Telegram ID')
    order_no = Column(String(64), unique=True, nullable=False, index=True, comment='支付订单号')
    payment_method = Column(Enum(PaymentMethod), nullable=False, comment='支付方式')
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False, comment='支付状态')
    amount = Column(Numeric(10, 2), nullable=False, comment='支付金额（元）')
    points = Column(Integer, nullable=False, comment='购买积分')
    payment_url = Column(String(512), nullable=True, comment='支付链接')
    callback_data = Column(String(2048), nullable=True, comment='回调数据')
    paid_at = Column(String(32), nullable=True, comment='支付时间')
    
    def __repr__(self):
        return f"<Payment(order_no={self.order_no}, user_id={self.user_id}, status={self.status})>"
    
    def update_status(self, status: PaymentStatus, paid_at: str = None):
        """
        更新支付状态
        
        @param status: 新状态
        @param paid_at: 支付时间
        @author seven
        @since 2024
        """
        try:
            logger.info(f"更新支付状态 - 订单号: {self.order_no}, 旧状态: {self.status}, 新状态: {status}")
            self.status = status
            if paid_at:
                self.paid_at = paid_at
        except Exception as e:
            logger.error(f"更新支付状态失败 - 订单号: {self.order_no}, 错误: {e}")
            raise

