@echo off
chcp 65001 >nul
echo 启动冰箱管理系统...
echo.

REM 检查虚拟环境
if exist venv\Scripts\activate.bat (
    echo 激活虚拟环境...
    call venv\Scripts\activate.bat
) else (
    echo 警告: 未找到虚拟环境，使用全局 Python
)

REM 安装依赖
echo 检查依赖...
py -m pip install -r requirements.txt --quiet

REM 启动应用
echo.
echo 启动应用...
echo 访问地址: http://127.0.0.1:8080
echo 按 Ctrl+C 停止服务器
echo.
py app.py

pause
