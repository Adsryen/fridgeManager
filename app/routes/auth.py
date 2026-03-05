# -*- coding: utf-8 -*-
"""认证路由"""
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from app import db_client
from app.services.user_service import UserService

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册"""
    if request.method == 'GET':
        return render_template('register.html')
    
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    
    if not username or not email or not password:
        return jsonify({'error': '所有字段都必须填写'}), 400
    
    try:
        user_service = UserService(db_client.fridge)
        user = user_service.create_user(username, email, password)
        
        # 自动登录
        session['user_id'] = user._id
        session['username'] = username
        
        return redirect(url_for('main.index'))
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


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
    
    next_url = request.args.get('next')
    if next_url:
        return redirect(next_url)
    return redirect(url_for('main.index'))


@auth_bp.route('/logout')
def logout():
    """用户登出"""
    session.clear()
    return redirect(url_for('auth.login'))
