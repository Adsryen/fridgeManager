# -*- coding: utf-8 -*-
"""主页路由"""
from flask import Blueprint, render_template, session
from app.utils.auth import get_current_username, login_required
from app import db_client
from app.models.system_settings import SystemSettings

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """主页 - 移动端优化版本 - 允许匿名访问"""
    username = get_current_username() or '游客'
    is_logged_in = 'user_id' in session
    
    # 获取系统设置
    system_settings = SystemSettings(db_client.fridge)
    settings = system_settings.get_all_settings()
    system_name = settings.get('system_name', '冰箱里面还有啥')
    
    return render_template('index.html', 
                         username=username, 
                         is_logged_in=is_logged_in,
                         system_name=system_name)


@main_bp.route('/mobile')
def mobile():
    """移动端页面（重定向到主页以保持兼容性）"""
    return index()


@main_bp.route('/family')
@login_required
def family():
    """家庭管理页面"""
    username = get_current_username()
    return render_template('family.html', username=username)
