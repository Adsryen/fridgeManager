# -*- coding: utf-8 -*-
"""冰箱管理路由"""
from flask import Blueprint, request, jsonify, session
from app.utils.auth import login_required, get_current_user_id
from app import db_client
from app.services.fridge_service import FridgeService

fridge_bp = Blueprint('fridge', __name__, url_prefix='/fridge')


def get_fridge_service():
    """获取冰箱服务实例"""
    return FridgeService(db_client.fridge)


@fridge_bp.route('/list', methods=['GET'])
@login_required
def list_fridges():
    """获取用户的所有冰箱（包括家庭共享冰箱）"""
    try:
        from app.services.family_service import FamilyService
        
        fridge_service = get_fridge_service()
        family_service = FamilyService(db_client.fridge)
        user_id = get_current_user_id()
        
        # 获取用户自己的冰箱
        my_fridges = fridge_service.get_user_fridges(user_id)
        
        # 为每个冰箱添加物品数量和权限信息
        for fridge in my_fridges:
            fridge['item_count'] = fridge_service.get_fridge_item_count(fridge['_id'])
            fridge['is_owner'] = True
            permission = family_service.get_fridge_permission(fridge['_id'])
            fridge['permission'] = permission
        
        # 获取家庭共享的冰箱
        families = family_service.get_user_families(user_id)
        shared_fridges = []
        
        for family in families:
            family_fridges = family_service.get_family_shared_fridges(family['_id'])
            for fridge in family_fridges:
                # 排除自己的冰箱
                if fridge['user_id'] != user_id:
                    fridge['item_count'] = fridge_service.get_fridge_item_count(fridge['_id'])
                    fridge['is_owner'] = False
                    fridge['family_name'] = family['name']
                    shared_fridges.append(fridge)
        
        return jsonify({
            'success': True,
            'my_fridges': my_fridges,
            'shared_fridges': shared_fridges
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@fridge_bp.route('/create', methods=['POST'])
@login_required
def create_fridge():
    """创建新冰箱"""
    try:
        fridge_service = get_fridge_service()
        data = request.get_json()
        name = data.get('name', '').strip()
        
        if not name:
            return jsonify({
                'success': False,
                'error': '冰箱名称不能为空'
            }), 400
        
        if len(name) > 20:
            return jsonify({
                'success': False,
                'error': '冰箱名称不能超过20个字符'
            }), 400
        
        user_id = get_current_user_id()
        
        # 检查用户冰箱数量限制(最多10个)
        existing_fridges = fridge_service.get_user_fridges(user_id)
        if len(existing_fridges) >= 10:
            return jsonify({
                'success': False,
                'error': '最多只能创建10个冰箱'
            }), 400
        
        fridge = fridge_service.create_fridge(user_id, name)
        
        return jsonify({
            'success': True,
            'fridge': fridge.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@fridge_bp.route('/<fridge_id>', methods=['GET'])
@login_required
def get_fridge(fridge_id):
    """获取单个冰箱信息"""
    try:
        fridge_service = get_fridge_service()
        user_id = get_current_user_id()
        fridge = fridge_service.get_fridge(fridge_id, user_id)
        
        if not fridge:
            return jsonify({
                'success': False,
                'error': '冰箱不存在'
            }), 404
        
        fridge['item_count'] = fridge_service.get_fridge_item_count(fridge_id)
        
        return jsonify({
            'success': True,
            'fridge': fridge
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@fridge_bp.route('/<fridge_id>/rename', methods=['PUT'])
@login_required
def rename_fridge(fridge_id):
    """重命名冰箱"""
    try:
        fridge_service = get_fridge_service()
        data = request.get_json()
        name = data.get('name', '').strip()
        
        if not name:
            return jsonify({
                'success': False,
                'error': '冰箱名称不能为空'
            }), 400
        
        if len(name) > 20:
            return jsonify({
                'success': False,
                'error': '冰箱名称不能超过20个字符'
            }), 400
        
        user_id = get_current_user_id()
        success = fridge_service.update_fridge(fridge_id, user_id, name)
        
        if not success:
            return jsonify({
                'success': False,
                'error': '冰箱不存在或无权限'
            }), 404
        
        return jsonify({
            'success': True,
            'message': '重命名成功'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@fridge_bp.route('/<fridge_id>', methods=['DELETE'])
@login_required
def delete_fridge(fridge_id):
    """删除冰箱"""
    try:
        fridge_service = get_fridge_service()
        user_id = get_current_user_id()
        
        # 检查冰箱是否存在
        fridge = fridge_service.get_fridge(fridge_id, user_id)
        if not fridge:
            return jsonify({
                'success': False,
                'error': '冰箱不存在或无权限'
            }), 404
        
        # 检查冰箱中是否还有物品
        item_count = fridge_service.get_fridge_item_count(fridge_id)
        if item_count > 0:
            return jsonify({
                'success': False,
                'error': f'冰箱中还有{item_count}件物品,请先清空'
            }), 400
        
        success = fridge_service.delete_fridge(fridge_id, user_id)
        
        if not success:
            return jsonify({
                'success': False,
                'error': '删除失败'
            }), 500
        
        return jsonify({
            'success': True,
            'message': '删除成功'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@fridge_bp.route('/switch', methods=['POST'])
@login_required
def switch_fridge():
    """切换当前冰箱"""
    try:
        fridge_service = get_fridge_service()
        data = request.get_json()
        fridge_id = data.get('fridge_id')
        
        if not fridge_id:
            return jsonify({
                'success': False,
                'error': '冰箱ID不能为空'
            }), 400
        
        # 如果是切换到公共冰箱
        if fridge_id == 'public':
            session['current_fridge_id'] = 'public'
            return jsonify({
                'success': True,
                'message': '已切换到公共冰箱'
            })
        
        # 验证冰箱是否属于当前用户
        user_id = get_current_user_id()
        fridge = fridge_service.get_fridge(fridge_id, user_id)
        
        if not fridge:
            return jsonify({
                'success': False,
                'error': '冰箱不存在或无权限'
            }), 404
        
        session['current_fridge_id'] = fridge_id
        
        return jsonify({
            'success': True,
            'message': f'已切换到{fridge["name"]}'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
