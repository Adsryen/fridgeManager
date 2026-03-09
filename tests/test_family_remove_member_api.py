# -*- coding: utf-8 -*-
"""测试移除家庭成员 API"""
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
    token = generate_token('creator_user_id', 'creator', 'creator@example.com', False)
    return {'Authorization': f'Bearer {token}'}


def test_remove_member_success(client, auth_headers, monkeypatch):
    """测试移除家庭成员成功"""
    class MockFamilyService:
        def __init__(self, db):
            pass
        
        def remove_member(self, family_id, user_id, target_user_id):
            return True
    
    import app.routes.family
    monkeypatch.setattr(app.routes.family, 'FamilyService', MockFamilyService)
    
    response = client.delete('/family/family123/members/user456', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['message'] == '成员已移除'


def test_remove_member_not_creator(client, auth_headers, monkeypatch):
    """测试非创建者移除成员"""
    class MockFamilyService:
        def __init__(self, db):
            pass
        
        def remove_member(self, family_id, user_id, target_user_id):
            raise ValueError('只有创建者和管理员可以移除成员')
    
    import app.routes.family
    monkeypatch.setattr(app.routes.family, 'FamilyService', MockFamilyService)
    
    response = client.delete('/family/family123/members/user456', headers=auth_headers)
    assert response.status_code == 403
    data = response.get_json()
    assert data['success'] is False
    assert 'error' in data


def test_remove_member_no_auth(client):
    """测试未认证移除成员"""
    response = client.delete('/family/family123/members/user456')
    assert response.status_code == 401
