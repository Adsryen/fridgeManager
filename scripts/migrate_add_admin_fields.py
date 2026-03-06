# -*- coding: utf-8 -*-
"""数据库迁移：添加管理员和激活状态字段"""
import sys
import os
import sqlite3

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def migrate():
    """执行数据库迁移"""
    db_path = 'data/fridge.db'
    
    if not os.path.exists(db_path):
        print('数据库文件不存在，无需迁移')
        return
    
    print('开始数据库迁移...')
    print(f'数据库路径: {db_path}')
    
    # 连接数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 检查 user 表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user'")
        if not cursor.fetchone():
            print('user 表不存在，无需迁移')
            conn.close()
            return
        
        # 检查字段是否已存在
        cursor.execute("PRAGMA table_info(user)")
        columns = [row[1] for row in cursor.fetchall()]
        
        # 添加 is_admin 字段
        if 'is_admin' not in columns:
            print('添加 is_admin 字段...')
            cursor.execute('ALTER TABLE user ADD COLUMN is_admin INTEGER DEFAULT 0')
            print('✓ is_admin 字段添加成功')
        else:
            print('is_admin 字段已存在')
        
        # 添加 is_active 字段
        if 'is_active' not in columns:
            print('添加 is_active 字段...')
            cursor.execute('ALTER TABLE user ADD COLUMN is_active INTEGER DEFAULT 1')
            print('✓ is_active 字段添加成功')
        else:
            print('is_active 字段已存在')
        
        # 提交更改
        conn.commit()
        print('\n✓ 数据库迁移完成！')
        
    except Exception as e:
        print(f'\n✗ 迁移失败: {e}')
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    try:
        migrate()
    except Exception as e:
        print(f'\n错误: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)
