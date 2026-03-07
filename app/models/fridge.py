# -*- coding: utf-8 -*-
"""冰箱模型"""
import uuid
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Fridge:
    """冰箱数据模型"""
    user_id: str
    name: str
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
            'user_id': self.user_id,
            'name': self.name,
            'created_at': self.created_at if isinstance(self.created_at, str) 
                         else self.created_at.strftime('%Y-%m-%dT%H:%M:%S.000Z'),
            'updated_at': self.updated_at if isinstance(self.updated_at, str)
                         else self.updated_at.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Fridge':
        """从字典创建冰箱"""
        return cls(
            _id=data.get('_id'),
            user_id=data['user_id'],
            name=data['name'],
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
