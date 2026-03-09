# -*- coding: utf-8 -*-
"""测试获取家庭列表 API（JWT 认证版本）"""
import pytest
import json
from app import create_app, db_client
from app.utils.jwt_auth import generate_token
from app.models import Family, FamilyMember


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
def test_user_id():
    """测试用户 ID"""
    return 'test_user_list_123'


@pytest.fixture
def auth_token(test_user_id):
    """生成测试用的 JWT Token"""
    return generate_token(
        user_id=test_user_id,
        username='testuser',
        email='test@example.com',
        is_admin=False
    )


@pytest.fixture
def setup_test_families(app, test_user_id):
    """设置测试家庭数据"""
    with app.app_context():
        from app import db_client
        db = db_client.fridge
        
        # 清理测试数据
        db.family.delete_many({'creator_id': test_user_id})
        db.family_member.delete_many({'user_id': test_user_id})
        
        # 创建测试家庭1（用户是创建者）
        family1 = Family(name='测试家庭1', creator_id=test_user_id)
        db.family.insert_one(family1.to_dict())
        member1 = FamilyMember(family_id=family1._id, user_id=test_user_id, role='creator')
        db.family_member.insert_one(member1.to_dict())
        
        # 创建测试家庭2（用户是普通成员）
        family2 = Family(name='测试家庭2', creator_id='other_user_456')
        db.family.insert_one(family2.to_dict())
        member2 = FamilyMember(family_id=family2._id, user_id=test_user_id, role='member')
        db.family_member.insert_one(member2.to_dict())
        
        yield [family1, family2]
        
        # 清理测试数据（逐个删除）
        db.family.delete_one({'_id': family1._id})
        db.family.delete_one({'_id': family2._id})
        db.family_member.delete_many({'user_id': test_user_id})


def test_list_families_success(client, auth_token, setup_test_families):
    """测试成功获取家庭列表"""
    response = client.get(
        '/family/list',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'data' in data
    assert isinstance(data['data'], list)
    assert len(data['data']) == 2
    
    # 验证返回的家庭信息
    family_names = [f['name'] for f in data['data']]
    assert '测试家庭1' in family_names
    assert '测试家庭2' in family_names
    
    # 验证角色信息
    for family in data['data']:
        assert 'role' in family
        assert family['role'] in ['creator', 'member']


def test_list_families_empty(client, auth_token, app, test_user_id):
    """测试用户没有加入任何家庭"""
    with app.app_context():
        from app import db_client
        db = db_client.fridge
        
        # 清理测试数据
        db.family_member.delete_many({'user_id': test_user_id})
    
    response = client.get(
        '/family/list',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'data' in data
    assert isinstance(data['data'], list)
    assert len(data['data']) == 0


def test_list_families_no_token(client):
    """测试未提供 Token 时获取家庭列表"""
    response = client.get('/family/list')
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['success'] is False
    assert '未提供认证令牌' in data['error']


def test_list_families_invalid_token(client):
    """测试使用无效 Token 获取家庭列表"""
    response = client.get(
        '/family/list',
        headers={'Authorization': 'Bearer invalid_token_here'}
    )
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['success'] is False
    assert '认证令牌无效或已过期' in data['error']


def test_list_families_response_format(client, auth_token, setup_test_families):
    """测试返回数据格式"""
    response = client.get(
        '/family/list',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    # 验证响应格式
    assert 'success' in data
    assert 'data' in data
    
    # 验证家庭对象包含必要字段
    for family in data['data']:
        assert '_id' in family
        assert 'name' in family
        assert 'creator_id' in family
        assert 'family_code' in family
        assert 'role' in family
        assert 'joined_at' in family


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
