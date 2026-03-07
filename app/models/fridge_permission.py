# -*- coding: utf-8 -*-
"""冰箱权限模型"""
import uuid
from datetime import datetime
from dataclasses import dataclass


@dataclass
class FridgePermission:
    """冰箱权限数据模型"""
    fridge_id: str
    is_family_shared: bool = False  # 是否家庭共享
    is_editable_by_family: bool = False  # 家庭成员是否可编辑
    _id: str = None
    created_at: datetime | str = None
    updated_at: datetime | str = None
    
    def __post_init__(self):
        if self._id is None:
            self._id = uuid.uuid4().hex
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            '_id': self._id,
            'fridge_id': self.fridge_id,
            'is_family_shared': self.is_family_shared,
            'is_editable_by_family': self.is_editable_by_family,
            'created_at': self.created_at if isinstance(self.created_at, str) 
                         else self.created_at.strftime('%Y-%m-%dT%H:%M:%S.000Z'),
            'updated_at': self.updated_at if isinstance(self.updated_at, str)
                         else self.updated_at.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'FridgePermission':
        """从字典创建冰箱权限"""
        return cls(
            _id=data.get('_id'),
            fridge_id=data['fridge_id'],
            is_family_shared=data.get('is_family_shared', False),
            is_editable_by_family=data.get('is_editable_by_family', False),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
