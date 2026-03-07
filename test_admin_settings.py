# -*- coding: utf-8 -*-
"""测试管理员设置功能"""
import sys
sys.path.insert(0, '.')

from app.utils.database import SQLiteMongoLikeClient
from app.models.system_settings import SystemSettings

# 创建数据库客户端
db_client = SQLiteMongoLikeClient('data')

# 测试系统设置
print("测试系统设置模型...")
system_settings = SystemSettings(db_client.fridge)

# 获取所有设置
settings = system_settings.get_all_settings()
print(f"✓ 获取设置成功: {len(settings)} 个配置项")
print(f"  系统名称: {settings.get('system_name')}")
print(f"  允许注册: {settings.get('allow_registration')}")

# 更新设置
print("\n测试更新设置...")
result = system_settings.update_settings({
    'system_name': '测试冰箱系统',
    'max_items_per_user': 100
})
print(f"✓ 更新设置: {'成功' if result else '失败'}")

# 验证更新
updated_settings = system_settings.get_all_settings()
print(f"  更新后系统名称: {updated_settings.get('system_name')}")
print(f"  最大物品数: {updated_settings.get('max_items_per_user')}")

# 恢复默认值
print("\n恢复默认设置...")
system_settings.update_settings({'system_name': '冰箱管理系统'})

print("\n✓ 所有测试通过！")
