from PyQt4 import QtGui, QtCore
import threading

class logDrawer(QtGui.QWidget):
    data_lock = threading.Lock()
    data = []
    def __init__(self,parent):
        super(logDrawer, self).__init__(parent)
        self.qp = QtGui.QPainter()
        self.lines = [[0,0],[10,10],[20,20],[30,30],[50,50],[100,100],[500,200],[0,0]]
    def paintEvent(self, e):
        self.qp.begin(self)
        self.size = self.geometry().getCoords()
        self.setbackground(self.qp,QtGui.QColor(40,30,20),self.size)
        self.drawLines(self.qp,self.size)
        self.qp.end()

    def drawLines(self,qp,size):
        pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        points = []
        for p in self.lines:
            points.append(QtCore.QPoint(p[0],p[1]))
        qp.drawPolyline(QtGui.QPolygon(points))
        pen = QtGui.QPen(QtCore.Qt.yellow, 5, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.drawPoints(QtGui.QPolygon(points))
    def setbackground(self,qp,color,size):
        qp.fillRect(0,0,size[2],size[3],color)

    def set_data(self,data):
        if self.data_lock.acquire(1):
            self.data = data
            self.data_lock.release()
            self.update()
            return True
        else:
            return False
    def get_data(self):
        if self.data_lock.acquire():
            data_copy = self.data
            self.data_lock.release()
            return data_copy
        else:
            return[[0,0]]
