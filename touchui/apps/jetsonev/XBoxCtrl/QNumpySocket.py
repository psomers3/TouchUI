from PyQt4.QtCore import *
from PyQt4.QtGui import *
import socket
import numpy as np
from io import BytesIO
import time


# a client socket
class NumpySocket(QObject):
    reconnecting = pyqtSignal()
    new_data = pyqtSignal(tuple)

    def __init__(self, tcp_port, tcp_ip='localhost'):
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.port = tcp_port
        self.ip = tcp_ip
        self.block_size = 0
        self.is_connected = False
        self.shut_down_flag = False

    def initialize(self):
        print("initializing")
        while not self.is_connected and not self.shut_down_flag:
            try:
                self.socket.connect((self.ip, self.port))
            except Exception as e:
                # print(e)
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                time.sleep(0.001)
                continue
            print("connected on port ", self.port)
            self.is_connected = True

    def recieve_data(self):
        self.initialize()
        while self.is_connected and not self.shut_down_flag:
            toread = 4
            buf = bytearray(toread)
            view = memoryview(buf)
            while toread and not self.shut_down_flag:
                try:
                    nbytes = self.socket.recv_into(view, toread)
                except OSError:
                    continue
                view = view[nbytes:]  # slicing views is cheap
                toread -= nbytes

            toread = int.from_bytes(buf, "little")
            buf = bytearray(toread)
            view = memoryview(buf)
            while toread and not self.shut_down_flag:
                try:
                    nbytes = self.socket.recv_into(view, toread)
                except OSError:
                    continue
                view = view[nbytes:]  # slicing views is cheap
                toread -= nbytes

            as_file = BytesIO(buf)
            as_file.seek(0)
            try:
                self.new_data.emit((np.load(as_file)['data'], time.time()))
            except:
                pass

    def shut_down(self):
        self.shut_down_flag = True
        self.socket.close()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

