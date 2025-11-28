/**
 * 官方频道检查服务
 * 
 * @author seven
 * @since 2024
 */
import TelegramBot from 'node-telegram-bot-api';
import logger from '@/lib/logger';
import { config } from '@/lib/config';

/**
 * 检查用户是否关注了官方频道
 * 
 * @param {TelegramBot} bot - Bot 实例
 * @param {number} userId - 用户 Telegram ID
 * @param {string} channelId - 频道 ID（可选，默认从配置读取）
 * @return {Promise<boolean>} 是否已关注
 * @author seven
 * @since 2024
 */
export async function checkUserSubscribed(
  bot: TelegramBot,
  userId: number,
  channelId?: string
): Promise<boolean> {
  try {
    const channel = channelId || config.officialChannelId;
    if (!channel) {
      logger.warning('OFFICIAL_CHANNEL_ID 未配置，跳过频道检查');
      return true; // 如果未配置，默认通过
    }
    
    logger.info(`检查用户是否关注频道 - 用户ID: ${userId}, 频道: ${channel}`);
    
    // 获取频道成员信息
    try {
      const member = await bot.getChatMember(channel, userId);
      const isSubscribed = ['member', 'administrator', 'creator'].includes(member.status);
      
      logger.info(`用户频道关注状态 - 用户ID: ${userId}, 频道: ${channel}, 状态: ${member.status}, 已关注: ${isSubscribed}`);
      return isSubscribed;
    } catch (error) {
      logger.error(`获取频道成员信息失败 - 用户ID: ${userId}, 频道: ${channel}, 错误: ${error}`);
      // 如果无法获取（可能是频道不存在或权限不足），默认返回True
      return true;
    }
  } catch (error) {
    logger.error(`检查用户频道关注状态失败 - 用户ID: ${userId}, 错误: ${error}`);
    // 出错时默认返回True，避免影响用户体验
    return true;
  }
}

