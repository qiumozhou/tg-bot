# -*- coding: utf-8 -*-
"""
订单服务

@author seven
@since 2024
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from loguru import logger
from bot.models.order import Order, OrderType, OrderStatus
from bot.utils.helpers import generate_order_no
from datetime import datetime


class OrderService:
    """
    订单服务类
    
    @author seven
    @since 2024
    """
    
    @staticmethod
    async def create_order(
        session: AsyncSession,
        user_id: int,
        order_type: OrderType,
        points_cost: int
    ) -> Order:
        """
        创建订单
        
        @param session: 数据库会话
        @param user_id: 用户Telegram ID
        @param order_type: 订单类型
        @param points_cost: 消耗积分
        @return: 订单对象
        @author seven
        @since 2024
        """
        try:
            logger.info(f"创建订单 - 用户ID: {user_id}, 订单类型: {order_type.value}, 消耗积分: {points_cost}")
            
            order_no = generate_order_no()
            order = Order(
                user_id=user_id,
                order_no=order_no,
                order_type=order_type,
                status=OrderStatus.PENDING,
                points_cost=points_cost
            )
            session.add(order)
            await session.commit()
            
            logger.info(f"订单创建成功 - 订单号: {order_no}, 用户ID: {user_id}")
            return order
            
        except Exception as e:
            logger.error(f"创建订单失败 - 用户ID: {user_id}, 错误: {e}")
            await session.rollback()
            raise
    
    @staticmethod
    async def get_order_by_no(session: AsyncSession, order_no: str) -> Order:
        """
        根据订单号获取订单
        
        @param session: 数据库会话
        @param order_no: 订单号
        @return: 订单对象，不存在返回None
        @author seven
        @since 2024
        """
        try:
            logger.debug(f"查询订单 - 订单号: {order_no}")
            result = await session.execute(
                select(Order).where(Order.order_no == order_no)
            )
            order = result.scalar_one_or_none()
            return order
        except Exception as e:
            logger.error(f"查询订单失败 - 订单号: {order_no}, 错误: {e}")
            raise
    
    @staticmethod
    async def update_order_status(
        session: AsyncSession,
        order: Order,
        status: OrderStatus,
        image_url: str = None,
        video_url: str = None,
        error_message: str = None
    ):
        """
        更新订单状态
        
        @param session: 数据库会话
        @param order: 订单对象
        @param status: 新状态
        @param image_url: 图片URL（如果完成）
        @param video_url: 视频URL（如果完成）
        @param error_message: 错误信息（如果失败）
        @author seven
        @since 2024
        """
        try:
            logger.info(f"更新订单状态 - 订单号: {order.order_no}, 新状态: {status.value}")
            order.update_status(status, error_message)
            if image_url:
                order.image_url = image_url
            if video_url:
                order.video_url = video_url
            await session.commit()
            logger.info(f"订单状态更新成功 - 订单号: {order.order_no}, 状态: {status.value}")
        except Exception as e:
            logger.error(f"更新订单状态失败 - 订单号: {order.order_no}, 错误: {e}")
            await session.rollback()
            raise

