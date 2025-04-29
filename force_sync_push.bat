
@echo off
chcp 65001 >nul
cd /d %~dp0

set LOGFILE=git_sync_log.txt
echo [START] Git 强制同步开始 >> %LOGFILE%
echo 当前时间: %date% %time% >> %LOGFILE%

git rev-parse --is-inside-work-tree >nul 2>&1
IF ERRORLEVEL 1 (
    echo ❌ 当前目录不是 Git 仓库，请检查路径。 >> %LOGFILE%
    echo 当前目录不是 Git 仓库，请检查路径。
    goto END
)

echo ✅ 已检测到 Git 仓库，准备同步远程...
echo ✅ 正在暂存当前更改 (stash) ... >> %LOGFILE%
call git stash >> %LOGFILE% 2>&1

echo 🔁 正在执行 git pull --rebase ... >> %LOGFILE%
call git pull --rebase >> %LOGFILE% 2>&1

echo 🔄 正在恢复暂存更改 (stash pop) ... >> %LOGFILE%
call git stash pop >> %LOGFILE% 2>&1

echo ✅ 添加更改到暂存区...
call git add . >> %LOGFILE% 2>&1
call git commit -m "auto: force sync and push" >> %LOGFILE% 2>&1
call git push >> %LOGFILE% 2>&1

echo ✅ 同步完成，所有日志已记录至 %LOGFILE%
:END
pause
