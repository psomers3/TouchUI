from PyQt4.QtCore import *
from PyQt4.QtGui import *
from QDataSocket import QDataSocket
from plotTypes import CurvePlot


class SpeedWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.plot = CurvePlot(num_curves=1)
        self.plot.plot.setYRange(-0.5, 5)
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
        self.socket.new_data.connect(self.plot.queue_new_values)
        self.socket_thread.start()
        self.connected = True

    def shutdown(self):
        try:
            self.socket.stop()
        except:
            pass
        self.connected = False

