@echo off
REM PDF邮件合并工具 - 部署验证脚本
REM 用于验证软件包是否正确部署

echo ================================================
echo   PDF邮件合并工具 - 部署验证
echo ================================================
echo.

set ERROR_COUNT=0
set WARNING_COUNT=0

REM 检查1：检查主程序文件
echo [检查1] 检查主程序文件...
if exist "PDF邮件合并工具.exe.bat" (
    echo   [OK] 启动脚本存在
) else (
    echo   [ERROR] 启动脚本不存在：PDF邮件合并工具.exe.bat
    set /a ERROR_COUNT+=1
)

REM 检查2：检查Python文件夹
echo [检查2] 检查Python环境...
if exist "Python\python.exe" (
    echo   [OK] Python环境存在
    Python\python.exe --version
) else (
    echo   [WARNING] 未找到绑定的Python，将使用系统Python
    set /a WARNING_COUNT+=1
)

REM 检查3：检查应用程序文件夹
echo [检查3] 检查应用程序文件...
if exist "app\src\__init__.py" (
    echo   [OK] 应用程序文件存在
) else (
    echo   [ERROR] 应用程序文件缺失：app\src\__init__.py
    set /a ERROR_COUNT+=1
)

REM 检查4：检查测试文件
echo [检查4] 检查测试文件...
if exist "tests\test_data_loader.py" (
    echo   [OK] 测试文件存在
) else (
    echo   [WARNING] 测试文件缺失
    set /a WARNING_COUNT+=1
)

REM 检查5：检查文档
echo [检查5] 检查文档文件...
if exist "使用说明.txt" (
    echo   [OK] 使用说明存在
) else (
    echo   [WARNING] 使用说明缺失
    set /a WARNING_COUNT+=1
)

REM 检查6：创建输出目录
echo [检查6] 检查输出目录...
if exist "output" (
    echo   [OK] 输出目录存在
) else (
    echo   [INFO] 创建输出目录...
    mkdir output 2>nul
    if exist "output" (
        echo   [OK] 输出目录创建成功
    ) else (
        echo   [ERROR] 无法创建输出目录
        set /a ERROR_COUNT+=1
    )
)

REM 检查7：检查依赖
echo [检查7] 检查Python依赖...
python -c "import pypdf, pandas, jinja2, chardet, openpyxl" 2>nul
if errorlevel 1 (
    echo   [WARNING] 缺少依赖库，正在检查...
    python -m pip list | findstr /C:"pypdf" /C:"pandas" /C:"jinja2"
    if errorlevel 1 (
        echo   [ERROR] 依赖未安装
        set /a ERROR_COUNT+=1
    ) else (
        echo   [OK] 依赖已安装
    )
) else (
    echo   [OK] 所有依赖已就绪
)

REM 检查8：验证Python版本
echo [检查8] 检查Python版本...
python --version >nul 2>&1
if errorlevel 1 (
    echo   [ERROR] Python未安装或未配置PATH
    set /a ERROR_COUNT+=1
) else (
    for /f "delims=" %%i in ('python --version 2^>^&1') do set PYTHON_VER=%%i
    echo   [OK] %PYTHON_VER%
)

echo.
echo ================================================
echo   验证结果汇总
echo ================================================
echo.

if %ERROR_COUNT% gtr 0 (
    echo   [RESULT] 发现 %ERROR_COUNT% 个错误，%WARNING_COUNT% 个警告
    echo.
    echo   请修复上述错误后重新运行
) else if %WARNING_COUNT% gtr 0 (
    echo   [RESULT] 发现 %WARNING_COUNT% 个警告，无错误
    echo.
    echo   软件包可以正常运行，但建议解决警告
) else (
    echo   [RESULT] 所有检查通过！✓
    echo.
    echo   软件包已正确部署，可以正常使用
)

echo.
echo ================================================
echo   下一步操作
echo ================================================
echo.
echo   1. 双击 "PDF邮件合并工具.exe.bat" 启动程序
echo   2. 选择PDF模板和数据文件
echo   3. 点击"开始生成"处理数据
echo   4. 在output文件夹中查看结果
echo.
echo   如需查看详细说明，请阅读"使用说明.txt"
echo.
echo ================================================
echo.

pause