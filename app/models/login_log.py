# -*- coding: utf-8 -*-
"""登录日志模型"""
from datetime import datetime
import uuid


class LoginLog:
    """登录日志数据模型"""
    
    def __init__(self, db):
        self.db = db
        self.collection = db.login_logs
    
    def log_login(self, user_id: str, username: str, success: bool, ip_address: str = None, user_agent: str = None, error_message: str = None):
        """记录登录日志
        
        Args:
            user_id: 用户ID
            username: 用户名
            success: 是否成功
            ip_address: IP地址
            user_agent: 用户代理
            error_message: 错误信息（失败时）
        """
        log_entry = {
            '_id': str(uuid.uuid4()),
            'user_id': user_id,
            'username': username,
            'success': success,
            'ip_address': ip_address,
            'user_agent': user_agent,
            'error_message': error_message,
            'login_time': datetime.now().isoformat()
        }
        
        self.collection.insert_one(log_entry)
        return log_entry
    
    def get_user_logs(self, user_id: str, limit: int = 50) -> list[dict]:
        """获取用户的登录日志"""
        logs = self.collection.find({'user_id': user_id})
        # 按时间倒序
        logs = sorted(logs, key=lambda x: x.get('login_time', ''), reverse=True)
        return logs[:limit]
    
    def get_all_logs(self, limit: int = 100) -> list[dict]:
        """获取所有登录日志"""
        logs = self.collection.find()
        # 按时间倒序
        logs = sorted(logs, key=lambda x: x.get('login_time', ''), reverse=True)
        return logs[:limit]
    
    def get_failed_attempts(self, username: str, minutes: int = 30) -> int:
        """获取指定时间内的失败登录次数"""
        from datetime import timedelta
        
        cutoff_time = (datetime.now() - timedelta(minutes=minutes)).isoformat()
        all_logs = self.collection.find({
            'username': username,
            'success': False
        })
        recent_logs = [log for log in all_logs if log.get('login_time', '') >= cutoff_time]
        return len(recent_logs)
    
    def clear_old_logs(self, days: int = 90):
        """清理旧日志"""
        from datetime import timedelta
        
        cutoff_time = (datetime.now() - timedelta(days=days)).isoformat()
        all_logs = self.collection.find({})
        old_logs = [log for log in all_logs if log.get('login_time', '') < cutoff_time]
        
        deleted_count = 0
        for log in old_logs:
            result = self.collection.delete_one({'_id': log['_id']})
            deleted_count += result.deleted_count
        
        return deleted_count
