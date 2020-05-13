from PyQt4.QtCore import *
from PyQt4.QtGui import *
from QDataSocket import QDataSocket
from plotTypes import ScatterPlot
import numpy as np


class LidarWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.plot = ScatterPlot(label="Lidar")
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.plot)
        self.layout().setSpacing(0)
        self.connected = False

    def start(self, port, ip="localhost"):
        if self.connected:
            return
        self.socket = QDataSocket(tcp_ip=ip, tcp_port=port)
        self.socket_thread = QThread()
        self.socket.moveToThread(self.socket_thread)
        self.socket_thread.started.connect(self.socket.start)
        self.socket.new_data.connect(self.recieve_data)
        self.socket_thread.start()
        self.connected = True

    def shutdown(self):
        try:
            self.socket.stop()
        except:
            pass
        self.connected = False

    def recieve_data(self, new_data):
        data = new_data[0]['data']
        self.plot.x_data = np.multiply(np.cos(np.deg2rad(data[:, 0])), data[:, 1])
        self.plot.y_data = np.multiply(np.sin(np.deg2rad(data[:, 0])), data[:, 1])