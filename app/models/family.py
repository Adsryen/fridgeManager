# -*- coding: utf-8 -*-
"""家庭模型"""
import uuid
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Family:
    """家庭数据模型"""
    name: str
    creator_id: str
    family_code: str = None
    _id: str = None
    created_at: datetime | str = None
    updated_at: datetime | str = None
    
    def __post_init__(self):
        if self._id is None:
            self._id = uuid.uuid4().hex
        if self.family_code is None:
            # 生成6位家庭编号
            self.family_code = uuid.uuid4().hex[:6].upper()
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            '_id': self._id,
            'name': self.name,
            'creator_id': self.creator_id,
            'family_code': self.family_code,
            'created_at': self.created_at if isinstance(self.created_at, str) 
                         else self.created_at.strftime('%Y-%m-%dT%H:%M:%S.000Z'),
            'updated_at': self.updated_at if isinstance(self.updated_at, str)
                         else self.updated_at.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Family':
        """从字典创建家庭"""
        return cls(
            _id=data.get('_id'),
            name=data['name'],
            creator_id=data['creator_id'],
            family_code=data.get('family_code'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )


@dataclass
class FamilyMember:
    """家庭成员数据模型"""
    family_id: str
    user_id: str
    role: str = 'member'  # creator, admin, member
    _id: str = None
    joined_at: datetime | str = None
    
    def __post_init__(self):
        if self._id is None:
            self._id = uuid.uuid4().hex
        if self.joined_at is None:
            self.joined_at = datetime.now()
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            '_id': self._id,
            'family_id': self.family_id,
            'user_id': self.user_id,
            'role': self.role,
            'joined_at': self.joined_at if isinstance(self.joined_at, str)
                        else self.joined_at.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'FamilyMember':
        """从字典创建家庭成员"""
        return cls(
            _id=data.get('_id'),
            family_id=data['family_id'],
            user_id=data['user_id'],
            role=data.get('role', 'member'),
            joined_at=data.get('joined_at')
        )
