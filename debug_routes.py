# -*- coding: utf-8 -*-
"""调试路由问题"""
import sys
sys.path.insert(0, '.')

from app import create_app

app = create_app('default')

print("=" * 60)
print("所有注册的路由:")
print("=" * 60)

for rule in app.url_map.iter_rules():
    if rule.rule == '/':
        print(f"\n找到根路由 '/':")
        print(f"  端点: {rule.endpoint}")
        print(f"  方法: {rule.methods}")
        
        # 获取视图函数
        view_func = app.view_functions.get(rule.endpoint)
        if view_func:
            print(f"  视图函数: {view_func.__name__}")
            print(f"  模块: {view_func.__module__}")
            
            # 检查装饰器
            import inspect
            source = inspect.getsource(view_func)
            print(f"\n  源代码:")
            print("  " + "\n  ".join(source.split('\n')[:10]))
            
            if 'login_required' in source:
                print("\n  ⚠️ 警告: 发现 login_required 装饰器!")
            else:
                print("\n  ✓ 没有 login_required 装饰器")

print("\n" + "=" * 60)
