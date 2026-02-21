# Sit Too Long ⏰

久坐提醒程式 - 監測滑鼠移動，定時提醒使用者站起來活動

## 功能介紹

「久坐提醒」是一個簡單的桌面應用，旨在幫助長時間工作的使用者改善健康習慣。

### 主要功能
- 🖱️ **滑鼠移動監測**：自動監控滑鼠活動
- ⏱️ **自訂倒計時**：設定久坐時間和休息時間 
- 🔔 **多種提醒方式**：
  - 系統蜂鳴聲警報
  - 彈出提醒視窗
  - 每分鐘重複提醒（直到充分休息）
- 📊 **即時顯示**：終端顯示倒計時和累積休息時間

## 系統需求

- **作業系統**：Windows
- **Python 版本**：3.7+
- **依賴包**：見 `requirements.txt`

## 安裝步驟

### 方法 1：手動安裝

1. 克隆或下載本專案
   ```bash
   git clone https://github.com/LegendaryBarney/sit-too-long.git
   cd sit-too-long
   ```

2. 建立虛擬環境（推薦）
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. 安裝依賴所需套件
   ```bash
   pip install -r requirements.txt
   ```

### 方法 2：自動安裝（批次檔）

Windows 使用者可直接執行：
```bash
install.bat
```

## 使用方法

### 基本使用

執行程式：
```bash
python sit-too-long.py
```

或開啟批次檔：
```bash
sit-too-long.bat
```

### 使用流程

1. **啟動程式** - 執行上述命令
2. **設定參數** - 在設定視窗中輸入：
   - **久坐時間**：多少分鐘後提醒（預設：30分鐘）
   - **休息時間**：需要休息多長時間才可停止提醒（預設：1分鐘）
3. **開始監測** - 點擊「開始監測」按鈕
4. **輕鬆工作** - 程式會在背景監控滑鼠移動

### 提醒機制

- **正常流程**：
  1. 偵測到滑鼠移動 → 開始倒計時
  2. 倒計時完成 → 出現提醒視窗 + 蜂鳴聲
  3. 點擊「我知道了」確認
  4. 如果使用者沒有休息足夠時間 → 每分鐘重複提醒
  5. 活動滑鼠達到休息時間後 → 重設計時器

## 檔案說明

```
sit-too-long/
├── sit-too-long.py          # 主程式
├── requirements.txt          # Python 依賴列表
├── install.bat              # Windows 安裝批次檔
├── run_hidden.vbs           # 隱藏視窗執行腳本
├── sit-too-long.bat         # 執行批次檔
├── README.md                # 專案文檔（本檔案）
└── LICENSE                  # MIT 許可證
```

## 配置說明

程式啟動時會彈出設定視窗，允許自訂以下參數：

| 參數 | 預設值 | 說明 |
|------|--------|------|
| 久坐時間 | 30 分鐘 | 多長時間後發出第一次提醒 |
| 休息時間 | 1 分鐘 | 需要休息多長時間以重設計時器 |

## 常見問題

### Q: 提醒視窗沒有出現？
A: 檢查是否已正確安裝依賴套件。執行 `pip install -r requirements.txt`

### Q: 能在 Mac/Linux 上使用嗎？
A: 目前僅支援 Windows（使用了 `winsound` 模組）

### Q: 能改成不同的提醒聲音嗎？
A: 可以修改 `show_alert()` 方法中的 `BEEP_FREQUENCY` 和 `BEEP_DURATION` 常數

## 開發資訊

### 技術棧
- **GUI**：Tkinter
- **系統監控**：PyAutoGUI
- **並發處理**：Threading

### 核心模組
- `SettingsDialog`：設定對話框
- `ReminderApp`：主應用邏輯
  - `monitor_mouse()`：滑鼠監測線程
  - `update_display()`：終端顯示線程
  - `alert_display()`：警告顯示線程
  - `show_alert()`：顯示提醒視窗

## 貢獻

歡迎提交 Issue 和 Pull Request！

## 許可證

本專案採用 MIT License - 詳見 [LICENSE](LICENSE) 檔案

## 作者

**Barney Huang** (LegendaryBarney)

---

**健康提示**：長時間工作應定時活動，熬夜對身體有害，請好好休息！💪