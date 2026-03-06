# -*- coding: utf-8 -*-
"""创建管理员账号脚本"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.database import SQLiteMongoLikeClient
from app.models.user import User
from app.utils.auth import hash_password
import uuid


def create_admin():
    """创建管理员账号"""
    # 连接数据库
    db_client = SQLiteMongoLikeClient('data')
    db = db_client.fridge
    
    # 管理员信息
    username = input('请输入管理员用户名 (默认: admin): ').strip() or 'admin'
    email = input('请输入管理员邮箱 (默认: admin@example.com): ').strip() or 'admin@example.com'
    password = input('请输入管理员密码 (默认: admin123): ').strip() or 'admin123'
    
    # 检查用户是否已存在
    existing_user = db.user.find_one({'username': username})
    if existing_user:
        print(f'\n用户 "{username}" 已存在！')
        
        # 询问是否设置为管理员
        choice = input('是否将该用户设置为管理员？(y/n): ').strip().lower()
        if choice == 'y':
            db.user.update_one(
                {'username': username},
                {'$set': {'is_admin': True, 'is_active': True}}
            )
            print(f'✓ 用户 "{username}" 已设置为管理员')
        return
    
    # 创建新管理员
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
    
    print(f'\n✓ 管理员账号创建成功！')
    print(f'  用户名: {username}')
    print(f'  邮箱: {email}')
    print(f'  密码: {password}')
    print(f'\n请访问 http://localhost:8080/auth/login 登录')
    
    db_client.close()


if __name__ == '__main__':
    try:
        create_admin()
    except KeyboardInterrupt:
        print('\n\n操作已取消')
    except Exception as e:
        print(f'\n错误: {e}')
        import traceback
        traceback.print_exc()
