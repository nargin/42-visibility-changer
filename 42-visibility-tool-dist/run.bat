@echo off
echo 42 Visibility Tool
if "%GITHUB_TOKEN%"=="" (echo Error: Set GITHUB_TOKEN first & pause & exit /b 1)
python 42-visibility-tool.py
pause
