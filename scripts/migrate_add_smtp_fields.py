# -*- coding: utf-8 -*-
"""添加SMTP邮件服务器字段的迁移脚本"""
import os
import sys
import sqlite3

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 数据库目录
DATABASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
DB_PATH = os.path.join(DATABASE_DIR, 'fridge.db')


def migrate():
    """执行迁移"""
    print("开始迁移：添加SMTP邮件服务器字段...")
    
    if not os.path.exists(DB_PATH):
        print(f"✗ 数据库文件不存在: {DB_PATH}")
        return False
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 检查表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='system_settings'")
        if not cursor.fetchone():
            print("✗ system_settings 表不存在")
            return False
        
        # 获取现有列
        cursor.execute("PRAGMA table_info(system_settings)")
        existing_columns = {row[1] for row in cursor.fetchall()}
        
        # 需要添加的列
        new_columns = {
            'smtp_server': 'TEXT',
            'smtp_port': 'INTEGER DEFAULT 587',
            'smtp_username': 'TEXT',
            'smtp_password': 'TEXT',
            'from_email': 'TEXT',
            'from_name': 'TEXT'
        }
        
        # 添加缺失的列
        added_count = 0
        for column_name, column_type in new_columns.items():
            if column_name not in existing_columns:
                try:
                    cursor.execute(f"ALTER TABLE system_settings ADD COLUMN {column_name} {column_type}")
                    print(f"✓ 添加列: {column_name}")
                    added_count += 1
                except sqlite3.OperationalError as e:
                    print(f"✗ 添加列 {column_name} 失败: {e}")
        
        conn.commit()
        
        if added_count > 0:
            print(f"\n✓ 成功添加 {added_count} 个列")
        else:
            print("\n✓ 所有列已存在，无需迁移")
        
        print("\n迁移完成！")
        return True
        
    except Exception as e:
        print(f"✗ 迁移失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        conn.close()


if __name__ == '__main__':
    success = migrate()
    sys.exit(0 if success else 1)
