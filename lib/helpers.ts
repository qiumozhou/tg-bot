/**
 * 辅助工具函数
 * 
 * @author seven
 * @since 2024
 */
import logger from './logger';

/**
 * 生成订单号
 * 格式: 时间戳 + 10位随机数字
 * 
 * @return {string} 订单号
 * @author seven
 * @since 2024
 */
export function generateOrderNo(): string {
  try {
    const timestamp = new Date().toISOString().replace(/[-:T]/g, '').replace(/\..+/, '').slice(0, 14);
    const randomStr = Math.floor(Math.random() * 10000000000).toString().padStart(10, '0');
    const orderNo = `${timestamp}${randomStr}`;
    logger.debug(`生成订单号: ${orderNo}`);
    return orderNo;
  } catch (error) {
    logger.error(`生成订单号失败: ${error}`);
    throw error;
  }
}

/**
 * 生成推广码
 * 生成8位大写字母数字组合
 * 
 * @return {string} 推广码
 * @author seven
 * @since 2024
 */
export function generateReferralCode(): string {
  try {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let code = '';
    for (let i = 0; i < 8; i++) {
      code += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    logger.debug(`生成推广码: ${code}`);
    return code;
  } catch (error) {
    logger.error(`生成推广码失败: ${error}`);
    throw error;
  }
}

/**
 * 根据积分获取用户等级
 * 
 * @param {number} points - 积分数量
 * @return {string} 等级 (P1-P5)
 * @author seven
 * @since 2024
 */
export function getUserLevel(points: number): string {
  try {
    if (points >= 10000) {
      return 'P5';
    } else if (points >= 5000) {
      return 'P4';
    } else if (points >= 2000) {
      return 'P3';
    } else if (points >= 500) {
      return 'P2';
    } else {
      return 'P1';
    }
  } catch (error) {
    logger.error(`获取用户等级失败 - 积分: ${points}, 错误: ${error}`);
    return 'P1';
  }
}

