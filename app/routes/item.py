# -*- coding: utf-8 -*-
"""物品路由"""
from flask import Blueprint, request, redirect, url_for, jsonify, session
from datetime import datetime
from app import db_client
from app.services.item_service import ItemService
from app.utils.auth import get_current_user_id, get_effective_user_id

item_bp = Blueprint('item', __name__)


@item_bp.route('/insert', methods=['POST'])
def insert():
    """添加物品"""
    from app.models.system_settings import SystemSettings
    
    user_id = get_effective_user_id()
    
    # 检查用户物品数量限制
    if user_id != 'public':  # 只对私人冰箱检查限制
        system_settings = SystemSettings(db_client.fridge)
        settings = system_settings.get_all_settings()
        max_items = settings.get('max_items_per_user', 0)
        
        if max_items > 0:
            item_service = ItemService(db_client.fridge)
            current_items = item_service.get_user_items(user_id)
            if len(current_items) >= max_items:
                return jsonify({'error': f'已达到最大物品数量限制（{max_items}个）'}), 400
    
    try:
        date = request.values['itemDate'].replace('-', '')
        item_service = ItemService(db_client.fridge)
        
        item_service.create_item(
            user_id=user_id,
            name=request.values['itemName'],
            expire_date=datetime.strptime(date, "%Y%m%d"),
            place=request.values['itemPlace'],
            num=int(request.values['itemNum']),
            item_type=request.values['itemType']
        )
    except Exception:
        pass
    
    return redirect(url_for('main.index'))


@item_bp.route('/search', methods=['GET', 'POST'])
def search():
    """搜索物品"""
    searchbox = request.form.get('text')
    user_id = get_effective_user_id()
    
    item_service = ItemService(db_client.fridge)
    items = item_service.search_items(user_id, searchbox)
    
    return jsonify(list(items))


@item_bp.route('/stateok/<time>', methods=['GET', 'POST'])
def stateok(time):
    """获取未过期物品"""
    user_id = get_effective_user_id()
    date = datetime.fromtimestamp(int(time)/1000.0)
    
    item_service = ItemService(db_client.fridge)
    items = item_service.get_items_by_status(user_id, False, datetime(date.year, date.month, date.day))
    
    return jsonify(list(items))


@item_bp.route('/statebad/<time>', methods=['GET', 'POST'])
def statebad(time):
    """获取已过期物品"""
    user_id = get_effective_user_id()
    date = datetime.fromtimestamp(int(time)/1000.0)
    
    item_service = ItemService(db_client.fridge)
    items = item_service.get_items_by_status(user_id, True, datetime(date.year, date.month, date.day))
    
    return jsonify(list(items))


@item_bp.route('/cold', methods=['GET', 'POST'])
def cold():
    """获取冷藏物品"""
    user_id = get_effective_user_id()
    
    item_service = ItemService(db_client.fridge)
    items = item_service.get_items_by_place(user_id, 'cold')
    
    return jsonify(list(items))


@item_bp.route('/frozer', methods=['GET', 'POST'])
def frozer():
    """获取冷冻物品"""
    user_id = get_effective_user_id()
    
    item_service = ItemService(db_client.fridge)
    items = item_service.get_items_by_place(user_id, 'frozer')
    
    return jsonify(list(items))


@item_bp.route('/tag/<tagName>', methods=['GET', 'POST'])
def tag(tagName):
    """按类别获取物品"""
    user_id = get_effective_user_id()
    
    item_service = ItemService(db_client.fridge)
    items = item_service.get_items_by_type(user_id, tagName)
    
    return jsonify(list(items))


@item_bp.route('/total', methods=['GET', 'POST'])
def total():
    """获取所有物品"""
    user_id = get_effective_user_id()
    
    item_service = ItemService(db_client.fridge)
    items = item_service.get_user_items(user_id)
    
    return jsonify(list(items))


@item_bp.route('/delete/<_id>', methods=['POST'])
def delete(_id):
    """删除物品"""
    user_id = get_effective_user_id()
    
    item_service = ItemService(db_client.fridge)
    item_service.delete_item(user_id, _id)
    
    return '', 200


@item_bp.route('/getone/<_id>', methods=['GET', 'POST'])
def getone(_id):
    """获取单个物品"""
    user_id = get_effective_user_id()
    
    item_service = ItemService(db_client.fridge)
    item = item_service.get_item(user_id, _id)
    
    return jsonify([item] if item else [])


@item_bp.route('/edit/<_id>', methods=['POST'])
def edit(_id):
    """编辑物品"""
    user_id = get_effective_user_id()
    
    try:
        date = request.values['itemDate'].replace('-', '')
        
        item_service = ItemService(db_client.fridge)
        item_service.update_item(
            user_id=user_id,
            item_id=_id,
            Name=request.values['itemName'],
            ExpireDate=datetime.strptime(date, "%Y%m%d"),
            Place=request.values['itemPlace'],
            Num=int(request.values['itemNum']),
            Type=request.values['itemType']
        )
    except Exception:
        pass
    
    return redirect(url_for('main.index'))


@item_bp.route('/switch-mode', methods=['POST'])
def switch_mode():
    """切换查看模式（公共/私人）"""
    mode = request.json.get('mode', 'private')
    
    if mode == 'public':
        session['view_mode'] = 'public'
    else:
        session.pop('view_mode', None)
    
    return jsonify({'success': True, 'mode': mode})


@item_bp.route('/switch-user', methods=['POST'])
def switch_user():
    """管理员切换查看的用户（需要管理员权限）"""
    from app.utils.auth import is_admin
    
    if not is_admin():
        return jsonify({'error': '权限不足'}), 403
    
    user_id = request.json.get('user_id')
    
    if user_id:
        session['view_user_id'] = user_id
        session.pop('view_mode', None)  # 清除公共模式
    else:
        session.pop('view_user_id', None)
    
    return jsonify({'success': True, 'user_id': user_id})


@item_bp.route('/get-current-mode', methods=['GET'])
def get_current_mode():
    """获取当前查看模式"""
    from app.utils.auth import is_admin, get_effective_user_id, is_viewing_public, get_current_user_id
    
    current_user_id = get_current_user_id()
    effective_user_id = get_effective_user_id()
    is_public = is_viewing_public()
    
    # 如果用户已登录但没有明确选择模式，默认为私人冰箱
    if current_user_id and not session.get('view_mode') and not session.get('view_user_id'):
        is_public = False
    
    return jsonify({
        'is_logged_in': current_user_id is not None,
        'is_admin': is_admin(),
        'current_user_id': current_user_id,
        'effective_user_id': effective_user_id,
        'is_public': is_public,
        'view_user_id': session.get('view_user_id')
    })


@item_bp.route('/get-users-list', methods=['GET'])
def get_users_list():
    """获取用户列表（管理员专用）"""
    from app.utils.auth import is_admin
    from app.services.user_service import UserService
    
    if not is_admin():
        return jsonify({'error': '权限不足'}), 403
    
    user_service = UserService(db_client.fridge)
    users = user_service.get_all_users()
    
    # 添加公共冰箱选项
    users_list = [{'_id': 'public', 'username': '公共冰箱', 'email': ''}]
    users_list.extend([{
        '_id': user['_id'],
        'username': user['username'],
        'email': user['email']
    } for user in users])
    
    return jsonify(users_list)


@item_bp.route('/get-system-settings', methods=['GET'])
def get_system_settings():
    """获取系统设置（供前端使用）"""
    from app.models.system_settings import SystemSettings
    
    system_settings = SystemSettings(db_client.fridge)
    settings = system_settings.get_all_settings()
    
    # 只返回前端需要的设置
    return jsonify({
        'default_expiry_warning_days': settings.get('default_expiry_warning_days', 3),
        'max_items_per_user': settings.get('max_items_per_user', 0)
    })
