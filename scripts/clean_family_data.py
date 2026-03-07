# -*- coding: utf-8 -*-
"""清理家庭测试数据"""
import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.database import SQLiteMongoLikeClient

# 数据库目录
DATABASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')


def clean_family_data():
    """清理家庭数据"""
    print("开始清理家庭测试数据...")
    
    client = SQLiteMongoLikeClient(DATABASE_DIR)
    db = client.fridge
    
    try:
        # 删除所有家庭
        families = db.family.find({})
        family_count = len(families)
        db.family.delete_many({})
        print(f"✓ 删除了 {family_count} 个家庭")
        
        # 删除所有家庭成员
        members = db.family_member.find({})
        member_count = len(members)
        db.family_member.delete_many({})
        print(f"✓ 删除了 {member_count} 条家庭成员记录")
        
        # 删除所有冰箱权限
        permissions = db.fridge_permission.find({})
        permission_count = len(permissions)
        db.fridge_permission.delete_many({})
        print(f"✓ 删除了 {permission_count} 条冰箱权限记录")
        
        print("\n清理完成！现在可以重新开始使用家庭功能了。")
        return True
        
    except Exception as e:
        print(f"✗ 清理失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        client.close()


if __name__ == '__main__':
    success = clean_family_data()
    sys.exit(0 if success else 1)
