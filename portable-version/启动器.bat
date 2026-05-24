@echo off
REM PDF邮件合并工具 - Windows优化版启动器
REM 专为Windows系统优化，支持中文界面和交互式操作
REM
REM 功能特点:
REM   - 自动检测Python环境
REM   - 交互式引导操作
REM   - 中文界面支持
REM   - 路径自动处理（去除引号、空格）
REM   - 错误处理和恢复

setlocal enabledelayedexpansion

REM ================================================
REM 颜色定义 (Windows CMD)
REM ================================================
set "C_RESET="
set "C_BOLD="
set "C_RED=[91m"
set "C_GREEN=[92m"
set "C_YELLOW=[93m"
set "C_BLUE=[94m"
set "C_CYAN=[96m"
set "C_WHITE=[97m"

REM ================================================
REM 初始化
REM ================================================
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

set "PYTHON="
set "PYTHON_FOUND=0"

REM ================================================
REM 函数定义
REM =============================================

:print_banner
echo.
echo %C_CYAN%%C_BOLD%╔══════════════════════════════════════════════════════════════╗%C_RESET%
echo %C_CYAN%%C_BOLD%║                                                              ║%C_RESET%
echo %C_CYAN%%C_BOLD%║           PDF邮件合并工具 - Windows优化版                      ║%C_RESET%
echo %C_CYAN%%C_BOLD%║           PDF Mail Merge Tool - Windows Optimized             ║%C_RESET%
echo %C_CYAN%%C_BOLD%║                                                              ║%C_RESET%
echo %C_CYAN%%C_BOLD%╚══════════════════════════════════════════════════════════════╝%C_RESET%
echo.
exit /b

:check_python
REM 检查Python环境
set "PYTHON_FOUND=0"

REM 1. 虚拟环境
if exist "venv\Scripts\python.exe" (
    set "PYTHON=venv\Scripts\python.exe"
    set "PYTHON_FOUND=1"
    echo %C_GREEN%  [OK]%C_RESET% 虚拟环境Python
)

REM 2. 便携Python
if "!PYTHON_FOUND!"=="0" (
    if exist "Python\python.exe" (
        set "PYTHON=Python\python.exe"
        set "PYTHON_FOUND=1"
        echo %C_GREEN%  [OK]%C_RESET% 便携版Python
    )
)

REM 3. 系统Python
if "!PYTHON_FOUND!"=="0" (
    where python >nul 2>&1
    if !errorlevel! equ 0 (
        set "PYTHON=python"
        set "PYTHON_FOUND=1"
        echo %C_GREEN%  [OK]%C_RESET% 系统Python
    )
)

REM 4. Python3
if "!PYTHON_FOUND!"=="0" (
    where python3 >nul 2>&1
    if !errorlevel! equ 0 (
        set "PYTHON=python3"
        set "PYTHON_FOUND=1"
        echo %C_GREEN%  [OK]%C_RESET% 系统Python3
    )
)

if "!PYTHON_FOUND!"=="0" (
    echo %C_RED%  [ERROR]%C_RESET% 未找到Python
    exit /b 1
)

REM 显示Python版本
!PYTHON! --version 2>&1 | findstr /V "Python" >nul
for /f "delims=" %%i in ('!PYTHON! --version 2^>^&1') do echo %C_CYAN%  版本:%%i%C_RESET%

exit /b 0

:check_dependencies
REM 检查Python依赖
!PYTHON! -c "import pypdf, pandas, jinja2, chardet, openpyxl" 2>nul
if errorlevel 1 (
    echo %C_YELLOW%  [WARNING]%C_RESET% 缺少依赖，正在安装...
    !PYTHON! -m pip install --quiet --upgrade pip
    !PYTHON! -m pip install --quiet pypdf pandas jinja2 chardet openpyxl PyMuPDF
    if errorlevel 1 (
        echo %C_RED%  [ERROR]%C_RESET% 依赖安装失败
        exit /b 1
    )
    echo %C_GREEN%  [OK]%C_RESET% 依赖安装完成
) else (
    echo %C_GREEN%  [OK]%C_RESET% 所有依赖已就绪
)
exit /b 0

:get_template
REM 获取模板文件路径
echo.
echo %C_CYAN%请输入PDF模板文件路径:%C_RESET%
echo 示例:
echo   - 相对路径: template.pdf, ..\docs\template.pdf
echo   - 绝对路径: C:\Users\Admin\template.pdf
echo   - 拖拽路径: "C:\Users\Admin\template.pdf" ^(引号会自动移除^)
echo.

set /p TEMPLATE_PATH="路径: "

REM 移除路径两端的引号
set "TEMPLATE_PATH=!TEMPLATE_PATH:"=!"
set "TEMPLATE_PATH=!TEMPLATE_PATH:"=!"

REM 去除首尾空格
for /f "tokens=*" %%i in ("!TEMPLATE_PATH!") do set "TEMPLATE_PATH=%%i"

REM 验证文件存在
if not exist "!TEMPLATE_PATH!" (
    echo %C_RED%  [ERROR]%C_RESET% 文件不存在: !TEMPLATE_PATH!
    exit /b 1
)

REM 验证PDF格式
echo !TEMPLATE_PATH! | findstr /I "\.pdf$" >nul
if errorlevel 1 (
    echo %C_RED%  [ERROR]%C_RESET% 文件必须是PDF格式
    exit /b 1
)

echo %C_GREEN%  [OK]%C_RESET% 已选择: !TEMPLATE_PATH!
exit /b 0

:get_data_file
REM 获取数据文件路径
echo.
echo %C_CYAN%请输入数据文件路径:%C_RESET%
echo 支持格式: CSV (.csv), Excel (.xlsx/.xls), JSON (.json)
echo 示例:
echo   - data.csv
echo   - C:\Users\Admin\data.xlsx
echo   - "C:\Users\Admin\data.csv"
echo.

set /p DATA_PATH="路径: "

REM 移除路径两端的引号
set "DATA_PATH=!DATA_PATH:"=!"
set "DATA_PATH=!DATA_PATH:"=!"

REM 去除首尾空格
for /f "tokens=*" %%i in ("!DATA_PATH!") do set "DATA_PATH=%%i"

REM 验证文件存在
if not exist "!DATA_PATH!" (
    echo %C_RED%  [ERROR]%C_RESET% 文件不存在: !DATA_PATH!
    exit /b 1
)

REM 验证格式
echo !DATA_PATH! | findstr /I /R "\.csv$ \.xlsx$ \.xls$ \.json$" >nul
if errorlevel 1 (
    echo %C_RED%  [ERROR]%C_RESET% 不支持的格式，请使用 .csv, .xlsx, .xls, 或 .json
    exit /b 1
)

echo %C_GREEN%  [OK]%C_RESET% 已选择: !DATA_PATH!
exit /b 0

:get_output_dir
REM 获取输出目录
echo.
echo %C_CYAN%请输入输出目录路径:%C_RESET%
echo 目录不存在时会自动创建
echo 示例:
echo   - ./output
echo   - C:\Users\Admin\output
echo   - "C:\Program Files\output"
echo.

set /p OUTPUT_DIR="路径 (直接回车使用 ./output): "

REM 移除引号
set "OUTPUT_DIR=!OUTPUT_DIR:"=!"
set "OUTPUT_DIR=!OUTPUT_DIR:"=!"

REM 去除首尾空格
for /f "tokens=*" %%i in ("!OUTPUT_DIR!") do set "OUTPUT_DIR=%%i"

REM 使用默认目录
if "!OUTPUT_DIR!"=="" (
    set "OUTPUT_DIR=./output"
)

echo %C_GREEN%  [OK]%C_RESET% 输出目录: !OUTPUT_DIR!
exit /b 0

:select_mode
REM 选择处理模式
echo.
echo %C_CYAN%请选择处理模式:%C_RESET%
echo.
echo   1. 表单模式 - PDF包含可填充表单域
echo   2. 文本模式 - PDF包含 {{placeholder}} 占位符
echo   3. 自动检测 - 系统自动识别PDF类型
echo.

set /p MODE_CHOICE="请选择 (1-3，默认3): "

if "!MODE_CHOICE!"=="" set "MODE_CHOICE=3"
if "!MODE_CHOICE!"=="1" set "MODE=form"
if "!MODE_CHOICE!"=="2" set "MODE=text"
if "!MODE_CHOICE!"=="3" set "MODE=auto"

echo %C_GREEN%  [OK]%C_RESET% 处理模式: !MODE!
exit /b 0

:get_naming
REM 获取命名规则
echo.
echo %C_CYAN%请输入输出文件命名规则:%C_RESET%
echo.
echo 可用占位符:
echo   {row}     - 行号 (1, 2, 3...)
echo   {name}    - 数据列名 (如 name, email)
echo   {timestamp} - 时间戳
echo.
echo 示例:
echo   - document_{row}
echo   - {name}_{row}
echo   - {company}_{name}
echo.

set /p NAMING="命名规则 (直接回车使用 document_{row}): "

REM 去除空格
for /f "tokens=*" %%i in ("!NAMING!") do set "NAMING=%%i"

if "!NAMING!"=="" set "NAMING=document_{row}"

echo %C_GREEN%  [OK]%C_RESET% 命名规则: !NAMING!
exit /b 0

:get_options
REM 获取其他选项
echo.
echo %C_CYAN%其他选项:%C_RESET%
echo.

set /p ZIP_OPTION="是否生成ZIP压缩包? (Y/N，默认N): "
if /i "!ZIP_OPTION!"=="Y" (
    set "ZIP_ENABLED=1"
    echo %C_GREEN%  [OK]%C_RESET% 将生成ZIP压缩包
) else (
    set "ZIP_ENABLED=0"
    echo %C_INFO%  [INFO]%C_RESET% 不生成ZIP压缩包
)

set /p CLEAN_OPTION="是否清空输出目录? (Y/N，默认N): "
if /i "!CLEAN_OPTION!"=="Y" (
    set "CLEAN_OUTPUT=1"
    echo %C_YELLOW%  [WARNING]%C_RESET% 将清空输出目录
) else (
    set "CLEAN_OUTPUT=0"
    echo %C_INFO%  [INFO]%C_RESET% 保留输出目录中的现有文件
)

exit /b 0

:show_summary
REM 显示摘要
echo.
echo %C_CYAN%%C_BOLD%═══════════════════════════════════════════════════════════════%C_RESET%
echo %C_CYAN%%C_BOLD%                    配置摘要                                   %C_RESET%
echo %C_CYAN%%C_BOLD%═══════════════════════════════════════════════════════════════%C_RESET%
echo.
echo %C_WHITE%  1. PDF模板:     !TEMPLATE_PATH!%C_RESET%
echo %C_WHITE%  2. 数据文件:     !DATA_PATH!%C_RESET%
echo %C_WHITE%  3. 输出目录:     !OUTPUT_DIR!%C_RESET%
echo %C_WHITE%  4. 处理模式:     !MODE!%C_RESET%
echo %C_WHITE%  5. 命名规则:     !NAMING!%C_RESET%
echo %C_WHITE%  6. 生成ZIP:      !ZIP_ENABLED!%C_RESET%
echo %C_WHITE%  7. 清空输出:      !CLEAN_OUTPUT!%C_RESET%
echo.
echo %C_CYAN%%C_BOLD%═══════════════════════════════════════════════════════════════%C_RESET%
echo.
exit /b 0

:confirm
REM 确认执行
set /p CONFIRM="确认以上配置并开始处理? (Y/N): "
if /i "!CONFIRM!"=="Y" exit /b 0
if /i "!CONFIRM!"=="YES" exit /b 0
exit /b 1

:run_process
REM 执行处理
echo.
echo %C_CYAN%正在处理...%C_RESET%
echo.

REM 构建命令
set "CMD=!PYTHON! -m src.cli --template !TEMPLATE_PATH! --data !DATA_PATH! --output !OUTPUT_DIR! --mode !MODE! --name !NAMING!"

if "!ZIP_ENABLED!"=="1" set "CMD=!CMD! --zip"
if "!CLEAN_OUTPUT!"=="1" set "CMD=!CMD! --clean"

REM 执行命令
!CMD!

if errorlevel 1 (
    echo.
    echo %C_RED%  [ERROR]%C_RESET% 处理过程中出现错误
    exit /b 1
)

echo.
echo %C_GREEN%═══════════════════════════════════════════════════════════════%C_RESET%
echo %C_GREEN%                     处理完成!                                    %C_RESET%
echo %C_GREEN%═══════════════════════════════════════════════════════════════%C_RESET%
echo.
exit /b 0

:show_menu
REM 显示主菜单
echo.
echo %C_CYAN%主菜单:%C_RESET%
echo.
echo   1. %C_GREEN%[推荐]%C_RESET% 交互式操作 - 逐步引导配置
echo   2. 快速开始 - 使用默认设置处理
echo   3. 验证环境 - 检查系统配置
echo   4. 运行测试 - 测试核心功能
echo   5. 查看帮助 - 使用说明
echo   0. 退出程序
echo.
exit /b

:show_help
REM 显示帮助
echo.
echo %C_CYAN%%C_BOLD%═══════════════════════════════════════════════════════════════%C_RESET%
echo %C_CYAN%%C_BOLD%                           帮助信息                               %C_RESET%
echo %C_CYAN%%C_BOLD%═══════════════════════════════════════════════════════════════%C_RESET%
echo.
echo %C_WHITE%PDF邮件合并工具使用说明:%C_RESET%
echo.
echo %C_YELLOW%基本使用:%C_RESET%
echo   1. 选择PDF模板文件
echo   2. 选择数据源文件 (CSV/Excel/JSON)
echo   3. 指定输出目录
echo   4. 选择处理模式
echo   5. 开始处理
echo.
echo %C_YELLOW%处理模式:%C_RESET%
echo   表单模式:  适用于包含表单域的PDF
echo   文本模式:  适用于包含 {{placeholder}} 的PDF
echo   自动检测:  系统自动识别PDF类型
echo.
echo %C_YELLOW%支持的数据格式:%C_RESET%
echo   CSV:    .csv 文件，UTF-8编码
echo   Excel:  .xlsx, .xls 文件
echo   JSON:   .json 文件
echo.
echo %C_YELLOW%命名规则:%C_RESET%
echo   {row}       - 行号
echo   {name}      - 数据列名
echo   {timestamp} - 时间戳
echo.
echo 示例: document_{row}.pdf, {name}_{company}.pdf
echo.
pause
exit /b

:test_mode
REM 测试模式 - 使用示例文件
echo.
echo %C_CYAN%测试模式 - 使用示例文件验证功能%RESET%
echo.

if not exist "examples\sample_data.csv" (
    echo %C_YELLOW%  [WARNING]%C_RESET% 示例数据文件不存在
    echo   请创建: examples\sample_data.csv
    pause
    exit /b 1
)

REM 创建测试模板（如果不存在）
if not exist "template.pdf" (
    echo %C_YELLOW%  [INFO]%C_RESET% 请手动创建 template.pdf 文件
    echo   可以使用 examples\template.pdf 作为参考
    pause
    exit /b 1
)

echo %C_GREEN%  [OK]%C_RESET% 找到示例文件
echo.

REM 自动执行测试
set "CMD=!PYTHON! -m src.cli --template template.pdf --data examples\sample_data.csv --output ./test_output --mode auto --verbose"
echo 执行: !CMD!
echo.

!CMD!

if errorlevel 1 (
    echo.
    echo %C_YELLOW%  [WARNING]%C_RESET% 测试过程中出现错误
    echo   请检查模板文件和数据文件
) else (
    echo.
    echo %C_GREEN%  [OK]%C_RESET% 测试完成!
)

pause
exit /b 0

REM ================================================
REM 主程序
REM ================================================

:main
cls
call :print_banner

echo %C_YELLOW%欢迎使用PDF邮件合并工具！%C_RESET%
echo 本工具将帮助您批量生成个性化PDF文件。
echo.
echo %C_CYAN%检查运行环境...%C_RESET%

call :check_python
if errorlevel 1 (
    echo.
    echo %C_RED%错误: 未找到Python环境%RESET%
    echo.
    echo 请安装Python 3.8或更高版本:
    echo   https://www.python.org/downloads/
    echo.
    echo 或下载便携版本（包含Python环境）
    echo.
    pause
    exit /b 1
)

call :check_dependencies
if errorlevel 1 (
    echo.
    echo %C_RED%错误: 依赖检查失败%RESET%
    pause
    exit /b 1
)

echo.
call :show_menu

set /p CHOICE="请选择操作 (0-5): "

if "!CHOICE!"=="1" goto :interactive
if "!CHOICE!"=="2" goto :quick_start
if "!CHOICE!"=="3" goto :validate
if "!CHOICE!"=="4" goto :test
if "!CHOICE!"=="5" goto :help_display
if "!CHOICE!"=="0" goto :exit_program

echo.
echo %C_YELLOW%无效选项，请重新选择%RESET%
timeout /t 2 >nul
goto :main

:interactive
REM 交互式操作模式
cls
call :print_banner

echo %C_CYAN%%C_BOLD%交互式操作模式%RESET%
echo 此模式将引导您逐步完成所有配置。
echo.

call :get_template
if errorlevel 1 (
    echo.
    echo %C_YELLOW%按任意键返回主菜单...%C_RESET%
    pause >nul
    goto :main
)

call :get_data_file
if errorlevel 1 (
    echo.
    echo %C_YELLOW%按任意键返回主菜单...%C_RESET%
    pause >nul
    goto :main
)

call :get_output_dir
call :select_mode
call :get_naming
call :get_options
cls
call :print_banner
call :show_summary

call :confirm
if errorlevel 1 (
    echo.
    echo %C_YELLOW%已取消执行，返回主菜单%C_RESET%
    timeout /t 2 >nul
    goto :main
)

call :run_process

echo.
echo %C_GREEN%感谢使用PDF邮件合并工具！%C_RESET%
echo.

:exit_program
cls
echo.
echo %C_CYAN%═══════════════════════════════════════════════════════════════%C_RESET%
echo.
echo    感谢使用PDF邮件合并工具！
echo.
echo    如有其他问题，请查看帮助文档或提交Issue
echo.
echo %C_CYAN%═══════════════════════════════════════════════════════════════%C_RESET%
echo.
exit /b 0

:quick_start
REM 快速开始
cls
call :print_banner

echo %C_CYAN%%C_BOLD%快速开始模式%C_RESET%
echo 此模式将使用默认设置处理文件。
echo.

set /p QUICK_TEMPLATE="请输入PDF模板路径: "
set "QUICK_TEMPLATE=!QUICK_TEMPLATE:"=!"

set /p QUICK_DATA="请输入数据文件路径: "
set "QUICK_DATA=!QUICK_DATA:"=!"

call :get_output_dir

echo.
echo %C_CYAN%使用以下配置:%C_RESET%
echo   模板: !QUICK_TEMPLATE!
echo   数据: !QUICK_DATA!
echo   输出: !OUTPUT_DIR!
echo   模式: auto
echo.

set /p QUICK_CONFIRM="确认开始处理? (Y/N): "
if /i "!QUICK_CONFIRM!"=="Y" (
    set "MODE=auto"
    set "NAMING=document_{row}"
    set "ZIP_ENABLED=0"
    set "CLEAN_OUTPUT=0"
    call :run_process
)

goto :main

:validate
REM 验证环境
cls
call :print_banner

echo %C_CYAN%%C_BOLD%环境验证%RESET%
echo.

call :check_python
call :check_dependencies

echo.
echo %C_GREEN%═══════════════════════════════════════════════════════════════%C_RESET%
echo 环境验证完成！
echo %C_GREEN%═══════════════════════════════════════════════════════════════%C_RESET%
echo.

pause
goto :main

:test
REM 运行测试
call :test_mode
goto :main

:help_display
REM 显示帮助
call :show_help
goto :main

endlocal