# -*- coding: utf-8 -*-
"""测试冰箱权限设置 API"""
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
    token = generate_token('owner_user_id', 'owner', 'owner@example.com', False)
    return {'Authorization': f'Bearer {token}'}


def test_set_fridge_permission_success(client, auth_headers, monkeypatch):
    """测试设置冰箱权限成功"""
    class MockDB:
        class FridgeCollection:
            def find_one(self, query):
                return {
                    '_id': 'fridge123',
                    'user_id': 'owner_user_id',
                    'name': '我的冰箱'
                }
        
        fridge = FridgeCollection()
    
    class MockFamilyService:
        def __init__(self, db):
            pass
        
        def set_fridge_permission(self, fridge_id, is_family_shared, is_editable_by_family):
            return True
    
    import app.routes.family
    
    def mock_get_db():
        return MockDB()
    
    monkeypatch.setattr(app.routes.family, 'get_db', mock_get_db)
    monkeypatch.setattr(app.routes.family, 'FamilyService', MockFamilyService)
    
    response = client.post('/family/fridge/fridge123/permission',
                          headers=auth_headers,
                          json={
                              'is_family_shared': True,
                              'is_editable_by_family': True
                          })
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['message'] == '权限设置成功'


def test_set_fridge_permission_not_owner(client, auth_headers, monkeypatch):
    """测试非所有者设置权限"""
    class MockDB:
        class FridgeCollection:
            def find_one(self, query):
                return {
                    '_id': 'fridge123',
                    'user_id': 'other_user_id',  # 不是当前用户
                    'name': '别人的冰箱'
                }
        
        fridge = FridgeCollection()
    
    import app.routes.family
    
    def mock_get_db():
        return MockDB()
    
    monkeypatch.setattr(app.routes.family, 'get_db', mock_get_db)
    
    response = client.post('/family/fridge/fridge123/permission',
                          headers=auth_headers,
                          json={
                              'is_family_shared': True,
                              'is_editable_by_family': False
                          })
    assert response.status_code == 403
    data = response.get_json()
    assert data['success'] is False
    assert 'error' in data


def test_set_fridge_permission_fridge_not_found(client, auth_headers, monkeypatch):
    """测试冰箱不存在"""
    class MockDB:
        class FridgeCollection:
            def find_one(self, query):
                return None
        
        fridge = FridgeCollection()
    
    import app.routes.family
    
    def mock_get_db():
        return MockDB()
    
    monkeypatch.setattr(app.routes.family, 'get_db', mock_get_db)
    
    response = client.post('/family/fridge/fridge123/permission',
                          headers=auth_headers,
                          json={
                              'is_family_shared': True,
                              'is_editable_by_family': False
                          })
    assert response.status_code == 403
    data = response.get_json()
    assert data['success'] is False


def test_set_fridge_permission_no_auth(client):
    """测试未认证设置权限"""
    response = client.post('/family/fridge/fridge123/permission',
                          json={
                              'is_family_shared': True,
                              'is_editable_by_family': False
                          })
    assert response.status_code == 401
