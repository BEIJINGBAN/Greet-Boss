import pyautogui
import pypinyin
import time
import sys
import pynput
import threading
from pynput.keyboard import Controller,Key, Listener,KeyCode

#点击idea左上角的缩小
# pyautogui.click(2373,30)
# time.sleep(2)

#触发打招呼的组合，可自定义
COMBINATION = {Key.f2}
#退出键
STOP_KEY = Key.esc

current_keys = set()

lock = threading.Lock()

#打招呼的内容
aa = f'经理,你好'
bb = f'我是新疆大学软件工程应届生赵宇跃,主攻Java后端开发'
cc = f'在上海已式文化科技主导留学规划系统后端开发'
dd = f'基于Spring Boot+MyBatis-Plus实现院校信息CRUD与Excel导入导出,并优化多角色聊天系统的未读消息统计;'
ee = f'在新疆丝路融创开发校招系统时,设计职业推荐模块并结合MyBatis动态SQL优化分页性能.'
ff = f'技术博客:https://blog.csdn.net/m0_73884162?type=blog'
hh = f'对贵司的Java后端开发岗位非常感兴趣,期待进一步沟通技术细节!'
keyboard = Controller ()
is_executing = False
#按键监听
def on_press(key):
    global is_executing

    if is_executing:
        return

    if key == STOP_KEY:
        print("检测到退出按键ESC，停止监听...")
        return False

    with lock:
        current_keys.add(key)

        #查看按下了什么键
        # print(f"现在按下{key}")

        if is_executing:
            return

        if all(k in current_keys for k in COMBINATION):
            t = time.asctime()
            print(f"{t} 正在执行自动打招呼...")
            is_executing = True
            threading.Thread(target=execute_geeting).start()


#按键释放事件
def  on_release(key):
    with lock:
        current_keys.discard(key)

#打招呼函数
def execute_geeting():
    global is_executing
    try:
        for greet in [aa,bb,cc,dd,ee,ff,hh]:
            keyboard.type(greet)
            keyboard.tap(Key.enter)
            time.sleep(1.5)
        print("成功执行，继续监听...")
    finally:
        is_executing = False


if __name__ == '__main__':
    print("自动打招呼脚本开始了...")
    print(f"按{COMBINATION}自动打招呼")
    print(f"按{STOP_KEY}关闭程序")

    with Listener(on_press=on_press, on_release=on_release) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            pring("\n程序被用户中断")