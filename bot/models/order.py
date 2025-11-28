# -*- coding: utf-8 -*-
"""
订单模型

@author seven
@since 2024
"""
from sqlalchemy import Column, String, Integer, BigInteger, Enum
import enum
from loguru import logger
from .base import BaseModel


class OrderType(enum.Enum):
    """订单类型"""
    IMAGE = "image"  # 图片生成
    VIDEO = "video"  # 视频生成


class OrderStatus(enum.Enum):
    """订单状态"""
    PENDING = "pending"  # 待处理
    PROCESSING = "processing"  # 处理中
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"  # 失败


class Order(BaseModel):
    """
    订单模型
    
    @author seven
    @since 2024
    """
    __tablename__ = 'orders'
    
    user_id = Column(BigInteger, nullable=False, index=True, comment='用户Telegram ID')
    order_no = Column(String(64), unique=True, nullable=False, index=True, comment='订单号')
    order_type = Column(Enum(OrderType), nullable=False, comment='订单类型')
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False, comment='订单状态')
    points_cost = Column(Integer, nullable=False, comment='消耗积分')
    image_url = Column(String(512), nullable=True, comment='生成的图片URL')
    video_url = Column(String(512), nullable=True, comment='生成的视频URL')
    error_message = Column(String(512), nullable=True, comment='错误信息')
    
    def __repr__(self):
        return f"<Order(order_no={self.order_no}, user_id={self.user_id}, status={self.status})>"
    
    def update_status(self, status: OrderStatus, error_message: str = None):
        """
        更新订单状态
        
        @param status: 新状态
        @param error_message: 错误信息（如果有）
        @author seven
        @since 2024
        """
        try:
            logger.info(f"更新订单状态 - 订单号: {self.order_no}, 旧状态: {self.status}, 新状态: {status}")
            self.status = status
            if error_message:
                self.error_message = error_message
                logger.error(f"订单错误信息: {error_message}")
        except Exception as e:
            logger.error(f"更新订单状态失败 - 订单号: {self.order_no}, 错误: {e}")
            raise

