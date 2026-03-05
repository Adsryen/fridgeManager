# -*- coding: utf-8 -*-
"""物品服务"""
from datetime import datetime
from app.models import Item


class ItemService:
    """物品业务逻辑"""
    
    def __init__(self, db):
        self.db = db
    
    def create_item(self, user_id: str, name: str, expire_date: datetime, 
                   place: str, num: int, item_type: str) -> Item:
        """创建物品"""
        item = Item(
            user_id=user_id,
            Name=name,
            ExpireDate=expire_date,
            Place=place,
            Num=num,
            Type=item_type
        )
        
        self.db.item.insert_one(item.to_dict())
        return item
    
    def get_user_items(self, user_id: str) -> list[dict]:
        """获取用户所有物品"""
        return self.db.item.find({'user_id': user_id})
    
    def search_items(self, user_id: str, keyword: str = None) -> list[dict]:
        """搜索物品"""
        if not keyword:
            return self.get_user_items(user_id)
        return self.db.item.find({'user_id': user_id, 'Name': {'$regex': keyword}})
    
    def get_items_by_status(self, user_id: str, expired: bool, date: datetime) -> list[dict]:
        """根据过期状态获取物品"""
        if expired:
            return self.db.item.find({'user_id': user_id, 'ExpireDate': {'$lt': date}})
        else:
            return self.db.item.find({'user_id': user_id, 'ExpireDate': {'$gte': date}})
    
    def get_items_by_place(self, user_id: str, place: str) -> list[dict]:
        """根据位置获取物品"""
        return self.db.item.find({'user_id': user_id, 'Place': place})
    
    def get_items_by_type(self, user_id: str, item_type: str) -> list[dict]:
        """根据类别获取物品"""
        return self.db.item.find({'user_id': user_id, 'Type': item_type})
    
    def get_item(self, user_id: str, item_id: str) -> dict | None:
        """获取单个物品"""
        return self.db.item.find_one({'_id': item_id, 'user_id': user_id})
    
    def update_item(self, user_id: str, item_id: str, **kwargs) -> bool:
        """更新物品"""
        result = self.db.item.update_one(
            {'_id': item_id, 'user_id': user_id},
            {'$set': kwargs}
        )
        return result.modified_count > 0
    
    def delete_item(self, user_id: str, item_id: str) -> bool:
        """删除物品"""
        result = self.db.item.delete_one({'_id': item_id, 'user_id': user_id})
        return result.deleted_count > 0
