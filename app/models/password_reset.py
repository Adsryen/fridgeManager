# -*- coding: utf-8 -*-
"""密码重置令牌模型"""
from datetime import datetime, timedelta
import secrets


class PasswordResetToken:
    """密码重置令牌"""
    
    COLLECTION_NAME = 'password_reset_tokens'
    
    @staticmethod
    def create_token(db_client, user_id, email):
        """
        创建密码重置令牌
        
        Args:
            db_client: 数据库客户端
            user_id: 用户ID
            email: 用户邮箱
        
        Returns:
            str: 重置令牌
        """
        # 生成随机令牌
        token = secrets.token_urlsafe(32)
        
        # 设置过期时间（30分钟）
        expires_at = datetime.now() + timedelta(minutes=30)
        
        # 保存到数据库
        token_data = {
            'token': token,
            'user_id': user_id,
            'email': email,
            'created_at': datetime.now(),
            'expires_at': expires_at,
            'used': False
        }
        
        db_client.insert_one(PasswordResetToken.COLLECTION_NAME, token_data)
        
        return token
    
    @staticmethod
    def verify_token(db_client, token):
        """
        验证令牌是否有效
        
        Args:
            db_client: 数据库客户端
            token: 重置令牌
        
        Returns:
            dict: 令牌数据，如果无效则返回None
        """
        token_data = db_client.find_one(
            PasswordResetToken.COLLECTION_NAME,
            {'token': token, 'used': False}
        )
        
        if not token_data:
            return None
        
        # 检查是否过期
        if datetime.now() > token_data['expires_at']:
            return None
        
        return token_data
    
    @staticmethod
    def mark_as_used(db_client, token):
        """
        标记令牌为已使用
        
        Args:
            db_client: 数据库客户端
            token: 重置令牌
        """
        db_client.update_one(
            PasswordResetToken.COLLECTION_NAME,
            {'token': token},
            {'$set': {'used': True, 'used_at': datetime.now()}}
        )
    
    @staticmethod
    def cleanup_expired(db_client):
        """
        清理过期的令牌
        
        Args:
            db_client: 数据库客户端
        """
        now = datetime.now()
        all_tokens = db_client.find(PasswordResetToken.COLLECTION_NAME, {})
        expired_tokens = [token for token in all_tokens if token.get('expires_at') and token['expires_at'] < now]
        
        for token in expired_tokens:
            db_client.delete_one(PasswordResetToken.COLLECTION_NAME, {'_id': token['_id']})
