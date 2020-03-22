from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QThread
from GUI.NumpySocket import NumpySocket
from .plotTypes import CurvePlot


class SpeedWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.plot = CurvePlot(num_curves=1, label="Speed (m/s)")
        self.plot.plot.setYRange(-0.5, 3)
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

