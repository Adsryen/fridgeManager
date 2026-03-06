# -*- coding: utf-8 -*-
"""Flask 应用工厂"""
import os
import secrets
from flask import Flask
from app.utils.database import SQLiteMongoLikeClient


# 全局数据库客户端
db_client = None


def create_app(config_name: str = 'default') -> Flask:
    """创建 Flask 应用实例
    
    Args:
        config_name: 配置名称 (default, development, production, testing)
        
    Returns:
        Flask 应用实例
    """
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    # 加载配置
    from config.settings import config
    app.config.from_object(config[config_name])
    
    # 设置密钥
    app.secret_key = app.config.get('SECRET_KEY') or secrets.token_hex(32)
    
    # 初始化数据库
    global db_client
    db_dir = app.config.get('DATABASE_DIR', 
                            os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data'))
    db_client = SQLiteMongoLikeClient(db_dir=db_dir)
    
    # 注册蓝图
    from app.routes import auth_bp, item_bp, main_bp, admin_bp, settings_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(item_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(settings_bp, url_prefix='/settings')
    
    # 注册错误处理
    register_error_handlers(app)
    
    return app


def register_error_handlers(app: Flask):
    """注册错误处理器"""
    
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500
