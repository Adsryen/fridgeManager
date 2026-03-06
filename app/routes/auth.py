# -*- coding: utf-8 -*-
"""认证路由"""
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from app import db_client
from app.services.user_service import UserService
from app.utils.auth import login_required, get_current_user_id
import re

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册"""
    if request.method == 'GET':
        return render_template('register.html')
    
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    
    # 验证必填字段
    if not username or not email or not password:
        return jsonify({'error': '所有字段都必须填写'}), 400
    
    # 验证用户名格式
    if not re.match(r'^[a-zA-Z0-9_\u4e00-\u9fa5]{3,20}$', username):
        return jsonify({'error': '用户名必须是 3-20 个字符，只能包含字母、数字、下划线或中文'}), 400
    
    # 验证邮箱格式
    if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
        return jsonify({'error': '邮箱格式不正确'}), 400
    
    # 验证密码强度
    if len(password) < 6:
        return jsonify({'error': '密码至少需要 6 个字符'}), 400
    
    if not re.search(r'[a-zA-Z]', password):
        return jsonify({'error': '密码必须包含字母'}), 400
    
    if not re.search(r'[0-9]', password):
        return jsonify({'error': '密码必须包含数字'}), 400
    
    try:
        user_service = UserService(db_client.fridge)
        user = user_service.create_user(username, email, password)
        
        # 自动登录
        session['user_id'] = user._id
        session['username'] = username
        session['is_admin'] = user.is_admin
        
        return jsonify({'success': True, 'message': '注册成功'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': '注册失败，请稍后重试'}), 500


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""
    if request.method == 'GET':
        return render_template('login.html')
    
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    
    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400
    
    user_service = UserService(db_client.fridge)
    user = user_service.authenticate(username, password)
    
    if not user:
        return jsonify({'error': '用户名或密码错误'}), 401
    
    session['user_id'] = user._id
    session['username'] = user.username
    session['is_admin'] = user.is_admin
    
    return jsonify({'success': True, 'message': '登录成功'}), 200


@auth_bp.route('/logout')
def logout():
    """用户登出"""
    session.clear()
    return redirect(url_for('auth.login'))


@auth_bp.route('/profile')
@login_required
def profile():
    """个人资料页面"""
    user_id = get_current_user_id()
    user_service = UserService(db_client.fridge)
    user = user_service.get_user_by_id(user_id)
    
    if not user:
        return redirect(url_for('auth.logout'))
    
    return render_template('profile.html', user=user)


@auth_bp.route('/check-username', methods=['POST'])
def check_username():
    """检查用户名是否可用"""
    username = request.form.get('username', '').strip()
    
    if not username:
        return jsonify({'available': False, 'message': '用户名不能为空'})
    
    if not re.match(r'^[a-zA-Z0-9_\u4e00-\u9fa5]{3,20}$', username):
        return jsonify({'available': False, 'message': '用户名格式不正确'})
    
    user_service = UserService(db_client.fridge)
    exists = user_service.check_username_exists(username)
    
    return jsonify({
        'available': not exists,
        'message': '用户名已被使用' if exists else '用户名可用'
    })


@auth_bp.route('/check-email', methods=['POST'])
def check_email():
    """检查邮箱是否可用"""
    email = request.form.get('email', '').strip()
    
    if not email:
        return jsonify({'available': False, 'message': '邮箱不能为空'})
    
    if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
        return jsonify({'available': False, 'message': '邮箱格式不正确'})
    
    user_service = UserService(db_client.fridge)
    exists = user_service.check_email_exists(email)
    
    return jsonify({
        'available': not exists,
        'message': '邮箱已被注册' if exists else '邮箱可用'
    })


@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """修改密码"""
    if request.method == 'GET':
        return render_template('change_password.html')
    
    user_id = get_current_user_id()
    old_password = request.form.get('old_password', '')
    new_password = request.form.get('new_password', '')
    
    if not old_password or not new_password:
        return jsonify({'error': '请填写所有字段'}), 400
    
    # 验证新密码强度
    if len(new_password) < 6:
        return jsonify({'error': '新密码至少需要 6 个字符'}), 400
    
    if not re.search(r'[a-zA-Z]', new_password):
        return jsonify({'error': '新密码必须包含字母'}), 400
    
    if not re.search(r'[0-9]', new_password):
        return jsonify({'error': '新密码必须包含数字'}), 400
    
    try:
        user_service = UserService(db_client.fridge)
        user_service.change_password(user_id, old_password, new_password)
        
        return jsonify({'success': True, 'message': '密码修改成功'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': '密码修改失败，请稍后重试'}), 500


@auth_bp.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    """更新个人资料"""
    user_id = get_current_user_id()
    email = request.form.get('email', '').strip()
    
    if not email:
        return jsonify({'error': '邮箱不能为空'}), 400
    
    if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
        return jsonify({'error': '邮箱格式不正确'}), 400
    
    try:
        user_service = UserService(db_client.fridge)
        user_service.update_user(user_id, email=email)
        
        return jsonify({'success': True, 'message': '资料更新成功'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': '资料更新失败，请稍后重试'}), 500
