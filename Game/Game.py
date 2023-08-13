# -*- encoding: utf-8 -*-
"""
@File: Game.py
@Description: 对游戏进行抽象, 添加io, 消息队列等
@Author: Ray
@Time: 2023/08/11 17:34:51
"""

from collections import Iterable
from types import FunctionType
import time
from threading import Thread
from queue import Queue
import pyautogui as pag
import sys
sys.path.append("..")
from Utils.utils import type_text, get_hwnd
import pydirectinput
from Utils.Music import SheetMusic
import win32gui as wgui


class Game(Thread):
    def __init__(self, hwnd=None) -> None:
        super().__init__()
        self.hwnd = hwnd
        self.loop_paused = False
        self.loop_stopped = False
        self.thread_stopped = False
        self.command2key = {}
        self.queue = Queue()

    def set_ui(self, ui):
        self.ui = ui

    def command_loop(self, iterator:Iterable, handler:FunctionType, **args):
        for i in iterator:
            if self.loop_stopped:
                break
            while self.loop_paused:
                time.sleep(1)

            handler(i, **args)

    def pause_loop(self):
        self.loop_paused=True

    def continue_loop(self):
        self.loop_paused=False

    def stop_loop(self):
        self.loop_stopped=True

    def stop_thread(self):
        self.thread_stopped = True

    def capture(self):
        pass

    def key_down(self, key):
        pag.keyDown(key)

    def key_up(self, key):
        pag.keyUp(key)

    def type_text(self, text):
        type_text(text)

    def mouse_click(self, x=None, y=None, button=None):
        if button is None:
            button = 'left'
        pag.click(x, y, button=button)

    def mouse_move(self, dx=0, dy=0):
        pydirectinput.moveRel(dx, dy, duration=0.5, relative=True)

    def mouse_moveTo(self, x, y):
        pag.moveTo(x,y)

    def message_receive(self, message):
        if message in ['p', "pause"]:
            self.pause_loop()
            self.message_output("已暂停!")
        elif message in ['c', 'continue']:
            self.continue_loop()
            self.message_output("继续播放!")
        elif message in ['s', 'stop', 'q', 'quit', 'terminal']:
            self.stop_loop()
            self.message_output("终止播放")
        else:
            self.queue.put(message)

    def set_message_output_func(self, func:FunctionType):
        self.message_output = func

    def music_play(self, note, delay=0.25):
        if len(note) == 0:
            time.sleep(delay)
        else:
            pag.press(note)
            time.sleep(delay)
            # for key in note:
            #     self.key_down(key)
            # time.sleep(delay)
            # for key in note:
            #     self.key_up(key)
            # time.sleep(delay/2)


    def run(self):
        # self.mouse_click()
        # self.key_down('w')
        # for _ in range(10):
        #     self.mouse_move(100, 0)
        #     time.sleep(0.01)
        # time.sleep(1)
        # self.key_up('w')
        # self.mouse_click()
        # self.mouse_click(button='right')
        # while len(self.ui.connected_clients) <= 0:
        #     print("客户端未连接!")
        #     time.sleep(1)
        time.sleep(5)
        x1, y1, x2, y2 = wgui.GetWindowRect(self.hwnd)
        self.mouse_click(x1+50, y1+50)
        while wgui.GetForegroundWindow() != self.hwnd:
            self.message_output("原神未在最上层!!! 请点击原神!!!!!")
        sheets = SheetMusic()
        self.message_output(f"乐曲: {sheets.get_titles()}")
        while not self.thread_stopped:
            self.message_output("请输入乐曲名称(quit推出)")
            title = self.queue.get()
            if title == 'quit':
                self.stop_thread()
                break
            music = sheets.get_music(title)
            if music.title != title:
                self.message_output(f"歌曲 {title} 未录入, 以随机选择 {music.title}")

            self.loop_paused = False
            self.loop_stopped = False
            self.message_output(
                "乐曲播放中, 输入p/pause暂停播放, c/continue继续播放, q/quit/s/stop终止播放")
            bpm = music.songNotes['bpm']
            delay = 60 / bpm
            self.command_loop(music.songNotes['notes'], self.music_play, delay=delay)
            self.message_output("播放已结束")




if __name__ == "__main__":
    from UI.WebUI.app import WebUI
    hwnd = get_hwnd(title="原神", class_name="UnityWndClass")
    game = Game(hwnd=hwnd)
    ui = WebUI(game.message_receive)
    ui.set_game_close(game.stop_thread)
    game.set_ui(ui)
    game.set_message_output_func(ui.send_message)
    ui.setDaemon(True)
    game.setDaemon(True)
    ui.start()
    game.start()
    command = input("input commond > ")
    while True:
        if command == "stop":
            exit(0)
        command = input("input commond > ")
    print("finished!")
