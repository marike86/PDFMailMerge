@echo off
REM PDF邮件合并工具 - Windows交互式启动器
REM 使用交互式对话引导用户完成配置
REM 无需记忆复杂的命令行参数

setlocal enabledelayedexpansion

REM 设置颜色
set "ESC=[92m"    REM 绿色
set "ERR=[91m"    REM 红色
set "WARN=[93m"   REM 黄色
set "INFO=[96m"   REM 青色
set "BOLD=[1m"     REM 粗体
set "RESET=[0m"   REM 重置

:start
REM 清屏
cls

REM 显示标题
echo.
echo %ESC%%BOLD%═══════════════════════════════════════════════════════════════════%RESET%
echo %ESC%%BOLD%                                                                      %RESET%
echo %ESC%%BOLD%              PDF邮件合并工具 - 交互式操作界面                         %RESET%
echo %ESC%%BOLD%              PDF Mail Merge Tool - Interactive Mode                    %RESET%
echo %ESC%%BOLD%                                                                      %RESET%
echo %ESC%%BOLD%═══════════════════════════════════════════════════════════════════%RESET%
echo.

echo %INFO%欢迎使用PDF邮件合并工具！%RESET%
echo 本工具将引导您完成所有配置，无需记忆复杂的命令行参数。
echo.
echo 操作说明:
echo   - 输入信息后按Enter确认
echo   - 输入 N 取消当前步骤
echo   - 输入 Q 退出程序
echo   - 支持拖拽文件到终端
echo   - 路径两端的引号会自动移除
echo.

REM 检查Python环境
echo %INFO%检查运行环境...%RESET%

REM 尝试多种Python路径
set PYTHON_FOUND=0

REM 1. 优先检查虚拟环境
if exist "venv\Scripts\python.exe" (
    set PYTHON=venv\Scripts\python.exe
    set PYTHON_FOUND=1
    echo   [找到] 虚拟环境Python
)

REM 2. 检查Python文件夹（便携版）
if "!PYTHON_FOUND!"=="0" (
    if exist "Python\python.exe" (
        set PYTHON=Python\python.exe
        set PYTHON_FOUND=1
        echo   [找到] 便携版Python
    )
)

REM 3. 检查系统Python
if "!PYTHON_FOUND!"=="0" (
    where python >nul 2>&1
    if !errorlevel! equ 0 (
        set PYTHON=python
        set PYTHON_FOUND=1
        echo   [找到] 系统Python
    )
)

if "!PYTHON_FOUND!"=="0" (
    echo.
    echo %ERR%错误: 未找到Python环境！%RESET%
    echo.
    echo 请确保已安装Python 3.8或更高版本
    echo 下载地址: https://www.python.org/downloads/
    echo.
    echo 或者使用便携版本（包含Python环境）
    echo.
    pause
    exit /b 1
)

REM 显示Python版本
echo.
for /f "delims=" %%i in ('!PYTHON! --version 2^>^&1') do echo   %%i

REM 检查依赖
echo.
echo %INFO%检查依赖库...%RESET%

!PYTHON! -c "import pypdf, pandas, jinja2, chardet, openpyxl" 2>nul
if errorlevel 1 (
    echo   %WARN%缺少依赖，正在安装...%RESET%
    !PYTHON! -m pip install --quiet pypdf pandas jinja2 chardet openpyxl PyMuPDF
    if errorlevel 1 (
        echo.
        echo %ERR%错误: 依赖安装失败！%RESET%
        echo 请检查网络连接后重试
        echo.
        pause
        exit /b 1
    )
    echo   %ESC%依赖安装完成%RESET%
) else (
    echo   %ESC%所有依赖已就绪%RESET%
)

echo.

REM 显示主菜单
:menu
cls
call :print_banner

echo 主菜单:
echo.
echo   1. %ESC%[推荐]%RESET% 交互式对话 - 引导式操作（新手推荐）
echo   2. 命令行模式 - 高级用户使用参数
echo   3. 验证环境 - 检查系统配置
echo   4. 运行测试 - 测试核心功能
echo   5. 查看帮助 - 使用说明和文档
echo   0. 退出程序
echo.
echo %BOLD%═══════════════════════════════════════════════════════════════════%RESET%
echo.

set /p choice="请选择操作 (0-5): "

if "!choice!"=="1" goto interactive_mode
if "!choice!"=="2" goto cli_mode
if "!choice!"=="3" goto validate_env
if "!choice!"=="4" goto run_tests
if "!choice!"=="5" goto show_help
if "!choice!"=="0" goto end

echo.
echo %WARN%无效选项，请重新选择%RESET%
timeout /t 2 >nul
goto menu

:interactive_mode
cls
call :print_banner

echo %ESC%%BOLD%交互式对话模式%RESET%
echo 此模式将引导您逐步完成所有配置，无需记忆命令行参数。
echo.

REM 启动交互式CLI
!PYTHON! -m src.interactive_cli --interactive

if errorlevel 1 (
    echo.
    echo %ERR%交互式界面运行出错%RESET%
) else (
    echo.
    echo %ESC%操作完成！%RESET%
)

echo.
pause
goto menu

:cli_mode
cls
call :print_banner

echo %ESC%%BOLD%命令行模式%RESET%
echo.
echo 请输入命令行参数，或直接按Enter使用默认参数
echo 格式示例:
echo   --template template.pdf --data data.csv --output ./output
echo.
echo 或使用简短格式:
echo   -t template.pdf -d data.csv -o ./output
echo.

set /p args="参数 (直接回车显示帮助): "

if "!args!"=="" (
    !PYTHON! -m src.cli --help
    echo.
    pause
    goto cli_mode
)

echo.
echo 正在执行: !args!
echo.

!PYTHON! -m src.cli !args!

if errorlevel 1 (
    echo.
    echo %WARN%命令执行完成，但有错误发生%RESET%
) else (
    echo.
    echo %ESC%命令执行成功！%RESET%
)

echo.
pause
goto menu

:validate_env
cls
call :print_banner

echo %ESC%%BOLD%环境验证%RESET%
echo.

REM 检查Python版本
echo [%INFO%1/6%RESET%] 检查Python版本...
!PYTHON! --version

REM 检查pip
echo.
echo [%INFO%2/6%RESET%] 检查pip...
!PYTHON! -m pip --version

REM 检查依赖
echo.
echo [%INFO%3/6%RESET%] 检查依赖库...
!PYTHON! -c "import pypdf; print('  pypdf:', pypdf.__version__)" 2>nul
!PYTHON! -c "import pandas; print('  pandas:', pandas.__version__)" 2>nul
!PYTHON! -c "import jinja2; print('  Jinja2:', jinja2.__version__)" 2>nul
!PYTHON! -c "import chardet; print('  chardet:', chardet.__version__)" 2>nul
!PYTHON! -c "import openpyxl; print('  openpyxl:', openpyxl.__version__)" 2>nul

REM 检查源文件
echo.
echo [%INFO%4/6%RESET%] 检查源代码文件...
if exist "src\__init__.py" (
    echo   %ESC%[OK]%RESET% 源代码目录完整
) else (
    echo   %ERR%[ERROR]%RESET% 源代码目录缺失
)

REM 检查示例文件
echo.
echo [%INFO%5/6%RESET%] 检查示例文件...
if exist "examples\sample_data.csv" (
    echo   %ESC%[OK]%RESET% 示例数据文件存在
) else (
    echo   %WARN%[WARNING]%RESET% 示例数据文件缺失
)

REM 检查输出目录
echo.
echo [%INFO%6/6%RESET%] 检查输出目录...
if not exist "output" mkdir output 2>nul
if exist "output" (
    echo   %ESC%[OK]%RESET% 输出目录存在
) else (
    echo   %WARN%[WARNING]%RESET% 无法创建输出目录
)

echo.
echo %ESC%═══════════════════════════════════════════════════════════════════%RESET%
echo 环境验证完成！
echo %ESC%═══════════════════════════════════════════════════════════════════%RESET%
echo.

pause
goto menu

:run_tests
cls
call :print_banner

echo %ESC%%BOLD%运行测试%RESET%
echo.

REM 检查测试文件
if exist "tests\test_data_loader.py" (
    echo [%INFO%1/3%RESET%] 测试数据加载模块...
    !PYTHON! tests/test_data_loader.py
) else (
    echo %WARN%数据加载测试文件不存在%RESET%
)

if exist "tests\test_pdf_processor.py" (
    echo.
    echo [%INFO%2/3%RESET%] 测试PDF处理模块...
    !PYTHON! tests/test_pdf_processor.py
) else (
    echo %WARN%PDF处理测试文件不存在%RESET%
)

if exist "tests\test_template_engine.py" (
    echo.
    echo [%INFO%3/3%RESET%] 测试模板引擎模块...
    !PYTHON! tests/test_template_engine.py
) else (
    echo %WARN%模板引擎测试文件不存在%RESET%
)

echo.
echo %ESC%═══════════════════════════════════════════════════════════════════%RESET%
echo 测试完成！
echo %ESC%═══════════════════════════════════════════════════════════════════%RESET%
echo.

pause
goto menu

:show_help
cls
call :print_banner

echo %ESC%%BOLD%帮助信息%RESET%
echo.

echo 可用文档:
echo.
echo   1. 使用说明 (README.md)
echo   2. 快速开始 (docs\QUICK_START.md)
echo   3. 命令参考 (docs\COMMAND_REFERENCE.md)
echo   4. 故障排除 (docs\TROUBLESHOOTING.md)
echo   5. 用户指南 (docs\USER_GUIDE_CN.md)
echo.

set /p doc_choice="请选择 (1-5): "

if "!doc_choice!"=="1" (
    if exist "README.md" (
        type README.md
    ) else (
        echo %ERR%文件不存在%RESET%
    )
)
if "!doc_choice!"=="2" (
    if exist "docs\QUICK_START.md" (
        type docs\QUICK_START.md
    ) else (
        echo %ERR%文件不存在%RESET%
    )
)
if "!doc_choice!"=="3" (
    if exist "docs\COMMAND_REFERENCE.md" (
        type docs\COMMAND_REFERENCE.md
    ) else (
        echo %ERR%文件不存在%RESET%
    )
)
if "!doc_choice!"=="4" (
    if exist "docs\TROUBLESHOOTING.md" (
        type docs\TROUBLESHOOTING.md
    ) else (
        echo %ERR%文件不存在%RESET%
    )
)
if "!doc_choice!"=="5" (
    if exist "docs\USER_GUIDE_CN.md" (
        type docs\USER_GUIDE_CN.md
    ) else (
        echo %ERR%文件不存在%RESET%
    )
)

echo.
pause
goto menu

:print_banner
echo.
echo %ESC%%BOLD%═══════════════════════════════════════════════════════════════════%RESET%
echo %ESC%%BOLD%              PDF邮件合并工具 - 交互式操作界面                         %RESET%
echo %ESC%%BOLD%═══════════════════════════════════════════════════════════════════%RESET%
echo.
exit /b

:end
cls
echo.
echo %ESC%═══════════════════════════════════════════════════════════════════%RESET%
echo.
echo    感谢使用PDF邮件合并工具！
echo.
echo    如有其他问题，请查看帮助文档或提交Issue
echo.
echo %ESC%═══════════════════════════════════════════════════════════════════%RESET%
echo.
exit /b 0