# -*- coding: utf-8 -*-
"""测试创建家庭 API 集成测试"""
import pytest
import json
from app import create_app, db_client
from app.utils.jwt_auth import generate_token
from app.services.family_service import FamilyService


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
        user_id='integration_test_user',
        username='integrationuser',
        email='integration@example.com',
        is_admin=False
    )


def test_create_family_integration(client, auth_token, app):
    """集成测试：创建家庭并验证响应格式"""
    # 1. 调用 API 创建家庭
    response = client.post(
        '/family/create',
        json={'name': '集成测试家庭'},
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    # 2. 验证响应格式符合设计文档要求
    assert response.status_code == 200
    data = json.loads(response.data)
    
    # 验证响应结构：{success: true, data: {family_id, family_code}}
    assert data['success'] is True
    assert 'data' in data
    assert 'family_id' in data['data']
    assert 'family_code' in data['data']
    
    # 验证 family_id 不为空
    family_id = data['data']['family_id']
    assert family_id is not None
    assert len(family_id) > 0
    
    # 验证 family_code 格式（6位大写字母数字）
    family_code = data['data']['family_code']
    assert len(family_code) == 6
    assert family_code.isupper()
    assert family_code.isalnum()
    
    # 3. 清理测试数据
    with app.app_context():
        from app import db_client
        db = db_client.fridge
        db.family.delete_one({'_id': family_id})
        db.family_member.delete_many({'family_id': family_id})


def test_create_multiple_families(client, auth_token, app):
    """测试同一用户创建多个家庭"""
    family_ids = []
    
    try:
        # 创建3个家庭
        for i in range(3):
            response = client.post(
                '/family/create',
                json={'name': f'测试家庭{i+1}'},
                headers={'Authorization': f'Bearer {auth_token}'}
            )
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['success'] is True
            family_ids.append(data['data']['family_id'])
        
        # 验证所有家庭都创建成功
        with app.app_context():
            from app import db_client
            db = db_client.fridge
            family_service = FamilyService(db)
            user_families = family_service.get_user_families('integration_test_user')
            
            # 至少应该有我们刚创建的3个家庭
            created_families = [f for f in user_families if f['_id'] in family_ids]
            assert len(created_families) == 3
        
    finally:
        # 清理测试数据
        with app.app_context():
            from app import db_client
            db = db_client.fridge
            for family_id in family_ids:
                db.family.delete_one({'_id': family_id})
                db.family_member.delete_many({'family_id': family_id})


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
