# -*- coding: utf-8 -*-
"""统一错误处理装饰器"""
from flask import jsonify
from functools import wraps
import traceback


def handle_errors(f):
    """统一错误处理装饰器
    
    捕获函数执行过程中的异常，并返回标准化的 JSON 错误响应
    
    Args:
        f: 被装饰的函数
        
    Returns:
        装饰后的函数
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            # 参数验证错误
            return jsonify({'success': False, 'error': str(e)}), 400
        except PermissionError as e:
            # 权限不足错误
            return jsonify({'success': False, 'error': str(e)}), 403
        except FileNotFoundError as e:
            # 资源不存在错误
            return jsonify({'success': False, 'error': str(e)}), 404
        except Exception as e:
            # 其他未预期的错误
            print(f"Error in {f.__name__}: {e}")
            traceback.print_exc()
            return jsonify({'success': False, 'error': '服务器内部错误'}), 500
    return decorated_function
