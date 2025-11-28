/**
 * Telegram Webhook API 端点
 * 
 * @author seven
 * @since 2024
 */
import type { NextApiRequest, NextApiResponse } from 'next';
import TelegramBot from 'node-telegram-bot-api';
import { config as appConfig, validateConfig } from '@/lib/config';
import logger from '@/lib/logger';
import { initDatabase } from '@/lib/prisma';
import { handleStartCommand } from '@/handlers/startHandler';
import { handleCallbackQuery } from '@/handlers/callbackHandler';
import { handlePhotoMessage, handleTextMessage } from '@/handlers/messageHandler';

let bot: TelegramBot | null = null;

/**
 * 初始化 Bot 实例
 * 
 * @author seven
 * @since 2024
 */
function initBot(): TelegramBot {
  if (bot) {
    return bot;
  }
  
  try {
    validateConfig();
    
    bot = new TelegramBot(appConfig.botToken, { polling: false });
    
    // 注册命令处理器
    bot.onText(/\/start(.*)/, async (msg, match) => {
      try {
        logger.info(`收到 /start 命令 - 用户ID: ${msg.from?.id}, 参数: ${match?.[1]}`);
        await handleStartCommand(bot!, msg, match?.[1]);
      } catch (error) {
        logger.error(`处理 /start 命令失败: ${error}`);
        throw error;
      }
    });
    
    // 注册回调查询处理器
    bot.on('callback_query', async (query) => {
      try {
        logger.info(`收到回调查询 - 用户ID: ${query.from.id}, 数据: ${query.data}`);
        await handleCallbackQuery(bot!, query);
      } catch (error) {
        logger.error(`处理回调查询失败: ${error}`);
        throw error;
      }
    });
    
    // 注册照片消息处理器
    bot.on('photo', async (msg) => {
      try {
        logger.info(`收到图片消息 - 用户ID: ${msg.from?.id}, 文件ID: ${msg.photo?.[msg.photo.length - 1]?.file_id}`);
        await handlePhotoMessage(bot!, msg);
      } catch (error) {
        logger.error(`处理图片消息失败: ${error}`);
        throw error;
      }
    });
    
    // 注册文本消息处理器
    bot.on('message', async (msg) => {
      try {
        // 跳过命令和照片（已单独处理）
        if (msg.text?.startsWith('/') || msg.photo) {
          return;
        }
        logger.info(`收到文本消息 - 用户ID: ${msg.from?.id}, 内容: ${msg.text}`);
        await handleTextMessage(bot!, msg);
      } catch (error) {
        logger.error(`处理文本消息失败: ${error}`);
        throw error;
      }
    });
    
    logger.info('Telegram Bot 初始化完成');
    return bot;
  } catch (error) {
    logger.error(`初始化 Bot 失败: ${error}`);
    throw error;
  }
}

/**
 * API 路由配置
 * 配置 bodyParser 以支持较大的请求体（用于接收 Telegram Webhook）
 */
export const config = {
  api: {
    bodyParser: {
      sizeLimit: '10mb',
    },
  },
};

/**
 * Webhook API 处理函数
 * 
 * @param {NextApiRequest} req - 请求对象
 * @param {NextApiResponse} res - 响应对象
 * @author seven
 * @since 2024
 */
export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    // 处理 CORS 预检请求
    if (req.method === 'OPTIONS') {
      res.setHeader('Access-Control-Allow-Origin', '*');
      res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
      res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
      return res.status(200).end();
    }
    
    // 记录所有请求
    logger.info(`收到 Webhook 请求 - Method: ${req.method}, URL: ${req.url}`);
    
    // 只接受 POST 请求
    if (req.method !== 'POST') {
      logger.warn(`收到非 POST 请求: ${req.method}`);
      res.setHeader('Allow', 'POST, OPTIONS');
      return res.status(405).json({ error: 'Method not allowed' });
    }
    
    // 记录请求体
    logger.info(`Webhook 请求体: ${JSON.stringify(req.body, null, 2)}`);
    
    // 初始化数据库连接
    await initDatabase();
    
    // 初始化 Bot
    if (!bot) {
      logger.info('初始化 Bot 实例...');
      initBot();
    }
    
    // 处理 Telegram 更新
    const update = req.body;
    
    if (!update) {
      logger.warn('收到空的更新对象');
      return res.status(400).json({ error: 'Empty update' });
    }
    
    // 打印收到的更新信息
    console.log('\n' + '='.repeat(80));
    console.log('📨 收到 Webhook 更新');
    console.log('='.repeat(80));
    console.log('完整更新对象:');
    console.log(JSON.stringify(update, null, 2));
    console.log('='.repeat(80));
    
    logger.info(`处理更新 - 更新类型: ${update.message ? 'message' : update.callback_query ? 'callback_query' : 'unknown'}`);
    
    // 使用 Bot 的内部处理逻辑
    if (update.message) {
      // 处理消息
      const msg = update.message;
      
      // 打印消息详细信息
      const user = msg.from;
      const chat = msg.chat;
      console.log(`👤 用户信息:`);
      console.log(`   - 用户ID: ${user?.id}`);
      console.log(`   - 用户名: @${user?.username || '无'}`);
      console.log(`   - 姓名: ${user?.first_name || ''} ${user?.last_name || ''}`.trim());
      console.log(`💬 聊天信息:`);
      console.log(`   - 聊天ID: ${chat?.id}`);
      console.log(`   - 聊天类型: ${chat?.type}`);
      if (msg.text) {
        console.log(`📝 文本内容: ${msg.text}`);
      }
      if (msg.photo) {
        console.log(`🖼️  图片消息`);
      }
      if (msg.video) {
        console.log(`🎥 视频消息`);
      }
      console.log(`🕐 时间: ${new Date(msg.date * 1000).toLocaleString('zh-CN')}`);
      console.log('='.repeat(80) + '\n');
      
      logger.info(`收到消息 - 用户ID: ${msg.from?.id}, 用户名: ${msg.from?.username}, 文本: ${msg.text || '(非文本消息)'}`);
      
      // 处理 /start 命令
      if (msg.text?.startsWith('/start')) {
        const match = msg.text.match(/\/start(.*)/);
        const referralCode = match?.[1]?.trim();
        logger.info(`处理 /start 命令 - 用户ID: ${msg.from?.id}, 推广码: ${referralCode || '无'}`);
        await handleStartCommand(bot!, msg, referralCode);
      }
      // 处理照片
      else if (msg.photo) {
        logger.info(`处理照片消息 - 用户ID: ${msg.from?.id}`);
        await handlePhotoMessage(bot!, msg);
      }
      // 处理文本消息
      else if (msg.text && !msg.text.startsWith('/')) {
        logger.info(`处理文本消息 - 用户ID: ${msg.from?.id}, 内容: ${msg.text}`);
        await handleTextMessage(bot!, msg);
      } else {
        logger.info(`收到其他类型的消息 - 用户ID: ${msg.from?.id}, 类型: ${JSON.stringify(Object.keys(msg))}`);
      }
    }
    // 处理回调查询
    else if (update.callback_query) {
      const query = update.callback_query;
      console.log(`🔘 回调查询:`);
      console.log(`   - 用户ID: ${query.from.id}`);
      console.log(`   - 用户名: @${query.from.username || '无'}`);
      console.log(`   - 回调数据: ${query.data}`);
      console.log('='.repeat(80) + '\n');
      
      logger.info(`处理回调查询 - 用户ID: ${query.from.id}, 数据: ${query.data}`);
      await handleCallbackQuery(bot!, query);
    }
    else {
      logger.warn(`收到未知类型的更新: ${JSON.stringify(Object.keys(update))}`);
    }
    
    logger.info('Webhook 请求处理完成');
    return res.status(200).json({ ok: true });
  } catch (error) {
    logger.error(`处理 Webhook 请求失败: ${error}`);
    logger.error(`错误堆栈: ${error instanceof Error ? error.stack : '无堆栈信息'}`);
    return res.status(500).json({ error: 'Internal server error' });
  }
}

// 初始化 Bot（在模块加载时，仅服务端）
if (typeof window === 'undefined') {
  // 延迟初始化，避免在模块加载时执行
  process.nextTick(() => {
    try {
      if (!bot) {
        initBot();
      }
      initDatabase().catch((error) => {
        logger.error(`数据库初始化失败: ${error}`);
      });
    } catch (error) {
      logger.error(`初始化失败: ${error}`);
    }
  });
}

