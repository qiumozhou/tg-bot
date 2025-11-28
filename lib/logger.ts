/**
 * 日志工具
 * 
 * @author seven
 * @since 2024
 */
import winston from 'winston';
import path from 'path';
import fs from 'fs';

// 确保 logs 目录存在
const logsDir = path.join(process.cwd(), 'logs');
if (!fs.existsSync(logsDir)) {
  fs.mkdirSync(logsDir, { recursive: true });
}

/**
 * 创建 Winston logger 实例
 * 
 * @author seven
 * @since 2024
 */
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
    winston.format.errors({ stack: true }),
    winston.format.splat(),
    winston.format.json()
  ),
  defaultMeta: { service: 'tg-bot' },
  transports: [
    // 错误日志写入文件
    new winston.transports.File({
      filename: path.join(logsDir, 'error.log'),
      level: 'error',
      maxsize: 10485760, // 10MB
      maxFiles: 7,
    }),
    // 所有日志写入文件
    new winston.transports.File({
      filename: path.join(logsDir, 'bot.log'),
      maxsize: 10485760, // 10MB
      maxFiles: 7,
    }),
  ],
});

// 开发环境同时输出到控制台
if (process.env.NODE_ENV !== 'production') {
  logger.add(
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.printf(({ timestamp, level, message, ...meta }) => {
          const metaStr = Object.keys(meta).length ? JSON.stringify(meta, null, 2) : '';
          return `${timestamp} | ${level} | ${message} ${metaStr}`;
        })
      ),
    })
  );
}

export default logger;

