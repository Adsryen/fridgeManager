# -*- coding: utf-8 -*-
"""测试创建家庭 API（JWT 认证版本）"""
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


def test_create_family_success(client, auth_token):
    """测试成功创建家庭"""
    response = client.post(
        '/family/create',
        json={'name': '测试家庭'},
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'data' in data
    assert 'family_id' in data['data']
    assert 'family_code' in data['data']
    # 验证家庭邀请码格式（应该是6位大写字母数字）
    assert len(data['data']['family_code']) == 6
    assert data['data']['family_code'].isupper()


def test_create_family_empty_name(client, auth_token):
    """测试创建家庭时名称为空"""
    response = client.post(
        '/family/create',
        json={'name': ''},
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert '家庭名称不能为空' in data['error']


def test_create_family_no_name(client, auth_token):
    """测试创建家庭时未提供名称"""
    response = client.post(
        '/family/create',
        json={},
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert '家庭名称不能为空' in data['error']


def test_create_family_no_token(client):
    """测试未提供 Token 时创建家庭"""
    response = client.post(
        '/family/create',
        json={'name': '测试家庭'}
    )
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['success'] is False
    assert '未提供认证令牌' in data['error']


def test_create_family_invalid_token(client):
    """测试使用无效 Token 创建家庭"""
    response = client.post(
        '/family/create',
        json={'name': '测试家庭'},
        headers={'Authorization': 'Bearer invalid_token_here'}
    )
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['success'] is False
    assert '认证令牌无效或已过期' in data['error']


def test_create_family_whitespace_name(client, auth_token):
    """测试创建家庭时名称只包含空格"""
    response = client.post(
        '/family/create',
        json={'name': '   '},
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert '家庭名称不能为空' in data['error']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
