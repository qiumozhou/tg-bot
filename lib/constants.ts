/**
 * 常量定义
 * 
 * @author seven
 * @since 2024
 */

/**
 * 订单类型
 */
export const OrderType = {
  IMAGE: 'IMAGE',
  VIDEO: 'VIDEO',
} as const;

export type OrderType = typeof OrderType[keyof typeof OrderType];

/**
 * 订单状态
 */
export const OrderStatus = {
  PENDING: 'PENDING',
  PROCESSING: 'PROCESSING',
  COMPLETED: 'COMPLETED',
  FAILED: 'FAILED',
} as const;

export type OrderStatus = typeof OrderStatus[keyof typeof OrderStatus];

/**
 * 支付方式
 */
export const PaymentMethod = {
  ALIPAY: 'ALIPAY',
  WECHAT: 'WECHAT',
  USDT: 'USDT',
} as const;

export type PaymentMethod = typeof PaymentMethod[keyof typeof PaymentMethod];

/**
 * 支付状态
 */
export const PaymentStatus = {
  PENDING: 'PENDING',
  PAID: 'PAID',
  FAILED: 'FAILED',
  EXPIRED: 'EXPIRED',
} as const;

export type PaymentStatus = typeof PaymentStatus[keyof typeof PaymentStatus];

/**
 * 交易类型
 */
export const TransactionType = {
  CHARGE: 'CHARGE',
  CONSUME: 'CONSUME',
  REFERRAL: 'REFERRAL',
} as const;

export type TransactionType = typeof TransactionType[keyof typeof TransactionType];

