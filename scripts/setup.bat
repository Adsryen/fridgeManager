@echo off
chcp 65001 >nul
echo ========================================
echo   冰箱里面还有啥 - 环境配置
echo ========================================
echo.

REM 创建虚拟环境
if not exist venv (
    echo [1/3] 创建虚拟环境...
    py -m venv venv
    if errorlevel 1 (
        echo 错误: 创建虚拟环境失败
        echo 请确保已安装 Python 3.12+
        pause
        exit /b 1
    )
    echo ✓ 虚拟环境创建成功
) else (
    echo ✓ 虚拟环境已存在
)

REM 激活虚拟环境
echo.
echo [2/3] 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装依赖
echo.
echo [3/3] 安装依赖包...
py -m pip install -r requirements.txt
if errorlevel 1 (
    echo 错误: 依赖安装失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo   配置完成！
echo ========================================
echo.
echo 运行 scripts\start.bat 启动应用
echo 或手动运行: py run.py
echo.
pause
