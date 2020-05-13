from PyQt4.QtCore import pyqtSignal,  QObject
from DataSocket import ReceiveSocket
import time


# a client socket
class QDataSocket(QObject):
    reconnecting = pyqtSignal()
    new_data = pyqtSignal(tuple)

    def __init__(self, tcp_port, tcp_ip='localhost'):
        super().__init__()
        self.socket = ReceiveSocket(tcp_ip=tcp_ip, tcp_port=tcp_port, handler_function=self._data_received)

    def _data_received(self, data):
        self.new_data.emit((data, time.time()))

    def start(self):
        self.socket.start()

    def stop(self):
        self.socket.stop()
