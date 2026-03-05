# -*- coding: utf-8 -*-
"""应用配置"""
import os


class Config:
    """基础配置"""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE_DIR = os.environ.get('DATABASE_DIR', 'data')
    
    # Flask 配置
    JSON_AS_ASCII = False
    JSON_SORT_KEYS = False
    
    # 会话配置
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 86400  # 24 小时


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    TESTING = False
    
    # 生产环境安全配置
    SESSION_COOKIE_SECURE = True  # 仅 HTTPS


class TestingConfig(Config):
    """测试环境配置"""
    DEBUG = True
    TESTING = True
    DATABASE_DIR = 'test_data'


# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
