@echo off
REM 久坐提醒 - 自動安裝腳本
REM 功能：建立虛擬環境並安裝依賴套件

echo.
echo ================================
echo 久坐提醒 - 安裝程式
echo ================================
echo.

REM 檢查 Python 是否已安裝
python --version >nul 2>&1
if errorlevel 1 (
    echo [錯誤] 未發現 Python！
    echo 請先下載安裝 Python 3.7+ (https://www.python.org)
    echo.
    pause
    exit /b 1
)

echo [✓] 偵測到 Python
echo.

REM 檢查虛擬環境是否存在
if exist "venv\" (
    echo [提示] 虛擬環境已存在，跳過建立步驟
    echo.
) else (
    echo [步驟 1/3] 正在建立虛擬環境...
    python -m venv venv
    if errorlevel 1 (
        echo [錯誤] 虛擬環境建立失敗！
        pause
        exit /b 1
    )
    echo [✓] 虛擬環境建立成功
    echo.
)

REM 啟動虛擬環境
echo [步驟 2/3] 啟動虛擬環境...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [錯誤] 虛擬環境啟動失敗！
    pause
    exit /b 1
)
echo [✓] 虛擬環境已啟動
echo.

REM 安裝依賴套件
echo [步驟 3/3] 安裝依賴套件...
pip install -r requirements.txt
if errorlevel 1 (
    echo [錯誤] 依賴套件安裝失敗！
    pause
    exit /b 1
)
echo [✓] 依賴套件安裝成功
echo.

echo ================================
echo [✓] 安裝完成！
echo ================================
echo.
echo 現在你可以執行下列命令啟動程式：
echo   sit-too-long.bat
echo.
pause