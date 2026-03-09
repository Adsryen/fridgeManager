# -*- coding: utf-8 -*-
"""测试加入家庭 API（JWT 认证版本）"""
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
def auth_token():
    """生成测试用的 JWT Token"""
    return generate_token(
        user_id='test_user_123',
        username='testuser',
        email='test@example.com',
        is_admin=False
    )


@pytest.fixture
def another_auth_token():
    """生成另一个用户的 JWT Token"""
    return generate_token(
        user_id='test_user_456',
        username='anotheruser',
        email='another@example.com',
        is_admin=False
    )


@pytest.fixture
def test_family(app):
    """创建测试家庭"""
    with app.app_context():
        from app import db_client
        db = db_client.fridge
        family = Family(name='测试家庭', creator_id='test_user_123')
        db.family.insert_one(family.to_dict())
        
        # 添加创建者为成员
        member = FamilyMember(
            family_id=family._id,
            user_id='test_user_123',
            role='creator'
        )
        db.family_member.insert_one(member.to_dict())
        
        yield family
        
        # 清理
        db.family.delete_one({'_id': family._id})
        db.family_member.delete_many({'family_id': family._id})


def test_join_family_success(client, another_auth_token, test_family):
    """测试成功加入家庭"""
    response = client.post(
        '/family/join',
        json={'family_code': test_family.family_code},
        headers={'Authorization': f'Bearer {another_auth_token}'}
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['message'] == '成功加入家庭'


def test_join_family_empty_code(client, auth_token):
    """测试加入家庭时邀请码为空"""
    response = client.post(
        '/family/join',
        json={'family_code': ''},
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert '家庭邀请码不能为空' in data['error']


def test_join_family_no_code(client, auth_token):
    """测试加入家庭时未提供邀请码"""
    response = client.post(
        '/family/join',
        json={},
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert '家庭邀请码不能为空' in data['error']


def test_join_family_invalid_code(client, auth_token):
    """测试使用无效的家庭邀请码"""
    response = client.post(
        '/family/join',
        json={'family_code': 'INVALID'},
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert '家庭编号不存在' in data['error']


def test_join_family_already_member(client, auth_token, test_family):
    """测试加入已经是成员的家庭"""
    response = client.post(
        '/family/join',
        json={'family_code': test_family.family_code},
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert '您已经是该家庭的成员' in data['error']


def test_join_family_no_token(client, test_family):
    """测试未提供 Token 时加入家庭"""
    response = client.post(
        '/family/join',
        json={'family_code': test_family.family_code}
    )
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['success'] is False
    assert '未提供认证令牌' in data['error']


def test_join_family_invalid_token(client, test_family):
    """测试使用无效 Token 加入家庭"""
    response = client.post(
        '/family/join',
        json={'family_code': test_family.family_code},
        headers={'Authorization': 'Bearer invalid_token_here'}
    )
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['success'] is False
    assert '认证令牌无效或已过期' in data['error']


def test_join_family_lowercase_code(client, another_auth_token, test_family):
    """测试使用小写邀请码加入家庭（应自动转换为大写）"""
    response = client.post(
        '/family/join',
        json={'family_code': test_family.family_code.lower()},
        headers={'Authorization': f'Bearer {another_auth_token}'}
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['message'] == '成功加入家庭'


def test_join_family_whitespace_code(client, auth_token):
    """测试邀请码只包含空格"""
    response = client.post(
        '/family/join',
        json={'family_code': '   '},
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert '家庭邀请码不能为空' in data['error']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
