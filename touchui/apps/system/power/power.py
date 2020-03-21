#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
import sys, os, socket
from subprocess import call
from CommonButtons import ShadowButton
from TouchStyle import *


class FtcGuiApplication(TouchApplication):
    def __init__(self, args):
        TouchApplication.__init__(self, args)

        # create the empty main window
        self.w = TouchWindow("Power")

        self.vbox = QVBoxLayout()

        self.vbox.addStretch()

        self.poweroff = ShadowButton(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'powerdown'))
        self.poweroff.setText("Power off")
        self.poweroff.clicked.connect(self.on_poweroff)
        self.vbox.addWidget(self.poweroff)

        self.vbox.addStretch()

        self.reboot = ShadowButton(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'reboot'))
        self.reboot.setText("Reboot")
        self.reboot.clicked.connect(self.on_reboot)
        self.vbox.addWidget(self.reboot)

        self.vbox.addStretch()

        self.w.centralWidget.setLayout(self.vbox)

        self.w.show()
        self.exec_()        
 
    def on_poweroff(self):
        print("poweroff")
        notify_launcher("Shutting down ...")
        call(["sudo", "poweroff"])

    def on_reboot(self):
        print("reboot")
        notify_launcher("Rebooting ...")
        call(["sudo", "reboot"])


if __name__ == "__main__":
    FtcGuiApplication(sys.argv)
