from PyQt4.QtCore import *
from PyQt4.QtGui import *
from QNumpySocket import NumpySocket
from plotTypes import ScatterPlot


class LidarWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.plot = ScatterPlot(label="Lidar")
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.plot)
        self.layout().setSpacing(0)
        self.connected = False

    def connect(self, port, ip="localhost"):
        if self.connected:
            return
        self.socket = NumpySocket(tcp_ip=ip, tcp_port=port)
        self.socket_thread = QThread()
        self.socket.moveToThread(self.socket_thread)
        self.socket_thread.started.connect(self.socket.recieve_data)
        self.socket.new_data.connect(self.plot.queue_new_values)
        self.socket_thread.start()
        self.connected = True

    def shutdown(self):
        try:
            self.socket.shut_down()
        except:
            pass
        self.connected = False