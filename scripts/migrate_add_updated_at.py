# -*- coding: utf-8 -*-
"""数据库迁移脚本 - 添加updated_at字段"""
import sys
import os
import sqlite3
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def migrate_add_updated_at():
    """为所有表添加updated_at字段"""
    print("开始数据库迁移: 添加updated_at字段...")
    
    # 连接数据库
    db_path = os.path.join('data', 'fridge.db')
    if not os.path.exists(db_path):
        print(f"❌ 数据库文件不存在: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        # 1. 为user表添加updated_at字段
        print("\n1. 处理user表...")
        try:
            cursor.execute("ALTER TABLE user ADD COLUMN updated_at TEXT")
            print("   ✓ 添加updated_at列")
        except sqlite3.OperationalError as e:
            if 'duplicate column name' in str(e).lower():
                print("   - updated_at列已存在,跳过")
            else:
                raise
        
        # 更新现有记录
        cursor.execute("UPDATE user SET updated_at = created_at WHERE updated_at IS NULL")
        updated_users = cursor.rowcount
        print(f"   ✓ 更新了 {updated_users} 个用户记录")
        
        # 2. 为item表添加updated_at字段
        print("\n2. 处理item表...")
        try:
            cursor.execute("ALTER TABLE item ADD COLUMN updated_at TEXT")
            print("   ✓ 添加updated_at列")
        except sqlite3.OperationalError as e:
            if 'duplicate column name' in str(e).lower():
                print("   - updated_at列已存在,跳过")
            else:
                raise
        
        # 更新现有记录(item表没有创建时间字段,使用当前时间)
        cursor.execute(f"UPDATE item SET updated_at = '{current_time}' WHERE updated_at IS NULL")
        updated_items = cursor.rowcount
        print(f"   ✓ 更新了 {updated_items} 个物品记录")
        
        # 3. 为settings表添加updated_at字段
        print("\n3. 处理settings表...")
        try:
            cursor.execute("ALTER TABLE settings ADD COLUMN updated_at TEXT")
            print("   ✓ 添加updated_at列")
        except sqlite3.OperationalError as e:
            if 'duplicate column name' in str(e).lower():
                print("   - updated_at列已存在,跳过")
            else:
                raise
        
        # 更新现有记录
        cursor.execute(f"UPDATE settings SET updated_at = '{current_time}' WHERE updated_at IS NULL")
        updated_settings = cursor.rowcount
        print(f"   ✓ 更新了 {updated_settings} 个设置记录")
        
        # 4. 为system_settings表添加updated_at字段
        print("\n4. 处理system_settings表...")
        try:
            cursor.execute("ALTER TABLE system_settings ADD COLUMN updated_at TEXT")
            print("   ✓ 添加updated_at列")
        except sqlite3.OperationalError as e:
            if 'duplicate column name' in str(e).lower():
                print("   - updated_at列已存在,跳过")
            else:
                raise
        
        # 更新现有记录
        cursor.execute(f"UPDATE system_settings SET updated_at = '{current_time}' WHERE updated_at IS NULL")
        updated_system_settings = cursor.rowcount
        print(f"   ✓ 更新了 {updated_system_settings} 个系统设置记录")
        
        # 提交更改
        conn.commit()
        
        print("\n✅ 数据库迁移完成!")
        print(f"总计更新: {updated_users + updated_items + updated_settings + updated_system_settings} 条记录")
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


if __name__ == '__main__':
    try:
        migrate_add_updated_at()
    except Exception as e:
        print(f"\n❌ 迁移失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
