# -*- coding: utf-8 -*-
"""测试获取冰箱列表 API（JWT 认证版本）"""
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
    with app.app_context():
        from app import db_client
        
        # 清理测试用户的数据
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


def test_list_fridges_empty(client, auth_headers):
    """测试获取空冰箱列表"""
    response = client.get(
        '/fridge/list',
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'my_fridges' in data
    assert 'shared_fridges' in data
    assert isinstance(data['my_fridges'], list)
    assert isinstance(data['shared_fridges'], list)


def test_list_fridges_with_own_fridges(client, auth_headers):
    """测试获取包含自己冰箱的列表"""
    # 创建几个冰箱
    fridge_names = ['冰箱1', '冰箱2', '冰箱3']
    for name in fridge_names:
        client.post(
            '/fridge/create',
            json={'name': name},
            headers=auth_headers
        )
    
    # 获取冰箱列表
    response = client.get(
        '/fridge/list',
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert len(data['my_fridges']) == 3
    
    # 验证冰箱信息
    for fridge in data['my_fridges']:
        assert 'name' in fridge
        assert 'item_count' in fridge
        assert 'is_owner' in fridge
        assert fridge['is_owner'] is True
        assert 'permission' in fridge


def test_list_fridges_no_token(client):
    """测试未提供 Token 时获取冰箱列表"""
    response = client.get('/fridge/list')
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['success'] is False
    assert '未提供认证令牌' in data['error']


def test_list_fridges_invalid_token(client):
    """测试使用无效 Token 获取冰箱列表"""
    response = client.get(
        '/fridge/list',
        headers={'Authorization': 'Bearer invalid_token_here'}
    )
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['success'] is False
    assert '认证令牌无效或已过期' in data['error']


def test_list_fridges_response_format(client, auth_headers):
    """测试冰箱列表响应格式"""
    # 创建一个冰箱
    client.post(
        '/fridge/create',
        json={'name': '测试冰箱'},
        headers=auth_headers
    )
    
    # 获取冰箱列表
    response = client.get(
        '/fridge/list',
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    # 验证响应格式
    assert data['success'] is True
    assert 'my_fridges' in data
    assert 'shared_fridges' in data
    
    # 验证冰箱对象格式
    if len(data['my_fridges']) > 0:
        fridge = data['my_fridges'][0]
        assert '_id' in fridge
        assert 'name' in fridge
        assert 'user_id' in fridge
        assert 'item_count' in fridge
        assert 'is_owner' in fridge
        assert 'permission' in fridge
        assert 'created_at' in fridge


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
