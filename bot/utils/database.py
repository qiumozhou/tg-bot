# -*- coding: utf-8 -*-
"""
数据库工具

@author seven
@since 2024
"""
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from loguru import logger
from bot.models.base import Base
from bot.models.user import User
from bot.models.order import Order
from bot.models.payment import Payment
from bot.models.transaction import Transaction


# 数据库引擎
_engine = None
_session_factory = None


def get_db_url() -> str:
    """
    获取数据库URL
    
    @return: 数据库URL
    @author seven
    @since 2024
    """
    db_url = os.getenv('DATABASE_URL', 'sqlite+aiosqlite:///./data/bot.db')
    logger.info(f"数据库URL: {db_url}")
    return db_url


async def init_db():
    """
    初始化数据库
    
    @author seven
    @since 2024
    """
    try:
        global _engine, _session_factory
        
        db_url = get_db_url()
        
        # 创建数据目录
        if 'sqlite' in db_url:
            db_path = db_url.split('///')[-1] if '///' in db_url else './data/bot.db'
            db_dir = os.path.dirname(db_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)
                logger.info(f"创建数据库目录: {db_dir}")
        
        # 创建引擎
        _engine = create_async_engine(
            db_url,
            echo=False,
            future=True
        )
        
        # 创建会话工厂
        _session_factory = async_sessionmaker(
            _engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        # 创建表
        async with _engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("数据库初始化完成")
        
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        raise


async def get_db():
    """
    获取数据库会话（生成器函数，用于依赖注入）
    
    @yield: 数据库会话
    @author seven
    @since 2024
    """
    if _session_factory is None:
        raise RuntimeError("数据库未初始化，请先调用 init_db()")
    
    async with _session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


def get_session():
    """
    获取数据库会话上下文管理器
    
    @return: 数据库会话上下文管理器（可直接用于 async with）
    @author seven
    @since 2024
    """
    if _session_factory is None:
        raise RuntimeError("数据库未初始化，请先调用 init_db()")
    # _session_factory() 返回一个 AsyncSession，它本身就是异步上下文管理器
    return _session_factory()

