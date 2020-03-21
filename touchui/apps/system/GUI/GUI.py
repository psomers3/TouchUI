#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
import sys, os, socket
from subprocess import call
from TouchStyle import *
from CommonButtons import ShadowButton


class FtcGuiApplication(TouchApplication):
    def __init__(self, args):
        TouchApplication.__init__(self, args)

        # create the empty main window
        self.w = TouchWindow("Launch Normal GUI")

        self.vbox = QVBoxLayout()

        self.vbox.addStretch()

        self.launch_gui_btn = ShadowButton(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'icon'))
        self.launch_gui_btn.setText("Launch GUI")
        self.launch_gui_btn.clicked.connect(self.launch_gui)
        self.vbox.addWidget(self.launch_gui_btn)

        self.vbox.addStretch()

        self.w.centralWidget.setLayout(self.vbox)

        self.w.show()
        self.exec_()        
 
    def launch_gui(self):
        print("launch gui")
        notify_launcher("Launching Gui ...")
        call(["sudo", "systemctl", "start", "gdm3.service"])


if __name__ == "__main__":
    FtcGuiApplication(sys.argv)
