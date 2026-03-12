# -*- coding: utf-8 -*-
"""定时任务调度器"""
import threading
import time
from datetime import datetime, timedelta
from app.models.system_settings import SystemSettings


class TaskScheduler:
    """定时任务调度器"""
    
    def __init__(self, db):
        self.db = db
        self.running = False
        self.thread = None
    
    def start(self):
        """启动调度器"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        print("[定时任务] 调度器已启动")
    
    def stop(self):
        """停止调度器"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("[定时任务] 调度器已停止")
    
    def _run(self):
        """运行调度器主循环"""
        last_cleanup = None
        
        while self.running:
            try:
                now = datetime.now()
                
                # 每天凌晨3点执行清理任务
                if last_cleanup is None or (now.hour == 3 and now.date() != last_cleanup.date()):
                    self._auto_delete_expired_items()
                    self._cleanup_old_logs()
                    last_cleanup = now
                
                # 每小时检查一次
                time.sleep(3600)
                
            except Exception as e:
                print(f"[定时任务] 错误: {e}")
                time.sleep(60)
    
    def _auto_delete_expired_items(self):
        """自动删除过期物品"""
        try:
            system_settings = SystemSettings(self.db)
            settings = system_settings.get_all_settings()
            
            # 检查是否启用自动删除
            if not settings.get('auto_delete_expired', False):
                return
            
            auto_delete_days = settings.get('auto_delete_days', 7)
            cutoff_date = (datetime.now() - timedelta(days=auto_delete_days)).strftime('%Y-%m-%dT%H:%M:%S.000Z')
            
            # 查找过期超过指定天数的物品
            all_items = self.db.item.find({})
            expired_items = [item for item in all_items if item.get('ExpireDate', '') < cutoff_date]
            count = len(expired_items)
            
            if count > 0:
                for item in expired_items:
                    self.db.item.delete_one({'_id': item['_id']})
                print(f"[定时任务] 自动删除了 {count} 个过期物品")
            
        except Exception as e:
            print(f"[定时任务] 自动删除过期物品失败: {e}")
    
    def _cleanup_old_logs(self):
        """清理旧日志（保留90天）"""
        try:
            from app.models.login_log import LoginLog
            
            login_log = LoginLog(self.db)
            count = login_log.clear_old_logs(days=90)
            
            if count > 0:
                print(f"[定时任务] 清理了 {count} 条旧日志")
            
        except Exception as e:
            print(f"[定时任务] 清理旧日志失败: {e}")


# 全局调度器实例
_scheduler = None


def get_scheduler(db):
    """获取调度器实例"""
    global _scheduler
    if _scheduler is None:
        _scheduler = TaskScheduler(db)
    return _scheduler


def start_scheduler(db):
    """启动调度器"""
    scheduler = get_scheduler(db)
    scheduler.start()
    return scheduler


def stop_scheduler():
    """停止调度器"""
    global _scheduler
    if _scheduler:
        _scheduler.stop()
