# -*- coding: utf-8 -*-
"""测试家庭成员 API"""
import pytest
from app import create_app
from app.utils.jwt_auth import generate_token


@pytest.fixture
def client():
    """创建测试客户端"""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def auth_headers():
    """生成认证头"""
    token = generate_token('test_user_id', 'testuser', 'test@example.com', False)
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def admin_headers():
    """生成管理员认证头"""
    token = generate_token('admin_user_id', 'admin', 'admin@example.com', True)
    return {'Authorization': f'Bearer {token}'}


def test_get_family_members_success(client, auth_headers, monkeypatch):
    """测试获取家庭成员成功"""
    # Mock 数据库操作
    class MockFamilyService:
        def __init__(self, db):
            pass
        
        def is_family_member(self, family_id, user_id):
            return True
        
        def get_family_members(self, family_id):
            return [
                {
                    '_id': 'member1',
                    'user_id': 'user1',
                    'username': 'user1',
                    'email': 'user1@example.com',
                    'role': 'creator',
                    'joined_at': '2024-01-01T00:00:00.000Z'
                },
                {
                    '_id': 'member2',
                    'user_id': 'user2',
                    'username': 'user2',
                    'email': 'user2@example.com',
                    'role': 'member',
                    'joined_at': '2024-01-02T00:00:00.000Z'
                }
            ]
    
    import app.routes.family
    monkeypatch.setattr(app.routes.family, 'FamilyService', MockFamilyService)
    
    response = client.get('/family/family123/members', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'data' in data
    assert len(data['data']) == 2
    assert data['data'][0]['username'] == 'user1'


def test_get_family_members_not_member(client, auth_headers, monkeypatch):
    """测试非家庭成员获取成员列表"""
    class MockFamilyService:
        def __init__(self, db):
            pass
        
        def is_family_member(self, family_id, user_id):
            return False
    
    import app.routes.family
    monkeypatch.setattr(app.routes.family, 'FamilyService', MockFamilyService)
    
    response = client.get('/family/family123/members', headers=auth_headers)
    assert response.status_code == 403
    data = response.get_json()
    assert data['success'] is False
    assert 'error' in data


def test_get_family_members_no_auth(client):
    """测试未认证获取家庭成员"""
    response = client.get('/family/family123/members')
    assert response.status_code == 401
