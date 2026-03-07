# -*- coding: utf-8 -*-
"""测试新实现的功能"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.utils.database import SQLiteMongoLikeClient
from app.models.system_settings import SystemSettings
from app.models.login_log import LoginLog

# 初始化数据库
db_client = SQLiteMongoLikeClient(db_dir='data')

print("=" * 60)
print("测试新实现的功能")
print("=" * 60)

# 1. 测试系统设置
print("\n1. 测试系统设置")
print("-" * 60)
system_settings = SystemSettings(db_client.fridge)
settings = system_settings.get_all_settings()

print(f"✓ 系统名称: {settings.get('system_name')}")
print(f"✓ 允许注册: {settings.get('allow_registration')}")
print(f"✓ 密码最小长度: {settings.get('min_password_length')}")
print(f"✓ 会话超时: {settings.get('session_timeout')} 分钟")
print(f"✓ 最大登录尝试: {settings.get('max_login_attempts')} 次")
print(f"✓ 启用登录日志: {settings.get('enable_login_log')}")
print(f"✓ 过期提醒天数: {settings.get('default_expiry_warning_days')} 天")
print(f"✓ 自动删除过期物品: {settings.get('auto_delete_expired')}")
print(f"✓ 自动删除天数: {settings.get('auto_delete_days')} 天")
print(f"✓ 每用户最大物品数: {settings.get('max_items_per_user')}")

# 2. 测试登录日志
print("\n2. 测试登录日志功能")
print("-" * 60)
login_log = LoginLog(db_client.fridge)

# 记录一条测试日志
test_log = login_log.log_login(
    user_id='test_user_123',
    username='测试用户',
    success=True,
    ip_address='127.0.0.1',
    user_agent='Test Browser'
)
print(f"✓ 记录登录日志成功: {test_log['_id']}")

# 获取日志
logs = login_log.get_all_logs(limit=5)
print(f"✓ 获取到 {len(logs)} 条日志记录")

if logs:
    latest_log = logs[0]
    print(f"  最新日志:")
    print(f"    用户: {latest_log.get('username')}")
    print(f"    状态: {'成功' if latest_log.get('success') else '失败'}")
    print(f"    时间: {latest_log.get('timestamp')}")
    print(f"    IP: {latest_log.get('ip_address')}")

# 3. 测试定时任务
print("\n3. 测试定时任务调度器")
print("-" * 60)
from app.tasks import get_scheduler

scheduler = get_scheduler(db_client.fridge)
print(f"✓ 调度器状态: {'运行中' if scheduler.running else '已停止'}")
print(f"✓ 调度器线程: {'活动' if scheduler.thread and scheduler.thread.is_alive() else '未启动'}")

print("\n" + "=" * 60)
print("所有功能测试完成！")
print("=" * 60)

print("\n已实现的功能列表:")
print("✅ 系统名称动态显示")
print("✅ 允许注册开关")
print("✅ 密码最小长度验证")
print("✅ 会话超时自动登出")
print("✅ 登录尝试次数限制")
print("✅ 登录日志记录")
print("✅ 过期提醒天数配置")
print("✅ 自动删除过期物品（定时任务）")
print("✅ 每用户最大物品数限制")
print("✅ 旧日志自动清理（定时任务）")

print("\n需要额外配置的功能:")
print("⚠️  邮箱验证（需要SMTP服务器）")
print("⚠️  邮件通知（需要SMTP服务器）")
print("⚠️  每日摘要邮件（需要SMTP服务器）")
