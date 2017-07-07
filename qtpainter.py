#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys,os
import random
import threading
import time
import datetime
from PyQt4 import QtGui, QtCore

from logdrawer    import logDrawer
from logcollecter import logCollecter
from toolbar      import toolBar
from textviewer   import textViewer

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding) 
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
    
class Ui_MainWindow(QtGui.QMainWindow):
    def __init__(self,parent=None):
        super(Ui_MainWindow,self).__init__(parent)
        self.setWindowTitle("LogViewer")
        self.setupUi(self)
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("LogViewer"))
        MainWindow.resize(1000, 700)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(200, 100))
        self.centralWidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralWidget)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.splitter = QtGui.QSplitter(self.centralWidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.drawer = logDrawer(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.drawer.sizePolicy().hasHeightForWidth())
        self.drawer.setSizePolicy(sizePolicy)
        self.drawer.setObjectName(_fromUtf8("widget"))
        self.texter = textViewer(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.texter.sizePolicy().hasHeightForWidth())
        self.texter.setSizePolicy(sizePolicy)
        self.texter.setObjectName(_fromUtf8("textEdit"))
        self.horizontalLayout.addWidget(self.splitter)
        self.toolbar = toolBar(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolbar.sizePolicy().hasHeightForWidth())
        self.toolbar.setSizePolicy(sizePolicy)
        self.toolbar.setMinimumSize(QtCore.QSize(200, 100))
        self.toolbar.setObjectName(_fromUtf8("toolbar"))
        self.splitter.raise_()
        self.splitter.raise_()
        self.splitter.raise_()
        self.horizontalLayout.addWidget(self.toolbar)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralWidget)
        self.retranslateUi(MainWindow)
        #QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        
def main():
    app = QtGui.QApplication(sys.argv)
    mainWindow = Ui_MainWindow()
    #mainWindow.show()
    mainWindow.showMaximized() #最大化显示
    print app.exec_()
    mainWindow.toolbar.quit()
    sys.exit()


if __name__ == '__main__':
    main()
