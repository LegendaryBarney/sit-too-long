@echo off
chcp 65001 > nul

REM 取得指令碼目錄
setlocal enabledelayedexpansion
set "SCRIPT_DIR=%~dp0"

REM 檢查虛擬環境是否存在
if not exist "%SCRIPT_DIR%venv" (
    echo [錯誤] 虛擬環境不存在！
    echo 請先執行 install.bat 安裝依賴套件
    echo.
    pause
    exit /b 1
)

REM 啟動虛擬環境
call "%SCRIPT_DIR%venv\Scripts\activate.bat"

REM 執行程式
echo ====================================
echo 久坐提醒 - 監測中
echo ====================================
echo.
python "%SCRIPT_DIR%sit-too-long.py"
pause