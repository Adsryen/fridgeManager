# -*- coding: utf-8 -*-
"""用户服务"""
from app.models import User
from app.utils.auth import hash_password, verify_password


class UserService:
    """用户业务逻辑"""
    
    def __init__(self, db):
        self.db = db
    
    def create_user(self, username: str, email: str, password: str) -> User:
        """创建用户"""
        # 检查用户名是否存在
        if self.db.user.find_one({'username': username}):
            raise ValueError('用户名已存在')
        
        # 检查邮箱是否存在
        if self.db.user.find_one({'email': email}):
            raise ValueError('邮箱已被注册')
        
        # 创建用户
        password_hash, salt = hash_password(password)
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            salt=salt
        )
        
        self.db.user.insert_one(user.to_dict())
        return user
    
    def authenticate(self, username: str, password: str) -> User | None:
        """验证用户"""
        user_data = self.db.user.find_one({'username': username})
        if not user_data:
            return None
        
        if not verify_password(password, user_data['password_hash'], user_data['salt']):
            return None
        
        return User.from_dict(user_data)
    
    def get_user_by_id(self, user_id: str) -> User | None:
        """根据 ID 获取用户"""
        user_data = self.db.user.find_one({'_id': user_id})
        if not user_data:
            return None
        return User.from_dict(user_data)
