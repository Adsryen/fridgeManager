# -*- coding: utf-8 -*-
"""物品历史记录模型"""
import uuid
from datetime import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class ItemHistory:
    """物品历史记录数据模型"""
    item_id: str
    fridge_id: str
    user_id: str
    action: str  # 'created', 'updated', 'deleted', 'taken_out'
    item_data: dict  # 物品的完整数据快照
    quantity_change: Optional[int] = None  # 数量变化（取出时使用）
    reason: Optional[str] = None  # 操作原因
    _id: str = None
    created_at: datetime | str = None
    
    def __post_init__(self):
        if self._id is None:
            self._id = uuid.uuid4().hex
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            '_id': self._id,
            'item_id': self.item_id,
            'fridge_id': self.fridge_id,
            'user_id': self.user_id,
            'action': self.action,
            'item_data': self.item_data,
            'quantity_change': self.quantity_change,
            'reason': self.reason,
            'created_at': self.created_at if isinstance(self.created_at, str) 
                         else self.created_at.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ItemHistory':
        """从字典创建物品历史记录"""
        return cls(
            _id=data.get('_id'),
            item_id=data['item_id'],
            fridge_id=data['fridge_id'],
            user_id=data['user_id'],
            action=data['action'],
            item_data=data['item_data'],
            quantity_change=data.get('quantity_change'),
            reason=data.get('reason'),
            created_at=data.get('created_at')
        )