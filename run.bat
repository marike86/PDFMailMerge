@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

cd /d "%~dp0"

echo.
echo ================================================
echo   PDF邮件合并工具
echo   PDF Mail Merge Tool
echo ================================================
echo.

where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] 未找到Python！请先安装Python 3.8+
    echo   https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "delims=" %%i in ('python --version 2^>^&1') do echo [OK] %%i

python -c "import pypdf, pandas, jinja2, chardet, openpyxl, fitz" 2>nul
if errorlevel 1 (
    echo [INFO] 正在安装依赖...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] 依赖安装失败！
        pause
        exit /b 1
    )
)

echo.
echo 启动交互式界面...
echo.
python -m src.interactive_cli --interactive

pause
