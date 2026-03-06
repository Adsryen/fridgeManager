# -*- coding: utf-8 -*-
"""管理员路由"""
from flask import Blueprint, render_template, jsonify, request
from app import db_client
from app.services.admin_service import AdminService
from app.utils.auth import admin_required

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """管理员仪表板"""
    admin_service = AdminService(db_client.fridge)
    stats = admin_service.get_statistics()
    return render_template('admin/dashboard.html', stats=stats)


@admin_bp.route('/users')
@admin_required
def users():
    """用户管理页面"""
    admin_service = AdminService(db_client.fridge)
    users = admin_service.get_all_users()
    return render_template('admin/users.html', users=users)


@admin_bp.route('/user/<user_id>')
@admin_required
def user_detail(user_id):
    """用户详情"""
    admin_service = AdminService(db_client.fridge)
    user = admin_service.get_user_details(user_id)
    
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    return render_template('admin/user_detail.html', user=user)


@admin_bp.route('/user/<user_id>/toggle-status', methods=['POST'])
@admin_required
def toggle_user_status(user_id):
    """切换用户激活状态"""
    admin_service = AdminService(db_client.fridge)
    success = admin_service.toggle_user_status(user_id)
    
    if success:
        return jsonify({'success': True, 'message': '状态已更新'})
    return jsonify({'error': '操作失败'}), 400


@admin_bp.route('/user/<user_id>/toggle-admin', methods=['POST'])
@admin_required
def toggle_admin_status(user_id):
    """切换用户管理员状态"""
    admin_service = AdminService(db_client.fridge)
    success = admin_service.toggle_admin_status(user_id)
    
    if success:
        return jsonify({'success': True, 'message': '权限已更新'})
    return jsonify({'error': '操作失败'}), 400


@admin_bp.route('/user/<user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    """删除用户"""
    admin_service = AdminService(db_client.fridge)
    success = admin_service.delete_user(user_id)
    
    if success:
        return jsonify({'success': True, 'message': '用户已删除'})
    return jsonify({'error': '删除失败'}), 400


@admin_bp.route('/stats')
@admin_required
def stats():
    """获取统计数据"""
    admin_service = AdminService(db_client.fridge)
    stats = admin_service.get_statistics()
    return jsonify(stats)
