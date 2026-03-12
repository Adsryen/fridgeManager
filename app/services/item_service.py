# -*- coding: utf-8 -*-
"""物品服务"""
from datetime import datetime
from app.models import Item
from app.services.item_history_service import ItemHistoryService


class ItemService:
    """物品业务逻辑"""
    
    def __init__(self, db):
        self.db = db
        self.history_service = ItemHistoryService(db)
    
    def create_item(self, user_id: str, name: str, expire_date: datetime, 
                   place: str, num: int, item_type: str, fridge_id: str = 'public') -> Item:
        """创建物品"""
        item = Item(
            user_id=user_id,
            Name=name,
            ExpireDate=expire_date,
            Place=place,
            Num=num,
            Type=item_type
        )
        
        # 添加冰箱ID
        item_dict = item.to_dict()
        item_dict['fridge_id'] = fridge_id
        
        self.db.item.insert_one(item_dict)
        
        # 记录创建历史
        self.history_service.record_action(
            item_id=item._id,
            fridge_id=fridge_id,
            user_id=user_id,
            action='created',
            item_data=item_dict
        )
        
        return item
    
    def get_user_items(self, user_id: str) -> list[dict]:
        """获取用户所有物品"""
        return self.db.item.find({'user_id': user_id})
    
    def search_items(self, user_id: str, keyword: str = None) -> list[dict]:
        """搜索物品"""
        if not keyword:
            return self.get_user_items(user_id)
        
        # SQLite 兼容的模糊搜索
        all_items = self.db.item.find({'user_id': user_id})
        return [item for item in all_items if keyword.lower() in item.get('Name', '').lower()]
    
    def get_items_by_status(self, user_id: str, expired: bool, date: datetime) -> list[dict]:
        """根据过期状态获取物品"""
        date_str = date.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        all_items = self.db.item.find({'user_id': user_id})
        
        if expired:
            return [item for item in all_items if item.get('ExpireDate', '') < date_str]
        else:
            return [item for item in all_items if item.get('ExpireDate', '') >= date_str]
    
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
        # 获取更新前的数据
        old_item = self.db.item.find_one({'_id': item_id, 'user_id': user_id})
        if not old_item:
            return False
        
        result = self.db.item.update_one(
            {'_id': item_id, 'user_id': user_id},
            {'$set': kwargs}
        )
        
        if result.modified_count > 0:
            # 获取更新后的数据
            new_item = self.db.item.find_one({'_id': item_id, 'user_id': user_id})
            
            # 记录更新历史
            self.history_service.record_action(
                item_id=item_id,
                fridge_id=old_item.get('fridge_id', 'public'),
                user_id=user_id,
                action='updated',
                item_data=new_item
            )
        
        return result.modified_count > 0
    
    def delete_item(self, user_id: str, item_id: str) -> bool:
        """删除物品"""
        # 获取删除前的数据
        item = self.db.item.find_one({'_id': item_id, 'user_id': user_id})
        if not item:
            return False
        
        result = self.db.item.delete_one({'_id': item_id, 'user_id': user_id})
        
        if result.deleted_count > 0:
            # 记录删除历史
            self.history_service.record_action(
                item_id=item_id,
                fridge_id=item.get('fridge_id', 'public'),
                user_id=user_id,
                action='deleted',
                item_data=item
            )
        
        return result.deleted_count > 0
    
    def take_out_item(self, user_id: str, item_id: str, quantity: int) -> bool:
        """取出物品"""
        item = self.db.item.find_one({'_id': item_id, 'user_id': user_id})
        if not item:
            return False
        
        current_num = item.get('Num', 0)
        if current_num < quantity:
            raise ValueError('取出数量超过库存')
        
        new_num = current_num - quantity
        
        if new_num == 0:
            # 数量为0时删除物品
            result = self.db.item.delete_one({'_id': item_id, 'user_id': user_id})
            success = result.deleted_count > 0
        else:
            # 更新数量
            result = self.db.item.update_one(
                {'_id': item_id, 'user_id': user_id},
                {'$set': {'Num': new_num}}
            )
            success = result.modified_count > 0
        
        if success:
            # 记录取出历史
            self.history_service.record_action(
                item_id=item_id,
                fridge_id=item.get('fridge_id', 'public'),
                user_id=user_id,
                action='taken_out',
                item_data=item,
                quantity_change=-quantity,
                reason=f'取出 {quantity} 个'
            )
        
        return success
