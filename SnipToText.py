import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QRect
import pytesseract


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        screen = QtWidgets.QApplication.primaryScreen()
        screen_geometry = screen.geometry()

        self.setGeometry(screen_geometry)
        self.setWindowTitle(' ')
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowOpacity(0.3)
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        print('Select area to copy to clipboard.')
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), 3))
        qp.setBrush(QtGui.QColor(128, 128, 255, 128))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.close()

        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        screen = QtWidgets.QApplication.primaryScreen()
        screenshot = screen.grabWindow(0, x1, y1, x2 - x1, y2 - y1)

        image = QtGui.QImage(screenshot)
        pixmap = QtGui.QPixmap(image)
        pixmap.save('capture.png')

        #OCR using tesseract
        extracted_text = self.extract_text('capture.png')

        #Copy extracted text to clipboard
        QtWidgets.QApplication.clipboard().setText(extracted_text)

    def extract_text(self, image_path):
        #Use pytesseract to extract text
        text = pytesseract.image_to_string(image_path)
        return text



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget()
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())
