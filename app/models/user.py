# -*- coding: utf-8 -*-
"""用户模型"""
import uuid
from datetime import datetime
from dataclasses import dataclass


@dataclass
class User:
    """用户数据模型"""
    username: str
    email: str
    password_hash: str
    salt: str
    _id: str = None
    created_at: str = None
    
    def __post_init__(self):
        if self._id is None:
            self._id = uuid.uuid4().hex
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> dict[str, str]:
        """转换为字典"""
        return {
            '_id': self._id,
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'salt': self.salt,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """从字典创建用户"""
        return cls(
            _id=data.get('_id'),
            username=data['username'],
            email=data['email'],
            password_hash=data['password_hash'],
            salt=data['salt'],
            created_at=data.get('created_at')
        )
