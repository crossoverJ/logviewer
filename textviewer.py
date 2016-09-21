from PyQt4 import QtGui, QtCore

class textViewer(QtGui.QTextEdit):
    def __init__(self,parent):
        super(textViewer, self).__init__(parent)
        self.setReadOnly(True)
