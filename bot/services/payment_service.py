# -*- coding: utf-8 -*-
"""
支付服务

@author seven
@since 2024
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from loguru import logger
from bot.models.payment import Payment, PaymentMethod, PaymentStatus
from bot.utils.helpers import generate_order_no
from datetime import datetime


class PaymentService:
    """
    支付服务类
    
    @author seven
    @since 2024
    """
    
    # 积分套餐配置
    POINTS_PACKAGES = {
        "20": {"points": 20, "price": 20.00},
        "55": {"points": 55, "price": 50.00},
        "120": {"points": 120, "price": 100.00},
        "250": {"points": 250, "price": 200.00},
    }
    
    @staticmethod
    async def create_payment(
        session: AsyncSession,
        user_id: int,
        package_key: str,
        payment_method: PaymentMethod
    ) -> Payment:
        """
        创建支付订单
        
        @param session: 数据库会话
        @param user_id: 用户Telegram ID
        @param package_key: 套餐key
        @param payment_method: 支付方式
        @return: 支付对象
        @author seven
        @since 2024
        """
        try:
            logger.info(f"创建支付订单 - 用户ID: {user_id}, 套餐: {package_key}, 支付方式: {payment_method.value}")
            
            if package_key not in PaymentService.POINTS_PACKAGES:
                raise ValueError(f"无效的套餐key: {package_key}")
            
            package = PaymentService.POINTS_PACKAGES[package_key]
            order_no = generate_order_no()
            
            payment = Payment(
                user_id=user_id,
                order_no=order_no,
                payment_method=payment_method,
                status=PaymentStatus.PENDING,
                amount=package["price"],
                points=package["points"]
            )
            session.add(payment)
            await session.commit()
            
            logger.info(f"支付订单创建成功 - 订单号: {order_no}, 用户ID: {user_id}, 金额: {package['price']}, 积分: {package['points']}")
            return payment
            
        except Exception as e:
            logger.error(f"创建支付订单失败 - 用户ID: {user_id}, 错误: {e}")
            await session.rollback()
            raise
    
    @staticmethod
    async def get_payment_by_no(session: AsyncSession, order_no: str) -> Payment:
        """
        根据订单号获取支付订单
        
        @param session: 数据库会话
        @param order_no: 订单号
        @return: 支付对象，不存在返回None
        @author seven
        @since 2024
        """
        try:
            logger.debug(f"查询支付订单 - 订单号: {order_no}")
            result = await session.execute(
                select(Payment).where(Payment.order_no == order_no)
            )
            payment = result.scalar_one_or_none()
            return payment
        except Exception as e:
            logger.error(f"查询支付订单失败 - 订单号: {order_no}, 错误: {e}")
            raise
    
    @staticmethod
    async def update_payment_url(session: AsyncSession, payment: Payment, payment_url: str):
        """
        更新支付链接
        
        @param session: 数据库会话
        @param payment: 支付对象
        @param payment_url: 支付链接
        @author seven
        @since 2024
        """
        try:
            logger.info(f"更新支付链接 - 订单号: {payment.order_no}, URL: {payment_url}")
            payment.payment_url = payment_url
            await session.commit()
            logger.info(f"支付链接更新成功 - 订单号: {payment.order_no}")
        except Exception as e:
            logger.error(f"更新支付链接失败 - 订单号: {payment.order_no}, 错误: {e}")
            await session.rollback()
            raise
    
    @staticmethod
    async def complete_payment(session: AsyncSession, payment: Payment, paid_at: str = None):
        """
        完成支付
        
        @param session: 数据库会话
        @param payment: 支付对象
        @param paid_at: 支付时间
        @author seven
        @since 2024
        """
        try:
            logger.info(f"完成支付 - 订单号: {payment.order_no}")
            if not paid_at:
                paid_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            payment.update_status(PaymentStatus.PAID, paid_at)
            await session.commit()
            logger.info(f"支付完成 - 订单号: {payment.order_no}, 支付时间: {paid_at}")
        except Exception as e:
            logger.error(f"完成支付失败 - 订单号: {payment.order_no}, 错误: {e}")
            await session.rollback()
            raise

