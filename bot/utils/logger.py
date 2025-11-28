# -*- coding: utf-8 -*-
"""
日志配置工具

@author seven
@since 2024
"""
import sys
import os
from loguru import logger


def setup_logger(log_level: str = "INFO", log_file: str = "logs/bot.log"):
    """
    配置日志系统
    
    @param log_level: 日志级别
    @param log_file: 日志文件路径
    @author seven
    @since 2024
    """
    try:
        # 移除默认处理器
        logger.remove()
        
        # 创建日志目录
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        
        # 添加控制台输出
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level=log_level,
            colorize=True
        )
        
        # 添加文件输出
        logger.add(
            log_file,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level=log_level,
            rotation="10 MB",
            retention="7 days",
            compression="zip",
            encoding="utf-8"
        )
        
        logger.info(f"日志系统初始化完成 - 日志级别: {log_level}, 日志文件: {log_file}")
        
    except Exception as e:
        print(f"日志系统初始化失败: {e}")
        raise

