# -*- encoding: utf-8 -*-
"""
@File: Music.py
@Description: 乐谱数据结构
@Author: Ray
@Time: 2023/08/12 14:27:01
"""

import json
import time
import os
import random

class Music:

    def __init__(self, title=None, bpm=240, music_type="num_list", notes=None, songNotes=None) -> None:
        if title is None:
            self.title = str(time.time)
        else:
            self.title = title

        # music_type ['num_list', 'key_list', 'key_str']
        if songNotes is None:
            if notes is None:
                notes = [] if 'list' in music_type else ""
            self.songNotes = {'bpm': bpm, 'type': music_type, 'notes': notes}
        else:
            self.songNotes = songNotes

    # TODO 增添其他形式
    def str2list(self):
        '''
        把 *_str 格式转换成*_list格式
        暂时为 key_str -> key_list
        '''
        new_notes = []
        flag = False
        for i in self.songNotes['notes']:
            if i not in {'(', ')'}:
                if flag:
                    new_notes[-1].append(i)
                else:
                    if i == " ":
                        new_notes.append([])
                    elif i == "/":
                        continue
                    else:
                        new_notes.append([i])
            else:
                flag = not flag
                new_notes.append([])
        self.songNotes['type'] = 'key_list'
        self.songNotes['notes'] = new_notes


    def read(self):
        pass

    def add_notes(self, notes):
        self.songNotes['notes'].append(notes)

    def save(self, path=None):
        # 去掉末尾的空
        while len(self.songNotes['notes']) > 16:
            if len(self.songNotes['notes'][-1]) == 0:
                self.songNotes['notes'].pop(-1)
            else:
                break
        if path is None:
            path = r"E:\VSCode\python_file\Game\Genshin_Impact\data\music.json"

        if os.path.exists(path):
            with open(path, encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {}

        if self.title in data:
            flag = input("乐曲已存在 覆盖(y/[n])?")
            if flag != 'y':
                return
        data[self.title] = self.songNotes
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

class SheetMusic:
    def __init__(self, sheet_path=None) -> None:
        if sheet_path is None:
            sheet_path = r"E:\VSCode\python_file\Game\Genshin_Impact\data\music.json"
        with open(sheet_path, encoding='utf-8') as f:
            sheets = json.load(f)
        
        self.sheets = {}
        for title, notes in sheets.items():
            self.sheets[title] = Music(title=title, songNotes=notes)
        
    def get_titles(self):
        return list(self.sheets.keys())
    
    def get_music(self, title=None):
        if title is not None and title not in self.sheets:
            print(f"{title} 未录入!")
            title=None
        if title is None:
            title = random.choice(self.get_titles())
        music = self.sheets[title]
        if "str" in music.songNotes['type']:
            music.str2list()
        return music
