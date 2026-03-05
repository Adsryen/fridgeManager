# -*- coding: utf-8 -*-
"""用户认证模块"""
import hashlib
import secrets
from functools import wraps
from flask import session, redirect, url_for, request


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
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def get_current_user_id() -> str | None:
    """获取当前登录用户 ID"""
    return session.get('user_id')


def get_current_username() -> str | None:
    """获取当前登录用户名"""
    return session.get('username')
