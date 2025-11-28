/**
 * 菜单定义
 * 
 * @author seven
 * @since 2024
 */

/**
 * Inline Keyboard Markup 类型定义（兼容 Workers）
 */
export interface InlineKeyboardButton {
  text: string;
  callback_data?: string;
  url?: string;
}

export interface InlineKeyboardMarkup {
  inline_keyboard: InlineKeyboardButton[][];
}

/**
 * 欢迎消息
 */
export const WELCOME_MESSAGE = '🤖 黑科技AIOOXX，一款可以【去衣】【换脸】 【OOXX】的机器人，功能强大，欢迎体验。';

/**
 * 免责声明
 */
export const DISCLAIMER_MESSAGE = `本机器人的使用条款和免责声明

➡️ 本机器人是一个根据用户输入生成图像的机器人。
➡️ 但是，该机器人不对用户使用它创建的任何特定图像负责。
➡️ 使用应该由用户自行全面认识和负责。
➡️ 用户在利用此机器人时必须对内容和行为承担全部责任。
➡️ 本机器人仅是一个工具，无法控制或对用户的使用方式负责。
⭐️ 禁止用户使用机器人传播可能对个人或组织造成伤害的图像。
⭐️ 不会存储用户提交的任何信息或图像，除了TelegramID，也没有权利将用户信息用于任何目的。`;

/**
 * 获取主菜单键盘
 * 
 * @return {InlineKeyboardMarkup} 主菜单键盘
 * @author seven
 * @since 2024
 */
export function getMainMenuKeyboard(): InlineKeyboardMarkup {
  return {
    inline_keyboard: [
      [
        { text: '👗 脱衣', callback_data: 'menu_strip' },
        { text: '💋 胸部爱抚', callback_data: 'menu_breast' },
        { text: '🫦 自慰', callback_data: 'menu_masturbate' },
      ],
      [
        { text: '💦 颜射', callback_data: 'menu_facial' },
        { text: '👄 口交', callback_data: 'menu_oral' },
        { text: '✋ 手交', callback_data: 'menu_handjob' },
      ],
      [
        { text: '🔥 性交', callback_data: 'menu_sex' },
      ],
      [
        { text: '📢 进入官方频道', url: 'https://t.me/your_official_channel' },
      ],
      [
        { text: '👤 个人中心', callback_data: 'menu_profile' },
        { text: '💰 获积分', callback_data: 'menu_points' },
        { text: '📣 官方频道', callback_data: 'menu_channel' },
      ],
    ],
  };
}

/**
 * 获取脱衣菜单键盘
 * 
 * @return {InlineKeyboardMarkup} 脱衣菜单键盘
 * @author seven
 * @since 2024
 */
export function getStripMenuKeyboard(): InlineKeyboardMarkup {
  return {
    inline_keyboard: [
      [
        { text: '🖼️ 图片脱衣', callback_data: 'strip_image' },
        { text: '🎬 视频脱衣', callback_data: 'strip_video' },
      ],
      [
        { text: '⬅️ 返回主菜单', callback_data: 'menu_main' },
      ],
    ],
  };
}

/**
 * 获取积分菜单键盘
 * 
 * @return {InlineKeyboardMarkup} 积分菜单键盘
 * @author seven
 * @since 2024
 */
export function getPointsMenuKeyboard(): InlineKeyboardMarkup {
  return {
    inline_keyboard: [
      [
        { text: '💳 充值获积分', callback_data: 'points_recharge' },
        { text: '🎁 分享获积分', callback_data: 'points_share' },
      ],
      [
        { text: '⬅️ 返回主菜单', callback_data: 'menu_main' },
      ],
    ],
  };
}

/**
 * 获取充值菜单键盘
 * 
 * @return {InlineKeyboardMarkup} 充值菜单键盘
 * @author seven
 * @since 2024
 */
export function getRechargeMenuKeyboard(): InlineKeyboardMarkup {
  return {
    inline_keyboard: [
      [
        { text: '💰 20积分/20元', callback_data: 'recharge_20' },
        { text: '💎 55积分/50元', callback_data: 'recharge_55' },
      ],
      [
        { text: '💵 120积分/100元', callback_data: 'recharge_120' },
        { text: '💶 250积分/200元', callback_data: 'recharge_250' },
      ],
      [
        { text: '⬅️ 返回', callback_data: 'menu_points' },
      ],
    ],
  };
}

/**
 * 获取支付方式键盘
 * 
 * @param {string} packageKey - 套餐 key
 * @return {InlineKeyboardMarkup} 支付方式键盘
 * @author seven
 * @since 2024
 */
export function getPaymentMethodKeyboard(packageKey: string): InlineKeyboardMarkup {
  return {
    inline_keyboard: [
      [
        { text: '₿ USDT', callback_data: `pay_${packageKey}_usdt` },
        { text: '💚 微信', callback_data: `pay_${packageKey}_wechat` },
        { text: '💙 支付宝', callback_data: `pay_${packageKey}_alipay` },
      ],
      [
        { text: '⬅️ 返回', callback_data: 'points_recharge' },
      ],
    ],
  };
}

