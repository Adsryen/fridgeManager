# -*- coding: utf-8 -*-
"""添加主题相关字段到settings表"""
import sys
import os
import sqlite3

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def migrate():
    """执行迁移"""
    print("开始迁移：添加主题相关字段到settings表...")
    
    try:
        # 直接连接数据库文件
        db_path = os.path.join('data', 'fridge.db')
        if not os.path.exists(db_path):
            print(f"错误：数据库文件不存在: {db_path}")
            return False
        
        conn = sqlite3.connect(db_path)
        
        # 检查列是否已存在
        cursor = conn.execute("PRAGMA table_info(settings)")
        columns = [row[1] for row in cursor.fetchall()]
        
        # 添加theme_color列
        if 'theme_color' not in columns:
            print("添加theme_color列...")
            conn.execute("ALTER TABLE settings ADD COLUMN theme_color TEXT DEFAULT 'pink'")
            print("✓ theme_color列添加成功")
        else:
            print("✓ theme_color列已存在")
        
        # 添加dark_mode列
        if 'dark_mode' not in columns:
            print("添加dark_mode列...")
            conn.execute("ALTER TABLE settings ADD COLUMN dark_mode TEXT DEFAULT 'auto'")
            print("✓ dark_mode列添加成功")
        else:
            print("✓ dark_mode列已存在")
        
        conn.commit()
        conn.close()
        print("\n迁移完成！")
        
    except Exception as e:
        print(f"\n迁移失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == '__main__':
    success = migrate()
    sys.exit(0 if success else 1)
