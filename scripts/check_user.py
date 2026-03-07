# -*- coding: utf-8 -*-
"""检查用户数据"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.database import SQLiteMongoLikeClient
from app.utils.auth import hash_password, verify_password

db_client = SQLiteMongoLikeClient('data')
db = db_client.fridge

users = db.user.find()
print('数据库中的用户：')
for user in users:
    print(f'\n用户名: {user["username"]}')
    print(f'邮箱: {user["email"]}')
    print(f'密码哈希: {user["password_hash"][:20]}...')
    print(f'Salt: {user["salt"][:20]}...')
    print(f'是否管理员: {user.get("is_admin", False)}')
    print(f'是否活跃: {user.get("is_active", True)}')
    
    # 测试密码验证
    test_password = 'admin'
    is_valid = verify_password(test_password, user['password_hash'], user['salt'])
    print(f'测试密码 "admin": {"✓ 正确" if is_valid else "✗ 错误"}')

db_client.close()
