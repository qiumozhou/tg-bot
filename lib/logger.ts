/**
 * 日志工具（适配 Cloudflare Workers）
 * 
 * Cloudflare Workers 不支持文件系统，所有日志输出到 console
 * 可以在 Cloudflare Dashboard 中查看实时日志
 * 
 * @author seven
 * @since 2025-11-28
 */

/**
 * 日志级别枚举
 */
enum LogLevel {
  ERROR = 'ERROR',
  WARN = 'WARN',
  INFO = 'INFO',
  DEBUG = 'DEBUG',
}

/**
 * 日志类
 * 
 * @author seven
 * @since 2025-11-28
 */
class Logger {
  private logLevel: LogLevel;

  constructor() {
    // 从环境变量获取日志级别，默认为 INFO
    const level = (process.env.LOG_LEVEL || 'INFO').toUpperCase();
    this.logLevel = LogLevel[level as keyof typeof LogLevel] || LogLevel.INFO;
  }

  /**
   * 格式化日志消息
   * 
   * @param {LogLevel} level - 日志级别
   * @param {any} message - 日志消息
   * @param {any[]} args - 额外参数
   * @return {string} 格式化后的日志字符串
   * @author seven
   * @since 2025-11-28
   */
  private formatMessage(level: LogLevel, message: any, ...args: any[]): string {
    const timestamp = new Date().toISOString();
    const formattedArgs = args.length > 0 ? ' ' + JSON.stringify(args) : '';
    return `[${timestamp}] [${level}] ${message}${formattedArgs}`;
  }

  /**
   * 判断是否应该记录该级别的日志
   * 
   * @param {LogLevel} level - 日志级别
   * @return {boolean} 是否应该记录
   * @author seven
   * @since 2025-11-28
   */
  private shouldLog(level: LogLevel): boolean {
    const levels = [LogLevel.ERROR, LogLevel.WARN, LogLevel.INFO, LogLevel.DEBUG];
    const currentLevelIndex = levels.indexOf(this.logLevel);
    const messageLevelIndex = levels.indexOf(level);
    return messageLevelIndex <= currentLevelIndex;
  }

  /**
   * 记录错误日志
   * 
   * @param {any} message - 日志消息
   * @param {any[]} args - 额外参数
   * @author seven
   * @since 2025-11-28
   */
  error(message: any, ...args: any[]): void {
    if (this.shouldLog(LogLevel.ERROR)) {
      console.error(this.formatMessage(LogLevel.ERROR, message, ...args));
    }
  }

  /**
   * 记录警告日志
   * 
   * @param {any} message - 日志消息
   * @param {any[]} args - 额外参数
   * @author seven
   * @since 2025-11-28
   */
  warn(message: any, ...args: any[]): void {
    if (this.shouldLog(LogLevel.WARN)) {
      console.warn(this.formatMessage(LogLevel.WARN, message, ...args));
    }
  }

  /**
   * 记录警告日志（warning 别名，兼容旧代码）
   * 
   * @param {any} message - 日志消息
   * @param {any[]} args - 额外参数
   * @author seven
   * @since 2025-11-28
   */
  warning(message: any, ...args: any[]): void {
    this.warn(message, ...args);
  }

  /**
   * 记录信息日志
   * 
   * @param {any} message - 日志消息
   * @param {any[]} args - 额外参数
   * @author seven
   * @since 2025-11-28
   */
  info(message: any, ...args: any[]): void {
    if (this.shouldLog(LogLevel.INFO)) {
      console.log(this.formatMessage(LogLevel.INFO, message, ...args));
    }
  }

  /**
   * 记录调试日志
   * 
   * @param {any} message - 日志消息
   * @param {any[]} args - 额外参数
   * @author seven
   * @since 2025-11-28
   */
  debug(message: any, ...args: any[]): void {
    if (this.shouldLog(LogLevel.DEBUG)) {
      console.debug(this.formatMessage(LogLevel.DEBUG, message, ...args));
    }
  }
}

// 导出单例实例
const logger = new Logger();
export default logger;

