# -*- coding: utf-8 -*-
"""数据迁移脚本：为现有 item 添加 user_id 字段"""
import sqlite3
import os

def migrate():
    db_path = os.path.join('data', 'fridge.db')
    
    if not os.path.exists(db_path):
        print("数据库文件不存在，无需迁移")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 检查 item 表是否存在 user_id 列
    cursor.execute("PRAGMA table_info(item)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'user_id' in columns:
        print("user_id 列已存在，无需迁移")
        conn.close()
        return
    
    print("开始迁移...")
    
    # 添加 user_id 列
    try:
        cursor.execute("ALTER TABLE item ADD COLUMN user_id TEXT")
        print("✓ 已添加 user_id 列")
    except Exception as e:
        print(f"添加列失败: {e}")
        conn.close()
        return
    
    # 检查是否有现有数据
    cursor.execute("SELECT COUNT(*) FROM item WHERE user_id IS NULL")
    count = cursor.fetchone()[0]
    
    if count > 0:
        print(f"发现 {count} 条旧数据")
        print("警告：这些数据没有关联用户，建议手动处理或删除")
        print("你可以：")
        print("1. 删除这些数据：DELETE FROM item WHERE user_id IS NULL")
        print("2. 分配给特定用户：UPDATE item SET user_id='用户ID' WHERE user_id IS NULL")
    
    conn.commit()
    conn.close()
    print("迁移完成！")

if __name__ == '__main__':
    migrate()
