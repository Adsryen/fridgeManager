# -*- coding: utf-8 -*-
"""物品模型"""
import uuid
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Item:
    """物品数据模型"""
    user_id: str
    Name: str
    ExpireDate: datetime | str
    Place: str
    Num: int
    Type: str
    _id: str = None
    
    def __post_init__(self):
        if self._id is None:
            self._id = uuid.uuid4().hex
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            '_id': self._id,
            'user_id': self.user_id,
            'Name': self.Name,
            'ExpireDate': self.ExpireDate if isinstance(self.ExpireDate, str) 
                         else self.ExpireDate.strftime('%Y-%m-%dT%H:%M:%S.000Z'),
            'Place': self.Place,
            'Num': self.Num,
            'Type': self.Type
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Item':
        """从字典创建物品"""
        return cls(
            _id=data.get('_id'),
            user_id=data['user_id'],
            Name=data['Name'],
            ExpireDate=data['ExpireDate'],
            Place=data['Place'],
            Num=data['Num'],
            Type=data['Type']
        )
