from PyQt4.QtCore import *
from PyQt4.QtGui import *
from QDataSocket import QDataSocket
from plotTypes import CurvePlot
import pyqtgraph as pg


class IMUWidget(QWidget):
    def __init__(self):
        super().__init__()
        tabs = QTabWidget()

        self.accel = CurvePlot(num_curves=3, label="Accelerometer")
        self.accel.plot.setYRange(-2, 2)

        self.gyro = CurvePlot(num_curves=3, label="Gyroscope")
        self.mag = CurvePlot(num_curves=3, label="Magnetometer")
        tabs.addTab(self.accel, "ACCEL")
        tabs.addTab(self.gyro, "GYRO")
        tabs.addTab(self.mag, "MAG")
        tabs.setStyleSheet('QTabBar::tab:selected { color: red; }')
        #tabs.setStyleSheet('QTabBar::tab { font-size: 10pt}')

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(tabs)
        self.layout().setSpacing(0)
        self.connected = False

    def start(self, port, ip="localhost"):
        if self.connected:
            return
        self.socket = QDataSocket(tcp_ip=ip, tcp_port=port)
        self.socket_thread = QThread()
        self.socket.moveToThread(self.socket_thread)
        self.socket_thread.started.connect(self.socket.start)
        self.socket.new_data.connect(self.disperse_values)
        self.socket_thread.start()
        self.connected = True

    def shutdown(self):
        try:
            self.socket.stop()
        except:
            pass
        self.connected = False

    def disperse_values(self, new_values):
        accel_data = {'data': new_values[0]['accel']}
        gyro_data = {'data': new_values[0]['gyro']}
        # mag_data = {'data': new_values[0]['mag']}
        self.accel.queue_new_values((accel_data, new_values[1]))
        self.gyro.queue_new_values((gyro_data, new_values[1]))
        # self.mag.queue_new_values((mag_data, new_values[1]))
