@echo off
REM 清理旧文件脚本
REM 删除与旧参数执行方法相关的文件

echo ================================================
echo   PDF邮件合并工具 - 清理旧文件
echo ================================================
echo.

set DELETE_COUNT=0
set SKIP_COUNT=0

REM 清理 __pycache__ 目录
echo [1/5] 清理Python缓存...
if exist "src\__pycache__" (
    rmdir /S /Q "src\__pycache__"
    echo   [OK] 已删除 src\__pycache__
    set /a DELETE_COUNT+=1
) else (
    echo   [SKIP] 无缓存文件
    set /a SKIP_COUNT+=1
)

if exist "tests\__pycache__" (
    rmdir /S /Q "tests\__pycache__"
    echo   [OK] 已删除 tests\__pycache__
    set /a DELETE_COUNT+=1
) else (
    echo   [SKIP] 无缓存文件
    set /a SKIP_COUNT+=1
)

REM 清理编译的.pyc文件
echo.
echo [2/5] 清理编译文件...
for /R "src" %%f in (*.pyc) do (
    del "%%f" 2>nul
    set /a DELETE_COUNT+=1
)

for /R "tests" %%f in (*.pyc) do (
    del "%%f" 2>nul
    set /a DELETE_COUNT+=1
)

REM 清理输出目录中的测试文件
echo.
echo [3/5] 清理输出目录...
if exist "output" (
    for %%f in (output\*.pdf) do (
        del "%%f" 2>nul
        set /a DELETE_COUNT+=1
    )
    
    for %%f in (output\*.zip) do (
        del "%%f" 2>nul
        set /a DELETE_COUNT+=1
    )
    
    echo   [OK] 已清理输出目录中的临时文件
    set /a DELETE_COUNT+=1
) else (
    echo   [SKIP] 输出目录不存在
    set /a SKIP_COUNT+=1
)

REM 清理测试产生的临时文件
echo.
echo [4/5] 清理测试临时文件...
if exist "test_output" (
    rmdir /S /Q "test_output"
    echo   [OK] 已删除 test_output
    set /a DELETE_COUNT+=1
) else (
    echo   [SKIP] 无测试目录
    set /a SKIP_COUNT+=1
)

REM 清理日志文件
echo.
echo [5/5] 清理日志文件...
if exist "*.log" (
    del *.log 2>nul
    echo   [OK] 已删除日志文件
    set /a DELETE_COUNT+=1
) else (
    echo   [SKIP] 无日志文件
    set /a SKIP_COUNT+=1
)

REM 显示结果
echo.
echo ================================================
echo   清理完成
echo ================================================
echo.
echo   删除文件: %DELETE_COUNT%
echo   跳过: %SKIP_COUNT%
echo.
echo   清理后的目录结构:
echo   - src/      (源代码)
echo   - tests/    (测试)
echo   - examples/ (示例)
echo   - docs/     (文档)
echo   - output/   (输出)
echo.
echo ================================================
echo.

pause