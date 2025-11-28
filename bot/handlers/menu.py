# -*- coding: utf-8 -*-
"""
菜单相关处理器

@author seven
@since 2024
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from loguru import logger


# 欢迎消息
WELCOME_MESSAGE = """黑科技AIOOXX，一款可以【去衣】【换脸】 【OOXX】的机器人，功能强大，欢迎体验。"""

# 免责声明
DISCLAIMER_MESSAGE = """本机器人的使用条款和免责声明

➡️ 本机器人是一个根据用户输入生成图像的机器人。
➡️ 但是，该机器人不对用户使用它创建的任何特定图像负责。
➡️ 使用应该由用户自行全面认识和负责。
➡️ 用户在利用此机器人时必须对内容和行为承担全部责任。
➡️ 本机器人仅是一个工具，无法控制或对用户的使用方式负责。
⭐️ 禁止用户使用机器人传播可能对个人或组织造成伤害的图像。
⭐️ 不会存储用户提交的任何信息或图像，除了TelegramID，也没有权利将用户信息用于任何目的。"""


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """
    获取主菜单键盘
    
    @return: 主菜单键盘
    @author seven
    @since 2024
    """
    try:
        keyboard = [
            [
                InlineKeyboardButton("脱衣", callback_data="menu_strip"),
                InlineKeyboardButton("胸部爱抚", callback_data="menu_breast"),
                InlineKeyboardButton("自慰", callback_data="menu_masturbate")
            ],
            [
                InlineKeyboardButton("颜射", callback_data="menu_facial"),
                InlineKeyboardButton("口交", callback_data="menu_oral"),
                InlineKeyboardButton("手交", callback_data="menu_handjob")
            ],
            [
                InlineKeyboardButton("性交", callback_data="menu_sex")
            ],
            [
                InlineKeyboardButton("进入官方频道", url="https://t.me/your_official_channel")
            ],
            [
                InlineKeyboardButton("个人中心", callback_data="menu_profile"),
                InlineKeyboardButton("获积分", callback_data="menu_points"),
                InlineKeyboardButton("官方频道", callback_data="menu_channel")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    except Exception as e:
        logger.error(f"生成主菜单键盘失败: {e}")
        raise


def get_strip_menu_keyboard() -> InlineKeyboardMarkup:
    """
    获取脱衣菜单键盘
    
    @return: 脱衣菜单键盘
    @author seven
    @since 2024
    """
    try:
        keyboard = [
            [
                InlineKeyboardButton("图片脱衣", callback_data="strip_image"),
                InlineKeyboardButton("视频脱衣", callback_data="strip_video")
            ],
            [
                InlineKeyboardButton("⬅️ 返回主菜单", callback_data="menu_main")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    except Exception as e:
        logger.error(f"生成脱衣菜单键盘失败: {e}")
        raise


def get_points_menu_keyboard() -> InlineKeyboardMarkup:
    """
    获取积分菜单键盘
    
    @return: 积分菜单键盘
    @author seven
    @since 2024
    """
    try:
        keyboard = [
            [
                InlineKeyboardButton("充值获积分", callback_data="points_recharge"),
                InlineKeyboardButton("分享获积分", callback_data="points_share")
            ],
            [
                InlineKeyboardButton("⬅️ 返回主菜单", callback_data="menu_main")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    except Exception as e:
        logger.error(f"生成积分菜单键盘失败: {e}")
        raise


def get_recharge_menu_keyboard() -> InlineKeyboardMarkup:
    """
    获取充值菜单键盘
    
    @return: 充值菜单键盘
    @author seven
    @since 2024
    """
    try:
        keyboard = [
            [
                InlineKeyboardButton("20积分20元", callback_data="recharge_20"),
                InlineKeyboardButton("55积分50元", callback_data="recharge_55")
            ],
            [
                InlineKeyboardButton("120积分100元", callback_data="recharge_120"),
                InlineKeyboardButton("250积分200元", callback_data="recharge_250")
            ],
            [
                InlineKeyboardButton("⬅️ 返回", callback_data="menu_points")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    except Exception as e:
        logger.error(f"生成充值菜单键盘失败: {e}")
        raise


def get_payment_method_keyboard(package_key: str) -> InlineKeyboardMarkup:
    """
    获取支付方式键盘
    
    @param package_key: 套餐key
    @return: 支付方式键盘
    @author seven
    @since 2024
    """
    try:
        keyboard = [
            [
                InlineKeyboardButton("USTD", callback_data=f"pay_{package_key}_usdt"),
                InlineKeyboardButton("微信", callback_data=f"pay_{package_key}_wechat"),
                InlineKeyboardButton("支付宝", callback_data=f"pay_{package_key}_alipay")
            ],
            [
                InlineKeyboardButton("⬅️ 返回", callback_data="points_recharge")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    except Exception as e:
        logger.error(f"生成支付方式键盘失败: {e}")
        raise

