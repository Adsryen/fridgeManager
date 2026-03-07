# -*- coding: utf-8 -*-
"""测试修改的代码"""

# 测试导入
try:
    from app.utils.auth import get_effective_user_id, is_viewing_public
    print("✓ auth.py 导入成功")
except Exception as e:
    print(f"✗ auth.py 导入失败: {e}")

try:
    from app.services.user_service import UserService
    print("✓ user_service.py 导入成功")
except Exception as e:
    print(f"✗ user_service.py 导入失败: {e}")

try:
    from app.routes.item import item_bp
    print("✓ item.py 导入成功")
except Exception as e:
    print(f"✗ item.py 导入失败: {e}")

try:
    from app.routes.main import main_bp
    print("✓ main.py 导入成功")
except Exception as e:
    print(f"✗ main.py 导入失败: {e}")

print("\n所有导入测试完成！")
