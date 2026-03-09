# -*- coding: utf-8 -*-
"""测试重命名冰箱 API（JWT 认证版本）"""
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


def test_rename_fridge_success(client, auth_headers, auth_token):
    """测试成功重命名冰箱"""
    # 首先创建一个冰箱
    create_response = client.post(
        '/fridge/create',
        json={'name': '原始冰箱'},
        headers=auth_headers
    )
    assert create_response.status_code == 200
    create_data = json.loads(create_response.data)
    fridge_id = create_data['fridge']['_id']
    
    # 重命名冰箱
    response = client.put(
        f'/fridge/{fridge_id}/rename',
        json={'name': '新冰箱名称'},
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert '重命名成功' in data['message']


def test_rename_fridge_empty_name(client, auth_headers, auth_token):
    """测试重命名冰箱时名称为空"""
    # 首先创建一个冰箱
    create_response = client.post(
        '/fridge/create',
        json={'name': '测试冰箱'},
        headers=auth_headers
    )
    assert create_response.status_code == 200
    create_data = json.loads(create_response.data)
    fridge_id = create_data['fridge']['_id']
    
    # 尝试用空名称重命名
    response = client.put(
        f'/fridge/{fridge_id}/rename',
        json={'name': ''},
        headers=auth_headers
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert '冰箱名称不能为空' in data['error']


def test_rename_fridge_name_too_long(client, auth_headers, auth_token):
    """测试重命名冰箱时名称过长"""
    # 首先创建一个冰箱
    create_response = client.post(
        '/fridge/create',
        json={'name': '测试冰箱'},
        headers=auth_headers
    )
    assert create_response.status_code == 200
    create_data = json.loads(create_response.data)
    fridge_id = create_data['fridge']['_id']
    
    # 尝试用过长名称重命名（21个字符）
    response = client.put(
        f'/fridge/{fridge_id}/rename',
        json={'name': '这是一个非常非常非常非常长的冰箱名称啊啊啊'},
        headers=auth_headers
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert '不能超过20个字符' in data['error']


def test_rename_fridge_no_token(client):
    """测试未提供 Token 时重命名冰箱"""
    response = client.put(
        '/fridge/test_fridge_id/rename',
        json={'name': '新名称'}
    )
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['success'] is False
    assert '未提供认证令牌' in data['error']


def test_rename_fridge_invalid_token(client):
    """测试使用无效 Token 重命名冰箱"""
    response = client.put(
        '/fridge/test_fridge_id/rename',
        json={'name': '新名称'},
        headers={'Authorization': 'Bearer invalid_token_here'}
    )
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['success'] is False
    assert '认证令牌无效或已过期' in data['error']


def test_rename_nonexistent_fridge(client, auth_headers):
    """测试重命名不存在的冰箱"""
    response = client.put(
        '/fridge/nonexistent_fridge_id/rename',
        json={'name': '新名称'},
        headers=auth_headers
    )
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['success'] is False
    assert '不存在' in data['error'] or '无权限' in data['error']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
