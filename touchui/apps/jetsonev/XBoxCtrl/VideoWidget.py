from PyQt4.QtCore import *
from PyQt4.QtGui import *
from QDataSocket import QDataSocket
import numpy as np


class VideoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.image = QGraphicsView()
        color = QColor("black")
        self.image.setBackgroundBrush(QBrush(color))
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.image)
        self.connected = False

    def start(self, port, ip="localhost"):
        if self.connected:
            return
        self.socket = QDataSocket(tcp_ip=ip, tcp_port=port)
        self.socket_thread = QThread()
        self.socket.moveToThread(self.socket_thread)
        self.socket_thread.started.connect(self.socket.start)
        self.socket.new_data.connect(self.update_image)
        self.socket_thread.start()
        self.connected = True

    def shutdown(self):
        try:
            self.socket.stop()
        except:
            pass
        self.connected = False

    def update_image(self, data):
        image = data[0]['data']
        assert (np.max(image) <= 255)
        image8 = image.astype(np.uint8, order='C', casting='unsafe')
        height, width, colors = image8.shape
        bytesPerLine = 3 * width

        image = QImage(image8.data, width, height, bytesPerLine, QImage.Format_RGB888)
        image = image.rgbSwapped()

        pixmap = QPixmap(image)
        scene = QGraphicsScene()
        scene.addPixmap(pixmap.scaled(self.image.width(), self.image.height(), Qt.KeepAspectRatio))
        self.image.setScene(scene)

