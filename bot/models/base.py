# -*- coding: utf-8 -*-
"""
数据库基础模型

@author seven
@since 2024
"""
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime

Base = declarative_base()


class BaseModel(Base):
    """
    基础模型类，包含通用字段
    
    @author seven
    @since 2024
    """
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment='更新时间')

