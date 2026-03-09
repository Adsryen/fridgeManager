# -*- coding: utf-8 -*-
"""测试删除冰箱 API（JWT 认证版本）"""
import pytest
import json
from app import create_app, db_client
from app.utils.jwt_auth import generate_token


@pytest.fixture
def app():
    """创建测试应用"""
    app = create_app('testing')
    return app


@pytest.fixture
def client(app):
    """创建测试客户端"""
    return app.test_client()


@pytest.fixture
def auth_token():
    """生成测试用的 JWT Token"""
    return generate_token(
        user_id='test_user_123',
        username='testuser',
        email='test@example.com',
        is_admin=False
    )


@pytest.fixture
def auth_headers(auth_token):
    """创建认证头"""
    return {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json'
    }


@pytest.fixture(autouse=True)
def cleanup_test_data(app):
    """每个测试前清理测试数据"""
    # 需要在应用上下文中访问 db_client
    with app.app_context():
        from app import db_client
        
        # 清理测试用户的冰箱和物品
        test_user_ids = ['test_user_123', 'user_1', 'user_2']
        db = db_client.fridge
        
        for user_id in test_user_ids:
            db.fridge.delete_many({'user_id': user_id})
            db.item.delete_many({'user_id': user_id})
            db.settings.delete_many({'user_id': user_id})
        
        yield
        
        # 测试后清理
        for user_id in test_user_ids:
            db.fridge.delete_many({'user_id': user_id})
            db.item.delete_many({'user_id': user_id})
            db.settings.delete_many({'user_id': user_id})


def test_delete_empty_fridge_success(client, auth_headers):
    """测试成功删除空冰箱"""
    # 首先创建一个冰箱
    create_response = client.post(
        '/fridge/create',
        json={'name': '待删除的冰箱'},
        headers=auth_headers
    )
    assert create_response.status_code == 200
    create_data = json.loads(create_response.data)
    fridge_id = create_data['fridge']['_id']
    
    # 删除冰箱
    response = client.delete(
        f'/fridge/{fridge_id}',
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert '删除成功' in data['message']
    assert '0 件物品' in data['message']


def test_delete_fridge_with_items(client, auth_headers):
    """测试删除包含物品的冰箱"""
    # 首先创建一个冰箱
    create_response = client.post(
        '/fridge/create',
        json={'name': '有物品的冰箱'},
        headers=auth_headers
    )
    assert create_response.status_code == 200
    create_data = json.loads(create_response.data)
    fridge_id = create_data['fridge']['_id']
    
    # 添加一些物品到冰箱
    item_data = {
        'name': '测试物品',
        'num': 1,
        'expire_date': '2024-12-31',
        'place': 'cold',
        'type': '蔬菜',
        'fridge_id': fridge_id
    }
    
    # 添加3个物品
    for i in range(3):
        client.post(
            '/item/insert',
            json={**item_data, 'name': f'测试物品{i+1}'},
            headers=auth_headers
        )
    
    # 删除冰箱（应该同时删除所有物品）
    response = client.delete(
        f'/fridge/{fridge_id}',
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert '删除成功' in data['message']
    # 验证消息中包含删除的物品数量
    assert '3 件物品' in data['message']


def test_delete_fridge_no_token(client):
    """测试未提供 Token 时删除冰箱"""
    response = client.delete('/fridge/test_fridge_id')
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['success'] is False
    assert '未提供认证令牌' in data['error']


def test_delete_fridge_invalid_token(client):
    """测试使用无效 Token 删除冰箱"""
    response = client.delete(
        '/fridge/test_fridge_id',
        headers={'Authorization': 'Bearer invalid_token_here'}
    )
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['success'] is False
    assert '认证令牌无效或已过期' in data['error']


def test_delete_nonexistent_fridge(client, auth_headers):
    """测试删除不存在的冰箱"""
    response = client.delete(
        '/fridge/nonexistent_fridge_id',
        headers=auth_headers
    )
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['success'] is False
    assert '不存在' in data['error'] or '无权限' in data['error']


def test_delete_other_user_fridge(client):
    """测试删除其他用户的冰箱"""
    # 创建第一个用户的冰箱
    token1 = generate_token(
        user_id='user_1',
        username='user1',
        email='user1@example.com',
        is_admin=False
    )
    headers1 = {
        'Authorization': f'Bearer {token1}',
        'Content-Type': 'application/json'
    }
    
    create_response = client.post(
        '/fridge/create',
        json={'name': '用户1的冰箱'},
        headers=headers1
    )
    assert create_response.status_code == 200
    create_data = json.loads(create_response.data)
    fridge_id = create_data['fridge']['_id']
    
    # 尝试用第二个用户的 Token 删除
    token2 = generate_token(
        user_id='user_2',
        username='user2',
        email='user2@example.com',
        is_admin=False
    )
    headers2 = {
        'Authorization': f'Bearer {token2}',
        'Content-Type': 'application/json'
    }
    
    response = client.delete(
        f'/fridge/{fridge_id}',
        headers=headers2
    )
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['success'] is False
    assert '不存在' in data['error'] or '无权限' in data['error']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
