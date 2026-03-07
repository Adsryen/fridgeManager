# -*- coding: utf-8 -*-
"""管理员服务"""
from datetime import datetime, timedelta


class AdminService:
    """管理员业务逻辑"""
    
    def __init__(self, db):
        self.db = db
    
    def get_statistics(self) -> dict:
        """获取系统统计信息"""
        # 用户统计
        all_users = self.db.user.find()
        total_users = len(all_users)
        active_users = len([u for u in all_users if u.get('is_active', True)])
        admin_users = len([u for u in all_users if u.get('is_admin', False)])
        
        # 物品统计
        all_items = self.db.item.find()
        total_items = len(all_items)
        
        # 按用户统计物品
        user_items = {}
        for item in all_items:
            user_id = item.get('user_id')
            user_items[user_id] = user_items.get(user_id, 0) + 1
        
        avg_items_per_user = total_items / total_users if total_users > 0 else 0
        
        # 过期物品统计
        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z')
        expired_items = len([i for i in all_items if i.get('ExpireDate', '') < now])
        
        return {
            'users': {
                'total': total_users,
                'active': active_users,
                'inactive': total_users - active_users,
                'admins': admin_users
            },
            'items': {
                'total': total_items,
                'expired': expired_items,
                'valid': total_items - expired_items,
                'avg_per_user': round(avg_items_per_user, 2)
            }
        }
    
    def get_all_users(self) -> list[dict]:
        """获取所有用户"""
        users = self.db.user.find()
        # 隐藏敏感信息
        for user in users:
            user.pop('password_hash', None)
            user.pop('salt', None)
        return users
    
    def get_user_details(self, user_id: str) -> dict | None:
        """获取用户详细信息"""
        user = self.db.user.find_one({'_id': user_id})
        if not user:
            return None
        
        # 隐藏敏感信息
        user.pop('password_hash', None)
        user.pop('salt', None)
        
        # 获取用户物品数量
        items = self.db.item.find({'user_id': user_id})
        user['item_count'] = len(items)
        
        return user
    
    def toggle_user_status(self, user_id: str) -> bool:
        """切换用户激活状态"""
        user = self.db.user.find_one({'_id': user_id})
        if not user:
            return False
        
        new_status = not user.get('is_active', True)
        result = self.db.user.update_one(
            {'_id': user_id},
            {'$set': {'is_active': new_status}}
        )
        return result.modified_count > 0
    
    def toggle_admin_status(self, user_id: str) -> bool:
        """切换用户管理员状态"""
        user = self.db.user.find_one({'_id': user_id})
        if not user:
            return False
        
        new_status = not user.get('is_admin', False)
        result = self.db.user.update_one(
            {'_id': user_id},
            {'$set': {'is_admin': new_status}}
        )
        return result.modified_count > 0
    
    def delete_user(self, user_id: str) -> bool:
        """删除用户及其所有数据"""
        # 删除用户的所有物品
        self.db.item.delete_many({'user_id': user_id})
        
        # 删除用户设置
        self.db.settings.delete_one({'user_id': user_id})
        
        # 删除用户
        result = self.db.user.delete_one({'_id': user_id})
        return result.deleted_count > 0
    
    def reset_user_password(self, user_id: str, new_password: str) -> bool:
        """重置用户密码"""
        from app.utils.auth import hash_password
        
        user = self.db.user.find_one({'_id': user_id})
        if not user:
            return False
        
        # 使用与注册相同的加密方式
        password_hash, salt = hash_password(new_password)
        
        # 更新密码
        result = self.db.user.update_one(
            {'_id': user_id},
            {'$set': {
                'password_hash': password_hash,
                'salt': salt,
                'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }}
        )
        return result.modified_count > 0
    
    def clean_expired_items(self) -> int:
        """清理所有过期物品"""
        from datetime import datetime
        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z')
        
        # 查找所有过期物品
        expired_items = self.db.item.find({'ExpireDate': {'$lt': now}})
        count = len(expired_items)
        
        # 删除过期物品
        if count > 0:
            expired_ids = [item['_id'] for item in expired_items]
            self.db.item.delete_many({'_id': {'$in': expired_ids}})
        
        return count
    
    def get_system_logs(self, limit: int = 100) -> list[dict]:
        """获取系统日志"""
        from app.models.login_log import LoginLog
        
        # 获取登录日志
        login_log = LoginLog(self.db)
        logs = login_log.get_all_logs(limit)
        
        return logs
