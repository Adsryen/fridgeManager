# -*- coding: utf-8 -*-
"""系统设置模型"""
from datetime import datetime


class SystemSettings:
    """系统设置数据模型"""
    
    def __init__(self, db):
        self.db = db
        self.collection = db.system_settings
        self._ensure_defaults()
    
    def _ensure_defaults(self):
        """确保默认设置存在"""
        existing = self.collection.find_one({'_id': 'system'})
        if not existing:
            defaults = self.get_default_settings()
            self.collection.insert_one(defaults)
    
    @staticmethod
    def get_default_settings() -> dict:
        """获取默认设置"""
        return {
            '_id': 'system',
            # 基本设置
            'system_name': '冰箱里面还有啥',
            'system_description': '智能冰箱物品管理',
            'allow_registration': 1,
            'require_email_verification': 0,
            
            # 物品管理设置
            'default_expiry_warning_days': 3,
            'auto_delete_expired': 0,
            'auto_delete_days': 7,
            'max_items_per_user': 0,  # 0表示不限制
            
            # 安全设置
            'min_password_length': 6,
            'session_timeout': 60,  # 分钟
            'enable_login_log': 1,
            'max_login_attempts': 5,
            
            # 邮件服务器设置
            'smtp_server': '',
            'smtp_port': 587,
            'smtp_username': '',
            'smtp_password': '',
            'from_email': '',
            'from_name': '冰箱管理系统',
            
            # 通知设置
            'enable_email_notification': 0,
            'daily_summary_email': 0,
            'summary_email_time': '09:00',
            
            # 系统信息
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
    
    def get_all_settings(self) -> dict:
        """获取所有设置"""
        settings = self.collection.find_one({'_id': 'system'})
        if not settings:
            settings = self.get_default_settings()
            self.collection.insert_one(settings)
        
        # 转换整数为布尔值以便在模板中使用
        bool_fields = [
            'allow_registration', 'require_email_verification',
            'auto_delete_expired', 'enable_login_log',
            'enable_email_notification', 'daily_summary_email'
        ]
        for field in bool_fields:
            if field in settings:
                settings[field] = bool(settings[field])
        
        return settings
    
    def get_setting(self, key: str, default=None):
        """获取单个设置"""
        settings = self.get_all_settings()
        return settings.get(key, default)
    
    def update_settings(self, updates: dict) -> bool:
        """更新设置"""
        try:
            # 转换布尔值为整数
            bool_fields = [
                'allow_registration', 'require_email_verification',
                'auto_delete_expired', 'enable_login_log',
                'enable_email_notification', 'daily_summary_email'
            ]
            for field in bool_fields:
                if field in updates and isinstance(updates[field], bool):
                    updates[field] = 1 if updates[field] else 0
            
            updates['updated_at'] = datetime.now().isoformat()
            result = self.collection.update_one(
                {'_id': 'system'},
                {'$set': updates}
            )
            return result.modified_count > 0 or True
        except Exception as e:
            print(f"更新设置失败: {e}")
            return False
    
    def reset_to_defaults(self) -> bool:
        """重置为默认设置"""
        try:
            defaults = self.get_default_settings()
            self.collection.update_one(
                {'_id': 'system'},
                {'$set': defaults}
            )
            return True
        except Exception as e:
            print(f"重置设置失败: {e}")
            return False
    
    @staticmethod
    def get_settings(db_client):
        """静态方法：获取系统设置（供其他模块使用）"""
        try:
            settings = db_client.find_one('system_settings', {'_id': 'system'})
            if not settings:
                # 如果没有设置，返回默认值
                return SystemSettings.get_default_settings()
            return settings
        except Exception as e:
            print(f"获取系统设置失败: {e}")
            return SystemSettings.get_default_settings()
