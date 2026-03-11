#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复 system_settings 表，添加缺失的 AI 模型字段"""
import os
import sys
import sqlite3

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def migrate():
    """执行迁移"""
    print("开始迁移：修复 system_settings 表...")
    
    db_path = os.path.join('data', 'fridge.db')
    
    if not os.path.exists(db_path):
        print(f"错误: 数据库文件不存在: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 获取现有列
        cursor.execute("PRAGMA table_info(system_settings)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"现有列: {', '.join(columns)}")
        
        # 添加缺失的列
        fields_to_add = [
            ('openai_chat_model', "TEXT DEFAULT 'gpt-3.5-turbo'"),
            ('openai_vision_model', "TEXT DEFAULT 'gpt-4-vision-preview'"),
            ('openai_audio_model', "TEXT DEFAULT 'whisper-1'"),
        ]
        
        for field_name, field_type in fields_to_add:
            if field_name not in columns:
                print(f"添加 {field_name} 列...")
                cursor.execute(f"ALTER TABLE system_settings ADD COLUMN {field_name} {field_type}")
                print(f"✓ {field_name} 列添加成功")
            else:
                print(f"○ {field_name} 列已存在，跳过")
        
        conn.commit()
        conn.close()
        
        print("迁移完成！")
        return True
        
    except Exception as e:
        print(f"迁移失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = migrate()
    sys.exit(0 if success else 1)
