@echo off
chcp 65001 >nul
title 正在打包程序...

echo 正在打包，请稍候...

:: 清理旧文件
if exist "build" rmdir /s /q "build" 2>nul
if exist "dist" rmdir /s /q "dist" 2>nul
if exist "*.spec" del /q "*.spec" 2>nul

:: 打包
pyinstaller --onefile --windowed --name="通用票据识别查看器" interactive_viewer.py >nul 2>&1

:: 复制到当前目录
copy /y "dist\通用票据识别查看器.exe" ".\" >nul

:: 清理临时文件
if exist "build" rmdir /s /q "build" 2>nul
if exist "dist" rmdir /s /q "dist" 2>nul
if exist "*.spec" del /q "*.spec" 2>nul

echo 打包完成！生成文件：通用票据识别查看器.exe
ping 127.0.0.1 -n 3 >nul
