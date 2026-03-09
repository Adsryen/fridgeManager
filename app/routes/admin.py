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


@admin_bp.route('/ai-settings')
@admin_required
def ai_settings():
    """AI设置页面"""
    system_settings = SystemSettings(db_client.fridge)
    settings = system_settings.get_all_settings()
    return render_template('admin/ai_settings.html', settings=settings)


@admin_bp.route('/ai/test-connection', methods=['POST'])
@admin_required
def test_ai_connection():
    """测试AI API连接"""
    import requests
    
    data = request.get_json()
    api_base = data.get('api_base', '').strip()
    api_key = data.get('api_key', '').strip()
    
    if not api_base or not api_key:
        return jsonify({'success': False, 'error': 'API地址和密钥不能为空'}), 400
    
    # 确保API地址格式正确
    if not api_base.startswith('http'):
        api_base = 'https://' + api_base
    
    # 移除末尾的斜杠
    api_base = api_base.rstrip('/')
    
    try:
        # 调用OpenAI协议的models接口测试连接
        url = f"{api_base}/models"
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return jsonify({
                'success': True,
                'message': 'API连接测试成功'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': f'API返回错误: {response.status_code} - {response.text}'
            }), 400
        
    except requests.exceptions.Timeout:
        return jsonify({
            'success': False,
            'error': '连接超时，请检查API地址是否正确'
        }), 500
    except requests.exceptions.ConnectionError:
        return jsonify({
            'success': False,
            'error': '无法连接到API服务器，请检查网络和API地址'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'连接失败: {str(e)}'
        }), 500


@admin_bp.route('/ai/list-models', methods=['POST'])
@admin_required
def list_ai_models():
    """获取可用的AI模型列表"""
    try:
        import requests
    except ImportError as e:
        print(f"[AI API] 导入requests失败: {e}")
        return jsonify({'success': False, 'error': 'requests模块未安装，请运行: pip install requests'}), 500
    
    try:
        data = request.get_json()
        print(f"[AI API] 收到请求数据: {data}")
        
        if not data:
            return jsonify({'success': False, 'error': '请求数据为空'}), 400
            
        api_base = data.get('api_base', '').strip()
        api_key = data.get('api_key', '').strip()
        
        print(f"[AI API] API地址: {api_base}")
        print(f"[AI API] API密钥长度: {len(api_key) if api_key else 0}")
        
        if not api_base or not api_key:
            return jsonify({'success': False, 'error': 'API地址和密钥不能为空'}), 400
    except Exception as e:
        print(f"[AI API] 解析请求数据失败: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': f'解析请求数据失败: {str(e)}'}), 400
    
    # 确保API地址格式正确
    if not api_base.startswith('http'):
        api_base = 'https://' + api_base
    
    # 移除末尾的斜杠
    api_base = api_base.rstrip('/')
    
    print(f"[AI API] 处理后的API地址: {api_base}")
    
    try:
        # 调用OpenAI协议的models接口
        url = f"{api_base}/models"
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        print(f"[AI API] 请求URL: {url}")
        
        response = requests.get(url, headers=headers, timeout=15)
        
        print(f"[AI API] 响应状态码: {response.status_code}")
        print(f"[AI API] 响应内容: {response.text[:200]}")  # 只打印前200字符
        
        if response.status_code == 200:
            result = response.json()
            print(f"[AI API] 解析JSON成功")
            
            # 解析模型列表
            models = []
            if 'data' in result:
                # 标准OpenAI格式
                print(f"[AI API] 使用标准OpenAI格式，data字段包含 {len(result['data'])} 项")
                for model in result['data']:
                    if isinstance(model, dict) and 'id' in model:
                        models.append(model['id'])
                    elif isinstance(model, str):
                        models.append(model)
            elif isinstance(result, list):
                # 某些API直接返回列表
                print(f"[AI API] 直接返回列表格式，包含 {len(result)} 项")
                for model in result:
                    if isinstance(model, dict) and 'id' in model:
                        models.append(model['id'])
                    elif isinstance(model, str):
                        models.append(model)
            
            print(f"[AI API] 解析出 {len(models)} 个模型")
            
            # 过滤和排序模型
            # 优先显示常用的聊天模型
            chat_models = [m for m in models if any(x in m.lower() for x in ['gpt', 'claude', 'chat', 'turbo'])]
            other_models = [m for m in models if m not in chat_models]
            
            # 排序：GPT-4 > GPT-3.5 > Claude > 其他
            def model_priority(model_name):
                model_lower = model_name.lower()
                if 'gpt-4' in model_lower:
                    return 0
                elif 'gpt-3.5' in model_lower or 'gpt-35' in model_lower:
                    return 1
                elif 'claude' in model_lower:
                    return 2
                elif 'gpt' in model_lower:
                    return 3
                else:
                    return 4
            
            chat_models.sort(key=model_priority)
            sorted_models = chat_models + sorted(other_models)
            
            print(f"[AI API] 排序后的模型列表: {sorted_models[:5]}...")  # 只打印前5个
            
            if not sorted_models:
                return jsonify({
                    'success': False,
                    'error': '未找到可用的模型'
                }), 404
            
            return jsonify({
                'success': True,
                'models': sorted_models
            }), 200
        else:
            error_msg = f'获取模型列表失败: {response.status_code} - {response.text}'
            print(f"[AI API] {error_msg}")
            return jsonify({
                'success': False,
                'error': error_msg
            }), 400
        
    except requests.exceptions.Timeout as e:
        print(f"[AI API] 请求超时: {e}")
        return jsonify({
            'success': False,
            'error': '请求超时，请稍后重试'
        }), 500
    except requests.exceptions.ConnectionError as e:
        print(f"[AI API] 连接错误: {e}")
        return jsonify({
            'success': False,
            'error': '无法连接到API服务器'
        }), 500
    except Exception as e:
        print(f"[AI API] 未知错误: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'获取模型列表失败: {str(e)}'
        }), 500
