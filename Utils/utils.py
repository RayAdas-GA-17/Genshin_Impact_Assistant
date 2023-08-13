# -*- encoding: utf-8 -*-
"""
@File: utils.py
@Description: 游戏的IO操作, 截图, 键鼠等
@Author: Ray
@Time: 2023/08/11 17:48:48
"""

import pyautogui as pag
import win32gui as wgui
# import win32api as wapi
# import win32con as wcon
# import pydirectinput
from pyperclip import copy


def get_hwnd(title:str=None, class_name=None):
    if title is None:
        return wgui.WindowFromPoint(wgui.GetCursorPos())
    else:
        hwnd = wgui.FindWindow(class_name, title)
        return hwnd

def type_text(text):
    copy(text)
    pag.hotkey('ctrl', 'v')

# def capture():
    # # 获取主屏幕的句柄
    # hdesktop = wgui.GetDesktopWindow()

    # # 获取主屏幕的尺寸
    # width = wapi.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    # height = wapi.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)

    # # 创建设备上下文对象
    # desktop_dc = wgui.GetWindowDC(hdesktop)
    # img_dc = win32ui.CreateDCFromHandle(desktop_dc)

    # # 创建位图对象
    # mem_dc = img_dc.CreateCompatibleDC()
    # screenshot_bitmap = win32ui.CreateBitmap()
    # screenshot_bitmap.CreateCompatibleBitmap(img_dc, width, height)
    # mem_dc.SelectObject(screenshot_bitmap)

    # # 将屏幕内容复制到位图对象
    # mem_dc.BitBlt((0, 0), (width, height), img_dc, (0, 0), win32con.SRCCOPY)

    # # 保存位图到文件
    # screenshot_bitmap.SaveBitmapFile(mem_dc, filename)

    # # 清理资源
    # mem_dc.DeleteDC()
    # wgui.DeleteObject(screenshot_bitmap.GetHandle())
    # img_dc.DeleteDC()
    # wgui.ReleaseDC(hdesktop, desktop_dc)