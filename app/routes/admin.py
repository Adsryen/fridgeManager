# -*- coding: utf-8 -*-
"""管理员路由"""
from flask import Blueprint, render_template, jsonify, request, send_file
from app import db_client
from app.services.admin_service import AdminService
from app.models.system_settings import SystemSettings
from app.utils.auth import admin_required
import sys
import os
from datetime import datetime

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


@admin_bp.route('/user/<user_id>/reset-password', methods=['POST'])
@admin_required
def reset_user_password(user_id):
    """重置用户密码"""
    try:
        data = request.get_json()
        new_password = data.get('password')
        
        if not new_password:
            return jsonify({'error': '密码不能为空'}), 400
        
        if len(new_password) < 6:
            return jsonify({'error': '密码长度至少6位'}), 400
        
        admin_service = AdminService(db_client.fridge)
        success = admin_service.reset_user_password(user_id, new_password)
        
        if success:
            return jsonify({'success': True, 'message': '密码已重置'})
        return jsonify({'error': '重置失败'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/stats')
@admin_required
def stats():
    """获取统计数据"""
    admin_service = AdminService(db_client.fridge)
    stats = admin_service.get_statistics()
    return jsonify(stats)


@admin_bp.route('/settings')
@admin_required
def settings():
    """系统设置页面"""
    system_settings = SystemSettings(db_client.fridge)
    settings_data = system_settings.get_all_settings()
    
    # 获取系统信息
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    # 获取数据库大小
    try:
        db_path = 'data/fridge.db'
        if os.path.exists(db_path):
            db_size = os.path.getsize(db_path)
            db_size_mb = round(db_size / (1024 * 1024), 2)
            db_size_str = f"{db_size_mb} MB"
        else:
            db_size_str = "未知"
    except:
        db_size_str = "未知"
    
    return render_template('admin/settings.html', 
                         settings=settings_data,
                         python_version=python_version,
                         db_size=db_size_str,
                         last_update=settings_data.get('updated_at', '未知'))


@admin_bp.route('/settings/save', methods=['POST'])
@admin_required
def save_settings():
    """保存系统设置"""
    try:
        data = request.get_json()
        category = data.get('category')
        settings = data.get('settings')
        
        system_settings = SystemSettings(db_client.fridge)
        success = system_settings.update_settings(settings)
        
        if success:
            return jsonify({'success': True, 'message': '设置已保存'})
        return jsonify({'error': '保存失败'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/maintenance/clean-expired', methods=['POST'])
@admin_required
def clean_expired_items():
    """清理过期物品"""
    try:
        admin_service = AdminService(db_client.fridge)
        count = admin_service.clean_expired_items()
        return jsonify({'success': True, 'count': count})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/maintenance/backup')
@admin_required
def backup_database():
    """备份数据库"""
    try:
        db_path = 'data/fridge.db'
        if os.path.exists(db_path):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            return send_file(db_path, 
                           as_attachment=True,
                           download_name=f'fridge_backup_{timestamp}.db')
        return jsonify({'error': '数据库文件不存在'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/maintenance/logs')
@admin_required
def view_logs():
    """查看系统日志"""
    try:
        admin_service = AdminService(db_client.fridge)
        logs = admin_service.get_system_logs()
        return render_template('admin/logs.html', logs=logs)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
