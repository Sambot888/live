@echo off
:: fix_and_push.bat - 自动解决 Git push 被拒绝的问题

:: 检查是否在 Git 仓库目录
git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 (
    echo 当前目录不是 Git 仓库，请进入正确的 Git 项目目录后再运行脚本。
    pause
    exit /b 1
)

echo 正在拉取远程仓库...
git pull --rebase
if errorlevel 1 (
    echo 拉取远程仓库时出错，请检查网络或远程仓库状态。
    pause
    exit /b 1
)

echo 正在添加更改到暂存区...
git add .
if errorlevel 1 (
    echo 添加更改时发生错误。
    pause
    exit /b 1
)

echo 正在提交更改...
git commit -m "auto: sync and push"
if errorlevel 1 (
    echo 没有需要提交的更改或提交失败。
    REM 如果没有更改，也继续尝试推送
)

echo 正在推送更改到远程仓库...
git push
if errorlevel 1 (
    echo 推送失败，请检查远程仓库地址和网络连接。
    pause
    exit /b 1
)

echo 推送成功！
pause
