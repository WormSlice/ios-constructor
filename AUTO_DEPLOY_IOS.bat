@echo off
chcp 65001 >nul
cd /d "%~dp0"
python "%~dp0ios_auto_deploy.py" %*
