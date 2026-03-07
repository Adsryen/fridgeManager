# -*- coding: utf-8 -*-
"""冰箱服务"""
from datetime import datetime
from app.models import Fridge


class FridgeService:
    """冰箱业务逻辑"""
    
    def __init__(self, db):
        self.db = db
    
    def create_fridge(self, user_id: str, name: str) -> Fridge:
        """创建冰箱"""
        fridge = Fridge(
            user_id=user_id,
            name=name
        )
        
        self.db.fridge.insert_one(fridge.to_dict())
        return fridge
    
    def get_user_fridges(self, user_id: str) -> list[dict]:
        """获取用户所有冰箱"""
        return self.db.fridge.find({'user_id': user_id})
    
    def get_fridge(self, fridge_id: str, user_id: str) -> dict | None:
        """获取单个冰箱"""
        return self.db.fridge.find_one({'_id': fridge_id, 'user_id': user_id})
    
    def update_fridge(self, fridge_id: str, user_id: str, name: str) -> bool:
        """更新冰箱名称"""
        result = self.db.fridge.update_one(
            {'_id': fridge_id, 'user_id': user_id},
            {'$set': {
                'name': name,
                'updated_at': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z')
            }}
        )
        return result.modified_count > 0
    
    def delete_fridge(self, fridge_id: str, user_id: str) -> bool:
        """删除冰箱"""
        result = self.db.fridge.delete_one({'_id': fridge_id, 'user_id': user_id})
        return result.deleted_count > 0
    
    def get_fridge_item_count(self, fridge_id: str) -> int:
        """获取冰箱中的物品数量"""
        items = self.db.item.find({'fridge_id': fridge_id})
        return len(items)
