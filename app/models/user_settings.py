# -*- coding: utf-8 -*-
"""用户设置模型"""
from dataclasses import dataclass


@dataclass
class UserSettings:
    """用户设置数据模型"""
    user_id: str
    
    # 通知设置
    notify_expiring: bool = True  # 过期提醒
    notify_days: int = 3  # 提前几天提醒
    
    # 显示设置
    items_per_page: int = 20  # 每页显示数量
    default_view: str = 'all'  # 默认视图 (all/cold/frozer)
    
    # 隐私设置
    profile_public: bool = False  # 个人资料是否公开
    
    _id: str = None
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            '_id': self._id or self.user_id,
            'user_id': self.user_id,
            'notify_expiring': self.notify_expiring,
            'notify_days': self.notify_days,
            'items_per_page': self.items_per_page,
            'default_view': self.default_view,
            'profile_public': self.profile_public
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'UserSettings':
        """从字典创建设置"""
        return cls(
            _id=data.get('_id'),
            user_id=data['user_id'],
            notify_expiring=data.get('notify_expiring', True),
            notify_days=data.get('notify_days', 3),
            items_per_page=data.get('items_per_page', 20),
            default_view=data.get('default_view', 'all'),
            profile_public=data.get('profile_public', False)
        )
