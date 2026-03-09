# -*- coding: utf-8 -*-
"""测试离开家庭 API"""
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
    token = generate_token('member_user_id', 'member', 'member@example.com', False)
    return {'Authorization': f'Bearer {token}'}


def test_leave_family_success(client, auth_headers, monkeypatch):
    """测试离开家庭成功"""
    class MockFamilyService:
        def __init__(self, db):
            pass
        
        def leave_family(self, family_id, user_id):
            return True
    
    import app.routes.family
    monkeypatch.setattr(app.routes.family, 'FamilyService', MockFamilyService)
    
    response = client.post('/family/leave/family123', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['message'] == '已离开家庭'


def test_leave_family_creator_cannot_leave(client, auth_headers, monkeypatch):
    """测试创建者不能离开家庭"""
    class MockFamilyService:
        def __init__(self, db):
            pass
        
        def leave_family(self, family_id, user_id):
            raise ValueError('创建者不能离开家庭，请先转让家庭或删除家庭')
    
    import app.routes.family
    monkeypatch.setattr(app.routes.family, 'FamilyService', MockFamilyService)
    
    response = client.post('/family/leave/family123', headers=auth_headers)
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False
    assert 'error' in data


def test_leave_family_no_auth(client):
    """测试未认证离开家庭"""
    response = client.post('/family/leave/family123')
    assert response.status_code == 401
