# -*- coding: utf-8 -*-
"""简单测试主页路由"""

# 直接测试路由函数
from flask import Flask, session
from app.routes.main import main_bp

app = Flask(__name__)
app.secret_key = 'test-secret-key'
app.register_blueprint(main_bp)

print("测试主页路由...")
print(f"路由规则: {[str(rule) for rule in app.url_map.iter_rules()]}")

# 查找主页路由
for rule in app.url_map.iter_rules():
    if rule.rule == '/':
        print(f"\n找到主页路由:")
        print(f"  端点: {rule.endpoint}")
        print(f"  方法: {rule.methods}")
        
        # 获取视图函数
        view_func = app.view_functions.get(rule.endpoint)
        if view_func:
            print(f"  视图函数: {view_func.__name__}")
            
            # 检查是否有装饰器
            if hasattr(view_func, '__wrapped__'):
                print(f"  有装饰器包装")
            else:
                print(f"  没有装饰器包装")

print("\n检查完成！")
