@echo off
REM PDF邮件合并工具 - Windows启动脚本
REM Portable Version v1.0.0

REM 设置脚本目录
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM 检查Python环境
echo ================================================
echo   PDF邮件合并工具 - 开箱即用版 v1.0.0
echo ================================================
echo.

REM 检查Python是否可用
if exist "Python\python.exe" (
    set PYTHON=Python\python.exe
    echo [OK] 找到绑定的Python环境
) else (
    where python >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] 未找到Python环境！
        echo.
        echo 请确保已正确解压软件包，或安装Python 3.8+
        echo 下载地址：https://www.python.org/downloads/
        echo.
        pause
        exit /b 1
    ) else (
        set PYTHON=python
        echo [OK] 使用系统Python环境
    )
)

REM 显示Python版本
echo.
echo 正在检查Python版本...
%PYTHON% --version
echo.

REM 检查依赖
echo 正在检查依赖库...
%PYTHON% -c "import pypdf, pandas, jinja2, chardet, openpyxl" 2>nul
if errorlevel 1 (
    echo [WARNING] 缺少依赖库，正在安装...
    %PYTHON% -m pip install --quiet pypdf pandas jinja2 chardet openpyxl PyMuPDF
    if errorlevel 1 (
        echo [ERROR] 依赖安装失败！
        echo 请检查网络连接后重试
        pause
        exit /b 1
    )
    echo [OK] 依赖安装完成
) else (
    echo [OK] 所有依赖已就绪
)

REM 显示主菜单
:menu
cls
echo ================================================
echo   PDF邮件合并工具 - 主菜单
echo ================================================
echo.
echo  1. 图形界面模式（推荐给初学者）
echo  2. 命令行模式（适合高级用户）
echo  3. 查看帮助文档
echo  4. 运行测试
echo  5. 检查更新
echo  0. 退出
echo.
echo ================================================
set /p choice=请输入选项 (0-5):

if "%choice%"=="1" goto gui_mode
if "%choice%"=="2" goto cli_mode
if "%choice%"=="3" goto help_doc
if "%choice%"=="4" goto run_tests
if "%choice%"=="5" goto check_update
if "%choice%"=="0" goto end

echo 无效选项，请重新选择
timeout /t 2 >nul
goto menu

:gui_mode
cls
echo ================================================
echo   图形界面模式
echo ================================================
echo.
echo 正在启动图形界面...
echo.
echo [提示] 如果没有图形界面，将启动命令行模式
echo.
REM 启动GUI（如果有）
%PYTHON% -m app.src.gui 2>nul
if errorlevel 1 (
    echo [INFO] 图形界面未实现，将启动命令行模式
    echo.
    goto cli_mode
)
pause
goto menu

:cli_mode
cls
echo ================================================
echo   命令行模式
echo ================================================
echo.
echo 请输入命令行参数，或按Enter使用默认参数：
echo 格式：--template 模板.pdf --data 数据.csv --output ./output
echo.
set /p args=参数:
if not defined args (
    set args=--template template.pdf --data data.csv --output ./output
)
echo.
echo 正在执行：%args%
echo.
%PYTHON% -m app.src.cli %args%
echo.
pause
goto menu

:help_doc
cls
echo ================================================
echo   帮助文档
echo ================================================
echo.
echo 可用文档：
echo  1. 使用说明 (使用说明.txt)
echo  2. 快速开始 (docs/QUICK_START.md)
echo  3. 命令参考 (docs/COMMAND_REFERENCE.md)
echo  4. 故障排除 (docs/TROUBLESHOOTING.md)
echo  5. 用户指南 (docs/USER_GUIDE_CN.md)
echo.
set /p doc_choice=请选择 (1-5):

if "%doc_choice%"=="1" start "" "使用说明.txt"
if "%doc_choice%"=="2" start "" "docs\QUICK_START.md"
if "%doc_choice%"=="3" start "" "docs\COMMAND_REFERENCE.md"
if "%doc_choice%"=="4" start "" "docs\TROUBLESHOOTING.md"
if "%doc_choice%"=="5" start "" "docs\USER_GUIDE_CN.md"

goto menu

:run_tests
cls
echo ================================================
echo   运行测试
echo ================================================
echo.
echo 正在运行测试套件...
echo.
%PYTHON% tests/test_data_loader.py
%PYTHON% tests/test_pdf_processor.py
%PYTHON% tests/test_template_engine.py
echo.
pause
goto menu

:check_update
cls
echo ================================================
echo   检查更新
echo ================================================
echo.
echo 当前版本：v1.0.0
echo 发布日期：2026-05-18
echo.
echo [INFO] 这是一个开源项目，如需更新请访问：
echo   https://github.com/yourusername/pdf-mail-merge
echo.
pause
goto menu

:end
cls
echo ================================================
echo   感谢使用 PDF邮件合并工具！
echo ================================================
echo.
echo 按任意键退出...
pause >nul
exit /b 0