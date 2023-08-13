# -*- encoding: utf-8 -*-
"""
@File: app.py
@Description: 为游戏助手构建网站, 从而可以在移动设备中进行控制(原神游戏需要获得焦点才能接收键鼠事件)
@Author: Ray
@Time: 2023/08/09 18:54:14
"""

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from threading import Thread
import time
import queue

MAX_LINKING = 3
MAX_MESSAGE = 500

# def shutdown_server():
#     func = request.environ.get('werkzeug.server.shutdown')
#     if func is None:
#         # raise RuntimeError('Not running with the Werkzeug Server')
#         raise KeyboardInterrupt
#     func()

# def background_thread(message_queue, connected_clients):
#     while True:
#         message = message_queue.get()
#         while len(connected_clients) == 0:
#             print("无客户端连接!!!")
#             time.sleep(2)
#         for client_sid in connected_clients:
#             emit('message', {'message': message}, room=client_sid)


class WebUI(Thread):

    def __init__(self, message_handler) -> None:
        super().__init__()
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'secret!'
        socketio = SocketIO(app, ping_timeout=2)
        self.message_handler = message_handler

        # 用于存储连接的客户端
        self.connected_clients = set()
        self.close_game = None
        self.message_queue = queue.Queue()
        # self.thread = None
        # self.thread_lock = Lock()

        @app.route('/')
        def index():
            return render_template('index.html')

        @app.route('/close/')
        def close():
            if self.close_game is None:
                raise KeyboardInterrupt
            self.close_game()
            return "服务关闭!"

        @socketio.on('connect')
        def handle_connect():
            # with self.thread_lock:
            #     if self.thread is None:
            #         self.thread = socketio.start_background_task(background_thread, self.message_queue, self.connected_clients)

            if len(self.connected_clients) >= MAX_LINKING:
                # emit("message", {'message': "连接以达上限!"}, room=request.sid)
                return False
            self.connected_clients.add(request.sid)
            emit("message", {'message': f"{request.sid} 已连接!"},
                 room=request.sid)
            self.send_message(f"{request.sid} 已连接!")
            print(f"{request.sid} 已连接!")

        @socketio.on('disconnect')
        def handle_disconnect():
            self.connected_clients.discard(request.sid)
            print(f"{request.sid} 已断开!")

        @socketio.on("message")
        def handle_message(data):
            self.message_handler(data['message'])

        self.app = app
        self.socketio = socketio
        socketio.start_background_task

    def set_game_close(self, func):
        self.close_game = func

    def set_message_handler(self, message_handler=None):
        if message_handler is not None:
            self.message_handler = message_handler

        @self.socketio.on("message")
        def handle_message(data):
            self.message_handler(data['message'])

    def send_message(self, message):
        self.message_queue.put(message)
        if self.message_queue.qsize() > MAX_MESSAGE:
            try:
                self.message_queue.get_nowait()
            except queue.Empty:
                print("队列已清空!")
        temp = []
        clients_copy = self.connected_clients.copy()
        for client_sid in clients_copy:
            if client_sid in self.connected_clients:
                if not temp:
                    while not self.message_queue.empty():
                        temp.append(self.message_queue.get())
                for i in temp:
                    # self.socketio.emit('message', {'message': i}, room=client_sid)
                    self.socketio.emit('message', {'message': message})
        # self.socketio.emit('message', {'message': message})

    def run(self):
        # try:
        #     self.socketio.run(self.app, host='0.0.0.0', port=8765)
        # except KeyboardInterrupt:
        #     print("web close")
        self.socketio.run(self.app, host='0.0.0.0', port=8765)


if __name__ == '__main__':

    def f(s):
        print(f"receive {s}")

    webui = WebUI(f)
    webui.set_message_handler(f)
    webui.setDaemon(True)
    webui.start()
    time.sleep(5)
    flag = input("press message (stop to exit)\n> ")
    while True:
        if flag == "stop":
            break
        else:
            webui.send_message(flag)
        flag = input("press message (stop to exit)\n> ")
    print("exit")
