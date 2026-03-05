# -*- coding: utf-8 -*-
"""物品路由"""
from flask import Blueprint, request, redirect, url_for, jsonify
from datetime import datetime
from app import db_client
from app.services.item_service import ItemService
from app.utils.auth import login_required, get_current_user_id

item_bp = Blueprint('item', __name__)


@item_bp.route('/insert', methods=['POST'])
@login_required
def insert():
    """添加物品"""
    user_id = get_current_user_id()
    
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
@login_required
def search():
    """搜索物品"""
    searchbox = request.form.get('text')
    user_id = get_current_user_id()
    
    item_service = ItemService(db_client.fridge)
    items = item_service.search_items(user_id, searchbox)
    
    return jsonify(list(items))


@item_bp.route('/stateok/<time>', methods=['GET', 'POST'])
@login_required
def stateok(time):
    """获取未过期物品"""
    user_id = get_current_user_id()
    date = datetime.fromtimestamp(int(time)/1000.0)
    
    item_service = ItemService(db_client.fridge)
    items = item_service.get_items_by_status(user_id, False, datetime(date.year, date.month, date.day))
    
    return jsonify(list(items))


@item_bp.route('/statebad/<time>', methods=['GET', 'POST'])
@login_required
def statebad(time):
    """获取已过期物品"""
    user_id = get_current_user_id()
    date = datetime.fromtimestamp(int(time)/1000.0)
    
    item_service = ItemService(db_client.fridge)
    items = item_service.get_items_by_status(user_id, True, datetime(date.year, date.month, date.day))
    
    return jsonify(list(items))


@item_bp.route('/cold', methods=['GET', 'POST'])
@login_required
def cold():
    """获取冷藏物品"""
    user_id = get_current_user_id()
    
    item_service = ItemService(db_client.fridge)
    items = item_service.get_items_by_place(user_id, 'cold')
    
    return jsonify(list(items))


@item_bp.route('/frozer', methods=['GET', 'POST'])
@login_required
def frozer():
    """获取冷冻物品"""
    user_id = get_current_user_id()
    
    item_service = ItemService(db_client.fridge)
    items = item_service.get_items_by_place(user_id, 'frozer')
    
    return jsonify(list(items))


@item_bp.route('/tag/<tagName>', methods=['GET', 'POST'])
@login_required
def tag(tagName):
    """按类别获取物品"""
    user_id = get_current_user_id()
    
    item_service = ItemService(db_client.fridge)
    items = item_service.get_items_by_type(user_id, tagName)
    
    return jsonify(list(items))


@item_bp.route('/total', methods=['GET', 'POST'])
@login_required
def total():
    """获取所有物品"""
    user_id = get_current_user_id()
    
    item_service = ItemService(db_client.fridge)
    items = item_service.get_user_items(user_id)
    
    return jsonify(list(items))


@item_bp.route('/delete/<_id>', methods=['POST'])
@login_required
def delete(_id):
    """删除物品"""
    user_id = get_current_user_id()
    
    item_service = ItemService(db_client.fridge)
    item_service.delete_item(user_id, _id)
    
    return '', 200


@item_bp.route('/getone/<_id>', methods=['GET', 'POST'])
@login_required
def getone(_id):
    """获取单个物品"""
    user_id = get_current_user_id()
    
    item_service = ItemService(db_client.fridge)
    item = item_service.get_item(user_id, _id)
    
    return jsonify([item] if item else [])


@item_bp.route('/edit/<_id>', methods=['POST'])
@login_required
def edit(_id):
    """编辑物品"""
    user_id = get_current_user_id()
    
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
