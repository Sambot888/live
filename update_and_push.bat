@echo off
REM 切换到脚本所在目录
cd /d %~dp0

echo 正在检查当前目录是否为 Git 仓库...
git rev-parse --is-inside-work-tree >nul 2>&1
IF ERRORLEVEL 1 (
    echo 当前目录不是 Git 仓库，请检查目录.
) ELSE (
    echo 检测到 Git 仓库，开始同步...
    call git pull --rebase
    call git add .
    call git commit -m "auto: sync and push"
    call git push
    echo 同步操作已完成.
)

pause


echo 推送成功！
pause
