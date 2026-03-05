# -*- coding: utf-8 -*-
"""测试导入"""
try:
    import auth
    print("✓ auth.py 导入成功")
except Exception as e:
    print(f"✗ auth.py 导入失败: {e}")

try:
    import app
    print("✓ app.py 导入成功")
except Exception as e:
    print(f"✗ app.py 导入失败: {e}")

print("\n所有模块检查完成！")
