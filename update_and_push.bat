@echo off
chcp 65001 >nul
cd /d %~dp0

echo 正在检查当前目录是否为 Git 仓库...
git rev-parse --is-inside-work-tree >nul 2>&1
IF ERRORLEVEL 1 (
    echo ❌ 当前目录不是 Git 仓库，请检查路径。
) ELSE (
    echo ✅ 已检测到 Git 仓库，开始同步操作...
    call git pull --rebase
    call git add .
    call git commit -m "auto: sync and push"
    call git push
    echo ✅ 已完成同步！
)

pause
