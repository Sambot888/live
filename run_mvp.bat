@echo off
setlocal

set MODE=%1
if "%MODE%"=="" set MODE=free

echo [INFO] Running tests...
python -m unittest discover -s tests
if errorlevel 1 (
  echo [ERROR] Tests failed.
  exit /b 1
)

echo [INFO] Starting bot in mode: %MODE%
python -m mvp_bot.main --mode %MODE%
if errorlevel 1 (
  echo [ERROR] Runner failed.
  exit /b 1
)

echo [DONE]
endlocal
