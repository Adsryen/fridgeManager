# -*- coding: utf-8 -*-
"""添加家庭功能相关表的迁移脚本"""
import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.database import SQLiteMongoLikeClient

# 数据库目录
DATABASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')


def migrate():
    """执行迁移"""
    print("开始迁移：添加家庭功能相关表...")
    
    client = SQLiteMongoLikeClient(DATABASE_DIR)
    db = client.fridge
    
    try:
        # 家庭表已经在 database.py 中自动创建
        # 这里只是验证表是否存在
        
        # 检查 family 表
        families = db.family.find({})
        print(f"✓ family 表已存在，当前记录数: {len(families)}")
        
        # 检查 family_member 表
        members = db.family_member.find({})
        print(f"✓ family_member 表已存在，当前记录数: {len(members)}")
        
        # 检查 fridge_permission 表
        permissions = db.fridge_permission.find({})
        print(f"✓ fridge_permission 表已存在，当前记录数: {len(permissions)}")
        
        print("\n迁移完成！家庭功能已就绪。")
        print("\n功能说明：")
        print("1. 用户可以创建家庭，系统会自动生成6位家庭编号")
        print("2. 其他用户可以通过家庭编号加入家庭")
        print("3. 冰箱所有者可以设置冰箱是否家庭共享")
        print("4. 可以设置家庭成员是否可以编辑共享冰箱")
        
    except Exception as e:
        print(f"✗ 迁移失败: {e}")
        return False
    finally:
        client.close()
    
    return True


if __name__ == '__main__':
    success = migrate()
    sys.exit(0 if success else 1)
