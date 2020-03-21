#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
import sys
from TouchStyle import *
from PyQt4.Qt import QGridLayout
from CommonButtons import ShadowButton


class FtcGuiApplication(TouchApplication):
    def __init__(self, args):
        TouchApplication.__init__(self, args)

        # create the empty main window
        self.w = TouchWindow("Run JetsonEV")

        self.relative_path = os.path.dirname(os.path.realpath(__file__))
        self.script = os.path.join(self.relative_path, 'Run_car.py')
        self.grid = QGridLayout()
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.stdoutReady)
        self.process.readyReadStandardError.connect(self.stderrReady)

        self.play_btn = ShadowButton(os.path.join(self.relative_path, 'start'))
        self.play_btn.setText("Start")
        self.play_btn.clicked.connect(self.start_script)
        self.grid.addWidget(self.play_btn, 0, 0, 1, 1)
        self.grid.setColumnStretch(0, 1.25)

        self.imu_box = QCheckBox('IMU')
        self.imu_box.setChecked(True)
        self.camera_box = QCheckBox('Cam')
        self.camera_box.setChecked(False)
        self.lidar_box = QCheckBox('Lidar')
        self.lidar_box.setChecked(False)
        self.grid.addWidget(self.imu_box, 0, 1, 1, 1)
        self.grid.setColumnStretch(1, 1)
        self.grid.addWidget(self.camera_box, 0, 2, 1, 1)
        self.grid.setColumnStretch(2, 1)
        self.grid.addWidget(self.lidar_box, 0, 3, 1, 1)
        self.grid.setColumnStretch(3, 1.5)
        self.grid.setAlignment(Qt.AlignCenter)

        self.stop_btn = ShadowButton(os.path.join(self.relative_path, 'stop'))
        self.stop_btn.setText("Stop")
        self.stop_btn.clicked.connect(self.stop_script)
        self.grid.addWidget(self.stop_btn, 0, 4, 1, 1)
        self.grid.setRowStretch(1, 4)

        self.console_output = QPlainTextEdit()
        self.console_output.setReadOnly(True)
        console_style = "QPlainTextEdit {" \
                        "background-color: black;" \
                        "color: white;" \
                        "}"
        self.console_output.setFocusPolicy(Qt.NoFocus)
        self.console_output.setFrameStyle(3)
        self.console_output.setStyleSheet(console_style)

        self.grid.addWidget(self.console_output, 1, 0, 1, 5)

        self.w.centralWidget.setLayout(self.grid)
        self.w.centralWidget.keyReleaseEvent = lambda event: self.filter_out_arrow_release_keys(self.w.centralWidget,
                                                                                                event)
        self.w.centralWidget.keyPressEvent = lambda event: self.filter_out_arrow_press_keys(self.w.centralWidget, event)
        self.w.keyPressEvent = lambda event: self.filter_out_arrow_press_keys(self.w, event)
        self.w.keyReleaseEvent = lambda event: self.filter_out_arrow_release_keys(self.w, event)
        self.play_btn.keyReleaseEvent = lambda event: self.filter_out_arrow_release_keys(self.play_btn, event)
        self.play_btn.keyPressEvent = lambda event: self.filter_out_arrow_press_keys(self.play_btn, event)
        self.stop_btn.keyReleaseEvent = lambda event: self.filter_out_arrow_release_keys(self.stop_btn, event)
        self.stop_btn.keyPressEvent = lambda event: self.filter_out_arrow_press_keys(self.stop_btn, event)

        self.imu_box.keyReleaseEvent = lambda event: self.filter_out_arrow_release_keys(self.imu_box, event)
        self.imu_box.keyPressEvent = lambda event: self.filter_out_arrow_press_keys(self.imu_box, event)
        self.camera_box.keyReleaseEvent = lambda event: self.filter_out_arrow_release_keys(self.camera_box, event)
        self.camera_box.keyPressEvent = lambda event: self.filter_out_arrow_press_keys(self.camera_box, event)
        self.lidar_box.keyReleaseEvent = lambda event: self.filter_out_arrow_release_keys(self.lidar_box, event)
        self.lidar_box.keyPressEvent = lambda event: self.filter_out_arrow_press_keys(self.lidar_box, event)

        self.w.show()
        self.exec_()
 
    def start_script(self):
        flags = ['-u', self.script]
        if self.imu_box.isChecked():
            flags.extend(['--enable-imu'])
        if self.lidar_box.isChecked():
            flags.extend(['--enable-lidar'])
        if self.camera_box.isChecked():
            flags.extend(['--enable-camera'])
        self.process.start('python3', flags)

    def stop_script(self):
        self.process.terminate()

    def fwd_output(self, text):
        self.console_output.appendPlainText(text)
        cursor = self.console_output.textCursor()
        cursor.movePosition(cursor.End)

    def stdoutReady(self):
        text = str(self.process.readAllStandardOutput(), encoding='utf8')
        self.fwd_output(text)

    def stderrReady(self):
        text = str(self.process.readAllStandardError(), encoding='utf8')
        self.fwd_output(text)

    def filter_out_arrow_release_keys(self, widget, event):
        if event.key() == Qt.Key_Up:
            self.console_output.verticalScrollBar().triggerAction(QAbstractSlider.SliderSingleStepSub)
        elif event.key() == Qt.Key_Down:
            self.console_output.verticalScrollBar().triggerAction(QAbstractSlider.SliderSingleStepAdd)
        else:
            type(widget).keyReleaseEvent(widget, event)

    def filter_out_arrow_press_keys(self, widget, event):
        if event.key() == Qt.Key_Up:
            self.console_output.verticalScrollBar().triggerAction(QAbstractSlider.SliderSingleStepSub)
        elif event.key() == Qt.Key_Down:
            self.console_output.verticalScrollBar().triggerAction(QAbstractSlider.SliderSingleStepAdd)
        else:
            type(widget).keyPressEvent(widget, event)


if __name__ == "__main__":
    FtcGuiApplication(sys.argv)
