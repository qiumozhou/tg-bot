/**
 * Telegram Bot Polling 模式（用于本地开发）
 * 
 * @author seven
 * @since 2024
 */
import TelegramBot from 'node-telegram-bot-api';
import { config, validateConfig } from '@/lib/config';
import logger from '@/lib/logger';
import { initDatabase } from '@/lib/prisma';
import { handleStartCommand } from '@/handlers/startHandler';
import { handleCallbackQuery } from '@/handlers/callbackHandler';
import { handlePhotoMessage, handleTextMessage } from '@/handlers/messageHandler';

let bot: TelegramBot | null = null;

/**
 * 启动 Polling 模式（用于本地开发）
 * 
 * @author seven
 * @since 2024
 */
export async function startPolling(): Promise<void> {
  try {
    logger.info('='.repeat(80));
    logger.info('启动 Telegram Bot (Polling 模式)...');
    logger.info('='.repeat(80));
    
    // 验证配置
    validateConfig();
    
    // 初始化数据库
    await initDatabase();
    logger.info('数据库初始化完成');
    
    // 配置 Bot 选项
    const botOptions: any = {
      polling: true,
    };
    
    // 如果配置了代理，添加代理配置
    if (config.proxy) {
      logger.info(`使用代理: ${config.proxy}`);
      // node-telegram-bot-api 使用 request 库，代理配置格式
      botOptions.request = {
        proxy: config.proxy,
      };
    }
    
    // 创建 Bot 实例（使用 polling 模式）
    bot = new TelegramBot(config.botToken, botOptions);
    
    // 获取 Bot 信息
    const botInfo = await bot.getMe();
    logger.info('='.repeat(80));
    logger.info(`Bot 连接成功！`);
    logger.info(`Bot 用户名: @${botInfo.username}`);
    logger.info(`Bot 名称: ${botInfo.first_name}`);
    logger.info(`Bot ID: ${botInfo.id}`);
    logger.info('='.repeat(80));
    
    // 注册全局消息监听器 - 打印所有收到的消息
    bot.on('message', (msg) => {
      try {
        console.log('\n' + '='.repeat(80));
        console.log('📨 收到新消息');
        console.log('='.repeat(80));
        console.log('完整消息对象:');
        console.log(JSON.stringify(msg, null, 2));
        console.log('='.repeat(80));
        
        // 打印关键信息
        const user = msg.from;
        const chat = msg.chat;
        console.log(`👤 用户信息:`);
        console.log(`   - 用户ID: ${user?.id}`);
        console.log(`   - 用户名: @${user?.username || '无'}`);
        console.log(`   - 姓名: ${user?.first_name || ''} ${user?.last_name || ''}`.trim());
        console.log(`💬 聊天信息:`);
        console.log(`   - 聊天ID: ${chat?.id}`);
        console.log(`   - 聊天类型: ${chat?.type}`);
        console.log(`   - 聊天标题: ${chat?.title || chat?.first_name || '无'}`);
        
        if (msg.text) {
          console.log(`📝 文本内容: ${msg.text}`);
        }
        if (msg.photo) {
          console.log(`🖼️  图片消息 - 有 ${msg.photo.length} 个尺寸`);
        }
        if (msg.video) {
          console.log(`🎥 视频消息 - 时长: ${msg.video.duration}秒`);
        }
        if (msg.document) {
          console.log(`📄 文档消息 - 文件名: ${msg.document.file_name}`);
        }
        if (msg.sticker) {
          console.log(`😀 贴纸消息 - Emoji: ${msg.sticker.emoji}`);
        }
        if (msg.voice) {
          console.log(`🎤 语音消息 - 时长: ${msg.voice.duration}秒`);
        }
        if (msg.location) {
          console.log(`📍 位置消息 - 纬度: ${msg.location.latitude}, 经度: ${msg.location.longitude}`);
        }
        if (msg.contact) {
          console.log(`👥 联系人消息 - 电话: ${msg.contact.phone_number}`);
        }
        
        console.log(`🕐 时间: ${new Date(msg.date * 1000).toLocaleString('zh-CN')}`);
        console.log('='.repeat(80) + '\n');
        
        // 同时记录到日志文件
        logger.info(`收到消息 - 用户ID: ${user?.id}, 用户名: @${user?.username || '无'}, 类型: ${msg.photo ? '图片' : msg.video ? '视频' : msg.text ? '文本' : '其他'}`);
      } catch (error) {
        logger.error(`打印消息失败: ${error}`);
      }
    });
    
    // 注册命令处理器
    bot.onText(/\/start(.*)/, async (msg, match) => {
      try {
        logger.info(`收到 /start 命令 - 用户ID: ${msg.from?.id}, 用户名: ${msg.from?.username}, 参数: ${match?.[1] || ''}`);
        await handleStartCommand(bot!, msg, match?.[1]?.trim());
      } catch (error) {
        logger.error(`处理 /start 命令失败: ${error}`);
        throw error;
      }
    });
    
    // 注册回调查询处理器
    bot.on('callback_query', async (query) => {
      try {
        // 打印回调查询信息
        console.log('\n' + '='.repeat(80));
        console.log('🔘 收到回调查询');
        console.log('='.repeat(80));
        console.log('完整回调查询对象:');
        console.log(JSON.stringify(query, null, 2));
        console.log('='.repeat(80));
        console.log(`👤 用户ID: ${query.from.id}`);
        console.log(`👤 用户名: @${query.from.username || '无'}`);
        console.log(`📌 回调数据: ${query.data}`);
        console.log(`💬 消息ID: ${query.message?.message_id || '无'}`);
        console.log('='.repeat(80) + '\n');
        
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
    
    logger.info('='.repeat(80));
    logger.info('Bot 正在轮询中，等待消息...');
    logger.info('按 Ctrl+C 停止Bot');
    logger.info('='.repeat(80));
    
  } catch (error) {
    logger.error(`启动 Polling 失败: ${error}`);
    throw error;
  }
}

// 如果直接运行此文件，启动 polling
if (require.main === module) {
  startPolling().catch((error) => {
    logger.error(`启动失败: ${error}`);
    process.exit(1);
  });
  
  // 优雅关闭
  process.on('SIGINT', () => {
    logger.info('收到停止信号，Bot 正在关闭...');
    if (bot) {
      bot.stopPolling();
    }
    process.exit(0);
  });
}

