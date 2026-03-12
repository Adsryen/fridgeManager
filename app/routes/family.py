# -*- coding: utf-8 -*-
"""家庭路由"""
from flask import Blueprint, request, jsonify
from app.services.family_service import FamilyService
from app.utils.jwt_auth import jwt_required
from app import db_client

family_bp = Blueprint('family', __name__, url_prefix='/family')


def get_db():
    """获取数据库实例"""
    return db_client.fridge


@family_bp.route('/create', methods=['POST'])
@jwt_required
def create_family():
    """创建家庭（JWT 认证）"""
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        
        if not name:
            return jsonify({'success': False, 'error': '家庭名称不能为空'}), 400
        
        # 从 JWT Token 中获取用户 ID
        user_id = request.user_id
        db = get_db()
        family_service = FamilyService(db)
        
        family = family_service.create_family(name, user_id)
        
        return jsonify({
            'success': True,
            'data': {
                'family_id': family._id,
                'family_code': family.family_code
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@family_bp.route('/join', methods=['POST'])
@jwt_required
def join_family():
    """加入家庭（JWT 认证）"""
    try:
        data = request.get_json()
        family_code = data.get('family_code', '').strip().upper()
        
        if not family_code:
            return jsonify({'success': False, 'error': '家庭邀请码不能为空'}), 400
        
        # 从 JWT Token 中获取用户 ID
        user_id = request.user_id
        db = get_db()
        family_service = FamilyService(db)
        
        family_service.join_family(family_code, user_id)
        
        return jsonify({
            'success': True,
            'message': '成功加入家庭'
        }), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': '服务器内部错误'}), 500


@family_bp.route('/leave/<family_id>', methods=['POST'])
@jwt_required
def leave_family(family_id):
    """离开家庭（JWT 认证）"""
    try:
        # 从 JWT Token 中获取用户 ID
        user_id = request.user_id
        db = get_db()
        family_service = FamilyService(db)
        
        family_service.leave_family(family_id, user_id)
        
        return jsonify({
            'success': True,
            'message': '已离开家庭'
        }), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@family_bp.route('/list', methods=['GET'])
@jwt_required
def list_families():
    """获取用户所在的所有家庭（JWT 认证）"""
    try:
        print(f"[调试] 收到家庭列表请求")
        # 从 JWT Token 中获取用户 ID
        user_id = request.user_id
        print(f"[调试] 用户ID: {user_id}")
        db = get_db()
        family_service = FamilyService(db)
        
        families = family_service.get_user_families(user_id)
        print(f"[调试] 查询到的家庭数量: {len(families)}")
        
        return jsonify({
            'success': True,
            'data': families
        })
    except Exception as e:
        print(f"[调试] 家庭列表查询出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@family_bp.route('/<family_id>/members', methods=['GET'])
@jwt_required
def get_family_members(family_id):
    """获取家庭成员列表（JWT 认证）"""
    try:
        # 从 JWT Token 中获取用户 ID
        user_id = request.user_id
        db = get_db()
        family_service = FamilyService(db)
        
        # 检查是否是家庭成员
        if not family_service.is_family_member(family_id, user_id):
            return jsonify({'success': False, 'error': '您不是该家庭的成员'}), 403
        
        members = family_service.get_family_members(family_id)
        
        return jsonify({
            'success': True,
            'data': members
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@family_bp.route('/<family_id>', methods=['PUT'])
@jwt_required
def update_family(family_id):
    """更新家庭信息（JWT 认证）"""
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        
        if not name:
            return jsonify({'success': False, 'error': '家庭名称不能为空'}), 400
        
        # 从 JWT Token 中获取用户 ID
        user_id = request.user_id
        db = get_db()
        family_service = FamilyService(db)
        
        family_service.update_family(family_id, user_id, name)
        
        return jsonify({
            'success': True,
            'message': '家庭信息更新成功'
        }), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 403
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@family_bp.route('/<family_id>', methods=['DELETE'])
@jwt_required
def delete_family(family_id):
    """删除家庭（JWT 认证）"""
    try:
        # 从 JWT Token 中获取用户 ID
        user_id = request.user_id
        db = get_db()
        family_service = FamilyService(db)
        
        family_service.delete_family(family_id, user_id)
        
        return jsonify({
            'success': True,
            'message': '家庭已删除'
        }), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 403
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@family_bp.route('/<family_id>/members/<target_user_id>', methods=['DELETE'])
@jwt_required
def remove_member(family_id, target_user_id):
    """移除家庭成员（JWT 认证）"""
    try:
        # 从 JWT Token 中获取用户 ID
        user_id = request.user_id
        db = get_db()
        family_service = FamilyService(db)
        
        family_service.remove_member(family_id, user_id, target_user_id)
        
        return jsonify({
            'success': True,
            'message': '成员已移除'
        }), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 403
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@family_bp.route('/<family_id>/fridges', methods=['GET'])
@jwt_required
def get_family_fridges(family_id):
    """获取家庭共享的冰箱列表（JWT 认证）"""
    try:
        # 从 JWT Token 中获取用户 ID
        user_id = request.user_id
        db = get_db()
        family_service = FamilyService(db)
        
        # 检查是否是家庭成员
        if not family_service.is_family_member(family_id, user_id):
            return jsonify({'success': False, 'error': '您不是该家庭的成员'}), 403
        
        fridges = family_service.get_family_shared_fridges(family_id)
        
        return jsonify({
            'success': True,
            'data': fridges
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@family_bp.route('/fridge/<fridge_id>/permission', methods=['POST'])
@jwt_required
def set_fridge_permission(fridge_id):
    """设置冰箱权限（JWT 认证）"""
    try:
        data = request.get_json()
        is_family_shared = data.get('is_family_shared', False)
        is_editable_by_family = data.get('is_editable_by_family', False)
        
        print(f"[权限设置] 冰箱ID: {fridge_id}")
        print(f"[权限设置] 请求数据: {data}")
        print(f"[权限设置] 家庭共享: {is_family_shared}")
        print(f"[权限设置] 允许编辑: {is_editable_by_family}")
        
        # 从 JWT Token 中获取用户 ID
        user_id = request.user_id
        print(f"[权限设置] 用户ID: {user_id}")
        db = get_db()
        
        # 检查是否是冰箱所有者
        fridge = db.fridge.find_one({'_id': fridge_id})
        print(f"[权限设置] 冰箱信息: {fridge}")
        if not fridge or fridge['user_id'] != user_id:
            print(f"[权限设置] 权限检查失败 - 冰箱所有者: {fridge.get('user_id') if fridge else 'None'}, 当前用户: {user_id}")
            return jsonify({'success': False, 'error': '只有冰箱所有者可以设置权限'}), 403
        
        family_service = FamilyService(db)
        result = family_service.set_fridge_permission(fridge_id, is_family_shared, is_editable_by_family)
        print(f"[权限设置] 设置结果: {result}")
        
        return jsonify({
            'success': True,
            'message': '权限设置成功'
        }), 200
    except Exception as e:
        print(f"[权限设置] 异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@family_bp.route('/fridge/<fridge_id>/permission', methods=['GET'])
@jwt_required
def get_fridge_permission(fridge_id):
    """获取冰箱权限（JWT 认证）"""
    try:
        print(f"[获取权限] 冰箱ID: {fridge_id}")
        db = get_db()
        family_service = FamilyService(db)
        permission = family_service.get_fridge_permission(fridge_id)
        print(f"[获取权限] 权限数据: {permission}")
        
        return jsonify({
            'success': True,
            'data': permission
        }), 200
    except Exception as e:
        print(f"[获取权限] 异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500
