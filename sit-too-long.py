#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
sit-too-long.py - 久坐提醒程式
功能：監測滑鼠移動，定時提醒使用者站起來活動
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import winsound
import pyautogui
import os
import sys
from datetime import datetime, timedelta

class SettingsDialog:
    """設定視窗"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("久坐提醒設定")
        self.root.geometry("300x200")
        self.root.resizable(False, False)
        
        # 設定視窗置中
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # 久坐時間設定
        ttk.Label(self.root, text="久坐時間 (分鐘):").pack(pady=10)
        self.sit_time = tk.StringVar(value="30")
        ttk.Entry(self.root, textvariable=self.sit_time, width=20).pack()
        
        # 休息時間設定
        ttk.Label(self.root, text="休息時間 (分鐘):").pack(pady=10)
        self.break_time = tk.StringVar(value="1")
        ttk.Entry(self.root, textvariable=self.break_time, width=20).pack()
        
        # 確認按鈕
        ttk.Button(self.root, text="開始監測", command=self.on_confirm).pack(pady=20)
        
        # 設定關閉視窗的處理
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.sit_minutes = None
        self.break_minutes = None
        
    def on_confirm(self):
        """確認按鈕點擊事件"""
        try:
            sit = int(self.sit_time.get())
            break_t = int(self.break_time.get())
            
            if sit <= 0 or break_t <= 0:
                messagebox.showerror("錯誤", "請輸入正整數")
                return
            
            self.sit_minutes = sit
            self.break_minutes = break_t
            self.root.destroy()
            
        except ValueError:
            messagebox.showerror("錯誤", "請輸入有效的數字")
    
    def on_close(self):
        """關閉視窗事件"""
        self.sit_minutes = None
        self.root.destroy()
    
    def show(self):
        """顯示視窗並等待使用者輸入"""
        self.root.mainloop()
        return self.sit_minutes, self.break_minutes

class ReminderApp:
    def __init__(self, sit_minutes, break_minutes):
        self.sit_minutes = sit_minutes
        self.break_minutes = break_minutes
        self.sit_seconds = sit_minutes * 60
        self.break_seconds = break_minutes * 60
        
        # 計時器狀態 - 簡化版本
        self.counting_down = False  # 是否在倒數中
        self.last_mouse_position = pyautogui.position()
        self.last_move_time = time.time()
        self.remaining_time = self.sit_seconds
        self.running = True
        
        # 需要顯示警告的標誌
        self.should_show_alert = False
        
        # 鎖用於線程同步
        self.lock = threading.Lock()
        
        # 啟動監測線程
        self.monitor_thread = threading.Thread(target=self.monitor_mouse, daemon=True)
        self.monitor_thread.start()
        
        # 啟動顯示線程
        self.display_thread = threading.Thread(target=self.update_display, daemon=True)
        self.display_thread.start()
        
        # 啟動警告顯示線程（獨立線程）
        self.alert_thread = threading.Thread(target=self.alert_display, daemon=True)
        self.alert_thread.start()
        
    def monitor_mouse(self):
        """監測滑鼠移動的線程"""
        
        while self.running:
            current_position = pyautogui.position()
            current_time = time.time()
            
            with self.lock:
                # 若滑鼠動了 and counting_down == False，則開始倒數
                if current_position != self.last_mouse_position:
                    if not self.counting_down:
                        self.counting_down = True
                        self.remaining_time = self.sit_seconds
                    
                    self.last_mouse_position = current_position
                    self.last_move_time = current_time
                
                # 若滑鼠未動 and 已經超過休息時間，則重設計時器
                elif (current_time - self.last_move_time) >= self.break_seconds:
                    self.counting_down = False
                    self.remaining_time = self.sit_seconds
            
            time.sleep(1)
    
    def update_display(self):
        """更新終端顯示的線程"""
        print("\n" + "="*50)
        print("久坐提醒程式執行中")
        print(f"久坐時間: {self.sit_minutes} 分鐘")
        print(f"休息時間: {self.break_minutes} 分鐘")
        print("="*50)
        
        while self.running:
            with self.lock:
                # 更新剩餘時間
                if self.counting_down:
                    self.remaining_time = max(0, self.remaining_time - 1)
                    
                    # 時間到達0時，觸發警告並重設為60秒
                    if self.remaining_time == 0:
                        self.should_show_alert = True
                        self.remaining_time = 60  # 重設為60秒以便每分鐘提醒一次
                
                current_time = time.time()
                
                # 計算累積休息時間（現在 - last_move_time）
                rest_duration = int(current_time - self.last_move_time)
                rest_min = rest_duration // 60
                rest_sec = rest_duration % 60
                rest_time_str = f"{rest_min:02d}:{rest_sec:02d}"
                
                # 格式化距離下次警示時間
                if self.counting_down:
                    minutes = self.remaining_time // 60
                    seconds = self.remaining_time % 60
                    next_alert_str = f"{minutes:02d}:{seconds:02d}"
                    status = "倒數中"
                else:
                    # 計算距離開始倒數還需多長時間
                    time_to_alert = max(0, self.break_seconds - rest_duration)
                    min_to_alert = time_to_alert // 60
                    sec_to_alert = time_to_alert % 60
                    next_alert_str = f"{min_to_alert:02d}:{sec_to_alert:02d}"
                    status = "暫停"
                
                # 獲取當前滑鼠位置
                mouse_x, mouse_y = pyautogui.position()
            
            # 在 lock 外執行 print，避免長時間占用 lock
            display = (f"\r滑鼠位置: ({mouse_x:4d}, {mouse_y:4d}) | "
                      f"狀態: {status:6s} | 下次警示: {next_alert_str} | 累積休息: {rest_time_str}")
            print(display, end="", flush=True)
            
            time.sleep(1)
    
    def alert_display(self):
        """獨立線程：持續檢查並顯示警告窗口"""
        while self.running:
            with self.lock:
                should_alert = self.should_show_alert
                if should_alert:
                    self.should_show_alert = False
            
            if should_alert:
                self.show_alert()
            
            time.sleep(0.5)  # 頻繁檢查
    
    def show_alert(self):
        """顯示提醒視窗並發出聲音"""
        # 發出系統嗶嗶聲10次
        def beep_alert():
            for i in range(10):
                if not self.running:
                    break
                winsound.Beep(800, 500)  # 頻率800Hz，持續500ms
                time.sleep(0.2)
        
        # 在獨立線程中播放聲音
        beep_thread = threading.Thread(target=beep_alert, daemon=True)
        beep_thread.start()
        
        # 創建提醒視窗
        try:
            root = tk.Tk()
            root.title("休息提醒")
            root.geometry("300x150")
            root.attributes('-topmost', True)
            
            # 設定視窗置中
            root.update_idletasks()
            width = root.winfo_width()
            height = root.winfo_height()
            x = (root.winfo_screenwidth() // 2) - (width // 2)
            y = (root.winfo_screenheight() // 2) - (height // 2)
            root.geometry(f'{width}x{height}+{x}+{y}')
            
            # 訊息標籤
            ttk.Label(
                root, 
                text=f"您已經坐了 {self.sit_minutes} 分鐘了！\n\n請站起來活動一下！",
                font=("Arial", 12)
            ).pack(pady=30)
            
            # 確認按鈕
            ttk.Button(
                root,
                text="我知道了",
                command=root.destroy
            ).pack()
            
            root.protocol("WM_DELETE_WINDOW", root.destroy)
            root.mainloop()
        except Exception as e:
            print(f"顯示提醒視窗時出錯: {e}")
    
    def stop(self):
        """停止程式"""
        self.running = False
        print("\n\n程式結束")

def main():
    """主程式"""
    print("久坐提醒程式啟動中...")
    
    # 顯示設定視窗
    settings = SettingsDialog()
    sit_minutes, break_minutes = settings.show()
    
    # 檢查使用者是否取消
    if sit_minutes is None or break_minutes is None:
        print("使用者取消設定，程式結束")
        return
    
    # 建立提醒應用程式
    app = ReminderApp(sit_minutes, break_minutes)
    
    try:
        # 保持主程式執行
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # 使用者按 Ctrl+C 結束程式
        print("\n\n正在關閉程式...")
        app.stop()
        sys.exit(0)

if __name__ == "__main__":
    main()