@echo off
chcp 65001 >nul
echo ================================================
echo           通用票据识别查看器 - 打包工具
echo ================================================
echo.

echo [1/5] 检查PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller未安装，正在安装...
    pip install pyinstaller
    if errorlevel 1 (
        echo 安装失败！请检查网络连接。
        pause
        exit /b 1
    )
)
echo PyInstaller已就绪
echo.

echo [2/5] 清理旧的打包文件...
if exist "build" (
    rmdir /s /q "build"
    echo 已删除 build 目录
)
if exist "dist" (
    rmdir /s /q "dist"
    echo 已删除 dist 目录
)
if exist "*.spec" (
    del /q "*.spec"
    echo 已删除 .spec 文件
)
echo 清理完成
echo.

echo [3/5] 开始打包程序...
pyinstaller --onefile --windowed --name="通用票据识别查看器" interactive_viewer.py
if errorlevel 1 (
    echo.
    echo 打包失败！请检查错误信息。
    pause
    exit /b 1
)
echo.

echo [4/5] 打包成功！
echo 正在复制文件到当前目录...
copy /y "dist\通用票据识别查看器.exe" ".\"
if errorlevel 1 (
    echo 复制文件失败！
    pause
    exit /b 1
)
echo.

echo [5/5] 清理临时文件...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del /q "*.spec"
echo.

echo ================================================
echo               打包完成！
echo ================================================
echo.
echo 生成的文件：
echo   - 通用票据识别查看器.exe (主程序)
echo.
echo 文件位置：%CD%\通用票据识别查看器.exe
echo.
echo 文件大小：
for %%A in ("通用票据识别查看器.exe") do echo   %%~zA 字节 (约 %%~zA:~0,-2% / 1024 MB)
echo.
echo ================================================
echo  按任意键退出...
pause >nul
