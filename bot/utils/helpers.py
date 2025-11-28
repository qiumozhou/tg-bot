# -*- coding: utf-8 -*-
"""
辅助工具函数

@author seven
@since 2024
"""
import random
import string
import uuid
from datetime import datetime
from loguru import logger


def generate_order_no() -> str:
    """
    生成订单号
    
    @return: 订单号
    @author seven
    @since 2024
    """
    try:
        # 格式: 时间戳 + 随机字符
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_str = ''.join(random.choices(string.digits, k=10))
        order_no = f"{timestamp}{random_str}"
        logger.debug(f"生成订单号: {order_no}")
        return order_no
    except Exception as e:
        logger.error(f"生成订单号失败: {e}")
        raise


def generate_referral_code() -> str:
    """
    生成推广码
    
    @return: 推广码
    @author seven
    @since 2024
    """
    try:
        # 生成8位大写字母数字组合
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        logger.debug(f"生成推广码: {code}")
        return code
    except Exception as e:
        logger.error(f"生成推广码失败: {e}")
        raise


def get_user_level(points: int) -> str:
    """
    根据积分获取用户等级
    
    @param points: 积分数量
    @return: 等级
    @author seven
    @since 2024
    """
    try:
        # 等级规则可以根据需求调整
        if points >= 10000:
            return "P5"
        elif points >= 5000:
            return "P4"
        elif points >= 2000:
            return "P3"
        elif points >= 500:
            return "P2"
        else:
            return "P1"
    except Exception as e:
        logger.error(f"获取用户等级失败 - 积分: {points}, 错误: {e}")
        return "P1"

