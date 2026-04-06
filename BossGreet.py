import tkinter as tk
from tkinter import messagebox
import threading
import time
import json
import os
import ctypes
from pynput import keyboard
from pynput.keyboard import Controller, Key, KeyCode

CONFIG_FILE = "boss_config.json"


# -------------------- Windows API 强力切换英文布局 --------------------
def force_english_layout():
    """
    强制当前活动窗口切换到美国英语布局 (0x409)
    """
    try:
        # 获取当前获得焦点的窗口（即用户准备输入的聊天框窗口）
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        # 加载并激活美国英语布局
        english_layout = ctypes.windll.user32.LoadKeyboardLayoutW("00000409", 1)
        # 向该窗口发送布局更改请求消息 (WM_INPUTLANGCHANGEREQUEST = 0x50)
        ctypes.windll.user32.PostMessageA(hwnd, 0x0050, 0, english_layout)
    except Exception as e:
        print(f"输入法转换异常: {e}")


# -------------------- 机器人核心逻辑 --------------------
class BossBot:
    def __init__(self):
        self.keyboard_ctrl = Controller()
        self.is_executing = False
        self.stop_requested = False
        self.listener = None

        self.default_data = {
            "greeting_lines": ["请更改打招呼内容"],
            "delay_time": 1.5,
            "hotkey_names": ["f2"]
        }
        self.config = self.init_config()
        self.current_pressed_keys = set()

    def init_config(self):
        if not os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.default_data, f, ensure_ascii=False, indent=4)
            return self.default_data
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if "hotkey_names" not in data: data["hotkey_names"] = ["f2"]
                return data
        except:
            return self.default_data

    def save_config_file(self, lines, delay, hotkeys):
        self.config = {
            "greeting_lines": lines,
            "delay_time": delay,
            "hotkey_names": hotkeys
        }
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)

    def execute_greeting(self):
        """【原有逻辑锁死：严禁改动】"""
        self.is_executing = True
        self.stop_requested = False
        try:
            for line in self.config["greeting_lines"]:
                if self.stop_requested: break
                # 逐字键入
                for char in line:
                    if self.stop_requested: break
                    self.keyboard_ctrl.type(char)
                    time.sleep(0.02)
                if self.stop_requested: break
                self.keyboard_ctrl.tap(Key.enter)
                time.sleep(self.config["delay_time"])
        finally:
            self.is_executing = False


# -------------------- GUI 界面 (双框版) --------------------
class App:
    def __init__(self, root):
        self.root = root
        self.bot = BossBot()
        self.is_listening = False
        self.is_recording = False
        self.recorded_keys = set()

        self.root.title("Boss 自动打招呼 (触发即切英文版)")
        self.root.attributes("-topmost", True)
        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=5, fill=tk.BOTH)

        # 生效框
        tk.Label(main_frame, text="[ 生效中 (只读) ]", fg="gray").grid(row=0, column=0, sticky="w")
        self.history_area = tk.Text(main_frame, height=8, width=35, bg="#f4f4f4", state=tk.DISABLED)
        self.history_area.grid(row=1, column=0, padx=5)

        # 编辑框
        tk.Label(main_frame, text="[ 编辑区 ]", fg="blue").grid(row=0, column=1, sticky="w")
        self.edit_area = tk.Text(main_frame, height=8, width=35)
        self.edit_area.grid(row=1, column=1, padx=5)

        self.refresh_history_display()

        cfg_frame = tk.Frame(self.root)
        cfg_frame.pack(pady=5)
        tk.Label(cfg_frame, text="延时(s):").grid(row=0, column=0)
        self.delay_ent = tk.Entry(cfg_frame, width=8)
        self.delay_ent.insert(0, str(self.bot.config["delay_time"]))
        self.delay_ent.grid(row=0, column=1, padx=5)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="💾 保存编辑", bg="#BBDEFB", width=12, command=self.save_and_refresh).pack(
            side=tk.LEFT, padx=5)
        self.prep_btn = tk.Button(btn_frame, text="准备开始自动打招呼", bg="#C8E6C9", width=20,
                                  command=self.toggle_listening)
        self.prep_btn.pack(side=tk.LEFT, padx=5)
        self.hk_btn = tk.Button(btn_frame, text="刷新快捷键", bg="#FFF9C4", width=12,
                                command=self.start_recording_hotkey)
        self.hk_btn.pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(self.root, text="状态: 停止", fg="#757575", font=("Arial", 10, "bold"))
        self.status_label.pack(pady=2)

        hk_str = " + ".join(self.bot.config['hotkey_names']).upper()
        self.current_hk_display = tk.Label(self.root, text=f"当前快捷键: {hk_str}", fg="blue")
        self.current_hk_display.pack()

        tk.Label(self.root, text="[ 逻辑 ] : 按下快捷键瞬间即强制切英文；ESC 终止发送", fg="#D32F2F",
                 font=("Arial", 9)).pack(pady=5)

    def refresh_history_display(self):
        self.history_area.config(state=tk.NORMAL)
        self.history_area.delete("1.0", tk.END)
        self.history_area.insert(tk.END, "\n".join(self.bot.config["greeting_lines"]))
        self.history_area.config(state=tk.DISABLED)

    def save_and_refresh(self):
        lines = self.edit_area.get("1.0", tk.END).strip().split("\n")
        lines = [l.strip() for l in lines if l.strip()]
        try:
            delay = float(self.delay_ent.get())
            self.bot.save_config_file(lines, delay, self.bot.config["hotkey_names"])
            self.refresh_history_display()
            messagebox.showinfo("成功", "JSON已更新")
        except:
            messagebox.showerror("错误", "参数有误")

    def toggle_listening(self):
        if not self.is_listening:
            self.is_listening = True
            self.prep_btn.config(text="停止监听", bg="#FFCDD2")
            hk_text = " + ".join(self.bot.config['hotkey_names']).upper()
            self.status_label.config(text=f"监听中，按 {hk_text} 开始自动打招呼", fg="#2E7D32")
            self.bot.listener = keyboard.Listener(on_press=self.on_trigger_press, on_release=self.on_trigger_release)
            self.bot.listener.start()
        else:
            self.is_listening = False
            if self.bot.listener: self.bot.listener.stop()
            self.prep_btn.config(text="准备开始自动打招呼", bg="#C8E6C9")
            self.status_label.config(text="状态: 停止", fg="#757575")

    def start_recording_hotkey(self):
        self.is_recording = True
        self.recorded_keys = set()
        self.hk_btn.config(text="请按键...", relief=tk.SUNKEN)
        self.recorder = keyboard.Listener(on_press=self.record_press, on_release=self.record_release)
        self.recorder.start()

    def record_press(self, key):
        self.recorded_keys.add(self.get_key_str(key))

    def record_release(self, key):
        if self.recorded_keys:
            new_hks = list(self.recorded_keys)
            self.bot.config["hotkey_names"] = new_hks
            self.bot.save_config_file(self.bot.config["greeting_lines"], float(self.delay_ent.get()), new_hks)
            self.current_hk_display.config(text=f"当前快捷键: {' + '.join(new_hks).upper()}")
            messagebox.showinfo("成功", "快捷键已保存")
        self.is_recording = False
        self.hk_btn.config(text="刷新快捷键", relief=tk.RAISED)
        self.recorder.stop()
        return False

    def on_trigger_press(self, key):
        k_name = self.get_key_str(key)
        self.bot.current_pressed_keys.add(k_name)
        target_keys = set(self.bot.config["hotkey_names"])

        # --- 核心变动：检测到快捷键按下的瞬间，立即执行强制切换英文 ---
        if target_keys.issubset(self.bot.current_pressed_keys):
            force_english_layout()  # 执行API切换
            if not self.bot.is_executing:
                # 开启线程执行原有逻辑
                threading.Thread(target=self.bot.execute_greeting, daemon=True).start()

        if key == keyboard.Key.esc:
            self.bot.stop_requested = True

    def on_trigger_release(self, key):
        k_name = self.get_key_str(key)
        if k_name in self.bot.current_pressed_keys:
            self.bot.current_pressed_keys.remove(k_name)

    def get_key_str(self, key):
        if isinstance(key, keyboard.Key):
            return key.name
        elif isinstance(key, keyboard.KeyCode):
            if key.char: return key.char.lower()
            return str(key.vk)
        return str(key)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()