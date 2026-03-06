# -*- coding: utf-8 -*-
"""初始化默认管理员账号"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.database import SQLiteMongoLikeClient
from app.models.user import User
from app.utils.auth import hash_password
import uuid


def init_default_admin():
    """初始化默认管理员账号 (admin/admin)"""
    # 连接数据库
    db_client = SQLiteMongoLikeClient('data')
    db = db_client.fridge
    
    # 默认管理员信息
    username = 'admin'
    email = 'admin@fridgemanager.local'
    password = 'admin'
    
    # 检查管理员是否已存在
    existing_admin = db.user.find_one({'username': username})
    if existing_admin:
        print(f'管理员账号 "{username}" 已存在')
        
        # 确保该用户是管理员且处于活跃状态
        if not existing_admin.get('is_admin') or not existing_admin.get('is_active'):
            db.user.update_one(
                {'username': username},
                {'$set': {'is_admin': True, 'is_active': True}}
            )
            print(f'✓ 已更新用户 "{username}" 为管理员')
        
        db_client.close()
        return
    
    # 创建默认管理员
    salt = uuid.uuid4().hex
    password_hash, _ = hash_password(password, salt)
    
    admin = User(
        username=username,
        email=email,
        password_hash=password_hash,
        salt=salt,
        is_admin=True,
        is_active=True
    )
    
    db.user.insert_one(admin.to_dict())
    
    print('✓ 默认管理员账号创建成功！')
    print(f'  用户名: {username}')
    print(f'  密码: {password}')
    print(f'  邮箱: {email}')
    print('\n⚠️  请在首次登录后立即修改密码！')
    
    db_client.close()


if __name__ == '__main__':
    try:
        init_default_admin()
    except Exception as e:
        print(f'错误: {e}')
        import traceback
        traceback.print_exc()
