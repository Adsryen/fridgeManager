# -*- coding: utf-8 -*-
"""测试登录功能"""
import sys
sys.path.insert(0, '.')

from app import create_app, db_client
from app.services.user_service import UserService

app = create_app()

with app.app_context():
    try:
        print("=== 测试登录功能 ===")
        
        # 测试数据库连接
        print("\n1. 测试数据库连接...")
        user_service = UserService(db_client.fridge)
        print("✓ 数据库连接成功")
        
        # 获取所有用户
        print("\n2. 获取用户列表...")
        users = user_service.get_all_users()
        print(f"✓ 找到 {len(users)} 个用户")
        
        if users:
            for user in users:
                print(f"  - 用户名: {user.get('username')}, 邮箱: {user.get('email')}, 激活: {user.get('is_active', True)}")
        
        # 测试认证
        print("\n3. 测试用户认证...")
        test_username = input("请输入测试用户名 (默认: admin): ").strip() or "admin"
        test_password = input("请输入测试密码: ").strip()
        
        if test_password:
            user = user_service.authenticate(test_username, test_password)
            if user:
                print(f"✓ 认证成功!")
                print(f"  用户ID: {user._id}")
                print(f"  用户名: {user.username}")
                print(f"  是否管理员: {user.is_admin}")
                print(f"  是否激活: {user.is_active}")
            else:
                print("✗ 认证失败: 用户名或密码错误")
        
    except Exception as e:
        print(f"\n✗ 错误: {e}")
        import traceback
        traceback.print_exc()
