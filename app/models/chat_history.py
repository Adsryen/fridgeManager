# -*- coding: utf-8 -*-
"""AI对话历史模型"""
from datetime import datetime


class ChatHistory:
    """AI对话历史"""
    
    def __init__(self, collection):
        """
        Args:
            collection: SQLiteCollection实例
        """
        self.collection = collection
    
    def save_message(self, user_id: str, role: str, content: str) -> str:
        """保存单条消息
        
        Args:
            user_id: 用户ID
            role: 角色（user/assistant）
            content: 消息内容
            
        Returns:
            消息ID
        """
        message = {
            'user_id': user_id,
            'role': role,
            'content': content,
            'created_at': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z')
        }
        
        result = self.collection.insert_one(message)
        
        # 保持最近30条记录
        self._cleanup_old_messages(user_id)
        
        return result.inserted_id
    
    def get_user_history(self, user_id: str, limit: int = 30) -> list:
        """获取用户的对话历史
        
        Args:
            user_id: 用户ID
            limit: 最多返回的消息数量
            
        Returns:
            消息列表
        """
        # 获取所有消息
        messages = self.collection.find({'user_id': user_id})
        
        # 按创建时间排序（最新的在后）
        messages.sort(key=lambda x: x.get('created_at', ''), reverse=False)
        
        # 只保留最近的N条
        messages = messages[-limit:] if len(messages) > limit else messages
        
        # 转换为标准格式
        result = []
        for msg in messages:
            result.append({
                'role': msg['role'],
                'content': msg['content'],
                'created_at': msg.get('created_at', '')
            })
        
        return result
    
    def clear_user_history(self, user_id: str) -> int:
        """清空用户的对话历史
        
        Args:
            user_id: 用户ID
            
        Returns:
            删除的消息数量
        """
        result = self.collection.delete_many({'user_id': user_id})
        return result.deleted_count
    
    def _cleanup_old_messages(self, user_id: str, keep_count: int = 30):
        """清理旧消息，只保留最近的N条
        
        Args:
            user_id: 用户ID
            keep_count: 保留的消息数量
        """
        # 获取该用户的所有消息
        messages = self.collection.find({'user_id': user_id})
        
        if len(messages) > keep_count:
            # 按创建时间排序
            messages.sort(key=lambda x: x.get('created_at', ''))
            
            # 删除最旧的消息
            to_delete = messages[:len(messages) - keep_count]
            for msg in to_delete:
                self.collection.delete_one({'_id': msg['_id']})
