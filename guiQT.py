#!/usr/bin/python3

import sys
import tempfile
import subprocess
import time
from random import randint
import urllib.request
from PyQt5 import QtWidgets, QtGui
#from PyQt5.QtCore import QObject,QThread, pyqtSigna
#from mainwindow import Ui_MainWindow
MidiKey=0
MidiValue=0
MidiChannel=0



class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        global MidiKey
        global MidiValue
        global MidiChannel

        self.list_widget = QtWidgets.QListWidget()
        self.button = QtWidgets.QPushButton("Start")
        #self.button.clicked.connect(self.start_download)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.list_widget)
        self.widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.widget)
        self.widget.setLayout(layout)

    def start_download(self,info):
        self.list_widget.addItem(info)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
