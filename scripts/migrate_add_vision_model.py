# -*- coding: utf-8 -*-
"""添加视觉模型字段"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.database import SQLiteMongoLikeClient

def migrate():
    """执行迁移"""
    print("开始迁移：添加视觉模型字段...")
    
    # 初始化数据库
    db_client = SQLiteMongoLikeClient(db_dir='data')
    conn = db_client.fridge._conn
    
    # 添加新列到数据库
    try:
        conn.execute("ALTER TABLE system_settings ADD COLUMN openai_vision_model TEXT DEFAULT 'gpt-4-vision-preview'")
        print("✓ 已添加 openai_vision_model 列")
    except Exception as e:
        if 'duplicate column name' in str(e).lower():
            print("✓ openai_vision_model 列已存在")
        else:
            print(f"添加 openai_vision_model 列时出错: {e}")
    
    try:
        conn.execute("ALTER TABLE system_settings ADD COLUMN openai_chat_model TEXT DEFAULT 'gpt-3.5-turbo'")
        print("✓ 已添加 openai_chat_model 列")
    except Exception as e:
        if 'duplicate column name' in str(e).lower():
            print("✓ openai_chat_model 列已存在")
        else:
            print(f"添加 openai_chat_model 列时出错: {e}")
    
    conn.commit()
    
    # 更新现有数据
    db = db_client.fridge
    settings = db.system_settings.find_one({})
    
    if settings:
        updates = {}
        
        # 如果有旧的 openai_model，复制到 openai_chat_model
        if 'openai_model' in settings and settings['openai_model']:
            if not settings.get('openai_chat_model'):
                updates['openai_chat_model'] = settings['openai_model']
        
        # 设置默认视觉模型
        if not settings.get('openai_vision_model'):
            updates['openai_vision_model'] = 'gpt-4-vision-preview'
        
        if updates:
            db.system_settings.update_one(
                {'_id': settings['_id']},
                {'$set': updates}
            )
            print(f"✓ 已更新设置: {list(updates.keys())}")
    
    print("迁移完成！")

if __name__ == '__main__':
    migrate()
