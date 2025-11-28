/**
 * 消息处理器
 * 
 * @author seven
 * @since 2024
 */
import TelegramBot from 'node-telegram-bot-api';
import logger from '@/lib/logger';
import { getUserByTelegramId, deductPoints } from '@/services/userService';
import { checkUserSubscribed } from '@/services/channelService';
import { createOrder } from '@/services/orderService';
import { OrderType } from '@/lib/constants';
import { config } from '@/lib/config';

/**
 * 处理图片消息
 * 
 * @param {TelegramBot} bot - Bot 实例
 * @param {TelegramBot.Message} msg - 消息对象
 * @author seven
 * @since 2024
 */
export async function handlePhotoMessage(
  bot: TelegramBot,
  msg: TelegramBot.Message
): Promise<void> {
  try {
    const user = msg.from;
    if (!user) {
      logger.error('收到图片消息但无法获取用户信息');
      return;
    }
    
    const photo = msg.photo?.[msg.photo.length - 1]; // 获取最大尺寸的图片
    if (!photo) {
      return;
    }
    
    logger.info(`收到图片消息 - 用户ID: ${user.id}, 文件ID: ${photo.file_id}`);
    
    // 获取用户信息
    const dbUser = await getUserByTelegramId(BigInt(user.id));
    if (!dbUser) {
      await bot.sendMessage(msg.chat.id, '请先使用 /start 命令开始使用机器人。');
      return;
    }
    
    // 检查是否关注官方频道
    const isSubscribed = await checkUserSubscribed(bot, user.id);
    if (!isSubscribed) {
      const channelId = config.officialChannelId || '@your_official_channel';
      await bot.sendMessage(
        msg.chat.id,
        `❌ 请先关注官方频道才能使用此功能！\n\n官方频道：${channelId}\n关注后请重新上传图片。`
      );
      return;
    }
    
    // 检查用户积分（默认图片处理，5积分）
    const pointsRequired = 5;
    if (dbUser.points < pointsRequired) {
      await bot.sendMessage(
        msg.chat.id,
        `❌ 你的积分不足。当前积分：${dbUser.points}，需要积分：${pointsRequired}，请先获取足够积分`
      );
      return;
    }
    
    // 扣除积分并创建订单
    const success = await deductPoints(dbUser, pointsRequired);
    if (!success) {
      await bot.sendMessage(
        msg.chat.id,
        `❌ 积分扣除失败。当前积分：${dbUser.points}，需要积分：${pointsRequired}`
      );
      return;
    }
    
    // 创建订单
    const order = await createOrder(BigInt(user.id), OrderType.IMAGE, pointsRequired);
    
    await bot.sendMessage(
      msg.chat.id,
      `✅ 图片接收成功，订单号：${order.orderNo}\n正在处理中，请稍候...`
    );
    
    // TODO: 调用图像生成API处理图片
    // 这里应该调用实际的图像生成服务
    
    // 暂时模拟处理
    await bot.sendMessage(
      msg.chat.id,
      `⚠️ 图像生成功能待实现\n订单号：${order.orderNo}\n已扣除积分：${pointsRequired}\n剩余积分：${dbUser.points - pointsRequired}`
    );
    
    logger.info(`图片处理完成 - 订单号: ${order.orderNo}, 用户ID: ${user.id}`);
  } catch (error) {
    logger.error(`处理图片消息失败 - 用户ID: ${msg.from?.id}, 错误: ${error}`);
    
    if (msg.chat) {
      try {
        await bot.sendMessage(msg.chat.id, '处理图片时发生错误，请稍后重试。');
      } catch (sendError) {
        logger.error(`发送错误消息失败: ${sendError}`);
      }
    }
    
    throw error;
  }
}

/**
 * 处理文本消息
 * 
 * @param {TelegramBot} bot - Bot 实例
 * @param {TelegramBot.Message} msg - 消息对象
 * @author seven
 * @since 2024
 */
export async function handleTextMessage(
  bot: TelegramBot,
  msg: TelegramBot.Message
): Promise<void> {
  try {
    const user = msg.from;
    const text = msg.text;
    
    logger.info(`收到文本消息 - 用户ID: ${user?.id}, 内容: ${text}`);
    
    // 这里可以根据文本内容进行不同的处理
    // 暂时回复提示信息
    await bot.sendMessage(msg.chat.id, '请使用菜单按钮进行操作。');
  } catch (error) {
    logger.error(`处理文本消息失败 - 用户ID: ${msg.from?.id}, 错误: ${error}`);
    
    if (msg.chat) {
      try {
        await bot.sendMessage(msg.chat.id, '处理消息时发生错误，请稍后重试。');
      } catch (sendError) {
        logger.error(`发送错误消息失败: ${sendError}`);
      }
    }
    
    throw error;
  }
}

