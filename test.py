import tkinter as tk
import threading
import time
from pynput import keyboard
from pynput.keyboard import Controller, Key, KeyCode

# -------------------- 自动打招呼逻辑 --------------------
COMBINATION = {Key.f2}
STOP_KEY = Key.esc
current_keys = set()
keyboards = Controller()
lock = threading.Lock()
is_executing = False
listener = None
delay_time = 1
# 可配置的问候内容
greeting_lines = [
    "经理,你好",
    "我是新疆大学软件工程应届生赵宇跃,主攻Java后端开发",
    "对贵司Java岗位非常感兴趣,期待进一步沟通!"
]

# 执行打招呼
def execute_greeting():
    global is_executing
    try:
        for line in greeting_lines:
            keyboards.type(line)
            keyboards.tap(Key.enter)
            time.sleep(delay_time)
    finally:
        is_executing = False

# 监听器
def on_press(key):
    global is_executing

    if key == STOP_KEY:
        print("按ESC退出监听")
        return False

    with lock:
        current_keys.add(key)

        if not is_executing and all(k in current_keys for k in COMBINATION):
            is_executing = True
            threading.Thread(target=execute_greeting).start()

def on_release(key):
    with lock:
        current_keys.discard(key)

def start_listener():
    global listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

def stop_listener():
    global listener
    if listener:
        listener.stop()

# -------------------- GUI 控制台部分 --------------------
def launch_gui():
    def update_content():
        lines = text_input.get("1.0", tk.END).strip().split("\n")
        greeting_lines.clear()
        greeting_lines.extend(lines)
        print("更新问候内容：", greeting_lines)

    def update_delay():
        global delay_time
        new_delay = delay_input.get().strip()
        delay_time = float(new_delay)
        print("更新等待时间: ",delay_time)
    def on_start():
        update_content()
        update_delay()
        start_listener()
        status_label.config(text="监听中... 按 Tab+q 自动输入")

    def on_stop():
        stop_listener()
        status_label.config(text="监听已停止")

    window = tk.Tk()
    window.title("Boss自动打招呼控制台")

    tk.Label(window, text="请输入打招呼内容：").pack()
    text_input = tk.Text(window, height=10, width=60)
    text_input.insert(tk.END, "\n".join(greeting_lines))
    text_input.pack()

    delay_frame = tk.Frame(window)
    delay_frame.pack(pady=5)

    tk.Label(delay_frame, text="请输入休息时间：").pack(side=tk.LEFT)
    delay_input = tk.Entry(delay_frame,width=30)
    delay_input.insert(0,str(delay_time))
    delay_input.pack(side=tk.LEFT,padx=5)

    tk.Button(window, text="更新配置", command=on_start).pack(pady=5)
    tk.Button(window, text="停止监听", command=on_stop).pack(pady=5)

    status_label = tk.Label(window, text="未启动")
    status_label.pack()

    window.mainloop()

# -------------------- 启动 GUI --------------------
if __name__ == '__main__':
    launch_gui()
