@echo off
chcp 65001 >nul
cd /d %~dp0

set LOGFILE=git_sync_log.txt
echo [START] Git 自动同步开始 >> %LOGFILE%
echo 当前时间: %date% %time% >> %LOGFILE%

git rev-parse --is-inside-work-tree >nul 2>&1
IF ERRORLEVEL 1 (
    echo ❌ 当前目录不是 Git 仓库，请检查路径。 >> %LOGFILE%
    echo 当前目录不是 Git 仓库，请检查路径。
    goto END
)

echo ✅ 已检测到 Git 仓库，开始同步操作...
echo ✅ 已检测到 Git 仓库，开始同步操作... >> %LOGFILE%

call git pull --rebase >> %LOGFILE% 2>&1
call git add . >> %LOGFILE% 2>&1
call git commit -m "auto: sync and push" >> %LOGFILE% 2>&1
call git push >> %LOGFILE% 2>&1

echo ✅ Git 同步操作已完成。 >> %LOGFILE%
echo ✅ Git 同步操作已完成。

:END
echo 所有输出记录在 %LOGFILE%
pause
