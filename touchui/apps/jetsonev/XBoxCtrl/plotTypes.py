from PyQt4.QtCore import *
from PyQt4.QtGui import *
import pyqtgraph as pg
import numpy as np


class ScatterPlot(QWidget):
    def __init__(self, label=""):
        super().__init__()

        self.plot = pg.PlotWidget()

        self.plot_timer = QTimer()
        self.plot_timer.setInterval(10)
        self.plot_timer.timeout.connect(self.update_plot)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.plot)

        self.y_data = np.zeros(1000)  # used as buffers
        self.x_data = np.zeros(1000)

        self.plot_item = self.plot.getPlotItem()
        self.vb = self.plot_item.getViewBox()

        self.scatter = pg.ScatterPlotItem()
        self.origin  = pg.ScatterPlotItem()
        brush = pg.mkBrush("r")
        self.origin.setData(x=[0], y=[0], brush=brush)
        self.vb.addItem(self.origin)
        self.vb.addItem(self.scatter)

        self.plot.setXRange(-6000, 6000)
        self.plot.setYRange(-6000, 6000)
        self.plot_timer.start()

    def queue_new_values(self, new_data):
        data = new_data[0]
        self.x_data = data[:, 0]
        self.y_data = data[:, 1]

    def update_plot(self):
        self.blockSignals(True)
        self.scatter.setData(x=self.x_data, y=-self.y_data)
        self.blockSignals(False)


class CurvePlot(QWidget):
    def __init__(self, num_curves, label=""):
        super().__init__()

        self.plot = pg.PlotWidget()

        self.plot_timer = QTimer()
        self.plot_timer.setInterval(10)
        self.plot_timer.timeout.connect(self.update_plot)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.plot)
        self.num_curves = num_curves

        self.y_data = np.zeros((1000, self.num_curves))  # used as buffers
        self.x_data = np.full(1000, -1000)

        self.plot_item = self.plot.getPlotItem()
        self.vb = self.plot_item.getViewBox()
        self.curves = []
        for i in range(self.num_curves):
            pen = pg.mkPen(pg.intColor(i), width=3)
            new_curve = pg.PlotCurveItem(pen=pen)
            self.curves.append(new_curve)
            self.vb.addItem(new_curve, ignoreBounds=True)

        self.plot_item.setLabel("bottom", "time", "s")

        self.past_limit = -5  # seconds

        self.plot.setXRange(0, self.past_limit)
        self.plot.setYRange(-20, 20)
        self.last_update_time = 0
        self.plot_timer.start()

    def queue_new_values(self, new_data):
        current_time = new_data[1]
        if self.last_update_time == 0:
            time_since_last_update = 0
        else:
            time_since_last_update = current_time - self.last_update_time

        self.last_update_time = current_time

        self.x_data = np.roll(self.x_data, -1) - time_since_last_update
        self.x_data[-1] = 0

        self.y_data = np.roll(self.y_data, -1, axis=0)
        if self.num_curves == 1:
            self.y_data[-1] = new_data[0]
        else:
            for i in range(self.num_curves):
                self.y_data[-1, i] = new_data[0][i]

    def update_plot(self):
        self.blockSignals(True)

        indices = self.x_data > self.past_limit
        for i in range(self.num_curves):

            self.curves[i].setData(x=self.x_data[indices], y=self.y_data[indices, i])
        self.blockSignals(False)