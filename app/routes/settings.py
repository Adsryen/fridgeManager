# -*- coding: utf-8 -*-
"""用户设置路由"""
from flask import Blueprint, render_template, request, jsonify
from app import db_client
from app.services.settings_service import SettingsService
from app.utils.auth import login_required, get_current_user_id

settings_bp = Blueprint('settings', __name__)


@settings_bp.route('/')
@login_required
def index():
    """用户设置页面"""
    user_id = get_current_user_id()
    settings_service = SettingsService(db_client.fridge)
    settings = settings_service.get_user_settings(user_id)
    
    return render_template('settings/index.html', settings=settings)


@settings_bp.route('/update', methods=['POST'])
@login_required
def update():
    """更新用户设置"""
    user_id = get_current_user_id()
    
    # 获取表单数据
    notify_expiring = request.form.get('notify_expiring') == 'on'
    notify_days = int(request.form.get('notify_days', 3))
    items_per_page = int(request.form.get('items_per_page', 20))
    default_view = request.form.get('default_view', 'all')
    profile_public = request.form.get('profile_public') == 'on'
    
    settings_service = SettingsService(db_client.fridge)
    success = settings_service.update_settings(
        user_id,
        notify_expiring=notify_expiring,
        notify_days=notify_days,
        items_per_page=items_per_page,
        default_view=default_view,
        profile_public=profile_public
    )
    
    if success:
        return jsonify({'success': True, 'message': '设置已保存'})
    return jsonify({'success': False, 'error': '保存失败'}), 400


@settings_bp.route('/update-theme', methods=['POST'])
def update_theme():
    """更新用户主题设置"""
    user_id = get_current_user_id()
    
    data = request.get_json()
    theme_color = data.get('theme_color')
    dark_mode = data.get('dark_mode')
    
    # 如果用户已登录，保存到数据库
    if user_id:
        settings_service = SettingsService(db_client.fridge)
        
        # 构建更新参数
        update_params = {}
        if theme_color:
            update_params['theme_color'] = theme_color
        if dark_mode:
            update_params['dark_mode'] = dark_mode
        
        if update_params:
            success = settings_service.update_settings(user_id, **update_params)
            if success:
                return jsonify({'success': True, 'message': '主题设置已保存', 'saved_to_server': True})
        
        return jsonify({'success': False, 'error': '保存失败'}), 400
    else:
        # 游客用户，返回成功但提示未保存到服务器
        return jsonify({'success': True, 'message': '主题已切换（未登录，仅本地生效）', 'saved_to_server': False})
