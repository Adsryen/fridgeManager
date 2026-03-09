# -*- coding: utf-8 -*-
"""数据库迁移：为用户设置添加 current_fridge_id 字段"""
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.database import SQLiteMongoLikeClient


def migrate():
    """执行迁移"""
    print('开始迁移：为用户设置添加 current_fridge_id 字段...')
    
    # 初始化数据库
    db_client = SQLiteMongoLikeClient(db_dir='data')
    conn = db_client.fridge._conn
    
    # 添加新列到数据库
    try:
        cursor = conn.cursor()
        cursor.execute("""
            ALTER TABLE settings ADD COLUMN current_fridge_id TEXT DEFAULT 'public'
        """)
        conn.commit()
        print('✓ 已添加 current_fridge_id 列到 settings 表')
    except Exception as e:
        if 'duplicate column name' in str(e).lower():
            print('✓ current_fridge_id 列已存在，跳过')
        else:
            print(f'✗ 添加列失败: {e}')
            return
    
    # 更新现有数据
    db = db_client.fridge
    settings_collection = db.settings.find({})
    
    updated_count = 0
    for settings in settings_collection:
        if 'current_fridge_id' not in settings or settings['current_fridge_id'] is None:
            db.settings.update_one(
                {'_id': settings['_id']},
                {'$set': {'current_fridge_id': 'public'}}
            )
            updated_count += 1
    
    print(f'✓ 已更新 {updated_count} 条用户设置记录')
    
    db_client.close()
    print('迁移完成！')


if __name__ == '__main__':
    migrate()
