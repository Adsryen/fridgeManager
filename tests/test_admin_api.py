# -*- coding: utf-8 -*-
"""管理员 API 测试"""

import pytest
import json
from app import create_app
from app import db_client
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
def admin_token():
    """生成管理员 Token"""
    return generate_token(
        user_id='test_admin_id',
        username='admin',
        email='admin@test.com',
        is_admin=True
    )


@pytest.fixture
def user_token():
    """生成普通用户 Token"""
    return generate_token(
        user_id='test_user_id',
        username='user',
        email='user@test.com',
        is_admin=False
    )


def test_get_stats_without_token(client):
    """测试未提供 Token 时获取统计数据"""
    response = client.get('/admin/stats')
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['success'] is False
    assert '未提供认证令牌' in data['error']


def test_get_stats_with_user_token(client, user_token):
    """测试普通用户无法获取统计数据"""
    response = client.get(
        '/admin/stats',
        headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403
    data = json.loads(response.data)
    assert data['success'] is False
    assert '权限不足' in data['error']


def test_get_stats_with_admin_token(client, admin_token):
    """测试管理员获取统计数据"""
    response = client.get(
        '/admin/stats',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'data' in data


def test_get_users_with_admin_token(client, admin_token):
    """测试管理员获取用户列表"""
    response = client.get(
        '/admin/users',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'data' in data
    assert isinstance(data['data'], list)


def test_get_settings_with_admin_token(client, admin_token):
    """测试管理员获取系统设置"""
    response = client.get(
        '/admin/settings',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'data' in data


def test_save_settings_with_admin_token(client, admin_token):
    """测试管理员保存系统设置"""
    settings_data = {
        'settings': {
            'session_timeout': 3600,
            'max_items_per_user': 1000,
            'default_expiry_warning_days': 3
        }
    }
    
    response = client.post(
        '/admin/settings/save',
        headers={
            'Authorization': f'Bearer {admin_token}',
            'Content-Type': 'application/json'
        },
        data=json.dumps(settings_data)
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True


def test_save_settings_without_data(client, admin_token):
    """测试保存空设置数据"""
    response = client.post(
        '/admin/settings/save',
        headers={
            'Authorization': f'Bearer {admin_token}',
            'Content-Type': 'application/json'
        },
        data=json.dumps({})
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert '设置数据不能为空' in data['error']


def test_test_ai_connection_without_data(client, admin_token):
    """测试 AI 连接时缺少必需参数"""
    response = client.post(
        '/admin/ai/test-connection',
        headers={
            'Authorization': f'Bearer {admin_token}',
            'Content-Type': 'application/json'
        },
        data=json.dumps({})
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert 'API地址和密钥不能为空' in data['error']


def test_list_ai_models_without_data(client, admin_token):
    """测试获取模型列表时缺少必需参数"""
    response = client.post(
        '/admin/ai/list-models',
        headers={
            'Authorization': f'Bearer {admin_token}',
            'Content-Type': 'application/json'
        },
        data=json.dumps({'api_base': '', 'api_key': ''})
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert 'API地址和密钥不能为空' in data['error']


def test_reset_password_without_password(client, admin_token):
    """测试重置密码时未提供密码"""
    response = client.post(
        '/admin/user/test_user_id/reset-password',
        headers={
            'Authorization': f'Bearer {admin_token}',
            'Content-Type': 'application/json'
        },
        data=json.dumps({})
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert '密码不能为空' in data['error']


def test_reset_password_with_short_password(client, admin_token):
    """测试重置密码时密码过短"""
    response = client.post(
        '/admin/user/test_user_id/reset-password',
        headers={
            'Authorization': f'Bearer {admin_token}',
            'Content-Type': 'application/json'
        },
        data=json.dumps({'password': '12345'})
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert '密码长度至少6位' in data['error']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
