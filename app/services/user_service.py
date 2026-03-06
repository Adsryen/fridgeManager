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
    
    def check_username_exists(self, username: str) -> bool:
        """检查用户名是否存在"""
        return self.db.user.find_one({'username': username}) is not None
    
    def check_email_exists(self, email: str) -> bool:
        """检查邮箱是否存在"""
        return self.db.user.find_one({'email': email}) is not None
    
    def is_username_available(self, username: str) -> bool:
        """检查用户名是否可用"""
        return not self.check_username_exists(username)
    
    def is_email_available(self, email: str) -> bool:
        """检查邮箱是否可用"""
        return not self.check_email_exists(email)

    def is_username_available(self, username: str) -> bool:
        """检查用户名是否可用"""
        return not self.check_username_exists(username)

    def is_email_available(self, email: str) -> bool:
        """检查邮箱是否可用"""
        return not self.check_email_exists(email)

    
    def update_user(self, user_id: str, **kwargs) -> bool:
        """更新用户信息"""
        # 过滤掉不允许更新的字段
        allowed_fields = {'email'}
        update_data = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not update_data:
            return False
        
        # 如果更新邮箱，检查是否已被使用
        if 'email' in update_data:
            existing = self.db.user.find_one({'email': update_data['email']})
            if existing and existing['_id'] != user_id:
                raise ValueError('邮箱已被其他用户使用')
        
        result = self.db.user.update_one(
            {'_id': user_id},
            {'$set': update_data}
        )
        return result.modified_count > 0
    
    def change_password(self, user_id: str, old_password: str, new_password: str) -> bool:
        """修改密码"""
        user_data = self.db.user.find_one({'_id': user_id})
        if not user_data:
            raise ValueError('用户不存在')
        
        # 验证旧密码
        if not verify_password(old_password, user_data['password_hash'], user_data['salt']):
            raise ValueError('原密码错误')
        
        # 生成新密码哈希
        new_password_hash, new_salt = hash_password(new_password)
        
        result = self.db.user.update_one(
            {'_id': user_id},
            {'$set': {
                'password_hash': new_password_hash,
                'salt': new_salt
            }}
        )
        return result.modified_count > 0
