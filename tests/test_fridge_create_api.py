# -*- coding: utf-8 -*-
"""测试创建冰箱 API（JWT 认证版本）"""
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


def test_create_fridge_success(client, auth_token):
    """测试成功创建冰箱"""
    response = client.post(
        '/fridge/create',
        json={'name': '测试冰箱'},
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'fridge' in data
    assert data['fridge']['name'] == '测试冰箱'


def test_create_fridge_empty_name(client, auth_token):
    """测试创建冰箱时名称为空"""
    response = client.post(
        '/fridge/create',
        json={'name': ''},
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert '冰箱名称不能为空' in data['error']


def test_create_fridge_name_too_long(client, auth_token):
    """测试创建冰箱时名称过长"""
    response = client.post(
        '/fridge/create',
        json={'name': '这是一个非常非常非常非常长的冰箱名称超过二十个字符了'},
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert '不能超过20个字符' in data['error']


def test_create_fridge_no_token(client):
    """测试未提供 Token 时创建冰箱"""
    response = client.post(
        '/fridge/create',
        json={'name': '测试冰箱'}
    )
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['success'] is False
    assert '未提供认证令牌' in data['error']


def test_create_fridge_invalid_token(client):
    """测试使用无效 Token 创建冰箱"""
    response = client.post(
        '/fridge/create',
        json={'name': '测试冰箱'},
        headers={'Authorization': 'Bearer invalid_token_here'}
    )
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['success'] is False
    assert '认证令牌无效或已过期' in data['error']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
