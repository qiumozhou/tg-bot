# -*- coding: utf-8 -*-
"""
官方频道检查服务

@author seven
@since 2024
"""
import os
from telegram import Bot
from loguru import logger


class ChannelService:
    """
    频道服务类
    
    @author seven
    @since 2024
    """
    
    @staticmethod
    async def check_user_subscribed(bot: Bot, user_id: int, channel_id: str = None) -> bool:
        """
        检查用户是否关注了官方频道
        
        @param bot: Bot实例
        @param user_id: 用户Telegram ID
        @param channel_id: 频道ID（如果为None，从环境变量读取）
        @return: 是否已关注
        @author seven
        @since 2024
        """
        try:
            if not channel_id:
                channel_id = os.getenv('OFFICIAL_CHANNEL_ID')
                if not channel_id:
                    logger.warning("OFFICIAL_CHANNEL_ID 未配置，跳过频道检查")
                    return True  # 如果未配置，默认通过
            
            logger.info(f"检查用户是否关注频道 - 用户ID: {user_id}, 频道: {channel_id}")
            
            # 获取频道成员信息
            try:
                member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
                is_subscribed = member.status in ['member', 'administrator', 'creator']
                
                logger.info(f"用户频道关注状态 - 用户ID: {user_id}, 频道: {channel_id}, 状态: {member.status}, 已关注: {is_subscribed}")
                return is_subscribed
                
            except Exception as e:
                logger.error(f"获取频道成员信息失败 - 用户ID: {user_id}, 频道: {channel_id}, 错误: {e}")
                # 如果无法获取（可能是频道不存在或权限不足），默认返回True
                return True
                
        except Exception as e:
            logger.error(f"检查用户频道关注状态失败 - 用户ID: {user_id}, 错误: {e}")
            # 出错时默认返回True，避免影响用户体验
            return True

