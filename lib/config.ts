/**
 * 配置管理
 * 
 * @author seven
 * @since 2024
 */
import dotenv from 'dotenv';

dotenv.config();

/**
 * 应用配置
 * 
 * @author seven
 * @since 2024
 */
export const config = {
  // Telegram Bot 配置
  botToken: process.env.BOT_TOKEN || '',
  
  // 数据库配置
  databaseUrl: process.env.DATABASE_URL || 'file:./data/bot.db',
  
  // 支付配置
  alipay: {
    appId: process.env.ALIPAY_APP_ID || '',
    privateKey: process.env.ALIPAY_PRIVATE_KEY || '',
    publicKey: process.env.ALIPAY_PUBLIC_KEY || '',
    notifyUrl: process.env.ALIPAY_NOTIFY_URL || '',
  },
  
  wechat: {
    appId: process.env.WECHAT_APP_ID || '',
    mchId: process.env.WECHAT_MCH_ID || '',
    apiKey: process.env.WECHAT_API_KEY || '',
    notifyUrl: process.env.WECHAT_NOTIFY_URL || '',
  },
  
  usdt: {
    apiKey: process.env.USTD_API_KEY || '',
    notifyUrl: process.env.USTD_NOTIFY_URL || '',
  },
  
  // 官方频道配置
  officialChannelId: process.env.OFFICIAL_CHANNEL_ID || '',
  
  // 图像生成API配置
  imageGeneration: {
    apiUrl: process.env.IMAGE_GENERATION_API_URL || '',
    apiKey: process.env.IMAGE_GENERATION_API_KEY || '',
  },
  
  // 视频生成API配置
  videoGeneration: {
    apiUrl: process.env.VIDEO_GENERATION_API_URL || '',
    apiKey: process.env.VIDEO_GENERATION_API_KEY || '',
  },
  
  // 日志配置
  logLevel: process.env.LOG_LEVEL || 'INFO',
  logFile: process.env.LOG_FILE || 'logs/bot.log',
  
  // Webhook 配置
  webhookUrl: process.env.WEBHOOK_URL || '',
  webhookSecret: process.env.WEBHOOK_SECRET || '',
  
  // 代理配置（用于访问 Telegram API）
  proxy: process.env.PROXY_URL || undefined,
};

/**
 * 验证必要的配置项
 * 
 * @author seven
 * @since 2024
 */
export function validateConfig(): void {
  if (!config.botToken) {
    throw new Error('BOT_TOKEN 环境变量未设置，请在 .env 文件中配置');
  }
}

