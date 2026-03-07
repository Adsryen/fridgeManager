# -*- coding: utf-8 -*-
"""用户认证工具"""
import hashlib
import secrets
from functools import wraps
from flask import session, redirect, url_for, request, abort


def hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    """密码哈希加密
    
    Args:
        password: 明文密码
        salt: 盐值，如果为 None 则自动生成
        
    Returns:
        (password_hash, salt) 元组
    """
    if salt is None:
        salt = secrets.token_hex(16)
    
    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    return pwd_hash.hex(), salt


def verify_password(password: str, password_hash: str, salt: str) -> bool:
    """验证密码
    
    Args:
        password: 用户输入的密码
        password_hash: 存储的密码哈希
        salt: 盐值
        
    Returns:
        密码是否正确
    """
    pwd_hash, _ = hash_password(password, salt)
    return pwd_hash == password_hash


def login_required(f):
    """登录验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """管理员权限验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login', next=request.url))
        
        if not session.get('is_admin', False):
            abort(403)  # Forbidden
        
        return f(*args, **kwargs)
    return decorated_function


def get_current_user_id() -> str | None:
    """获取当前登录用户 ID"""
    return session.get('user_id')


def get_effective_user_id() -> str:
    """获取有效的用户 ID（用于物品查询）
    
    如果用户已登录且选择了私人冰箱，返回用户 ID
    否则返回 'public' 表示公共冰箱
    """
    # 如果用户选择查看公共冰箱
    if session.get('view_mode') == 'public':
        return 'public'
    
    # 如果管理员选择查看特定用户的冰箱
    if session.get('is_admin') and session.get('view_user_id'):
        return session.get('view_user_id')
    
    # 如果用户已登录，返回用户 ID
    user_id = session.get('user_id')
    if user_id:
        return user_id
    
    # 未登录用户默认使用公共冰箱
    return 'public'


def is_viewing_public() -> bool:
    """检查当前是否在查看公共冰箱"""
    return get_effective_user_id() == 'public'


def get_current_username() -> str | None:
    """获取当前登录用户名"""
    return session.get('username')


def get_current_username() -> str | None:
    """获取当前登录用户名"""
    return session.get('username')


def is_admin() -> bool:
    """检查当前用户是否是管理员"""
    return session.get('is_admin', False)
