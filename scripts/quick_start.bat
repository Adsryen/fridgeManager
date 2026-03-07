@echo off
chcp 65001 >nul
echo ========================================
echo 冰箱里面还有啥 - 快速启动
echo ========================================
echo.

echo [1/3] 检查数据库...
if not exist "data" mkdir data
if not exist "data\fridge.db" (
    echo ✓ 首次运行，将自动创建数据库
) else (
    echo ✓ 数据库已存在
)
echo.

echo [2/3] 初始化管理员账号...
py scripts\init_admin.py
echo.

echo [3/3] 启动服务器...
echo.
echo 服务器将在以下地址运行：
echo   - 本地访问: http://127.0.0.1:8080
echo   - 局域网访问: http://192.168.0.138:8080
echo.
echo 按 Ctrl+C 停止服务器
echo ========================================
echo.

py run.py

pause
