@echo off
REM PDF邮件合并工具 - 打包脚本
REM 用于将项目打包为可分发的ZIP文件

echo ================================================
echo   PDF邮件合并工具 - 打包脚本
echo   Version: 1.0.0
echo ================================================
echo.

REM 设置变量
set VERSION=v1.0.0
set TIMESTAMP=%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%
set PROJECT_NAME=pdf-mail-merge
set OUTPUT_DIR=..\releases

REM 创建输出目录
echo [1/5] 创建输出目录...
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"
echo   完成
echo.

REM 清理旧文件
echo [2/5] 清理旧文件...
if exist "%OUTPUT_DIR%\%PROJECT_NAME%-script-%VERSION%.zip" del "%OUTPUT_DIR%\%PROJECT_NAME%-script-%VERSION%.zip"
if exist "%OUTPUT_DIR%\%PROJECT_NAME%-portable-%VERSION%.zip" del "%OUTPUT_DIR%\%PROJECT_NAME%-portable-%VERSION%.zip"
echo   完成
echo.

REM 打包脚本版本
echo [3/5] 打包脚本版本...
cd /d "%~dp0..\script-version"
echo   正在压缩文件...
powershell -Command "Compress-Archive -Path '*' -DestinationPath '%OUTPUT_DIR%\%PROJECT_NAME%-script-%VERSION%.zip' -Force"
if exist "%OUTPUT_DIR%\%PROJECT_NAME%-script-%VERSION%.zip" (
    echo   [OK] 脚本版本打包完成：%PROJECT_NAME%-script-%VERSION%.zip
) else (
    echo   [ERROR] 脚本版本打包失败！
)
echo.

REM 复制必要的文件到打包版本
echo [4/5] 准备打包版本文件...
cd /d "%~dp0"
if not exist "..\temp-portable" mkdir "..\temp-portable"

REM 复制应用程序
xcopy /E /Y /Q "..\src" "..\temp-portable\app\src\" 2>nul
xcopy /E /Y /Q "..\tests" "..\temp-portable\app\tests\" 2>nul
xcopy /E /Y /Q "..\examples" "..\temp-portable\app\examples\" 2>nul
xcopy /E /Y /Q "..\docs" "..\temp-portable\app\docs\" 2>nul

REM 复制配置文件
if not exist "..\temp-portable\config" mkdir "..\temp-portable\config"
echo { "default_output": "./output", "default_mode": "auto", "naming_pattern": "{row}", "zip_enabled": false, "verbose": false, "max_workers": 4 } > "..\temp-portable\config\default_settings.json"

REM 复制文档
copy /Y "使用说明.txt" "..\temp-portable\" 2>nul
copy /Y "README.txt" "..\temp-portable\" 2>nul
copy /Y "LICENSE.txt" "..\temp-portable\" 2>nul

REM 复制启动脚本
copy /Y "PDF邮件合并工具.exe.bat" "..\temp-portable\PDF邮件合并工具.exe" 2>nul
copy /Y "PDF邮件合并工具.sh" "..\temp-portable\" 2>nul
copy /Y "验证部署.bat" "..\temp-portable\" 2>nul

REM 创建output目录
if not exist "..\temp-portable\output" mkdir "..\temp-portable\output"

echo   完成
echo.

REM 打包打包版本
echo [5/5] 打包开箱即用版本...
cd /d "..\temp-portable"
echo   正在压缩文件...
powershell -Command "Compress-Archive -Path '*' -DestinationPath '%OUTPUT_DIR%\%PROJECT_NAME%-portable-%VERSION%.zip' -Force"
if exist "%OUTPUT_DIR%\%PROJECT_NAME%-portable-%VERSION%.zip" (
    echo   [OK] 打包版本完成：%PROJECT_NAME%-portable-%VERSION%.zip
) else (
    echo   [ERROR] 打包版本打包失败！
)
echo.

REM 清理临时文件
echo [完成] 清理临时文件...
rd /S /Q "..\temp-portable" 2>nul
echo.

REM 显示结果
echo ================================================
echo   打包完成！
echo ================================================
echo.
echo   输出文件：
echo   - 脚本版本：%OUTPUT_DIR%\%PROJECT_NAME%-script-%VERSION%.zip
echo   - 打包版本：%OUTPUT_DIR%\%PROJECT_NAME%-portable-%VERSION%.zip
echo.
echo   文件大小：
for %%F in ("%OUTPUT_DIR%\%PROJECT_NAME%-script-%VERSION%.zip") do echo   - 脚本版本：%%~zF 字节
for %%F in ("%OUTPUT_DIR%\%PROJECT_NAME%-portable-%VERSION%.zip") do echo   - 打包版本：%%~zF 字节
echo.
echo ================================================
echo.

pause