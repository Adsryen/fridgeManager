# -*- coding: utf-8 -*-
"""测试冰箱切换 API"""
import pytest
import json
from app import create_app, db_client
from app.utils.jwt_auth import generate_token


@pytest.fixture
def app():
    """创建测试应用"""
    app = create_app()
    app.config['TESTING'] = True
    yield app


@pytest.fixture
def client(app):
    """创建测试客户端"""
    return app.test_client()


@pytest.fixture
def auth_headers():
    """创建认证头"""
    # 生成测试用户的 JWT Token
    token = generate_token(
        user_id='test_user_123',
        username='testuser',
        email='test@example.com',
        is_admin=False
    )
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }


@pytest.fixture(autouse=True)
def cleanup_test_data(app):
    """每个测试前清理测试数据"""
    with app.app_context():
        from app import db_client
        
        # 清理测试用户的数据
        test_user_ids = ['test_user_123']
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


def test_switch_to_public_fridge(client, auth_headers):
    """测试切换到公共冰箱"""
    response = client.post(
        '/fridge/switch',
        data=json.dumps({'fridge_id': 'public'}),
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert '公共冰箱' in data['message']


def test_switch_fridge_missing_id(client, auth_headers):
    """测试缺少冰箱 ID"""
    response = client.post(
        '/fridge/switch',
        data=json.dumps({}),
        headers=auth_headers
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert '不能为空' in data['error']


def test_switch_fridge_without_auth(client):
    """测试未认证的请求"""
    response = client.post(
        '/fridge/switch',
        data=json.dumps({'fridge_id': 'public'}),
        headers={'Content-Type': 'application/json'}
    )
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['success'] is False


def test_switch_to_nonexistent_fridge(client, auth_headers):
    """测试切换到不存在的冰箱"""
    response = client.post(
        '/fridge/switch',
        data=json.dumps({'fridge_id': 'nonexistent_fridge_id'}),
        headers=auth_headers
    )
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['success'] is False
    assert '不存在' in data['error'] or '无权限' in data['error']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
