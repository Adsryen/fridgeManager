# -*- coding: utf-8 -*-
"""物品历史记录服务"""
from typing import List, Dict, Optional
from app.models.item_history import ItemHistory


class ItemHistoryService:
    """物品历史记录服务"""
    
    def __init__(self, db):
        self.db = db
    
    def record_action(self, item_id: str, fridge_id: str, user_id: str, 
                     action: str, item_data: dict, quantity_change: Optional[int] = None,
                     reason: Optional[str] = None) -> ItemHistory:
        """记录物品操作历史"""
        history = ItemHistory(
            item_id=item_id,
            fridge_id=fridge_id,
            user_id=user_id,
            action=action,
            item_data=item_data.copy(),  # 创建数据副本
            quantity_change=quantity_change,
            reason=reason
        )
        
        # 保存到数据库
        self.db.item_history.insert_one(history.to_dict())
        return history
    
    def get_fridge_history(self, fridge_id: str, limit: int = 50) -> List[Dict]:
        """获取冰箱的物品历史记录"""
        # SQLite 不支持 MongoDB 风格的 sort 和 limit，需要直接使用 SQL
        histories = self.db.item_history.find({'fridge_id': fridge_id})
        
        # 手动排序和限制
        histories = sorted(histories, key=lambda x: x.get('created_at', ''), reverse=True)
        histories = histories[:limit]
        
        # 为每条记录添加用户信息
        for history in histories:
            user = self.db.user.find_one({'_id': history['user_id']})
            if user:
                history['username'] = user['username']
            else:
                history['username'] = '未知用户'
        
        return histories
    
    def get_item_history(self, item_id: str) -> List[Dict]:
        """获取特定物品的历史记录"""
        histories = self.db.item_history.find({'item_id': item_id})
        
        # 手动排序
        histories = sorted(histories, key=lambda x: x.get('created_at', ''), reverse=True)
        
        # 为每条记录添加用户信息
        for history in histories:
            user = self.db.user.find_one({'_id': history['user_id']})
            if user:
                history['username'] = user['username']
            else:
                history['username'] = '未知用户'
        
        return histories
    
    def get_deleted_items(self, fridge_id: str, limit: int = 20) -> List[Dict]:
        """获取已删除的物品列表（用于恢复）"""
        deleted_histories = self.db.item_history.find({
            'fridge_id': fridge_id,
            'action': 'deleted'
        })
        
        # 手动排序和限制
        deleted_histories = sorted(deleted_histories, key=lambda x: x.get('created_at', ''), reverse=True)
        deleted_histories = deleted_histories[:limit]
        
        # 为每条记录添加用户信息
        for history in deleted_histories:
            user = self.db.user.find_one({'_id': history['user_id']})
            if user:
                history['username'] = user['username']
            else:
                history['username'] = '未知用户'
        
        return deleted_histories
    
    def restore_item(self, history_id: str, user_id: str) -> Dict:
        """恢复已删除的物品"""
        # 获取历史记录
        history = self.db.item_history.find_one({'_id': history_id})
        if not history or history['action'] != 'deleted':
            raise ValueError('历史记录不存在或不是删除记录')
        
        # 检查物品是否已经存在
        existing_item = self.db.item.find_one({'_id': history['item_id']})
        if existing_item:
            raise ValueError('物品已存在，无法恢复')
        
        # 恢复物品数据
        item_data = history['item_data'].copy()
        item_data['_id'] = history['item_id']  # 保持原有ID
        
        # 插入物品
        self.db.item.insert_one(item_data)
        
        # 记录恢复操作
        self.record_action(
            item_id=history['item_id'],
            fridge_id=history['fridge_id'],
            user_id=user_id,
            action='restored',
            item_data=item_data,
            reason=f'从历史记录恢复 (原删除记录: {history_id})'
        )
        
        return item_data
    
    def cleanup_old_history(self, days: int = 30):
        """清理旧的历史记录"""
        from datetime import datetime, timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_str = cutoff_date.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        
        # SQLite 兼容的查询方式
        old_histories = self.db.item_history.find({})
        to_delete = []
        for history in old_histories:
            if history.get('created_at', '') < cutoff_str:
                to_delete.append(history['_id'])
        
        deleted_count = 0
        for history_id in to_delete:
            result = self.db.item_history.delete_one({'_id': history_id})
            deleted_count += result.deleted_count
        
        return deleted_count