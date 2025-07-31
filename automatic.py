import pyautogui
import pypinyin
import time
import sys
import pynput

from pynput.keyboard import Controller,Key, Listener

def pinyin(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s

pyautogui.click(2373,30)
time.sleep(2)

#字典名
word ='material_type'
#小写转化为大写upper()，大写转化为小写 lower()，句子的第一个大写capitalize()，单词的第一个大写title()
word = word.upper()
#需要的行数
n = 6


# for i in range(1,n+1) :
vocabulary = (f'早上好中午好下午好明天好'
              f'你好'
              f'中午好'
              f'下午好')
aa = f'经理,你好'
bb = f'我是新疆大学软件工程应届生赵宇跃,主攻Java后端开发'
cc = f'在上海已式文化科技主导留学规划系统后端开发'
dd = f'基于Spring Boot+MyBatis-Plus实现院校信息CRUD与Excel导入导出,并优化多角色聊天系统的未读消息统计;'
ee = f'在新疆丝路融创开发校招系统时,设计职业推荐模块并结合MyBatis动态SQL优化分页性能.'
ff = f'技术博客:https://blog.csdn.net/m0_73884162?type=blog'
hh = f'对贵司的Java后端开发岗位非常感兴趣,期待进一步沟通技术细节!'
print(vocabulary)
keyboard = Controller ()
keyboard.type(aa)
keyboard.tap(Key.enter)
time.sleep(0.5)
keyboard.type(bb)
keyboard.tap(Key.enter)
time.sleep(0.5)
keyboard.type(cc)
keyboard.tap(Key.enter)
time.sleep(0.5)
keyboard.type(dd)
keyboard.tap(Key.enter)
time.sleep(0.5)
keyboard.type(ee)
keyboard.tap(Key.enter)
time.sleep(0.5)
keyboard.type(ff)
keyboard.tap(Key.enter)
time.sleep(0.5)
keyboard.type(hh)
keyboard.tap(Key.enter)
time.sleep(0.5)

# pyautogui.write(vocabulary,interval=0.01)
# pyautogui.press('enter')