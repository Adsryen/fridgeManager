#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSS文件拆分脚本
将mobile.css拆分为多个模块化的CSS文件
"""

import os
import re

# 读取原始CSS文件
with open('static/style/mobile.css', 'r', encoding='utf-8') as f:
    content = f.read()

# 定义拆分规则
splits = {
    'layout.css': {
        'start': '/* 顶部导航栏',
        'end': '/* 抽屉组件',
        'description': '/* 布局相关样式：导航栏、内容区、侧边栏、底部导航等 */'
    },
    'components.css': {
        'start': '/* 抽屉组件',
        'end': '/* ==================== 高级功能优化',
        'description': '/* 通用组件样式：抽屉、表单、卡片、按钮等 */'
    },
    'advanced.css': {
        'start': '/* ==================== 高级功能优化',
        'end': '/* ==================== 页面视图',
        'description': '/* 高级功能：下拉刷新、骨架屏、Toast、滑动删除等 */'
    },
    'pages.css': {
        'start': '/* ==================== 页面视图',
        'end': None,
        'description': '/* 页面特定样式：分类页面、统计页面、设置页面等 */'
    }
}

# 创建目录
os.makedirs('static/style/mobile', exist_ok=True)

# 拆分文件
for filename, rule in splits.items():
    start_marker = rule['start']
    end_marker = rule['end']
    
    # 找到起始位置
    start_pos = content.find(start_marker)
    if start_pos == -1:
        print(f'警告: 未找到起始标记 "{start_marker}"')
        continue
    
    # 找到结束位置
    if end_marker:
        end_pos = content.find(end_marker, start_pos)
        if end_pos == -1:
            print(f'警告: 未找到结束标记 "{end_marker}"')
            continue
        section_content = content[start_pos:end_pos]
    else:
        section_content = content[start_pos:]
    
    # 写入文件
    output_path = f'static/style/mobile/{filename}'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rule['description'] + '\n\n')
        f.write(section_content)
    
    print(f'已创建: {output_path}')

print('\nCSS拆分完成！')
print('请在HTML中使用以下导入顺序：')
print('1. variables.css')
print('2. base.css')
print('3. layout.css')
print('4. components.css')
print('5. advanced.css')
print('6. pages.css')
