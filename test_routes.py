# -*- coding: utf-8 -*-
"""测试路由是否正常工作"""
import sys
sys.path.insert(0, '.')

from app import create_app

app = create_app('default')

with app.test_client() as client:
    # 测试主页是否可以匿名访问
    print("测试主页访问...")
    response = client.get('/')
    print(f"状态码: {response.status_code}")
    print(f"是否重定向: {response.status_code in [301, 302, 303, 307, 308]}")
    
    if response.status_code in [301, 302, 303, 307, 308]:
        print(f"重定向到: {response.location}")
    else:
        print("✓ 主页可以正常访问，无需登录")
    
    # 测试 get-current-mode 接口
    print("\n测试 get-current-mode 接口...")
    response = client.get('/item/get-current-mode')
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"返回数据: {response.get_json()}")
        print("✓ get-current-mode 接口正常")
    else:
        print(f"✗ get-current-mode 接口异常")
    
    # 测试 total 接口（获取物品列表）
    print("\n测试 total 接口...")
    response = client.post('/item/total')
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        print("✓ total 接口正常")
    else:
        print(f"✗ total 接口异常")
