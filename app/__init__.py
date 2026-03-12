# -*- coding: utf-8 -*-
"""Flask 应用工厂"""
import os
import secrets
from flask import Flask
from flask_session import Session
from flask_cors import CORS
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
    
    # 配置 CORS - 支持跨域请求
    cors_origins = app.config.get('CORS_ORIGINS', [
        'http://localhost:5173', 
        'http://127.0.0.1:5173',
        'http://localhost:8080',
        'http://127.0.0.1:8080'
    ])
    CORS(app, 
         resources={r"/*": {
             "origins": cors_origins,
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"],
             "expose_headers": ["Content-Type", "Authorization"],
             "supports_credentials": True,
             "max_age": 3600
         }})
    
    # 设置密钥 - 使用固定密钥或从环境变量读取，避免重启后session失效
    secret_key = app.config.get('SECRET_KEY')
    if not secret_key:
        # 尝试从文件读取，如果不存在则生成并保存
        secret_key_file = os.path.join(app.config.get('DATABASE_DIR', 'data'), '.secret_key')
        if os.path.exists(secret_key_file):
            with open(secret_key_file, 'r') as f:
                secret_key = f.read().strip()
        else:
            secret_key = secrets.token_hex(32)
            os.makedirs(os.path.dirname(secret_key_file), exist_ok=True)
            with open(secret_key_file, 'w') as f:
                f.write(secret_key)
    app.secret_key = secret_key
    
    # 确保session目录存在
    session_dir = app.config.get('SESSION_FILE_DIR')
    if session_dir and not os.path.exists(session_dir):
        os.makedirs(session_dir, exist_ok=True)
    
    # 初始化Flask-Session（必须在设置secret_key之后）
    Session(app)
    
    # 初始化数据库
    global db_client
    db_dir = app.config.get('DATABASE_DIR', 
                            os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data'))
    db_client = SQLiteMongoLikeClient(db_dir=db_dir)
    
    # 注册蓝图
    from app.routes import auth_bp, item_bp, main_bp, admin_bp, settings_bp
    from app.routes.fridge import fridge_bp
    from app.routes.family import family_bp
    from app.routes.item_history import item_history_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(item_bp, url_prefix='/item')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(settings_bp, url_prefix='/settings')
    app.register_blueprint(fridge_bp, url_prefix='/fridge')
    app.register_blueprint(family_bp, url_prefix='/family')
    app.register_blueprint(item_history_bp)
    
    # 注册健康检查端点
    @app.route('/health')
    def health_check():
        """健康检查端点"""
        return {'status': 'healthy', 'service': 'fridge-manager'}, 200
    
    # 注册错误处理
    register_error_handlers(app)
    
    # 注册会话超时检查
    register_session_timeout(app)
    
    # 启动定时任务调度器
    from app.tasks import start_scheduler
    start_scheduler(db_client.fridge)
    
    return app


def register_session_timeout(app: Flask):
    """注册会话超时检查"""
    from flask import session, request, redirect, url_for
    from datetime import datetime, timedelta
    
    @app.before_request
    def check_session_timeout():
        """检查会话是否超时"""
        # 排除不需要检查的路径
        if request.endpoint in ['auth.login', 'auth.register', 'static', 'main.index']:
            return
        
        # 只检查已登录用户
        if 'user_id' not in session:
            return
        
        # 获取系统设置
        from app.models.system_settings import SystemSettings
        system_settings = SystemSettings(db_client.fridge)
        settings = system_settings.get_all_settings()
        session_timeout = settings.get('session_timeout')
        
        # 确保session_timeout是有效的数字
        if session_timeout is None or not isinstance(session_timeout, (int, float)):
            session_timeout = 60  # 默认60分钟
        else:
            session_timeout = int(session_timeout)
        
        # 检查最后活动时间
        last_activity = session.get('last_activity')
        if last_activity:
            try:
                last_activity_time = datetime.fromisoformat(last_activity)
                if datetime.now() - last_activity_time > timedelta(minutes=session_timeout):
                    # 会话超时，清除session
                    session.clear()
                    if request.is_json:
                        from flask import jsonify
                        return jsonify({'error': '会话已超时，请重新登录'}), 401
                    return redirect(url_for('auth.login'))
            except (ValueError, TypeError):
                # 如果时间格式错误,重新设置
                pass
        
        # 更新最后活动时间
        session['last_activity'] = datetime.now().isoformat()
        # 确保session被标记为已修改
        session.modified = True


def register_error_handlers(app: Flask):
    """注册错误处理器"""
    
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500
