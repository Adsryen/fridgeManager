# -*- coding: utf-8 -*-
"""数据库迁移脚本 - 添加冰箱表和fridge_id字段"""
import os
import sys
import sqlite3

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import Config


def migrate():
    """执行迁移"""
    DATABASE_DIR = Config.DATABASE_DIR
    db_path = os.path.join(DATABASE_DIR, 'fridge.db')
    
    if not os.path.exists(db_path):
        print(f"数据库文件不存在: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. 创建fridge表
        print("创建fridge表...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fridge (
                _id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                name TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        
        # 创建索引
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_fridge_user_id ON fridge(user_id)")
        print("✓ fridge表创建成功")
        
        # 2. 检查item表是否已有fridge_id字段
        cursor.execute("PRAGMA table_info(item)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'fridge_id' not in columns:
            print("为item表添加fridge_id字段...")
            cursor.execute("ALTER TABLE item ADD COLUMN fridge_id TEXT")
            print("✓ fridge_id字段添加成功")
        else:
            print("✓ fridge_id字段已存在")
        
        # 3. 为现有物品设置默认fridge_id
        # 公共冰箱的物品设置为'public'
        # 私人物品暂时设置为NULL,等用户创建冰箱后再关联
        print("更新现有物品的fridge_id...")
        cursor.execute("""
            UPDATE item 
            SET fridge_id = 'public' 
            WHERE user_id = 'public' AND (fridge_id IS NULL OR fridge_id = '')
        """)
        public_count = cursor.rowcount
        print(f"✓ 更新了 {public_count} 条公共冰箱物品")
        
        conn.commit()
        print("\n迁移完成!")
        
    except Exception as e:
        print(f"迁移失败: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    migrate()
