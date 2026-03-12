# -*- coding: utf-8 -*-
"""物品历史记录路由"""
from flask import Blueprint, request, jsonify
from app.services.item_history_service import ItemHistoryService
from app.services.fridge_service import FridgeService
from app.utils.jwt_auth import jwt_required
from app import db_client

item_history_bp = Blueprint('item_history', __name__, url_prefix='/item-history')


def get_db():
    """获取数据库实例"""
    return db_client.fridge


@item_history_bp.route('/fridge/<fridge_id>', methods=['GET'])
@jwt_required
def get_fridge_history(fridge_id):
    """获取冰箱的物品历史记录"""
    try:
        user_id = request.user_id
        db = get_db()
        
        # 检查用户是否有权限访问该冰箱
        fridge_service = FridgeService(db)
        if not fridge_service.can_access_fridge(fridge_id, user_id):
            return jsonify({'success': False, 'error': '无权限访问该冰箱'}), 403
        
        # 获取历史记录
        history_service = ItemHistoryService(db)
        limit = request.args.get('limit', 50, type=int)
        histories = history_service.get_fridge_history(fridge_id, limit)
        
        return jsonify({
            'success': True,
            'data': histories
        })
    except Exception as e:
        import traceback
        print(f"[错误] 获取冰箱历史记录失败: {str(e)}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@item_history_bp.route('/item/<item_id>', methods=['GET'])
@jwt_required
def get_item_history(item_id):
    """获取特定物品的历史记录"""
    try:
        user_id = request.user_id
        db = get_db()
        
        # 检查物品是否存在且用户有权限
        item = db.item.find_one({'_id': item_id})
        if not item:
            return jsonify({'success': False, 'error': '物品不存在'}), 404
        
        # 检查冰箱权限
        fridge_service = FridgeService(db)
        fridge_id = item.get('fridge_id', 'public')
        if not fridge_service.can_access_fridge(fridge_id, user_id):
            return jsonify({'success': False, 'error': '无权限访问该物品'}), 403
        
        # 获取历史记录
        history_service = ItemHistoryService(db)
        histories = history_service.get_item_history(item_id)
        
        return jsonify({
            'success': True,
            'data': histories
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@item_history_bp.route('/deleted/<fridge_id>', methods=['GET'])
@jwt_required
def get_deleted_items(fridge_id):
    """获取已删除的物品列表（用于恢复）"""
    try:
        user_id = request.user_id
        db = get_db()
        
        # 检查用户是否有权限访问该冰箱
        fridge_service = FridgeService(db)
        if not fridge_service.can_access_fridge(fridge_id, user_id):
            return jsonify({'success': False, 'error': '无权限访问该冰箱'}), 403
        
        # 获取已删除的物品
        history_service = ItemHistoryService(db)
        limit = request.args.get('limit', 20, type=int)
        deleted_items = history_service.get_deleted_items(fridge_id, limit)
        
        return jsonify({
            'success': True,
            'data': deleted_items
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@item_history_bp.route('/restore/<history_id>', methods=['POST'])
@jwt_required
def restore_item(history_id):
    """恢复已删除的物品"""
    try:
        user_id = request.user_id
        db = get_db()
        
        # 获取历史记录
        history = db.item_history.find_one({'_id': history_id})
        if not history:
            return jsonify({'success': False, 'error': '历史记录不存在'}), 404
        
        # 检查冰箱权限
        fridge_service = FridgeService(db)
        if not fridge_service.can_edit_fridge(history['fridge_id'], user_id):
            return jsonify({'success': False, 'error': '无权限恢复该物品'}), 403
        
        # 恢复物品
        history_service = ItemHistoryService(db)
        restored_item = history_service.restore_item(history_id, user_id)
        
        return jsonify({
            'success': True,
            'data': restored_item,
            'message': '物品恢复成功'
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500