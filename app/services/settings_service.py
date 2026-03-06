# -*- coding: utf-8 -*-
"""用户设置服务"""
from app.models.user_settings import UserSettings


class SettingsService:
    """用户设置业务逻辑"""
    
    def __init__(self, db):
        self.db = db
    
    def get_user_settings(self, user_id: str) -> UserSettings:
        """获取用户设置，如果不存在则创建默认设置"""
        settings_data = self.db.settings.find_one({'user_id': user_id})
        
        if not settings_data:
            # 创建默认设置
            settings = UserSettings(user_id=user_id)
            self.db.settings.insert_one(settings.to_dict())
            return settings
        
        return UserSettings.from_dict(settings_data)
    
    def update_settings(self, user_id: str, **kwargs) -> bool:
        """更新用户设置"""
        # 过滤允许更新的字段
        allowed_fields = {
            'notify_expiring', 'notify_days', 'items_per_page', 
            'default_view', 'profile_public'
        }
        update_data = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not update_data:
            return False
        
        # 检查设置是否存在
        settings = self.db.settings.find_one({'user_id': user_id})
        
        if not settings:
            # 创建新设置
            new_settings = UserSettings(user_id=user_id, **update_data)
            self.db.settings.insert_one(new_settings.to_dict())
            return True
        
        # 更新现有设置
        result = self.db.settings.update_one(
            {'user_id': user_id},
            {'$set': update_data}
        )
        return result.modified_count > 0
