# -*- coding: utf-8 -*-
"""添加AI功能字段的数据库迁移脚本"""
import sys
import os
import sqlite3

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def migrate():
    """执行迁移"""
    db_path = 'data/fridge.db'
    
    if not os.path.exists(db_path):
        print(f"数据库文件不存在: {db_path}")
        return
    
    print("=" * 50)
    print("开始迁移：添加AI功能字段")
    print("=" * 50)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 检查字段是否已存在
        cursor.execute("PRAGMA table_info(system_settings)")
        columns = [row[1] for row in cursor.fetchall()]
        
        fields_to_add = [
            ('enable_ai_features', 'INTEGER DEFAULT 0'),
            ('openai_api_base', 'TEXT'),
            ('openai_api_key', 'TEXT'),
            ('openai_model', "TEXT DEFAULT 'gpt-3.5-turbo'")
        ]
        
        for field_name, field_type in fields_to_add:
            if field_name not in columns:
                print(f"添加字段: {field_name}")
                cursor.execute(f"ALTER TABLE system_settings ADD COLUMN {field_name} {field_type}")
                conn.commit()
                print(f"✓ 字段 {field_name} 添加成功")
            else:
                print(f"字段 {field_name} 已存在，跳过")
        
        print("\n" + "=" * 50)
        print("迁移完成！")
        print("=" * 50)
        
    except Exception as e:
        print(f"迁移失败: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    migrate()
