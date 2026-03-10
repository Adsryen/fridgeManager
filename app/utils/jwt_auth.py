# -*- coding: utf-8 -*-
"""JWT 认证工具模块"""

import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from config.settings import Config


def generate_token(user_id: str, username: str, email: str, is_admin: bool) -> str:
    """生成 JWT Token
    
    Args:
        user_id: 用户 ID
        username: 用户名
        email: 邮箱
        is_admin: 是否为管理员
        
    Returns:
        JWT Token 字符串
    """
    payload = {
        'user_id': user_id,
        'username': username,
        'email': email,
        'is_admin': is_admin,
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')


def verify_token(token: str) -> dict | None:
    """验证 JWT Token
    
    Args:
        token: JWT Token 字符串
        
    Returns:
        解码后的 payload 字典，如果验证失败返回 None
    """
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        # Token 已过期
        return None
    except jwt.InvalidTokenError:
        # Token 无效
        return None


def jwt_required(f):
    """JWT 认证装饰器
    
    用于保护需要认证的路由
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'success': False, 'error': '未提供认证令牌'}), 401
        
        payload = verify_token(token)
        if not payload:
            return jsonify({'success': False, 'error': '认证令牌无效或已过期'}), 401
        
        # 将用户信息注入到 request 上下文
        request.user_id = payload['user_id']
        request.username = payload['username']
        request.is_admin = payload['is_admin']
        
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """管理员权限装饰器
    
    用于保护需要管理员权限的路由
    自动包含 JWT 认证检查
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 先进行 JWT 认证
        token = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'success': False, 'error': '未提供认证令牌'}), 401
        
        payload = verify_token(token)
        if not payload:
            return jsonify({'success': False, 'error': '认证令牌无效或已过期'}), 401
        
        # 将用户信息注入到 request 上下文
        request.user_id = payload['user_id']
        request.username = payload['username']
        request.is_admin = payload['is_admin']
        
        # 检查管理员权限
        if not request.is_admin:
            return jsonify({'success': False, 'error': '权限不足'}), 403
        
        return f(*args, **kwargs)
    return decorated_function


def get_current_user() -> dict:
    """获取当前登录用户信息
    
    必须在使用 @jwt_required 装饰器的路由中调用
    
    Returns:
        包含用户信息的字典
    """
    return {
        'user_id': request.user_id,
        'username': request.username,
        'is_admin': request.is_admin
    }


def jwt_optional(f):
    """可选 JWT 认证装饰器
    
    允许游客访问，但如果提供了 token 则验证
    用于公共冰箱等允许游客访问的路由
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if token:
            # 如果提供了 token，验证它
            payload = verify_token(token)
            if payload:
                # Token 有效，设置用户信息
                request.user_id = payload['user_id']
                request.username = payload['username']
                request.is_admin = payload['is_admin']
            else:
                # Token 无效，作为游客处理
                request.user_id = 'public'
                request.username = '游客'
                request.is_admin = False
        else:
            # 没有 token，作为游客处理
            request.user_id = 'public'
            request.username = '游客'
            request.is_admin = False
        
        return f(*args, **kwargs)
    return decorated_function
