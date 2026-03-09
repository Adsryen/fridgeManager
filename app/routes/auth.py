# -*- coding: utf-8 -*-
"""认证路由 - RESTful API"""
from flask import Blueprint, request, jsonify
from app import db_client
from app.services.user_service import UserService
from app.utils.jwt_auth import jwt_required, admin_required, generate_token, get_current_user
from datetime import datetime
import re

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册 API"""
    from app.models.system_settings import SystemSettings
    
    # 检查是否允许注册
    system_settings = SystemSettings(db_client.fridge)
    settings = system_settings.get_all_settings()
    
    if not settings.get('allow_registration', True):
        return jsonify({'success': False, 'error': '系统当前不允许新用户注册'}), 403
    
    data = request.get_json() if request.is_json else request.form
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    # 验证必填字段
    if not username or not email or not password:
        return jsonify({'success': False, 'error': '所有字段都必须填写'}), 400
    
    # 验证用户名格式
    if not re.match(r'^[a-zA-Z0-9_\u4e00-\u9fa5]{3,20}$', username):
        return jsonify({'success': False, 'error': '用户名必须是 3-20 个字符，只能包含字母、数字、下划线或中文'}), 400
    
    # 验证邮箱格式
    if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
        return jsonify({'success': False, 'error': '邮箱格式不正确'}), 400
    
    # 从设置中获取密码最小长度
    min_password_length = settings.get('min_password_length', 6)
    
    # 验证密码强度
    if len(password) < min_password_length:
        return jsonify({'success': False, 'error': f'密码至少需要 {min_password_length} 个字符'}), 400
    
    if not re.search(r'[a-zA-Z]', password):
        return jsonify({'success': False, 'error': '密码必须包含字母'}), 400
    
    if not re.search(r'[0-9]', password):
        return jsonify({'success': False, 'error': '密码必须包含数字'}), 400
    
    try:
        user_service = UserService(db_client.fridge)
        user = user_service.create_user(username, email, password)
        
        return jsonify({'success': True, 'message': '注册成功'}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': '注册失败，请稍后重试'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录 API"""
    from app.models.system_settings import SystemSettings
    from app.models.login_log import LoginLog
    
    data = request.get_json() if request.is_json else request.form
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    print(f'[登录调试] 收到登录请求 - 用户名: {username}, 密码长度: {len(password)}')
    
    if not username or not password:
        print('[登录调试] 用户名或密码为空')
        return jsonify({'success': False, 'error': '用户名和密码不能为空'}), 400
    
    # 获取系统设置
    system_settings = SystemSettings(db_client.fridge)
    settings = system_settings.get_all_settings()
    
    # 获取IP地址和User-Agent
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent', '')
    
    # 检查是否启用登录日志
    enable_login_log = settings.get('enable_login_log', True)
    
    # 检查登录尝试次数限制
    if enable_login_log:
        login_log = LoginLog(db_client.fridge)
        max_attempts = settings.get('max_login_attempts', 5)
        failed_attempts = login_log.get_failed_attempts(username, minutes=30)
        
        if failed_attempts >= max_attempts:
            error_msg = f'登录尝试次数过多，请30分钟后再试'
            login_log.log_login(None, username, False, ip_address, user_agent, error_msg)
            return jsonify({'success': False, 'error': error_msg}), 429
    
    user_service = UserService(db_client.fridge)
    user = user_service.authenticate(username, password)
    
    print(f'[登录调试] 认证结果: {"成功" if user else "失败"}')
    
    if not user:
        error_msg = '用户名或密码错误'
        if enable_login_log:
            login_log = LoginLog(db_client.fridge)
            login_log.log_login(None, username, False, ip_address, user_agent, error_msg)
        return jsonify({'success': False, 'error': error_msg}), 401
    
    # 检查账号是否被禁用
    if not user.is_active:
        print(f'[登录调试] 账号已被禁用')
        error_msg = '账号已被禁用'
        if enable_login_log:
            login_log = LoginLog(db_client.fridge)
            login_log.log_login(user._id, username, False, ip_address, user_agent, error_msg)
        return jsonify({'success': False, 'error': error_msg}), 403
    
    # 生成 JWT Token
    token = generate_token(
        user_id=str(user._id),
        username=user.username,
        email=user.email,
        is_admin=user.is_admin
    )
    
    # 记录成功登录
    if enable_login_log:
        login_log = LoginLog(db_client.fridge)
        login_log.log_login(user._id, username, True, ip_address, user_agent)
    
    print(f'[登录调试] 登录成功 - 用户ID: {user._id}, 是否管理员: {user.is_admin}')
    
    # 返回 Token 和用户信息
    return jsonify({
        'success': True,
        'message': '登录成功',
        'token': token,
        'user': {
            'id': str(user._id),
            'username': user.username,
            'email': user.email,
            'is_admin': user.is_admin,
            'is_active': user.is_active
        }
    }), 200


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """用户登出 API"""
    # JWT 是无状态的，登出由前端处理（清除 localStorage 中的 Token）
    return jsonify({'success': True, 'message': '登出成功'}), 200


@auth_bp.route('/profile', methods=['GET'])
@jwt_required
def profile():
    """获取用户信息 API"""
    current_user = get_current_user()
    user_id = current_user['user_id']
    
    user_service = UserService(db_client.fridge)
    user = user_service.get_user_by_id(user_id)
    
    if not user:
        return jsonify({'success': False, 'error': '用户不存在'}), 404
    
    return jsonify({
        'success': True,
        'data': {
            'id': str(user._id),
            'username': user.username,
            'email': user.email,
            'is_admin': user.is_admin,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat() if hasattr(user, 'created_at') and user.created_at else None
        }
    }), 200


@auth_bp.route('/profile', methods=['PUT'])
@jwt_required
def update_profile():
    """更新个人资料 API"""
    current_user = get_current_user()
    user_id = current_user['user_id']
    
    data = request.get_json() if request.is_json else request.form
    email = data.get('email', '').strip()
    username = data.get('username', '').strip()
    
    update_data = {}
    
    # 验证邮箱
    if email:
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            return jsonify({'success': False, 'error': '邮箱格式不正确'}), 400
        update_data['email'] = email
    
    # 验证用户名
    if username:
        if not re.match(r'^[a-zA-Z0-9_\u4e00-\u9fa5]{3,20}$', username):
            return jsonify({'success': False, 'error': '用户名格式不正确(3-20个字符,支持中英文、数字、下划线)'}), 400
        update_data['username'] = username
    
    if not update_data:
        return jsonify({'success': False, 'error': '没有需要更新的内容'}), 400
    
    try:
        user_service = UserService(db_client.fridge)
        success = user_service.update_user(user_id, **update_data)
        
        if success or update_data:
            # 获取更新后的用户信息
            user = user_service.get_user_by_id(user_id)
            return jsonify({
                'success': True,
                'message': '资料更新成功',
                'data': {
                    'id': str(user._id),
                    'username': user.username,
                    'email': user.email,
                    'is_admin': user.is_admin
                }
            }), 200
        else:
            return jsonify({'success': False, 'error': '没有内容被更新'}), 400
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': '资料更新失败，请稍后重试'}), 500


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required
def change_password():
    """修改密码 API"""
    from app.models.system_settings import SystemSettings
    
    current_user = get_current_user()
    user_id = current_user['user_id']
    
    data = request.get_json() if request.is_json else request.form
    old_password = data.get('old_password', '')
    new_password = data.get('new_password', '')
    
    if not old_password or not new_password:
        return jsonify({'success': False, 'error': '请填写所有字段'}), 400
    
    # 从设置中获取密码最小长度
    system_settings = SystemSettings(db_client.fridge)
    settings = system_settings.get_all_settings()
    min_password_length = settings.get('min_password_length', 6)
    
    # 验证新密码强度
    if len(new_password) < min_password_length:
        return jsonify({'success': False, 'error': f'新密码至少需要 {min_password_length} 个字符'}), 400
    
    if not re.search(r'[a-zA-Z]', new_password):
        return jsonify({'success': False, 'error': '新密码必须包含字母'}), 400
    
    if not re.search(r'[0-9]', new_password):
        return jsonify({'success': False, 'error': '新密码必须包含数字'}), 400
    
    try:
        user_service = UserService(db_client.fridge)
        user_service.change_password(user_id, old_password, new_password)
        
        return jsonify({'success': True, 'message': '密码修改成功'}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': '密码修改失败，请稍后重试'}), 500



@auth_bp.route('/check-username', methods=['POST'])
def check_username():
    """检查用户名是否可用 API"""
    data = request.get_json() if request.is_json else request.form
    username = data.get('username', '').strip()
    
    if not username:
        return jsonify({'success': False, 'available': False, 'message': '用户名不能为空'})
    
    if not re.match(r'^[a-zA-Z0-9_\u4e00-\u9fa5]{3,20}$', username):
        return jsonify({'success': False, 'available': False, 'message': '用户名格式不正确'})
    
    user_service = UserService(db_client.fridge)
    exists = user_service.check_username_exists(username)
    
    return jsonify({
        'success': True,
        'available': not exists,
        'message': '用户名已被使用' if exists else '用户名可用'
    })


@auth_bp.route('/check-email', methods=['POST'])
def check_email():
    """检查邮箱是否可用 API"""
    data = request.get_json() if request.is_json else request.form
    email = data.get('email', '').strip()
    
    if not email:
        return jsonify({'success': False, 'available': False, 'message': '邮箱不能为空'})
    
    if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
        return jsonify({'success': False, 'available': False, 'message': '邮箱格式不正确'})
    
    user_service = UserService(db_client.fridge)
    exists = user_service.check_email_exists(email)
    
    return jsonify({
        'success': True,
        'available': not exists,
        'message': '邮箱已被注册' if exists else '邮箱可用'
    })


@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """忘记密码 - 发送重置邮件 API"""
    from app.models.password_reset import PasswordResetToken
    from app.utils.email import send_password_reset_email
    
    data = request.get_json()
    email = data.get('email', '').strip()
    
    if not email:
        return jsonify({'success': False, 'error': '请输入邮箱地址'}), 400
    
    # 验证邮箱格式
    if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
        return jsonify({'success': False, 'error': '邮箱格式不正确'}), 400
    
    try:
        # 查找用户
        user_service = UserService(db_client.fridge)
        user = db_client.find_one('users', {'email': email})
        
        if not user:
            # 为了安全，即使用户不存在也返回成功
            return jsonify({'success': True, 'message': '如果该邮箱已注册，重置链接将发送到您的邮箱'}), 200
        
        # 创建重置令牌
        token = PasswordResetToken.create_token(db_client, str(user['_id']), email)
        
        # 发送重置邮件
        if send_password_reset_email(email, token, user['username']):
            return jsonify({'success': True, 'message': '重置链接已发送到您的邮箱'}), 200
        else:
            return jsonify({'success': False, 'error': '邮件发送失败，请检查邮箱配置或稍后重试'}), 500
    
    except Exception as e:
        print(f'忘记密码处理失败: {e}')
        return jsonify({'success': False, 'error': '处理失败，请稍后重试'}), 500


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """重置密码 API"""
    from app.models.password_reset import PasswordResetToken
    
    data = request.get_json()
    token = data.get('token', '')
    new_password = data.get('password', '')
    
    if not token or not new_password:
        return jsonify({'success': False, 'error': '缺少必要参数'}), 400
    
    # 验证令牌
    token_data = PasswordResetToken.verify_token(db_client, token)
    if not token_data:
        return jsonify({'success': False, 'error': '重置链接已失效或已使用'}), 400
    
    # 验证密码强度
    if len(new_password) < 6:
        return jsonify({'success': False, 'error': '密码长度至少为6个字符'}), 400
    
    if not re.search(r'[a-zA-Z]', new_password):
        return jsonify({'success': False, 'error': '密码必须包含字母'}), 400
    
    if not re.search(r'\d', new_password):
        return jsonify({'success': False, 'error': '密码必须包含数字'}), 400
    
    try:
        # 更新密码
        user_service = UserService(db_client.fridge)
        user_service.update_password(token_data['user_id'], new_password)
        
        # 标记令牌为已使用
        PasswordResetToken.mark_as_used(db_client, token)
        
        return jsonify({'success': True, 'message': '密码重置成功，请使用新密码登录'}), 200
    
    except Exception as e:
        print(f'密码重置失败: {e}')
        return jsonify({'success': False, 'error': '密码重置失败，请稍后重试'}), 500
